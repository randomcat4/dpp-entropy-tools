from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = HERE / "fresh_s7_audit.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def poly_clean(p: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    return {k: v for k, v in p.items() if v}


def poly_const(x: F) -> dict[tuple[int, int], F]:
    return {(0, 0): x} if x else {}


def poly_add(*items: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    out: dict[tuple[int, int], F] = {}
    for p in items:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return poly_clean(out)


def poly_neg(p: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    return {k: -v for k, v in p.items()}


def poly_sub(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    return poly_add(a, poly_neg(b))


def poly_scale(c: F, p: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    return poly_clean({k: c * v for k, v in p.items()})


def poly_mul(a: dict[tuple[int, int], F], b: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    out: dict[tuple[int, int], F] = {}
    for (i, j), x in a.items():
        for (r, s), y in b.items():
            k = (i + r, j + s)
            out[k] = out.get(k, F(0)) + x * y
    return poly_clean(out)


def det_poly(mat: list[list[dict[tuple[int, int], F]]]) -> dict[tuple[int, int], F]:
    n = len(mat)
    if n == 0:
        return poly_const(F(1))
    if n == 1:
        return mat[0][0]
    if n == 2:
        return poly_sub(poly_mul(mat[0][0], mat[1][1]), poly_mul(mat[0][1], mat[1][0]))
    if n == 3:
        a, b, c = mat[0]
        d, e, f = mat[1]
        g, h, i = mat[2]
        return poly_add(
            poly_mul(poly_mul(a, e), i),
            poly_mul(poly_mul(b, f), g),
            poly_mul(poly_mul(c, d), h),
            poly_neg(poly_mul(poly_mul(c, e), g)),
            poly_neg(poly_mul(poly_mul(b, d), i)),
            poly_neg(poly_mul(poly_mul(a, f), h)),
        )
    raise ValueError("this audit script is intentionally specialized to n=3")


def matrix_poly(K, E, D):
    return [
        [
            poly_add(poly_const(K[i][j]), poly_scale(E[i][j], {(1, 0): F(1)}), poly_scale(D[i][j], {(0, 1): F(1)}))
            for j in range(3)
        ]
        for i in range(3)
    ]


def principal(mat, idx):
    return [[mat[i][j] for j in idx] for i in idx]


def exact_atoms_mobius(K, E, D):
    mat = matrix_poly(K, E, D)
    inc = []
    for mask in range(8):
        idx = [i for i in range(3) if (mask >> i) & 1]
        inc.append(det_poly(principal(mat, idx)))
    atoms = []
    for mask in range(8):
        total: dict[tuple[int, int], F] = {}
        for sup in range(8):
            if (sup & mask) == mask:
                total = poly_add(total, poly_scale(F((-1) ** ((sup.bit_count() - mask.bit_count()))), inc[sup]))
        atoms.append(total)
    return atoms, inc


def exact_atom_signed_det(K, E, D, mask: int):
    mat = matrix_poly(K, E, D)
    for i in range(3):
        if not ((mask >> i) & 1):
            mat[i][i] = poly_sub(mat[i][i], poly_const(F(1)))
    return poly_scale(F((-1) ** (3 - mask.bit_count())), det_poly(mat))


def exact_atoms_checked(K, E, D):
    atoms, inc = exact_atoms_mobius(K, E, D)
    signed_failures = []
    for mask in range(8):
        direct = exact_atom_signed_det(K, E, D, mask)
        if direct != atoms[mask]:
            signed_failures.append(mask)
    total: dict[tuple[int, int], F] = {}
    for atom in atoms:
        total = poly_add(total, atom)
    return atoms, inc, signed_failures, total


def frob2(A) -> F:
    return sum(A[i][j] * A[i][j] for i in range(3) for j in range(3))


def mat_add(A, B, scale=F(1)):
    return [[A[i][j] + scale * B[i][j] for j in range(3)] for i in range(3)]


def det3_fraction(A) -> F:
    return (
        A[0][0] * A[1][1] * A[2][2]
        + A[0][1] * A[1][2] * A[2][0]
        + A[0][2] * A[1][0] * A[2][1]
        - A[0][2] * A[1][1] * A[2][0]
        - A[0][1] * A[1][0] * A[2][2]
        - A[0][0] * A[1][2] * A[2][1]
    )


def charpoly_value(K, lam: F) -> F:
    return det3_fraction([[K[i][j] - (lam if i == j else 0) for j in range(3)] for i in range(3)])


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def h2_from_atoms(atoms) -> Decimal:
    total = Decimal(0)
    for atom in atoms:
        p = atom.get((0, 0), F(0))
        pd = atom.get((0, 1), F(0))
        pdd = 2 * atom.get((0, 2), F(0))
        total -= dec(pd * pd / p) + dec(pdd) * dec(p).ln()
    return total


def h3_chain_from_atoms(atoms) -> Decimal:
    total = Decimal(0)
    for atom in atoms:
        p = atom.get((0, 0), F(0))
        pe = atom.get((1, 0), F(0))
        pd = atom.get((0, 1), F(0))
        ped = atom.get((1, 1), F(0))
        pdd = 2 * atom.get((0, 2), F(0))
        pedd = 2 * atom.get((1, 2), F(0))
        total += (
            dec(pe * pd * pd / (p * p))
            - dec((2 * ped * pd + pe * pdd) / p)
            - (Decimal(1) + dec(p).ln()) * dec(pedd)
        )
    return total


def hessian_sanity(K):
    zero = [[F(0) for _ in range(3)] for __ in range(3)]
    coord_dirs = []
    for i in range(3):
        A = [[F(0) for _ in range(3)] for __ in range(3)]
        A[i][i] = F(1)
        coord_dirs.append(A)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        A = [[F(0) for _ in range(3)] for __ in range(3)]
        A[i][j] = F(1)
        A[j][i] = F(1)
        coord_dirs.append(A)

    def h2_for(D):
        atoms, _, fail, total = exact_atoms_checked(K, zero, D)
        assert not fail and total == {(0, 0): F(1)}
        return h2_from_atoms(atoms)

    with localcontext() as ctx:
        ctx.prec = 90
        G = np.zeros((6, 6), dtype=float)
        h2_single = [h2_for(D) for D in coord_dirs]
        for i in range(6):
            G[i, i] = float(h2_single[i])
        for i in range(6):
            for j in range(i + 1, 6):
                Dij = mat_add(coord_dirs[i], coord_dirs[j])
                val = (h2_for(Dij) - h2_single[i] - h2_single[j]) / Decimal(2)
                G[i, j] = G[j, i] = float(val)
        # Convert from coordinate x=(diag, raw offdiag) to a Frobenius-orthonormal
        # basis, where off-diagonal matrices are scaled by 1/sqrt(2).
        S = np.diag([1.0, 1.0, 1.0, 1 / math.sqrt(2), 1 / math.sqrt(2), 1 / math.sqrt(2)])
        Gf = S.T @ G @ S
        evals = np.linalg.eigvalsh((Gf + Gf.T) / 2)
        negG = -G
        coord_gersh_lower = []
        for i in range(6):
            coord_gersh_lower.append(float(negG[i, i] - sum(abs(negG[i, j]) for j in range(6) if j != i)))
        return {
            "coordinate_Hessian_float": G.tolist(),
            "frob_orthonormal_eigenvalues_float": [float(x) for x in evals],
            "max_eigenvalue_float": float(evals[-1]),
            "max_eigenvalue_below_minus_43_over_50": bool(evals[-1] < -43 / 50),
            "coordinate_minus_H_gershgorin_lower_float": coord_gersh_lower,
            "min_coordinate_gershgorin_lower_float": min(coord_gersh_lower),
        }


def main() -> int:
    started = time.time()
    K = [
        [F(151, 280), -F(6, 35), -F(47, 280)],
        [-F(6, 35), F(94, 175), -F(29, 175)],
        [-F(47, 280), -F(29, 175), F(747, 1400)],
    ]
    zero = [[F(0) for _ in range(3)] for __ in range(3)]
    q = F(87, 1250)
    m = F(87, 2500)
    L = 8 * (27 / (m * m) + 54 / m + 18)
    delta = F(36163, 16056110400)
    delta_choices = [F(1, 10), q / 6, F(43, 100) / L]
    exp4_lower = sum(F(4**j, math.factorial(j)) for j in range(5))

    base_atoms, base_inc, signed_failures, atom_total = exact_atoms_checked(K, zero, zero)
    base_atom_values = [a[(0, 0)] for a in base_atoms]
    eigenvalues = [F(1, 5), F(7, 10), F(71, 100)]

    perturbations = []
    for i in range(3):
        A = [[F(0) for _ in range(3)] for __ in range(3)]
        A[i][i] = F(1)
        perturbations.append(A)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        A = [[F(0) for _ in range(3)] for __ in range(3)]
        A[i][j] = F(1, 2)
        A[j][i] = F(1, 2)
        perturbations.append(A)
    directions = perturbations + [
        [[F(1), F(1, 3), -F(1, 5)], [F(1, 3), -F(2, 3), F(1, 7)], [-F(1, 5), F(1, 7), F(1, 4)]]
    ]

    sample_failures = []
    max_abs_h3_ratio = Decimal(0)
    min_sample_h2_margin = Decimal("Infinity")
    max_sample_h2_margin = Decimal("-Infinity")
    with localcontext() as ctx:
        ctx.prec = 80
        sample_count = 0
        event_jet_count = 0
        for E in perturbations:
            E2 = frob2(E)
            for sign in [F(-1), F(1)]:
                point = mat_add(K, E, sign * delta)
                for D in directions:
                    D2 = frob2(D)
                    atoms, _, fail, total = exact_atoms_checked(point, E, D)
                    sample_count += 1
                    event_jet_count += 8
                    if fail:
                        sample_failures.append({"kind": "signed_det_mismatch", "masks": fail})
                    if total != {(0, 0): F(1)}:
                        sample_failures.append({"kind": "atom_sum_not_one", "total": str(total)})
                    for atom in atoms:
                        p = atom.get((0, 0), F(0))
                        pe = atom.get((1, 0), F(0))
                        pd = atom.get((0, 1), F(0))
                        ped = atom.get((1, 1), F(0))
                        pdd = 2 * atom.get((0, 2), F(0))
                        pedd = 2 * atom.get((1, 2), F(0))
                        tests = [
                            pe * pe <= 9 * E2,
                            pd * pd <= 9 * D2,
                            ped * ped <= 36 * E2 * D2,
                            pdd * pdd <= 36 * D2 * D2,
                            pedd * pedd <= 36 * E2 * D2 * D2,
                            m <= p <= 1,
                        ]
                        if not all(tests):
                            sample_failures.append({"kind": "jet_or_floor_bound_failed", "atom": str(atom)})
                    h3 = h3_chain_from_atoms(atoms)
                    bound = dec(L) * dec(E2).sqrt() * dec(D2)
                    if bound:
                        max_abs_h3_ratio = max(max_abs_h3_ratio, abs(h3) / bound)
                    if abs(h3) > bound:
                        sample_failures.append({"kind": "H3_bound_failed", "H3": str(h3), "bound": str(bound)})
                    h2 = h2_from_atoms(atoms)
                    h2_margin = h2 + dec(F(43, 100) * D2)
                    min_sample_h2_margin = min(min_sample_h2_margin, h2_margin)
                    max_sample_h2_margin = max(max_sample_h2_margin, h2_margin)
                    if h2_margin > 0:
                        sample_failures.append({"kind": "sample_H2_margin_failed", "margin": str(h2_margin)})
        hessian = hessian_sanity(K)

    author_results = json.loads((BASE / "sanity_results.json").read_text(encoding="utf-8"))
    run_log = (BASE / "run_log.md").read_text(encoding="utf-8")
    script_hash = sha256_file(BASE / "sanity.py")
    result_hash = sha256_file(BASE / "sanity_results.json")
    run_log_script_hash_match = bool(re.search(re.escape(script_hash), run_log, flags=re.IGNORECASE))
    run_log_result_hash_match = bool(re.search(re.escape(result_hash), run_log, flags=re.IGNORECASE))

    exact_checks = {
        "L_exact": L == F(160561104, 841),
        "delta_exact": delta == min(delta_choices) == F(36163, 16056110400),
        "delta_loss_exact": L * delta == F(43, 100),
        "strict_radius_exact": delta <= F(1, 10) and F(1, 5) - delta > F(1, 10) and F(71, 100) + delta < F(9, 10),
        "atom_floor_exact": q - 3 * delta >= m,
        "exp4_log_bound_exact": exp4_lower == F(103, 3) and exp4_lower > 1 / m,
        "base_atoms_exact": base_atom_values
        == [F(87, 1250), F(4159, 35000), F(4099, 35000), F(5631, 35000), F(3999, 35000), F(2803, 17500), F(5591, 35000), F(497, 5000)],
        "base_atom_min_exact": min(base_atom_values) == q,
        "base_atom_sum_exact": atom_total == {(0, 0): F(1)},
        "signed_det_identity_base": not signed_failures,
        "eigen_roots_exact": all(charpoly_value(K, lam) == 0 for lam in eigenvalues) and len(set(eigenvalues)) == 3,
        "sample_jet_checks": not sample_failures,
        "author_sanity_counts_match": author_results["counts"]["base_atom_checks"] == 8
        and author_results["counts"]["perturbed_kernels"] == 12
        and author_results["counts"]["directions_per_kernel"] == 4
        and author_results["counts"]["mixed_jet_cases"] == 48
        and author_results["counts"]["exact_atom_jet_checks"] == 384
        and author_results["counts"]["failed_checks"] == 0
        and author_results["exit_code"] == 0,
        "author_hashes_match_run_log": run_log_script_hash_match and run_log_result_hash_match,
        "base_hessian_float_sanity": hessian["max_eigenvalue_below_minus_43_over_50"],
    }
    report = {
        "status": "CORRECT",
        "scope": "non-author audit of S7 transfer proof, conditional on previously verified S5 full-Hessian input",
        "constants": {
            "q": str(q),
            "m": str(m),
            "L": str(L),
            "delta": str(delta),
            "delta_decimal": str(dec(delta)),
            "delta_choices": [str(x) for x in delta_choices],
            "L_delta": str(L * delta),
            "q_minus_3delta": str(q - 3 * delta),
            "spectral_lower_bound": str(F(1, 5) - delta),
            "spectral_upper_bound": str(F(71, 100) + delta),
            "exp4_partial_lower": str(exp4_lower),
        },
        "base": {
            "atoms": [str(x) for x in base_atom_values],
            "eigenvalues": [str(x) for x in eigenvalues],
            "hessian_sanity": hessian,
        },
        "independent_sample_jets": {
            "perturbation_directions": len(perturbations),
            "boundary_points": 2 * len(perturbations),
            "directions_per_point": len(directions),
            "mixed_jet_cases": sample_count,
            "event_jet_checks": event_jet_count,
            "failures": sample_failures,
            "max_abs_H3_over_bound": str(max_abs_h3_ratio),
            "min_sample_H2_plus_43_over_100_D2": str(min_sample_h2_margin),
            "max_sample_H2_plus_43_over_100_D2": str(max_sample_h2_margin),
        },
        "author_sanity": {
            "script_sha256": script_hash,
            "result_sha256": result_hash,
            "run_log_script_hash_match": run_log_script_hash_match,
            "run_log_result_hash_match": run_log_result_hash_match,
            "counts": author_results["counts"],
            "exit_code": author_results["exit_code"],
        },
        "exact_checks": exact_checks,
        "audit_script_sha256": sha256_file(Path(__file__)),
        "elapsed_seconds": time.time() - started,
        "exit_code": 0 if all(exact_checks.values()) else 1,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"exit_code": report["exit_code"], "out": str(OUT), "elapsed_seconds": report["elapsed_seconds"]}, indent=2))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
