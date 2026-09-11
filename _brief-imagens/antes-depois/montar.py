# Converte as 5 fotos antes/depois enviadas pelo cliente para o site.
# Imagens 1-3 já vêm com a arte "EMERSON EF" do cliente: só redimensiona/converte.
# Imagens 4-5 são colagens cruas: recebem moldura no mesmo padrão (ANTES/AGORA).
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, glob
DL=os.path.expanduser('~/Downloads'); OUT='public/wp-content/uploads/2024/11'
SRC={1:'WhatsApp Image 2026-09-08 at 18.41.35.jpeg',      # homem, 61,70 -> 64,55 (tem legenda no form)
     2:'WhatsApp Image 2026-09-08 at 18.40.47 (1).jpeg',  # poster 896x1195
     3:'WhatsApp Image 2026-09-08 at 18.40.47.jpeg',      # poster 896x1195
     4:'WhatsApp Image 2026-09-10 at 12.10.25.jpeg',      # colagem crua 1440x1440
     5:'WhatsApp Image 2026-09-10 at 20.25.31.jpeg'}      # colagem crua 1179x1472
W,H=896,1195
def font(size, want=('Heavy','Bold')):
    for path in ['/System/Library/Fonts/Avenir Next Condensed.ttc','/System/Library/Fonts/HelveticaNeue.ttc','/System/Library/Fonts/Avenir Next.ttc']:
        for i in range(0,20):
            try: f=ImageFont.truetype(path,size,index=i)
            except Exception: break
            name=' '.join(f.getname())
            if any(w in name for w in want) and 'Italic' not in name: return f
    return ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',size)
def background():
    bg=Image.new('RGB',(W,H),(20,20,20)); d=ImageDraw.Draw(bg)
    for y in range(H):  # gradiente vertical sutil
        v=int(18+14*(y/H)); d.line([(0,y),(W,y)],fill=(v,v,v+2))
    for k in range(-H,W,70):  # linhas diagonais finas ("circuito")
        d.line([(k,0),(k+H,H)],fill=(34,34,36),width=1)
    return bg.filter(ImageFilter.GaussianBlur(0.4))
def rounded(im, r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.size[0]-1,im.size[1]-1],r,fill=255)
    out=im.convert('RGBA'); out.putalpha(m); return out
def frame(photo, box_w, box_h, color):
    # corte central para a proporção da caixa
    pw,ph=photo.size; target=box_w/box_h
    if pw/ph>target: nw=int(ph*target); photo=photo.crop(((pw-nw)//2,0,(pw-nw)//2+nw,ph))
    else: nh=int(pw/target); photo=photo.crop((0,(ph-nh)//2,pw,(ph-nh)//2+nh))
    photo=photo.resize((box_w,box_h),Image.LANCZOS)
    b=8; card=Image.new('RGBA',(box_w+2*b,box_h+2*b),(0,0,0,0))
    ImageDraw.Draw(card).rounded_rectangle([0,0,card.size[0]-1,card.size[1]-1],26,fill=color)
    card.alpha_composite(rounded(photo,20),(b,b)); return card
def text_center(d, cx, y, txt, f, fill, glow=None):
    w=d.textlength(txt,font=f)
    if glow:
        for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]: d.text((cx-w/2+dx,y+dy),txt,font=f,fill=glow)
    d.text((cx-w/2,y),txt,font=f,fill=fill)
def poster(src):
    im=Image.open(src).convert('RGB'); w,h=im.size
    left=im.crop((0,0,w//2,h)); right=im.crop((w//2,0,w,h))
    bg=background().convert('RGBA'); d=ImageDraw.Draw(bg)
    fh=font(118); fl=font(74); ff=font(30); fs=font(19,('Medium','Regular','Bold'))
    # cabeçalho "EMERSON EF"
    t1,t2='EMERSON ','EF'; w1=d.textlength(t1,font=fh); w2=d.textlength(t2,font=fh); x=(W-w1-w2)/2
    d.text((x,38),t1,font=fh,fill=(255,255,255)); d.text((x+w1,38),t2,font=fh,fill=(132,250,98))
    text_center(d,W*0.27,178,'ANTES',fl,(255,255,255)); text_center(d,W*0.73,178,'AGORA',fl,(132,250,98))
    bw,bh=400,690; y0=275
    bg.alpha_composite(frame(left,bw,bh,(214,60,60,255)),(int(W*0.27-bw/2-8),y0))
    bg.alpha_composite(frame(right,bw,bh,(70,200,90,255)),(int(W*0.73-bw/2-8),y0))
    d=ImageDraw.Draw(bg)
    text_center(d,W/2,1030,'METODOLOGIA EF: RESULTADOS COMPROVADOS E MEDÍVEIS',ff,(255,255,255))
    text_center(d,W/2,1118,'CONSULTORIA ESPORTIVA DE ELITE · EMERSON EF · TRANSFORMANDO CORPOS, REESCREVENDO DESTINOS',fs,(170,170,170))
    return bg.convert('RGB')
for n,name in SRC.items():
    src=os.path.join(DL,name); im=Image.open(src).convert('RGB')
    if n>=4: im=poster(src)
    elif im.size[0]>1000: im=im.resize((1000,int(im.size[1]*1000/im.size[0])),Image.LANCZOS)
    im.save(f'{OUT}/antes-depois-{n}.webp',quality=88,method=6)
    im.save(f'_brief-imagens/antes-depois/antes-depois-{n}.png')
    print(n, im.size)
# prévia lado a lado
ims=[Image.open(f'_brief-imagens/antes-depois/antes-depois-{n}.png') for n in range(1,6)]
th=500; strip=Image.new('RGB',(sum(int(i.size[0]*th/i.size[1]) for i in ims)+40,th),(60,60,60)); x=0
for i in ims:
    r=i.resize((int(i.size[0]*th/i.size[1]),th)); strip.paste(r,(x,0)); x+=r.size[0]+10
strip.save('_brief-imagens/antes-depois/previa.jpg',quality=80); print('previa ok')
