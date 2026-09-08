"""Exact real-rational finite-block transfer helper; theorem v1, no rate claims.

Python standard library only. JSON: K0, K1, blocks (zero-based), t.
Matrix entries and t must be integers or rational/decimal strings, never floats.
The sufficient feasibility test is Gershgorin; rejection is inconclusive.
"""
from fractions import Fraction as F
import argparse
import json


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError('use exact integers or rational/decimal strings')
    return F(x)


def matrix(raw):
    a = [[rational(x) for x in row] for row in raw]
    n = len(a)
    if not 1 <= n <= 256 or any(len(row) != n for row in a):
        raise ValueError('square matrix dimension must be 1..256')
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError('this exact helper accepts real symmetric matrices only')
    return a


def partition(blocks, n):
    if not isinstance(blocks, list) or any(not isinstance(b, list) or not b for b in blocks):
        raise ValueError('nonempty list of nonempty blocks required')
    flat = [i for b in blocks for i in b]
    if any(type(i) is not int for i in flat) or sorted(flat) != list(range(n)):
        raise ValueError('blocks must partition coordinates 0..n-1 exactly')
    return blocks


def pinch(a, blocks):
    labels = {}
    for label, block in enumerate(blocks):
        labels.update((i, label) for i in block)
    return [[a[i][j] if labels[i] == labels[j] else F(0)
             for j in range(len(a))] for i in range(len(a))]


def gershgorin_buffer(a):
    bounds = []
    for i, row in enumerate(a):
        radius = sum(abs(x) for j, x in enumerate(row) if j != i)
        bounds.extend((row[i]-radius, 1-row[i]-radius))
    return min(bounds)


def loss_bound(a, blocks):
    """Return exact C under sufficient exact feasibility and B-interiority tests."""
    if gershgorin_buffer(a) < 0:
        raise ValueError('Gershgorin does not establish 0<=K<=I; inconclusive')
    b = pinch(a, blocks)
    eta = gershgorin_buffer(b)
    if eta <= 0:
        raise ValueError('Gershgorin does not establish positive block buffer; inconclusive')
    energy = sum((a[i][j]-b[i][j])**2 for i in range(len(a)) for j in range(len(a)))
    return {'eta': eta, 'energy': energy, 'C': energy/(eta*(1-eta))}


def determinant(a):
    """Exact elimination, including the determinant of the empty matrix."""
    a = [row[:] for row in a]
    result = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            result = -result
        v = a[i][i]
        result *= v
        for j in range(i+1, len(a)):
            ratio = a[j][i]/v
            for k in range(i+1, len(a)):
                a[j][k] -= ratio*a[i][k]
    return result


def probabilities(a):
    n = len(a)
    if n > 8:
        raise ValueError('block enumeration is deliberately capped at 8 coordinates')
    out = []
    for mask in range(1 << n):
        m = [row[:] for row in a]
        excluded = n-mask.bit_count()
        for i in range(n):
            if not (mask >> i) & 1:
                m[i][i] -= 1
        out.append((-1)**excluded*determinant(m))
    if any(p < 0 for p in out) or sum(out) != 1:
        raise ValueError('computed masses are not a probability distribution')
    return out


def log_interval(x, terms=24):
    """Exact arctanh-series enclosure, with rational range reduction to [1,2]."""
    x = rational(x)
    if x <= 0 or type(terms) is not int or terms < 1:
        raise ValueError('positive log input and positive integer terms required')
    if x < 1:
        lo, hi = log_interval(1/x, terms)
        return -hi, -lo

    def unit(y):
        z = (y-1)/(y+1)
        total = sum((2*z**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
        tail = 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
        return total, total+tail

    exponent = 0
    while x > 2:
        x /= 2
        exponent += 1
    lo, hi = unit(x)
    l2, u2 = unit(F(2))
    return lo+exponent*l2, hi+exponent*u2


def entropy_interval(a):
    lo = hi = F(0)
    for p in probabilities(a):
        if p:
            low, high = log_interval(1/p)
            lo += p*low
            hi += p*high
    return lo, hi


def block_entropy(a, blocks):
    lo = hi = F(0)
    for b in blocks:
        low, high = entropy_interval([[a[i][j] for j in b] for i in b])
        lo += low
        hi += high
    return lo, hi


def decimal_outward(x, places, upper=False):
    scale = 10**places
    numerator = x.numerator*scale
    value = -((-numerator)//x.denominator) if upper else numerator//x.denominator
    sign = '-' if value < 0 else ''
    whole, frac = divmod(abs(value), scale)
    return f'{sign}{whole}.{frac:0{places}d}'


def interval_text(bounds):
    return [decimal_outward(bounds[0], 18), decimal_outward(bounds[1], 18, True)]


def transfer(raw):
    a0, a1 = matrix(raw['K0']), matrix(raw['K1'])
    if len(a0) != len(a1):
        raise ValueError('endpoint dimensions differ')
    n = len(a0)
    blocks = partition(raw['blocks'], n)
    if max(map(len, blocks)) > 8:
        raise ValueError('block size must be <=8 for exact entropy evaluation')
    t = rational(raw.get('t', '1/2'))
    if not 0 <= t <= 1:
        raise ValueError('t must lie in [0,1]')
    at = [[(1-t)*a0[i][j]+t*a1[i][j] for j in range(n)] for i in range(n)]
    kernels = [a0, a1, at]
    bounds = [loss_bound(a, blocks) for a in kernels]
    ent = [block_entropy(a, blocks) for a in kernels]
    jb = (ent[2][0]-(1-t)*ent[0][1]-t*ent[1][1],
          ent[2][1]-(1-t)*ent[0][0]-t*ent[1][0])
    result = (jb[0]-bounds[2]['C'], jb[1]+(1-t)*bounds[0]['C']+t*bounds[1]['C'])
    sign = 'POSITIVE' if result[0] > 0 else 'NEGATIVE' if result[1] < 0 else 'INCONCLUSIVE'
    return {
        'arithmetic': 'exact rational; logarithms rigorously enclosed by finite series',
        'scope': 'real rational inputs, sufficient Gershgorin tests, theorem v1',
        'n': n, 'block_sizes': list(map(len, blocks)), 't': str(t),
        'full_system_subsets_enumerated': 0,
        'block_subsets_evaluated': 3*sum(2**len(b) for b in blocks),
        'loss_bounds_0_1_t': [{k: str(v) for k, v in b.items()} for b in bounds],
        'block_jensen_interval_nats': interval_text(jb),
        'full_jensen_interval_nats': interval_text(result),
        'sign_from_exact_enclosure': sign,
        'theorem_validation': 'consult independent verification report for fixed version',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as f:
        raw = json.load(f)
    print(json.dumps(transfer(raw), indent=2))


if __name__ == '__main__':
    main()
