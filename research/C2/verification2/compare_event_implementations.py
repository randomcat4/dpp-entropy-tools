"""Exact cross-check of independently generated event jets, not a sign proof."""
import argparse
import json
import os
import platform
from fractions import Fraction
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reference',required=True)
    parser.add_argument('--candidate',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--allow-subset',action='store_true',
                        help='Compare an explicitly selected nonempty subset of frozen reference centers')
    args=parser.parse_args()
    reference=json.loads(Path(args.reference).read_text(encoding='utf-8-sig'))
    candidate=json.loads(Path(args.candidate).read_text(encoding='utf-8-sig'))
    assert reference['hessian_upper_order']==candidate['pair_index_order']
    assert ['a'+s for s in reference['coordinates']]==candidate['coordinate_order']
    refs={c['name']:c for c in reference['cases']}
    cands={c['name']:c for c in candidate['centers']}
    if args.allow_subset:
        assert cands and set(cands)<=set(refs)
        refs={name:refs[name] for name in cands}
    else:
        assert set(refs)==set(cands)
    count=0
    for name in refs:
        a,b=refs[name],cands[name]
        assert a['A']==b['matrix'],name
        ea={e['mask']:e for e in a['events']}
        eb={e['mask']:e for e in b['events']}
        assert set(ea)==set(eb)==set(range(32)),name
        for mask in ea:
            x,y=ea[mask],eb[mask]
            left=[x['p'],*x['gradient'],*x['hessian_upper']]
            right=[y['p'],*y['gradient'],*y['hessian_upper_triangle']]
            assert len(left)==len(right)==28
            assert [Fraction(v) for v in left]==[Fraction(v) for v in right],(name,mask)
            count+=len(left)
    result={'status':'PASS_EXACT_ALL_EVENT_JETS','pid':os.getpid(),
            'python':platform.python_version(),'centers':sorted(refs),
            'events_per_center':32,'exact_scalar_comparisons':count,
            'scope':'Exact event-derivative implementation check only; not a Hessian sign certificate.'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':
    main()
