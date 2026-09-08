"""Controlled rank-two sign flip, nine existing vector pairs, no new RNG."""
from probe import *

target=OUT/'paired_sign_diagnostic.json'
if target.exists(): raise FileExistsError('Paired-sign diagnostic already exists')
old=list(csv.DictReader((OUT/'candidate_ledger.csv').open(encoding='utf-8')))
chosen={}
for r in old:
    if r['kind']=='DIRECTION': chosen.setdefault((r['n'],r['gamma']),r['id'])
rows=[]; started=time.time()
for (ns,gs),key in chosen.items():
    data=json.loads((OUT/'parameters'/f'{key}.json').read_text(encoding='utf-8'))
    n=int(ns); gamma=F(gs); c=F(data['c']); u=data['u']; v=data['v']; uu=sum(x*x for x in u); vv=sum(x*x for x in v)
    M=baseline(n,gamma); K=arr(M); E=Events(n); p0=E.evaluate(K); i0=E.info(p0); directions={}
    for sign in (-1,1): directions[sign]=[[F(u[i]*u[j],uu)+sign*c*F(v[i]*v[j],vv) for j in range(n)] for i in range(n)]
    bound=min(limit(M,D,E.na) for D in directions.values())
    pair=dict(n=n,gamma=gs,source_id=key,u=u,v=v,c=str(c),common_step_limit=bound,chords=[])
    for fraction in (.2,.5,.85):
        t=F(math.floor(bound*fraction*10**6),10**6); signed=[]
        for sign,D in directions.items():
            Mm,Mp=combine(M,D,-t),combine(M,D,t); pm,pp=E.evaluate(arr(Mm)),E.evaluate(arr(Mp)); im,ip=E.info(pm),E.info(pp)
            q=(pm+pp)/2; r=q-p0; geom=float(-r@np.log(p0)); kl=float(q@np.log(q/p0)); js=entropy(q)-(im['E']+ip['E'])/2
            gap=(im['E']+ip['E'])/2-i0['E']; da=(im['A']+ip['A'])/2-i0['A']; db=(im['B']+ip['B'])/2-i0['B']; bump=i0['I']-(im['I']+ip['I'])/2
            mob=None
            if n<=8 and fraction==.85: mob=max(float(max(abs(E.mobius(arr(Mm))-pm))),float(max(abs(E.mobius(arr(Mp))-pp))))
            row=dict(sign=sign,exact_rank=2,inertia=[2,0,n-2] if sign==1 else [1,1,n-2],not_thinning_reason='direction rank 2 versus positive-definite center rank n',step=str(t),Delta_E=gap,Delta_A=da,Delta_B=db,MI_bump=bump,marginal_deficit_sum=-da-db,geometry_term=geom,KL_cost=kl,JS_cost=js,geometry_to_cost_ratio=geom/(kl+js),geometry_identity_residual=gap-geom+kl+js,information_identity_residual=gap-da-db-bump,mobius_max_error=mob,certificates=[certificate(Mm),certificate(M),certificate(Mp)],cross_norm_min=coupling_min_exact(M,D,t,E.na),status='FLOAT_CANDIDATE' if gap>0 else 'NO_SIGNAL')
            if gap>0: row['high_precision']=[high_precision(M,D,t,60),high_precision(M,D,t,100)]
            signed.append(row)
        pair['chords'].append(dict(fraction=fraction,sign_flip_geometry_residual=signed[0]['geometry_term']+signed[1]['geometry_term'],signed_results=signed))
    rows.append(pair)
    print(json.dumps(dict(n=n,gamma=gs,plus_gap=pair['chords'][1]['signed_results'][1]['Delta_E'],plus_geometry=pair['chords'][1]['signed_results'][1]['geometry_term'],plus_geometry_cost_ratio=pair['chords'][1]['signed_results'][1]['geometry_to_cost_ratio'])),flush=True)
flat=[z for row in rows for c in row['chords'] for z in c['signed_results']]; plus=[r for r in flat if r['sign']==1]
summary=dict(existing_vector_pairs=len(rows),new_random_proposals=0,chords=len(flat),PSD_chords=len(plus),positive_PSD_geometry_terms=sum(r['geometry_term']>0 for r in plus),positive_MI_bumps=sum(r['MI_bump']>0 for r in flat),float_candidates=sum(r['status']=='FLOAT_CANDIDATE' for r in flat),max_PSD_geometry_cost_ratio=max(r['geometry_to_cost_ratio'] for r in plus),max_PSD_gap=max(r['Delta_E'] for r in plus),max_geometry_flip_residual=max(abs(c['sign_flip_geometry_residual']) for row in rows for c in row['chords']),max_mobius_error=max(r['mobius_max_error'] for r in flat if r['mobius_max_error'] is not None),elapsed=time.time()-started,exit_code=0)
target.write_text(json.dumps(dict(summary=summary,rows=rows),indent=2),encoding='utf-8'); print(json.dumps(summary),flush=True)
