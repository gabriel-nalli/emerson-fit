# Hero com a foto nova do Emerson (camisa branca, rosca com halter): recorte Vision + integracao + fades laterais.
from PIL import Image, ImageFilter, ImageChops
import numpy as np
B='_brief-imagens/hero-bg/'; V='_brief-imagens/hero-v2/'; OUT='public/wp-content/uploads/2024/11/'
exec(open(B+'integrar.py').read().split('# desktop: recorte original')[0])     # traz integrar()
cut=Image.open(V+'recorte-gabriel.png').convert('RGBA'); cut=cut.crop(cut.getbbox())   # recorte feito pelo Gabriel
# camisa branca: segura as altas-luzes antes da integracao
rgb=np.asarray(cut.convert('RGB'),np.float32); al=cut.getchannel('A')
rgb=np.where(rgb>160,160+(rgb-160)*0.5,rgb)*0.93          # camisa branca sem estourar
cinza=rgb.mean(-1,keepdims=True); rgb=cinza+(rgb-cinza)*0.86     # menos saturacao, casa com o fundo cinza
rgb=rgb*np.array([0.985,0.995,1.02],np.float32)                   # leve puxada fria
cut=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).convert('RGBA'); cut.putalpha(al)
def integrar2(im, fade_px, bg=(15,15,17)):
    """integracao sem halo: borda suave, light-wrap leve, sombreamento lateral, grao e sombra difusa"""
    im=im.convert('RGBA'); W,H=im.size; BGc=np.array(bg,np.float32)
    rgb=np.asarray(im.convert('RGB'),np.float32)
    a=im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
    af=np.asarray(a,np.float32)/255
    in1=np.asarray(a.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(3)),np.float32)/255
    in2=np.asarray(a.filter(ImageFilter.MinFilter(25)).filter(ImageFilter.GaussianBlur(10)),np.float32)/255
    e1=np.clip(af-in1,0,1)[...,None]; e2=np.clip(af-in2,0,1)[...,None]
    rgb=rgb*(1-0.42*e1)+BGc*0.42*e1                     # a borda recebe a cor do ambiente
    rgb=rgb*(1-0.14*e2)                                   # afunda de leve, sem contorno preto
    ys,xs=np.nonzero(af>0.5); x0,x1=xs.min(),xs.max()
    grad=0.84+0.16*np.clip((np.arange(W)-x0)/max(1,x1-x0),0,1)   # luz vem da direita, esquerda mais escura
    rgb=rgb*grad[None,:,None]
    rgb=rgb+np.random.default_rng(7).normal(0,2.6,rgb.shape).astype(np.float32)   # grao unifica com o fundo
    yy=np.arange(H)[:,None]; af=af*np.clip((H-1-yy)/fade_px,0,1)**1.2
    sujeito=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).convert('RGBA')
    sujeito.putalpha(Image.fromarray((af*255).astype(np.uint8)))
    sil=Image.fromarray((af*255).astype(np.uint8))
    sombra=Image.new('RGBA',(W,H),(0,0,0,0))
    sombra.putalpha(ImageChops.offset(sil.filter(ImageFilter.GaussianBlur(38)),-26,30).point(lambda v:int(v*0.42)))
    out=Image.new('RGBA',(W,H),(0,0,0,0)); out.alpha_composite(sombra); out.alpha_composite(sujeito)
    return out
def lateral(layer, x0, x1, largura):
    """os halteres saem cortados pela foto original: some nas bordas do sujeito"""
    a=np.asarray(layer.getchannel('A'),np.float32); W=a.shape[1]; xx=np.arange(W)[None,:]
    f=np.clip((xx-x0)/largura,0,1)*np.clip((x1-xx)/largura,0,1)
    layer.putalpha(Image.fromarray((a*f**0.8).astype(np.uint8))); return layer
def colocar(size, escala, left, top):
    W,H=size; s=cut.resize((round(cut.width*escala),round(cut.height*escala)),Image.LANCZOS)
    c=Image.new('RGBA',size,(0,0,0,0)); c.alpha_composite(s.crop((0,0,min(s.width,W-left),min(s.height,H-top))),(left,top))
    return c, left, left+s.width
# desktop: camada recortada so do sujeito (posicionada por CSS a direita, altura relativa a hero)
M=90                                                    # margem para brilho e sombra
esc=1.0; s=cut.resize((round(cut.width*esc),round(cut.height*esc)),Image.LANCZOS)
tela=Image.new('RGBA',(s.width+2*M, s.height+M),(0,0,0,0)); tela.alpha_composite(s,(M,M))
d=integrar2(tela,210)
d=lateral(d,M,M+s.width,80)
d=d.crop(d.getbbox())
d.save(V+'desktop-emerson.png'); d.save(OUT+'ng-car12ol1-emerson.webp',quality=94,method=6)
# mobile: camada no fluxo, 800 de largura, cintura para cima
esc=780/cut.width; m,x0,x1=colocar((800,round(cut.height*esc)+10),esc,10,0)
m=lateral(integrar2(m,120),x0,x1,55)
m.save(V+'mobile-emerson.png'); m.save(OUT+'ng-carol1-mi12ble-emerson.webp',quality=94,method=6)
print('desktop',d.size,'mobile',m.size)
