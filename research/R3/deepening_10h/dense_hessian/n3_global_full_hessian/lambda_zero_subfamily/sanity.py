"""D10-U10g author sanity. Standard library; no imported research implementation.
Finite evaluations are SCOUT, not a proof of the global Lambda-zero sign.
Run from this directory: python sanity.py
"""
import hashlib
import itertools
import json
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def tr(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in tr(b)] for row in a]


def add(a, b, s=1):
    return [[x+s*y for x, y in zip(r, t)] for r, t in zip(a, b)]


def inv(a):
    n = len(a)
    z = a[0][0]*0
    aug = [row[:] + [z+int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[k] = aug[k], aug[j]
        p = aug[j][j]
        aug[j] = [v/p for v in aug[j]]
        for i in range(n):
            if i != j:
                v = aug[i][j]
                aug[i] = [x-v*y for x, y in zip(aug[i], aug[j])]
    return [r[n:] for r in aug]


def det(a):
    n = len(a)
    if not n:
        return Q(1)
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(n))


def ldls(a):
    a = [r[:] for r in a]
    pivots = []
    for k in range(len(a)):
        p = a[k][k]
        pivots.append(p)
        if p <= 0:
            return pivots
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                a[i][j] -= a[i][k]*a[k][j]/p
    return pivots


def atoms(k):
    inc = []
    for mask in range(8):
        ix = [i for i in range(3) if mask >> i & 1]
        inc.append(det([[k[i][j] for j in ix] for i in ix]))
    return [sum((-1)**((t ^ s).bit_count())*inc[t] for t in range(8) if t & s == s)
            for s in range(8)]


BASIS = []
for i, j in [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]:
    b = [[Q(0) for _ in range(3)] for _ in range(3)]
    b[i][j] = b[j][i] = Q(1)
    BASIS.append(b)


def jets(k):
    p = atoms(k)
    # All basis matrices have determinant zero, so their central first
    # difference has no cubic remainder. Mixed second differences are exact
    # for any polynomial of total degree <=3.
    j = [[(x-y)/2 for x, y in zip(atoms(add(k, b)), atoms(add(k, b, -1)))] for b in BASIS]
    h = [[[Q(0) for _ in range(6)] for _ in range(6)] for _ in range(8)]
    for i in range(6):
        for l in range(6):
            pp = atoms(add(add(k, BASIS[i]), BASIS[l]))
            pm = atoms(add(add(k, BASIS[i]), BASIS[l], -1))
            mp = atoms(add(add(k, BASIS[i], -1), BASIS[l]))
            mn = atoms(add(add(k, BASIS[i], -1), BASIS[l], -1))
            for s in range(8):
                h[s][i][l] = (pp[s]-pm[s]-mp[s]+mn[s])/4
    return p, tr(j), h


def dec(x):
    if isinstance(x, Q):
        return D(x.numerator)/D(x.denominator)
    return D(x)


def dm(a):
    return [[dec(x) for x in r] for r in a]


def err(a, b):
    return max(abs(x-y) for r, s in zip(a, b) for x, y in zip(r, s))


def k_from_l(l):
    return mm(l, inv(add(eye(3), l)))


def quad(v, a):
    return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


def analyze(name, k):
    p, jets1, jets2 = jets(k)
    assert min(p) > 0 and sum(p) == 1
    assert len(ldls(k)) == 3 and min(ldls(k)) > 0
    ik = add(eye(3), k, -1)
    assert len(ldls(ik)) == 3 and min(ldls(ik)) > 0
    for s in range(8):
        mixed = add(k, [[Q(i == j and not (s >> i & 1)) for j in range(3)] for i in range(3)], -1)
        assert p[s] == (-1)**(3-s.bit_count())*det(mixed)
    assert all(sum(jets1[s][i] for s in range(8)) == 0 for i in range(6))
    assert all(sum(jets2[s][i][j] for s in range(8)) == 0 for i in range(6) for j in range(6))
    lambda_ratio = p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6])
    assert lambda_ratio == 1
    fmat = [[sum(jets1[s][i]*jets1[s][j]/p[s] for s in range(8)) for j in range(6)] for i in range(6)]
    c = [[k[i][i]*(1-k[i][i]) if i == j else -k[i][j]**2 for j in range(3)] for i in range(3)]
    u = [[Q(int(i == l)+int(j == l), 2)*k[i][j]-k[i][l]*k[l][j] for l in range(3)]
         for i, j in [(0, 1), (0, 2), (1, 2)]]
    expected = eye(3)+[[Q(0)]*3 for _ in range(3)]
    assert mm(fmat, c+u) == expected  # 18 exact rational identities per point
    with localcontext() as ctx:
        ctx.prec = 120
        nn = [-(dec(p[0]*p[6]/(p[2]*p[4]))).ln(),
              -(dec(p[0]*p[5]/(p[1]*p[4]))).ln(),
              -(dec(p[0]*p[3]/(p[1]*p[2]))).ln()]
        assert min(nn) > 0
        delta = nn[0]*nn[1]*nn[2]
        fv = [1/v for v in nn]
        eta = fv+[D(0)]*3
        fd = dm(fmat)
        ad = [r[:] for r in fd]
        for i in range(3):
            ad[i][i] += delta/nn[i]**2
        for b, (i, j) in enumerate([(0, 1), (0, 2), (1, 2)], 3):
            ad[b][b] += 2*delta/(nn[i]*nn[j])
        bd = add(ad, [[delta*x*y for y in eta] for x in eta], -1)
        direct_b = [[fd[i][j]+sum(dec(jets2[s][i][j])*dec(p[s]).ln() for s in range(8))
                     for j in range(6)] for i in range(6)]
        edirect = err(bd, direct_b)
        cc, uu = dm(c), dm(u)
        ci = inv(cc)
        rr = [r[3:] for r in fd[3:]]
        zz = [[2*nn[2-i] if i == j else D(0) for j in range(3)] for i in range(3)]
        ww = add(rr, mm(mm(rr, inv(add(rr, zz))), rr), -1)
        ew = err(ww, inv(add(inv(rr), inv(zz))))
        ieff = add(ci, mm(mm(mm(mm(ci, tr(uu)), ww), uu), ci))
        jj = [[D(0) if i == j else nn[3-i-j] for j in range(3)] for i in range(3)]
        schur = add(ieff, jj, -1)
        bxx = [r[:3] for r in bd[:3]]
        bxz = [r[3:] for r in bd[:3]]
        bzz = [r[3:] for r in bd[3:]]
        eschur = err(schur, add(bxx, mm(mm(bxz, inv(bzz)), tr(bxz)), -1))
        ax = [[delta/nn[i]**2 if i == j else D(0) for j in range(3)] for i in range(3)]
        rho = delta*quad(eta, inv(ad))
        rho3 = delta*quad(fv, inv(add(ieff, ax)))
        v = quad(eta, inv(fd))
        ev = abs(v-quad(fv, cc))
        assert max(edirect, ew, eschur, abs(rho-rho3), ev) < D('1e-100')
        piv = ldls(bd)
        assert len(piv) == 6 and min(piv) > 0 and rho < 1
        return {'name': name, 'K': [[str(x) for x in r] for r in k],
                'atoms': list(map(str, p)), 'lambda_ratio_exact': str(lambda_ratio),
                'K_LDL': list(map(str, ldls(k))), 'I_minus_K_LDL': list(map(str, ldls(add(eye(3), k, -1)))),
                'F_field_exact_entries': 18, 'rho_decimal120': str(rho),
                'delta_V': str(delta*v), 'optimized_proxy_2deltaV_over3': str(2*delta*v/3),
                'B_LDL_decimal120': list(map(str, piv)),
                'max_identity_error': str(max(edirect, ew, eschur, abs(rho-rho3), ev)),
                'status': 'SCOUT'}


