# Integra o recorte do Emerson ao fundo escuro: feather, light-wrap, rim escuro, glow, sombra e fade inferior.
from PIL import Image, ImageFilter, ImageChops
import numpy as np
B='_brief-imagens/hero-bg/'; OUT='public/wp-content/uploads/2024/11/'; BG=np.array([14,14,16],np.float32)
def integrar(cut, fade_px, glow_amp=0.10, shadow_amp=0.55):
    im=cut.convert('RGBA'); W,H=im.size
    rgb=np.asarray(im.convert('RGB'),np.float32); a=im.getchannel('A')
    # 1) borda: erode 1px + feather 1.4px (mata o fio claro do recorte)
    a2=a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))
    af=np.asarray(a2,np.float32)/255
    # 2) distância à borda (0 na borda, 1 no interior) via erosões sucessivas
    inner=np.asarray(a2.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(4)),np.float32)/255
    inner2=np.asarray(a2.filter(ImageFilter.MinFilter(21)).filter(ImageFilter.GaussianBlur(9)),np.float32)/255
    edge=np.clip(af-inner,0,1); edge2=np.clip(af-inner2,0,1)
    # 3) light-wrap: puxa a cor da orla para o fundo escuro; rim: escurece 30% numa faixa maior
    lum=rgb.mean(-1,keepdims=True)
    rgb=rgb*(1-0.6*edge[...,None])+BG*(0.6*edge[...,None])
    rgb=rgb*(1-0.30*edge2[...,None])
    # 4) grade suave: menos altas-luzes, -6% saturação, leve frio para casar com o cinza
    gray=rgb.mean(-1,keepdims=True); rgb=gray+(rgb-gray)*0.94
    rgb=np.where(rgb>190, 190+(rgb-190)*0.75, rgb); rgb=rgb*np.array([0.985,0.99,1.01],np.float32)
    # 5) fade inferior
    yy=np.arange(H)[:,None]; fade=np.clip((H-1-yy)/fade_px,0,1)**0.8
    af=af*fade
    subject=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)).convert('RGBA'); subject.putalpha(Image.fromarray((af*255).astype(np.uint8)))
    # 6) glow ambiente (cinza claro bem difuso) + sombra difusa deslocada, ambos atrás dele
    sil=Image.fromarray((af*255).astype(np.uint8))
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); g=sil.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(70))
    glow.putalpha(g.point(lambda v:int(v*glow_amp))); glow=Image.composite(Image.new('RGBA',(W,H),(200,200,205,255)),glow,Image.new('L',(W,H),0)); glow.putalpha(g.point(lambda v:int(v*glow_amp)))
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); s=ImageChops.offset(sil.filter(ImageFilter.GaussianBlur(28)),-18,26); sh.putalpha(s.point(lambda v:int(v*shadow_amp)))
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); layer.alpha_composite(glow); layer.alpha_composite(sh); layer.alpha_composite(subject)
    return layer
# desktop: recorte original 1920x878, fade nos últimos 70px
d=integrar(Image.open(B+'emerson-desk-atual-cut.png'),70)
d.save(B+'ng-car12ol1-emerson-integrado.png'); d.save(OUT+'ng-car12ol1-emerson.webp',quality=95,method=6)
# mobile: mesmo recorte tratado, centralizado com topo em 1170 (arte 800x1884), fade 90px
W,H=800,1884; em=Image.open(B+'emerson-desk-atual-cut.png').convert('RGBA'); sub=em.crop(em.getbbox())
top=1170; k=(H-top)/sub.height; sub=sub.resize((round(sub.width*k),round(sub.height*k)),Image.LANCZOS)
canvas=Image.new('RGBA',(W,H),(0,0,0,0)); canvas.alpha_composite(sub,((W-sub.width)//2,top))
m=integrar(canvas,90)
m.save(B+'ng-carol1-mi12ble-emerson-integrado.png'); m.save(OUT+'ng-carol1-mi12ble-emerson.webp',quality=95,method=6)
for bg,lay,out in [('ng-car12ol1-fundo.png',d,'hero-desktop-1920x878.png'),('ng-carol1-mi12ble-fundo.png',m,'hero-mobile-800x1884.png')]:
    c=Image.open(B+bg).convert('RGBA'); c.alpha_composite(lay); c.convert('RGB').save('/Users/gabrielhenriquenalli/Downloads/hero-emerson/'+out)
print('ok')
