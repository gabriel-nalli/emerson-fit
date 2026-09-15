# Recorte do Gabriel sem tratamento de cor: so fades de transparencia nas bordas cortadas da foto.
from PIL import Image
import numpy as np
V='_brief-imagens/hero-v2/'; U='public/wp-content/uploads/2024/11/'
im=Image.open(V+'recorte-gabriel.png').convert('RGBA'); im=im.crop(im.getbbox())
a=np.asarray(im,np.float32).copy(); H,W=a.shape[:2]
xx=np.arange(W)[None,:]; yy=np.arange(H)[:,None]
direita=np.clip((W-1-xx)/150.0,0,1)**1.6      # halter cortado pela borda da foto
esquerda=np.clip(xx/70.0,0,1)**1.3            # halter da esquerda encosta na borda
baixo=np.clip((H-1-yy)/170.0,0,1)**1.4        # barra da camisa / calca some antes da faixa
a[...,3]*=direita*esquerda*baixo
out=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
out.save(V+'natural.png')
out.save(U+'ng-car12ol1-emerson.webp',lossless=True,quality=100,method=6)
out.save(U+'ng-carol1-mi12ble-emerson.webp',lossless=True,quality=100,method=6)
print('ok',out.size)