def main():
    q = Q(7, 200)
    m0 = q/2
    lh = 8*(27/m0**2+54/m0+30)
    eps = min(Q(1, 40), q/6, 1/(6*lh))
    assert lh == Q(35781360, 49) and eps == Q(49, 214688160)
    r = Q(18, 25)
    u = r*r
    core_lower = 48*(1-u)*u/(6-u)**2
    assert core_lower > Q(1, 3)
    assert Q(2, 3)*Q(15, 8) == Q(5, 4) > 1
    assert sum(Q(5)**i/Q([1, 1, 2, 6, 24][i]) for i in range(5)) > Q(400, 7)
    kstar = [[Q(1, 2), Q(3, 10), Q(0)], [Q(3, 10), Q(1, 2), Q(3, 10)], [Q(0), Q(3, 10), Q(1, 2)]]
    lstar = mm(kstar, inv(add(eye(3), kstar, -1)))
    assert lstar == [[Q(x, 7) for x in row] for row in [[25, 30, 18], [30, 43, 30], [18, 30, 25]]]
    cases = [('path_blocker', kstar)]
    for ix, (zs, ws) in enumerate([([1, 2, 4], [1, 2, 3]), ([1, 3, 7], [2, 1, 4]), ([2, 5, 9], [3, 2, 1])]):
        ll = [[Q(ws[i]*ws[j], zs[i]+zs[j]) for j in range(3)] for i in range(3)]
        kk = k_from_l(ll)
        cases.append((f'cauchy_{ix}', kk))
        signs = [1, -1, 1]
        cases.append((f'cauchy_{ix}_sign', [[kk[i][j]*signs[i]*signs[j] for j in range(3)] for i in range(3)]))
    for signs in itertools.product([-1, 1], repeat=3):
        scales = [1+s*eps/8 for s in signs]
        ll = [[lstar[i][j]*scales[i]*scales[j] for j in range(3)] for i in range(3)]
        cases.append(('local_field_corner_'+''.join('p' if s > 0 else 'm' for s in signs), k_from_l(ll)))
    result = [analyze(name, k) for name, k in cases]
    asym = []
    with localcontext() as ctx:
        ctx.prec = 120
        for exponent in [2, 4, 8, 16, 32]:
            rr = 1-D(10)**(-exponent)
            nn = ((1+rr)/(1-rr)).ln()
            m = -(1-rr*rr).ln()
            dv = m/2+nn*nn/(4*m)-rr*nn/2
            asym.append({'r': str(rr), 'delta_V': str(dv), 'delta_V_over_m': str(dv/m),
                         'optimized_proxy': str(2*dv/3), 'B_positive_reason': 'reviewed whole centered-path theorem, not this finite evaluation'})
    hashes = {}
    for rel in ['../derivation.md', '../symmetric_path_subfamily/derivation.md',
                '../symmetric_path_subfamily/audit_nonauthor/verdict.md', 'sanity.py',
                'frozen_problem.md', 'derivation.md', 'proof_or_blocker.md']:
        hashes[rel] = hashlib.sha256((HERE/rel).read_bytes()).hexdigest()
    out = {'status': 'AUTHOR_SANITY_SCOUT_GLOBAL_INCOMPLETE', 'precision': 120,
           'attempts': len(cases), 'completed': len(result), 'failures': 0,
           'positive_entropy_curvature_candidates': 0,
           'denominators': {'path_base': 1, 'cauchy_base_and_sign': 6, 'rational_local_field_corners': 8,
                            'total_exact_kernel_points': 15, 'exact_field_matrix_entries': 15*18,
                            'analytic_r_boundary_evaluations': 5},
           'radius_certificate': {'q': str(q), 'm0': str(m0), 'L_H': str(lh),
                                  'epsilon': str(eps), 'epsilon_decimal': str(dec(eps)),
                                  'core_lower_rational': str(core_lower), 'center_B_lower': '1/3',
                                  'ball_B_lower': '1/6', 'all_checks': True},
           'points': result, 'boundary_proxy_checks': asym, 'hashes': hashes}
    (HERE/'sanity.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: out[k] for k in ['status', 'attempts', 'completed', 'failures', 'denominators', 'radius_certificate']}, indent=2))


if __name__ == '__main__':
    main()
