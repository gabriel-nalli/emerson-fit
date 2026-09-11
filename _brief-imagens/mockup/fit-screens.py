# Mede as telas (retângulos rotacionados) e o contorno externo dos dois celulares da arte da Carol.
from PIL import Image
import numpy as np, json
im=Image.open('carol-frame.png').convert('RGBA'); a=np.asarray(im,np.float32); lum=a[...,:3].mean(-1); al=a[...,3]; H,W=lum.shape
def scan(pts_iter):
    """pts_iter yields sequences of (x,y) from outside inward. Returns (outer, inner) points."""
    outer=[];inner=[]
    for seq in pts_iter:
        o=None; run=0; 
        for i,(x,y) in enumerate(seq):
            if o is None:
                if al[y,x]>100: o=(x,y)
                continue
            if lum[y,x]<12 and al[y,x]>200: run+=1
            else:
                if run>=6: inner.append(seq[i-1] if False else (x,y)); break
                run=0
            if i-seq.index(o)>70: break
        if o is not None and inner and inner[-1] is not None and len(outer)<len(inner): outer.append(o)
    return outer,inner
def fit_line(pts):  # returns (nx,ny,c) with nx*x+ny*y=c (normal form) via PCA
    P=np.array(pts,float); m=P.mean(0); u,s,vt=np.linalg.svd(P-m); d=vt[0]; n=np.array([-d[1],d[0]]); return n, n@m
def inter(l1,l2):
    A=np.array([l1[0],l2[0]]); b=np.array([l1[1],l2[1]]); return np.linalg.solve(A,b)
R=range
right=dict(
 right=[[(x,y) for x in R(W-1,300,-1)] for y in R(130,700,4)],
 top=[[(x,y) for y in R(0,300)] for x in list(R(400,500,3))+list(R(645,720,3))],
 bottom=[[(x,y) for y in R(H-1,600,-1)] for x in R(520,586,3)],
 left=[[(x,y) for x in R(280,600)] for y in R(45,150,3)])
left=dict(
 left=[[(x,y) for x in R(0,400)] for y in R(260,900,4)],
 top=[[(x,y) for y in R(0,400)] for x in list(R(60,125,3))+list(R(265,330,3))],
 bottom=[[(x,y) for y in R(H-1,700,-1)] for x in R(210,500,4)],
 right=[[(x,y) for x in R(W-1,300,-1)] for y in R(820,980,4)])
out={}
for name,spec in [('right',right),('left',left)]:
    lines_o={};lines_i={}
    for side,seqs in spec.items():
        o,i=scan(seqs); print(name,side,'pts',len(o),len(i))
        lines_o[side]=fit_line(o); lines_i[side]=fit_line(i)
    def quad(L): return [inter(L['top'],L['left']).tolist(),inter(L['top'],L['right']).tolist(),inter(L['bottom'],L['right']).tolist(),inter(L['bottom'],L['left']).tolist()]
    out[name]={'screen':quad(lines_i),'outer':quad(lines_o)}
    print(name,'screen',[[round(v) for v in p] for p in out[name]['screen']]); print(name,'outer',[[round(v) for v in p] for p in out[name]['outer']])
json.dump(out,open('screens.json','w'))
# prévia dos quads
from PIL import ImageDraw
g=im.copy(); d=ImageDraw.Draw(g)
for name,c in [('right',(0,255,0,255)),('left',(255,0,0,255))]:
    d.polygon([tuple(p) for p in out[name]['screen']],outline=c); d.polygon([tuple(p) for p in out[name]['outer']],outline=(0,160,255,255))
p=Image.new('RGB',g.size,(60,60,60)); p.paste(g,(0,0),g); p.save('/private/tmp/claude-501/-Users-gabrielhenriquenalli-Projects-emerson-fit/10445658-e1b6-4c4e-b60f-6629ff595d86/scratchpad/quads.png')
