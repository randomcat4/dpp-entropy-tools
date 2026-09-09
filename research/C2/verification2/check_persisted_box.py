"""Recheck a stored outward-rational Hessian matrix by exact congruence.

This checks the saved matrix witness. Containment of the true Hessian also
requires the separately audited interval evaluation and logarithm bounds.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import os
import platform


def det(a):
    a=[r[:] for r in a]
    value=F(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        assert pivot is not None,'Singular preconditioner'
        if pivot!=k:
            a[k],a[pivot]=a[pivot],a[k]
            value=-value
        d=a[k][k]
        value*=d
        for i in range(k+1,len(a)):
            ratio=a[i][k]/d
            for j in range(k+1,len(a)):
                a[i][j]-=ratio*a[k][j]
    return value


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    cert=json.loads(Path(args.certificate).read_text(encoding='utf-8-sig'))
    boxes=cert['accepted_boxes']
    assert len(boxes)==1 and boxes[0]['center']=='R12_boundary_mid'
    box=boxes[0]
    assert F(box['radius'])==F(1,2048)
    assert list(map(F,box['center_coordinates']))==list(map(F,['41/100','17/50','3/4','-3/25','0','0']))
    h=[[(-F(c['hi_decimal']),-F(c['lo_decimal']))
        for c in row] for row in box['entropy_hessian_interval_decimal']]
    s=[[F(x) for x in row] for row in box['negative_hessian_preconditioner_S']]
    assert len(h)==len(s)==6 and all(len(r)==6 for r in h+s)
    assert all(h[i][j]==h[j][i] and h[i][j][0]<=h[i][j][1]
               for i in range(6) for j in range(6))
    determinant=det(s)
    q=[]
    for i in range(6):
        row=[]
        for j in range(6):
            lo=hi=F(0)
            for k in range(6):
                for l in range(6):
                    coefficient=s[k][i]*s[l][j]
                    endpoints=[coefficient*v for v in h[k][l]]
                    lo+=min(endpoints)
                    hi+=max(endpoints)
            row.append((lo,hi))
        q.append(row)
    margins=[q[i][i][0]-sum(max(abs(q[i][j][0]),abs(q[i][j][1]))
                           for j in range(6) if j!=i) for i in range(6)]
    assert all(x>0 for x in margins)
    events=box['event_probability_bounds']
    assert {e['mask'] for e in events}==set(range(32))
    positive=[]
    for event in events:
        if event['identically_zero']:
            assert event['mask'].bit_count()>3
        else:
            assert event['mask'].bit_count()<=3
            lo,hi=F(event['p']['lo']),F(event['p']['hi'])
            assert 0<lo<=hi
            positive.append(lo)
    assert len(positive)==26 and len(cert['zero_events'])==6
    result={'status':'PASS_PERSISTED_RATIONAL_MATRIX_WITNESS','pid':os.getpid(),
            'python':platform.python_version(),'center':box['center'],'radius':box['radius'],
            'positive_events':26,'constant_zero_events':6,
            'preconditioner_determinant':str(determinant),
            'gershgorin_margins_recomputed_from_displayed_H':[str(v) for v in margins],
            'all_margins_exceed_1_over_10':all(v>F(1,10) for v in margins),
            'minimum_positive_probability_lower':str(min(positive)),
            'scope':'Exact independent check of the persisted matrix witness; '
                    'true-Hessian containment is supplied by the audited interval algorithm.'}
    assert result['all_margins_exceed_1_over_10']
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS_PERSISTED_RATIONAL_MATRIX_WITNESS: all six exact margins > 1/10; 26 positive events, 6 constant zero.')


if __name__=='__main__':
    main()
