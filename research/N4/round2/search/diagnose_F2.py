"""Read existing F2 direction decompositions; no new search evaluations."""
import json
from pathlib import Path

base=Path(__file__).parent/'F2'
records=[json.loads(x) for x in (base/'cases.jsonl').read_text().splitlines()]
rows=[]
for r in records:
    for dr in r['directions']:
        top=dr['top_layer'];g=float(top['geometry_c_ddet']);f=float(top['fisher_positive'])
        layers=[]
        for old in dr['cardinality_layers']:
            layer={k:float(v) if k!='cardinality' else v for k,v in old.items()}
            layer['mass_second']=sum(float(dr['event_ddp'][i]) for i,s in enumerate(r['support_masks']) if s.bit_count()==layer['cardinality'])
            layer['literal_layer_entropy_second']=layer['curvature']-layer['mass_second']
            layers.append(layer)
        rows.append(dict(index=r['index'],frame=r['meta']['frame_index'],spectrum=r['meta']['spectrum_name'],
            direction=dr['name'],curvature=float(dr['curvature']),acceleration=float(dr['acceleration']),
            negative_fisher=float(dr['negative_fisher']),entropy_q=float(r['entropy_q']),
            geometry=g,top_fisher=f,geometry_over_fisher=g/f if f>1e-25 else None,
            top_base_acceleration=float(top['base_acceleration_minus_ddet_logdet']),
            top_total=float(top['total']),lower_total=sum(float(l['curvature']) for l in dr['cardinality_layers'][:3]),
            literal_top_entropy_second=layers[3]['literal_layer_entropy_second'],
            literal_lower_entropy_second=sum(x['literal_layer_entropy_second'] for x in layers[:3]),
            layers=layers,
            commutator_norm=dr['commutator_norm'],geometry_exceeds_top_fisher=top['geometry_exceeds_top_fisher']))
summary=dict(status='F2_DIAGNOSTIC_NO_NEW_CENTERS',centers=len(records),directions=len(rows),
    layer_convention='curvature C_k=-sum(dp^2/p+ddp*logp); sum C_k=Hsecond; literal layer entropy second=C_k-mass_second',
    noncommuting_directions=sum(x['commutator_norm']>1e-10 for x in rows),
    geometry_nonpositive=sum(x['geometry']<=0 for x in rows),
    geometry_positive_within_top_fisher=sum(0<x['geometry']<=x['top_fisher'] for x in rows),
    geometry_exceeds_top_fisher=sum(x['geometry_exceeds_top_fisher'] for x in rows),
    positive_top_total=sum(x['top_total']>0 for x in rows),
    positive_literal_top_entropy_second=sum(x['literal_top_entropy_second']>0 for x in rows),
    positive_total_acceleration=sum(x['acceleration']>0 for x in rows),
    highest_curvature=max(rows,key=lambda x:x['curvature']),
    highest_geometry_ratio=max((x for x in rows if x['geometry_over_fisher'] is not None),key=lambda x:x['geometry_over_fisher']),
    highest_top_total=max(rows,key=lambda x:x['top_total']),
    frames=[dict(frame=fi,entropy_q=float(next(r['entropy_q'] for r in records if r['meta']['frame_index']==fi)),
                 maximum_curvature=max(r['lambda_max'] for r in records if r['meta']['frame_index']==fi)) for fi in range(3)],
    all_rows=rows)
(base/'mechanism_diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n')
selected=[]
for label,row in [('highest_geometry_ratio',summary['highest_geometry_ratio']),('highest_total_curvature',summary['highest_curvature'])]:
    record=next(r for r in records if r['index']==row['index'])
    direction=next(d for d in record['directions'] if d['name']==row['direction'])
    selected.append(dict(label=label,index=record['index'],meta=record['meta'],
        U=record['U'],A=record['A'],V=direction['V'],chords=direction['chords'],
        q_triple=record['q_triple'],entropy_q=record['entropy_q'],
        determinant_jets_exact=direction['determinant_jets_exact'],
        top_layer=direction['top_layer'],decomposition=row,
        curvature=direction['curvature'],fisher_negative=direction['negative_fisher'],
        acceleration=direction['acceleration']))
(base/'selected_mechanism_cases.json').write_text(json.dumps(dict(
    status='FROZEN_NUMERICAL_NEGATIVE_EXAMPLES_NOT_CERTIFICATES',
    source='F2/cases.jsonl; postprocessing only, no additional kernel evaluations',
    layer_convention=summary['layer_convention'],cases=selected),indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='all_rows'},indent=2))
