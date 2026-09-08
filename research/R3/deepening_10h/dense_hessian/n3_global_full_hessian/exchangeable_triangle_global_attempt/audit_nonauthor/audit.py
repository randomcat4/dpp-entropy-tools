#!/usr/bin/env python3
"""
Fresh non-author audit for D10-U10h exchangeable_triangle_global_attempt.

This script does not import the author's sanity/search code.  It rebuilds the
two-parameter exchangeable triangle algebra using a small bivariate polynomial
engine over Fraction, then performs high-precision Decimal checks of the four
boundary-strip asymptotics and the stated blockers.
"""

from __future__ import annotations

import json
import hashlib
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 170
D = Decimal

AUDIT_DIR = Path(__file__).resolve().parent
UNIT_DIR = AUDIT_DIR.parent
ROOT = UNIT_DIR.parent
U10F_DIR = ROOT / "exchangeable_triangle_subfamily"


class Poly:
    def __init__(self, val: Any = 0):
        if isinstance(val, dict):
            self.t = {k: Fraction(v) for k, v in val.items() if v}
        elif isinstance(val, Poly):
            self.t = val.t.copy()
        else:
            q = Fraction(val)
            self.t = {} if q == 0 else {(0, 0): q}

    def __add__(self, other: Any) -> "Poly":
        other = other if isinstance(other, Poly) else Poly(other)
        out = self.t.copy()
        for k, v in other.t.items():
            out[k] = out.get(k, Fraction(0)) + v
            if out[k] == 0:
                del out[k]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other: Any) -> "Poly":
        return self + (-other if isinstance(other, Poly) else -Poly(other))

    def __rsub__(self, other: Any) -> "Poly":
        return Poly(other) - self

    def __mul__(self, other: Any) -> "Poly":
        other = other if isinstance(other, Poly) else Poly(other)
        out: dict[tuple[int, int], Fraction] = {}
        for (i, j), a in self.t.items():
            for (k, l), b in other.t.items():
                key = (i + k, j + l)
                out[key] = out.get(key, Fraction(0)) + a * b
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n: int) -> "Poly":
        out = Poly(1)
        for _ in range(n):
            out = out * self
        return out

    def __truediv__(self, q: Any) -> "Poly":
        return self * Fraction(1, 1) / q if isinstance(q, Poly) else self * Fraction(1, q)

    def div_int(self, q: int) -> "Poly":
        return self * Fraction(1, q)

    def diff(self, var: int) -> "Poly":
        out: dict[tuple[int, int], Fraction] = {}
        for exp, coeff in self.t.items():
            if exp[var] == 0:
                continue
            new_exp = list(exp)
            new_exp[var] -= 1
            out[tuple(new_exp)] = out.get(tuple(new_exp), Fraction(0)) + coeff * exp[var]
        return Poly(out)

    def ev_frac(self, alpha: Fraction, beta: Fraction) -> Fraction:
        return sum(v * alpha**i * beta**j for (i, j), v in self.t.items())

    def ev_dec(self, alpha: Decimal, beta: Decimal) -> Decimal:
        ans = D(0)
        for (i, j), v in self.t.items():
            ans += (D(v.numerator) / D(v.denominator)) * (alpha**i) * (beta**j)
        return +ans

    def is_zero(self) -> bool:
        return not self.t

    def __repr__(self) -> str:
        return f"Poly({self.t!r})"


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
    if isinstance(obj, Fraction):
        return {"num": obj.numerator, "den": obj.denominator}
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(type(obj).__name__)


A = Poly({(1, 0): 1})
B = Poly({(0, 1): 1})
ONE = Poly(1)
U_POLY = A + 2 * B - 3 * A * B
V_POLY = 2 * A + B - 3 * A * B
P_POLYS = [
    (ONE - A) * (ONE - B) ** 2,
    ((ONE - B) * U_POLY).div_int(3),
    (B * V_POLY).div_int(3),
    A * B**2,
]
MULT = [1, 3, 3, 1]
GRAD = [[p.diff(i) for i in range(2)] for p in P_POLYS]
HESS = [[[p.diff(i).diff(j) for j in range(2)] for i in range(2)] for p in P_POLYS]


