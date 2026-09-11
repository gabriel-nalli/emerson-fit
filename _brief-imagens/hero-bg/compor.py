# Hero com fundo de academia (extraído do site original da Carol, sem a Carol) + Emerson atual.
from PIL import Image, ImageFilter, ImageOps, ImageChops
import numpy as np, sys
OUT='../public/wp-content/uploads/2024/11/'
def box1d(a, r, axis):
    n=a.shape[axis]; pad=[(0,0)]*a.ndim; pad[axis]=(r,r)
    ap=np.pad(a,pad,mode='edge'); c=np.cumsum(ap,axis=axis,dtype=np.float64)
    c=np.concatenate([np.zeros_like(np.take(c,[0],axis=axis)),c],axis=axis)
    hi=np.take(c,range(2*r+1,2*r+1+n),axis=axis); lo=np.take(c,range(0,n),axis=axis)
    return ((hi-lo)/(2*r+1)).astype(np.float32)
def gblur(a, r):
    for _ in range(3): a=box1d(box1d(a,max(1,int(r*0.6)),0),max(1,int(r*0.6)),1)
    return a
def inpaint(rgb, mask, rounds=(4,8,16,32,64,64)):
    # preenchimento por difusão: convolução normalizada iterativa dentro da máscara
    a=np.asarray(rgb,np.float32); m=(np.asarray(mask,np.float32)/255.0)[...,None]
    known=1-m; cur=a*known; w=known.copy()
    for r in rounds:
        cb=gblur(cur,r); wb=gblur(w[...,:1],r)
        fill=cb/np.maximum(wb,1e-4)
        cur=a*known+fill*m; w=np.maximum(w, (wb>1e-3)*m+known)
    return Image.fromarray(np.clip(cur,0,255).astype(np.uint8))
def build(carol_png, carol_cut, emerson_cut, size, name, grow, dark, wm_region, left_cut=0, shadow=0.7):
    W,H=size
    carol=Image.open(carol_png).convert('RGB').resize(size)
    if left_cut:  # apaga a marca-d'água da Carol com rampa para preto
        ramp=np.clip((np.arange(W)-left_cut)/260.0,0,1)[None,:,None]
        carol=Image.fromarray((np.asarray(carol,np.float32)*ramp).astype(np.uint8))
    m=Image.open(carol_cut).getchannel('A').resize(size).filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(6))
    m=m.point(lambda v: 255 if v>40 else 0).filter(ImageFilter.MaxFilter(9))
    bg=inpaint(carol,m)
    bg=ImageOps.grayscale(bg).filter(ImageFilter.GaussianBlur(1.2))
    arr=np.asarray(bg,np.float32)/255
    # vinheta radial centrada no Emerson (não na silhueta da Carol) + blur extra na zona preenchida
    em0=Image.open(emerson_cut).convert('RGBA'); bx=em0.getbbox(); cx=(bx[0]+bx[2])/2; cy=(bx[1]+bx[3])/2
    yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-cx)/(W*0.36))**2+((yy-cy)/(H*0.9))**2)
    vig=np.clip(1-r,0,1)**1.6
    feather=np.asarray(m.filter(ImageFilter.GaussianBlur(75)),np.float32)/255
    arr=arr*(1-0.62*feather)            # zona preenchida vira sombra escura
    arr=arr*(1-0.45*vig)                # vinheta suave centrada no Emerson
    arr=np.clip((arr-0.03)/0.97,0,1)**1.15*dark          # escurece mantendo contraste
    bg=Image.fromarray((arr*255).astype(np.uint8)).convert('RGB')
    # marca-d'água EF: screen com a arte atual (região sem o Emerson)
    atual=Image.open(emerson_cut.replace('-cut','')).convert('RGB')
    x0,y0,x1,y1=wm_region
    wm=Image.new('RGB',size,(0,0,0)); wm.paste(atual.crop((x0,y0,x1,y1)),(x0,y0))
    bg=ImageChops.screen(bg,wm)
    em=Image.open(emerson_cut).convert('RGBA')
    bg.save(f'hero-bg/{name}-fundo.png'); em.save(f'hero-bg/{name}-emerson.png')
    if '--aplicar' in sys.argv:
        bg.save(OUT+name+'-fundo.webp',quality=90,method=6); em.save(OUT+name+'-emerson.webp',quality=95,method=6)
    out=bg.convert('RGBA'); out.alpha_composite(em); out=out.convert('RGB')
    out.save(f'hero-bg/{name}.png'); return out
d=build('hero-bg/carol-desk.png','hero-bg/carol-desk-cut.png','hero-bg/emerson-desk-atual-cut.png',(1920,878),'ng-car12ol1',31,0.62,(0,0,1000,878),left_cut=640)
mo=build('hero-bg/carol-mob.png','hero-bg/carol-mob-cut.png','hero-bg/emerson-mob-atual-cut.png',(800,1884),'ng-carol1-mi12ble',31,0.62,(0,0,800,1000),shadow=0.6)
if '--aplicar' in sys.argv:
    d.save(OUT+'ng-car12ol1.webp',quality=90,method=6); mo.save(OUT+'ng-carol1-mi12ble.webp',quality=90,method=6); print('aplicado')
# prévia
p=Image.new('RGB',(1920+420,878),(30,30,30)); p.paste(d,(0,0)); p.paste(mo.resize((373,878)),(1940,0)); p.save('hero-bg/previa.jpg',quality=82); print('previa ok')
