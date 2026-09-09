#!/usr/bin/env python3
"""
Independent exact checker for PR39's finite computational claims.

This script intentionally does not import the PR's audit code.  It rebuilds the
finite n=4 DPP laws from principal minors and Mobius inversion, checks the
equivalent row-determinant event formula, derives the entropy/KL series from the
resulting exact probability polynomials, and verifies the finite local-channel
fixture.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp


S = sp.S
I = sp.I


def rational(value: Any) -> sp.Rational:
    return sp.Rational(str(value))


def bit_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def popcount(mask: int) -> int:
    return int(mask).bit_count()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def as_fraction(value: Any) -> str:
    value = sp.factor(sp.simplify(value))
    if value == 0:
        return "0"
    return str(value)


def parse_fraction_list(values: list[Any]) -> list[sp.Rational]:
    return [rational(v) for v in values]


def assert_zero(value: Any, label: str) -> None:
    if sp.simplify(value) != 0:
        raise AssertionError(f"{label}: expected 0, got {sp.factor(value)}")


def assert_equal(actual: Any, expected: Any, label: str) -> None:
    assert_zero(sp.simplify(actual - expected), label)


def assert_list_equal(actual: list[Any], expected: list[Any], label: str) -> None:
    if len(actual) != len(expected):
        raise AssertionError(f"{label}: length {len(actual)} != {len(expected)}")
    for idx, (a, e) in enumerate(zip(actual, expected)):
        assert_equal(a, e, f"{label}[{idx}]")


def choose_existing(base: Path, candidates: list[str]) -> Path:
    for candidate in candidates:
        path = base / candidate
        if path.exists():
            return path
    joined = ", ".join(candidates)
    raise FileNotFoundError(f"none of these paths exists under {base}: {joined}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def serialize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serialize(v) for v in obj]
    if isinstance(obj, (sp.Integer, sp.Rational, sp.Expr)):
        return as_fraction(obj)
    return obj


def kernel_from_trig_spec(spec: dict[str, Any], z: Any) -> sp.Matrix:
    """Build K(i,j)=hat f(i-j) for the stated trigonometric polynomial."""
    n = int(spec["window"])
    mean = rational(spec["mean"])
    c2 = rational(spec["c_cos_2"])
    g_cos = rational(spec["g_cos_1"])
    g_sin = rational(spec["g_sin_1"])

    def coeff(d: int) -> Any:
        if d == 0:
            return mean
        if abs(d) == 2:
            return c2 / 2
        if d == 1:
            return z * (g_cos + I * g_sin) / 2
        if d == -1:
            return z * (g_cos - I * g_sin) / 2
        return S.Zero

    return sp.Matrix(n, n, lambda r, c: coeff(r - c))


def principal_minor(mat: sp.Matrix, mask: int) -> Any:
    if mask == 0:
        return S.One
    idx = bit_indices(mask, mat.rows)
    return sp.factor(mat.extract(idx, idx).det())


def inclusion_probabilities_by_mobius(K: sp.Matrix) -> list[Any]:
    """P(exact occupied set=S) from P(T subset occupied)=det(K_T)."""
    n = K.rows
    minors = [principal_minor(K, mask) for mask in range(1 << n)]
    out: list[Any] = []
    for exact in range(1 << n):
        total = S.Zero
        for sup in range(1 << n):
            if exact & ~sup:
                continue
            sign = -1 if (popcount(sup) - popcount(exact)) % 2 else 1
            total += sign * minors[sup]
        out.append(sp.factor(sp.expand(total)))
    return out


def exact_probabilities_by_row_determinant(K: sp.Matrix) -> list[Any]:
    """P(exact occupied set=S) by the standard mixed-row determinant formula."""
    n = K.rows
    eye = sp.eye(n)
    out: list[Any] = []
    for exact in range(1 << n):
        rows = []
        for r in range(n):
            source = K if ((exact >> r) & 1) else eye - K
            rows.append([source[r, c] for c in range(n)])
        out.append(sp.factor(sp.Matrix(rows).det()))
    return out


def poly_coefficients(probabilities: list[Any], z: sp.Symbol) -> tuple[list[Any], list[Any], list[Any]]:
    p0: list[Any] = []
    u2: list[Any] = []
    u4: list[Any] = []
    for mask, p in enumerate(probabilities):
        expr = sp.expand(p)
        poly = sp.Poly(expr, z)
        if poly.degree() > 4:
            raise AssertionError(f"event polynomial {mask} has degree {poly.degree()} > 4")
        for odd_power in (1, 3):
            assert_zero(poly.coeff_monomial(z**odd_power), f"event polynomial {mask} odd t^{odd_power} coefficient")
        for high_power in range(5, max(poly.degree(), 4) + 1):
            assert_zero(poly.coeff_monomial(z**high_power), f"event polynomial {mask} high t^{high_power} coefficient")
        p0.append(sp.factor(poly.coeff_monomial(z**0)))
        u2.append(sp.factor(poly.coeff_monomial(z**2)))
        u4.append(sp.factor(poly.coeff_monomial(z**4)))
    return p0, u2, u4


def kl_series_coefficients(p0: list[Any], u2: list[Any], u4: list[Any]) -> dict[str, Any]:
    """Derive D(P_t || P_0) through t^8 by formal series expansion."""
    z = sp.Symbol("z")
    total = S.Zero
    for q, a, b in zip(p0, u2, u4):
        perturb = a * z**2 + b * z**4
        total += sp.series((q + perturb) * sp.log(1 + perturb / q), z, 0, 10).removeO()
    total = sp.expand(total)
    return {
        "t4": sp.factor(total.coeff(z, 4)),
        "t6": sp.factor(total.coeff(z, 6)),
        "t8": sp.factor(total.coeff(z, 8)),
    }


def boolean_character_moment(probabilities: list[Any], subset: int, n: int) -> Any:
    total = S.Zero
    for exact, prob in enumerate(probabilities):
        empty_inside_subset = popcount(subset & (((1 << n) - 1) ^ exact))
        total += ((-1) ** empty_inside_subset) * prob
    return sp.factor(sp.simplify(total))


def boolean_determinant_probability(B: sp.Matrix, exact: int) -> Any:
    n = B.rows
    signs = [1 if ((exact >> i) & 1) else -1 for i in range(n)]
    D = sp.diag(*signs)
    return sp.factor((sp.eye(n) + D * B).det() / (2**n))


def audit_example(label: str, spec: dict[str, Any], author: dict[str, Any]) -> dict[str, Any]:
    z = sp.Symbol(f"{label}_t", real=True)
    n = int(spec["window"])
    Kz = kernel_from_trig_spec(spec, z)

    mobius_poly = inclusion_probabilities_by_mobius(Kz)
    row_poly = exact_probabilities_by_row_determinant(Kz)
    assert_list_equal(row_poly, mobius_poly, f"{label} row determinant law vs Mobius law")

    p0, u2, u4 = poly_coefficients(mobius_poly, z)
    assert_list_equal(p0, parse_fraction_list(author["probabilities_t_zero"]), f"{label} p(t=0)")
    assert_list_equal(u2, parse_fraction_list(author["polynomial_coefficient_t2"]), f"{label} t^2 coefficients")
    assert_list_equal(u4, parse_fraction_list(author["polynomial_coefficient_t4"]), f"{label} t^4 coefficients")
    assert_equal(sum(p0), S.One, f"{label} p0 mass")
    assert_equal(sum(u2), S.Zero, f"{label} t^2 mass")
    assert_equal(sum(u4), S.Zero, f"{label} t^4 mass")

    half = rational("1/2")
    Khalf = kernel_from_trig_spec(spec, half)
    half_law = inclusion_probabilities_by_mobius(Khalf)
    assert_list_equal([p.subs(z, half) for p in mobius_poly], half_law, f"{label} symbolic law at t=1/2")
    assert_list_equal(half_law, parse_fraction_list(author["probabilities_t_half"]), f"{label} p(t=1/2)")
    if any(sp.simplify(p) <= 0 for p in half_law):
        raise AssertionError(f"{label}: not all t=1/2 probabilities are positive")
    if any(sp.simplify(p) <= 0 for p in p0):
        raise AssertionError(f"{label}: not all t=0 probabilities are positive")
    assert_equal(sum(half_law), S.One, f"{label} p(t=1/2) mass")

    coeffs = kl_series_coefficients(p0, u2, u4)
    for power, expected in author["KL_coefficients"].items():
        assert_equal(coeffs[power], rational(expected), f"{label} KL coefficient {power}")

    B = 2 * Khalf - sp.eye(n)
    for subset in range(1 << n):
        moment = boolean_character_moment(half_law, subset, n)
        minor = principal_minor(B, subset)
        assert_equal(moment, minor, f"{label} Boolean moment subset {subset}")
    for exact in range(1 << n):
        assert_equal(boolean_determinant_probability(B, exact), half_law[exact], f"{label} Boolean determinant exact {exact}")

    g_cos = rational(spec["g_cos_1"])
    g_sin = rational(spec["g_sin_1"])
    gamma = sp.factor((g_cos**2 + g_sin**2) / 4)
    assert_equal(gamma, rational(author["gamma"]), f"{label} gamma")
    lower = sp.factor(rational("4/3") * (n - int(spec["k"])) * gamma**2)
    assert_equal(lower, rational(author["quartic_lower_bound"]), f"{label} quartic lower bound")

    a = rational(spec["a"])
    b_upper = rational(spec["b_upper"])
    R = rational(spec["R"])
    M_upper = rational(spec["M_upper"])
    T = rational(spec["T"])
    residual = sp.factor(8 * gamma**2 * R**6 - 54 * M_upper * T**2)
    assert_equal(residual, rational(author["parameter_inequality_residual"]), f"{label} residual")
    correction = sp.factor(rational("2/3") * gamma**2)
    assert_equal(correction, rational(author["rate_quartic_correction"]), f"{label} rate correction")
    if not (2 * T <= R and a < 1 and b_upper > 0 and residual > 0):
        raise AssertionError(f"{label}: parameter inequalities are not certified")

    return {
        "status": "PASS",
        "n": n,
        "event_polynomial_method": "principal minors plus Mobius inversion, cross-checked by mixed-row determinants",
        "event_polynomial_degree": "even through t^4 for all 16 events",
        "positive_probability_checks": {"t0": True, "t_half": True},
        "boolean_character_moments_checked": 16,
        "boolean_determinant_events_checked": 16,
        "KL_coefficients": serialize(coeffs),
        "gamma": serialize(gamma),
        "quartic_lower_bound": serialize(lower),
        "parameter_inequality_residual": serialize(residual),
        "rate_quartic_correction": serialize(correction),
    }


def audit_closed_walks(spec: dict[str, Any], walk_spec: dict[str, Any], author: dict[str, Any]) -> dict[str, Any]:
    n = int(spec["window"])
    z = rational(walk_spec["parameter"])
    max_length = int(walk_spec["max_length"])
    K = kernel_from_trig_spec(spec, z)
    probabilities = inclusion_probabilities_by_mobius(K)
    B = 2 * K - sp.eye(n)
    principal_minors = [principal_minor(B, mask) for mask in range(1 << n)]

    terms = []
    for ell in range(1, max_length + 1):
        lhs = S.Zero
        for exact, prob in enumerate(probabilities):
            signs = [1 if ((exact >> i) & 1) else -1 for i in range(n)]
            D = sp.diag(*signs)
            lhs += prob * sp.trace((D * B) ** ell)
        lhs = sp.factor(sp.simplify(lhs))

        rhs = S.Zero
        nonzero = 0
        for walk in itertools.product(range(n), repeat=ell):
            product = S.One
            odd_mask = 0
            for j, src in enumerate(walk):
                dst = walk[(j + 1) % ell]
                product *= B[src, dst]
                odd_mask ^= 1 << src
            product = sp.simplify(product)
            if product != 0:
                nonzero += 1
                rhs += product * principal_minors[odd_mask]
        rhs = sp.factor(sp.simplify(rhs))
        assert_equal(lhs, rhs, f"closed-walk moment identity length {ell}")
        expected = author["terms"][ell - 1]
        if int(expected["length"]) != ell:
            raise AssertionError(f"author walk term order mismatch at length {ell}")
        if int(expected["nonzero_closed_walks"]) != nonzero:
            raise AssertionError(f"length {ell}: nonzero walk count {nonzero} != {expected['nonzero_closed_walks']}")
        assert_equal(lhs, rational(expected["expected_trace"]), f"closed-walk expected trace length {ell}")
        terms.append({"length": ell, "nonzero_closed_walks": nonzero, "expected_trace": lhs})

    F_partial = S.Zero
    for item in terms:
        ell = int(item["length"])
        F_partial += ((-1) ** (ell + 1)) * item["expected_trace"] / ell
    F_partial = sp.factor(sp.simplify(F_partial))
    assert_equal(F_partial, rational(author["F_partial"]), "closed-walk F_partial")

    row_norm = S.Zero
    for r in range(n):
        total = sum(abs(sp.simplify(B[r, c])) for c in range(n))
        row_norm = max(row_norm, sp.simplify(total))
    assert_equal(row_norm, rational(author["actual_row_norm"]), "closed-walk row norm")
    tail = sp.factor(n * row_norm ** (max_length + 1) / ((max_length + 1) * (1 - row_norm)))
    assert_equal(tail, rational(author["absolute_tail_bound_from_proof"]), "closed-walk tail bound")

    return {
        "status": "PASS",
        "parameter": serialize(z),
        "terms": serialize(terms),
        "F_partial": serialize(F_partial),
        "actual_row_norm": serialize(row_norm),
        "absolute_tail_bound_from_proof": serialize(tail),
        "scope": "finite trace/moment identity and stated theorem tail constant only",
    }


def two_by_two_law(K: sp.Matrix) -> list[Any]:
    return inclusion_probabilities_by_mobius(K)


def audit_channel(channel_spec: dict[str, Any], author: dict[str, Any]) -> dict[str, Any]:
    d = rational(channel_spec["diagonal"])
    w = rational(channel_spec["within_block"])
    eps = rational(channel_spec["epsilon"])
    r = rational(channel_spec["r"])
    A = sp.Matrix([[d, w], [w, d]])
    C = eps * sp.eye(2)

    def block_kernel(scale: Any) -> sp.Matrix:
        return A.row_join(scale * C).col_join((scale * C).T.row_join(A))

    det_full = sp.factor(block_kernel(sp.Symbol("s")).det())
    p0 = sp.factor(det_full.subs({"s": 0}))
    p1 = sp.factor(det_full.subs({"s": 1}))
    actual = sp.factor(det_full.subs({"s": r}))
    forced = sp.factor(p0 + r**2 * (p1 - p0))
    difference = sp.factor(forced - actual)
    assert_equal(actual, rational(author["all_occupied_actual"]), "channel all-occupied actual")
    assert_equal(forced, rational(author["all_occupied_forced_by_local_channels"]), "channel forced all-occupied value")
    assert_equal(difference, rational(author["difference"]), "channel conflict difference")
    assert_equal(difference, eps**4 * r**2 * (1 - r**2), "channel difference closed form")

    eigenvals = sorted([sp.factor(ev) for ev in block_kernel(1).eigenvals().keys()], key=lambda x: float(x), reverse=True)
    assert_list_equal(eigenvals, parse_fraction_list(author["eigenvalues_K1"]), "channel K1 eigenvalues")
    if not all(0 < ev < 1 for ev in eigenvals):
        raise AssertionError("channel K1 is not a strict contraction")

    base_law = two_by_two_law(A)
    delta = rational("1/128")
    rank_vectors = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1])]
    columns = []
    for v in rank_vectors:
        perturbed = two_by_two_law(A + delta * (v * v.T))
        columns.append([(perturbed[i] - base_law[i]) / delta for i in range(4)])
    rank = sp.Matrix(columns).T.rank()
    if int(rank) != int(author["derivative_span_rank"]):
        raise AssertionError(f"channel derivative rank {rank} != {author['derivative_span_rank']}")

    v = sp.Matrix([1, 2])
    wvec = sp.Matrix([1, -1])
    small = rational("1/128")
    joint = inclusion_probabilities_by_mobius(A.row_join(small * (v * wvec.T)).col_join((small * (v * wvec.T)).T.row_join(A)))
    dv = [(two_by_two_law(A + small * (v * v.T))[i] - base_law[i]) / small for i in range(4)]
    dw = [(two_by_two_law(A + small * (wvec * wvec.T))[i] - base_law[i]) / small for i in range(4)]
    for xmask in range(4):
        for ymask in range(4):
            factorized = base_law[xmask] * base_law[ymask] - small**2 * dv[xmask] * dw[ymask]
            assert_equal(joint[xmask | (ymask << 2)], factorized, f"channel rank-one factorization {xmask},{ymask}")

    return {
        "status": "PASS",
        "eigenvalues_K1": serialize(eigenvals),
        "derivative_span_rank": int(rank),
        "all_occupied_actual": serialize(actual),
        "all_occupied_forced_by_local_channels": serialize(forced),
        "difference": serialize(difference),
        "rank_one_factorization": "PASS",
        "scope": "finite local-channel fixture only",
    }


def audit_tail_series(author_value: str) -> dict[str, Any]:
    x = sp.Symbol("x")
    remainder_second_derivative = (sp.diff(1 / (1 - x**2), x, 2) - 2 - 12 * x**2) / x**4
    value = sp.factor(remainder_second_derivative.subs(x, rational("1/2")))
    assert_equal(value, rational(author_value), "tail series at 1/2")
    if not value < 54:
        raise AssertionError("tail series comparison value is not < 54")
    return {"status": "PASS", "tail_series_at_half": serialize(value), "strictly_less_than_54": True}


def run(input_path: Path, author_output_path: Path, output_path: Path) -> dict[str, Any]:
    started = time.perf_counter()
    inputs = load_json(input_path)
    author = load_json(author_output_path)

    result = {
        "status": "PASS_INDEPENDENT_EXACT_CHECKS",
        "pr": 39,
        "head": "5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f",
        "method_independence": [
            "does not import or execute the PR author audit script",
            "event probabilities are rebuilt from principal minors and Mobius inversion",
            "event probabilities are cross-checked by mixed-row determinants",
            "KL coefficients are derived by formal log-series expansion from exact event polynomials",
            "local-channel conflict is recomputed from block determinants",
        ],
        "inputs_sha256": sha256_file(input_path),
        "author_output_sha256": sha256_file(author_output_path),
        "script_sha256": sha256_file(Path(__file__)),
        "checks": {
            "example": audit_example("even", inputs["example"], author["example"]),
            "non_even_example": audit_example("non_even", inputs["non_even_example"], author["non_even_example"]),
            "walks": audit_closed_walks(inputs["example"], inputs["closed_walk"], author["walks"]),
            "channel": audit_channel(inputs["channel_obstruction"], author["channel"]),
            "tail_series": audit_tail_series(author["tail_series_at_half"]),
        },
        "limits": [
            "finite n=4 named examples only",
            "no scan over other symbols or orbit families",
            "no independent proof of the full analytic theorem or entropy-rate limit",
            "no certification of the full legal interval beyond the stated finite fixtures",
        ],
        "versions": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
    }
    result["seconds"] = round(time.perf_counter() - started, 6)
    dump_json(output_path, serialize(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent exact reproducibility checker for PR39 finite computations.")
    cwd = Path.cwd()
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to research/W2/nonconstant_orbit/inputs/new.json or the frozen local copy.",
    )
    parser.add_argument(
        "--author-output",
        type=Path,
        default=None,
        help="Path to research/W2/nonconstant_orbit/output/new_audit.json or the frozen local copy.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=cwd / "independent_pr39_exact_check.json",
        help="Path for this checker's JSON report.",
    )
    args = parser.parse_args()

    input_path = args.input or choose_existing(
        cwd,
        [
            "research/W2/nonconstant_orbit/inputs/new.json",
            "inputs/new.json",
            "research__W2__nonconstant_orbit__inputs__new.json",
        ],
    )
    author_output_path = args.author_output or choose_existing(
        cwd,
        [
            "research/W2/nonconstant_orbit/output/new_audit.json",
            "output/new_audit.json",
            "research__W2__nonconstant_orbit__output__new_audit.json",
        ],
    )

    try:
        result = run(input_path.resolve(), author_output_path.resolve(), args.output.resolve())
    except Exception as exc:  # keep a machine-readable failure artifact
        failure = {
            "status": "FAIL_INDEPENDENT_EXACT_CHECKS",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "versions": {
                "python": platform.python_version(),
                "sympy": getattr(sp, "__version__", "unknown"),
                "platform": platform.platform(),
            },
        }
        dump_json(args.output.resolve(), failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps({"status": result["status"], "output": str(args.output.resolve()), "seconds": result["seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
