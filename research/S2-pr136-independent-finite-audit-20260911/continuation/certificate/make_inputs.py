from fractions import Fraction as F
from math import factorial, nextafter, inf
import json,time
from pathlib import Path
ROOT=Path(__file__).parent
start=time.perf_counter()

def atan_bounds(x,n):
    p=x; s=F(0)
    for k in range(n):
        s+=p/(2*k+1)*(-1 if k%2 else 1)
        p*=x*x
    e=abs(p)/(2*n+1)
    return (s-e,s+e)

a=atan_bounds(F(1,5),90); b=atan_bounds(F(1,239),30)
pi=(16*a[0]-4*b[1],16*a[1]-4*b[0])
assert pi[0]>3 and pi[1]<F(22,7)

def cos_at(x,n=40):
    term=F(1); total=F(1)
    for k in range(1,n):
        term*=-x*x/F((2*k-1)*(2*k))
        total+=term
    rem=abs(term*x*x/F((2*n-1)*(2*n)))
    return total-rem,total+rem

def outward(x,up):
    y=float(x)
    if (F.from_float(y)<x if up else F.from_float(y)>x):
        y=nextafter(y,inf if up else -inf)
    assert (F.from_float(y)>=x if up else F.from_float(y)<=x)
    return y

cs=[]
for j in range(65):
    if j==0: v=(F(1),F(1))
    elif j==64: v=(F(-1),F(-1))
    else:
        # Cosine is decreasing on [0,pi]. Both Taylor tails are explicit.
        lo=cos_at(pi[1]*F(j,64))[0]
        hi=cos_at(pi[0]*F(j,64))[1]
        v=(lo,hi)
    cs.append((outward(v[0],False),outward(v[1],True)))

nodes=[]
for cell in range(4):
    center=F(5+2*cell,8)
    for j in range(32):
        cl,ch=cs[2*j+1]
        lo=center+F.from_float(cl)/8
        hi=center+F.from_float(ch)/8
        tl,th=outward(lo,False),outward(hi,True)
        nodes.append({'id':32*cell+j,'cell':cell,'j':j,'t_lo':tl.hex(),'t_hi':th.hex()})

# Verify the exact dyadic literals used by C++ for log(2).
x=F(1,3); lg=2*sum((x**(2*j+1)/F(2*j+1) for j in range(40)),F(0))
rem=2*x**81/(81*(1-x*x))
loglo=float.fromhex('0x1.62e42fefa39eep-1')
loghi=float.fromhex('0x1.62e42fefa39f0p-1')
assert F.from_float(loglo)<lg and lg+rem<F.from_float(loghi)
assert 2*F(1,4)**33/(33*(1-F(1,4)**2)) < F(1,2**68)
assert sum((F(3)**k/factorial(k) for k in range(7)),F(0))>F(96,5)

obj={'status':'AUTHOR_INPUTS_PENDING_INDEPENDENT_REVIEW','N':32,'r':9,'rho':3,
     'cos_pi_j_over_64':[[lo.hex(),hi.hex()] for lo,hi in cs],
     'nodes':nodes,'pi_enclosure_method':'Machin 16 atan(1/5)-4 atan(1/239), explicit alternating tails',
     'cos_enclosure_method':'40-term rational Taylor with explicit next-term tail',
     'log2_hex':[loglo.hex(),loghi.hex()], 'generation_wall_seconds':time.perf_counter()-start}
(ROOT/'certificate_inputs.json').write_text(json.dumps(obj,indent=2)+'\n')
(ROOT/'nodes.tsv').write_text(''.join(f"{x['id']} {x['t_lo']} {x['t_hi']}\n" for x in nodes))
print(json.dumps({'generated_nodes':len(nodes),'cos_bounds':len(cs),'seconds':time.perf_counter()-start}))
