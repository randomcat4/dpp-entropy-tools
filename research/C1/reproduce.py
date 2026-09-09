"""Replay fixed C1 evidence in a fresh output directory; no network or scans."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=('core', 'geometry', 'certificate', 'audit', 'all'), default='certificate')
    parser.add_argument('--output-dir', type=Path, default=Path('reproduced'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    dest = args.output_dir.resolve()
    dest.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env.update({key: '1' for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'PYTHONUTF8')})
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    specs = {
        'core': [('main/precheck.py', []), ('main/tilt_probe.py', []), ('main/sparse_limit_algebra.py', [])],
        'geometry': [('geometry/probe.py', []), ('geometry/sparse_probe.py', [])],
        'certificate': [('mechanism/scripts/sparse_rational_certificate.py', ['--cert-steps', '60', '--table-exps', '6,8,12', '--table-steps', '80', '--cert-exp', '8', '--output', 'certificate.json'])],
        'audit': [('verifications/audit/formula_rebuild_audit.py', []), ('verifications/audit/geometry_asymptotic_audit.py', []), ('verifications/audit/sparse_asymptotic_audit.py', []), ('verifications/fresh_review/independent_sparse_check.py', []), ('verifications/fresh_review/endpoint_check.py', [])],
        'precheck': [('mechanism/scripts/mechanism_probe.py', ['--dps', '180', '--steps', '70', '--output', 'mechanism_probe.json'])],
    }
    specs['audit'].append(('verifications/audit/sparse_certificate_audit.py', [
        '--certificate', str(root / 'mechanism/outputs/sparse_rational_certificate.json'),
        '--source', str(root / 'mechanism/scripts/sparse_rational_certificate.py'),
        '--mechanism-probe', str(root / 'mechanism/scripts/mechanism_probe.py'),
        '--output', 'certificate_audit.json', '--dps', '120',
    ]))
    groups = list(specs) if args.suite == 'all' else [args.suite]
    records = []
    for group in groups:
        for relative, arguments in specs[group]:
            script = root / relative
            work = dest / group / script.stem
            work.mkdir(parents=True)
            command = [sys.executable, str(script), *arguments]
            completed = subprocess.run(command, cwd=work, env=env, text=True, encoding='utf-8', capture_output=True, check=False)
            (work / 'stdout.txt').write_text(completed.stdout, encoding='utf-8')
            (work / 'stderr.txt').write_text(completed.stderr, encoding='utf-8')
            record = {'script': relative, 'arguments': arguments, 'exit_status': completed.returncode}
            records.append(record)
            print(json.dumps(record), flush=True)
    (dest / 'execution.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    return 0 if all(row['exit_status'] == 0 for row in records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
