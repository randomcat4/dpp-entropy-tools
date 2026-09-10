#!/usr/bin/env python3
"""Independent exact finite/source checker for PR95 at frozen head 54d9803.

This implementation was written from RESULT.md and the immutable PR58 source.
It does not import, read, or execute the author checker.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import sys
import time
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as Q
from pathlib import Path


AUTHOR_HEAD = "54d9803b29f73669b9028e3519d17493e1b81be3"
SOURCE_REF = "89aa874c24dd5a3ea98f8474826392560b1d0397"
SOURCE_PATH = "research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md"
EPS = Q(1, 10**6)


class CheckFailure(RuntimeError):
    pass


CHECKS: list[dict[str, object]] = []


def q(x: str | int | Q) -> Q:
    return x if isinstance(x, Q) else Q(str(x))


def fs(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def require(name: str, condition: bool, **data: object) -> None:
    record = {"sequence": len(CHECKS) + 1, "name": name, "passed": bool(condition)}
    if data:
        record["data"] = data
    CHECKS.append(record)
    if not condition:
        raise CheckFailure(f"{name}: {data}")


def poly_trim(p: list[Q]) -> list[Q]:
    out = list(p)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: list[Q], b: list[Q], scale: Q = Q(1)) -> list[Q]:
    n = max(len(a), len(b))
    out = [Q(0) for _ in range(n)]
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + scale * (b[i] if i < len(b) else 0)
    return poly_trim(out)


def poly_mul(a: list[Q], b: list[Q]) -> list[Q]:
    out = [Q(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return poly_trim(out)


def poly_pad(p: list[Q], n: int) -> list[Q]:
    return p + [Q(0)] * (n - len(p))


def poly_eval(p: list[Q], x: Q) -> Q:
    total = Q(0)
    for coefficient in reversed(p):
        total = total * x + coefficient
    return total


def permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inversions % 2 else 1


def det_poly(matrix: list[list[list[Q]]]) -> list[Q]:
    n = len(matrix)
    if n == 0:
        return [Q(1)]
    total = [Q(0)]
    for perm in itertools.permutations(range(n)):
        term = [Q(permutation_sign(perm))]
        for i, j in enumerate(perm):
            term = poly_mul(term, matrix[i][j])
        total = poly_add(total, term)
    return poly_trim(total)


def det_const(matrix: list[list[Q]]) -> Q:
    return det_poly([[[entry] for entry in row] for row in matrix])[0]


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    n = len(matrix)
    aug = [list(row) + [Q(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None:
            raise CheckFailure("singular rational matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            scale = aug[r][col]
            if scale:
                aug[r] = [x - scale * y for x, y in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[Q]]) -> list[list[Q]]:
    return [list(row) for row in zip(*a)]


def complete_marginal(block: list[list[Q]], event_mask: int) -> Q:
    n = len(block)
    total = Q(0)
    for sup in range(1 << n):
        if sup & event_mask != event_mask:
            continue
        idx = [i for i in range(n) if sup >> i & 1]
        minor = [[block[i][j] for j in idx] for i in idx]
        total += (-1) ** (sup.bit_count() - event_mask.bit_count()) * det_const(minor)
    return total


def parse_source_matrices(text: str) -> dict[str, list[list[Q]]]:
    section = text.split("## 3.", 1)[1].split("## 4.", 1)[0]
    shapes = {"A": (3, 3), "C": (3, 3), "U": (3, 2), "V": (3, 2)}
    parsed: dict[str, list[list[Q]]] = {}
    for name, (rows, cols) in shapes.items():
        match = re.search(rf"{name}\s*=\s*\\begin\{{pmatrix\}}(.*?)\\end\{{pmatrix\}}", section, re.S)
        if match is None:
            raise CheckFailure(f"source matrix {name} not found")
        tokens = re.findall(r"[-+]?\d+(?:/\d+)?", match.group(1))
        require(f"source_{name}_entry_count", len(tokens) == rows * cols, found=len(tokens), expected=rows * cols)
        values = [q(token) for token in tokens]
        parsed[name] = [values[r * cols : (r + 1) * cols] for r in range(rows)]
    return parsed


def shifted_complete_polynomial(kpoly: list[list[list[Q]]], event: int) -> list[Q]:
    matrix = [[list(kpoly[i][j]) for j in range(6)] for i in range(6)]
    for i in range(6):
        if not (event >> i) & 1:
            matrix[i][i] = poly_add(matrix[i][i], [Q(-1)])
    sign = Q((-1) ** (6 - event.bit_count()))
    return [sign * x for x in det_poly(matrix)]


def schur_coefficients(
    a_block: list[list[Q]], c_block: list[list[Q]], u: list[list[Q]], v: list[list[Q]], s_mask: int, t_mask: int
) -> tuple[Q, Q]:
    ashift = [list(row) for row in a_block]
    cshift = [list(row) for row in c_block]
    for i in range(3):
        if not (s_mask >> i) & 1:
            ashift[i][i] -= 1
        if not (t_mask >> i) & 1:
            cshift[i][i] -= 1
    ga = matmul(matmul(transpose(u), inverse(ashift)), u)
    gc = matmul(matmul(transpose(v), inverse(cshift)), v)
    product = matmul(ga, gc)
    a = product[0][0] + product[1][1]
    b = det_const(ga) * det_const(gc)
    return a, b


def quadratic_extreme(coeff: list[Q], lo: Q, hi: Q, want_min: bool) -> tuple[Q, Q, str]:
    candidates: list[tuple[Q, Q, str]] = [(poly_eval(coeff, lo), lo, "left"), (poly_eval(coeff, hi), hi, "right")]
    padded = poly_pad(coeff, 3)
    if padded[2] != 0:
        vertex = -padded[1] / (2 * padded[2])
        if lo <= vertex <= hi:
            candidates.append((poly_eval(coeff, vertex), vertex, "vertex"))
    key = (lambda item: item[0])
    return (min(candidates, key=key) if want_min else max(candidates, key=key))


def decimal_bounds(value: Q, digits: int = 30) -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = digits
        ctx.rounding = ROUND_FLOOR
        lower = Decimal(value.numerator) / Decimal(value.denominator)
        ctx.rounding = ROUND_CEILING
        upper = Decimal(value.numerator) / Decimal(value.denominator)
    return {"lower": format(lower, "f"), "upper": format(upper, "f")}


def exact_value(value: Q) -> dict[str, object]:
    return {"fraction": fs(value), "decimal_outward": decimal_bounds(value)}


def leading_minors(matrix: list[list[Q]]) -> list[Q]:
    return [det_const([row[:k] for row in matrix[:k]]) for k in range(1, len(matrix) + 1)]


def log_unit_interval_bounds(x: Q, terms: int = 40) -> tuple[Q, Q]:
    require("log_unit_domain", Q(1) <= x <= Q(2), x=fs(x))
    z = (x - 1) / (x + 1)
    lower = Q(0)
    for k in range(terms):
        lower += 2 * z ** (2 * k + 1) / (2 * k + 1)
    remainder = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, lower + remainder


def log_bounds(x: Q, terms: int = 40) -> tuple[Q, Q]:
    require("log_positive_argument", x > 0, x=fs(x))
    y = x
    power = 0
    while y >= 2:
        y /= 2
        power += 1
    while y < 1:
        y *= 2
        power -= 1
    ly_lo, ly_hi = log_unit_interval_bounds(y, terms)
    l2_lo, l2_hi = log_unit_interval_bounds(Q(2), terms)
    if power >= 0:
        return ly_lo + power * l2_lo, ly_hi + power * l2_hi
    return ly_lo + power * l2_hi, ly_hi + power * l2_lo


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    started = time.time()
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    final: dict[str, object] = {"status": "RUNNING", "author_head": AUTHOR_HEAD, "source_ref": SOURCE_REF}

    try:
        fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        require("fixture_source_ref", fixture["source_ref"] == SOURCE_REF, actual=fixture["source_ref"])
        require("fixture_source_path", fixture["source_path"] == SOURCE_PATH, actual=fixture["source_path"])
        matrices = {name: [[q(x) for x in row] for row in fixture[name]] for name in ("A", "C", "U", "V")}
        source_matrices = parse_source_matrices(Path(args.source).read_text(encoding="utf-8"))
        entry_total = 0
        for name in ("A", "C", "U", "V"):
            for i, row in enumerate(matrices[name]):
                for j, value in enumerate(row):
                    entry_total += 1
                    require(f"source_binding_{name}_{i}_{j}", value == source_matrices[name][i][j], value=fs(value))
        require("source_binding_total_30", entry_total == 30, count=entry_total)

        a_block, c_block, u, v = (matrices[name] for name in ("A", "C", "U", "V"))
        b_block = matmul(u, transpose(v))
        spectral_rank: dict[str, object] = {}
        for name, block in (("A", a_block), ("C", c_block)):
            above = [list(row) for row in block]
            below = [[-entry for entry in row] for row in block]
            for i in range(3):
                above[i][i] -= Q(3, 10)
                below[i][i] += Q(7, 10)
            above_minors = leading_minors(above)
            below_minors = leading_minors(below)
            require(f"{name}_spectrum_above_3_10", all(value > 0 for value in above_minors), minors=[fs(x) for x in above_minors])
            require(f"{name}_spectrum_below_7_10", all(value > 0 for value in below_minors), minors=[fs(x) for x in below_minors])
            spectral_rank[f"{name}_minus_3_10I_leading_minors"] = [fs(x) for x in above_minors]
            spectral_rank[f"7_10I_minus_{name}_leading_minors"] = [fs(x) for x in below_minors]
        u_frob2 = sum(entry * entry for row in u for entry in row)
        v_frob2 = sum(entry * entry for row in v for entry in row)
        require("U_frobenius_lt_9_10", u_frob2 < Q(81, 100), exact=fs(u_frob2))
        require("V_frobenius_lt_19_10", v_frob2 < Q(361, 100), exact=fs(v_frob2))
        u_top_minor = det_const([row[:2] for row in u[:2]])
        v_top_minor = det_const([row[:2] for row in v[:2]])
        eta = Q(1, 10**12)
        rank_margin = 4 * eta + 2 * eta * eta
        require("U_top_minor_box_persistence", abs(u_top_minor) > rank_margin, exact=fs(u_top_minor), margin=fs(rank_margin))
        require("V_top_minor_box_persistence", abs(v_top_minor) > rank_margin, exact=fs(v_top_minor), margin=fs(rank_margin))
        b_min_abs = min(abs(entry) for row in b_block for entry in row)
        require("B_all_entries_box_persistence", b_min_abs > 9 * eta, exact=fs(b_min_abs), margin=fs(9 * eta))
        b_minors = []
        for rows in itertools.combinations(range(3), 2):
            for cols in itertools.combinations(range(3), 2):
                minor = det_const([[b_block[i][j] for j in cols] for i in rows])
                b_minors.append((rows, cols, minor))
        require("B_rank_two", any(minor != 0 for _, _, minor in b_minors))
        spectral_rank.update({
            "U_frobenius_squared": fs(u_frob2), "V_frobenius_squared": fs(v_frob2),
            "U_top_minor": fs(u_top_minor), "V_top_minor": fs(v_top_minor),
            "B_min_abs_entry": fs(b_min_abs),
            "B_two_by_two_minors": [{"rows": list(rows), "cols": list(cols), "value": fs(minor)} for rows, cols, minor in b_minors],
        })
        kpoly = [[[Q(0)] for _ in range(6)] for _ in range(6)]
        for i in range(3):
            for j in range(3):
                kpoly[i][j] = [a_block[i][j]]
                kpoly[i + 3][j + 3] = [c_block[i][j]]
                kpoly[i][j + 3] = [Q(0), b_block[i][j]]
                kpoly[j + 3][i] = [Q(0), b_block[i][j]]

        principal: dict[int, list[Q]] = {}
        for mask in range(64):
            idx = [i for i in range(6) if mask >> i & 1]
            principal[mask] = det_poly([[kpoly[i][j] for j in idx] for i in idx])

        p_a = [complete_marginal(a_block, mask) for mask in range(8)]
        p_c = [complete_marginal(c_block, mask) for mask in range(8)]
        for mask, value in enumerate(p_a):
            require(f"marginal_A_positive_{mask}", value > 0, value=fs(value))
        for mask, value in enumerate(p_c):
            require(f"marginal_C_positive_{mask}", value > 0, value=fs(value))
        require("marginal_A_total", sum(p_a) == 1, total=fs(sum(p_a)))
        require("marginal_C_total", sum(p_c) == 1, total=fs(sum(p_c)))

        events: list[dict[str, object]] = []
        for event in range(64):
            mobius = [Q(0)]
            for sup in range(64):
                if sup & event == event:
                    sign = Q((-1) ** (sup.bit_count() - event.bit_count()))
                    mobius = poly_add(mobius, principal[sup], sign)
            mobius = poly_pad(mobius, 7)
            shifted = poly_pad(shifted_complete_polynomial(kpoly, event), 7)
            require(f"mobius_shifted_identity_{event}", mobius == shifted)
            require(f"odd_and_rank2_degrees_{event}", all(mobius[d] == 0 for d in (1, 3, 5, 6)))
            s_mask, t_mask = event & 7, (event >> 3) & 7
            mu = p_a[s_mask] * p_c[t_mask]
            require(f"event_mu_{event}", mobius[0] == mu and mu > 0, mu=fs(mu))
            a = -mobius[2] / mu
            b = mobius[4] / mu
            schur_a, schur_b = schur_coefficients(a_block, c_block, u, v, s_mask, t_mask)
            require(f"schur_a_{event}", a == schur_a, mobius=fs(a), schur=fs(schur_a))
            require(f"schur_b_{event}", b == schur_b, mobius=fs(b), schur=fs(schur_b))
            events.append({"event": event, "S": s_mask, "T": t_mask, "mu": mu, "a": a, "b": b, "t_coeff": mobius})

        require("global_cancel_a", sum(e["mu"] * e["a"] for e in events) == 0)  # type: ignore[operator]
        require("global_cancel_b", sum(e["mu"] * e["b"] for e in events) == 0)  # type: ignore[operator]
        for s_mask in range(8):
            group = [e for e in events if e["S"] == s_mask]
            require(f"conditional_T_cancel_a_{s_mask}", sum(e["mu"] * e["a"] for e in group) == 0)  # type: ignore[operator]
            require(f"conditional_T_cancel_b_{s_mask}", sum(e["mu"] * e["b"] for e in group) == 0)  # type: ignore[operator]
        for t_mask in range(8):
            group = [e for e in events if e["T"] == t_mask]
            require(f"conditional_S_cancel_a_{t_mask}", sum(e["mu"] * e["a"] for e in group) == 0)  # type: ignore[operator]
            require(f"conditional_S_cancel_b_{t_mask}", sum(e["mu"] * e["b"] for e in group) == 0)  # type: ignore[operator]

        with (output_dir / "complete_event_coefficients.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["event", "S", "T", "mu", "a", "b", "p_t0", "p_t2", "p_t4", "p_t6"])
            for e in events:
                coeff = e["t_coeff"]  # type: ignore[assignment]
                writer.writerow([e["event"], e["S"], e["T"], fs(e["mu"]), fs(e["a"]), fs(e["b"]), fs(coeff[0]), fs(coeff[2]), fs(coeff[4]), fs(coeff[6])])  # type: ignore[index,arg-type]

        rows = [
            {
                "name": "J1_all64",
                "lo": Q(0), "hi": Q(9, 10), "exclude": None,
                "q_lo": Q(1, 30), "q_hi": Q(3), "V": Q(109, 200), "Z": Q(109, 200), "N": Q(29, 250),
                "lambda_lo": Q(1, 2), "lambda_hi": Q(18, 5), "rhs_gate": Q(1, 2), "rhs_claim": Q(8287, 15000),
            },
            {
                "name": "J2_all64",
                "lo": Q(9, 10), "hi": Q(99, 100), "exclude": None,
                "q_lo": Q(1, 400), "q_hi": Q(31, 10), "V": Q(83, 100), "Z": Q(49, 50), "N": Q(27, 200),
                "lambda_lo": Q(1, 2), "lambda_hi": Q(61, 10), "rhs_gate": Q(1, 2), "rhs_claim": Q(4177, 7750),
            },
            {
                "name": "J3_other63",
                "lo": Q(99, 100), "hi": Q(1), "exclude": 63,
                "q_lo": Q(1, 50), "q_hi": Q(31, 10), "V": Q(89, 100), "Z": Q(109, 100), "N": Q(14, 125),
                "lambda_lo": Q(1, 2), "lambda_hi": Q(41, 10), "rhs_gate": Q(7, 5), "rhs_claim": Q(110979, 77500),
            },
        ]
        interval_output: dict[str, object] = {}
        for row in rows:
            group = [e for e in events if e["event"] != row["exclude"]]
            lo, hi = row["lo"], row["hi"]
            q_min_candidates: list[tuple[Q, Q, str, int]] = []
            q_max_candidates: list[tuple[Q, Q, str, int]] = []
            for e in group:
                coeff = [Q(1), -e["a"], e["b"]]  # type: ignore[list-item,operator]
                mn = quadratic_extreme(coeff, lo, hi, True)
                mx = quadratic_extreme(coeff, lo, hi, False)
                q_min_candidates.append((*mn, int(e["event"])))
                q_max_candidates.append((*mx, int(e["event"])))
            qmin = min(q_min_candidates, key=lambda item: item[0])
            qmax = max(q_max_candidates, key=lambda item: item[0])
            ma = sum(e["mu"] * e["a"] * e["a"] for e in group)  # type: ignore[operator]
            mab = sum(e["mu"] * e["a"] * e["b"] for e in group)  # type: ignore[operator]
            mb = sum(e["mu"] * e["b"] * e["b"] for e in group)  # type: ignore[operator]
            vmin = quadratic_extreme([ma, -4 * mab, 4 * mb], lo, hi, True)
            zmin = quadratic_extreme([ma, -7 * mab, 6 * mb], lo, hi, True)
            n_total = Q(0)
            n_terms: list[dict[str, str]] = []
            for e in group:
                neg_z = [-e["a"] * e["a"], 7 * e["a"] * e["b"], -6 * e["b"] * e["b"]]  # type: ignore[list-item,operator]
                maximum = quadratic_extreme(neg_z, lo, hi, False)
                positive = max(Q(0), maximum[0])
                weighted = e["mu"] * positive  # type: ignore[operator]
                n_total += weighted
                if weighted:
                    n_terms.append({"event": str(e["event"]), "arg": fs(maximum[1]), "weighted": fs(weighted)})

            require(f"{row['name']}_q_lower_robust", qmin[0] - 2 * EPS > row["q_lo"], exact=fs(qmin[0]))
            require(f"{row['name']}_q_upper_robust", qmax[0] + 2 * EPS < row["q_hi"], exact=fs(qmax[0]))
            require(f"{row['name']}_V_robust", vmin[0] - 280 * EPS > row["V"], exact=fs(vmin[0]))
            require(f"{row['name']}_Z_robust", zmin[0] - 421 * EPS > row["Z"], exact=fs(zmin[0]))
            require(f"{row['name']}_N_robust", n_total + 421 * EPS < row["N"], exact=fs(n_total))
            rhs = 4 * row["V"] / row["q_hi"] + 2 * row["lambda_lo"] * row["Z"] - 2 * (row["lambda_hi"] - row["lambda_lo"]) * row["N"]
            require(f"{row['name']}_rhs_literal", rhs == row["rhs_claim"], exact=fs(rhs), claim=fs(row["rhs_claim"]))
            require(f"{row['name']}_rhs_gate", rhs > row["rhs_gate"], exact=fs(rhs), gate=fs(row["rhs_gate"]))
            interval_output[str(row["name"])] = {
                "interval": [fs(lo), fs(hi)], "retained_events": len(group),
                "q_min": {**exact_value(qmin[0]), "arg": fs(qmin[1]), "kind": qmin[2], "event": qmin[3]},
                "q_max": {**exact_value(qmax[0]), "arg": fs(qmax[1]), "kind": qmax[2], "event": qmax[3]},
                "V_min": {**exact_value(vmin[0]), "arg": fs(vmin[1]), "kind": vmin[2]},
                "Z_min": {**exact_value(zmin[0]), "arg": fs(zmin[1]), "kind": zmin[2]},
                "N_sum_of_eventwise_maxima": exact_value(n_total), "N_nonzero_terms": n_terms,
                "robust_table": {key: fs(row[key]) for key in ("q_lo", "q_hi", "V", "Z", "N", "lambda_lo", "lambda_hi")},
                "rhs": exact_value(rhs), "rhs_gate": fs(row["rhs_gate"]),
            }

        comparisons = [
            ("log_3_gt_1", Q(3), ">", Q(1)),
            ("log_30_lt_87_25", Q(30), "<", Q(87, 25)),
            ("log_31_10_gt_21_20", Q(31, 10), ">", Q(21, 20)),
            ("log_400_lt_6", Q(400), "<", Q(6)),
            ("log_50_lt_4", Q(50), "<", Q(4)),
            ("log_300_lt_6", Q(300), "<", Q(6)),
        ]
        log_output: dict[str, object] = {}
        for name, argument, direction, bound in comparisons:
            lower, upper = log_bounds(argument, 40)
            passed = lower > bound if direction == ">" else upper < bound
            require(name, passed, lower=fs(lower), upper=fs(upper), bound=fs(bound))
            log_output[name] = {"argument": fs(argument), "direction": direction, "bound": fs(bound), "lower": fs(lower), "upper": fs(upper)}

        rare = events[63]
        ae, be = rare["a"], rare["b"]  # type: ignore[assignment]
        rare_lo, rare_hi = Q(99, 100), Q(1)
        v_min = min(ae - 2 * rare_lo * be, ae - 2 * rare_hi * be)
        z_coeff = [ae * ae, -7 * ae * be, 6 * be * be]
        z_min = quadratic_extreme(z_coeff, rare_lo, rare_hi, True)[0]
        z_max = quadratic_extreme(z_coeff, rare_lo, rare_hi, False)[0]
        abs_z_max = max(abs(z_min), abs(z_max))
        q_99 = 1 - ae * rare_lo + be * rare_lo * rare_lo
        q_1 = 1 - ae + be
        require("rare_b_robust", be - EPS > 0, exact=fs(be))
        require("rare_v_robust", v_min - 3 * EPS > Q(1, 4), exact=fs(v_min))
        require("rare_abs_z_robust", abs_z_max + 37 * EPS < 3, exact=fs(abs_z_max))
        require("rare_q_99_upper_robust", q_99 + 2 * EPS < Q(1, 300), exact=fs(q_99))
        require("rare_q_1_negative_robust", q_1 + 2 * EPS < 0, exact=fs(q_1))
        require("rare_tail_constant", Q(1, 4) - Q(36, 299) == Q(155, 1196) > 0)

        a_star = Q(4181050254735181419359, 2416512579905515000000)
        b_star = Q(4847471688450288382004871, 6638770823916250000000000)
        require("rare_a_literal", ae == a_star, exact=fs(ae))
        require("rare_b_literal", be == b_star, exact=fs(be))
        s_lo = Q(999911107034345070, 10**18)
        s_hi = Q(999911107034345071, 10**18)
        t_lo = Q(999955552529383713, 10**18)
        t_hi = Q(999955552529383714, 10**18)
        qpoly_rare = [Q(1), -ae, be]
        require("root_s_lower_sign", poly_eval(qpoly_rare, s_lo) > 0, value=fs(poly_eval(qpoly_rare, s_lo)))
        require("root_s_upper_sign", poly_eval(qpoly_rare, s_hi) < 0, value=fs(poly_eval(qpoly_rare, s_hi)))
        require("root_t_lower_sign", poly_eval(qpoly_rare, t_lo * t_lo) > 0, value=fs(poly_eval(qpoly_rare, t_lo * t_lo)))
        require("root_t_upper_sign", poly_eval(qpoly_rare, t_hi * t_hi) < 0, value=fs(poly_eval(qpoly_rare, t_hi * t_hi)))
        require("root_simple_decreasing_segment", v_min > 0, v_min=fs(v_min))

        rare_output = {
            "event": 63, "mu": exact_value(rare["mu"]), "a": exact_value(ae), "b": exact_value(be),
            "v_min_99_1": exact_value(v_min), "abs_z_max_99_1": exact_value(abs_z_max),
            "q_99": exact_value(q_99), "q_1": exact_value(q_1),
            "s_root_bracket": [fs(s_lo), fs(s_hi)], "t_root_bracket": [fs(t_lo), fs(t_hi)],
            "tail_lower_constant": fs(Q(155, 1196)),
        }

        evidence = {
            "status": "MACHINE_PASS",
            "scope": "frozen PR95 finite/source reconstruction only; not mathematical review, entropy rate, or novelty",
            "author_head": AUTHOR_HEAD, "source_ref": SOURCE_REF, "source_path": SOURCE_PATH,
            "source_entries_bound": entry_total, "complete_events": len(events),
            "spectral_rank": spectral_rank, "intervals": interval_output, "logs": log_output, "rare_endpoint": rare_output,
            "check_count": len(CHECKS), "elapsed_seconds": time.time() - started,
        }
        (output_dir / "rational_certificate.json").write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
        (output_dir / "checks.jsonl").write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in CHECKS), encoding="utf-8")
        final = {"status": "MACHINE_PASS", "check_count": len(CHECKS), "elapsed_seconds": time.time() - started}
        print(json.dumps(final, sort_keys=True))
        return 0
    except CheckFailure as exc:
        final = {"status": "STOPPED_FIRST_EXACT_MISMATCH", "error": str(exc), "check_count": len(CHECKS), "elapsed_seconds": time.time() - started}
        (output_dir / "checks.jsonl").write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in CHECKS), encoding="utf-8")
        print(json.dumps(final, sort_keys=True))
        return 20
    except Exception as exc:
        final = {"status": "INFRASTRUCTURE_FAILURE", "error": repr(exc), "check_count": len(CHECKS), "elapsed_seconds": time.time() - started}
        print(json.dumps(final, sort_keys=True))
        return 1
    finally:
        (output_dir / "final.json").write_text(json.dumps(final, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
