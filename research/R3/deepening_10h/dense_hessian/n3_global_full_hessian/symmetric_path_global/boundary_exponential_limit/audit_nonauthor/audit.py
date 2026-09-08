#!/usr/bin/env python3
"""
Minimal fresh non-author audit for D10-U10i boundary_exponential_limit.

No author module is imported.  The script independently evaluates the closed
phi(beta), its stationary point, and the positive-matrix constrained-energy
Sherman--Morrison formula used for the finite-x exponential boundary samples.
"""

from __future__ import annotations

import json
import hashlib
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


getcontext().prec = 180
getcontext().Emin = -999999999
getcontext().Emax = 999999999
D = Decimal

AUDIT_DIR = Path(__file__).resolve().parent
UNIT_DIR = AUDIT_DIR.parent
GLOBAL_DIR = UNIT_DIR.parent

L = D(2).ln()
SQRT2 = D(2).sqrt()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fmt(x: Decimal, digits: int = 45) -> str:
    return format(+x, f".{digits}E")


def jdefault(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(type(obj).__name__)


def transpose(A):
    return [list(col) for col in zip(*A)]


def matmul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def matvec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def inv(A):
    n = len(A)
    M = [A[i][:] + [D(1) if i == j else D(0) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        assert M[piv][c] != 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        for j in range(2 * n):
            M[c][j] /= p
        for r in range(n):
            if r == c:
                continue
            f = M[r][c]
            if f == 0:
                continue
            for j in range(2 * n):
                M[r][j] -= f * M[c][j]
    return [row[n:] for row in M]


def det3(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def phi(beta: Decimal) -> Decimal:
    return (beta + L + D(2)) * (beta + L) ** 4 / (D(2) * beta * beta * L * L)


def beta_star() -> Decimal:
    return (((L + D(4)) ** 2 + D(24) * L * (L + D(2))).sqrt() - (L + D(4))) / D(6)


def to_matrix(z):
    d, e, h, k = z
    return [[d, h, k], [h, e, h], [k, h, d]]


BASIS = [to_matrix([D(1) if i == j else D(0) for j in range(4)]) for i in range(4)]


def tr(A):
    return sum(A[i][i] for i in range(len(A)))


def calculate_sigma(x: Decimal, beta: Decimal) -> dict[str, Any]:
    s = (-beta / x).exp()
    assert D(0) < x < D("0.5") and D(0) < s < D(1)
    one = D(1)
    sqrt_1ms = (one - s).sqrt()
    a = x * sqrt_1ms / SQRT2

    E = (one - x) * (one - D(2) * x + x * x * s)
    U = x * ((one - x) ** 2 + (one - D(2) * x) * x * (one - s) / D(2))
    W = x * (one - x) * (one - x * s)
    V = x * x * (one + (one - D(2) * x) * s) / D(2)
    Z = x * x * (one - x * s)
    F = x * x * x * s
    assert min(E, U, W, V, Z, F) > 0

    ell = (E * V / (U * W)).ln()
    kappa_log = (E * Z / (U * U)).ln()
    Lambda = s.ln() + (U * U * W / (E * x**3 * (V / (x * x)) ** 2 * (Z / (x * x)))).ln()
    n = -ell - x * Lambda
    m = -kappa_log - x * Lambda
    N = [[n, -Lambda * a, D(0)], [-Lambda * a, m, -Lambda * a], [D(0), -Lambda * a, n]]
    N_inv = inv(N)
    detN = det3(N)

    eta = [tr(matmul(N_inv, B)) for B in BASIS]
    gram = []
    for Bi in BASIS:
        row = []
        for Bj in BASIS:
            row.append(tr(matmul(matmul(matmul(N_inv, Bi), N_inv), Bj)))
        gram.append(row)

    w = [one + s, one, -D(2) * SQRT2 * sqrt_1ms, one - s]
    jf = [x * x * wi for wi in w]
    jq = [x, x, -D(2) * a, D(0)]
    je = [D(4) * x - D(2) - jf[0], D(2) * x - D(1) - jf[1], -D(4) * a - jf[2], -jf[3]]
    ju = [D(1) - D(3) * x + jf[0], -x + jf[1], D(2) * a + jf[2], jf[3]]
    jw = [-D(2) * x + jf[0], D(1) - D(2) * x + jf[1], D(4) * a + jf[2], jf[3]]
    jv = [jq[i] - jf[i] for i in range(4)]
    jz = [D(2) * x - jf[0], -jf[1], -jf[2], -jf[3]]

    rest = [[D(0) for _ in range(4)] for __ in range(4)]
    for mu, form, p in zip([D(1), D(2), D(1), D(2), D(1)], [je, ju, jw, jv, jz], [E, U, W, V, Z]):
        for i in range(4):
            for j in range(4):
                rest[i][j] += mu * form[i] * form[j] / p
    A0 = [[rest[i][j] + detN * gram[i][j] for j in range(4)] for i in range(4)]
    A0_inv = inv(A0)
    Aeta = matvec(A0_inv, eta)
    Aw = matvec(A0_inv, w)
    denom = s / x + dot(w, Aw)
    constrained_inv_eta = [Aeta[i] - Aw[i] * dot(w, Aeta) / denom for i in range(4)]
    T = dot(eta, constrained_inv_eta)
    sigma = eta[1] ** 2 * (D(1) / T - detN)
    zmin = [eta[1] * v / T for v in constrained_inv_eta]

    h_trial = eta[1] / (eta[2] + D(2) * SQRT2 * eta[3] / sqrt_1ms)
    trial = [D(0), D(0), h_trial, D(2) * SQRT2 * h_trial / sqrt_1ms]
    trial_eta_residual = dot(eta, trial) - eta[1]
    trial_w_residual = dot(w, trial)
    trial_energy = dot(trial, matvec(A0, trial)) - detN * eta[1] ** 2

    h0 = -(beta + L) ** 2 / (D(2) * SQRT2 * beta * L)
    z0 = [D(0), D(0), h0, D(2) * SQRT2 * h0]
    return {
        "x": x,
        "beta": beta,
        "s": s,
        "sigma": sigma,
        "phi": phi(beta),
        "sigma_minus_phi": sigma - phi(beta),
        "error_over_sqrt_x": abs(sigma - phi(beta)) / x.sqrt(),
        "zmin": zmin,
        "z0": z0,
        "zmin_minus_z0_over_sqrtx_max": max(abs(zmin[i] - z0[i]) for i in range(4)) / x.sqrt(),
        "trial_eta_residual": trial_eta_residual,
        "trial_w_residual": trial_w_residual,
        "trial_energy_minus_sigma": trial_energy - sigma,
        "detN": detN,
        "eta": eta,
        "N_limit_residuals": {
            "n_minus_beta_plus_l": n - (beta + L),
            "m_minus_beta": m - beta,
            "Lambda_plus_beta_over_x_minus_log4": Lambda + beta / x - D(4).ln(),
            "detN_minus_limit": detN - beta * L * (beta + L),
        },
        "min_kernel_eigenvalue_formula": x * s / (D(1) + sqrt_1ms),
        "max_kernel_eigenvalue_formula": x * (D(1) + sqrt_1ms),
    }


def read_author_sanity_summary() -> dict[str, Any]:
    path = UNIT_DIR / "sanity.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("exponential_rows", [])
    beta58 = [r for r in rows if r.get("beta") == "0.58"]
    finite_x_1e4 = [r for r in beta58 if r.get("x") == "0.0001"]
    finite_x_1e6 = [r for r in beta58 if r.get("x") == "0.000001"]
    return {
        "sha256": sha256(path),
        "status": data.get("status"),
        "denominators": data.get("denominators"),
        "beta_star": data.get("beta_star"),
        "phi_minimum": data.get("phi_minimum"),
        "beta_0p58_x_1e_minus_4": finite_x_1e4[0] if finite_x_1e4 else None,
        "beta_0p58_x_1e_minus_6": finite_x_1e6[0] if finite_x_1e6 else None,
    }


def collect_hashes() -> dict[str, str]:
    files = [
        UNIT_DIR / "frozen_problem.md",
        UNIT_DIR / "proof_candidate.md",
        UNIT_DIR / "verdict.md",
        UNIT_DIR / "run_log.md",
        UNIT_DIR / "sanity.py",
        UNIT_DIR / "sanity.json",
        GLOBAL_DIR / "boundary_full_atom" / "analysis.md",
        GLOBAL_DIR / "derivation.md",
    ]
    return {str(p.relative_to(GLOBAL_DIR)): sha256(p) for p in files if p.exists()}


def main() -> None:
    bstar = beta_star()
    derivative_poly_at_star = D(3) * bstar * bstar + (L + D(4)) * bstar - D(2) * L * (L + D(2))
    phi_min = phi(bstar)
    lower_bound = D(8) * (L + D(2))

    points = []
    for beta in [D("0.58"), bstar, D("0.3"), D("1"), D("3")]:
        for x in [D("1e-4"), D("1e-6")]:
            r = calculate_sigma(x, beta)
            points.append(
                {
                    "beta": fmt(beta, 50),
                    "x": str(x),
                    "sigma": fmt(r["sigma"], 55),
                    "phi": fmt(r["phi"], 55),
                    "sigma_minus_phi": fmt(r["sigma_minus_phi"], 45),
                    "error_over_sqrt_x": fmt(r["error_over_sqrt_x"], 35),
                    "zmin_minus_z0_over_sqrtx_max": fmt(r["zmin_minus_z0_over_sqrtx_max"], 35),
                    "trial_eta_residual": fmt(r["trial_eta_residual"], 30),
                    "trial_w_residual": fmt(r["trial_w_residual"], 30),
                    "trial_energy_minus_sigma": fmt(r["trial_energy_minus_sigma"], 35),
                    "detN": fmt(r["detN"], 45),
                    "N_limit_residuals": {k: fmt(v, 35) for k, v in r["N_limit_residuals"].items()},
                    "strict_kernel": r["min_kernel_eigenvalue_formula"] > 0 and r["max_kernel_eigenvalue_formula"] < 1,
                    "min_kernel_eigenvalue": fmt(r["min_kernel_eigenvalue_formula"], 25),
                    "max_kernel_eigenvalue": fmt(r["max_kernel_eigenvalue_formula"], 25),
                }
            )

    author = read_author_sanity_summary()
    beta58_phi = phi(D("0.58"))
    result = {
        "status": "SCOPED_AUDIT_CORRECT__GLOBAL_PATH_STILL_INCOMPLETE",
        "precision_decimal_digits": getcontext().prec,
        "input_hashes_sha256": collect_hashes(),
        "closed_phi": {
            "formula": "(beta+log2+2)*(beta+log2)^4/(2*beta^2*log2^2)",
            "beta_star": bstar,
            "derivative_polynomial_at_beta_star": derivative_poly_at_star,
            "phi_minimum": phi_min,
            "global_lower_bound_8_log2_plus_16": lower_bound,
            "phi_0p58": beta58_phi,
            "positivity_reason": "all factors positive; AM-GM gives (beta+log2)^2>=4 beta log2 and hence phi>8(log2+2)",
            "unique_min_reason": "log-derivative sign is the increasing quadratic 3 beta^2+(log2+4) beta-2 log2(log2+2)",
        },
        "independent_exponential_samples": points,
        "author_sanity_summary": author,
        "old_finite_vs_limit_minimum": {
            "old_finite_beta_0p58_x_1e_minus_4_sigma": None
            if author["beta_0p58_x_1e_minus_4"] is None
            else author["beta_0p58_x_1e_minus_4"]["sigma"],
            "audit_recomputed_beta_0p58_x_1e_minus_4_sigma": points[0]["sigma"],
            "audit_phi_0p58": fmt(beta58_phi, 55),
            "phi_minimum_at_beta_star": fmt(phi_min, 55),
            "distinction": "26.581... is a finite-x value at beta=.58,x=1e-4; 26.603760... is the closed limiting minimum at beta_star.",
        },
        "classification": {
            "phi_closed_form": "CORRECT in this scoped audit.",
            "phi_positive_unique_min": "CORRECT in this scoped audit.",
            "SM_energy_interpretation": "Consistent: trial satisfies eta constraint and annihilates w; constrained positive-matrix formula gives sigma.",
            "uniform_remainder": "Plausible/correct as a proof skeleton on fixed compact beta intervals, relying on U8 coercivity; constants may depend on interval endpoints.",
            "continuous_exponential_wedge": "Follows for each compact beta interval after choosing sufficiently small x_J; not noncompact in beta.",
            "global_path": "INCOMPLETE.",
        },
        "checks": {
            "beta_star_polynomial_zero": abs(derivative_poly_at_star) < D("1e-160"),
            "phi_min_above_lower_bound": phi_min > lower_bound,
            "all_sample_sigmas_positive": all(D(p["sigma"]) > 0 for p in points),
            "all_samples_strict_kernel": all(p["strict_kernel"] for p in points),
            "trial_constraints_small": all(abs(D(p["trial_eta_residual"])) < D("1e-120") and abs(D(p["trial_w_residual"])) < D("1e-120") for p in points),
            "trial_energy_not_below_sigma": all(D(p["trial_energy_minus_sigma"]) > -D("1e-100") for p in points),
            "author_old_finite_minimum_distinguished": author["beta_0p58_x_1e_minus_4"] is not None
            and D(author["beta_0p58_x_1e_minus_4"]["sigma"]) < beta58_phi
            and phi_min < beta58_phi,
        },
        "overall": "SCOPED_CORRECT_GLOBAL_INCOMPLETE",
    }
    out = AUDIT_DIR / "results.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=jdefault)
        f.write("\n")
    print(json.dumps({"overall": result["overall"], "out": str(out)}, indent=2))


if __name__ == "__main__":
    main()
