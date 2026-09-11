# Extrai o celular da frente como PNG isolado (tela vazada) e gera as fotos tratadas + geometria para o HTML.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json
im=Image.open('carol-frame.png').convert('RGBA'); W,H=im.size
S=json.load(open('screens.json'))
qr=[np.array(p,float) for p in S['right']['screen']]
ql=[np.array(p,float) for p in S['left']['screen']]
def expand(q,m):
    ms=m if isinstance(m,(list,tuple)) else [m]*4      # topo, direita, base, esquerda
    c=np.mean(q,0); k=[0]
    def line(p1,p2):
        d=p2-p1; d=d/np.linalg.norm(d); n=np.array([-d[1],d[0]])
        if n@(p1-c)<0: n=-n
        v=n,n@p1+ms[k[0]]; k[0]+=1; return v
    L=[line(q[0],q[1]),line(q[1],q[2]),line(q[2],q[3]),line(q[3],q[0])]
    return [np.linalg.solve(np.array([L[i][0],L[j][0]]),[L[i][1],L[j][1]]) for i,j in ((3,0),(0,1),(1,2),(2,3))]
def persp(q,w,h):
    src=[(0,0),(w,0),(w,h),(0,h)]; A=[];B=[]
    for (dx,dy),(sx,sy) in zip([tuple(p) for p in q],src):
        A.append([dx,dy,1,0,0,0,-sx*dx,-sx*dy]); A.append([0,0,0,dx,dy,1,-sy*dx,-sy*dy]); B+=[sx,sy]
    return np.linalg.solve(np.array(A),np.array(B))
def dims(q): return int(round(np.linalg.norm(q[1]-q[0]))), int(round(np.linalg.norm(q[3]-q[0])))
def mask_quad(q,rf=0.115,blur=0.6,size=(W,H)):
    w,h=dims(q); m=Image.new('L',(w,h),0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],int(w*rf),fill=255)
    return m.transform(size,Image.PERSPECTIVE,persp(q,w,h),Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
# corpo do celular da frente = alpha da arte limitado ao contorno geometrico
body=np.minimum(np.asarray(im.getchannel('A'),np.int16), np.asarray(mask_quad(expand(qr,[13,31,19,10]),rf=0.145,blur=1.0),np.int16))
screen=np.asarray(mask_quad(qr,blur=0.7),np.int16)
alpha=np.clip(body-screen,0,255).astype(np.uint8)          # corpo sem a tela (vazada)
frame=im.copy(); frame.putalpha(Image.fromarray(alpha))
bb=frame.getbbox(); frame=frame.crop(bb); frame.save('phone-frame.png')
ox,oy=bb[0],bb[1]; print('frame',frame.size,'offset',ox,oy)
# fotos tratadas no tamanho da tela
sw,sh=dims(qr)
def tratar(src,out,dark=0.52):
    p=Image.open(src).convert('RGB'); s=max(sw/p.width,sh/p.height)
    p=p.resize((round(p.width*s),round(p.height*s)),Image.LANCZOS)
    p=p.crop(((p.width-sw)//2,(p.height-sh)//2,(p.width-sw)//2+sw,(p.height-sh)//2+sh))
    a=np.asarray(p,np.float32)*dark
    yy,xx=np.mgrid[0:sh,0:sw]; r=np.sqrt(((xx-sw/2)/(sw/2))**2+((yy-sh/2)/(sh/2))**2)
    a*=(1-0.32*np.clip(r-0.40,0,1))[...,None]; a=np.where(a>165,165+(a-165)*0.65,a)
    q=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    d=ImageDraw.Draw(q); iw,ih=int(sw*0.30),int(sh*0.021); ix,iy=(sw-iw)//2,int(sh*0.015)
    d.rounded_rectangle([ix,iy,ix+iw,iy+ih],ih//2,fill=(8,8,9))
    q.save(out,quality=92,method=6); print(out,q.size)
tratar('treino-1.png','../../public/wp-content/uploads/2024/11/tela-treino-1.webp')
tratar('treino-3.png','../../public/wp-content/uploads/2024/11/tela-treino-3.webp')
frame.save('../../public/wp-content/uploads/2024/11/celular-moldura.png')
# matrizes afins: unidade(retangulo da tela) -> quad
def affine(q,w,h):
    A=np.array([[(q[1][0]-q[0][0])/w,(q[3][0]-q[0][0])/h,q[0][0]],
                [(q[1][1]-q[0][1])/w,(q[3][1]-q[0][1])/h,q[0][1]],[0,0,1]])
    return A
Af=affine(qr,sw,sh); Ab=affine(ql,*dims(ql))
# pose "tras" aplicada ao conjunto (moldura+tela): mapeia o quad da frente no quad de tras
Mswap=Ab@np.linalg.inv(affine(qr,*dims(ql)))
cfg={'stage':[W,H],'frame':{'x':ox,'y':oy,'w':frame.size[0],'h':frame.size[1]},
     'screen':{'w':sw,'h':sh,'m':[Af[0,0],Af[1,0],Af[0,1],Af[1,1],Af[0,2],Af[1,2]]},
     'swap':[Mswap[0,0],Mswap[1,0],Mswap[0,1],Mswap[1,1],Mswap[0,2],Mswap[1,2]]}
json.dump(cfg,open('mockup-cfg.json','w'),indent=1); print(json.dumps(cfg))
