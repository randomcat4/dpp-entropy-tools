#!/usr/bin/env python3
"""Read archived trials exactly; this is not a curvature certificate.
Numbers are Decimal objects until the optional explicit float conversion.
"""
from __future__ import annotations
import argparse
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent

def loads(text: str):
    return json.loads(text, parse_float=Decimal)

def dumps(value) -> str:
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError('non-finite numeric input')
        return str(value)
    if isinstance(value, dict):
        return '{' + ','.join(json.dumps(k)+':'+dumps(v) for k,v in value.items()) + '}'
    if isinstance(value, (list, tuple)):
        return '[' + ','.join(dumps(v) for v in value) + ']'
    return json.dumps(value, allow_nan=False, separators=(',', ':'))

def powers(degree: int):
    return [[i,j,d-i-j] for d in range(1,degree+1)
            for i in range(d+1) for j in range(d-i+1)]

def read_trial(degree: int, root: Path = ROOT) -> dict:
    if degree not in (6,8,10):
        raise ValueError('only the three original degrees are archived')
    if degree < 10:
        result = loads((root/f'scout_degree{degree}.json').read_text())
    else:
        result = loads((root/'degree10/meta.json').read_text())
        coefficients = {}
        for name in ('u','v','w'):
            part = loads((root/f'degree10/{name}.json').read_text())
            if coefficients.keys() & part.keys():
                raise ValueError('duplicate coefficient field')
            coefficients.update(part)
        result['coefficients'] = coefficients
    c=result['coefficients']; ex=powers(degree)
    assert result['status'] == 'SCOUT_ONLY_NOT_A_CERTIFICATE'
    assert result['t'] == '5/4' and result['degree'] == degree
    assert c['exponents'] == ex
    assert all(len(c[name]) == len(ex) for name in ('u','v','w'))
    assert Decimal(2)*result['candidate_h_second'] == c['c2'] or abs(
        Decimal(2)*result['candidate_h_second']-c['c2']) < Decimal('1e-18')
    return result

def evaluate(record: dict, name: str, coordinates) -> Fraction:
    """Evaluate the archived decimal coefficients as exact rational numbers."""
    if name not in ('u','v','w'):
        raise ValueError('unknown polynomial')
    x=[Fraction(Decimal(str(a)))*8 for a in coordinates]
    c=record['coefficients']
    return sum((Fraction(a) * x[0]**i * x[1]**j * x[2]**k
                for a,(i,j,k) in zip(c[name],c['exponents'])), Fraction(0))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--write-dir',type=Path)
    p.add_argument('--compare-zip',type=Path)
    args=p.parse_args(); result={}
    archive=zipfile.ZipFile(args.compare_zip) if args.compare_zip else None
    try:
        for degree in (6,8,10):
            record=read_trial(degree,args.root)
            # Check exact numeric parse/write/parse, not a numerical refit.
            assert loads(dumps(record)) == record
            if archive:
                name=f'DPP27_PR91_raw_execution/scout_degree{degree}.json'
                assert record == loads(archive.read(name).decode()), name
            if args.write_dir:
                args.write_dir.mkdir(parents=True,exist_ok=True)
                dst=args.write_dir/f'scout_degree{degree}.json'
                if dst.exists():
                    raise FileExistsError(dst)
                dst.write_text(dumps(record)+'\n')
            result[str(degree)]={'terms':len(record['coefficients']['exponents']),
                                'coefficient_count':3*len(record['coefficients']['u'])+3,
                                'parse_write_parse':'PASS',
                                'original_zip_numeric_equality':'PASS' if archive else 'NOT_CHECKED'}
    finally:
        if archive: archive.close()
    print(json.dumps({'status':'DATA_RESTORATION_ONLY','degrees':result},indent=2))

if __name__ == '__main__': main()
