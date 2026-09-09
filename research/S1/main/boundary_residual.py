"""Rational residual enclosures for extreme-past kernels of the fixed baseline.

Only the candidate linear solves are numerical. Their errors and infinite tails
are bounded afterward by exact rational arithmetic and the proved symbol margin.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

import mpmath as mp

Z = (F(0), F(0))
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def conj(a): return (a[0],-a[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def scale(a,s): return (a[0]*s,a[1]*s)
def norm1(a): return abs(a[0])+abs(a[1])
def mpc(a): return mp.mpc(mp.mpf(a[0].numerator)/a[0].denominator,mp.mpf(a[1].numerator)/a[1].denominator)
def encode(a): return [str(a[0]),str(a[1])]
def quantize(a,bits): return (F(int(mp.nint(a.real*2**bits)),2**bits),F(int(mp.nint(a.imag*2**bits)),2**bits))


def build(candidate,t,complement,M,bits):
    p=F(candidate['p']); a=list(map(F,candidate['a'])); b=list(map(F,candidate['b']))
    m=len(a); eps=F(candidate['uniform_margin'])
    cs=[(p,F(0))]+[(aa/2,-t*bb/2) for aa,bb in zip(a,b)]
    if complement:
        cs=[(1-p,F(0))]+[neg(c) for c in cs[1:]]
    def c(k): return cs[k] if 0<=k<=m else conj(cs[-k]) if -m<=k<0 else Z
    B=[[c(-r-1-j) for j in range(m)] for r in range(M)]
    T=mp.matrix([[mpc(c(s-r)) for s in range(M)] for r in range(M)])
    X=[[Z for j in range(m)] for r in range(M)]
    for j in range(m):
        solution=mp.lu_solve(T,mp.matrix([mpc(B[r][j]) for r in range(M)]))
        for r in range(M): X[r][j]=quantize(solution[r],bits)
    # Zero-extend X to the half-line. The full residual vanishes after M+m.
    residual=[]
    for r in range(M+m):
        row=[]
        for j in range(m):
            value=c(-r-1-j)
            for s in range(max(0,r-m),min(M,r+m+1)):
                value=sub(value,mul(c(s-r),X[s][j]))
            row.append(value)
        residual.append(row)
    b_bound=sum(norm1(x) for row in B for x in row)
    r_bound=sum(norm1(x) for row in residual for x in row)
    delta=b_bound*r_bound/eps
    BX=[[Z for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            for r in range(m): BX[i][j]=add(BX[i][j],mul(conj(B[r][i]),X[r][j]))
    corner=[[sub(c(i-j),scale(add(BX[i][j],conj(BX[j][i])),F(1,2))) for j in range(m)] for i in range(m)]
    return {'t':str(t),'complement_symbol':complement,'M':M,'dyadic_bits':bits,
            'epsilon':str(eps),'B_norm_bound':str(b_bound),'R_norm_bound':str(r_bound),
            'operator_error_upper_rational':str(delta),'operator_error_upper_float':float(delta),
            'corner_rational':[[encode(x) for x in row] for row in corner],
            'corner_float':[[[float(x[0]),float(x[1])] for x in row] for row in corner],
            'solution_dyadic':[[encode(x) for x in row] for row in X],
            'residual_rows_checked':M+m}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--M',type=int,default=48);args=parser.parse_args()
    if not 8<=args.M<=64: raise ValueError('bounded unit supports 8<=M<=64')
    started=time.time();mp.mp.dps=70
    candidate_path=Path(args.candidate);candidate=json.loads(candidate_path.read_text())
    cases=[build(candidate,t,complement,args.M,160) for t in [F(0),F(candidate['tau'])] for complement in [False,True]]
    record={'status':'RATIONAL_KERNEL_ENCLOSURES_NOT_YET_ENTROPY_CERTIFICATE','exit_status':0,'pid':os.getpid(),
            'seed':None,'randomness':'none','python':platform.python_version(),'mpmath':mp.__version__,'mp_dps':mp.mp.dps,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'candidate_sha256':hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'seconds':time.time()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'actual_cases':len(cases),'actual_residual_complex_entries':sum((c['M']+len(candidate['a']))*len(candidate['a']) for c in cases),
            'cases':cases}
    Path(args.output).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['status','pid','seconds','peak_rss_kib','actual_cases']}))
    print(json.dumps([{'t':c['t'],'complement':c['complement_symbol'],'error':c['operator_error_upper_float']} for c in cases]))


if __name__=='__main__':main()
