import os, sys, json, time
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import sympy as s
print(json.dumps({'pid':os.getpid(),'argv':sys.argv,'sympy':s.__version__,'seed':None}), flush=True)
d,r,t,u,v=s.symbols('d r t u v', real=True)
def probs(K):
    out=[]
    for mask in range(8):
        z=0
        for sup in range(8):
            if sup & mask == mask:
                ix=[i for i in range(3) if sup>>i&1]
                z+=(-1)**(len(ix)-mask.bit_count())*(K.extract(ix,ix).det() if ix else 1)
        out.append(s.expand(z))
    return out
K=s.Matrix([[d,r,r],[r,d,r],[r,r,d]])
P=probs(K)
for typ,x,y in [('trivial',[u,u,u],[v,v,v]),('standard',[u,-u,0],[v,-v,0])]:
    V=s.Matrix([[x[0],y[2],y[1]],[y[2],x[1],y[0]],[y[1],y[0],x[2]]])
    pt=probs(K+t*V)
    pd=[s.diff(z,t).subs(t,0).factor() for z in pt]
    pdd=[s.diff(z,t,2).subs(t,0).factor() for z in pt]
    print(typ,flush=True)
    for m in range(8): print(m,'P=',s.factor(P[m]),'D=',pd[m],'DD=',pdd[m],flush=True)
    for mon in [u*u,u*v,v*v]:
        fisher=sum(s.expand(z*z).coeff(u,s.degree(mon,u)).coeff(v,s.degree(mon,v))/p for z,p in zip(pd,P))
        logs={}
        for j in range(4):
            logs[j]=s.expand(sum(z for m,z in enumerate(pdd) if m.bit_count()==j)).coeff(u,s.degree(mon,u)).coeff(v,s.degree(mon,v))
        print(str(mon),'Fisher=',s.factor(fisher),'log_coeff=',logs,flush=True)
print('exit_code=0',flush=True)
