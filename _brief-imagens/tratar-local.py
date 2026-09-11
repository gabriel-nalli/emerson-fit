"""Retoque fotográfico determinístico; somente Pillow/numpy, sem síntese de detalhes.

Executar da pasta do projeto: python3 _brief-imagens/tratar-local.py
Sem --aplicar, gera candidatos em verificacao/candidatos. Originais imutáveis.
"""
from pathlib import Path
import argparse
import shutil
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BRIEF = ROOT / '_brief-imagens'
OUT = ROOT / 'public/wp-content/uploads/2024/11'
CHECK = BRIEF / 'verificacao'
WEIGHTS = np.array([.2126, .7152, .0722], dtype=np.float32)
FILES = ['ng-car12ol1.webp', 'ng-carol1-mi12ble.webp',
         'bg-biocarol13.jpg', 'bg-biocarol-mobile-1-1.webp']


def image(a):
    return Image.fromarray(np.clip(np.round(a), 0, 255).astype('uint8'))


def luminance(a):
    return a @ WEIGHTS


def bilinear(a, x, y):
    h, w = a.shape[:2]
    x = np.clip(x, 0, w-1.001); y = np.clip(y, 0, h-1.001)
    xi = x.astype(int); yi = y.astype(int)
    dx = (x-xi)[..., None]; dy = (y-yi)[..., None]
    return ((1-dy)*((1-dx)*a[yi, xi]+dx*a[yi, xi+1]) +
            dy*((1-dx)*a[yi+1, xi]+dx*a[yi+1, xi+1]))


def clean_edge(rgb, alpha, n):
    """Reduz luz residual no contorno, sem copiar cores nem textura para a borda.

    A normal da máscara define uma amostra interior, usada SOMENTE como limite
    de luminância. Atenua o excesso luminoso dos pixels originais numa faixa
    estreita; jamais aumenta brilho nem substitui o RGB pelo interior.
    A franja semitransparente recebe uma contração subpixel independente.
    """
    a = np.asarray(alpha, dtype=np.float32)/255
    binary = image((a > .5)*255)
    depth = np.zeros(a.shape, np.float32)
    mask = binary
    for _ in range(30):
        mask = mask.filter(ImageFilter.MinFilter(3))
        depth += np.asarray(mask) / 255
    smooth = np.asarray(binary.filter(ImageFilter.GaussianBlur(7)), np.float32)
    gy, gx = np.gradient(smooth)
    norm = np.maximum(np.hypot(gx, gy), .01)
    yy, xx = np.indices(a.shape, dtype=np.float32)
    ref = bilinear(rgb, xx+gx/norm*30, yy+gy/norm*30)
    ref_alpha = bilinear(a[..., None], xx+gx/norm*30, yy+gy/norm*30)[..., 0]
    excess = np.maximum(luminance(rgb)-luminance(ref)-3, 0)
    falloff = np.clip((depth-4)/22, 0, 1)
    weight = 1-falloff*falloff*(3-2*falloff)
    correction = np.minimum(excess, 140)*weight*(ref_alpha > .98)*.99
    # Smooth the exposure adjustment itself, never the skin or replacement colors.
    correction = np.asarray(image(correction).filter(ImageFilter.GaussianBlur(2)), np.float32)
    # Protect facial illumination. The main correction concerns shoulders/arms.
    fx,fy,rx,ry = (514,490,100,132) if n == 3 else (500,461,125,178)
    face = np.clip(1-(((xx-fx)/rx)**2+((yy-fy)/ry)**2),0,1)
    correction *= 1-.85*np.minimum(face*4,1)
    # Multiplicative luminance correction preserves hue and cannot clip channels
    # independently (which would create colored speckles along the jaw).
    gain = np.maximum(1-correction/np.maximum(luminance(rgb),1), .30)
    rgb *= gain[...,None]
    eroded = np.asarray(alpha.filter(ImageFilter.MinFilter(3)), np.float32)/255
    refined = np.clip((.65*eroded+.35*a-.06)/.94, 0, 1)
    return rgb, image(refined*255)


