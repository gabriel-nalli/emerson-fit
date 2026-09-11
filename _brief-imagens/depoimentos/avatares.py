# Refaz a faixa de avatares da hero (393x175) com as fotos das tres alunas.
from PIL import Image, ImageDraw
CACHE='/Users/gabrielhenriquenalli/.claude/image-cache/10445658-e1b6-4c4e-b60f-6629ff595d86/'
W,H=393,175; R=84; ANEL=4; CENTROS=[(85,87),(196,87),(307,87)]
FOTOS=[(CACHE+'31.png',0.10,1.0),(CACHE+'32.png',0.05,1.0),(CACHE+'33.png',0.02,1.0)]
def recorte(src,foco,d):
    im=Image.open(src).convert('RGB'); s=d/min(im.width,im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-d)//2; y=min(max(0,int((im.height-d)*foco)),max(0,im.height-d))
    return im.crop((x,y,x+d,y+d))
base=Image.new('RGBA',(W,H),(0,0,0,0))
ss=4                                   # supersampling para bordas suaves
big=Image.new('RGBA',(W*ss,H*ss),(0,0,0,0))
for (cx,cy),(src,foco,br) in list(zip(CENTROS,FOTOS))[::-1]:
    d=(R-ANEL)*2*ss
    foto=recorte(src,foco,d).convert('RGBA')
    mask=Image.new('L',(d,d),0); ImageDraw.Draw(mask).ellipse([0,0,d-1,d-1],fill=255)
    anel=Image.new('RGBA',(R*2*ss,R*2*ss),(0,0,0,0))
    ImageDraw.Draw(anel).ellipse([0,0,R*2*ss-1,R*2*ss-1],fill=(255,255,255,255))
    anel.paste(foto,(ANEL*ss,ANEL*ss),mask)
    big.alpha_composite(anel,((cx-R)*ss,(cy-R)*ss))
base=big.resize((W,H),Image.LANCZOS)
base.save('public/wp-content/uploads/2024/11/depos.webp',quality=92,method=6)
base.save('_brief-imagens/depoimentos/depos.png')
print('ok',base.size)
