from PIL import Image, ImageDraw
import numpy as np, json
exec(open('fit-screens.py').read().split('R=range')[0].split('def fit_line')[0])  # reuse scan()
R=range
right=dict(
 right=[[(x,y) for x in R(W-1,300,-1)] for y in R(160,640,4)],
 top=[[(x,y) for y in R(0,300)] for x in list(R(445,500,2))+list(R(645,700,2))],
 bottom=[[(x,y) for y in R(H-1,600,-1)] for x in R(542,586,2)],
 left=[[(x,y) for x in R(280,600)] for y in R(85,148,2)])
left=dict(
 left=[[(x,y) for x in R(0,400)] for y in R(280,880,4)],
 top=[[(x,y) for y in R(0,400)] for x in list(R(75,125,2))+list(R(265,320,2))],
 bottom=[[(x,y) for y in R(H-1,700,-1)] for x in R(240,480,4)],
 right=[[(x,y) for x in R(W-1,300,-1)] for y in R(830,970,4)])
def rect_from(edges, ref, edges_off=None):
    # ângulo pela aresta de referência (PCA), demais arestas só com offset (mediana)
    P=np.array(edges[ref],float); k=len(P)//3
    a=np.median(P[:k],0); b=np.median(P[-k:],0); d=b-a; d=d/np.linalg.norm(d)
    if abs(d[1])>abs(d[0]): d=d if d[1]>0 else -d  # vertical
    n_v=np.array([d[1],-d[0]])    # normal das arestas verticais (aponta p/ +x)
    n_h=d                          # normal das arestas horizontais (aponta p/ +y)
    if n_v[0]<0: n_v=-n_v
    if n_h[1]<0: n_h=-n_h
    off={s:float(np.median(np.array((edges_off or edges)[s],float)@(n_v if s in('left','right') else n_h))) for s in edges}
    def pt(s1,s2):
        A=np.array([n_v if s1 in('left','right') else n_h, n_v if s2 in('left','right') else n_h]); return np.linalg.solve(A,[off[s1],off[s2]]).tolist()
    return dict(tl=pt('left','top'),tr=pt('right','top'),br=pt('right','bottom'),bl=pt('left','bottom'),angle=float(np.degrees(np.arctan2(n_h[0],n_h[1]))*-1),
                w=off['right']-off['left'],h=off['bottom']-off['top'],center=((np.array(pt('left','top'))+np.array(pt('right','bottom')))/2).tolist())
out={}
for name,spec,ref in [('right',right,'right'),('left',left,'left')]:
    eo={};ei={}
    for side,seqs in spec.items():
        o,i=scan(seqs); eo[side]=o; ei[side]=i
    ei_ref=dict(ei); ei_ref[ref]=eo[ref]  # ângulo pela borda externa (limpa)
    out[name]={'screen':rect_from(eo,ref,ei),'outer':rect_from(eo,ref)}
    for k in ('screen','outer'):
        r=out[name][k]; print(name,k,'angle',round(r['angle'],2),'w',round(r['w']),'h',round(r['h']),'tl',[round(v) for v in r['tl']],'br',[round(v) for v in r['br']])
json.dump(out,open('screens.json','w'))
g=im.copy(); d=ImageDraw.Draw(g)
for name,c in [('right',(0,255,0,255)),('left',(255,0,0,255))]:
    for k,col in (('screen',c),('outer',(0,160,255,255))):
        r=out[name][k]; d.polygon([tuple(r[q]) for q in ('tl','tr','br','bl')],outline=col)
p=Image.new('RGB',g.size,(60,60,60)); p.paste(g,(0,0),g); p.save('/private/tmp/claude-501/-Users-gabrielhenriquenalli-Projects-emerson-fit/10445658-e1b6-4c4e-b60f-6629ff595d86/scratchpad/quads2.png')
