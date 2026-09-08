"""Independent exact-event checks for D10-U10b scalar-information route.

This script intentionally does not import the U8 author gates/search code.
It builds the eight n=3 DPP atoms by Mobius inversion of inclusion
determinants, computes exact first jets with Fraction arithmetic, and only
then uses high-precision Decimal logarithms/linear algebra for the Fisher
scalar rho.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
import json
from itertools import permutations
from pathlib import Path


getcontext().prec = 100


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "scalar_information_sanity_results.json"


def frac_to_dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def sign_perm(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return -1 if inv % 2 else 1


def mat_sub(M, mask):
    idx = [i for i in range(3) if (mask >> i) & 1]
    return [[M[i][j] for j in idx] for i in idx]


def det_fraction(M):
    n = len(M)
    if n == 0:
        return Fraction(1)
    total = Fraction(0)
    for p in permutations(range(n)):
        term = Fraction(sign_perm(p))
        for i, j in enumerate(p):
            term *= M[i][j]
        total += term
    return total


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(len(a)):
        out[i] += a[i]
    for i in range(len(b)):
        out[i] += b[i]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a, b):
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def det_poly_linear(K, D, mask):
    """det((K+tD)_mask) as a Fraction polynomial."""
    idx = [i for i in range(3) if (mask >> i) & 1]
    n = len(idx)
    if n == 0:
        return [Fraction(1)]
    total = [Fraction(0)]
    for p in permutations(range(n)):
        term = [Fraction(sign_perm(p))]
        for ii, jj in enumerate(p):
            i, j = idx[ii], idx[jj]
            term = poly_mul(term, [K[i][j], D[i][j]])
        total = poly_add(total, term)
    return total


def inclusion_values(K):
    return [det_fraction(mat_sub(K, mask)) for mask in range(8)]


def atoms_from_inclusion(q):
    p = [Fraction(0) for _ in range(8)]
    for s in range(8):
        total = Fraction(0)
        for t in range(8):
            if (t & s) == s:
                sign = -1 if ((t.bit_count() - s.bit_count()) % 2) else 1
                total += sign * q[t]
        p[s] = total
    return p


def atoms(K):
    return atoms_from_inclusion(inclusion_values(K))


BASIS = []
for i, j in [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]:
    E = [[Fraction(0) for _ in range(3)] for __ in range(3)]
    E[i][j] = Fraction(1)
    E[j][i] = Fraction(1)
    BASIS.append(E)


def atom_gradients(K):
    """Return grad[atom_mask][basis_index] exactly."""
    grad = [[Fraction(0) for _ in range(6)] for __ in range(8)]
    for bi, E in enumerate(BASIS):
        dq = []
        for mask in range(8):
            poly = det_poly_linear(K, E, mask)
            dq.append(poly[1] if len(poly) > 1 else Fraction(0))
        dp = atoms_from_inclusion(dq)
        for s in range(8):
            grad[s][bi] = dp[s]
    return grad


def dadd(a, b): return a + b
def dsub(a, b): return a - b
def dmul(a, b): return a * b


def mat_dec(M_frac):
    return [[frac_to_dec(x) for x in row] for row in M_frac]


def mat_eye(n):
    return [[Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]


def mat_mul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def mat_trace(A):
    return sum(A[i][i] for i in range(len(A)))


def mat_inv(A):
    n = len(A)
    aug = [[A[i][j] for j in range(n)] + [Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if aug[piv][col] == 0:
            raise ArithmeticError("singular matrix")
        if piv != col:
            aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            fac = aug[r][col]
            if fac:
                aug[r] = [aug[r][j] - fac * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def mat_solve(A, b):
    inv = mat_inv(A)
    return [sum(inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]


def det_dec(A):
    n = len(A)
    M = [[A[i][j] for j in range(n)] for i in range(n)]
    det = Decimal(1)
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            return Decimal(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            det = -det
        pv = M[col][col]
        det *= pv
        for r in range(col + 1, n):
            fac = M[r][col] / pv
            for j in range(col, n):
                M[r][j] -= fac * M[col][j]
    return det


def quad_solve(A, b):
    x = mat_solve(A, b)
    return sum(b[i] * x[i] for i in range(len(b))), x


def ldl_min_pivot(A):
    n = len(A)
    L = [[Decimal(0) for _ in range(n)] for __ in range(n)]
    pivs = []
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * pivs[k] for k in range(j))
            L[i][j] = (A[i][j] - s) / pivs[j]
        diag = A[i][i] - sum(L[i][k] * L[i][k] * pivs[k] for k in range(i))
        pivs.append(diag)
        L[i][i] = Decimal(1)
    return min(pivs), pivs


def transpose(A):
    return [list(row) for row in zip(*A)]


def structural_scalars(K_frac):
    p_frac = atoms(K_frac)
    if any(x <= 0 for x in p_frac):
        raise ValueError("non-strict atom")
    grad_frac = atom_gradients(K_frac)
    p = [frac_to_dec(x) for x in p_frac]
    grad = [[frac_to_dec(x) for x in row] for row in grad_frac]
    K = mat_dec(K_frac)

    l12 = (p[0] * p[3] / (p[1] * p[2])).ln()
    l13 = (p[0] * p[5] / (p[1] * p[4])).ln()
    l23 = (p[0] * p[6] / (p[2] * p[4])).ln()
    Lam = (p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6])).ln()

    N = [[-Lam * K[i][j] for j in range(3)] for i in range(3)]
    N[0][0] += -l23
    N[1][1] += -l13
    N[2][2] += -l12
    detN = det_dec(N)
    invN = mat_inv(N)

    F = [[Decimal(0) for _ in range(6)] for __ in range(6)]
    for s in range(8):
        for i in range(6):
            for j in range(6):
                F[i][j] += grad[s][i] * grad[s][j] / p[s]

    E_dec = [mat_dec(E) for E in BASIS]
    eta = [mat_trace(mat_mul(invN, E)) for E in E_dec]
    G = [[Decimal(0) for _ in range(6)] for __ in range(6)]
    for i in range(6):
        for j in range(6):
            G[i][j] = mat_trace(mat_mul(mat_mul(invN, E_dec[i]), mat_mul(invN, E_dec[j])))
    A = [[F[i][j] + detN * G[i][j] for j in range(6)] for i in range(6)]
    rho_raw, direction = quad_solve(A, eta)
    rho = detN * rho_raw
    B = [[A[i][j] - detN * eta[i] * eta[j] for j in range(6)] for i in range(6)]

    score_only = None
    try:
        score_only_raw, _ = quad_solve(F, eta)
        score_only = detN * score_only_raw
    except ArithmeticError:
        pass
    return {
        "atoms": p_frac,
        "log_coefficients": {"l12": l12, "l13": l13, "l23": l23, "Lambda": Lam},
        "N": N,
        "detN": detN,
        "min_N_ldl_pivot": ldl_min_pivot(N)[0],
        "rho": rho,
        "detN_eta_Ainv_eta_raw": rho_raw,
        "score_only_detN_eta_Finv_eta": score_only,
        "min_B_ldl_pivot": ldl_min_pivot(B)[0],
        "direction_Ainv_eta": direction,
    }


def make_K(diag, off):
    x, y, z = map(Fraction, diag)
    a, b, c = map(Fraction, off)
    return [[x, a, b], [a, y, c], [b, c, z]]


def serial_decimal(x):
    if x is None:
        return None
    if isinstance(x, Decimal):
        return format(x, "f")
    if isinstance(x, Fraction):
        return {"num": x.numerator, "den": x.denominator}
    if isinstance(x, list):
        return [serial_decimal(v) for v in x]
    if isinstance(x, dict):
        return {k: serial_decimal(v) for k, v in x.items()}
    return x


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    cases = {
        "heterogeneous_triangle": make_K(
            (Fraction(2, 5), Fraction(1, 3), Fraction(3, 7)),
            (Fraction(1, 12), Fraction(-1, 15), Fraction(1, 18)),
        ),
        "signed_path_like": make_K(
            (Fraction(3, 8), Fraction(5, 12), Fraction(7, 16)),
            (Fraction(1, 10), Fraction(0), Fraction(-1, 11)),
        ),
        "near_rank_one_dense": make_K(
            (
                Fraction(1, 10) + Fraction(2, 5) * Fraction(1, 9),
                Fraction(1, 10) + Fraction(2, 5) * Fraction(4, 9),
                Fraction(1, 10) + Fraction(2, 5) * Fraction(4, 9),
            ),
            (
                Fraction(2, 5) * Fraction(2, 9),
                Fraction(2, 5) * Fraction(2, 9),
                Fraction(2, 5) * Fraction(4, 9),
            ),
        ),
        "score_only_shortcut_blocker": make_K(
            (Fraction(2734, 10000), Fraction(8748, 10000), Fraction(7231, 10000)),
            (Fraction(280, 10000), Fraction(2892, 10000), Fraction(-132, 10000)),
        ),
    }
    results = {}
    for name, K in cases.items():
        st = structural_scalars(K)
        results[name] = {
            "K": K,
            "atoms": st["atoms"],
            "detN": st["detN"],
            "min_N_ldl_pivot": st["min_N_ldl_pivot"],
            "rho": st["rho"],
            "score_only_detN_eta_Finv_eta": st["score_only_detN_eta_Finv_eta"],
            "min_B_ldl_pivot": st["min_B_ldl_pivot"],
        }

    payload = {
        "status": "PASS",
        "description": "Mobius exact atoms + Fraction first jets + Decimal Fisher scalar checks.",
        "cases": results,
    }
    OUT.write_text(json.dumps(serial_decimal(payload), indent=2), encoding="utf-8")
    print(json.dumps(serial_decimal(payload), indent=2))
    print("sha256", sha256_file(OUT))


if __name__ == "__main__":
    main()
