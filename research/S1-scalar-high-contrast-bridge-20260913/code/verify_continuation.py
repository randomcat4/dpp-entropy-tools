"""Deterministic author checker; standard library only on this entrypoint.
All certified comparisons use directed integer intervals, never displayed floats.
Run --write FILE to produce, --verify FILE to recompute and check literal output.
The Fisher/entropy-rate theorems are proved separately; this is finite evidence.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse, hashlib, json, sys, time
import intervals as iv
from intervals import R, C, log, h
from certify import matrix, tree


def box(x, places=12):
    """Exact outward decimal envelope, represented as rational strings."""
    den = 10 ** places
    lo = (x.lo * den) // iv.S
    hi = -((-x.hi * den) // iv.S)
    return [str(F(lo, den)), str(F(hi, den))]


def det(a):
    n = len(a)
    ans = F(0)
    for p in permutations(range(n)):
        v = F((-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)))
        for i in range(n):
            v *= a[i][p[i]]
        ans += v
    return ans


def minor(a, gone):
    keep = [i for i in range(len(a)) if i not in gone]
    return [[a[i][j] for j in keep] for i in keep]


def independent_jet_test():
    # A rational rank-one cyclic projection: every complete atom, no sampling.
    n = 3
    c, a = F(3, 4), F(1, 8)
    q = [[C(F(1, n)) for j in range(n)] for i in range(n)]
    _, leaves, _ = tree(q, R(a), R(c), True)
    checked = 0
    for mask, jet in leaves:
        b = [[a * (i == j) + c/F(n) - ((i == j) and not ((mask >> i) & 1))
              for j in range(n)] for i in range(n)]
        sign = (-1) ** (n - mask.bit_count())
        ref = (sign*det(b),
               sign*sum((det(minor(b, {i})) for i in range(n)), F(0)),
               sign*sum((det(minor(b, {i, j})) for i in range(n) for j in range(i+1, n)), F(0)))
        for got, exact in zip(jet, ref):
            assert got.contains(exact), 'independent determinant/jet disagreement'
            checked += 1
    return checked


def fisher_case(name, bands, c_string, n=8):
    spec = {'bands': bands}
    c = F(c_string)
    a = (1-c)/2
    rho = sum((F(r)-F(l) for l, r in bands), F(0))
    Q = matrix(spec, n)
    stats, leaves, diagnostics = tree(Q, R(a), R(c), True)
    s = stats[-1]
    V = n*R(rho) - sum((Q[i][j].abs2() for i in range(n) for j in range(n)), R(0))
    v = (1-c*c)/4
    var = n*R(v) + c*c*V
    mu = n*(a+c*rho)
    moment_var = sum((p[0]*(R(mask.bit_count())-mu).sq() for mask, p in leaves), R(0))
    score_cov = sum((p[1]*(R(mask.bit_count())-mu) for mask, p in leaves), R(0))
    assert moment_var.overlaps(var), 'count variance identity failed'
    assert score_cov.contains(n), 'score-count covariance identity failed'
    floor = n/var
    info = s['F']/n
    accel = s['A']/n  # A=-sum p'' log p; H''=A-F.
    assert (info-floor).lo > 0, 'finite lower Fisher comparison unresolved'
    assert (R(1/v)-info).lo > 0, 'finite upper Fisher comparison unresolved'
    residual = sum((p[0]*(p[1]/p[0]-(n/var)*(R(mask.bit_count())-mu)).sq()
                    for mask, p in leaves), R(0))
    assert residual.overlaps(s['F']-n*n/var), 'orthogonal score projection identity failed'
    assert s['Hpp'].hi < 0, 'selected fixture curvature not certified negative'
    return {'name': name, 'bands': bands, 'c': c_string, 'a': str(a), 'n': n,
            'atoms': len(leaves), 'V': box(V), 'fisher_per_site': box(info),
            'count_floor_per_site': box(floor), 'limit_fisher_per_site': str(1/v),
            'acceleration_per_site': box(accel), 'Haa_per_site': box(s['Hpp']/n),
            'score_projection_residual': box(residual),
            'min_atom_lower': str(F(min(p[0].lo for _, p in leaves), iv.S))}


def density_checks():
    A = log(R(2))/2 + log(R(F(1,10)))/20 + 9*log(R(F(9,10)))/20
    assert A.lo > R(F(9,50)).hi, 'universal wedge constant not certified'
    rows = []
    for eps in (F(1,2), F(1,4), F(1,10), F(1,100), F(1,10000),
                F(1,1000000), F(1,2**40), F(1,2**80)):
        c = 1-eps
        threshold = 9*R(eps)/(100*c*log(R(F(10,3)/eps)))
        rho = F(threshold.lo, iv.S)  # exact rational inside the theorem's wedge
        G = h(R(eps/2))-(h(R(eps/10+c*rho))+h(R(9*eps/10+c*rho)))/2
        assert G.lo > R(9*eps/100).hi, 'density witness failed'
        rows.append({'epsilon': str(eps), 'rho': str(rho),
                     'threshold': box(threshold, 60), 'shape_independent_gap': box(G, 60),
                     'promised_gap_lower': str(9*eps/100)})
    return {'A': box(A, 60), 'A_strict_lower': '9/50', 'rows': rows}


def crossover_checks():
    # V_n <= 2J^2/pi^2(log n+2) <= 2J^2/9(log n+2).
    # The last expression divided by n is decreasing for n>=1.
    rows = []
    for J in (1, 4):
        for c in (F(99,100), F(9999,10000), 1-F(1,2**40)):
            v = (1-c*c)/4
            for m in range(1, 513):
                n = 1 << m
                perturbation = R(F(2*J*J,9))*c*c*(m*iv.ln2()+2)/n
                if perturbation.hi <= R(v).lo:
                    rows.append({'bands': J, 'c': str(c), 'n0': n,
                                 'm': m, 'perturbation_upper': box(perturbation, 60),
                                 'v': str(v), 'all_n_ge_n0_fisher_floor': str(1/(2*v))})
                    break
            else:
                raise AssertionError('crossover search budget exhausted')
    return rows


def recompute():
    iv.set_precision(256)
    independent = independent_jet_test()
    fixtures = [
        ('half_band', [['0','1/2']]),
        ('four_band', [['0','1/32'],['3/32','5/32'],['9/32','13/32'],['21/32','29/32']]),
        ('thin_band', [['0','1/1024']])]
    rows = [fisher_case(name, bands, c) for name, bands in fixtures
            for c in ('501/1000','99/100','9999/10000')]
    source = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (Path(__file__).parent / z for z in
                        ('intervals.py','certify.py','verify_continuation.py'))}
    return {'schema': 'scalar-high-contrast-continuation-v1',
            'status': 'AUTHOR_FINITE_PASS_NOT_INDEPENDENT_REVIEW',
            'universal_concavity': 'INCOMPLETE', 'bits': 256,
            'fresh_fisher_cases': len(rows), 'fresh_full_atoms': sum(r['atoms'] for r in rows),
            'independent_exact_jet_checks': independent,
            'density_witnesses': 8, 'analytic_crossover_checks': 6,
            'invalid_probability_cases': 0, 'failed_certified_comparisons': 0,
            'fisher_cases': rows, 'density': density_checks(),
            'crossover': crossover_checks(), 'source_sha256': source}


def verify_literal(saved, fresh):
    # Deterministic literal equality includes source binding and all exact endpoints.
    if saved != fresh:
        raise AssertionError('literal output/source binding differs from recomputation')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    fresh = recompute()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(fresh, indent=2)+'\n', encoding='utf-8')
    else:
        saved = json.loads(args.verify.read_text(encoding='utf-8'))
        verify_literal(saved, fresh)
        for key, replacement in (('fresh_full_atoms', 1), ('bits', 128),
                                 ('universal_concavity', 'PROVED')):
            damaged = dict(saved)
            damaged[key] = replacement
            try:
                verify_literal(damaged, fresh)
            except AssertionError:
                continue
            raise AssertionError('damaged output was accepted')
    print(json.dumps({'status':'PASS', 'mode':'write' if args.write else 'verify',
                      'fisher_cases':fresh['fresh_fisher_cases'],
                      'atoms':fresh['fresh_full_atoms'],
                      'independent_jets':fresh['independent_exact_jet_checks'],
                      'density_witnesses':fresh['density_witnesses'],
                      'analytic_crossover_checks':fresh['analytic_crossover_checks'],
                      'tamper_rejections':0 if args.write else 3,
                      'seconds':time.monotonic()-start}, indent=2))

if __name__ == '__main__':
    main()