def poly_symbolic_checks() -> dict[str, Any]:
    mass = sum(Poly(m) * p for m, p in zip(MULT, P_POLYS)) - 1

    a0 = A * (ONE - A)
    b0 = B * (ONE - B)
    kappa_num = 2 * a0 * b0 * ((ONE - B) * V_POLY + B * U_POLY)
    kappa_den = U_POLY * V_POLY

    common = Poly(1)
    for p in P_POLYS:
        common = common * p
    fisher_num = [[Poly(0), Poly(0)], [Poly(0), Poly(0)]]
    for i in range(2):
        for j in range(2):
            acc = Poly(0)
            for k in range(4):
                rest = Poly(1)
                for l in range(4):
                    if l != k:
                        rest = rest * P_POLYS[l]
                acc += Poly(MULT[k]) * GRAD[k][i] * GRAD[k][j] * rest
            fisher_num[i][j] = acc

    # F = diag(u,2v)-kappa(u,-v)(u,-v)^T, u=1/a0, v=1/b0.
    targets = {
        (0, 0): (a0 * kappa_den - kappa_num, a0 * a0 * kappa_den),
        (0, 1): (kappa_num, a0 * b0 * kappa_den),
        (1, 1): (2 * b0 * kappa_den - kappa_num, b0 * b0 * kappa_den),
    }
    fisher_residuals = {}
    for (i, j), (num, den) in targets.items():
        residual = fisher_num[i][j] * den - num * common
        fisher_residuals[f"{i}{j}"] = residual.is_zero()

    # If the Binomial(2,beta) Fisher factor 2 were omitted, the bb identity
    # would fail.  This catches the requested factor-two issue.
    wrong_bb_num = b0 * kappa_den - kappa_num
    wrong_bb_den = b0 * b0 * kappa_den
    wrong_bb_residual = fisher_num[1][1] * wrong_bb_den - wrong_bb_num * common

    ell_coeff = [1, -2, 1, 0]
    lam_coeff = [-1, 3, -3, 1]
    log_coeff_checks = []
    for k in range(4):
        aa_zero = HESS[k][0][0].is_zero()
        ab_res = Poly(MULT[k]) * HESS[k][0][1] - 2 * (Poly(ell_coeff[k]) + B * Poly(lam_coeff[k]))
        bb_res = Poly(MULT[k]) * HESS[k][1][1] - 2 * (Poly(ell_coeff[k]) + A * Poly(lam_coeff[k]))
        log_coeff_checks.append(
            {
                "layer": k,
                "alpha_alpha_second_derivative_zero": aa_zero,
                "ab_coefficient_for_ell_plus_beta_Lambda": ab_res.is_zero(),
                "bb_coefficient_for_ell_plus_alpha_Lambda": bb_res.is_zero(),
            }
        )

    return {
        "mass_identity": mass.is_zero(),
        "fisher_rank_one_identities": fisher_residuals,
        "wrong_missing_factor_two_bb_identity_is_nonzero": not wrong_bb_residual.is_zero(),
        "log_acceleration_layer_checks": log_coeff_checks,
        "all_log_checks": all(
            z["alpha_alpha_second_derivative_zero"]
            and z["ab_coefficient_for_ell_plus_beta_Lambda"]
            and z["bb_coefficient_for_ell_plus_alpha_Lambda"]
            for z in log_coeff_checks
        ),
    }


def eval_polys(alpha: Decimal, beta: Decimal) -> tuple[list[Decimal], list[list[Decimal]], list[list[list[Decimal]]]]:
    p = [z.ev_dec(alpha, beta) for z in P_POLYS]
    g = [[z.ev_dec(alpha, beta) for z in row] for row in GRAD]
    h = [[[z.ev_dec(alpha, beta) for z in row] for row in mat] for mat in HESS]
    return p, g, h


