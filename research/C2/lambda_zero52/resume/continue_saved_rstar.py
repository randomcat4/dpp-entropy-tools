#!/usr/bin/env python3
"""Bounded continuation from saved Rstar; no event/M reconstruction or scout."""
import argparse
import contextlib
import datetime
import json
import os
from pathlib import Path
import signal
import time
import traceback

import sympy as sp
from sympy.polys.matrices import DomainMatrix


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, default=str) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def textfile(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(str(value) + '\n', encoding='utf-8')
    os.replace(tmp, path)


@contextlib.contextmanager
def limit(seconds):
    def expired(signum, frame):
        raise TimeoutError('stage deadline reached')
    old = signal.signal(signal.SIGALRM, expired)
    signal.alarm(max(1, int(seconds)))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--deadline', default='2026-09-09T12:07:28+00:00')
    args = ap.parse_args()
    deadline = datetime.datetime.fromisoformat(args.deadline).timestamp()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'pid': os.getpid(), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'absolute_deadline': args.deadline, 'source': 'continue_saved_rstar.py',
                'scope': 'saved 4x4 Rstar principal determinants only; no new M reconstruction or scout',
                'sympy': sp.__version__, 'cases': []}
    write(out / 'manifest.json', manifest)
    for case in ('r0', 'full'):
        seconds = min(90, deadline - time.time() - 10) if case == 'r0' else deadline - time.time() - 5
        if seconds < 2:
            break
        caseout = out / case
        caseout.mkdir(exist_ok=True)
        report = {'case': case, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'seconds_available': int(seconds), 'status': 'RUNNING', 'minors': []}
        write(caseout / 'report.json', report)
        try:
            with limit(seconds):
                data = json.loads((args.input_dir / case / (case + '_Rstar_pre_minors.json')).read_text())
                R = sp.Matrix([[sp.sympify(e) for e in row] for row in data['structure_reduction']['Rstar_strings']])
                report['saved_structure_checks'] = data['structure_reduction']['checks']
                if not all(report['saved_structure_checks'].values()):
                    raise ValueError('saved structure gate failed')
                report['domain'] = str(DomainMatrix.from_Matrix(R).domain)
                write(caseout / 'report.json', report)
                for k in (2, 3, 4):
                    report['active_minor'] = k
                    write(caseout / 'report.json', report)
                    dm = DomainMatrix.from_Matrix(R[:k, :k]).to_field()
                    determinant = dm.domain.to_sympy(dm.det())
                    textfile(caseout / ('minor_%d_det.txt' % k), determinant)
                    num, den = sp.fraction(determinant)
                    item = {'size': k, 'determinant_saved': True, 'factor_status': 'RUNNING'}
                    report['minors'].append(item)
                    write(caseout / 'report.json', report)
                    nf, df = sp.factor_list(num), sp.factor_list(den)
                    item.update({'factor_status': 'COMPUTED',
                                 'numerator_content': str(nf[0]), 'denominator_content': str(df[0]),
                                 'numerator_factors': [{'factor': str(f), 'multiplicity': int(m)} for f, m in nf[1]],
                                 'denominator_factors': [{'factor': str(f), 'multiplicity': int(m)} for f, m in df[1]]})
                    textfile(caseout / ('minor_%d_factored.txt' % k), sp.factor(determinant))
                    write(caseout / 'report.json', report)
                report['status'] = 'DETERMINANTS_COMPUTED_SIGN_UNCLASSIFIED'
        except Exception as exc:
            report['status'] = 'TIMEOUT' if isinstance(exc, TimeoutError) else 'ERROR'
            report['error'] = repr(exc)
            report['traceback'] = traceback.format_exc().replace(str(Path(__file__).parent), '<source-dir>')
        report['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        write(caseout / 'report.json', report)
        manifest['cases'].append({'case': case, 'status': report['status']})
        write(out / 'manifest.json', manifest)
    manifest['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(out / 'manifest.json', manifest)


if __name__ == '__main__':
    main()
