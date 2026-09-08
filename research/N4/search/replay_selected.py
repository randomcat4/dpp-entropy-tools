"""Author-side 100-digit inverse-trace replay, not independent certification."""
import json, os, sys, time
from pathlib import Path
import mpmath as mp
mp.mp.dps=100
root=Path(__file__).parent
def matrix(x):return mp.matrix([[mp.mpf(float(a)) for a in row] for row in x])
def data(K,D):
    H=mp.mpf(0);F=mp.mpf(0);A=mp.mpf(0)
    for s in range(16):
        M=K.copy()
        for i in range(4):M[i,i]-=1-((s>>i)&1)
        p=(-1)**(4-s.bit_count())*mp.det(M)
        assert p>0
        H-=p*mp.log(p)
        if D is not None:
            X=M**-1*D;g=sum(X[i,i] for i in range(4));h=-sum(X[i,j]*X[j,i] for i in range(4) for j in range(4))
            F-=p*g*g;A-=p*mp.log(p)*(g*g+h)
    return H,F,A
start=time.time();results=[]
for filename in ('best_curvature.json','best_mechanism.json'):
    rec=json.loads((root/'batch1'/filename).read_text());K=matrix(rec['K'])
    for dr in rec['directions']:
        D=matrix(dr['D']);H,F,A=data(K,D);chords=[]
        for c in dr['chords']:
            t=mp.mpf(float(c['t']));gap=(data(K+t*D,None)[0]+data(K-t*D,None)[0])/2-H
            chords.append({'t_binary64_exact':str(t),'Delta_100d':str(gap)})
        results.append({'file':filename,'index':rec['index'],'direction':dr['name'],'curvature':str(F+A),'fisher':str(F),'acceleration':str(A),'chords':chords})
output={'status':'AUTHOR_HIGH_PRECISION_CHECK_ONLY','pid':os.getpid(),'mpmath':mp.__version__,'digits':100,'binary64_input_conversion':'mp.mpf(float) exactly preserves stored binary64 values','event_evaluations':4*7*16,'directional_curvature_calls':4,'entropy_evaluations':28,'results':results,'elapsed_seconds':time.time()-start,'exit_code':0}
(root/'batch1'/'selected_replay.json').write_text(json.dumps(output,indent=2));print(json.dumps(output))
