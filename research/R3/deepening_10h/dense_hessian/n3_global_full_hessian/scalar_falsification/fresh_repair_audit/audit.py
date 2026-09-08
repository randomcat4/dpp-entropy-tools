"""Fresh non-author U10c repair reconstruction; no research modules imported."""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
from fractions import Fraction as Q
from decimal import Decimal as R,localcontext
from pathlib import Path
import json,hashlib,time,itertools
HERE=Path(__file__).resolve().parent
SRC=HERE.parent
COORD=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))
NAMES=('0','1','2','12','3','13','23','123')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decimal(q):return R(q.numerator)/R(q.denominator) if isinstance(q,Q) else R(q)
def determinant(a):
    n=len(a)
    if n==0:return Q(1)
    if n==1:return a[0][0]
    if n==2:return a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return sum((-1)**j*a[0][j]*determinant([[a[i][k] for k in range(3) if k!=j] for i in (1,2)]) for j in range(3))
def adj(a):
    return [[(-1)**(i+j)*determinant([[a[k][l] for l in range(3) if l!=i] for k in range(3) if k!=j]) for j in range(3)] for i in range(3)]
def principal_certificate(K):
    p=[determinant([r[:n] for r in K[:n]]) for n in (1,2,3)]
    return p
def events(K):
    p=[];g=[]
    for s in range(8):
        M=[[K[i][j]-Q(i==j and not(s>>i&1)) for j in range(3)] for i in range(3)]
        sign=(-1)**(3-s.bit_count());co=adj(M)
        p.append(sign*determinant(M));g.append([sign*co[i][j]*(1 if i==j else 2) for i,j in COORD])
    # Separate inclusion-Mobius reconstruction of atoms and first jets.
    inc=[];ig=[]
    for s in range(8):
        ids=[i for i in range(3) if s>>i&1]
        inc.append(determinant([[K[i][j] for j in ids] for i in ids]));row=[]
        for i,j in COORD:
            if i not in ids or j not in ids:row.append(Q(0));continue
            ii=ids.index(i);jj=ids.index(j)
            cof=(-1)**(ii+jj)*determinant([[K[k][l] for l in ids if l!=j] for k in ids if k!=i])
            row.append(cof*(1 if i==j else 2))
        ig.append(row)
    for i in range(3):
        for s in range(8):
            if not(s>>i&1):
                inc[s]-=inc[s|1<<i];ig[s]=[a-b for a,b in zip(ig[s],ig[s|1<<i])]
    assert inc==p and ig==g and sum(p)==1
    assert all(sum(row[i] for row in g)==0 for i in range(6))
    return p,g
def solve(a,b):
    a=[row[:]+[b[i]] for i,row in enumerate(a)]
    n=len(a)
    for k in range(n):
        i=max(range(k,n),key=lambda i:abs(a[i][k]));a[k],a[i]=a[i],a[k]
        pivot=a[k][k];assert pivot
        for j in range(k,n+1):a[k][j]/=pivot
        for i in range(n):
            if i==k:continue
            factor=a[i][k]
            for j in range(k,n+1):a[i][j]-=factor*a[k][j]
    return [row[-1] for row in a]
