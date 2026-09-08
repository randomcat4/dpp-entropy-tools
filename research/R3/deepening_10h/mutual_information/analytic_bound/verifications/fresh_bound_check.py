"""Independent verification for D10-C2 analytic_bound.

The script reads the frozen result files but does not import the author's
certificate scripts.  It reconstructs M,D, recomputes all 2048 quadratic exact
event coefficients, checks Mobius exact-event semantics at the center, and
recomputes the rational log/rounding/L2/L4/H''''/radius inequalities.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path


N = 11
GRID = 10**24
TERMS = 18
U = [-2, 1, -3, 3, -2, 3, 2, 2, -1, 2, 3]
V = [-1, 3, 3, -1, 2, 3, -3, -2, -3, -1, -2]

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "results"


def zeros(n: int, m: int) -> list[list[F]]:
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> list[list[F]]:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mat_add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_scale(c: F, a):
    return [[c * x for x in row] for row in a]


def leading_block(a, k: int):
    return [row[:k] for row in a[:k]]


def principal(a, indices):
    return [[a[i][j] for j in indices] for i in indices]


def bit_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def bareiss_int(a: list[list[int]]) -> int:
    n = len(a)
    if n == 0:
        return 1
    m = [row[:] for row in a]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            return 0
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j] * pivot_value - m[i][k] * m[k][j]
                if numerator % previous != 0:
                    raise ArithmeticError("Bareiss divisibility failure")
                m[i][j] = numerator // previous
        previous = pivot_value
        for i in range(k + 1, n):
            m[i][k] = 0
    return sign * m[-1][-1]


def det_fraction(a: list[list[F]]) -> F:
    if not a:
        return F(1)
    den = math.lcm(*(x.denominator for row in a for x in row))
    ints = [[int(x * den) for x in row] for row in a]
    return F(bareiss_int(ints), den ** len(a))


def rank_fraction(a: list[list[F]]) -> int:
    m = [row[:] for row in a]
    rows = len(m)
    cols = 0 if rows == 0 else len(m[0])
    rank = 0
    col = 0
    while rank < rows and col < cols:
        pivot = None
        for i in range(rank, rows):
            if m[i][col] != 0:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        scale = m[rank][col]
        m[rank] = [x / scale for x in m[rank]]
        for i in range(rows):
            if i != rank and m[i][col] != 0:
                factor = m[i][col]
                m[i] = [x - factor * y for x, y in zip(m[i], m[rank])]
        rank += 1
        col += 1
    return rank


def frozen_matrices() -> tuple[list[list[F]], list[list[F]]]:
    uu = sum(x * x for x in U)
    vv = sum(x * x for x in V)
    m = zeros(N, N)
    for i in range(N):
        m[i][i] = F(1, 3) + F(i + 1, 36)
        for j in range(i + 1, N):
            numerator = 3 + (((i + 1) * 7 + (j + 1) * 11) % 5)
            sign = -1 if ((i * j + i + j) % 2) else 1
            m[i][j] = m[j][i] = sign * F(numerator, 110)
    d = [
        [F(U[i] * U[j], uu) + F(V[i] * V[j], 2 * vv) for j in range(N)]
        for i in range(N)
    ]
    return m, d


def combine(m, d, t: F):
    return [[m[i][j] + t * d[i][j] for j in range(N)] for i in range(N)]


def event_probs_signed_matrix(k) -> list[F]:
    den = math.lcm(*(x.denominator for row in k for x in row))
    base = [[int(x * den) for x in row] for row in k]
    out: list[F] = []
    for mask in range(1 << N):
        a = [row[:] for row in base]
        missing = 0
        for i in range(N):
            if not ((mask >> i) & 1):
                a[i][i] -= den
                missing += 1
        out.append(F(((-1) ** missing) * bareiss_int(a), den**N))
    return out


def event_probs_mobius(k) -> list[F]:
    full = (1 << N) - 1
    inclusions = [
        det_fraction(principal(k, bit_indices(mask, N))) for mask in range(1 << N)
    ]
    out: list[F] = []
    for mask in range(1 << N):
        comp = full ^ mask
        sub = comp
        total = F(0)
        while True:
            total += (-1 if sub.bit_count() & 1 else 1) * inclusions[mask | sub]
            if sub == 0:
                break
            sub = (sub - 1) & comp
        out.append(total)
    return out


def exact_ldl_min(a) -> F:
    n = len(a)
    ell = zeros(n, n)
    pivots: list[F] = []
    for j in range(n):
        pivot = a[j][j] - sum(ell[j][r] ** 2 * pivots[r] for r in range(j))
        if pivot <= 0:
            raise ArithmeticError(f"nonpositive LDL pivot at {j}: {pivot}")
        pivots.append(pivot)
        ell[j][j] = F(1)
        for i in range(j + 1, n):
            ell[i][j] = (a[i][j] - sum(ell[i][r] * ell[j][r] * pivots[r] for r in range(j))) / pivot
    return min(pivots)


def floor_scaled(x: F) -> int:
    return x.numerator * GRID // x.denominator


def ceil_scaled(x: F) -> int:
    return -((-x.numerator * GRID) // x.denominator)


def atanh_log_bounds(z: F) -> tuple[F, F]:
    if not (F(1) <= z <= F(2)):
        raise ValueError(f"z outside [1,2]: {z}")
    x = (z - 1) / (z + 1)
    x2 = x * x
    power = x
    partial = F(0)
    for j in range(TERMS):
        partial += 2 * power / (2 * j + 1)
        power *= x2
    tail = 2 * power / ((2 * TERMS + 1) * (1 - x2))
    return partial, partial + tail


LOG2 = atanh_log_bounds(F(2))


def log_bounds_grid(p: F) -> tuple[F, F]:
    if not (0 < p <= 1):
        raise ValueError("probability outside (0,1]")
    k = max(0, p.denominator.bit_length() - p.numerator.bit_length())
    z = p * (2**k)
    while z < 1:
        k += 1
        z *= 2
    while z >= 2:
        k -= 1
        z /= 2
    lo, hi = atanh_log_bounds(z)
    lower = lo - k * LOG2[1]
    upper = hi - k * LOG2[0]
    return F(floor_scaled(lower), GRID), F(ceil_scaled(upper), GRID)


def load_coefficients() -> tuple[list[F], list[F], list[F]]:
    rows = [json.loads(line) for line in (RESULTS / "exact_coefficients.jsonl").read_text(encoding="utf-8").splitlines()]
    if len(rows) != 1 << N:
        raise AssertionError(f"coefficient line count {len(rows)}")
    if [row["mask"] for row in rows] != list(range(1 << N)):
        raise AssertionError("coefficient masks are not exactly 0..2047")
    return (
        [F(row["p"]) for row in rows],
        [F(row["a"]) for row in rows],
        [F(row["b"]) for row in rows],
    )


def recompute_intervals(p: list[F], a: list[F], b: list[F]) -> dict[str, F]:
    b_lo = b_hi = fisher_lo = fisher_hi = l2_lo = l2_hi = l4_lo = l4_hi = h4_upper = 0
    max_a = max(abs(x) / z for x, z in zip(a, p))
    max_b = max(abs(y) / z for y, z in zip(b, p))
    for prob, alpha, beta in zip(p, a, b):
        log_lo, log_hi = log_bounds_grid(prob)
        if beta >= 0:
            blog_lo, blog_hi = beta * log_lo, beta * log_hi
        else:
            blog_lo, blog_hi = beta * log_hi, beta * log_lo
        fisher = alpha * alpha / prob
        b_lo += floor_scaled(blog_lo)
        b_hi += ceil_scaled(blog_hi)
        fisher_lo += floor_scaled(fisher)
        fisher_hi += ceil_scaled(fisher)
        l2_lo += floor_scaled(blog_lo + fisher / 2)
        l2_hi += ceil_scaled(blog_hi + fisher / 2)
        l4 = beta * beta / (2 * prob) - alpha * alpha * beta / (2 * prob * prob) + alpha**4 / (12 * prob**3)
        l4_lo += floor_scaled(l4)
        l4_hi += ceil_scaled(l4)
        arel = abs(alpha) / prob
        brel = abs(beta) / prob
        slope = arel + 2 * brel
        fourth = prob * (24 * brel**2 + 48 * slope**2 * brel + 16 * slope**4)
        h4_upper += ceil_scaled(fourth)
    return {
        "B_lo": F(b_lo, GRID),
        "B_hi": F(b_hi, GRID),
        "Fisher_lo": F(fisher_lo, GRID),
        "Fisher_hi": F(fisher_hi, GRID),
        "L2_lo": F(l2_lo, GRID),
        "L2_hi": F(l2_hi, GRID),
        "L4_lo": F(l4_lo, GRID),
        "L4_hi": F(l4_hi, GRID),
        "H4_upper": F(h4_upper, GRID),
        "maxA": max_a,
        "maxB": max_b,
    }


def fstr(x):
    if isinstance(x, F):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, list):
        return [fstr(y) for y in x]
    if isinstance(x, dict):
        return {key: fstr(value) for key, value in x.items()}
    return x


def main() -> None:
    cert = json.loads((RESULTS / "certificate.json").read_text(encoding="utf-8"))
    radius_cert = json.loads((RESULTS / "radius_1_over_32.json").read_text(encoding="utf-8"))
    p_file, a_file, b_file = load_coefficients()
    m, d = frozen_matrices()

    p0 = event_probs_signed_matrix(m)
    p_plus = event_probs_signed_matrix(combine(m, d, F(1)))
    p_minus = event_probs_signed_matrix(combine(m, d, F(-1)))
    a_recomputed = [(x - y) / 2 for x, y in zip(p_plus, p_minus)]
    b_recomputed = [(x + y) / 2 - z for x, y, z in zip(p_plus, p_minus, p0)]
    p_at_2 = event_probs_signed_matrix(combine(m, d, F(2)))

    mobius_center = event_probs_mobius(m)
    intervals = recompute_intervals(p0, a_recomputed, b_recomputed)

    uu = sum(x * x for x in U)
    vv = sum(x * x for x in V)
    uv = sum(x * y for x, y in zip(U, V))
    gram_det = uu * vv - uv * uv
    d_rank = rank_fraction(d)
    d_trace = sum(d[i][i] for i in range(N))
    a_block = U[:5], V[:5]
    b_block = U[5:], V[5:]
    block_a_gram_det = sum(x*x for x in a_block[0]) * sum(y*y for y in a_block[1]) - sum(x*y for x, y in zip(*a_block)) ** 2
    block_b_gram_det = sum(x*x for x in b_block[0]) * sum(y*y for y in b_block[1]) - sum(x*y for x, y in zip(*b_block)) ** 2
    d_a_rank = rank_fraction(principal(d, list(range(5))))
    d_b_rank = rank_fraction(principal(d, list(range(5, N))))
    d_ab_nonzero = any(d[i][j] != 0 for i in range(5) for j in range(5, N))
    cross_sq = sum(m[i][j] ** 2 for i in range(5) for j in range(5, N))
    diag_bound = F(1, 36) - F(1, 32) * 8 * (F(1, 58) + F(1, 120))

    ldl_m = exact_ldl_min(mat_sub(m, mat_scale(F(1, 10), eye(N))))
    ldl_i_minus_m = exact_ldl_min(mat_sub(mat_sub(eye(N), m), mat_scale(F(1, 10), eye(N))))
    radius = F(1, 32)
    endpoint_minus = [z - radius * x + radius * radius * y for z, x, y in zip(p0, a_recomputed, b_recomputed)]
    endpoint_plus = [z + radius * x + radius * radius * y for z, x, y in zip(p0, a_recomputed, b_recomputed)]

    checks = {
        "coefficient_rows": len(p_file),
        "coefficients_match_recomputed_signed_event_determinants": p_file == p0 and a_file == a_recomputed and b_file == b_recomputed,
        "degree_two_check_at_t_2": p_at_2 == [z + 2 * x + 4 * y for z, x, y in zip(p0, a_recomputed, b_recomputed)],
        "center_mobius_matches_signed_event_formula": mobius_center == p0,
        "sum_p": sum(p0),
        "sum_a": sum(a_recomputed),
        "sum_b": sum(b_recomputed),
        "min_p": min(p0),
        "endpoint_min_p_at_radius": min(min(endpoint_minus), min(endpoint_plus)),
        "endpoint_sums_at_radius": [sum(endpoint_minus), sum(endpoint_plus)],
        "uu": uu,
        "vv": vv,
        "uv": uv,
        "gram_det": gram_det,
        "direction_rank": d_rank,
        "direction_trace": d_trace,
        "block_A_gram_det": block_a_gram_det,
        "block_B_gram_det": block_b_gram_det,
        "D_A_rank": d_a_rank,
        "D_B_rank": d_b_rank,
        "D_AB_nonzero": d_ab_nonzero,
        "cross_frobenius_squared": cross_sq,
        "diag_separation_bound": diag_bound,
        "ldl_min_M_minus_1_over_10_I": ldl_m,
        "ldl_min_I_minus_M_minus_1_over_10_I": ldl_i_minus_m,
        "B_interval": [intervals["B_lo"], intervals["B_hi"]],
        "Fisher_interval": [intervals["Fisher_lo"], intervals["Fisher_hi"]],
        "L2_interval": [intervals["L2_lo"], intervals["L2_hi"]],
        "L4_interval": [intervals["L4_lo"], intervals["L4_hi"]],
        "H4_upper": intervals["H4_upper"],
        "maxA": intervals["maxA"],
        "maxB": intervals["maxB"],
        "radius": radius,
        "radius_condition_actual": radius * intervals["maxA"] + radius * radius * intervals["maxB"],
        "radius_condition_simplified": radius * 4 + radius * radius * 3,
        "remainder_quadratic_cost_941": F(941, 24) * radius * radius,
        "spectral_margin_at_radius": F(1, 10) - radius * F(3, 2),
        "gap_bound_coeff_margin": intervals["L2_lo"] - F(941, 24) * radius * radius,
    }

    expected = {
        "event_count": cert["event_count"],
        "sum_probabilities": F(cert["sum_probabilities"]),
        "sum_a": F(cert["sum_a"]),
        "sum_b": F(cert["sum_b"]),
        "minimum_center_probability": F(cert["minimum_center_probability"]),
        "B_interval": [F(x) for x in cert["B_interval"]],
        "Fisher_interval": [F(x) for x in cert["Fisher_interval"]],
        "L2_interval": [F(x) for x in cert["L2_interval"]],
        "L4_interval": [F(x) for x in cert["L4_interval"]],
        "H4_upper": F(cert["uniform_fourth_derivative_upper"]),
        "maxA": F(cert["max_relative_a"]),
        "maxB": F(cert["max_relative_b"]),
        "radius_extension": F(radius_cert["radius"]),
        "gap_bound": radius_cert["uniform_gap_bound"],
        "spectral_margin": F(radius_cert["uniform_spectral_margin"]),
        "cross_lower_bound": F(radius_cert["uniform_cross_Frobenius_lower_bound"]),
        "diag_lower_bound": F(radius_cert["uniform_diagonal_separation_lower_bound"]),
    }

    predicates = [
        checks["coefficient_rows"] == 2048,
        checks["coefficients_match_recomputed_signed_event_determinants"],
        checks["degree_two_check_at_t_2"],
        checks["center_mobius_matches_signed_event_formula"],
        checks["sum_p"] == expected["sum_probabilities"] == 1,
        checks["sum_a"] == expected["sum_a"] == 0,
        checks["sum_b"] == expected["sum_b"] == 0,
        checks["min_p"] == expected["minimum_center_probability"] and checks["min_p"] > 0,
        checks["endpoint_min_p_at_radius"] > 0,
        checks["endpoint_sums_at_radius"] == [F(1), F(1)],
        gram_det == 3191 and d_rank == 2 and d_trace == F(3, 2),
        block_a_gram_det == 527 and block_b_gram_det == 1080,
        d_a_rank == 2 and d_b_rank == 2 and d_ab_nonzero,
        ldl_m == F(cert["base_ldl_minima"][0]) and ldl_i_minus_m == F(cert["base_ldl_minima"][1]),
        checks["B_interval"] == expected["B_interval"],
        checks["Fisher_interval"] == expected["Fisher_interval"],
        checks["L2_interval"] == expected["L2_interval"],
        checks["L4_interval"] == expected["L4_interval"],
        checks["H4_upper"] == expected["H4_upper"] and checks["H4_upper"] < 941,
        checks["maxA"] == expected["maxA"] and checks["maxA"] < 4,
        checks["maxB"] == expected["maxB"] and checks["maxB"] < 3,
        radius == expected["radius_extension"] == F(1, 32),
        checks["radius_condition_actual"] < F(1, 2),
        checks["radius_condition_simplified"] < F(1, 2),
        checks["remainder_quadratic_cost_941"] < F(1, 20),
        checks["spectral_margin_at_radius"] == expected["spectral_margin"] == F(17, 320),
        cross_sq > F(1, 16) and expected["cross_lower_bound"] == F(13, 64),
        diag_bound == expected["diag_lower_bound"] and diag_bound > F(1, 50),
        checks["gap_bound_coeff_margin"] > F(1, 2),
        radius_cert["uniform_gap_bound"] == "Delta(t) <= -t^2/2",
    ]

    result = {
        "status": "PASS" if all(predicates) else "FAIL",
        "failed_predicate_indices": [i for i, ok in enumerate(predicates) if not ok],
        "checks": checks,
        "expected_from_certificates": expected,
        "notes": [
            "Signed event determinant coefficients were recomputed at t=-1,0,1 and degree-2 checked at t=2.",
            "Center exact atoms were recomputed independently by inclusion determinants plus Mobius inversion.",
            "Log bounds use the same atanh tail theorem and explicit floor/ceil grid direction, recomputed without importing author scripts.",
            "The Taylor conclusion follows from L2_lower > 11/20 and 941/(24*32^2) < 1/20.",
        ],
    }
    print(json.dumps(fstr(result), indent=2))


if __name__ == "__main__":
    main()
