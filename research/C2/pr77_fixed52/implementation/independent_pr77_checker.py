#!/usr/bin/env python3
"""Independent fixed PR77 unit, one process and one immutable 2700s deadline."""
import argparse
import decimal
import gzip
import hashlib
import itertools
import json
import os
import platform
import resource
import sys
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path

sys.set_int_max_str_digits(0)
START = time.monotonic()
OUT = None
DEADLINE = None
CHECKS = 0
PHASE = 'entry'
DEC = decimal.Decimal
LOW = decimal.Context(prec=100, rounding=decimal.ROUND_FLOOR)
HIGH = decimal.Context(prec=100, rounding=decimal.ROUND_CEILING)
NEAR = decimal.Context(prec=100, rounding=decimal.ROUND_HALF_EVEN)
for _ctx in [LOW, HIGH, NEAR]:
    _ctx.traps[decimal.FloatOperation] = True
WIDEN = DEC('1e-90')
WIDTH = DEC('1e-40')


def utc():
    return datetime.now(timezone.utc).isoformat()


def pack(value):
    if isinstance(value, (Q, DEC)):
        return str(value)
    if isinstance(value, dict):
        return {str(k): pack(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [pack(v) for v in value]
    return value


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(pack(value), indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    tmp.replace(path)


class Halt(Exception):
    def __init__(self, state, gate):
        self.state, self.gate = state, gate
        super().__init__(state + ': ' + gate)


def tick():
    if time.time() >= DEADLINE:
        raise Halt('TIMEOUT', 'immutable_deadline')


def check(name, passed, data=None, state='STOPPED_FIRST_EXACT_MISMATCH'):
    global CHECKS
    tick()
    CHECKS += 1
    row = {'sequence':CHECKS, 'phase':PHASE, 'gate':name, 'passed':bool(passed), 'data':data}
    with (OUT / 'CHECKS.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(pack(row), separators=(',', ':')) + '\n')
    if not passed:
        write('FIRST_FAILURE.json', row | {'status':state})
        raise Halt(state, name)


def progress(stage, **fields):
    tick()
    value = {'phase':PHASE, 'stage':stage, 'utc':utc(), 'elapsed_seconds':time.monotonic()-START, **fields}
    write('PROGRESS.json', value)
    print(json.dumps(pack(value), separators=(',', ':')), flush=True)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def pa(a, b):
    return trim((a[i] if i < len(a) else Q(0)) + (b[i] if i < len(b) else Q(0))
                for i in range(max(len(a), len(b))))


def ps(a, c):
    return trim(x*c for x in a)


def pm(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def pv(a, x):
    out = Q(0)
    for c in reversed(a):
        out = out*x+c
    return out


def poly_det_laplace(matrix):
    if not matrix:
        return (Q(1),)
    out = (Q(0),)
    for j, a in enumerate(matrix[0]):
        sub = [row[:j]+row[j+1:] for row in matrix[1:]]
        out = pa(out, ps(pm(a, poly_det_laplace(sub)), Q((-1)**j)))
    return out


def poly_det_permutation(matrix):
    out = (Q(0),)
    n = len(matrix)
    for perm in itertools.permutations(range(n)):
        inv = sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term = (Q((-1)**inv),)
        for i, j in enumerate(perm):
            term = pm(term, matrix[i][j])
        out = pa(out, term)
    return out


def residuals(a, b, rho):
    return [Q(1,2)-2*a*rho-2*b*rho**2,
            rho/2-a*(1+rho**2)-b*(rho+rho**3),
            rho**2/2-a*(rho+rho**3)-b*(1+rho**4),
            Q(1,2)-a*(1/rho+rho)-b*(1/rho**2+rho**2)]


def geometric(R, q):
    return [q**R/(1-q), q**R*(R/(1-q)+q/(1-q)**2),
            q**R*(R**2/(1-q)+2*R*q/(1-q)**2+q*(1+q)/(1-q)**3)]


def tail_constants(d, M2, M3, M4, U1, U2):
    k1, k2 = 1/d, 2/d**2
    return [M2/2, k1*M2+M3*U1/2,
            M2*(k1**2+k2)+2*k1*M3*U1+(M4*U1**2+M3*U2)/2]


def curvature_tail(Cstar, rho, As, R=18):
    A0, A1, A2 = As
    coefficients = [A2+4*A1+8*A0, 4*A1+12*A0, 4*A0]
    sums = geometric(R, rho**4)
    return Cstar**2*rho**(-12)*sum((coefficients[i]*sums[i] for i in range(3)), Q(0))


def phase_a(spec):
    global PHASE
    PHASE = 'A_exact_constants_and_covariance'
    progress('start')
    delta = Q(1,16)
    minimum = Q(1,4)-Q(3,2)**2/128
    maximum = Q(3,4)+Q(3,2)/8
    check('symbol_legality', minimum==Q(119,512) and maximum==Q(15,16), {'min':minimum,'max':maximum})
    u = spec['uniform']
    a,b,rho = (Q(u[k]) for k in ['a','b','rho'])
    res = residuals(a,b,rho)
    C = 1/res[0]
    factors = [a*rho+b, a*rho+b+b*rho]
    Cstar = C**3*factors[0]**2*factors[1]**2
    C0 = Q(u['C0'])
    dominance = Q(1,2)-2*a-2*b
    uniform = {'a':a,'b':b,'rho':rho,'dominance':dominance,'residuals':res,'C':C,
               'factors':factors,'Cstar':Cstar,'C0':C0,'strict_positive_difference':C0-Cstar}
    write('A/uniform_comparison.json', uniform)
    check('uniform_dominance_literal', dominance==Q(u['dominance']) and dominance>0,dominance)
    for i, value in enumerate(res):
        check(f'uniform_residual_{i}', value==Q(u['residuals'][i]) and value>0,value)
    check('uniform_C_and_factors', C==Q(u['C']) and factors==list(map(Q,u['factors'])),uniform)
    check('uniform_Cstar_strict_bound', Cstar<C0<1,uniform)
    M2 = 1/delta+1/(1-delta)
    M3 = 1/delta**2-1/(1-delta)**2
    M4 = 2/delta**3+2/(1-delta)**3
    real_a=Q(3,2)/16
    real_margin=Q(1,2)-2*real_a-2*b
    Ri,b1,bi,d1,di,Ai = 1/real_margin,real_a+b,max(real_a,b),Q(1,16),Q(1,16),Q(2,16)
    U1 = 2*d1*Ri*bi+b1*Ri*Ai*Ri*bi
    U2 = 4*d1*Ri*Ai*Ri*bi+2*d1*Ri*di+2*b1*Ri*Ai*Ri*Ai*Ri*bi
    values = {'M2':M2,'M3':M3,'M4':M4,'U1':U1,'U2':U2}
    As = tail_constants(Q(1,8),M2,M3,M4,U1,U2)
    E18 = M2*C0**2*rho**(4*18-12)
    uniform_tail = curvature_tail(C0,rho,As)
    write('A/derivative_and_uniform_tail.json', {'values':values,'delta':delta,
          'inverse_norm':Ri,'b_l1':b1,'b_linf':bi,'d_l1':d1,'d_linf':di,'Aprime_norm':Ai,
          'Bregman_A0_A1_A2':As,'real_diagonal_margin':real_margin,
          'event_score_bound_per_site':Ri*Ai,'event_score_derivative_bound_per_site':(Ri*Ai)**2,
          'E18':E18,'uniform_Tail18':uniform_tail,'S0_S1_S2':geometric(18,rho**4),
          'geometric_formulas':['q^R/(1-q)','q^R*(R/(1-q)+q/(1-q)^2)',
          'q^R*(R^2/(1-q)+2*R*q/(1-q)^2+q*(1+q)/(1-q)^3)']})
    for name,value in values.items():
        check(name+'_literal',value==Q(spec[name]),value)
    check('event_score_coefficients',Ri*Ai==2 and (Ri*Ai)**2==4)
    check('Bregman_uniform_A2_identity', As[2]==192*M2+16*M3*U1+(M4*U1**2+M3*U2)/2,As)
    point_tails = {}
    for point in spec['points']:
        t,d,z,rp = (Q(point[k]) for k in ['t','d','max_abs_z','rho'])
        ap = z/16
        rr = residuals(ap,b,rp)
        Cp = 1/rr[0]
        factorsp = [Cp,ap*rp+b,ap*rp+b+b*rp]
        Cs = Cp**3*factorsp[1]**2*factorsp[2]**2
        Aa = tail_constants(d,M2,M3,M4,U1,U2)
        T = curvature_tail(Cs,rp,Aa)
        ss = geometric(18,rp**4)
        ss_next = geometric(19,rp**4)
        record = {'t':t,'d':d,'max_abs_z':z,'a':ap,'b':b,'rho':rp,'residuals':rr,
                  'factors':factorsp,'Cstar':Cs,'kappa1':1/d,'kappa2':2/d**2,
                  'A0_A1_A2':Aa,'S0_S1_S2':ss,'Tail18':T,'threshold':Q(point['threshold'])}
        write('A/point_'+str(t).replace('/','_')+'.json',record)
        check('point_disk_'+str(t),t+d==z and 0<rp<1,record)
        for j,value in enumerate(rr):
            check(f'point_{t}_residual_{j}',value==Q(point['residuals'][j]) and value>0,value)
        check('point_factors_'+str(t),factorsp==list(map(Q,point['factors'])),factorsp)
        for j in range(3):
            check(f'geometric_boundary_identity_{t}_{j}',ss[j]-ss_next[j]==18**j*rp**(4*18))
        check('point_tail_positive_'+str(t),T>0,T)
        point_tails[str(t)] = T

    sets = [[0,1],[0,1,2],[0,1,2,3],[0,1,3,4]]
    determinants = []
    for sites in sets:
        matrix = [[(Q(1,2),) if i==j else (Q(0),Q(1)) if abs(i-j)==1 else
                   (Q(1,8),) if abs(i-j)==2 else (Q(0),) for j in sites] for i in sites]
        first,second = poly_det_laplace(matrix),poly_det_permutation(matrix)
        determinants.append(first)
        write('A/inclusion_polynomials.json', {'site_sets':sets[:len(determinants)],'determinants':determinants})
        check('polynomial_determinant_dual_'+str(sites),first==second,{'laplace':first,'permutation':second})
    m=determinants[0]
    m2=pm(m,m)
    cs=[pa(m,ps(m2,-1))]+[pa(value,ps(m2,-1)) for value in determinants[1:]]
    V=cs[0]
    for c in cs[1:]:
        V=pa(V,ps(c,2))
    computed={'m':m,'c0':cs[0],'c1':cs[1],'c2':cs[2],'c3':cs[3],'V':V}
    endpoints=[pv(V,Q(1,32)),pv(V,Q(3,32))]
    Vt=tuple(coef/Q(16)**i for i,coef in enumerate(V))
    Vs=trim(Vt[::2])
    monotonic_numerator=trim((1-i)*coef for i,coef in enumerate(Vs))
    fisher=Q(1,4)/(16384*endpoints[0])
    mprime_t=trim(i*m[i]/Q(16)**i for i in range(1,len(m)))
    write('A/covariances.json',{'in_u':computed,'V_in_t':Vt,'V_in_s_t_squared':Vs,
          'V_endpoints':endpoints,'V_minus_sVprime':monotonic_numerator,'fisher_lower_bound':fisher,
          'mprime_in_t':mprime_t})
    check('mprime_physical_t',mprime_t==(Q(0),Q(-1,128)),mprime_t)
    for name,value in computed.items():
        check('covariance_literal_'+name,value==trim(map(Q,spec['covariance_polynomials_in_u'][name])),value)
    check('variance_endpoint_literals',endpoints==list(map(Q,spec['variance_endpoints'])),endpoints)
    check('variance_positivity_monotonicity',endpoints[1]>0 and Vs[1]<0 and Vs[2]<0 and
          monotonic_numerator[0]>0 and all(x>=0 for x in monotonic_numerator),monotonic_numerator)
    check('fisher_bound_literal',fisher==Q(spec['fisher_lower_bound']) and fisher>0,fisher)
    progress('complete',point_tails=point_tails,E18=E18)
    return E18,point_tails


def bareiss(matrix):
    """Exact integer determinant with pivoting and explicit division checks."""
    n=len(matrix)
    if n==0:
        return 1
    a=[list(row) for row in matrix]
    sign,previous=1,1
    for k in range(n-1):
        pivot_row=next((i for i in range(k,n) if a[i][k]),None)
        if pivot_row is None:
            return 0
        if pivot_row!=k:
            a[k],a[pivot_row]=a[pivot_row],a[k]
            sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                quotient,remainder=divmod(numerator,previous)
                if remainder:
                    check('Bareiss_division_remainder',False,{'k':k,'numerator':str(numerator),'divisor':str(previous)})
                a[i][j]=quotient
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]


def integer_kernel(n,a):
    return [[16 if i==j else a if abs(i-j)==1 else 4 if abs(i-j)==2 else 0
             for j in range(n)] for i in range(n)]


def direct_event(n,a,word):
    matrix=integer_kernel(n,a)
    # This event convention is used only by the independent direct determinant path.
    missing=0
    for i in range(n):
        if (word>>i)&1==0:
            matrix[i][i]-=32
            missing+=1
    sign=-1 if missing%2 else 1
    return matrix,sign*bareiss(matrix),sign


def direct_derivatives(matrix,sign):
    n=len(matrix)
    derivative=[[2 if abs(i-j)==1 else 0 for j in range(n)] for i in range(n)]
    first=0
    second=0
    for i in range(n):
        changed=[list(row) for row in matrix]
        changed[i]=derivative[i]
        first+=bareiss(changed)
        for j in range(i+1,n):
            twice=[list(row) for row in changed]
            twice[j]=derivative[j]
            second+=2*bareiss(twice)
    return sign*first,sign*second


MASKS=(3,5,6,9,10,12)
MASK_INDEX={mask:i for i,mask in enumerate(MASKS)}


def transitions(n,a):
    """Four frontier bits for columns i-2..i+1; choose column i-2+j."""
    tables=[]
    for i in range(n):
        branches=[]
        for occupied in [False,True]:
            entries=[]
            for src,mask in enumerate(MASKS):
                for j in range(5):
                    column=i-2+j
                    if column<0 or column>=n or mask&(1<<j):
                        continue
                    updated=mask|(1<<j)
                    if not updated&1:
                        continue
                    newmask=updated>>1
                    sign=-1 if (mask>>(j+1)).bit_count()%2 else 1
                    offset=abs(column-i)
                    coefficient=(16 if occupied else -16) if offset==0 else a if offset==1 else 4
                    derivative=2 if offset==1 else 0
                    entries.append((3*src,3*MASK_INDEX[newmask],sign*coefficient,sign*derivative))
            branches.append(entries)
        tables.append(branches)
    return tables


def advance(state,table):
    result=[0]*18
    for source,target,c,cp in table:
        x,y,z=state[source],state[source+1],state[source+2]
        result[target]+=c*x
        result[target+1]+=c*y+cp*x
        result[target+2]+=c*z+2*cp*y
    return result


def diadd(a,b):
    return LOW.add(a[0],b[0]),HIGH.add(a[1],b[1])


def dineg(a):
    return a[1].copy_negate(),a[0].copy_negate()


def disub(a,b):
    return LOW.subtract(a[0],b[1]),HIGH.subtract(a[1],b[0])


def dimul_int(a,c):
    coefficient=DEC(c)
    if c>=0:
        return LOW.multiply(a[0],coefficient),HIGH.multiply(a[1],coefficient)
    return LOW.multiply(a[1],coefficient),HIGH.multiply(a[0],coefficient)


def didiv_int(a,c):
    if c<=0:
        raise ValueError('positive interval divisor required')
    denominator=DEC(c)
    return LOW.divide(a[0],denominator),HIGH.divide(a[1],denominator)


def diq(q):
    q=Q(q)
    numerator,denominator=DEC(q.numerator),DEC(q.denominator)
    return LOW.divide(numerator,denominator),HIGH.divide(numerator,denominator)


def direcord(a):
    return {'lower':str(a[0]),'upper':str(a[1]),'arithmetic_width_upper':str(HIGH.subtract(a[1],a[0]))}


def context_record(ctx):
    return {'precision':ctx.prec,'rounding':ctx.rounding,'Emin':ctx.Emin,'Emax':ctx.Emax,
            'capitals':ctx.capitals,'clamp':ctx.clamp,
            'flags':{key.__name__:value for key,value in ctx.flags.items()},
            'traps':{key.__name__:value for key,value in ctx.traps.items()}}


def log_integer(N):
    if N==1:
        return DEC(0),DEC(0)
    if N<=0 or N>32**19:
        check('log_integer_domain',False,{'N':str(N)},'FAILED_POSITIVITY')
    rounded=DEC(N).ln(context=NEAR)
    return LOW.subtract(rounded,WIDEN),HIGH.add(rounded,WIDEN)


def finite_pair(t,n,histogram):
    a=int(2*t)
    log32=log_integer(32)
    weighted=(DEC(0),DEC(0))
    fisher=(DEC(0),DEC(0))
    acceleration=(DEC(0),DEC(0))
    processed=0
    # Streaming log inventory consumes exactly the same independently generated arguments.
    def log_rows():
        nonlocal weighted,fisher,acceleration,processed
        for N in sorted(histogram):
            count,sum_first,sum_second,sum_squared=histogram[N]
            bounds=log_integer(N)
            weighted=diadd(weighted,dimul_int(bounds,count*N))
            fisher=diadd(fisher,(LOW.divide(DEC(sum_squared),DEC(N)),HIGH.divide(DEC(sum_squared),DEC(N))))
            acceleration=diadd(acceleration,dimul_int(bounds,sum_second))
            processed+=1
            if processed%25000==0:
                progress('directed_log_accumulation',t=t,n=n,processed_arguments=processed,total_arguments=len(histogram))
            yield [str(N),str(bounds[0]),str(bounds[1])]
    gzip_chunks(f'D/t{a}_n{n}_log_intervals',log_rows(),['N','natural_log_lower','natural_log_upper'])
    scale=32**n
    H=disub(dimul_int(log32,n),didiv_int(weighted,scale))
    Hsecond=didiv_int(dineg(diadd(fisher,acceleration)),scale)
    record={'t':t,'n':n,'scale':str(scale),'distinct_log_arguments':processed,'log32':direcord(log32),
            'sum_count_N_logN':direcord(weighted),'Fisher_numerator_sum_Nprime_squared_over_N':direcord(fisher),
            'acceleration_numerator_sum_Nsecond_logN':direcord(acceleration),
            'Fisher_probability_scale':direcord(didiv_int(fisher,scale)),
            'acceleration_probability_scale':direcord(didiv_int(acceleration,scale)),
            'H':direcord(H),'Hsecond':direcord(Hsecond),
            'log32_acceleration_removed_only_after_exact_normalization':True}
    write(f'D/t{a}_n{n}_finite.json',record)
    for name,bounds in [('H',H),('Hsecond',Hsecond)]:
        check(f'finite_width_t{a}_n{n}_{name}',bounds[0]<=bounds[1] and HIGH.subtract(bounds[1],bounds[0])<=WIDTH,
              direcord(bounds),'UNRESOLVED_INTERVAL')
    return H,Hsecond


def phase_d(spec,all_histograms,E18,point_tails):
    global PHASE
    PHASE='D_directed_intervals_and_true_bounds'
    progress('start')
    # 32^19<10^29 and log(10)<3, since the first four terms of exp(3) sum to13>10.
    # Thus 0<log(N)<87<100 and half an ulp at precision100 is at most5e-99.
    check('log_rounding_widening_dominates_error',32**19<10**29 and Q(1,10**90)>Q(5,10**99),
          {'integer_ceiling':str(32**19),'decimal_digit_ceiling':29,'log_upper_bound':87,
           'half_ulp_upper':'5e-99','widening':'1e-90','N1_exact':True})
    write('D/decimal_contract.json',{'precision':100,'widening':'1e-90','finite_width_limit':'1e-40',
          'implementation':platform.python_implementation(),'decimal_version':decimal.__version__,
          'libmpdec_version':getattr(decimal,'__libmpdec_version__','unavailable'),
          'Decimal_class_module':DEC.__module__,'HAVE_CONTEXTVAR':getattr(decimal,'HAVE_CONTEXTVAR',None),
          'correct_rounding_source':'https://docs.python.org/3/library/decimal.html#decimal.Decimal.ln',
          'ln_rule':'ROUND_HALF_EVEN correctly rounded; then absolute widening using directed subtraction/addition',
          'integer_conversion':'Decimal(int) is exact, independent of context precision; no float conversion',
          'rational_conversion':'integer numerator and denominator converted exactly, then FLOOR and CEILING division',
          'negation':'copy_negate plus endpoint swap, never context-rounded unary negation',
          'error_derivation':'N<=32^19<10^29; exp(3)>1+3+9/2+27/6=13>10; log N<87<100; half ulp<=5e-99<1e-90',
          'initial_contexts':{'floor':context_record(LOW),'ceiling':context_record(HIGH),'ln_nearest':context_record(NEAR)}})
    finite={}
    conditional={}
    for literal_t in spec['parameters']:
        t=Q(literal_t)
        finite[str(t)]={}
        for n in [18,19]:
            finite[str(t)][n]=finite_pair(t,n,all_histograms[str(t)][n])
        h=disub(finite[str(t)][19][0],finite[str(t)][18][0])
        hsecond=disub(finite[str(t)][19][1],finite[str(t)][18][1])
        conditional[str(t)]=(h,hsecond)
        write('D/t'+str(int(2*t))+'_conditional.json',{'t':t,'depth':18,'h18':direcord(h),'h18second':direcord(hsecond)})
        for name,bounds in [('h18',h),('h18second',hsecond)]:
            check(f'conditional_width_t{t}_{name}',bounds[0]<=bounds[1] and HIGH.subtract(bounds[1],bounds[0])<=WIDTH,
                  direcord(bounds),'UNRESOLVED_INTERVAL')
        progress('finite_point_complete',t=t,h18=direcord(h),h18second=direcord(hsecond))
    # Analytic tails are separate from the finite arithmetic width.
    hmid=conditional['1'][0]
    hend1=conditional['1/2'][0]
    hend2=conditional['3/2'][0]
    gap=disub(disub(hmid,diq(E18)),didiv_int(diadd(hend1,hend2),2))
    margin=disub(gap,diq(Q(spec['jensen_threshold'])))
    jensen={'h18_mid':direcord(hmid),'h18_endpoints':[direcord(hend1),direcord(hend2)],
            'E18_exact':E18,'E18_outward':direcord(diq(E18)),
            'true_gap_lower':str(gap[0]),'threshold':spec['jensen_threshold'],
            'strict_margin_lower':str(margin[0]),
            'upper_gap_note':'No claim that this upper gap bounds the true gap; only the lower bound is used.'}
    write('D/true_rate_Jensen.json',jensen)
    check('true_rate_Jensen_margin',margin[0]>0,jensen,'UNRESOLVED_TRUE_RATE_CERTIFICATE')
    true_points={}
    for point in spec['points']:
        key=str(Q(point['t']))
        hsecond=conditional[key][1]
        tail=diq(point_tails[key])
        true=diadd(hsecond,(tail[1].copy_negate(),tail[1]))
        threshold=diq(Q(point['threshold']))
        strict_margin=LOW.subtract(threshold[0],true[1])
        record={'t':point['t'],'finite_h18second':direcord(hsecond),'Tail18_exact':point_tails[key],
                'Tail18_outward':direcord(tail),'true_curvature':{'lower':str(true[0]),'upper':str(true[1]),
                    'total_width_upper':str(HIGH.subtract(true[1],true[0])),
                    'width_note':'Includes the separate analytic tail; not the finite arithmetic error.'},
                'threshold':point['threshold'],'strict_margin_lower':str(strict_margin)}
        true_points[key]=record
        write('D/true_curvature_t'+str(int(2*Q(key)))+'.json',record)
        check('true_curvature_margin_t'+key,strict_margin>0,record,'UNRESOLVED_TRUE_CURVATURE_CERTIFICATE')
    write('D/final_contexts.json',{'floor':context_record(LOW),'ceiling':context_record(HIGH),'ln_nearest':context_record(NEAR)})
    return {'status':'MACHINE_PASS','scope':'PR77 original fixed t=1/2,1,3/2, r18,n18/19 only',
            'true_Jensen':jensen,'true_curvatures':true_points,'mathematical_review':'not supplied'}


def main():
    global OUT,DEADLINE,PHASE
    parser=argparse.ArgumentParser()
    parser.add_argument('--input-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    OUT=args.out
    OUT.mkdir(parents=True,exist_ok=True)
    DEADLINE=int(os.environ['C2_ABSOLUTE_DEADLINE_EPOCH'])
    write('environment.json',{'pid':os.getpid(),'start_utc':utc(),'deadline_epoch':DEADLINE,
          'deadline_utc':datetime.fromtimestamp(DEADLINE,timezone.utc).isoformat(),
          'source_commit':os.environ.get('C2_PRODUCTION_SOURCE_COMMIT'),
          'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),
          'affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':resource.getrlimit(resource.RLIMIT_AS),
          'thread_settings':{key:os.environ.get(key) for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']},
          'decimal_version':decimal.__version__,'libmpdec_version':getattr(decimal,'__libmpdec_version__','unavailable'),
          'clock':'external immutable2700second deadline started before this Python/package loading'})
    code=0
    try:
        tick()
        spec=json.loads((args.input_root/'fixed.json').read_text(encoding='utf-8-sig'))
        write('input_echo.json',spec)
        check('frozen_scope',spec['author_head']=='6ebe38dc6503120d47e9d644cfac78cfb43666f5' and
              list(map(Q,spec['parameters']))==[Q(1,2),Q(1),Q(3,2)] and spec['depth']==18 and spec['lengths']==[18,19] and
              spec['decimal_precision']==100 and DEC(spec['ln_widening'])==WIDEN and DEC(spec['finite_width_limit'])==WIDTH)
        E18,tails=phase_a(spec)
        phase_b(spec)
        PHASE='C_production_complete_event_jets'
        progress('start')
        all_histograms={}
        for value in spec['parameters']:
            t=Q(value)
            all_histograms[str(t)]=produce_point(t)
        result=phase_d(spec,all_histograms,E18,tails)
    except Halt as exc:
        result={'status':exc.state,'first_gate':exc.gate,'phase':PHASE}
        code=124 if exc.state=='TIMEOUT' else 20
    except MemoryError:
        result={'status':'MEMORY_LIMIT','phase':PHASE}
        code=125
    except Exception as exc:
        write('MECHANICAL_EXCEPTION.json',{'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
        result={'status':'MECHANICAL_EXCEPTION','phase':PHASE,'type':type(exc).__name__}
        code=30
    write('decimal_contexts_at_exit.json',{'floor':context_record(LOW),'ceiling':context_record(HIGH),'ln_nearest':context_record(NEAR)})
    result.update({'pid':os.getpid(),'finish_utc':utc(),'elapsed_seconds':time.monotonic()-START,
                   'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'checks':CHECKS,
                   'exit_code':code,'deadline_epoch':DEADLINE})
    write('STATUS.json',result)
    manifest=[]
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name not in ['output_hashes.json','stdout.log','stderr.log','exit.json']:
            manifest.append({'path':path.relative_to(OUT).as_posix(),'bytes':path.stat().st_size,
                             'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    write('output_hashes.json',manifest)
    print(json.dumps({'status':result['status'],'phase':PHASE,'pid':os.getpid(),'exit_code':code,
                      'elapsed_seconds':result['elapsed_seconds']},separators=(',',':')),flush=True)
    return code


def recurrence_event(n,a,word,horizon=None):
    tables=transitions(n if horizon is None else horizon,a)
    state=[0]*18
    state[0]=1  # mask3: the two negative-index dummy columns are occupied.
    parity=1
    for i in range(n):
        occupied=(word>>i)&1
        state=advance(state,tables[i][occupied])
        if not occupied:
            parity=-parity
    return tuple(parity*state[j] for j in range(3))


def phase_b(spec):
    global PHASE
    PHASE='B_small_independent_crosschecks'
    progress('start')
    counts={'mobius_word_cases':0,'direct_word_cases':0,'jet_word_cases':0}
    for literal_t in spec['parameters']:
        t=Q(literal_t)
        a=int(2*t)
        for n in range(1,9):
            mobius=None
            if n<=6:
                K=integer_kernel(n,a)
                inc=[]
                for subset in range(1<<n):
                    ids=[i for i in range(n) if subset&(1<<i)]
                    inc.append(bareiss([[K[i][j] for j in ids] for i in ids])*32**(n-len(ids)))
                mobius=list(inc)
                # In-place upper-set Mobius inversion, no absent-diagonal/sign helper.
                for bit in range(n):
                    for subset in range(1<<n):
                        if not subset&(1<<bit):
                            mobius[subset]-=mobius[subset|(1<<bit)]
            audit=hashlib.sha256()
            for word in range(1<<n):
                tick()
                N,N1,N2=recurrence_event(n,a,word)
                matrix,direct,sign=direct_event(n,a,word)
                check(f'direct_t{t}_n{n}_word{word}',N==direct,{'N':str(N),'direct':str(direct)})
                counts['direct_word_cases']+=1
                if n<=6:
                    check(f'prefix_harvest_t{t}_n{n}_word{word}',
                          (N,N1,N2)==recurrence_event(n,a,word,n+1))
                    check(f'mobius_t{t}_n{n}_word{word}',N==mobius[word],{'N':str(N),'mobius':str(mobius[word])})
                    counts['mobius_word_cases']+=1
                    J1,J2=direct_derivatives(matrix,sign)
                    check(f'jets_t{t}_n{n}_word{word}',(N1,N2)==(J1,J2),
                          {'recurrence':[str(N1),str(N2)],'row_derivatives':[str(J1),str(J2)]})
                    counts['jet_word_cases']+=1
                audit.update(f'{word}:{N}:{N1}:{N2}\n'.encode('ascii'))
            write(f'B/t{a}_n{n}.json',{'t':t,'n':n,'all_word_count':1<<n,
                  'event_jet_sha256':audit.hexdigest(),'all_agreements':True,
                  'value_routes':['frontier permutation recurrence','pivoted Bareiss signed determinant']+
                  (['inclusion determinants and Mobius inversion'] if n<=6 else []),
                  'jet_route':'multilinear row replacement determinants' if n<=6 else 'not requested'})
        progress('parameter_complete',t=t,counts=counts)
    write('B/coverage.json',counts|{'n_ranges':spec['small_checks'],'jet_parameter':'physical t; first offdiagonal derivative2'})
    check('small_coverage_counts',counts=={'mobius_word_cases':378,'direct_word_cases':1530,'jet_word_cases':378},counts)


def gzip_chunks(relative_prefix,rows,schema,rows_per_chunk=25000):
    """Deterministic gzip (mtime0), data-only JSONL chunks with byte hashes."""
    prefix=OUT/relative_prefix
    prefix.parent.mkdir(parents=True,exist_ok=True)
    files=[]
    gz=None
    raw=None
    count=0
    chunk=0
    path=None
    def finish():
        if gz is not None:
            gz.close()
            raw.close()
            files.append({'path':path.relative_to(OUT).as_posix(),'rows':count,
                          'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    try:
        for row in rows:
            if count==0 or count==rows_per_chunk:
                finish()
                path=prefix.with_name(prefix.name+f'_{chunk:03d}.jsonl.gz')
                raw=path.open('wb')
                gz=gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=1)
                count=0
                chunk+=1
            gz.write((json.dumps(row,separators=(',',':'))+'\n').encode('ascii'))
            count+=1
            if count%1024==0:
                tick()
        finish()
        gz=None
        raw=None
    finally:
        if gz is not None:
            gz.close()
        if raw is not None:
            raw.close()
    manifest={'schema':schema,'compression':'gzip level1,mtime0,ASCII JSONL,all integer fields decimal strings',
              'ordering':'ascending integer N','chunks':files}
    write(relative_prefix+'_manifest.json',manifest)
    return manifest


def produce_point(t):
    a=int(2*t)
    tables=transitions(19,a)
    histograms={18:{},19:{}}
    audits={n:hashlib.sha256() for n in [18,19]}
    counts={18:0,19:0}
    totals={18:[0,0,0],19:[0,0,0]}
    minima={18:None,19:None}
    state=[0]*18
    state[0]=1

    def record(depth,word,parity,current):
        N,N1,N2=(parity*current[j] for j in range(3))
        if N<=0:
            check('production_event_positive',False,{'t':t,'n':depth,'word':word,'jets':[str(N),str(N1),str(N2)]},'FAILED_POSITIVITY')
        bucket=histograms[depth].get(N)
        if bucket is None:
            histograms[depth][N]=[1,N1,N2,N1*N1]
        else:
            bucket[0]+=1
            bucket[1]+=N1
            bucket[2]+=N2
            bucket[3]+=N1*N1
        counts[depth]+=1
        totals[depth][0]+=N
        totals[depth][1]+=N1
        totals[depth][2]+=N2
        minima[depth]=N if minima[depth] is None else min(minima[depth],N)
        audits[depth].update(f'{word}:{N}:{N1}:{N2}\n'.encode('ascii'))
        if counts[depth]%65536==0:
            progress('enumeration_checkpoint',t=t,n=depth,event_count=counts[depth],distinct=len(histograms[depth]))

    def visit(i,current,word,parity):
        if i>=18:
            record(i,word,parity,current)
        if i==19:
            return
        visit(i+1,advance(current,tables[i][0]),word,-parity)
        visit(i+1,advance(current,tables[i][1]),word|(1<<i),parity)

    visit(0,state,0,1)
    result={}
    for n in [18,19]:
        histogram=histograms[n]
        record_out={'t':t,'n':n,'event_count':counts[n],'sum_N':str(totals[n][0]),
                    'sum_Nprime':str(totals[n][1]),'sum_Nsecond':str(totals[n][2]),
                    'positive_minimum_N':str(minima[n]),'distinct_N':len(histogram),
                    'deterministic_word_jet_sha256':audits[n].hexdigest(),
                    'enumeration_order':'depth-first bit0 then bit1, site index increases; word integer uses site i as bit i',
                    'depth18_harvest':'frontier mask3 at depth18 excludes every selected outside column; same leading18 determinant'}
        write(f'C/t{a}_n{n}_totals.json',record_out)
        check(f'production_counts_t{a}_n{n}',counts[n]==1<<n,record_out)
        check(f'production_normalization_t{a}_n{n}',totals[n]==[32**n,0,0],record_out)
        check(f'production_minimum_t{a}_n{n}',minima[n]>0,record_out,'FAILED_POSITIVITY')
        # Histograms are independently sufficient for both value and curvature sums.
        aggregation=[sum(v[0] for v in histogram.values()),sum(N*v[0] for N,v in histogram.items()),
                     sum(v[1] for v in histogram.values()),sum(v[2] for v in histogram.values())]
        check(f'aggregation_normalization_t{a}_n{n}',aggregation==[1<<n,32**n,0,0],aggregation)
        gzip_chunks(f'C/t{a}_n{n}_histogram',
                    ([str(N)]+[str(x) for x in histogram[N]] for N in sorted(histogram)),
                    ['N','count','sum_Nprime','sum_Nsecond','sum_Nprime_squared'])
        result[n]=histogram
    progress('point_enumeration_complete',t=t)
    return result


if __name__=='__main__':
    raise SystemExit(main())