def inverse(a):
    cols=[solve(a,[R(i==j) for i in range(len(a))]) for j in range(len(a))]
    return [list(row) for row in zip(*cols)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def inner(x,y):return sum(a*b for a,b in zip(x,y))
def evaluate(K,precision,detail=False):
    p,g=events(K)
    kp=principal_certificate(K);ip=principal_certificate([[Q(i==j)-K[i][j] for j in range(3)] for i in range(3)])
    if min(p)<=0 or min(kp+ip)<=0:
        return {'status':'REJECT_EXACT_NONSTRICT','minimum_atom':str(min(p)),
                'K_principal_minors':list(map(str,kp)),'IK_principal_minors':list(map(str,ip))}
    with localcontext() as ctx:
        ctx.prec=precision
        pp=list(map(decimal,p));kk=[[decimal(x) for x in row] for row in K]
        l12=decimal(p[0]*p[3]/(p[1]*p[2])).ln()
        l13=decimal(p[0]*p[5]/(p[1]*p[4])).ln()
        l23=decimal(p[0]*p[6]/(p[2]*p[4])).ln()
        lam=decimal(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6])).ln()
        N=[[-lam*kk[i][j] for j in range(3)] for i in range(3)]
        for i,l in enumerate((l23,l13,l12)):N[i][i]-=l
        assert min(principal_certificate(N))>0
        ni=inverse(N);delta=determinant(N)
        bases=[]
        for i,j in COORD:
            E=[[R(0)]*3 for _ in range(3)];E[i][j]=E[j][i]=R(1);bases.append(E)
        products=[mm(ni,E) for E in bases];eta=[tr(v) for v in products]
        # Exact rational score products, only logarithms and solves are Decimal.
        Fisher=[[sum(decimal(g[s][i]*g[s][j]/p[s]) for s in range(8)) for j in range(6)] for i in range(6)]
        A=[[Fisher[i][j]+delta*tr(mm(products[i],products[j])) for j in range(6)] for i in range(6)]
        z=solve(A,eta);rho=delta*inner(eta,z)
        residual=max(abs(inner(row,z)-eta[i]) for i,row in enumerate(A))/max(R(1),max(map(abs,eta)))
        result={'status':'SCOUT_RECOMPUTED','rho':str(rho),'one_minus_rho':str(1-rho),'precision':precision,
                'min_atom':str(min(p)),'Lambda':str(lam),'all_exact_atoms_and_jets_match_Mobius':True,
                'exact_strict_principal_minors_positive':True,'solve_relative_residual':str(residual)}
        assert residual<R(10)**(-40) and rho<1
        if detail:
            result.update({'K':[[str(v) for v in row] for row in K],'atoms':dict(zip(NAMES,map(str,p))),
              'correct_p0_jet':list(map(str,g[0])),'Fisher':[[str(v) for v in row] for row in Fisher],
              'N':[[str(v) for v in row] for row in N],'eta':list(map(str,eta)),'detN':str(delta)})
        return result
def boundary_K(theta,k,rates,complement):
    O=[[Q(1,3),Q(2,3),Q(2,3)],[Q(2,3),Q(1,3),Q(-2,3)],[Q(2,3),Q(-2,3),Q(1,3)]]
    assert mm(O,[list(r) for r in zip(*O)])==[[Q(i==j) for j in range(3)] for i in range(3)]
    eigen=[Q(1,10**(k*rates[0])),Q(1,10**(k*rates[1])),Q(theta)]
    K=[[sum(O[i][z]*eigen[z]*O[j][z] for z in range(3)) for j in range(3)] for i in range(3)]
    return [[Q(i==j)-K[i][j] for j in range(3)] for i in range(3)] if complement else K
