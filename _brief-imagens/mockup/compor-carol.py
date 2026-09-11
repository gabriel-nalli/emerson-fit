# Coloca fotos do Emerson nas telas dos celulares da arte original, preservando moldura e sobreposicao.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, sys, json
im=Image.open('carol-frame.png').convert('RGBA'); W,H=im.size
S=json.load(open('screens.json'))
def quad(name): return [np.array(p,float) for p in S[name]['screen']]
def expand(q, m):
    """afasta cada aresta do quadrilatero em m px (para fora)"""
    c=np.mean(q,0); out=[]
    def line(p1,p2):
        d=p2-p1; d/=np.linalg.norm(d); n=np.array([-d[1],d[0]])
        if n@(p1-c)<0: n=-n
        return n, n@p1+m
    L=[line(q[0],q[1]),line(q[1],q[2]),line(q[2],q[3]),line(q[3],q[0])]   # top,right,bottom,left
    for i,j in ((3,0),(0,1),(1,2),(2,3)):
        out.append(np.linalg.solve(np.array([L[i][0],L[j][0]]),[L[i][1],L[j][1]]))
    return out
def persp(q,w,h):
    src=[(0,0),(w,0),(w,h),(0,h)]; A=[];B=[]
    for (dx,dy),(sx,sy) in zip([tuple(p) for p in q],src):
        A.append([dx,dy,1,0,0,0,-sx*dx,-sx*dy]); A.append([0,0,0,dx,dy,1,-sy*dx,-sy*dy]); B+=[sx,sy]
    return np.linalg.solve(np.array(A),np.array(B))
def dims(q): return int(np.linalg.norm(q[1]-q[0])), int(np.linalg.norm(q[3]-q[0]))
def mask_quad(q, radius_frac=0.115, blur=0.6):
    w,h=dims(q); m=Image.new('L',(w,h),0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],int(w*radius_frac),fill=255)
    return m.transform((W,H),Image.PERSPECTIVE,persp(q,w,h),Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
def tela(photo, q, dark):
    w,h=dims(q); pw,ph=photo.size; s=max(w/pw,h/ph)
    p=photo.resize((round(pw*s),round(ph*s)),Image.LANCZOS)
    p=p.crop(((p.width-w)//2,(p.height-h)//2,(p.width-w)//2+w,(p.height-h)//2+h))
    arr=np.asarray(p,np.float32)*dark
    yy,xx=np.mgrid[0:h,0:w]; r=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2)
    arr*=(1-0.32*np.clip(r-0.40,0,1))[...,None]
    arr=np.where(arr>165,165+(arr-165)*0.65,arr)
    p=Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    d=ImageDraw.Draw(p); iw,ih=int(w*0.30),int(h*0.021); ix,iy=(w-iw)//2,int(h*0.015)
    d.rounded_rectangle([ix,iy,ix+iw,iy+ih],ih//2,fill=(8,8,9))
    return p.transform((W,H),Image.PERSPECTIVE,persp(q,w,h),Image.BICUBIC)
DARK=float(sys.argv[3]) if len(sys.argv)>3 else 0.52
qr, ql = quad('right'), quad('left')
body_front = mask_quad(expand(qr,22), radius_frac=0.14, blur=0.8)   # corpo do celular da frente
canvas=im.copy()
mback=mask_quad(ql); mback=Image.fromarray(np.minimum(np.asarray(mback,np.int16),255-np.asarray(body_front,np.int16)).clip(0,255).astype(np.uint8))
canvas.paste(tela(Image.open(sys.argv[1]).convert('RGB'),ql,DARK),(0,0),mback)
canvas.paste(tela(Image.open(sys.argv[2]).convert('RGB'),qr,DARK),(0,0),mask_quad(qr))
canvas.save('mockup-carol.png')
p=Image.new('RGB',(W,H),(14,14,14)); p.paste(canvas,(0,0),canvas)
p.save('/private/tmp/claude-501/-Users-gabrielhenriquenalli-Projects-emerson-fit/10445658-e1b6-4c4e-b60f-6629ff595d86/scratchpad/mockup-carol-prev.png')
print('ok dark',DARK)
