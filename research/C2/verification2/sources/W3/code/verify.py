#!/usr/bin/env python3
"""Exact certificate for I05-W3-20260909; Python standard library only.

No floating-point value is used in a proof decision. Logarithms are bounded
by rational atanh series. Run from any working directory:
    python3 code/verify.py --output-dir output
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import platform
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


def check(condition: bool, label: str) -> None:
    if not condition:
        raise ArithmeticError('FAILED: ' + label)


def dot(x, y): return sum((a*b for a,b in zip(x,y)), F(0))
def transpose(A): return [list(x) for x in zip(*A)]
def mm(A,B): return [[dot(x,y) for y in transpose(B)] for x in A]
def scale(A,t): return [[t*x for x in row] for row in A]
def add(A,B): return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def sub(A,B): return add(A,scale(B,-1))
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def trace(A): return sum((A[i][i] for i in range(len(A))), F(0))
def outer(x,y): return [[a*b for b in y] for a in x]
def cross(x,y): return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
def quad(A,x): return dot(x,[dot(row,x) for row in A])
def adj(A):
    tr=trace(A)
    e2=(tr*tr-trace(mm(A,A)))/2
    return add(sub(mm(A,A),scale(A,tr)),scale(eye(3),e2))
def det3(A): return dot(A[0],cross(A[1],A[2]))
def trprod(A,B): return trace(mm(A,B))
def vecform(x): return [x[0]**2,x[1]**2,x[2]**2,2*x[0]*x[1],2*x[0]*x[2],2*x[1]*x[2]]


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        if self.lo>self.hi: raise ValueError('inverted interval')
    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self, other): return self+(-as_interval(other))
    def __rsub__(self, other): return as_interval(other)+(-self)
    def __mul__(self, other):
        other=as_interval(other)
        z=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return Interval(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self, other):
        other=as_interval(other)
        if other.lo<=0<=other.hi: raise ZeroDivisionError('interval includes zero')
        return self*Interval(1/other.hi,1/other.lo)


def as_interval(x):
    return x if isinstance(x,Interval) else Interval(F(x),F(x))


def log_interval(x: F, terms: int=32) -> Interval:
    """Range reduce x=2**k*y, 1<=y<2; exact tail for atanh series."""
    if x<=0: raise ValueError('log input must be positive')
    if terms<1: raise ValueError('terms must be positive')
    k=0; y=x
    while y<1: y*=2; k-=1
    while y>=2: y/=2; k+=1
    def series(z):
        total=sum((2*z**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
        remainder=2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
        return Interval(total,total+remainder)
    return series((y-1)/(y+1))+k*series(F(1,3))


def floor_grid(x: F, scale: int) -> F:
    return F((x.numerator*scale)//x.denominator,scale)


def ceil_grid(x: F, scale: int) -> F:
    return -floor_grid(-x,scale)


def rational_enclosure(x, digits=12):
    x=as_interval(x); den=10**digits
    return [str(floor_grid(x.lo,den)),str(ceil_grid(x.hi,den))]


def fixed_decimal(x: F, digits: int) -> str:
    """Only called for x on the grid 10**(-digits); no float conversion."""
    n=x*10**digits
    check(n.denominator==1,'decimal grid')
    a=abs(n.numerator); q,r=divmod(a,10**digits)
    return ('-' if n<0 else '')+str(q)+'.'+str(r).zfill(digits)


def nice_interval(x, digits=12):
    x=as_interval(x); den=10**digits
    return '['+fixed_decimal(floor_grid(x.lo,den),digits)+', '+fixed_decimal(ceil_grid(x.hi,den),digits)+']'


def ldl(A):
    """Exact unpivoted LDL^T; requires positive pivots, checks factorization."""
    n=len(A); L=eye(n); d=[]
    for i in range(n):
        p=A[i][i]-sum((L[i][k]**2*d[k] for k in range(i)),F(0))
        check(p>0,f'LDL pivot {i+1}')
        d.append(p)
        for j in range(i+1,n):
            L[j][i]=(A[j][i]-sum((L[j][k]*L[i][k]*d[k] for k in range(i)),F(0)))/p
    D=[[d[i] if i==j else F(0) for j in range(n)] for i in range(n)]
    check(mm(mm(L,D),transpose(L))==A,'LDL reconstruction')
    return L,d


def p_add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return c

def p_mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def polynomial_minor(K,D,S):
    """Independent permutation expansion of det((K+tD)_S)."""
    n=len(S)
    if not n: return [F(1)]
    out=[F(0)]*(n+1)
    for perm in itertools.permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        product=[F(sign)]
        for i,j in enumerate(perm): product=p_mul(product,[K[S[i]][S[j]],D[S[i]][S[j]]])
        out=p_add(out,product)
    return out


def stringify(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,Interval):
        # Serialized intervals are rational outward enclosures; calculations above
        # retain their full exact fractions. Avoid huge decimal integer strings.
        return {'lo':str(floor_grid(x.lo,10**24)),'hi':str(ceil_grid(x.hi,10**24))}
    if isinstance(x,dict): return {str(k):stringify(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [stringify(y) for y in x]
    return x


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'output')
    args=parser.parse_args(); out=args.output_dir; out.mkdir(parents=True,exist_ok=True)
    report=[]
    def say(s): report.append(s); print(s)
    a=list(map(F,[1,2,3,4,5])); b=list(map(F,[2,-1,3,-2,1]))
    H_a=sub(eye(5),scale(outer(a,a),2/dot(a,a)))
    H_b=sub(eye(5),scale(outer(b,b),2/dot(b,b)))
    U=[row[:3] for row in mm(H_a,H_b)]
    check(mm(transpose(U),U)==eye(3),'isometry')
    pairs=list(itertools.combinations(range(5),2)); triples=list(itertools.combinations(range(5),3))
    r=U; w=[cross(r[i],r[j]) for i,j in pairs]
    g=[dot(x,x) for x in r]; h=[dot(x,x) for x in w]
    q=[det3([U[i] for i in S])**2 for S in triples]
    check(all(x>0 for x in g+h+q),'full spark and lower weights')
    check(sum(g)==sum(h)==3 and sum(q)==1,'weight sums')
    check(sum_matrices([outer(x,x) for x in r])==eye(3),'row tight frame')
    check(sum_matrices([outer(x,x) for x in w])==eye(3),'cross-product tight frame')
    say('PASS isometry, full spark, weight sums, and both tight frames')

    logg=[log_interval(x) for x in g]; logh=[log_interval(x) for x in h]; logq=[log_interval(x) for x in q]
    tg=sum((x*z for x,z in zip(g,logg)),as_interval(0))
    th=sum((x*z for x,z in zip(h,logh)),as_interval(0))
    c=-sum((x*z for x,z in zip(q,logq)),as_interval(0))
    T=[[sum((x[i]*x[j]*z for x,z in zip(r+w,logg+logh)),as_interval(0)) for j in range(3)] for i in range(3)]
    tt=tg+th; beta=th-tg+c
    m0=2*tg-F(2,3)*tt; m1=2*(th+c)-F(2,3)*tt
    Eg=[[2*T[i][j]-(F(2,3)*tt if i==j else 0) for j in range(3)] for i in range(3)]
    check(F(1,4)<m0.lo and m0.hi<F(1,2),'m0')
    check(F(1,4)<m1.lo and m1.hi<F(1,2),'m1')
    check(0<beta.lo and beta.hi<F(1,8),'beta')
    check(F('1.900161876460949643')<c.lo and c.hi<F('1.900161876460949644'),'prompt entropy interval')
    E0=[[floor_grid((z.lo+z.hi)/2+F(1,2_000_000),1_000_000) for z in row] for row in Eg]
    e=F(1,1_000_000)
    for i in range(3):
        for j in range(3):
            check(E0[i][j]-e<=Eg[i][j].lo and Eg[i][j].hi<=E0[i][j]+e,'E rounding error')
    frob_upper_sq=sum((abs(E0[i][j])+e)**2 for i in range(3) for j in range(3))
    check(frob_upper_sq<F(1,25),'E Frobenius bound')
    Ecert_plus=add(scale(eye(3),F(3,20)-3*e),E0)
    Ecert_minus=sub(scale(eye(3),F(3,20)-3*e),E0)
    LEp,dEp=ldl(Ecert_plus); LEm,dEm=ldl(Ecert_minus)
    say('PASS 1/4 < m(0),m(1) < 1/2; 0 < beta < 1/8')
    say('PASS ||E_geo||op < 3/20 and ||E_geo||F < 1/5')
    say('c = '+nice_interval(c,20))
    say('tg = '+nice_interval(tg)); say('th = '+nice_interval(th))
    say('beta = '+nice_interval(beta)); say('m(0) = '+nice_interval(m0)); say('m(1) = '+nice_interval(m1))

    Fmat=[[sum((2*vecform(x)[i]*vecform(x)[j]/dot(x,x) for x in r+w),F(0)) for j in range(6)] for i in range(6)]
    metric=[[F([1,1,1,2,2,2][i]) if i==j else F(0) for j in range(6)] for i in range(6)]
    C=sub(Fmat,scale(metric,F(1,4)))
    LF,dF=ldl(C)
    say('PASS F_(1/2)(V) >= (1/4)||V||F^2 by exact 6x6 LDL^T')
    for i,p in enumerate(dF): say(f'  F certificate pivot {i+1}: '+nice_interval(p,9))
    say('E0 (each entry within 1/1000000 of E_geo):')
    for row in E0: say('  '+' '.join(str(x) for x in row))
    for label,ps in [('+E0',dEp),('-E0',dEm)]:
        say('  '+label+' certificate pivots: '+', '.join(nice_interval(p,9) for p in ps))
    say('E Frobenius squared upper = '+str(frob_upper_sq))

    rho=F(1,2000)
    check(F(9,10)/(1+rho)**3>F(7,8),'Fisher discount coefficient')
    transfer=F(119,1600)-F(66,1999)-F(243,250000)-F(1,16000)
    check(transfer>F(1,25),'final uniform margin')
    say('PASS uniform final curvature margin = '+str(transfer)+' > 1/25')

    eta=F(1,10000)
    A=add(scale(eye(3),F(1,2)),[[eta,0,0],[0,-eta,0],[0,0,0]])
    V=add(eye(3),[[0,F(1,10),0],[F(1,10),0,0],[0,0,0]])
    comm=sub(mm(A,V),mm(V,A)); check(any(x for row in comm for x in row),'noncommuting example')
    d=det3(A); d1=trprod(adj(A),V); J=adj(V); d2=2*trprod(A,J)
    topF=d1*d1/d
    check(F(19,10)*d2>F(5,4)*topF,'top-only control fails by factor >5/4')
    ratio=c*d2/topF
    say('PASS explicit example [A,V] != 0 and c*d_second > (5/4)*F_top')
    say('d = '+str(d)+'; d_first = '+str(d1)+'; d_second = '+str(d2))
    say('c*d_second/F_top = '+nice_interval(ratio))

    tau=trace(V); ta=trace(A)
    D1=add(add(mm(A,A),scale(A,1-ta)),scale(eye(3),d))
    D2=sub(adj(A),scale(eye(3),d))
    D1p=add(sub(add(add(mm(A,V),mm(V,A)),scale(V,1-ta)),scale(A,tau)),scale(eye(3),d1))
    adjp=add(sub(sub(add(mm(A,V),mm(V,A)),scale(A,tau)),scale(V,ta)),scale(eye(3),ta*tau-trprod(A,V)))
    D2p=sub(adjp,scale(eye(3),d1))
    D1pp=sub(scale(J,2),scale(eye(3),2*trprod(sub(eye(3),A),J)))
    D2pp=sub(scale(J,2),scale(eye(3),d2))
    data={():[det3(sub(eye(3),A)),-trprod(adj(sub(eye(3),A)),V),2*trprod(sub(eye(3),A),J)]}
    for i in range(5): data[(i,)]=[quad(D1,r[i]),quad(D1p,r[i]),quad(D1pp,r[i])]
    for S,x in zip(pairs,w): data[S]=[quad(D2,x),quad(D2p,x),quad(D2pp,x)]
    for S,z in zip(triples,q): data[S]=[d*z,d1*z,d2*z]
    allsets=[S for k in range(6) for S in itertools.combinations(range(5),k)]
    for S in allsets:
        if S not in data: data[S]=[F(0),F(0),F(0)]
    check([sum(data[S][j] for S in allsets) for j in range(3)]==[1,0,0],'mass and derivatives')
    check([sum(len(S)*data[S][j] for S in allsets) for j in range(3)]==[trace(A),trace(V),0],'first moment and derivatives')
    check(all(data[S][0]>0 for S in allsets if len(S)<=3),'example support')

    K=mm(mm(U,A),transpose(U)); D=mm(mm(U,V),transpose(U))
    minors={S:polynomial_minor(K,D,S) for S in allsets}
    for S in allsets:
        poly=[F(0)]*6
        for T in allsets:
            if set(S).issubset(T):
                poly=p_add(poly,[(-1)**(len(T)-len(S))*x for x in minors[T]])
        check([poly[0],poly[1],2*poly[2]]==data[S],f'containment cross-check {S}')
        check(all(x==0 for x in poly[4:]),'degree <=3')
    say('PASS all 32 configuration p,p_first,p_second match independent containment/permutation expansion')

    fisher=sum((x[1]*x[1]/x[0] for x in data.values() if x[0]>0),F(0))
    accel=-sum((x[2]*log_interval(x[0]) for x in data.values() if x[0]>0),as_interval(0))
    entropy_second=accel-fisher
    check(entropy_second.hi<0,'example entropy second derivative')
    normv=trace(mm(V,V))
    check(entropy_second.hi<=-normv/25,'example theorem bound')
    say('example H_second = '+nice_interval(entropy_second))
    say('example theorem bound H_second <= '+str(-normv/25))

    with (out/'example_probabilities.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f); writer.writerow(['S_1_based','p','p_first','p_second'])
        for S in allsets: writer.writerow(['empty' if not S else ''.join(str(i+1) for i in S),*[str(x) for x in data[S]]])
    certificate={'task_id':'I05-W3-20260909','arithmetic':'fractions.Fraction; no float proof decisions','log_terms':32,'serialized_interval_decimal_grid':24,
        'U':U,'g':g,'h':h,'q':q,'pairs_1_based':[[i+1 for i in S] for S in pairs],'triples_1_based':[[i+1 for i in S] for S in triples],
        'c':c,'tg':tg,'th':th,'beta':beta,'m0':m0,'m1':m1,'T':T,'E_geo':Eg,'E0':E0,
        'E_entry_error':e,'E_frobenius_squared_upper':frob_upper_sq,
        'E_plus_matrix':Ecert_plus,'E_plus_L':LEp,'E_plus_pivots':dEp,
        'E_minus_matrix':Ecert_minus,'E_minus_L':LEm,'E_minus_pivots':dEm,
        'F_center_matrix':Fmat,'Frobenius_metric':metric,'F_certificate_matrix':C,'F_L':LF,'F_pivots':dF,
        'uniform_margin':transfer,'example':{'A':A,'V':V,'commutator':comm,'d':d,'d_first':d1,'d_second':d2,
        'F_top':topF,'top_ratio':ratio,'F_total':fisher,'H_second':entropy_second,'V_norm_squared':normv}}
    (out/'certificate.json').write_text(json.dumps(stringify(certificate),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'platform':platform.platform(),'proof_dependencies':'Python standard library only'},indent=2)+'\n',encoding='utf-8')
    say('ALL EXACT CHECKS PASSED. This is author self-verification, not independent review.')
    (out/'verification_output.txt').write_text('\n'.join(report)+'\n',encoding='utf-8')


def sum_matrices(mats):
    if not mats: raise ValueError('empty matrix sum')
    n=len(mats[0]); out=[[F(0) for _ in range(n)] for _ in range(n)]
    for A in mats: out=add(out,A)
    return out


if __name__=='__main__': main()
