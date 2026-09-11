# Mede as telas como paralelogramos: direcao horizontal pela aresta superior, vertical pela lateral limpa.
from PIL import Image, ImageDraw
import numpy as np, json
im=Image.open('carol-frame.png').convert('RGBA')
a=np.asarray(im,np.float32); lum=a[...,:3].mean(-1); al=a[...,3]; H,W=lum.shape
R=range
def scan(seqs, depth=200):
    o=[];i=[]
    for seq in seqs:
        start=None; run=0; k0=0
        for k,(x,y) in enumerate(seq):
            if start is None:
                if al[y,x]>100: start=(x,y); k0=k
                continue
            if lum[y,x]<12 and al[y,x]>200: run+=1
            else:
                if run>=6: o.append(start); i.append((x,y)); break
                run=0
            if k-k0>depth: break
    return o,i
def dirv(pts):
    P=np.array(pts,float); k=max(2,len(P)//3)
    d=np.median(P[-k:],0)-np.median(P[:k],0); d/=np.linalg.norm(d); return d
SPEC={
 'right':{'top':[[(x,y) for y in R(0,300)] for x in list(R(440,510,2))+list(R(640,710,2))],
          'right':[[(x,y) for x in R(W-1,300,-1)] for y in R(150,650,4)],
          'left':[[(x,y) for x in R(280,600)] for y in R(80,150,2)],
          'bottom':[[(x,y) for y in R(900,600,-1)] for x in R(300,530,3)]},
 'left':{'top':[[(x,y) for y in R(0,400)] for x in list(R(70,130,2))+list(R(260,325,2))],
         'left':[[(x,y) for x in R(0,400)] for y in R(280,880,4)],
         'right':[[(x,y) for x in R(W-1,300,-1)] for y in R(840,960,4)],
         'bottom':[[(x,y) for y in R(H-1,700,-1)] for x in R(240,480,4)]}}
def fit(name, vert_ref):
    eo={};ei={}
    for s,seqs in SPEC[name].items():
        o,i=scan(seqs); eo[s]=o; ei[s]=i; print(f'  {name}.{s}: {len(o)} pts')
    dh=dirv(eo['top']);  dh = dh if dh[0]>0 else -dh
    dv=dirv(eo[vert_ref]); dv = dv if dv[1]>0 else -dv
    nh=np.array([-dh[1],dh[0]]); nh = nh if nh[1]>0 else -nh     # normal das horizontais
    nv=np.array([dv[1],-dv[0]]); nv = nv if nv[0]>0 else -nv     # normal das verticais
    def quad(E):
        off={s:float(np.median(np.array(p,float)@(nv if s in('left','right') else nh))) for s,p in E.items()}
        P=lambda s1,s2: np.linalg.solve(np.array([nv if s1 in('left','right') else nh, nv if s2 in('left','right') else nh]),[off[s1],off[s2]])
        return [P('left','top'),P('right','top'),P('right','bottom'),P('left','bottom')]
    return quad(ei), quad(eo)
res={}
for name,vr in [('right','right'),('left','left')]:
    s,o=fit(name,vr); res[name]={'screen':[p.tolist() for p in s],'outer':[p.tolist() for p in o]}
    wq=np.linalg.norm(s[1]-s[0]); hq=np.linalg.norm(s[3]-s[0])
    print(name,'tela',[[round(v) for v in p] for p in s],'w',round(wq),'h',round(hq),'ratio',round(hq/wq,2))
json.dump(res,open('screens.json','w'))
g=im.copy(); d=ImageDraw.Draw(g)
for n,c in [('right',(0,255,0,255)),('left',(255,60,60,255))]:
    d.polygon([tuple(p) for p in res[n]['screen']],outline=c)
    d.polygon([tuple(p) for p in res[n]['outer']],outline=(0,170,255,255))
p=Image.new('RGB',g.size,(60,60,60)); p.paste(g,(0,0),g)
p.save('/private/tmp/claude-501/-Users-gabrielhenriquenalli-Projects-emerson-fit/10445658-e1b6-4c4e-b60f-6629ff595d86/scratchpad/quads3.png')