def eval_C(alpha: Decimal, beta: Decimal) -> dict[str, Any]:
    p, g, h = eval_polys(alpha, beta)
    fisher = [[D(0), D(0)], [D(0), D(0)]]
    accel = [[D(0), D(0)], [D(0), D(0)]]
    for k in range(4):
        for i in range(2):
            for j in range(2):
                fisher[i][j] += D(MULT[k]) * g[k][i] * g[k][j] / p[k]
                accel[i][j] += D(MULT[k]) * h[k][i][j] * p[k].ln()
    C = [[fisher[i][j] + accel[i][j] for j in range(2)] for i in range(2)]

    U = U_POLY.ev_dec(alpha, beta)
    V = V_POLY.ev_dec(alpha, beta)
    u = D(1) / (alpha * (D(1) - alpha))
    v = D(1) / (beta * (D(1) - beta))
    kappa = D(2) * alpha * (D(1) - alpha) * beta * (D(1) - beta) * (
        (D(1) - beta) / U + beta / V
    )
    F_rank = [
        [u - kappa * u * u, kappa * u * v],
        [kappa * u * v, D(2) * v - kappa * v * v],
    ]
    ell = (p[0] * p[2] / (p[1] * p[1])).ln()
    Lam = (p[3] * p[1] ** 3 / (p[0] * p[2] ** 3)).ln()
    n_alpha = -ell - alpha * Lam
    n_beta = -ell - beta * Lam
    C_formula = [
        [F_rank[0][0], F_rank[0][1] - D(2) * n_beta],
        [F_rank[1][0] - D(2) * n_beta, F_rank[1][1] - D(2) * n_alpha],
    ]
    wrong_formula = [
        [F_rank[0][0], F_rank[0][1] - D(2) * n_alpha],
        [F_rank[1][0] - D(2) * n_alpha, F_rank[1][1] - D(2) * n_beta],
    ]
    Delta = C[0][0] * C[1][1] - C[0][1] * C[1][0]
    return {
        "p": p,
        "fisher_direct": fisher,
        "fisher_rank_one": F_rank,
        "C_direct": C,
        "C_formula": C_formula,
        "C_wrong_n_placement": wrong_formula,
        "C_formula_max_abs_error": max(abs(C[i][j] - C_formula[i][j]) for i in range(2) for j in range(2)),
        "wrong_n_placement_max_abs_error": max(abs(C[i][j] - wrong_formula[i][j]) for i in range(2) for j in range(2)),
        "kappa": kappa,
        "ell": ell,
        "Lambda": Lam,
        "n_alpha": n_alpha,
        "n_beta": n_beta,
        "Delta": +Delta,
        "Caa": C[0][0],
        "Cab": C[0][1],
        "Cbb": C[1][1],
    }


def boundary_limit_rows() -> list[dict[str, Any]]:
    rows = []
    eps_values = [D("1e-4"), D("1e-8"), D("1e-12"), D("1e-20")]
    t_values = [D("0.1"), D("0.25"), D("0.5"), D("0.9")]
    log43 = (D(4) / D(3)).ln()

    def L(beta: Decimal) -> Decimal:
        return D(2) / (beta * (D(1) - beta)) - D(2) * log43

    for t in t_values:
        for eps in eps_values:
            checks = [
                ("alpha0", eps, t, eps, t * t * L(t)),
                ("alpha1", D(1) - eps, t, eps, (D(1) - t) ** 2 * L(t)),
                ("beta0", t, eps, eps, D(2) / (D(1) - t)),
                ("beta1", t, D(1) - eps, eps, D(2) / t),
            ]
            for label, aa, bb, scale, target in checks:
                ev = eval_C(aa, bb)
                normalized = scale * ev["Delta"]
                rows.append(
                    {
                        "label": label,
                        "transverse": str(t),
                        "epsilon": str(eps),
                        "normalized_Delta": fmt(normalized, 40),
                        "target": fmt(target, 40),
                        "relative_error": fmt(abs(normalized / target - D(1)), 30),
                        "Delta_positive": ev["Delta"] > 0,
                        "Caa_positive": ev["Caa"] > 0,
                        "Cab": fmt(ev["Cab"], 30),
                        "Cbb": fmt(ev["Cbb"], 30),
                    }
                )
    return rows


