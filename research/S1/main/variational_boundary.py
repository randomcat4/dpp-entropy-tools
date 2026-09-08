"""Tighten the selected phase candidate using its already-recorded rational X."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import time
from boundary_residual import Z,add,sub,neg,conj,mul,scale,norm1,encode


def tighten(candidate,case):
    m=len(candidate['a']);M=case['M'];t=F(case['t']);eps=F(candidate['uniform_margin'])
    p=F(candidate['p']);cs=[(p,F(0))]+[(F(a)/2,-t*F(b)/2) for a,b in zip(candidate['a'],candidate['b'])]
    if case['complement_symbol']:cs=[(1-p,F(0))]+[neg(c) for c in cs[1:]]
    def c(k):return cs[k] if 0<=k<=m else conj(cs[-k]) if -m<=k<0 else Z
    X=[[tuple(map(F,x)) for x in row] for row in case['solution_dyadic']]
    R=[]
    for r in range(M+m):
        row=[]
        for j in range(m):
            value=c(-r-j-1)
            for s in range(max(0,r-m),min(M,r+m+1)):value=sub(value,mul(c(s-r),X[s][j]))
            row.append(value)
        R.append(row)
    rbound=sum(norm1(x) for row in R for x in row)
    if rbound!=F(case['R_norm_bound']):raise ArithmeticError('residual record mismatch')
    XR=[[Z for j in range(m)] for i in range(m)]
    BX=[[Z for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            for r in range(M):
                XR[i][j]=add(XR[i][j],mul(conj(X[r][i]),R[r][j]))
                BX[i][j]=add(BX[i][j],mul(conj(c(-r-i-1)),X[r][j]))
    old=[[sub(c(i-j),scale(add(BX[i][j],conj(BX[j][i])),F(1,2))) for j in range(m)] for i in range(m)]
    if [[encode(x) for x in row] for row in old]!=case['corner_rational']:raise ArithmeticError('old corner mismatch')
    corner=[[sub(old[i][j],scale(add(XR[i][j],conj(XR[j][i])),F(1,2))) for j in range(m)] for i in range(m)]
    delta=rbound*rbound/eps
    out=dict(case)
    out.update({'enclosure_method':'VARIATIONAL_RESIDUAL_SQUARED',
                'previous_operator_error_upper_rational':case['operator_error_upper_rational'],
                'operator_error_upper_rational':str(delta),'operator_error_upper_float':float(delta),
                'corner_rational':[[encode(x) for x in row] for row in corner],
                'corner_float':[[[float(x[0]),float(x[1])] for x in row] for row in corner]})
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',required=True);parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();started=time.time();cp=Path(args.candidate);ip=Path(args.input)
    candidate=json.loads(cp.read_text());record=json.loads(ip.read_text())
    out={'status':'RATIONAL_VARIATIONAL_KERNEL_ENCLOSURES_REVIEW_PENDING','exit_status':0,'pid':os.getpid(),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),
         'candidate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'python':platform.python_version(),
         'seed':None,'randomness':'none','cases':[tighten(candidate,c) for c in record['cases']]}
    out.update(seconds=time.time()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,actual_cases=len(out['cases']))
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','seconds','actual_cases']}))
    print(json.dumps([c['operator_error_upper_float'] for c in out['cases']]))


if __name__=='__main__':main()
