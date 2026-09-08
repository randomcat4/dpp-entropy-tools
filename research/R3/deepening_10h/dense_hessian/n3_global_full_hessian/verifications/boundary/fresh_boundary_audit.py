"""Fresh boundary audit for U8/M10 n3_global_full_hessian.

No author module is imported.  The script uses a tiny second-order automatic
differentiation jet around 3x3 shifted determinants to rebuild exact-event
probabilities, full six-coordinate Hessians, the structural rho scalar, and a
few high-precision rank-one boundary sanity cases.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path
import time


getcontext().prec = 220

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIM = 6


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


class Jet:
    __slots__ = ("v", "g", "h")

    def __init__(self, v=0, g=None, h=None):
        self.v = Decimal(v)
        self.g = [Decimal(0)] * DIM if g is None else list(g)
        self.h = [[Decimal(0) for _ in range(DIM)] for _ in range(DIM)] if h is None else [list(row) for row in h]

    @staticmethod
    def var(value, idx):
        g = [Decimal(0)] * DIM
        g[idx] = Decimal(1)
        return Jet(value, g)

    def __add__(self, other):
        other = ensure(other)
        return Jet(
            self.v + other.v,
            [self.g[i] + other.g[i] for i in range(DIM)],
            [[self.h[i][j] + other.h[i][j] for j in range(DIM)] for i in range(DIM)],
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, [-x for x in self.g], [[-x for x in row] for row in self.h])

    def __sub__(self, other):
        return self + (-ensure(other))

    def __rsub__(self, other):
        return ensure(other) + (-self)

    def __mul__(self, other):
        other = ensure(other)
        h = [[Decimal(0) for _ in range(DIM)] for _ in range(DIM)]
        for i in range(DIM):
            for j in range(DIM):
                h[i][j] = (
                    self.h[i][j] * other.v
                    + self.g[i] * other.g[j]
                    + self.g[j] * other.g[i]
                    + self.v * other.h[i][j]
                )
        return Jet(
            self.v * other.v,
            [self.g[i] * other.v + self.v * other.g[i] for i in range(DIM)],
            h,
        )

    __rmul__ = __mul__


def ensure(x):
    return x if isinstance(x, Jet) else Jet(x)


def det3_jet(M):
    return (
        M[0][0] * M[1][1] * M[2][2]
        + M[0][1] * M[1][2] * M[2][0]
        + M[0][2] * M[1][0] * M[2][1]
        - M[0][2] * M[1][1] * M[2][0]
        - M[0][1] * M[1][0] * M[2][2]
        - M[0][0] * M[1][2] * M[2][1]
    )


def shifted_atom_jets(K):
    out = []
    coord = {(0, 0): 0, (1, 1): 1, (2, 2): 2, (0, 1): 3, (1, 0): 3, (0, 2): 4, (2, 0): 4, (1, 2): 5, (2, 1): 5}
    for mask in range(8):
        M = []
        for i in range(3):
            row = []
            for j in range(3):
                entry = Jet.var(K[i][j], coord[(i, j)])
                if i == j and not (mask >> i & 1):
                    entry = entry - Decimal(1)
                row.append(entry)
            M.append(row)
        atom = det3_jet(M)
        if (3 - mask.bit_count()) % 2:
            atom = -atom
        out.append(atom)
    return out


def B_and_fisher(K):
    atoms = shifted_atom_jets(K)
    B = [[Decimal(0) for _ in range(DIM)] for _ in range(DIM)]
    F = [[Decimal(0) for _ in range(DIM)] for _ in range(DIM)]
    for p in atoms:
        lp1 = p.v.ln() + Decimal(1)
        for i in range(DIM):
            for j in range(DIM):
                fij = p.g[i] * p.g[j] / p.v
                F[i][j] += fij
                B[i][j] += fij + p.h[i][j] * lp1
    return B, F, atoms


def matmul(A, B):
    n, m, p = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def transpose(A):
    return [list(row) for row in zip(*A)]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def ldl(A):
    n = len(A)
    L = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    D = [Decimal(0)] * n
    for i in range(n):
        L[i][i] = Decimal(1)
        for j in range(i):
            s = A[i][j]
            for k in range(j):
                s -= L[i][k] * L[j][k] * D[k]
            L[i][j] = s / D[j]
        d = A[i][i]
        for k in range(i):
            d -= L[i][k] * L[i][k] * D[k]
        D[i] = +d
        if D[i] <= 0:
            raise ArithmeticError(f"nonpositive LDL pivot {i}: {D[i]}")
    return L, D


def solve_spd(A, bcols):
    L, D = ldl(A)
    n = len(A)
    m = len(bcols[0])
    Y = [[Decimal(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for c in range(m):
            s = bcols[i][c]
            for k in range(i):
                s -= L[i][k] * Y[k][c]
            Y[i][c] = +s
    Z = [[Y[i][c] / D[i] for c in range(m)] for i in range(n)]
    X = [[Decimal(0) for _ in range(m)] for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for c in range(m):
            s = Z[i][c]
            for k in range(i + 1, n):
                s -= L[k][i] * X[k][c]
            X[i][c] = +s
    return X


def inverse_spd(A):
    n = len(A)
    I = [[Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]
    return solve_spd(A, I)


def det_spd(A):
    _, D = ldl(A)
    out = Decimal(1)
    for d in D:
        out *= d
    return +out


def basis_mats():
    mats = []
    for k in range(DIM):
        M = [[Decimal(0) for _ in range(3)] for _ in range(3)]
        if k < 3:
            M[k][k] = Decimal(1)
        elif k == 3:
            M[0][1] = M[1][0] = Decimal(1)
        elif k == 4:
            M[0][2] = M[2][0] = Decimal(1)
        else:
            M[1][2] = M[2][1] = Decimal(1)
        mats.append(M)
    return mats


def mat_to_coord(M):
    return [M[0][0], M[1][1], M[2][2], M[0][1], M[0][2], M[1][2]]


def bilinear_in_basis(B, mats):
    coords = [mat_to_coord(M) for M in mats]
    out = [[Decimal(0) for _ in mats] for _ in mats]
    for a, ca in enumerate(coords):
        for b, cb in enumerate(coords):
            out[a][b] = sum(ca[i] * B[i][j] * cb[j] for i in range(DIM) for j in range(DIM))
    return out


def scale_congruence(M, scales):
    return [[M[i][j] * scales[i] * scales[j] for j in range(len(M))] for i in range(len(M))]


def rank_one_K(theta, eps, u):
    P = [[u[i] * u[j] for j in range(3)] for i in range(3)]
    return [[(eps if i == j else Decimal(0)) + (theta - eps) * P[i][j] for j in range(3)] for i in range(3)]


def complement(K):
    return [[(Decimal(1) if i == j else Decimal(0)) - K[i][j] for j in range(3)] for i in range(3)]


def atom_order_checks(theta, eps, u, atoms):
    s = [x * x for x in u]
    pairs = {(0, 1): 3, (0, 2): 5, (1, 2): 6}
    pair_checks = {}
    for (i, j), mask in pairs.items():
        lead = theta * (s[i] + s[j])
        pair_checks[f"p{i+1}{j+1}_over_eps"] = {
            "value": str(atoms[mask].v / eps),
            "expected_limit": str(lead),
            "difference": str(atoms[mask].v / eps - lead),
        }
    return {
        "p123_over_eps2": {"value": str(atoms[7].v / (eps * eps)), "expected": str(theta)},
        "p0_exact_formula_difference": str(atoms[0].v - (Decimal(1) - theta) * (Decimal(1) - eps) * (Decimal(1) - eps)),
        "pair_linear_checks": pair_checks,
        "positive_atoms": all(a.v > 0 for a in atoms),
        "min_atom": str(min(a.v for a in atoms)),
    }


def structural_rho(K, F):
    atoms = shifted_atom_jets(K)
    p = [a.v for a in atoms]
    p0, p1, p2, p12, p3, p13, p23, p123 = p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7]
    l12 = (p0 * p12 / (p1 * p2)).ln()
    l13 = (p0 * p13 / (p1 * p3)).ln()
    l23 = (p0 * p23 / (p2 * p3)).ln()
    Lam = (p123 * p1 * p2 * p3 / (p0 * p12 * p13 * p23)).ln()
    N = [[-Lam * K[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= l23
    N[1][1] -= l13
    N[2][2] -= l12
    detN = det_spd(N)
    Ninv = inverse_spd(N)
    E = basis_mats()
    eta = []
    G = [[Decimal(0) for _ in range(DIM)] for _ in range(DIM)]
    for A in E:
        eta.append(trace(matmul(Ninv, A)))
    for i, A in enumerate(E):
        for j, C in enumerate(E):
            G[i][j] = trace(matmul(matmul(matmul(Ninv, A), Ninv), C))
    Avec = [[F[i][j] + detN * G[i][j] for j in range(DIM)] for i in range(DIM)]
    sol = solve_spd(Avec, [[x] for x in eta])
    eta_A_inv_eta = sum(eta[i] * sol[i][0] for i in range(DIM))
    rho = detN * eta_A_inv_eta
    B_from_formula = [[Avec[i][j] - detN * eta[i] * eta[j] for j in range(DIM)] for i in range(DIM)]
    return {
        "rho": +rho,
        "one_minus_rho": +(Decimal(1) - rho),
        "logs": {"l12": str(l12), "l13": str(l13), "l23": str(l23), "Lambda": str(Lam)},
        "detN": str(detN),
        "N_min_pivot": str(min(ldl(N)[1])),
        "A_min_pivot": str(min(ldl(Avec)[1])),
        "B_from_formula": B_from_formula,
    }


def mat_diff_max(A, B):
    return max(abs(A[i][j] - B[i][j]) for i in range(len(A)) for j in range(len(A[0])))


def scaled_basis_for_u(u):
    P = [[u[i] * u[j] for j in range(3)] for i in range(3)]
    w1 = [Decimal(2), Decimal(-1), Decimal(0)]
    w2 = [Decimal(2), Decimal(0), Decimal(-1)]

    def outer(a, b):
        return [[a[i] * b[j] for j in range(3)] for i in range(3)]

    def sym_outer(a, b):
        return [[a[i] * b[j] + b[i] * a[j] for j in range(3)] for i in range(3)]

    N1 = outer(w1, w1)
    N2 = sym_outer(w1, w2)
    N3 = outer(w2, w2)
    return [P, sym_outer(u, w1), sym_outer(u, w2), N1, N2, N3]


def case_metrics(theta, eps_power):
    eps = Decimal(10) ** Decimal(-eps_power)
    u = [Decimal(1) / 3, Decimal(2) / 3, Decimal(2) / 3]
    K = rank_one_K(theta, eps, u)
    B, F, atoms = B_and_fisher(K)
    rho = structural_rho(K, F)
    B_formula_diff = mat_diff_max(B, rho["B_from_formula"])
    B_pivots = ldl(B)[1]
    L = (Decimal(1) / eps).ln()
    moving = bilinear_in_basis(B, scaled_basis_for_u(u))
    scales = [Decimal(1), Decimal(1) / L.sqrt(), Decimal(1) / L.sqrt(), eps.sqrt(), eps.sqrt(), eps.sqrt()]
    scaled = scale_congruence(moving, scales)
    scaled_pivots = ldl(scaled)[1]
    Kc = complement(K)
    Bc, Fc, _ = B_and_fisher(Kc)
    rhoc = structural_rho(Kc, Fc)
    return {
        "theta": str(theta),
        "epsilon": f"1e-{eps_power}",
        "strict_eigenvalues": [str(eps), str(eps), str(theta)],
        "strict_complement_eigenvalues": [str(Decimal(1) - eps), str(Decimal(1) - eps), str(Decimal(1) - theta)],
        "atom_orders": atom_order_checks(theta, eps, u, atoms),
        "B_min_ldl_pivot": str(min(B_pivots)),
        "scaled_1_2_3_min_ldl_pivot": str(min(scaled_pivots)),
        "scaled_1_2_3_pivots": [str(x) for x in scaled_pivots],
        "rho": str(rho["rho"]),
        "theta_L_one_minus_rho": str(theta * L * rho["one_minus_rho"]),
        "rho_deficit_times_L": str(L * rho["one_minus_rho"]),
        "B_formula_max_abs_difference": str(B_formula_diff),
        "N_min_pivot": rho["N_min_pivot"],
        "A_min_pivot": rho["A_min_pivot"],
        "complement_rho": str(rhoc["rho"]),
        "complement_rho_difference": str(rhoc["rho"] - rho["rho"]),
        "complement_B_min_ldl_pivot": str(min(ldl(Bc)[1])),
    }


def main():
    start = time.time()
    hash_files = [
        "frozen_problem.md",
        "proof_or_blocker.md",
        "boundary_asymptotic.md",
        "derivation.md",
        "verdict.md",
        "run_log.md",
        "rank_one_recheck.py",
        "rank_one_results.json",
        "symbolic_identity_gate.py",
        "symbolic_identity_results.json",
    ]
    hashes = {rel: {"sha256": sha256(ROOT / rel), "bytes": (ROOT / rel).stat().st_size} for rel in hash_files}
    cases = [
        case_metrics(Decimal(1) / 2, 8),
        case_metrics(Decimal(1) / 2, 16),
        case_metrics(Decimal(9) / 10, 16),
        case_metrics(Decimal(1) / 10, 16),
    ]
    tiny = Decimal("1e-170")
    checks = {
        "all_atoms_positive": all(c["atom_orders"]["positive_atoms"] for c in cases),
        "all_B_positive": all(Decimal(c["B_min_ldl_pivot"]) > 0 for c in cases),
        "all_scaled_positive": all(Decimal(c["scaled_1_2_3_min_ldl_pivot"]) > 0 for c in cases),
        "all_rho_below_one": all(Decimal(c["rho"]) < 1 for c in cases),
        "rho_constant_has_correct_sign_and_scale": all(Decimal("0.5") < Decimal(c["theta_L_one_minus_rho"]) < Decimal("1.2") for c in cases),
        "complement_rho_matches": all(abs(Decimal(c["complement_rho_difference"])) < Decimal("1e-180") for c in cases),
        "formula_matches_direct_B": all(Decimal(c["B_formula_max_abs_difference"]) < Decimal("1e-180") for c in cases),
        "p0_formula_decimal_tolerance": all(abs(Decimal(c["atom_orders"]["p0_exact_formula_difference"])) < tiny for c in cases),
        "p123_formula_decimal_tolerance": all(abs(Decimal(c["atom_orders"]["p123_over_eps2"]["value"]) - Decimal(c["atom_orders"]["p123_over_eps2"]["expected"])) < tiny for c in cases),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "finite high-precision sanity only; proof audit is in fresh_boundary_audit.md",
        "decimal_precision": getcontext().prec,
        "input_hashes": hashes,
        "cases": cases,
        "checks": checks,
        "elapsed_seconds": time.time() - start,
    }
    out = HERE / "fresh_boundary_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
