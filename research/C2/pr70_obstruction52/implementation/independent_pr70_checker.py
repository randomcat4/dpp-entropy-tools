#!/usr/bin/env python3
"""One frozen PR70 finite unit. Independent implementation; no author imports."""
import argparse
import hashlib
import itertools
import json
import os
import platform
import resource
import sys
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path

sys.set_int_max_str_digits(0)
NTERMS = 80
WIDTH = Q(1, 10**32)
START = time.monotonic()
OUT = None
DEADLINE = None
CHECK_COUNT = 0


def utc():
    return datetime.now(timezone.utc).isoformat()


def pack(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): pack(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [pack(v) for v in value]
    return value


def write(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(pack(value), ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


class Halt(Exception):
    def __init__(self, state, gate):
        self.state, self.gate = state, gate
        super().__init__(state + ': ' + gate)


def tick():
    if time.time() >= DEADLINE:
        raise Halt('TIMEOUT', 'immutable_deadline')


def gate(name, condition, evidence=None, state='STOPPED_FIRST_EXACT_MISMATCH'):
    global CHECK_COUNT
    tick()
    CHECK_COUNT += 1
    row = {'sequence': CHECK_COUNT, 'gate': name, 'passed': bool(condition), 'evidence': evidence}
    with (OUT / 'CHECKS.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(pack(row), ensure_ascii=True, separators=(',', ':')) + '\n')
    if not condition:
        write('FIRST_FAILURE.json', row | {'status': state})
        raise Halt(state, name)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def padd(a, b):
    return trim((a[i] if i < len(a) else Q(0)) +
                (b[i] if i < len(b) else Q(0)) for i in range(max(len(a), len(b))))


def pscale(a, c):
    return trim(c * x for x in a)


def pmul(a, b):
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return trim(result)


def peval(a, t):
    result = Q(0)
    for x in reversed(a):
        result = result * t + x
    return result


def det_leibniz(matrix):
    """Inclusion determinants: permutation expansion, independent of Laplace below."""
    n = len(matrix)
    result = (Q(0),)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = (Q(-1 if inversions % 2 else 1),)
        for i, j in enumerate(perm):
            term = pmul(term, matrix[i][j])
        result = padd(result, term)
    return result


def det_laplace(matrix):
    """Complete-event determinants: recursive first-row expansion."""
    if not matrix:
        return (Q(1),)
    result = (Q(0),)
    for j, entry in enumerate(matrix[0]):
        minor = [row[:j] + row[j + 1:] for row in matrix[1:]]
        term = pmul(entry, det_laplace(minor))
        result = padd(result, pscale(term, Q(-1 if j % 2 else 1)))
    return result


def inclusion_events(matrix):
    n = len(matrix)
    inc = []
    for mask in range(1 << n):
        ids = [i for i in range(n) if mask & (1 << i)]
        inc.append(det_leibniz([[matrix[i][j] for j in ids] for i in ids]))
    atoms = []
    for mask in range(1 << n):
        value = (Q(0),)
        for sup in range(1 << n):
            if sup & mask == mask:
                value = padd(value, pscale(inc[sup], Q(-1 if (sup ^ mask).bit_count() % 2 else 1)))
        atoms.append(value)
    return inc, atoms


def signed_event(matrix, mask):
    n = len(matrix)
    event = [[tuple(entry) for entry in row] for row in matrix]
    absent = 0
    for i in range(n):
        if not (mask & (1 << i)):
            event[i][i] = padd(event[i][i], (Q(-1),))
            absent += 1
    return pscale(det_laplace(event), Q(-1 if absent % 2 else 1))


def jet(poly):
    return (poly[0], poly[1] if len(poly) > 1 else Q(0),
            2 * poly[2] if len(poly) > 2 else Q(0))


def jmul(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1],
            a[2] * b[0] + 2 * a[1] * b[1] + a[0] * b[2])


def jinv(a):
    return (1 / a[0], -a[1] / a[0]**2,
            2 * a[1]**2 / a[0]**3 - a[2] / a[0]**2)


def isum(a, b):
    return (a[0] + b[0], a[1] + b[1])


def iscale(a, c):
    return (c * a[0], c * a[1]) if c >= 0 else (c * a[1], c * a[0])


def decimal_out(value, upper=False, places=40):
    scaled = value * 10**places
    integer = -((-scaled.numerator) // scaled.denominator) if upper else scaled.numerator // scaled.denominator
    sign = '-' if integer < 0 else ''
    text = str(abs(integer)).rjust(places + 1, '0')
    return sign + text[:-places] + '.' + text[-places:]


def interval_record(bounds):
    return {'lower': bounds[0], 'upper': bounds[1], 'width': bounds[1] - bounds[0],
            'outward_decimal_40': [decimal_out(bounds[0]), decimal_out(bounds[1], True)]}


class LinearLogs:
    """Exact rational constant plus rational coefficients of logs of rational keys."""
    def __init__(self, constant=Q(0), terms=None):
        self.constant = Q(constant)
        self.terms = {Q(k): Q(v) for k, v in (terms or {}).items() if v and Q(k) != 1}

    def add(self, other):
        terms = dict(self.terms)
        for key, value in other.terms.items():
            terms[key] = terms.get(key, Q(0)) + value
        return LinearLogs(self.constant + other.constant, terms)

    def scale(self, value):
        return LinearLogs(self.constant * value, {k: v * value for k, v in self.terms.items()})

    def same(self, other):
        return self.constant == other.constant and self.terms == other.terms

    def raw(self):
        return {'constant': self.constant, 'log_coefficients': self.terms}

    def evaluate(self, logs):
        result = (self.constant, self.constant)
        for argument, coefficient in sorted(self.terms.items()):
            result = isum(result, iscale(logs.get(argument), coefficient))
        return result


class RationalLogs:
    def __init__(self):
        self.cache = {}
        self.log2 = self.series(Q(1, 3))
        write('logs/log2.json', self.log2 | {'argument': '2', 'N': NTERMS})

    @staticmethod
    def series(w):
        partial = Q(0)
        power = w
        terms = []
        for j in range(NTERMS):
            tick()
            term = 2 * power / (2 * j + 1)
            terms.append(term)
            partial += term
            power *= w * w
        tail = 2 * power / ((2 * NTERMS + 1) * (1 - w * w))
        return {'w': w, 'partial': partial, 'tail': tail, 'terms': terms,
                'lower': partial, 'upper': partial + tail}

    def get(self, argument):
        argument = Q(argument)
        if argument in self.cache:
            return self.cache[argument]
        gate('positive_log_argument_' + str(len(self.cache)), argument > 0, argument, 'FAILED_POSITIVITY')
        y, exponent = argument, 0
        while y < 1:
            y *= 2
            exponent -= 1
        while y >= 2:
            y /= 2
            exponent += 1
        w = (y - 1) / (y + 1)
        local = self.series(w)
        bounds = isum((local['lower'], local['upper']),
                      iscale((self.log2['lower'], self.log2['upper']), Q(exponent)))
        index = len(self.cache)
        write(f'logs/log_{index:03d}.json', {'argument': argument, 'k': exponent, 'y': y,
              'N': NTERMS, 'normalized_series': local, 'interval': interval_record(bounds)})
        self.cache[argument] = bounds
        return bounds


def curvature(jets):
    fisher = sum((a[1]**2 / a[0] for a in jets), Q(0))
    acceleration = LinearLogs()
    for a in jets:
        acceleration = acceleration.add(LinearLogs(terms={a[0]: a[2]}))
    return LinearLogs(fisher).add(acceleration), fisher, acceleration


def entropy(probabilities):
    result = LinearLogs()
    for probability in probabilities:
        result = result.add(LinearLogs(terms={probability: -probability}))
    return result


def compare_interval(name, bounds, expected, sign, width_gate=True):
    write('intervals/' + name + '.json', interval_record(bounds))
    if width_gate:
        gate(name + '_width', Q(0) <= bounds[1] - bounds[0] <= WIDTH,
             interval_record(bounds), 'UNRESOLVED_INTERVAL')
    gate(name + '_broad_sign', bounds[0] > 0 if sign == 'positive' else bounds[1] < 0,
         interval_record(bounds), 'UNRESOLVED_SIGN')
    literal = tuple(Q(x) for x in expected)
    passed = literal[0] <= bounds[0] and bounds[1] <= literal[1]
    state = 'STOPPED_FIRST_LITERAL_DISCREPANCY' if bounds[1] < literal[0] or literal[1] < bounds[0] else 'UNRESOLVED_LITERAL_CONTAINMENT'
    gate(name + '_literal_containment', passed,
         {'computed': interval_record(bounds), 'literal': literal}, state)


def run(input_root):
    tick()
    raw = json.loads((input_root / 'object.json').read_text(encoding='utf-8-sig'))
    K = [[Q(x) for x in row] for row in raw['K']]
    D = [[Q(x) for x in row] for row in raw['D']]
    tau = Q(raw['tau'])
    write('input_echo.json', raw)
    gate('fixed_arithmetic_contract', raw['atanh_terms'] == NTERMS and Q(raw['maximum_interval_width']) == WIDTH)
    matrix = [[(K[i][j], D[i][j]) for j in range(3)] for i in range(3)]
    inc, atoms = inclusion_events(matrix)
    direct = [signed_event(matrix, mask) for mask in range(8)]
    jets = [jet(poly) for poly in atoms]
    marginals = [padd(atoms[i], atoms[i + 4]) for i in range(4)]
    marginal_jets = [jet(poly) for poly in marginals]
    _, direct_leaf = inclusion_events([row[:2] for row in matrix[:2]])
    write('events.json', {'coefficient_convention': 'ascending powers of physical t',
          'mask_order': list(range(8)), 'inclusion_minors': inc, 'mobius_event_polynomials': atoms,
          'signed_event_polynomials': direct, 'jets_p_pprime_psecond': jets,
          'marginal_polynomials': marginals, 'marginal_jets': marginal_jets,
          'independent_leaf_polynomials': direct_leaf})
    for i in range(8):
        gate(f'event_polynomial_dual_{i}', atoms[i] == direct[i], {'mobius': atoms[i], 'signed': direct[i]})
        gate(f'center_atom_positive_{i}', jets[i][0] > 0, jets[i][0], 'FAILED_POSITIVITY')
    for i in range(4):
        gate(f'leaf_marginal_dual_{i}', marginals[i] == direct_leaf[i], marginals[i])
    total_poly = (Q(0),)
    for poly in atoms:
        total_poly = padd(total_poly, poly)
    gate('full_polynomial_normalization', total_poly == (Q(1),), total_poly)
    gate('jet_normalization', tuple(sum((j[k] for j in jets), Q(0)) for k in range(3)) == (1, 0, 0))
    expected = json.loads((input_root / 'expected.json').read_text(encoding='utf-8-sig'))
    for i, row in enumerate(jets):
        for j, value in enumerate(row):
            gate(f'literal_atom_{i}_derivative_{j}', value == Q(expected['atoms'][i][j]),
                 {'computed': value, 'literal': expected['atoms'][i][j]})

    legality = {}
    point_probs = {}
    for label, t in [('minus', -tau), ('center', Q(0)), ('plus', tau)]:
        M = [[K[i][j] + t * D[i][j] for j in range(3)] for i in range(3)]
        point_probs[label] = [peval(poly, t) for poly in atoms]
        for complement in [False, True]:
            actual = [[Q(int(i == j)) - M[i][j] for j in range(3)] for i in range(3)] if complement else M
            name = label + ('_complement' if complement else '_K')
            minors = [det_laplace([[(actual[i][j],) for j in range(n)] for i in range(n)])[0] for n in range(1, 4)]
            legality[name] = {'matrix': actual, 'leading_sylvester_minors': minors}
    write('legality.json', legality)
    write('three_point_probabilities.json', point_probs)
    for name, row in legality.items():
        for j, value in enumerate(row['leading_sylvester_minors']):
            gate(f'{name}_minor_{j+1}_positive', value > 0, value, 'FAILED_POSITIVITY')
            gate(f'{name}_minor_{j+1}_literal', value == Q(expected['sylvester'][name][j]),
                 {'computed': value, 'literal': expected['sylvester'][name][j]})
    for label, probabilities in point_probs.items():
        gate(label + '_probability_normalization', sum(probabilities, Q(0)) == 1)
        for i, value in enumerate(probabilities):
            gate(f'{label}_atom_{i}_positive', value > 0, value, 'FAILED_POSITIVITY')

    phi_values = {}
    phi_rows = []
    for side in [0, 1]:
        total = Q(0)
        for i, P in enumerate(marginal_jets):
            r = jets[i + 4 * side]
            via_jet = jmul(jmul(P, P), jinv(r))[2]
            formula = 2 * (P[1] - P[0] * r[1] / r[0])**2 / r[0] + 2 * P[0] * P[2] / r[0] - P[0]**2 * r[2] / r[0]**2
            phi_rows.append({'side': side, 'marginal': i, 'P_jet': P, 'r_jet': r,
                             'quotient_jet_second': via_jet, 'P3_second': formula})
            write('phi_rows.json', phi_rows)
            gate(f'P3_dual_side_{side}_marginal_{i}', via_jet == formula, phi_rows[-1])
            total += via_jet
        phi_values['Phi' + str(side)] = total
    phi_values['Phi_pair'] = phi_values['Phi0'] + phi_values['Phi1']
    write('phi_exact.json', phi_values)
    for name in ['Phi0', 'Phi1', 'Phi_pair']:
        gate(name + '_P2_exact', phi_values[name] == Q(expected['phi'][name]),
             {'computed': phi_values[name], 'literal': expected['phi'][name]})
    compare_interval('Phi_pair', (phi_values['Phi_pair'], phi_values['Phi_pair']),
                     expected['intervals']['Phi_pair'], 'negative', False)

    full, full_fisher, full_accel = curvature(jets)
    leaf, leaf_fisher, leaf_accel = curvature([jet(poly) for poly in direct_leaf])
    conditional = full.add(leaf.scale(-1))
    sides = []
    side_rows = []
    for side in [0, 1]:
        total = LinearLogs()
        total_perspective = LinearLogs()
        rows = []
        for i, P in enumerate(marginal_jets):
            r = jets[i + 4 * side]
            # Direct derivative of r*log(r)-r*log(P), with all accelerations.
            constant = r[2] + r[1]**2 / r[0] - 2*r[1]*P[1]/P[0] - r[0]*P[2]/P[0] + r[0]*P[1]**2/P[0]**2
            direct_form = LinearLogs(constant).add(LinearLogs(terms={r[0]: r[2]})).add(LinearLogs(terms={P[0]: -r[2]}))
            # Separate product/quotient jet differentiation of P*q*log(q).
            q = jmul(r, jinv(P))
            log_coefficient = P[2]*q[0] + 2*P[1]*q[1] + P[0]*q[2]
            perspective_constant = 2*P[1]*q[1] + P[0]*q[2] + P[0]*q[1]**2/q[0]
            perspective = LinearLogs(perspective_constant).add(LinearLogs(terms={r[0]: log_coefficient})).add(LinearLogs(terms={P[0]: -log_coefficient}))
            row = {'side': side, 'marginal': i, 'r_jet': r, 'P_jet': P, 'q_jet': q,
                   'direct_full_derivative': direct_form.raw(), 'perspective_derivative': perspective.raw(),
                   'conditional_Fisher': (r[1]-r[0]*P[1]/P[0])**2/r[0],
                   'acceleration_log_coefficient': r[2], 'retained_Psecond_term': -r[0]*P[2]/P[0],
                   'retained_rsecond_constant': r[2]}
            rows.append(row)
            write(f'side_{side}_terms.json', rows)
            gate(f'G{side}_dual_derivative_row_{i}', direct_form.same(perspective), row)
            total = total.add(direct_form)
            total_perspective = total_perspective.add(perspective)
        gate(f'G{side}_dual_total', total.same(total_perspective))
        sides.append(total)
        side_rows.append(rows)
    gate('conditional_structural_identity', sides[0].add(sides[1]).same(conditional),
         {'sum_sides': sides[0].add(sides[1]).raw(), 'full_minus_leaf': conditional.raw()})
    forms = {'G0': sides[0], 'G1': sides[1], 'negative_Hconditional': conditional, 'negative_Hfull': full}
    write('curvature_exact_forms.json', {'forms': {k: v.raw() for k, v in forms.items()},
          'full_Fisher': full_fisher, 'full_acceleration': full_accel.raw(),
          'leaf_negative_entropy': leaf.raw(), 'leaf_Fisher': leaf_fisher, 'leaf_acceleration': leaf_accel.raw()})
    logs = RationalLogs()
    bounds = {name: form.evaluate(logs) for name, form in forms.items()}
    write('curvature_components_intervals.json', {
        'full_acceleration': interval_record(full_accel.evaluate(logs)),
        'leaf_acceleration': interval_record(leaf_accel.evaluate(logs)),
        'leaf_negative_entropy': interval_record(leaf.evaluate(logs)),
        'P5': {name: interval_record(bound) for name, bound in bounds.items()}})
    for name in ['G0', 'G1', 'negative_Hconditional', 'negative_Hfull']:
        compare_interval(name, bounds[name], expected['intervals'][name], 'positive')

    entropies = {name: entropy(values) for name, values in point_probs.items()}
    jensen = entropies['minus'].add(entropies['plus']).scale(Q(1, 2)).add(entropies['center'].scale(-1))
    write('jensen_exact_form.json', {'entropies': {k: v.raw() for k, v in entropies.items()}, 'Jensen': jensen.raw()})
    entropy_bounds = {name: form.evaluate(logs) for name, form in entropies.items()}
    jensen_bound = jensen.evaluate(logs)
    # Separately assemble the three entropy intervals, with directed subtraction.
    via_entropies = isum(iscale(isum(entropy_bounds['minus'], entropy_bounds['plus']), Q(1, 2)), iscale(entropy_bounds['center'], Q(-1)))
    write('three_entropy_intervals.json', {name: interval_record(value) for name, value in entropy_bounds.items()})
    write('jensen_assembly.json', {'linear_form_interval': interval_record(jensen_bound),
          'three_entropy_interval': interval_record(via_entropies)})
    gate('Jensen_assembly_overlap', max(jensen_bound[0], via_entropies[0]) <= min(jensen_bound[1], via_entropies[1]))
    compare_interval('Jensen', via_entropies, expected['intervals']['Jensen'], 'negative')
    write('log_inventory.json', {'N': NTERMS, 'log2_file': 'logs/log2.json',
          'arguments': list(logs.cache), 'count': len(logs.cache),
          'tail_formula': '2*w^(2*N+1)/((2*N+1)*(1-w^2))',
          'normalization': 'argument=2^k*y; 1<=y<2; w=(y-1)/(y+1)',
          'negative_multiplier_rule': 'swap lower and upper before scaling'})
    return {'status': 'MACHINE_PASS', 'scope': 'fixed PR70 K,D,tau only',
            'all_checks': CHECK_COUNT, 'Phi_pair': phi_values['Phi_pair'],
            'P5': {name: interval_record(value) for name, value in bounds.items()},
            'Jensen': interval_record(via_entropies), 'mathematical_review': 'not supplied'}


def main():
    global OUT, DEADLINE
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    OUT = args.out
    OUT.mkdir(parents=True, exist_ok=True)
    DEADLINE = int(os.environ['C2_ABSOLUTE_DEADLINE_EPOCH'])
    environment = {'pid': os.getpid(), 'start_utc': utc(), 'deadline_epoch': DEADLINE,
       'deadline_utc': datetime.fromtimestamp(DEADLINE, timezone.utc).isoformat(),
       'source_commit': os.environ.get('C2_PRODUCTION_SOURCE_COMMIT'),
       'python_version': sys.version, 'implementation': platform.python_implementation(),
       'platform': platform.platform(), 'affinity': sorted(os.sched_getaffinity(0)),
       'virtual_memory_limit_bytes': resource.getrlimit(resource.RLIMIT_AS),
       'thread_settings': {key: os.environ.get(key) for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']},
       'arithmetic': 'stdlib Fraction only; N=80 fixed; no binary float in bounds'}
    write('environment.json', environment)
    code = 0
    try:
        result = run(args.input_root)
    except Halt as exc:
        result = {'status': exc.state, 'first_gate': exc.gate, 'all_checks_completed_before_stop': CHECK_COUNT}
        code = 20 if exc.state != 'TIMEOUT' else 124
    except MemoryError:
        result = {'status': 'MEMORY_LIMIT', 'all_checks_completed_before_stop': CHECK_COUNT}
        code = 125
    except Exception as exc:
        write('MECHANICAL_EXCEPTION.json', {'type': type(exc).__name__, 'message': str(exc),
             'traceback': traceback.format_exc()})
        result = {'status': 'MECHANICAL_EXCEPTION', 'exception_type': type(exc).__name__}
        code = 30
    result.update({'pid': os.getpid(), 'finish_utc': utc(), 'elapsed_seconds': time.monotonic() - START,
                   'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   'exit_code': code, 'deadline_epoch': DEADLINE})
    write('STATUS.json', result)
    manifest = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name not in ['output_hashes.json', 'stdout.log', 'stderr.log', 'exit.json']:
            manifest.append({'path': path.relative_to(OUT).as_posix(), 'bytes': path.stat().st_size,
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    write('output_hashes.json', manifest)
    print(json.dumps({'status': result['status'], 'pid': os.getpid(), 'exit_code': code,
                      'elapsed_seconds': result['elapsed_seconds']}, separators=(',', ':')), flush=True)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
