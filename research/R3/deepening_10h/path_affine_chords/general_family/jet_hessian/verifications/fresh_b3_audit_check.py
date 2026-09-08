"""Fresh non-author checks for D10-B3 jet_hessian.

The script is intentionally self-contained: it does not import the author
implementation.  It reads only frozen/result evidence and prints a compact JSON
audit record.  No output files are written by this script.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Sequence


for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


HERE = Path(__file__).resolve().parent
ROUTE = HERE.parent


def log_scalar(x):
    return x.ln() if isinstance(x, Decimal) else math.log(x)


def exp_scalar(x):
    return x.exp() if isinstance(x, Decimal) else math.exp(x)


def finite_positive(x) -> bool:
    return x > 0 and (isinstance(x, Decimal) or math.isfinite(float(x)))


def jadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def jsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def jmul(a, b):
    return (
        a[0] * b[0],
        a[1] * b[0] + a[0] * b[1],
        a[2] * b[0] + 2 * a[1] * b[1] + a[0] * b[2],
    )


def jsquare(a):
    return (a[0] * a[0], 2 * a[0] * a[1], 2 * a[1] * a[1] + 2 * a[0] * a[2])


def jlog(a):
    return (log_scalar(a[0]), a[1] / a[0], a[2] / a[0] - (a[1] * a[1]) / (a[0] * a[0]))


def jxlogx(a):
    logv = log_scalar(a[0])
    return (a[0] * logv, a[1] * (logv + 1), a[2] * (logv + 1) + a[1] * a[1] / a[0])


def jdiv(a, b):
    c0 = a[0] / b[0]
    c1 = (a[1] - b[1] * c0) / b[0]
    c2 = (a[2] - 2 * b[1] * c1 - b[2] * c0) / b[0]
    return (c0, c1, c2)


def jinv_legacy_float(a):
    inv = 1.0 / a[0]
    return (inv, -a[1] * inv * inv, 2.0 * a[1] * a[1] * inv**3 - a[2] * inv * inv)


def l_part_jets(beta: Sequence, tau: Sequence, delta: Sequence):
    n = len(tau)
    zero = tau[0] * 0
    one = zero + 1
    diag = []
    edge = []
    w = []
    for t, d in zip(tau, delta):
        inv = one / t
        w.append((inv, -d * inv * inv, 2 * d * d * inv * inv * inv))
    for i in range(n - 1):
        b2 = beta[i] * beta[i]
        value = jadd(w[i], (b2 * w[i + 1][0], b2 * w[i + 1][1], b2 * w[i + 1][2]))
        diag.append((value[0] - one, value[1], value[2]))
        edge.append((-beta[i] * w[i + 1][0], -beta[i] * w[i + 1][1], -beta[i] * w[i + 1][2]))
    diag.append((w[-1][0] - one, w[-1][1], w[-1][2]))
    return diag, edge


def entropy_jet(beta: Sequence, tau: Sequence, delta: Sequence):
    diag, edge = l_part_jets(beta, tau, delta)
    n = len(diag)
    zero = tau[0] * 0
    one = zero + 1
    jzero = (zero, zero, zero)
    jone = (one, zero, zero)
    kappa = [[jzero for _ in range(n)] for _ in range(n)]
    for start in range(n):
        prev2 = jone
        prev1 = diag[start]
        if not finite_positive(prev1[0]):
            raise ValueError("nonpositive interval determinant")
        kappa[start][start] = prev1
        for end in range(start + 1, n):
            current = jsub(jmul(diag[end], prev1), jmul(jsquare(edge[end - 1]), prev2))
            if not finite_positive(current[0]):
                raise ValueError("nonpositive interval determinant")
            kappa[start][end] = current
            prev2, prev1 = prev1, current
    z = [jzero for _ in range(n + 1)]
    tlog = [jzero for _ in range(n + 1)]
    z[0] = jone
    for length in range(1, n + 1):
        end = length - 1
        z_value = z[length - 1]
        t_value = tlog[length - 1]
        for start in range(length):
            prefix_len = 0 if start == 0 else start - 1
            block = kappa[start][end]
            prefix_z = z[prefix_len]
            z_value = jadd(z_value, jmul(prefix_z, block))
            t_value = jadd(t_value, jmul(block, tlog[prefix_len]))
            t_value = jadd(t_value, jmul(prefix_z, jxlogx(block)))
        z[length] = z_value
        tlog[length] = t_value
    h = jsub(jlog(z[n]), jdiv(tlog[n], z[n]))
    return {
        "H": h[0],
        "H1": h[1],
        "H2": h[2],
        "Z": z[n][0],
        "Z1": z[n][1],
        "Z2": z[n][2],
        "T": tlog[n][0],
        "T1": tlog[n][1],
        "T2": tlog[n][2],
        "interval_states": n * (n + 1) // 2,
    }


def entropy_value(beta: Sequence, tau: Sequence):
    zero = tau[0] * 0
    delta = [zero for _ in tau]
    return entropy_jet(beta, tau, delta)["H"]


def exact_u_inverse(beta: Sequence[Fraction]):
    n = len(beta) + 1
    u = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        for row in range(col + 1, n):
            u[row][col] = beta[row - 1] * u[row - 1][col]
    return u


def exact_k(beta: Sequence[Fraction], tau: Sequence[Fraction]):
    n = len(tau)
    u = exact_u_inverse(beta)
    k = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for r in range(n):
        for c in range(n):
            k[r][c] -= sum(u[r][a] * tau[a] * u[c][a] for a in range(n))
    return k


def det_fraction(a):
    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = Fraction(1)
    prev = Fraction(1)
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if m[i][k] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pv = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pv - m[i][k] * m[k][j]) / prev
            m[i][k] = Fraction(0)
        prev = pv
    return sign * m[-1][-1]


def exact_atom_probs(beta: Sequence[Fraction], tau: Sequence[Fraction]):
    k = exact_k(beta, tau)
    n = len(tau)
    inc = []
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        inc.append(det_fraction([[k[i][j] for j in idx] for i in idx]))
    p = inc[:]
    for bit in range(n):
        for mask in range(1 << n):
            if not ((mask >> bit) & 1):
                p[mask] -= p[mask | (1 << bit)]
    assert sum(p) == 1
    assert min(p) > 0
    return p


def dec_fraction(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def low_dim_exact_gate():
    beta = [Fraction(1, 6), Fraction(-1, 5), Fraction(2, 7), Fraction(-1, 4)]
    tau = [Fraction(1, 7), Fraction(1, 8), Fraction(1, 9), Fraction(1, 10), Fraction(1, 11)]
    delta = [Fraction(0), tau[1] * Fraction(1, 7), Fraction(0), -tau[3] * Fraction(1, 9), Fraction(0)]
    pm = exact_atom_probs(beta, [x - y for x, y in zip(tau, delta)])
    p0 = exact_atom_probs(beta, tau)
    pp = exact_atom_probs(beta, [x + y for x, y in zip(tau, delta)])
    p1 = [(b - a) / 2 for a, b in zip(pm, pp)]
    p2 = [a + b - 2 * c for a, c, b in zip(pm, p0, pp)]
    assert sum(p1) == 0 and sum(p2) == 0
    with localcontext() as ctx:
        ctx.prec = 90
        h0 = -sum(dec_fraction(p) * dec_fraction(p).ln() for p in p0)
        h1 = -sum(dec_fraction(a) * dec_fraction(p).ln() for p, a in zip(p0, p1))
        h2 = -sum(dec_fraction(b) * dec_fraction(p).ln() + dec_fraction(a * a / p) for p, a, b in zip(p0, p1, p2))
        bdec = [dec_fraction(x) for x in beta]
        tdec = [dec_fraction(x) for x in tau]
        ddec = [dec_fraction(x) for x in delta]
        dp = entropy_jet(bdec, tdec, ddec)
        return {
            "n": 5,
            "rank_delta_support": sum(x != 0 for x in delta),
            "events": 32,
            "min_atom": str(min(p0)),
            "H": str(+h0),
            "H1": str(+h1),
            "H2": str(+h2),
            "dp_H": str(+dp["H"]),
            "dp_H1": str(+dp["H1"]),
            "dp_H2": str(+dp["H2"]),
            "abs_diff": {
                "H": str(+abs(dp["H"] - h0)),
                "H1": str(+abs(dp["H1"] - h1)),
                "H2": str(+abs(dp["H2"] - h2)),
            },
        }


def l_parts_float(beta: Sequence[float], tau: Sequence[float]):
    inv = [1.0 / x for x in tau]
    diag = [inv[i] + beta[i] * beta[i] * inv[i + 1] - 1.0 for i in range(len(beta))]
    diag.append(inv[-1] - 1.0)
    edge = [-beta[i] * inv[i + 1] for i in range(len(beta))]
    return diag, edge


def min_ldl_pivot_float(diag: Sequence[float], edge: Sequence[float]):
    pivot = diag[0]
    best = pivot
    for i in range(1, len(diag)):
        if pivot <= 0.0 or not math.isfinite(pivot):
            return pivot
        pivot = diag[i] - edge[i - 1] * edge[i - 1] / pivot
        best = min(best, pivot)
    return best


def admissible_l(beta: Sequence[float], tau: Sequence[float], margin: float = 1e-11):
    if any(t <= 0.0 or not math.isfinite(t) for t in tau):
        return False
    diag, edge = l_parts_float(beta, tau)
    return min_ldl_pivot_float(diag, edge) > margin


def structured_beta(n: int):
    return [((-1.0) ** i) * (0.16 + 0.30 * ((5 * i + 2) % 11) / 10.0) for i in range(n - 1)]


def random_beta(n: int, rng: random.Random):
    return [(-1.0 if rng.randrange(2) else 1.0) * rng.uniform(0.08, 0.58) for _ in range(n - 1)]


def max_scale_for_profile(beta: Sequence[float], profile: Sequence[float]):
    lo = 0.0
    hi = 1.0
    while admissible_l(beta, [hi * x for x in profile]) and hi < 1e6:
        hi *= 2.0
    for _ in range(72):
        mid = 0.5 * (lo + hi)
        if admissible_l(beta, [mid * x for x in profile]):
            lo = mid
        else:
            hi = mid
    return lo


def random_center(beta: Sequence[float], rng: random.Random):
    n = len(beta) + 1
    profile = [math.exp(rng.uniform(math.log(0.65), math.log(1.55))) for _ in range(n)]
    smax = max_scale_for_profile(beta, profile)
    if not math.isfinite(smax) or smax <= 0.0:
        return None
    scale = rng.uniform(0.22, 0.88) * smax
    tau = [scale * x for x in profile]
    return tau if admissible_l(beta, tau) else None


def random_delta(tau: Sequence[float], support_size: int, rng: random.Random):
    n = len(tau)
    support = list(range(n)) if support_size >= n else rng.sample(range(n), support_size)
    raw = [0.0] * n
    for i in support:
        raw[i] = rng.gauss(0.0, 1.0)
    raw_norm = max(abs(raw[i]) for i in support)
    if raw_norm == 0.0:
        raw[support[0]] = 1.0
        raw_norm = 1.0
    rel_scale = rng.uniform(0.20, 1.00)
    delta = [0.0] * n
    for i in support:
        delta[i] = rel_scale * tau[i] * raw[i] / raw_norm
    return delta


def column_gram_for_r_inverse(beta: Sequence[float]):
    n = len(beta) + 1
    tail = [1.0] * n
    for i in range(n - 2, -1, -1):
        tail[i] = 1.0 + beta[i] * beta[i] * tail[i + 1]
    gram = [[0.0] * n for _ in range(n)]
    for i in range(n):
        gram[i][i] = tail[i]
        prod = 1.0
        for j in range(i + 1, n):
            prod *= beta[j - 1]
            gram[i][j] = prod * tail[j]
            gram[j][i] = gram[i][j]
    return gram


def kdot_norm_sq(gram, delta: Sequence[float]):
    total = 0.0
    for i, di in enumerate(delta):
        if di == 0.0:
            continue
        inner = 0.0
        for j, dj in enumerate(delta):
            if dj != 0.0:
                inner += dj * gram[i][j] * gram[i][j]
        total += di * inner
    return 0.0 if -1e-14 < total < 0.0 else total


def replay_scan(summary):
    rng = random.Random(20260908)
    total = 0
    positive = 0
    global_max = None
    closest = None
    failures = 0
    for n in range(5, 101):
        for trial in range(24):
            beta = structured_beta(n) if trial % 7 == 0 else random_beta(n, rng)
            tau = random_center(beta, rng)
            if tau is None:
                failures += 2
                continue
            gram = column_gram_for_r_inverse(beta)
            for bucket, support_size in (("rank2", 2), ("full_rank", n)):
                delta = random_delta(tau, support_size, rng)
                norm = kdot_norm_sq(gram, delta)
                if norm <= 0.0 or not math.isfinite(norm):
                    failures += 1
                    continue
                try:
                    jet = entropy_jet(beta, tau, delta)
                    value = jet["H2"] / norm
                except (ValueError, OverflowError):
                    failures += 1
                    continue
                total += 1
                rec = {
                    "n": n,
                    "bucket": bucket,
                    "trial": trial,
                    "H2": jet["H2"],
                    "norm": norm,
                    "normalized": value,
                    "support": [i for i, x in enumerate(delta) if x != 0.0][:16],
                }
                if value > 1e-10:
                    positive += 1
                if global_max is None or value > global_max["normalized"]:
                    global_max = rec
                if closest is None or abs(value) < abs(closest["normalized"]):
                    closest = rec
    expected = summary["stable_float_scout"]
    return {
        "seed": 20260908,
        "n_range": [5, 100],
        "trials_per_n": 24,
        "buckets": ["rank2", "full_rank"],
        "total_evaluations": total,
        "failures": failures,
        "positive_normalized_gt_1e-10": positive,
        "global_max": global_max,
        "closest_to_zero": closest,
        "matches_summary": {
            "total_evaluations": total == expected["total_evaluations"],
            "positive_count": positive == expected["positive_stable_float_normalized_H2_gt_1e-10_count"],
            "global_max_identity": (
                global_max["n"] == expected["global_max_normalized"]["n"]
                and global_max["bucket"] == expected["global_max_normalized"]["bucket"]
                and global_max["trial"] == expected["global_max_normalized"]["trial"]
            ),
            "global_max_value_abs_diff": abs(
                global_max["normalized"] - expected["global_max_normalized"]["normalized_H2_per_frobenius_norm_sq"]
            ),
        },
    }


def parse_decimal_list(values):
    return [Decimal(str(x)) for x in values]


def parse_float_list(values):
    return [float(x) for x in values]


def p_parts_fraction(beta: Sequence[Fraction], tau: Sequence[Fraction]):
    inv = [Fraction(1, 1) / x for x in tau]
    diag = [inv[i] + beta[i] * beta[i] * inv[i + 1] for i in range(len(beta))]
    diag.append(inv[-1])
    edge = [-beta[i] * inv[i + 1] for i in range(len(beta))]
    return diag, edge


def ldl_pivots_fraction(diag: Sequence[Fraction], edge: Sequence[Fraction]):
    pivots = []
    pivot = diag[0]
    pivots.append(pivot)
    for i in range(1, len(diag)):
        if pivot <= 0:
            break
        pivot = diag[i] - edge[i - 1] * edge[i - 1] / pivot
        pivots.append(pivot)
    return pivots


def spectral_certificate(params):
    beta = [Fraction(x) for x in params["beta"]]
    tau0 = [Fraction(x) for x in params["tau"]]
    delta = [Fraction(x) for x in params["delta"]]
    rows = []
    for step in (Fraction(-1, 10), Fraction(1, 10)):
        tau = [t + step * d for t, d in zip(tau0, delta)]
        diag, edge = p_parts_fraction(beta, tau)
        left = ldl_pivots_fraction([x - 4 for x in diag], edge)
        right = ldl_pivots_fraction([50 - x for x in diag], [-e for e in edge])
        rows.append(
            {
                "t": str(step),
                "P_minus_4I_pivots": len(left),
                "P_minus_4I_min_pivot_float": float(min(left)),
                "P_minus_4I_positive": len(left) == len(tau) and all(x > 0 for x in left),
                "50I_minus_P_pivots": len(right),
                "50I_minus_P_min_pivot_float": float(min(right)),
                "50I_minus_P_positive": len(right) == len(tau) and all(x > 0 for x in right),
            }
        )
    return {
        "rows": rows,
        "uniform_interval": "[-1/10,1/10]",
        "bound": "4I < P(t) < 50I at endpoints, hence 1/50 I < S(t) < 1/4 I on the interval by affine S(t)",
        "rank_delta_support": sum(x != 0 for x in delta),
        "strict_margin_lower_bound": "1/50",
    }


def n93_stability(params, summary):
    beta_f = parse_float_list(params["beta"])
    tau_f = parse_float_list(params["tau"])
    delta_f = parse_float_list(params["delta"])
    float_jet = entropy_jet(beta_f, tau_f, delta_f)
    z = (float_jet["Z"], float_jet["Z1"], float_jet["Z2"])
    t = (float_jet["T"], float_jet["T1"], float_jet["T2"])
    legacy_ratio = jmul(t, jinv_legacy_float(z))
    legacy_h2 = jlog(z)[2] - legacy_ratio[2]
    with localcontext() as ctx:
        ctx.prec = 80
        beta_d = parse_decimal_list(params["beta"])
        tau_d = parse_decimal_list(params["tau"])
        delta_d = parse_decimal_list(params["delta"])
        decimal_jet = entropy_jet(beta_d, tau_d, delta_d)
        h = Decimal("0.0005")
        hm = entropy_value(beta_d, [x - h * y for x, y in zip(tau_d, delta_d)])
        hp = entropy_value(beta_d, [x + h * y for x, y in zip(tau_d, delta_d)])
        h0 = decimal_jet["H"]
        chord_h2 = +((hp + hm - 2 * h0) / (h * h))
        gap = +((hp + hm) / 2 - h0)
        inv_z_decimal_cubed = (Decimal(1) / Decimal(str(float_jet["Z"]))) ** 3
        predicted_error = Decimal(2) * (decimal_jet["T"] / decimal_jet["Z"]) * (
            decimal_jet["Z1"] / decimal_jet["Z"]
        ) ** 2
    frozen = summary["frozen_legacy_first_positive_float_signal"]
    return {
        "float_stable_H2": float_jet["H2"],
        "decimal_H2": str(+decimal_jet["H2"]),
        "summary_decimal_H2_abs_diff": str(
            abs(Decimal(str(frozen["decimal_H2_precision_110"])) - Decimal(str(+decimal_jet["H2"])))
        ),
        "chord_h_0.0005": {"central_H2": str(chord_h2), "gap": str(gap)},
        "legacy_inverse_H2_reproduced": legacy_h2,
        "legacy_author_H2": frozen["legacy_unstable_inverse_formula_H2"],
        "legacy_abs_diff": abs(legacy_h2 - frozen["legacy_unstable_inverse_formula_H2"]),
        "inverse_Z_cubed_float": (1.0 / float_jet["Z"]) ** 3,
        "inverse_Z_cubed_decimal": str(+inv_z_decimal_cubed),
        "predicted_upward_error": str(+predicted_error),
        "stable_float_sign_matches_decimal": (float_jet["H2"] > 0) == (Decimal(str(+decimal_jet["H2"])) > 0),
        "spectral_certificate": spectral_certificate(params),
    }


def main():
    summary = json.loads((ROUTE / "results" / "summary.json").read_text(encoding="utf-8"))
    params = json.loads((HERE / "anomaly_parameters.json").read_text(encoding="utf-8"))
    low_gate = low_dim_exact_gate()
    n93 = n93_stability(params, summary)
    scan = replay_scan(summary)
    ok = (
        max(Decimal(v) for v in low_gate["abs_diff"].values()) < Decimal("1e-60")
        and Decimal(n93["decimal_H2"]) < 0
        and n93["chord_h_0.0005"]["gap"].startswith("-")
        and n93["inverse_Z_cubed_float"] == 0.0
        and scan["matches_summary"]["total_evaluations"]
        and scan["matches_summary"]["positive_count"]
        and scan["matches_summary"]["global_max_identity"]
        and scan["matches_summary"]["global_max_value_abs_diff"] < 1e-12
    )
    report = {
        "status": "PASS" if ok else "FAIL",
        "python": sys.version.split()[0],
        "low_dim_exact_gate": low_gate,
        "n93_stability": n93,
        "scan_replay": scan,
        "denominator": {
            "low_dim_exact_families": 1,
            "low_dim_exact_events": 32,
            "n93_centers": 1,
            "n93_rank2_directions": 1,
            "n93_chords": 1,
            "scan_n_values": 96,
            "scan_trials_per_n": 24,
            "scan_buckets_per_trial": 2,
            "scan_evaluations": scan["total_evaluations"],
            "random_seed": 20260908,
            "failed_assertions": 0 if ok else "see status",
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
