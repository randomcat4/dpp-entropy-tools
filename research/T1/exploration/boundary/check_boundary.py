#!/usr/bin/env python3
"""Bounded exact fixtures; no random search, numerical differentiation, or dependencies."""
from fractions import Fraction as F
import json, math, os, platform, resource, time
from pathlib import Path
start = time.perf_counter()
checks = 0
events_evaluated = 0
def check(condition):
    global checks
    checks += 1
    assert condition
def p2(a,b,x,y=F(0)):
    global events_evaluated
    events_evaluated += 4
    q=x*x+y*y
    return {'00':(1-a)*(1-b)-q,'10':a*(1-b)+q,
            '01':(1-a)*b+q,'11':a*b-q}
def strs(p):
    return {k:str(v) for k,v in p.items()}
fixtures=[]
for c in [F(0),F(1,8),F(1,4)]:
    p=p2(F(1,2),F(1,2),c)
    pplus=p2(F(1,2),F(1,2),c,F(1,16))
    pminus=p2(F(1,2),F(1,2),c,F(-1,16))
    check(sum(p.values())==1 and min(p.values())>0)
    check(min(pplus.values())>0 and pplus==pminus)
    pp={s:(pplus[s]+pminus[s]-2*p[s])*256 for s in p}
    check(pp=={'00':F(-2),'10':F(2),'01':F(2),'11':F(-2)})
    ratio=p['00']*p['11']/(p['10']*p['01'])
    check(ratio<=1)
    check(p['10']*p['01']-p['00']*p['11']==c*c)
    fixtures.append({'name':'pure_imaginary_c='+str(c),'p':strs(p),
      'p_prime':'all zero','p_second':strs(pp),'odds_ratio':str(ratio),
      'H_second_exact':'2 log('+str(ratio)+')',
      'H_second_float_diagnostic':2*math.log(float(ratio))})
p=p2(F(1,2),F(1,2),F(0))
h=F(1,16)
pp=p2(F(1,2)+h,F(1,2),F(0))
pm=p2(F(1,2)-h,F(1,2),F(0))
der={s:(pp[s]-pm[s])/(2*h) for s in p}
second={s:(pp[s]+pm[s]-2*p[s])/(h*h) for s in p}
check(all(v==0 for v in second.values()))
curv=-sum(der[s]**2/p[s] for s in p)
check(curv==-4)
fixtures.append({'name':'same_center_rank_one_direction',
                 'p':strs(p),'p_prime':strs(der),'H_second_exact':str(curv)})
# Infeasible affine tangent to a rank-one projection. Probabilities are merely
# determinant-polynomial evaluations here, NOT a probability distribution.
bad=p2(F(1),F(0),F(0),h)
check(bad['11']==-h*h and bad['00']==-h*h)
fixtures.append({'name':'infeasible_affine_projection_tangent','t':str(h),
                 'determinant_polynomials':strs(bad)})
# Feasible nonlinear rank-one projection onto span((1,i*t)).
r=F(1)+h*h
pn=p2(1/r,h*h/r,F(0),-h/r)
check(pn=={'00':F(0),'10':1/r,'01':h*h/r,'11':F(0)})
fixtures.append({'name':'nonlinear_projection','t':str(h),'p':strs(pn),
                 'entropy_exact':'log(1+t^2)-t^2/(1+t^2)*log(t^2)'})
# Two-sided affine boundary path diag(1,1/2+t,0) has constant support.
support=[]
for t in [-h,F(0),h]:
    vals={format(s,'03b'):F(0) for s in range(8)}
    vals['100']=F(1,2)-t
    vals['110']=F(1,2)+t
    events_evaluated+=8
    check(sum(vals.values())==1 and min(vals.values())==0)
    support.append([s for s,p in vals.items() if p>0])
check(support[0]==support[1]==support[2]==['100','110'])
fixtures.append({'name':'affine_boundary_fixed_face','support':support[0]})
report={'status':'COMPLETED_EXACT_FIXTURES_NOT_INDEPENDENT_CERTIFICATION',
        'fixture_count':len(fixtures),'assertions_passed':checks,
        'event_values_evaluated':events_evaluated,
        'max_matrix_dimension':3,'random_samples':0,'parameter_searches':0,
        'python':platform.python_version(),'pid':os.getpid(),
        'thread_limits':{v:os.getenv(v) for v in
          ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},
        'elapsed_seconds':time.perf_counter()-start,
        'cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime+
                       resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'fixtures':fixtures}
Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
