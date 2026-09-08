import os,sys,json
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import sympy as s
print(json.dumps({'pid':os.getpid(),'argv':sys.argv,'sympy':s.__version__,'seed':None}),flush=True)
q=s.symbols('q',positive=True)
M=s.log((1-q*q)*(1-4*q*q)/(1+3*q*q+4*q**4))/2
L=s.log((1-q)*(1-2*q)*(1+q+2*q*q)**3/((1+q)*(1+2*q)*(1-q+2*q*q)**3))
for name,x in [('Lprime',s.diff(L,q)),('Mprime',s.diff(M,q)),('fsecond',2*s.diff(L,q)+q*s.diff(L,q,2)-s.diff(M,q,2))]:
 print(name,s.factor(x),flush=True)
print('exit_code=0')