def key(r):return (r['theta'],r['k'],tuple(r['rates']),r['complement'])
def main():
    started=time.time();files=[SRC/n for n in ('rho_scalar_search.py','search_ledger.json','near_threshold_candidates.json','repair_status.md','verdict.md','run_log.md')]
    hashes={p.name:sha(p) for p in files};ledger=json.loads(files[1].read_text());art=json.loads(files[2].read_text())
    assert hashes['rho_scalar_search.py']==ledger['script_sha256']
    stats=ledger['route_stats']
    assert sum(v['attempted'] for v in stats.values())==ledger['attempted_float_total']==38436
    assert sum(v['accepted'] for v in stats.values())==ledger['accepted_float_total']==22023
    for row in stats.values():assert row['attempted']==row['accepted']+row['rejected'] and sum(row['reject_breakdown'].values())==row['rejected']
    assert art['top_float_decimal_rechecks']==ledger['decimal_top_float_rechecks']
    assert len(art['top_float_decimal_rechecks'])==15 and len(art['lambda0_path_decimal_probes'])==150
    assert len(art['near_threshold_candidates'])==40 and len(art['positive_candidates_rho_gt_1'])==0
    assert ledger['decimal_boundary_probe_count']==280
    assert art['top_float_candidates'][:25]==ledger['top_float']
    stored_boundary={key(r):r for r in art['near_threshold_candidates'] if r['route']=='decimal_rank_one_rate_extremes'}
    allrows=[];top=[];boundary=[];paths=[]
    print('Frozen accounting passes; independent exact jets and scalar recomputation begins',flush=True)
    for rec in art['top_float_decimal_rechecks']:
        K=[[Q(str(v)) for v in row] for row in rec['K']]
        item=evaluate(K,max(rec.get('dps',200)+80,240),detail=rec['source_rank_float']==0)
        item.update({'route':'top_float','source_rank':rec['source_rank_float'],'author_status':rec['status'],'source_rho_float':rec['source_rho_float']})
        if rec.get('ok'):
            assert item['status']=='SCOUT_RECOMPUTED' and abs(R(item['rho'])-R(rec['rho']))<R('1e-50')
        else:assert item['status']=='REJECT_EXACT_NONSTRICT'
        top.append(item)
    rates=((1,1),(1,2),(1,3),(2,3),(1,5),(2,5),(1,8))
    for theta,k,rate,comp in itertools.product(('0.1','0.5','0.9','0.99'),(8,16,32,64,96),rates,(False,True)):
        meta={'theta':theta,'k':k,'rates':list(rate),'complement':comp}
        detail=(theta=='0.99' and k==96 and rate==(1,1) and not comp) or (theta=='0.5' and k==96 and rate==(2,3) and not comp)
        item=evaluate(boundary_K(theta,k,rate,comp),max(240,2*max(rate)*k+180),detail=detail)
        item.update(meta);item['route']='boundary';assert item['status']=='SCOUT_RECOMPUTED'
        rec=stored_boundary.get(key(meta))
        if rec:assert abs(R(item['rho'])-R(rec['rho']))<R('1e-40')
        boundary.append(item)
        if len(boundary)%40==0:print('Boundary rows',len(boundary),'/ 280',flush=True)
    combos=set()
    for rec in art['lambda0_path_decimal_probes']:
        diag=list(map(Q,rec['diag']));weights=list(map(Q,rec['weights']));eps=Q(1,10**rec['k'])
        combo=(tuple(diag),tuple(weights),rec['k']);assert combo not in combos;combos.add(combo)
        K=[[diag[i] if i==j else Q(0) for j in range(3)] for i in range(3)]
        K[0][1]=K[1][0]=eps*weights[0];K[1][2]=K[2][1]=eps*weights[1]
        item=evaluate(K,max(rec['dps']+80,240));item.update({'route':'lambda0_path','diag':rec['diag'],'weights':rec['weights'],'k':rec['k']})
        assert item['status']=='SCOUT_RECOMPUTED' and abs(R(item['rho'])-R(rec['rho']))<R('1e-50')
        paths.append(item)
    assert len(combos)==5*5*6
    allrows=top+boundary+paths;valid=[r for r in allrows if r['status']=='SCOUT_RECOMPUTED']
    near=sum(R(r['rho'])>R('.95') for r in valid)
    assert near==ledger['decimal_near_threshold_count']
    assert len(valid)==444 and len(allrows)==445 and len(boundary)==280
    best=max(valid,key=lambda r:R(r['rho']));unequal=max((r for r in boundary if r['rates'][0]!=r['rates'][1]),key=lambda r:R(r['rho']))
    unchanged=all(sha(p)==hashes[p.name] for p in files);assert unchanged
    result={'status':'SCOUT_FRESH_NONAUTHOR_RECHECK','frozen_sha256':hashes,'inputs_unchanged':unchanged,
      'float_accounting':{'scope':'compact aggregate arithmetic, not full float seed regeneration','attempts':38436,'accepted_by_float_screen':22023,'route_stats':stats},
      'denominator':{'top_attempts':15,'top_valid':14,'top_exact_rejected':1,'boundary':280,'path':150,'total_attempts':445,'valid':444,'rho_gt_one':0,'rho_gt_point95':near},
      'best':best,'best_unequal':unequal,'float_hazard':top[0],'rows':allrows,
      'findings':['Author verdict stale: says 54 near-threshold records; frozen ledger and fresh reconstruction give 69.',
                  'One of 15 top-float rechecks is an exact nonstrict rejection; 15 is an attempts denominator.',
                  'Author verdict elapsed time differs from frozen run log/ledger; timing is provenance metadata only.',
                  'Compact ledger does not contain all 38436 raw float proposals. Full float seed regeneration is INCOMPLETE.'],
      'implementation_scope':'No author script or previous audit imports. Exact rational signed-event adjugate jets crosschecked with direct inclusion Mobius; independent Decimal Fisher/N/rho. Boundary input uses exact rational orthogonal Q rather than finite-precision thirds.',
      'source_sha256':sha(Path(__file__)),'exit_code':0,'elapsed_seconds':time.time()-started}
    (HERE/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'status':'SCOUT','best_rho':best['rho'][:65],'unequal':unequal['rho'][:65],'near':near,'valid':len(valid),'seconds':result['elapsed_seconds'],'exit_code':0}),flush=True)
if __name__=='__main__':main()