def subject(n):
    im = Image.open(BRIEF / 'recortes' / f'p{n}.png').convert('RGBA')
    rgb = np.asarray(im.convert('RGB'), np.float32)
    alpha = im.getchannel('A')
    rgb, alpha = clean_edge(rgb, alpha, n)
    # Restrained chroma denoising, retaining the source luminance and skin texture.
    low = np.asarray(image(rgb).filter(ImageFilter.GaussianBlur(.65)), np.float32)
    lum = luminance(rgb)
    rgb = lum[..., None] + .78*(rgb-lum[..., None]) + .22*(low-luminance(low)[..., None])
    rgb *= np.array([1.025, .982, 1.005], np.float32)
    lum = luminance(rgb)
    # Modest exposure lift with a protected black point, no illumination flattening.
    t = np.clip(lum/255, 0, 1)
    mapped = np.clip(((t**.84-.014)/.986)*1.045, 0, 1)*255
    rgb *= (mapped/np.maximum(lum, 1))[..., None]
    lum = luminance(rgb)
    rgb = lum[..., None] + (rgb-lum[..., None])*1.075
    result = image(rgb).convert('RGBA'); result.putalpha(alpha)
    result = result.crop(result.getbbox())
    result.save(CHECK / f'p{n}-tratado.png')
    return result


def resize_sharp(im, size):
    # Pillow RGBA resizing uses premultiplied alpha: invisible RGB cannot bleed out.
    im = im.resize(size, Image.Resampling.LANCZOS)
    a = np.asarray(im.convert('RGB'), np.float32)
    lum = luminance(a)
    low = np.asarray(image(lum).filter(ImageFilter.GaussianBlur(.85)), np.float32)
    detail = lum-low
    gate = np.clip((np.abs(detail)-1.2)/3, 0, 1)
    delta = np.clip(detail*.42*gate, -5, 5)
    # Do not sharpen the silhouette; only the opaque interior gets the detail pass.
    interior = np.asarray(im.getchannel('A').filter(ImageFilter.MinFilter(5)), np.float32)/255
    delta *= interior**4
    lo = np.asarray(image(lum).filter(ImageFilter.MinFilter(3)), np.float32)
    hi = np.asarray(image(lum).filter(ImageFilter.MaxFilter(3)), np.float32)
    target = np.clip(lum+delta, lo, hi)
    result = image(a+(target-lum)[..., None]).convert('RGBA')
    result.putalpha(im.getchannel('A'))
    return result


def background(w, h, side):
    bg = Image.open(OUT / 'sfdhsdh23sadh-1.webp').convert('L')
    bg = ImageOps.fit(bg, (w,h), method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(18))
    x = np.linspace(0,1,w)
    if side == 'left': x = 1-x
    gradient = np.clip(x/.62,0,1)**1.5
    return image(np.asarray(bg, np.float32)*.12*gradient[None,:]).convert('RGBA')


def compose(sub, size, height, cx, top, side):
    w,h = size
    sw = round(sub.width*height/sub.height)
    s = resize_sharp(sub, (sw,height))
    canvas = background(w,h,side)
    canvas.alpha_composite(s, (round(cx*w-sw/2), top))
    return canvas.convert('RGB')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--aplicar',action='store_true')
    args=parser.parse_args()
    CHECK.mkdir(exist_ok=True)
    candidates=CHECK/'candidatos'; candidates.mkdir(exist_ok=True)
    backup=CHECK/'backup'; backup.mkdir(exist_ok=True)
    for name in FILES:
        if not (backup/name).exists(): shutil.copy2(OUT/name,backup/name)
    p3,p2=subject(3),subject(2)
    # Preserve the site's layout: desktop text zones, mobile head/waist crop.
    outputs=[
        compose(p3,(1920,878),790,.70,88,'right'),
        compose(p3,(800,1884),1000,.50,1125,'right'),
        compose(p2,(1920,992),970,.30,22,'left'),
        compose(p2,(800,992),1300,.50,159,'left'),
    ]
    for name,im in zip(FILES,outputs):
        if name.endswith('.jpg'): im.save(candidates/name,quality=97,subsampling=0)
        else: im.save(candidates/name,quality=96,method=6)
        if args.aplicar: shutil.copy2(candidates/name,OUT/name)
        print(name, im.size, 'aplicado' if args.aplicar else 'candidato')
    sheet=Image.new('RGB',(1600,1000),'#111111');draw=ImageDraw.Draw(sheet)
    for i,(name,im) in enumerate(zip(FILES,outputs)):
        im=im.copy(); im.thumbnail((790,460))
        x=i%2*800;y=i//2*500
        sheet.paste(im,(x,y+30));draw.text((x+10,y+8),name,fill='white')
    sheet.save(CHECK/'depois.jpg',quality=95)


if __name__=='__main__': main()