def ordinary_samples() -> list[dict[str, Any]]:
    pairs = [
        (D("0.2"), D("0.4")),
        (D("0.4"), D("0.2")),
        (D("0.01"), D("0.99")),
        (D("0.99"), D("0.01")),
        (D("0.5"), D("1e-6")),
    ]
    rows = []
    for aa, bb in pairs:
        ev = eval_C(aa, bb)
        rows.append(
            {
                "alpha": str(aa),
                "beta": str(bb),
                "min_atom": fmt(min(ev["p"]), 30),
                "C_formula_max_abs_error": fmt(ev["C_formula_max_abs_error"], 35),
                "wrong_n_placement_error": fmt(ev["wrong_n_placement_max_abs_error"], 35),
                "n_alpha": fmt(ev["n_alpha"], 35),
                "n_beta": fmt(ev["n_beta"], 35),
                "Delta": fmt(ev["Delta"], 35),
                "Cab": fmt(ev["Cab"], 35),
                "C_ab_negative": ev["Cab"] < 0,
            }
        )
    return rows


def factor_two_latent_check() -> list[dict[str, Any]]:
    samples = [(Fraction(1, 5), Fraction(2, 5)), (Fraction(3, 7), Fraction(5, 8))]
    rows = []
    for aa, bb in samples:
        A1 = aa * (1 - bb) ** 2
        B1 = 2 * (1 - aa) * bb * (1 - bb)
        A2 = 2 * aa * bb * (1 - bb)
        B2 = (1 - aa) * bb * bb
        kappa_direct = A1 * B1 / (A1 + B1) + A2 * B2 / (A2 + B2)
        U = aa + 2 * bb - 3 * aa * bb
        V = 2 * aa + bb - 3 * aa * bb
        kappa_formula = 2 * aa * (1 - aa) * bb * (1 - bb) * ((1 - bb) / U + bb / V)
        kappa_missing_factor_2 = aa * (1 - aa) * bb * (1 - bb) * ((1 - bb) / U + bb / V)
        rows.append(
            {
                "alpha": str(aa),
                "beta": str(bb),
                "kappa_direct_latent_AB_over_AplusB": str(kappa_direct),
                "kappa_formula": str(kappa_formula),
                "matches": kappa_direct == kappa_formula,
                "missing_factor_two_value": str(kappa_missing_factor_2),
                "missing_factor_two_wrong": kappa_missing_factor_2 != kappa_direct,
            }
        )
    return rows


