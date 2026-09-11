"""Trata os recortes e monta as artes no padrao visual do site."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SCR = "/private/tmp/claude-501/-Users-gabrielhenriquenalli-Projects-carol-santos-personal/17423908-3b97-4146-ba0c-18b17833bfb1/scratchpad"
UP  = "/Users/gabrielhenriquenalli/Projects/carol-santos-personal/public/wp-content/uploads/2024/11"

def flat_field(rgb, alpha, strength=0.75, radius=90):
    """Corrige iluminacao desigual (mata o reflexo do espelho e sombras chapadas)."""
    a = np.asarray(rgb).astype(np.float32)
    m = (np.asarray(alpha).astype(np.float32) / 255.0)[..., None]
    lum = a.mean(axis=2)
    # iluminacao estimada: borrao forte da luminancia, so onde ha sujeito
    li = Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(radius))
    li = np.asarray(li).astype(np.float32)[..., None]
    target = float((lum * m[..., 0]).sum() / max(m.sum(), 1))
    corrected = a * (target / np.clip(li, 8, None))
    out = a * (1 - strength) + corrected * strength
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def subject(path, bw=True, contrast=1.28, bright=0.92, sharp=1.5, flat=0.75):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    rgb, alpha = im.convert("RGB"), im.getchannel("A")
    rgb = flat_field(rgb, alpha, strength=flat)
    if bw:
        rgb = rgb.convert("L").convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    rgb = ImageEnhance.Sharpness(rgb).enhance(sharp)
    # encolhe 1px a mascara pra matar franja clara da borda
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    out = rgb.convert("RGBA"); out.putalpha(alpha)
    return out

def backdrop(w, h, darkness=0.16, blur=14):
    bg = Image.open(f"{UP}/sfdhsdh23sadh-1.webp").convert("RGB")
    r = max(w / bg.width, h / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
    bg = bg.crop((0, 0, w, h)).filter(ImageFilter.GaussianBlur(blur)).convert("L").convert("RGB")
    return Image.fromarray((np.asarray(bg).astype(np.float32) * darkness).astype(np.uint8))

def vignette_left(img, upto=0.62, power=1.5):
    """Escurece progressivamente da esquerda ate `upto` da largura (deixa espaco pro texto)."""
    w, h = img.size
    x = np.linspace(0, 1, w)
    g = np.clip(x / upto, 0, 1) ** power
    g = np.tile(g, (h, 1))[..., None]
    a = np.asarray(img).astype(np.float32) * g
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def compose(sub, W, H, scale, cx, bottom_bleed=0, darkness=0.16, upto=0.62, blur=14):
    canvas = vignette_left(backdrop(W, H, darkness, blur), upto=upto)
    th = int(H * scale)
    tw = max(1, int(sub.width * th / sub.height))
    s = sub.resize((tw, th), Image.LANCZOS)
    x = int(W * cx) - tw // 2
    y = H - th + bottom_bleed
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(s, (x, y))
    return canvas.convert("RGB")

def deband(rgb, alpha, smooth=140, strength=0.9):
    """Remove faixa vertical de reflexo: normaliza a luminancia media por coluna."""
    a = np.asarray(rgb).astype(np.float32)
    m = (np.asarray(alpha).astype(np.float32) / 255.0)
    lum = a.mean(axis=2)
    wsum = m.sum(axis=0)
    prof = (lum * m).sum(axis=0) / np.clip(wsum, 1, None)      # perfil por coluna
    valid = wsum > (m.shape[0] * 0.02)
    if valid.sum() < 10:
        return rgb
    idx = np.arange(len(prof))
    prof = np.interp(idx, idx[valid], prof[valid])             # preenche colunas vazias
    k = np.ones(smooth) / smooth
    base = np.convolve(np.pad(prof, smooth, mode="edge"), k, mode="same")[smooth:-smooth]
    gain = np.clip(base / np.clip(prof, 1, None), 0.6, 1.6)
    gain = 1 + (gain - 1) * strength
    out = a * gain[None, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def subject2(path, flat=0.5, do_deband=False, contrast=1.22, bright=0.84, sharp=1.6):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    rgb, alpha = im.convert("RGB"), im.getchannel("A")
    if do_deband:
        rgb = deband(rgb, alpha)
    rgb = flat_field(rgb, alpha, strength=flat)
    rgb = rgb.convert("L").convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    rgb = ImageEnhance.Sharpness(rgb).enhance(sharp)
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    out = rgb.convert("RGBA"); out.putalpha(alpha)
    return out

def vignette_right(img, upto=0.62, power=1.5):
    w, h = img.size
    x = np.linspace(1, 0, w)
    g = np.clip(x / upto, 0, 1) ** power
    a = np.asarray(img).astype(np.float32) * np.tile(g, (h, 1))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def compose2(sub, W, H, scale, cx, side="left", darkness=0.16, upto=0.62, blur=14, dy=0):
    bg = backdrop(W, H, darkness, blur)
    bg = vignette_left(bg, upto) if side == "right" else vignette_right(bg, upto)
    th = int(H * scale); tw = max(1, int(sub.width * th / sub.height))
    s = sub.resize((tw, th), Image.LANCZOS)
    c = bg.convert("RGBA")
    c.alpha_composite(s, (int(W * cx) - tw // 2, H - th + dy))
    return c.convert("RGB")

def subject_color(path, flat=0.3, do_deband=True, contrast=1.30, bright=0.98,
                  sat=1.12, sharp=1.7, warm=1.03):
    """Mantem a cor natural da pele; so equaliza luz e da contraste."""
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    rgb, alpha = im.convert("RGB"), im.getchannel("A")
    if do_deband:
        rgb = deband(rgb, alpha, strength=0.85)
    rgb = flat_field(rgb, alpha, strength=flat, radius=120)
    a = np.asarray(rgb).astype(np.float32)
    a[..., 0] *= warm            # leve calor na pele
    a[..., 2] *= (2 - warm)
    rgb = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    rgb = ImageEnhance.Sharpness(rgb).enhance(sharp)
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    out = rgb.convert("RGBA"); out.putalpha(alpha)
    return out
