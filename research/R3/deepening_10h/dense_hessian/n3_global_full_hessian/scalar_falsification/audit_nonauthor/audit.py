#!/usr/bin/env python3
"""
D10-U10c scalar_falsification fresh audit.

This audit does not import or call the author script.  It reads the frozen JSON
ledger/candidates, rebuilds the n=3 scalar formula independently, and
high-precision recomputes the requested points plus the Decimal boundary/path
families that can be reconstructed from the frozen script/ledger.

Important provenance note: this file is written in a separate audit directory,
but the surrounding conversation context previously authored U10c.  The output
therefore records a provenance limitation and should not be treated as a final
fresh non-author certification.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")


BASE = Path(__file__).resolve().parent
AUTHOR_DIR = BASE.parent
ATOM_NAMES = ["0", "1", "2", "3", "12", "13", "23", "123"]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def D(x: Any) -> Decimal:
    return Decimal(str(x))


def zeros(n: int, m: int) -> List[List[Decimal]]:
    return [[Decimal(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> List[List[Decimal]]:
    M = zeros(n, n)
    for i in range(n):
        M[i][i] = Decimal(1)
    return M


def matmul(A: List[List[Decimal]], B: List[List[Decimal]]) -> List[List[Decimal]]:
    n, m, p = len(A), len(B), len(B[0])
    C = zeros(n, p)
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik:
                for j in range(p):
                    C[i][j] += aik * B[k][j]
    return C


def trace(A: List[List[Decimal]]) -> Decimal:
    return sum(A[i][i] for i in range(len(A)))


def det3(M: List[List[Decimal]]) -> Decimal:
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def inverse(A: List[List[Decimal]]) -> List[List[Decimal]]:
    n = len(A)
    M = [row[:] + e for row, e in zip([r[:] for r in A], eye(n))]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular inverse")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(2 * n):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(2 * n):
                    M[i][j] -= fac * M[col][j]
    return [row[n:] for row in M]


def solve(A: List[List[Decimal]], b: List[Decimal]) -> List[Decimal]:
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular solve")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(col, n + 1):
                    M[i][j] -= fac * M[col][j]
    return [M[i][n] for i in range(n)]


def ldl_pivots(M: List[List[Decimal]]) -> List[Decimal]:
    n = len(M)
    L = zeros(n, n)
    piv = [Decimal(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Decimal(1)
    for j in range(n):
        val = M[j][j]
        for k in range(j):
            val -= L[j][k] * L[j][k] * piv[k]
        piv[j] = val
        for i in range(j + 1, n):
            val2 = M[i][j]
            for k in range(j):
                val2 -= L[i][k] * L[j][k] * piv[k]
            L[i][j] = val2 / piv[j]
    return piv


def basis() -> List[List[List[Decimal]]]:
    out = []
    for k in range(6):
        M = zeros(3, 3)
        if k == 0:
            M[0][0] = Decimal(1)
        elif k == 1:
            M[1][1] = Decimal(1)
        elif k == 2:
            M[2][2] = Decimal(1)
        elif k == 3:
            M[0][1] = M[1][0] = Decimal(1)
        elif k == 4:
            M[0][2] = M[2][0] = Decimal(1)
        elif k == 5:
            M[1][2] = M[2][1] = Decimal(1)
        out.append(M)
    return out


BASIS = basis()


def atoms_and_correct_grads(K: List[List[Decimal]]) -> Tuple[List[Decimal], List[List[Decimal]]]:
    x, y, z = K[0][0], K[1][1], K[2][2]
    a, b, c = K[0][1], K[0][2], K[1][2]
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
    gq12 = [y, x, Decimal(0), -2 * a, Decimal(0), Decimal(0)]
    gq13 = [z, Decimal(0), x, Decimal(0), -2 * b, Decimal(0)]
    gq23 = [Decimal(0), z, y, Decimal(0), Decimal(0), -2 * c]
    gr = [
        y * z - c * c,
        x * z - b * b,
        x * y - a * a,
        2 * b * c - 2 * z * a,
        2 * a * c - 2 * y * b,
        2 * a * b - 2 * x * c,
    ]
    vals = [
        1 - x - y - z + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        z - q13 - q23 + r,
        q12 - r,
        q13 - r,
        q23 - r,
        r,
    ]
    base0 = [-1, -1, -1, 0, 0, 0]
    grads = [
        [Decimal(base0[i]) + gq12[i] + gq13[i] + gq23[i] - gr[i] for i in range(6)],
        [(Decimal(1) if i == 0 else Decimal(0)) - gq12[i] - gq13[i] + gr[i] for i in range(6)],
        [(Decimal(1) if i == 1 else Decimal(0)) - gq12[i] - gq23[i] + gr[i] for i in range(6)],
        [(Decimal(1) if i == 2 else Decimal(0)) - gq13[i] - gq23[i] + gr[i] for i in range(6)],
        [gq12[i] - gr[i] for i in range(6)],
        [gq13[i] - gr[i] for i in range(6)],
        [gq23[i] - gr[i] for i in range(6)],
        gr,
    ]
    return vals, grads


def rho_decimal_correct(Kvals: Sequence[Sequence[Any]], dps: int) -> Dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = dps
        K = [[D(Kvals[i][j]) for j in range(3)] for i in range(3)]
        atoms, grads = atoms_and_correct_grads(K)
        if min(atoms) <= 0:
            return {"ok": False, "status": "nonpositive_atom"}
        mass_jet_residual = max(abs(sum(grads[s][j] for s in range(8))) for j in range(6))
        p0, p1, p2, p3, p12, p13, p23, p123 = atoms
        l12 = (p0 * p12 / (p1 * p2)).ln()
        l13 = (p0 * p13 / (p1 * p3)).ln()
        l23 = (p0 * p23 / (p2 * p3)).ln()
        Lambda = (p123 * p1 * p2 * p3 / (p0 * p12 * p13 * p23)).ln()
        N = zeros(3, 3)
        N[0][0] = -l23
        N[1][1] = -l13
        N[2][2] = -l12
        for i in range(3):
            for j in range(3):
                N[i][j] -= Lambda * K[i][j]
        detN = det3(N)
        Ninv = inverse(N)
        Fmat = zeros(6, 6)
        for s in range(8):
            for i in range(6):
                for j in range(6):
                    Fmat[i][j] += grads[s][i] * grads[s][j] / atoms[s]
        G = zeros(6, 6)
        eta = [Decimal(0) for _ in range(6)]
        for i, Ei in enumerate(BASIS):
            eta[i] = trace(matmul(Ninv, Ei))
            for j, Ej in enumerate(BASIS):
                G[i][j] = trace(matmul(matmul(matmul(Ninv, Ei), Ninv), Ej))
        A = zeros(6, 6)
        for i in range(6):
            for j in range(6):
                A[i][j] = Fmat[i][j] + detN * G[i][j]
        sol = solve(A, eta)
        quad = sum(eta[i] * sol[i] for i in range(6))
        rho = detN * quad
        IminusK = eye(3)
        for i in range(3):
            for j in range(3):
                IminusK[i][j] -= K[i][j]
        return {
            "ok": True,
            "status": "ok",
            "dps": dps,
            "rho": str(+rho),
            "one_minus_rho": str(+(Decimal(1) - rho)),
            "min_atom": str(+min(atoms)),
            "min_atom_name": ATOM_NAMES[min(range(8), key=lambda i: atoms[i])],
            "atoms": {ATOM_NAMES[i]: str(+atoms[i]) for i in range(8)},
            "Lambda": str(+Lambda),
            "detN": str(+detN),
            "K_ldl_pivots": [str(+x) for x in ldl_pivots(K)],
            "I_minus_K_ldl_pivots": [str(+x) for x in ldl_pivots(IminusK)],
            "N_ldl_pivots": [str(+x) for x in ldl_pivots(N)],
            "A_ldl_min_pivot": str(+min(ldl_pivots(A))),
            "mass_jet_max_abs_residual": str(+mass_jet_residual),
        }


def rational_Q() -> List[List[Decimal]]:
    return [
        [Decimal(1) / 3, Decimal(2) / 3, Decimal(2) / 3],
        [Decimal(2) / 3, Decimal(1) / 3, -Decimal(2) / 3],
        [Decimal(2) / 3, -Decimal(2) / 3, Decimal(1) / 3],
    ]


def K_from_rational_Q(theta: str, k: int, rates: Sequence[int], complement: bool, dps: int) -> List[List[Decimal]]:
    with localcontext() as ctx:
        ctx.prec = dps
        eps = Decimal(10) ** Decimal(-k)
        lam = [eps ** int(rates[0]), eps ** int(rates[1]), Decimal(theta)]
        Q = rational_Q()
        K = zeros(3, 3)
        for m in range(3):
            for i in range(3):
                for j in range(3):
                    K[i][j] += lam[m] * Q[i][m] * Q[j][m]
        if complement:
            I = eye(3)
            K = [[I[i][j] - K[i][j] for j in range(3)] for i in range(3)]
        return K


def decimal_boundary_grid_correct() -> List[Dict[str, Any]]:
    out = []
    rates_list = [(1, 1), (1, 2), (1, 3), (2, 3), (1, 5), (2, 5), (1, 8)]
    theta_list = ["0.1", "0.5", "0.9", "0.99"]
    k_list = [8, 16, 32, 64, 96]
    for theta in theta_list:
        for k in k_list:
            for rates in rates_list:
                dps = max(140, 2 * max(rates) * k + 100)
                for complement in [False, True]:
                    K = K_from_rational_Q(theta, k, rates, complement, dps)
                    res = rho_decimal_correct(K, dps)
                    res.update({"route": "decimal_rank_one_rate_extremes", "theta": theta, "k": k, "rates": list(rates), "complement": complement})
                    out.append(res)
    return out


def decimal_lambda0_path_grid_correct() -> List[Dict[str, Any]]:
    out = []
    diag_list = [
        (Decimal(12) / 100, Decimal(1) / 2, Decimal(88) / 100),
        (Decimal(8) / 100, Decimal(31) / 100, Decimal(79) / 100),
        (Decimal(1) / 4, Decimal(37) / 100, Decimal(62) / 100),
        (Decimal(91) / 100, Decimal(64) / 100, Decimal(21) / 100),
        (Decimal(48) / 100, Decimal(51) / 100, Decimal(55) / 100),
    ]
    weights = [
        (Decimal(1), Decimal(1)),
        (Decimal(1), -Decimal(1)),
        (Decimal(3) / 10, Decimal(1)),
        (Decimal(1), Decimal(3) / 10),
        (Decimal(1), Decimal(1) / 100),
    ]
    for did, diag in enumerate(diag_list):
        for wid, (w12, w23) in enumerate(weights):
            for k in [2, 4, 8, 16, 32, 48]:
                dps = max(180, 10 * k + 140)
                with localcontext() as ctx:
                    ctx.prec = dps
                    eps = Decimal(10) ** Decimal(-k)
                    K = zeros(3, 3)
                    for i in range(3):
                        K[i][i] = diag[i]
                    K[0][1] = K[1][0] = eps * w12
                    K[1][2] = K[2][1] = eps * w23
                    res = rho_decimal_correct(K, dps)
                    res.update({"route": "decimal_lambda0_near_disconnected_paths", "diag_id": did, "weight_id": wid, "diag": [str(x) for x in diag], "weights": [str(w12), str(w23)], "k": k})
                    out.append(res)
    return out


def find_author_decimal_bug_line(script_text: str) -> List[int]:
    lines = []
    for idx, line in enumerate(script_text.splitlines(), start=1):
        if "g0 = [-1 + gq12[i] + gq13[i] + gq23[i] - gr[i]" in line:
            lines.append(idx)
    return lines


def decdiff(a: str, b: str) -> str:
    with localcontext() as ctx:
        ctx.prec = max(80, min(300, max(len(a), len(b)) + 20))
        return str(+(Decimal(a) - Decimal(b)))


def main() -> int:
    t0 = time.time()
    ledger_path = AUTHOR_DIR / "search_ledger.json"
    cand_path = AUTHOR_DIR / "near_threshold_candidates.json"
    script_path = AUTHOR_DIR / "rho_scalar_search.py"
    verdict_path = AUTHOR_DIR / "verdict.md"
    runlog_path = AUTHOR_DIR / "run_log.md"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    candidates = json.loads(cand_path.read_text(encoding="utf-8"))
    script_text = script_path.read_text(encoding="utf-8")

    route_sum_attempted = sum(v["attempted"] for v in ledger["route_stats"].values())
    route_sum_accepted = sum(v["accepted"] for v in ledger["route_stats"].values())
    route_internal_ok = all(v["attempted"] == v["accepted"] + v["rejected"] for v in ledger["route_stats"].values())
    line_bug = find_author_decimal_bug_line(script_text)

    # Three required independent high-precision checks.
    near = candidates["near_threshold_candidates"]
    equal_author = max(
        (x for x in near if x.get("route") == "decimal_rank_one_rate_extremes" and x.get("rates") == [1, 1]),
        key=lambda x: Decimal(x["rho"]),
    )
    unequal_author = max(
        (x for x in near if x.get("route") == "decimal_rank_one_rate_extremes" and x.get("rates") and x["rates"][0] != x["rates"][1]),
        key=lambda x: Decimal(x["rho"]),
    )
    pseudo_author = candidates["top_float_decimal_rechecks"][0]

    def recompute_boundary(author_item: Dict[str, Any]) -> Dict[str, Any]:
        dps = max(int(author_item["dps"]), 220)
        K = K_from_rational_Q(author_item["theta"], int(author_item["k"]), author_item["rates"], bool(author_item["complement"]), dps)
        fresh = rho_decimal_correct(K, dps)
        return {
            "author": {k: author_item.get(k) for k in ["rho", "one_minus_rho", "min_atom", "min_atom_name", "theta", "k", "rates", "complement", "dps"]},
            "fresh": fresh,
            "rho_difference_fresh_minus_author": decdiff(fresh["rho"], author_item["rho"]),
            "min_atom_matches": fresh["min_atom"] == author_item["min_atom"],
            "min_atom_name_matches": fresh["min_atom_name"] == author_item["min_atom_name"],
            "strict_K": all(Decimal(x) > 0 for x in fresh["K_ldl_pivots"]),
            "strict_I_minus_K": all(Decimal(x) > 0 for x in fresh["I_minus_K_ldl_pivots"]),
            "N_positive": all(Decimal(x) > 0 for x in fresh["N_ldl_pivots"]),
        }

    equal_check = recompute_boundary(equal_author)
    unequal_check = recompute_boundary(unequal_author)
    pseudo_fresh = rho_decimal_correct(pseudo_author["K"], max(int(pseudo_author["dps"]), 220))
    pseudo_check = {
        "author": {k: pseudo_author.get(k) for k in ["source_route", "source_rho_float", "rho", "one_minus_rho", "source_min_atom", "source_min_atom_name", "dps"]},
        "fresh": pseudo_fresh,
        "rho_difference_fresh_minus_author": decdiff(pseudo_fresh["rho"], pseudo_author["rho"]),
        "strict_K": all(Decimal(x) > 0 for x in pseudo_fresh["K_ldl_pivots"]),
        "strict_I_minus_K": all(Decimal(x) > 0 for x in pseudo_fresh["I_minus_K_ldl_pivots"]),
        "N_positive": all(Decimal(x) > 0 for x in pseudo_fresh["N_ldl_pivots"]),
        "diagnosis": "near Lambda=0 / nearly disconnected; N has tiny pivots and ordinary float is not a gate",
    }

    boundary_grid = decimal_boundary_grid_correct()
    path_grid = decimal_lambda0_path_grid_correct()
    all_recomputed = boundary_grid + path_grid + [equal_check["fresh"], unequal_check["fresh"], pseudo_check["fresh"]]
    ok_items = [x for x in all_recomputed if x.get("ok")]
    positives = [x for x in ok_items if Decimal(x["rho"]) > 1]
    best_boundary = max((x for x in boundary_grid if x.get("ok")), key=lambda x: Decimal(x["rho"]))
    best_unequal_grid = max((x for x in boundary_grid if x.get("ok") and x.get("rates")[0] != x.get("rates")[1]), key=lambda x: Decimal(x["rho"]))
    best_path = max((x for x in path_grid if x.get("ok")), key=lambda x: Decimal(x["rho"]))

    results = {
        "status": "CRITICAL_GAPS",
        "provenance_limitation": "same conversation context previously authored U10c; this cannot be final non-author certification",
        "finite_scout_only": True,
        "input_hashes": {
            "rho_scalar_search.py": sha256_file(script_path),
            "search_ledger.json": sha256_file(ledger_path),
            "near_threshold_candidates.json": sha256_file(cand_path),
            "run_log.md": sha256_file(runlog_path),
            "verdict.md": sha256_file(verdict_path),
        },
        "ledger_denominator_checks": {
            "attempted_float_total": ledger["attempted_float_total"],
            "accepted_float_total": ledger["accepted_float_total"],
            "route_sum_attempted": route_sum_attempted,
            "route_sum_accepted": route_sum_accepted,
            "route_internal_attempted_equals_accepted_plus_rejected": route_internal_ok,
            "route_counts_match_totals": route_sum_attempted == ledger["attempted_float_total"] and route_sum_accepted == ledger["accepted_float_total"],
            "route_stats": ledger["route_stats"],
            "small_atom_hit_counts": ledger["small_atom_hit_counts"],
            "all_8_atom_hit_counts_positive": all(ledger["small_atom_hit_counts"].get(name, 0) > 0 for name in ATOM_NAMES),
            "author_decimal_positive_count": ledger["decimal_positive_count"],
            "author_positive_candidate_list_len": len(candidates["positive_candidates_rho_gt_1"]),
        },
        "author_decimal_formula_bug": {
            "found": bool(line_bug),
            "lines": line_bug,
            "description": "Decimal atoms_and_grads_dec uses g0 = [-1 + ...] for all six coordinates; off-diagonal p0 jets must have zero contribution from 1-x-y-z.",
            "impact": "author Decimal rho rechecks and near-threshold Decimal candidates are not reliable as written",
        },
        "required_three_point_rechecks": {
            "best_equal_rate": equal_check,
            "best_unequal_rate": unequal_check,
            "float_pseudo_near_threshold": pseudo_check,
        },
        "recomputed_decimal_grids": {
            "boundary_grid_count": len(boundary_grid),
            "lambda0_path_grid_count": len(path_grid),
            "credible_rho_gt_1_count_in_recomputed_grids_and_required_points": len(positives),
            "best_boundary_correct": best_boundary,
            "best_unequal_correct": best_unequal_grid,
            "best_lambda0_path_correct": best_path,
        },
        "elapsed_seconds": time.time() - t0,
    }

    (BASE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    run_log = [
        "# D10-U10c scalar_falsification audit run log",
        "",
        f"Command: `{Path(sys.executable)} {Path(__file__).name}`",
        "Exit code: `0`",
        f"Elapsed seconds: `{results['elapsed_seconds']:.6f}`",
        "Author script was not imported or called.",
        "",
        f"Ledger route counts match totals: `{results['ledger_denominator_checks']['route_counts_match_totals']}`",
        f"All eight small-atom buckets positive: `{results['ledger_denominator_checks']['all_8_atom_hit_counts_positive']}`",
        f"Author Decimal bug found: `{results['author_decimal_formula_bug']['found']}` at lines `{line_bug}`",
        f"Recomputed Decimal boundary grid count: `{len(boundary_grid)}`",
        f"Recomputed Decimal Lambda≈0 path grid count: `{len(path_grid)}`",
        f"Credible rho>1 count in recomputed grids/required points: `{len(positives)}`",
    ]
    (BASE / "run_log.md").write_text("\n".join(run_log) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": results["status"],
        "bug_lines": line_bug,
        "route_counts_match": results["ledger_denominator_checks"]["route_counts_match_totals"],
        "credible_rho_gt_1": len(positives),
        "best_correct_rho": best_boundary["rho"],
        "elapsed_seconds": results["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
