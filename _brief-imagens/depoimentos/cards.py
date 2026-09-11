# Monta o fundo dos cards de depoimento: foto no topo desaparecendo em preto, no padrao do site (420x738).
from PIL import Image, ImageFilter
import numpy as np, sys
W,H=420,738; FOTO=470          # altura util da foto antes do fade terminar
CACHE='/Users/gabrielhenriquenalli/.claude/image-cache/10445658-e1b6-4c4e-b60f-6629ff595d86/'
def montar(src,out,foco=0.0,brilho=1.0):
    im=Image.open(src).convert('RGB')
    s=max(W/im.width, FOTO/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=max(0,(im.width-W)//2); y=max(0,min(im.height-FOTO, int((im.height-FOTO)*foco)))
    im=im.crop((x,y,x+W,y+FOTO))
    a=np.asarray(im,np.float32)*brilho
    yy=np.arange(FOTO)[:,None,None]
    tt=np.clip((yy-140.0)/(FOTO-140.0),0,1)        # fade suave, como no card original
    fade=(1-tt)**1.5
    a=a*fade
    canvas=np.zeros((H,W,3),np.float32); canvas[:FOTO]=a
    Image.fromarray(np.clip(canvas,0,255).astype(np.uint8)).save(out,quality=88,method=6)
    print(out)
montar(CACHE+'31.png','public/wp-content/uploads/2024/11/depo-aluna-1.webp',foco=0.0)
montar(CACHE+'32.png','public/wp-content/uploads/2024/11/depo-lais.webp',foco=0.0)
montar(CACHE+'33.png','public/wp-content/uploads/2024/11/depo-veronica.webp',foco=0.0)
