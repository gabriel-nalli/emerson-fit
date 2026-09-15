# Hero com a foto nova do Emerson (camisa branca, rosca com halter): recorte Vision + integracao + fades laterais.
from PIL import Image, ImageFilter, ImageChops
import numpy as np
B='_brief-imagens/hero-bg/'; V='_brief-imagens/hero-v2/'; OUT='public/wp-content/uploads/2024/11/'
exec(open(B+'integrar.py').read().split('# desktop: recorte original')[0])     # traz integrar()
cut=Image.open(V+'recorte.png').convert('RGBA'); cut=cut.crop(cut.getbbox())
# camisa branca: segura as altas-luzes antes da integracao
rgb=np.asarray(cut.convert('RGB'),np.float32); al=cut.getchannel('A')
rgb=np.where(rgb>175,175+(rgb-175)*0.62,rgb)*0.97
cut=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).convert('RGBA'); cut.putalpha(al)
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
d=integrar(tela,70,glow_amp=0.09,shadow_amp=0.45)
d=lateral(d,M,M+s.width,80)
d=d.crop(d.getbbox())
d.save(V+'desktop-emerson.png'); d.save(OUT+'ng-car12ol1-emerson.webp',quality=94,method=6)
# mobile: camada no fluxo, 800 de largura, cintura para cima
esc=780/cut.width; m,x0,x1=colocar((800,round(cut.height*esc)+10),esc,10,0)
m=lateral(integrar(m,80,glow_amp=0.09,shadow_amp=0.45),x0,x1,55)
m.save(V+'mobile-emerson.png'); m.save(OUT+'ng-carol1-mi12ble-emerson.webp',quality=94,method=6)
print('desktop',d.size,'mobile',m.size)
