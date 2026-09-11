from PIL import Image, ImageFilter, ImageChops
import numpy as np, sys
sys.path.insert(0,'_brief-imagens/hero-bg')
B='_brief-imagens/hero-bg/'; OUT='public/wp-content/uploads/2024/11/'
exec(open(B+'integrar.py').read().split('# desktop: recorte original')[0].replace("BG=np.array([14,14,16],np.float32)","BG=np.array([10,10,11],np.float32)"))
def box1d(a, r, axis):
    n=a.shape[axis]; pad=[(0,0)]*a.ndim; pad[axis]=(r,r)
    ap=np.pad(a,pad,mode='edge'); c=np.cumsum(ap,axis=axis,dtype=np.float64)
    c=np.concatenate([np.zeros_like(np.take(c,[0],axis=axis)),c],axis=axis)
    hi=np.take(c,range(2*r+1,2*r+1+n),axis=axis); lo=np.take(c,range(0,n),axis=axis)
    return ((hi-lo)/(2*r+1)).astype(np.float32)
def gblur(a,r):
    for _ in range(3): a=box1d(box1d(a,r,0),r,1)
    return a
def fundo_sem(art, cut):
    a=np.asarray(art,np.float32); m=np.asarray(cut.getchannel('A').filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(3)),np.float32)/255
    known=(1-m)[...,None]; cur=a*known; w=known.copy()
    for r in (10,25,50,90):
        cb=gblur(cur,r); wb=gblur(w,r); cur=a*known+(cb/np.maximum(wb,1e-4))*(1-known); w=np.maximum(w,(wb>1e-3).astype(np.float32))
    return Image.fromarray(np.clip(cur,0,255).astype(np.uint8))
for name,src,cut,fade,outname,kw in [('sobre-desk','sobre-desk.png','sobre-desk-cut.png',60,'bg-biocarol13.jpg',dict(quality=92)),('sobre-mob','sobre-mob.png','sobre-mob-cut.png',60,'bg-biocarol-mobile-1-1.webp',dict(quality=90,method=6))]:
    art=Image.open(B+src).convert('RGB'); cut=Image.open(B+cut).convert('RGBA')
    bg=fundo_sem(art,cut); layer=integrar(cut,fade)
    final=bg.convert('RGBA'); final.alpha_composite(layer); final=final.convert('RGB')
    final.save(B+name+'-integrado.png'); final.save(OUT+outname,**kw); print(name,'ok',final.size)
