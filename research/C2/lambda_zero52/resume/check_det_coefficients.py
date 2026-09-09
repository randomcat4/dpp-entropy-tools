#!/usr/bin/env python3
"""Exact positive-orthant coefficient test of saved determinant factors."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from math import comb
import os
from pathlib import Path
import sympy as sp


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2, default=str) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def basis(degree, power, is_u):
    ans = defaultdict(int)
    if is_u:
        for j in range(degree - power + 1):
            ans[power + j] += comb(degree - power, j)
    else:
        for i in range(power + 1):
            for j in range(degree - power + 1):
                ans[i+j] += comb(power, i) * (-1)**(power-i) * comb(degree-power, j)
    return {k:v for k,v in ans.items() if v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    for case in ('r0', 'full'):
        record = json.loads((a.input_dir / case / 'report.json').read_text())
        fourth = next(i for i in record['minors'] if i['size'] == 4)
        factors = fourth['numerator_factors']
        entry = max(factors, key=lambda f:len(f['factor']))
        assert entry['multiplicity'] == 1
        names = ('mu','nu','u') if case == 'r0' else ('mu','nu','r','u')
        syms = sp.symbols(' '.join(names))
        poly = sp.Poly(sp.sympify(entry['factor']), *syms, domain=sp.ZZ)
        degrees = tuple(int(poly.degree(x)) for x in syms)
        terms = {mon:int(c) for mon,c in poly.terms()}
        report = {'pid':os.getpid(), 'case':case, 'started_utc':datetime.now(timezone.utc).isoformat(),
                  'source_factor':entry['factor'], 'variables':names, 'degrees':degrees,
                  'input_terms':len(terms), 'substitution':'each z=(X-1)/(X+1), except u=X/(X+1)',
                  'clearing_multiplier':'product (1+X_j)^degree_j, strictly positive for X_j>0', 'stages':[]}
        save(a.output_dir / (case + '_coefficient_report.json'), report)
        for axis,(name,degree) in enumerate(zip(names,degrees)):
            cache = {k:basis(degree,k,name=='u') for k in range(degree+1)}
            newterms = defaultdict(int)
            for mon,c in terms.items():
                for k,b in cache[mon[axis]].items():
                    n = list(mon)
                    n[axis] = k
                    newterms[tuple(n)] += c*b
            terms = {mon:c for mon,c in newterms.items() if c}
            report['stages'].append({'variable':name,'terms':len(terms)})
            save(a.output_dir / (case + '_coefficient_report.json'), report)
        report.update({'positive_coefficients':sum(c>0 for c in terms.values()),
                       'negative_coefficients':sum(c<0 for c in terms.values()),
                       'nonzero_terms':len(terms),'min_coefficient':str(min(terms.values())),
                       'max_coefficient':str(max(terms.values())),
                       'strict_positive_certificate_candidate':bool(terms) and all(c>0 for c in terms.values()),
                       'scope':'exact integer transform; factor identity and domain signs require independent review',
                       'finished_utc':datetime.now(timezone.utc).isoformat()})
        save(a.output_dir / (case + '_coefficient_table.json'), [{'powers':m,'coefficient':str(c)} for m,c in sorted(terms.items())])
        save(a.output_dir / (case + '_coefficient_report.json'), report)


if __name__ == '__main__':
    main()