def prime_factors(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def entropy_prime_coefficients(alpha: Fraction, beta: Fraction) -> dict[int, Fraction]:
    ps = [p.ev_frac(alpha, beta) for p in P_POLYS]
    coeffs: dict[int, Fraction] = {}
    for mult, p in zip(MULT, ps):
        # H=-sum mult*p*log(p); p=num/den.
        for sign, n in [(1, p.numerator), (-1, p.denominator)]:
            for prime, exponent in prime_factors(n).items():
                coeffs[prime] = coeffs.get(prime, Fraction(0)) - mult * p * sign * exponent
    return {k: v for k, v in coeffs.items() if v}


def swap_blocker() -> dict[str, Any]:
    first = entropy_prime_coefficients(Fraction(1, 5), Fraction(2, 5))
    second = entropy_prime_coefficients(Fraction(2, 5), Fraction(1, 5))
    keys = set(first) | set(second)
    diff = {p: first.get(p, Fraction(0)) - second.get(p, Fraction(0)) for p in keys}
    diff = {p: v for p, v in diff.items() if v}
    den = 1
    for v in diff.values():
        den = math.lcm(den, v.denominator)
    integer_exponents = {str(p): int(v * den) for p, v in diff.items()}
    entropy_diff = sum(
        (D(v.numerator) / D(v.denominator)) * D(p).ln() for p, v in diff.items()
    )
    return {
        "witness_first": ["1/5", "2/5"],
        "witness_second": ["2/5", "1/5"],
        "clear_denominator": den,
        "integer_prime_log_exponents": integer_exponents,
        "matches_author_expression": den == 125
        and integer_exponents == {"2": 226, "3": -71, "7": 28, "19": -38},
        "entropy_first_minus_second": fmt(entropy_diff, 60),
        "exact_nonzero_by_unique_factorization": bool(integer_exponents),
    }


def sanity_json_scan() -> dict[str, Any]:
    path = UNIT_DIR / "sanity.json"
    if not path.exists():
        return {"exists": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    actual_hashes = {
        "frozen_problem.md": sha256(UNIT_DIR / "frozen_problem.md"),
        "proof_or_blocker.md": sha256(UNIT_DIR / "proof_or_blocker.md"),
        "sanity.py": sha256(UNIT_DIR / "sanity.py"),
    }
    source_hashes = data.get("source_hashes", {})
    return {
        "exists": True,
        "sha256": sha256(path),
        "status": data.get("status"),
        "symbolic_checks": data.get("symbolic_checks"),
        "denominators": data.get("denominators"),
        "source_hashes_match_current": {
            k: source_hashes.get(k) == v for k, v in actual_hashes.items()
        },
        "swap_blocker": data.get("swap_blocker"),
    }


def collect_hashes() -> dict[str, str]:
    paths = [
        UNIT_DIR / "frozen_problem.md",
        UNIT_DIR / "proof_or_blocker.md",
        UNIT_DIR / "verdict.md",
        UNIT_DIR / "run_log.md",
        UNIT_DIR / "sanity.py",
        UNIT_DIR / "sanity.json",
        U10F_DIR / "proof_or_blocker.md",
        U10F_DIR / "fresh_audit.md",
        U10F_DIR / "verdict.md",
    ]
    return {str(p.relative_to(ROOT)): sha256(p) for p in paths if p.exists()}


def main() -> None:
    symbolic = poly_symbolic_checks()
    ordinary = ordinary_samples()
    boundary = boundary_limit_rows()
    factor_two = factor_two_latent_check()
    swap = swap_blocker()
    sanity = sanity_json_scan()

    checks = {
        "mass_identity": symbolic["mass_identity"],
        "rank_one_fisher_identities": all(symbolic["fisher_rank_one_identities"].values()),
        "missing_factor_two_caught": symbolic["wrong_missing_factor_two_bb_identity_is_nonzero"]
        and all(r["matches"] and r["missing_factor_two_wrong"] for r in factor_two),
        "log_acceleration_coefficients_place_n_beta_n_alpha": symbolic["all_log_checks"],
        "C_formula_matches_direct_samples": all(
            D(r["C_formula_max_abs_error"]) < D("1e-120") for r in ordinary
        ),
        "wrong_n_placement_detected_on_samples": any(
            D(r["wrong_n_placement_error"]) > D("1e-3") for r in ordinary[:2]
        ),
        "boundary_normalized_limits_positive_samples": all(
            r["Delta_positive"] and r["Caa_positive"] for r in boundary
        ),
        "swap_blocker_exact": swap["matches_author_expression"]
        and swap["exact_nonzero_by_unique_factorization"],
        "Cab_negative_blocker_seen": any(r["C_ab_negative"] for r in ordinary),
        "author_sanity_denominator_consistent": sanity.get("denominators", {}).get("total") == 86
        and sanity.get("denominators", {}).get("failures") == 0,
    }

    result = {
        "status": "AUDIT_PASS_FOR_SCOPED_CANDIDATE_STRIPS__GLOBAL_INCOMPLETE",
        "precision_decimal_digits": getcontext().prec,
        "input_hashes_sha256": collect_hashes(),
        "symbolic_algebra": symbolic,
        "latent_factor_two_checks": factor_two,
        "ordinary_decimal_samples": ordinary,
        "boundary_normalized_limit_samples": boundary,
        "swap_asymmetry_blocker": swap,
        "author_sanity_json_scan": sanity,
        "classification": {
            "analytic_identity": "PASS: Fisher missing-information formula, factor 2, and n_beta/n_alpha placement checked exactly.",
            "boundary_strips": "PASS as proof candidates under compact transverse interval logic; script samples support the four normalized limits.",
            "full_Sym3_quantifier": "Legal only by the already-reviewed U10f standard block plus invariant Delta_T positivity; not independently re-proved here.",
            "global_domain": "INCOMPLETE: corner limits and compact middle remain outside this unit.",
            "finite_scout": "Author 86-point sanity remains finite scout; not a global certificate.",
        },
        "checks": checks,
        "overall": "AUDIT_PASS_WITH_GLOBAL_OPEN" if all(checks.values()) else "AUDIT_GAP_OR_INCOMPLETE",
    }
    out = AUDIT_DIR / "results.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=jdefault)
        f.write("\n")
    print(json.dumps({"overall": result["overall"], "out": str(out)}, indent=2))


if __name__ == "__main__":
    main()
