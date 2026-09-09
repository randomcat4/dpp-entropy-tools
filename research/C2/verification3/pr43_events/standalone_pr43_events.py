#!/usr/bin/env python3
"""Standalone exact verifier for PR43 continuation B/C event checks.

This file intentionally does not import the author's verification modules.
It reconstructs complete DPP event laws from inclusion determinants by
Boolean Mobius inversion and writes machine-readable certificates after each
bounded object is checked.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import traceback
from typing import Any

import sympy as sp


Q = sp.Rational
FROZEN_PR_COMMIT = "4e1369ef2a59ccfaba3ca8fce95d85e78857bf78"
DOC_ONLY_HEAD_NOT_USED = "7bd5962bbb2020ce47fbe286adda7dfe02f9645d"


SOURCE_REFERENCES = [
    {
        "file": "continuation/CODEX_VERIFICATION_TASKS_v2.md",
        "lines": "31-46",
        "role": "author replay and independent Mobius event reconstruction scope",
    },
    {
        "file": "continuation/CODEX_VERIFICATION_TASKS_v2.md",
        "lines": "50-63",
        "role": "bounded reversible mechanism obstruction scope",
    },
    {
        "file": "continuation/frozen_statement_v3.md",
        "lines": "19-77",
        "role": "diagonal active-sector 3+5 fixture statement",
    },
    {
        "file": "continuation/frozen_statement_v3.md",
        "lines": "78-150",
        "role": "rank-two exterior Markov mechanism statement",
    },
    {
        "file": "continuation/frozen_statement_v3.md",
        "lines": "151-170",
        "role": "diagonal refresh exterior-degree mechanism",
    },
    {
        "file": "continuation/frozen_statement_v3.md",
        "lines": "171-196",
        "role": "reversible two-point obstruction statement",
    },
    {
        "file": "continuation/frozen_statement_v3.md",
        "lines": "197-214",
        "role": "two-mode quasi-free measurement obstruction statement",
    },
    {
        "file": "proof/04_diagonal_active_sector.md",
        "lines": "103-164",
        "role": "rational 3+5 fixture inputs and legality bounds",
    },
    {
        "file": "proof/06_quantum_measurement_obstruction.md",
        "lines": "10-69",
        "role": "two-mode four-probability obstruction arithmetic",
    },
    {
        "file": "proof/07_markov_adjoint_and_reversible_obstruction.md",
        "lines": "91-170",
        "role": "reversible obstruction matrices and orthogonality argument",
    },
    {
        "file": "continuation/code/verify_continuation.py",
        "lines": "49-239",
        "role": "author continuation exact verifier replayed as a black-box script",
    },
    {
        "file": "continuation/code/verify_continuation_v2.py",
        "lines": "7-45",
        "role": "author v2 exact verifier replayed as a black-box script",
    },
]


def configure_timeout(seconds: int) -> None:
    if seconds <= 0:
        return
    if hasattr(signal, "SIGALRM"):
        def _handler(signum: int, frame: Any) -> None:
            raise TimeoutError(f"verification exceeded {seconds} seconds")

        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(seconds)


def ensure_thread_environment() -> None:
    limits = {
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "BLIS_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "CUDA_VISIBLE_DEVICES": "",
    }
    for key, value in limits.items():
        os.environ.setdefault(key, value)


def sstr(value: Any) -> str:
    return str(sp.factor(value)) if isinstance(value, sp.Basic) else str(value)


def matrix_to_str(M: sp.Matrix) -> list[list[str]]:
    return [[sstr(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def json_ready(value: Any) -> Any:
    if value == sp.S.true:
        return True
    if value == sp.S.false:
        return False
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, sp.Basic):
        return sstr(value)
    return value


def write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n")


def checkpoint(out_dir: Path, name: str, status: str, payload: dict[str, Any] | None = None) -> None:
    body = {
        "name": name,
        "status": status,
        "pid": os.getpid(),
        "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if payload:
        body.update(payload)
    write_json(out_dir / "checkpoints" / f"{name}.{status}.json", body)


def mask_bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def author_state_label(mask: int, n: int) -> str:
    """Author helper convention: rightmost label bit is matrix coordinate 1."""
    return "".join(str((mask >> i) & 1) for i in reversed(range(n)))


def coordinate_state_label(mask: int, n: int) -> str:
    """Coordinate-order label: leftmost label bit is matrix coordinate 1."""
    return "".join(str((mask >> i) & 1) for i in range(n))


def event_record(mask: int, n: int, probability: sp.Expr) -> dict[str, str | int | list[int]]:
    return {
        "mask": mask,
        "bits_by_matrix_coordinate": mask_bits(mask, n),
        "coordinate_order_label": coordinate_state_label(mask, n),
        "author_state_label": author_state_label(mask, n),
        "probability": sstr(probability),
    }


def principal_submatrix(M: sp.Matrix, mask: int) -> sp.Matrix:
    idx = [i for i in range(M.rows) if (mask >> i) & 1]
    if not idx:
        return sp.zeros(0, 0)
    return M.extract(idx, idx)


def principal_det(M: sp.Matrix, mask: int) -> sp.Expr:
    if mask == 0:
        return sp.Integer(1)
    return sp.factor(principal_submatrix(M, mask).det())


def inclusion_determinants(K: sp.Matrix) -> list[sp.Expr]:
    return [principal_det(K, mask) for mask in range(1 << K.rows)]


def event_law_from_inclusions(K: sp.Matrix) -> tuple[list[sp.Expr], list[sp.Expr]]:
    """Complete-event probabilities from q(U)=Pr[U subset X]=det(K_U)."""
    n = K.rows
    inclusions = inclusion_determinants(K)
    law: list[sp.Expr] = []
    for exact in range(1 << n):
        total = sp.Integer(0)
        for sup in range(1 << n):
            if (sup & exact) == exact:
                total += (-1) ** ((sup.bit_count() - exact.bit_count())) * inclusions[sup]
        law.append(sp.factor(total))
    return law, inclusions


def all_principal_minor_certificate(M: sp.Matrix, name: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for mask in range(1, 1 << M.rows):
        det = principal_det(M, mask)
        if det <= 0:
            raise AssertionError(f"{name} principal minor {author_state_label(mask, M.rows)} is not positive: {det}")
        rows.append({
            "mask": mask,
            "author_state_label": author_state_label(mask, M.rows),
            "det": sstr(det),
        })
    return {
        "matrix": name,
        "dimension": M.rows,
        "criterion": "all nonempty principal minors are exact positive rationals",
        "count": len(rows),
        "minors": rows,
    }


def strict_contraction_certificate(K: sp.Matrix, name: str) -> dict[str, Any]:
    if K != K.T:
        raise AssertionError(f"{name} is not symmetric")
    return {
        "name": name,
        "K_principal_minors": all_principal_minor_certificate(K, f"{name}:K"),
        "I_minus_K_principal_minors": all_principal_minor_certificate(sp.eye(K.rows) - K, f"{name}:I-K"),
    }


def event_matrix(K: sp.Matrix, mask: int) -> sp.Matrix:
    M = K.copy()
    for i in range(K.rows):
        if not ((mask >> i) & 1):
            M[i, i] -= 1
    return M


def block_matrix(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix, t: sp.Expr) -> sp.Matrix:
    return A.row_join(t * B).col_join((t * B.T).row_join(C))


def parse_rational_matrix(rows: list[list[str]]) -> sp.Matrix:
    return sp.Matrix([[Q(x) for x in row] for row in rows])


def active_sector_inputs() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, list[sp.Rational]]:
    A = sp.Matrix([
        [Q(2, 5), Q(1, 20), Q(1, 30)],
        [Q(1, 20), Q(1, 2), Q(1, 25)],
        [Q(1, 30), Q(1, 25), Q(3, 5)],
    ])
    C = sp.Matrix([
        [Q(1, 3), 0, 0, 0, 0],
        [0, Q(1, 2), 0, 0, 0],
        [0, 0, Q(2, 3), 0, 0],
        [0, 0, 0, Q(2, 5), Q(1, 20)],
        [0, 0, 0, Q(1, 20), Q(3, 5)],
    ])
    B = sp.Matrix([
        [Q(1, 100), Q(1, 100), Q(1, 50), 0, 0],
        [Q(1, 50), 0, Q(3, 100), 0, 0],
        [Q(1, 100), -Q(1, 100), Q(1, 100), 0, 0],
    ])
    return A, C, B, [Q(1, 5), Q(1, 2), Q(1, 1)]


def conditional_kernel(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix, left_mask: int, t: sp.Expr) -> sp.Matrix:
    X = event_matrix(A, left_mask)
    M = sp.simplify(B.T * X.inv() * B)
    return sp.simplify(C - t * t * M)


def sum_law(law: list[sp.Expr], name: str) -> None:
    total = sp.factor(sum(law))
    if total != 1:
        raise AssertionError(f"{name} event law sums to {total}, not 1")
    nonpositive = [(i, p) for i, p in enumerate(law) if p <= 0]
    if nonpositive:
        raise AssertionError(f"{name} has nonpositive event probabilities: {nonpositive[:3]}")


def active_sector_verification(out_dir: Path) -> dict[str, Any]:
    section = "active_sector_3plus5"
    checkpoint(out_dir, section, "started")
    A, C, B, t_values = active_sector_inputs()
    law_A, inc_A = event_law_from_inclusions(A)
    law_C, inc_C = event_law_from_inclusions(C)
    sum_law(law_A, "A")
    sum_law(law_C, "C")

    active_cols = [j for j in range(B.cols) if any(B[i, j] != 0 for i in range(B.rows))]
    rank_checks = {
        "rank_B": B.rank(),
        "row2_equals_row1_plus_row3": B.row(1) == B.row(0) + B.row(2),
        "row1_and_row3_not_proportional": B.extract([0, 2], [0, 1]).det() != 0,
        "active_columns_zero_based": active_cols,
        "last_two_columns_zero": all(B[i, j] == 0 for i in range(B.rows) for j in (3, 4)),
        "first_three_columns_nonzero": all(any(B[i, j] != 0 for i in range(B.rows)) for j in (0, 1, 2)),
        "not_contained_in_any_two_coordinate_principal_plane": len(active_cols) > 2,
        "C_active_block_diagonal": C[:3, :3].is_diagonal(),
        "C_active_to_inactive_zero": C[:3, 3:] == sp.zeros(3, 2) and C[3:, :3] == sp.zeros(2, 3),
        "A_has_offdiagonal_entry": any(A[i, j] != 0 for i in range(A.rows) for j in range(A.cols) if i != j),
        "C_has_offdiagonal_entry": any(C[i, j] != 0 for i in range(C.rows) for j in range(C.cols) if i != j),
    }
    if rank_checks["rank_B"] != 2:
        raise AssertionError("active-sector B rank is not 2")
    if not all(v for k, v in rank_checks.items() if k not in {"rank_B", "active_columns_zero_based"}):
        raise AssertionError(f"active-sector structural checks failed: {rank_checks}")

    frob_bound = Q(22, 10000)
    base_bound_K = Q(19, 60)
    base_bound_IK = Q(49, 150)
    uniform_legality = {
        "A_gershgorin_row_margins": ["19/60", "41/100", "79/150"],
        "I_minus_A_gershgorin_row_margins": ["31/60", "41/100", "49/150"],
        "C_and_I_minus_C_lower_bound": "1/3",
        "B_operator_norm_squared_upper_bound": sstr(frob_bound),
        "B_norm_lt_A_C_block_lower_bound": frob_bound < base_bound_K * base_bound_K,
        "B_norm_lt_I_minus_A_C_block_lower_bound": frob_bound < base_bound_IK * base_bound_IK,
        "conclusion": "Weyl plus exact rational squared inequalities proves 0<K(t)<I for every |t|<=1",
    }
    if not uniform_legality["B_norm_lt_A_C_block_lower_bound"]:
        raise AssertionError("B norm bound does not prove K(t)>0 for |t|<=1")
    if not uniform_legality["B_norm_lt_I_minus_A_C_block_lower_bound"]:
        raise AssertionError("B norm bound does not prove I-K(t)>0 for |t|<=1")

    payload: dict[str, Any] = {
        "status": "PASS",
        "source_scope": "PR43 continuation B/C only",
        "inputs": {
            "A": matrix_to_str(A),
            "C": matrix_to_str(C),
            "B": matrix_to_str(B),
            "t_values": [sstr(t) for t in t_values],
        },
        "event_law_method": "inclusion determinants det(K_U), then Boolean Mobius inversion p(S)=sum_{U superset S}(-1)^(|U|-|S|)det(K_U)",
        "state_label_convention": state_label_convention(),
        "structural_checks": rank_checks,
        "uniform_legality_rational_certificate": uniform_legality,
        "strict_contractions": [
            strict_contraction_certificate(A, "A"),
            strict_contraction_certificate(C, "C"),
        ],
        "A_event_law": [event_record(mask, 3, law_A[mask]) for mask in range(8)],
        "C_event_law": [event_record(mask, 5, law_C[mask]) for mask in range(32)],
        "A_inclusion_determinants": [event_record(mask, 3, inc_A[mask]) for mask in range(8)],
        "C_inclusion_determinants": [event_record(mask, 5, inc_C[mask]) for mask in range(32)],
        "t_checks": [],
    }

    for t in t_values:
        t_name = str(t).replace("/", "_")
        checkpoint(out_dir, f"{section}_t_{t_name}", "started")
        K = block_matrix(A, B, C, t)
        law_K, inc_K = event_law_from_inclusions(K)
        sum_law(law_K, f"K({t})")
        t_payload: dict[str, Any] = {
            "t": sstr(t),
            "strict_contraction": strict_contraction_certificate(K, f"K({t})"),
            "inclusion_determinants": [event_record(mask, 8, inc_K[mask]) for mask in range(256)],
            "full_event_law_256": [event_record(mask, 8, law_K[mask]) for mask in range(256)],
            "left_configuration_checks": [],
            "max_identity_residual": "0",
        }
        for left_mask in range(8):
            C_cond = conditional_kernel(A, B, C, left_mask, t)
            law_cond, inc_cond = event_law_from_inclusions(C_cond)
            sum_law(law_cond, f"C_cond(t={t}, S={author_state_label(left_mask, 3)})")
            marginal = sp.Integer(0)
            conditional_rows: list[dict[str, Any]] = []
            for right_mask in range(32):
                full_mask = left_mask | (right_mask << 3)
                lhs = sp.factor(law_K[full_mask])
                rhs = sp.factor(law_A[left_mask] * law_cond[right_mask])
                residual = sp.factor(lhs - rhs)
                if residual != 0:
                    raise AssertionError(
                        f"Schur event identity failed at t={t}, left={left_mask}, right={right_mask}: {residual}"
                    )
                marginal += lhs
                conditional_rows.append({
                    "right_mask": right_mask,
                    "right_author_state_label": author_state_label(right_mask, 5),
                    "full_mask": full_mask,
                    "full_author_state_label": author_state_label(full_mask, 8),
                    "p_full": sstr(lhs),
                    "p_A_times_p_cond": sstr(rhs),
                    "residual": "0",
                })
            marginal_residual = sp.factor(marginal - law_A[left_mask])
            if marginal_residual != 0:
                raise AssertionError(f"left marginal failed at t={t}, left={left_mask}: {marginal_residual}")
            t_payload["left_configuration_checks"].append({
                "left_mask": left_mask,
                "left_author_state_label": author_state_label(left_mask, 3),
                "p_A_left": sstr(law_A[left_mask]),
                "left_marginal_from_256_events": sstr(marginal),
                "marginal_residual": "0",
                "conditional_kernel": matrix_to_str(C_cond),
                "conditional_strict_contraction": strict_contraction_certificate(
                    C_cond, f"C_cond(t={t}, S={author_state_label(left_mask, 3)})"
                ),
                "conditional_inclusion_determinants": [
                    event_record(mask, 5, inc_cond[mask]) for mask in range(32)
                ],
                "conditional_event_law_32": [
                    event_record(mask, 5, law_cond[mask]) for mask in range(32)
                ],
                "conditional_event_identities_32": conditional_rows,
            })
        payload["t_checks"].append(t_payload)
        write_json(out_dir / "certificates" / f"active_sector_t_{t_name}.json", t_payload)
        checkpoint(out_dir, f"{section}_t_{t_name}", "done", {"full_events": 256, "conditional_events": 8 * 32})

    write_json(out_dir / "certificates" / "active_sector_3plus5.json", payload)
    checkpoint(out_dir, section, "done", {"t_values": [sstr(t) for t in t_values]})
    return payload


def state_label_convention() -> dict[str, Any]:
    return {
        "internal_masks": "zero-based bit i is matrix coordinate i+1",
        "author_state_label": "bits are printed in descending coordinate order; the rightmost bit is matrix coordinate 1",
        "coordinate_order_label": "bits are printed in matrix coordinate order; the leftmost bit is matrix coordinate 1",
        "example_n2_mask_order": [
            {"mask": i, "author_state_label": author_state_label(i, 2), "coordinate_order_label": coordinate_state_label(i, 2)}
            for i in range(4)
        ],
    }


def diagonal_refresh_verification(out_dir: Path) -> dict[str, Any]:
    section = "diagonal_refresh"
    checkpoint(out_dir, section, "started")
    c = [Q(1, 3), Q(1, 2), Q(2, 3)]
    V = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    theta = Q(2, 5)
    states = list(range(8))

    def mu(mask: int) -> sp.Expr:
        out = sp.Integer(1)
        for i, ci in enumerate(c):
            out *= ci if ((mask >> i) & 1) else 1 - ci
        return sp.factor(out)

    def z(mask: int, i: int) -> sp.Expr:
        return sp.factor((((mask >> i) & 1) - c[i]) / (c[i] * (1 - c[i])))

    def G(mask: int) -> sp.Matrix:
        out = sp.zeros(2)
        for i in range(3):
            vi = V[i, :].T
            out += z(mask, i) * vi * vi.T
        return sp.simplify(out)

    def d(mask: int) -> sp.Expr:
        direct = sp.factor(G(mask).det())
        mixed = sp.Integer(0)
        for i in range(3):
            for j in range(i + 1, 3):
                two_rows = sp.Matrix.vstack(V[i, :], V[j, :])
                mixed += z(mask, i) * z(mask, j) * two_rows.det() ** 2
        mixed = sp.factor(mixed)
        if sp.factor(direct - mixed) != 0:
            raise AssertionError(f"diagonal refresh Cauchy-Binet det mismatch at mask {mask}")
        return direct

    def transition(x: int, y: int) -> sp.Expr:
        p = sp.Integer(1)
        for i, ci in enumerate(c):
            xb = (x >> i) & 1
            yb = (y >> i) & 1
            redraw = ci if yb else 1 - ci
            p *= theta * int(xb == yb) + (1 - theta) * redraw
        return sp.factor(p)

    mus = [mu(x) for x in states]
    if sp.factor(sum(mus)) != 1:
        raise AssertionError("diagonal refresh stationary law does not sum to 1")
    Gs = [G(x) for x in states]
    ds = [d(x) for x in states]
    mean_G = sum((mus[x] * Gs[x] for x in states), sp.zeros(2))
    mean_d = sp.factor(sum(mus[x] * ds[x] for x in states))
    if sp.simplify(mean_G) != sp.zeros(2):
        raise AssertionError("diagonal refresh E[G] is not zero")
    if mean_d != 0:
        raise AssertionError("diagonal refresh E[det G] is not zero")

    transitions: list[dict[str, Any]] = []
    row_checks: list[dict[str, Any]] = []
    detailed_balance_failures: list[str] = []
    for x in states:
        row = [transition(x, y) for y in states]
        if sp.factor(sum(row)) != 1:
            raise AssertionError(f"diagonal refresh transition row {x} does not sum to 1")
        if any(p < 0 for p in row):
            raise AssertionError(f"diagonal refresh transition row {x} has negative probability")
        TG = sum((row[y] * Gs[y] for y in states), sp.zeros(2))
        Td = sp.factor(sum(row[y] * ds[y] for y in states))
        if sp.simplify(TG - theta * Gs[x]) != sp.zeros(2):
            raise AssertionError(f"diagonal refresh G eigenrelation failed at state {x}")
        if sp.factor(Td - theta ** 2 * ds[x]) != 0:
            raise AssertionError(f"diagonal refresh det eigenrelation failed at state {x}")
        row_checks.append({
            "from_mask": x,
            "from_author_state_label": author_state_label(x, 3),
            "row_sum": "1",
            "TG_minus_theta_G": matrix_to_str(sp.simplify(TG - theta * Gs[x])),
            "Td_minus_theta2_d": "0",
        })
        for y in states:
            transitions.append({
                "from_mask": x,
                "from_author_state_label": author_state_label(x, 3),
                "to_mask": y,
                "to_author_state_label": author_state_label(y, 3),
                "probability": sstr(row[y]),
            })

    stationarity: list[dict[str, Any]] = []
    for y in states:
        incoming = sp.factor(sum(mus[x] * transition(x, y) for x in states))
        if sp.factor(incoming - mus[y]) != 0:
            raise AssertionError(f"diagonal refresh stationarity failed at state {y}")
        stationarity.append({
            "to_mask": y,
            "to_author_state_label": author_state_label(y, 3),
            "incoming_mass": sstr(incoming),
            "mu": sstr(mus[y]),
            "residual": "0",
        })
        for x in states:
            residual = sp.factor(mus[x] * transition(x, y) - mus[y] * transition(y, x))
            if residual != 0:
                detailed_balance_failures.append(f"{x}->{y}:{residual}")
    if detailed_balance_failures:
        raise AssertionError(f"diagonal refresh detailed balance failures: {detailed_balance_failures[:3]}")

    payload = {
        "status": "PASS",
        "inputs": {
            "C_diagonal": [sstr(x) for x in c],
            "V": matrix_to_str(V),
            "theta": sstr(theta),
        },
        "state_label_convention": state_label_convention(),
        "state_rows": [
            {
                "mask": x,
                "author_state_label": author_state_label(x, 3),
                "bits_by_matrix_coordinate": mask_bits(x, 3),
                "mu": sstr(mus[x]),
                "z": [sstr(z(x, i)) for i in range(3)],
                "G": matrix_to_str(Gs[x]),
                "detG": sstr(ds[x]),
            }
            for x in states
        ],
        "transition_matrix_64": transitions,
        "row_eigen_checks": row_checks,
        "stationarity_checks": stationarity,
        "detailed_balance": "all 64 exact pairwise identities mu_x P_xy = mu_y P_yx checked",
        "moments": {
            "E_G": matrix_to_str(mean_G),
            "E_detG": sstr(mean_d),
        },
    }
    write_json(out_dir / "certificates" / "diagonal_refresh.json", payload)
    checkpoint(out_dir, section, "done", {"states": 8, "transitions": 64})
    return payload


def quantum_obstruction_verification(out_dir: Path) -> dict[str, Any]:
    section = "quantum_obstruction"
    checkpoint(out_dir, section, "started")
    K_plus = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    K_minus = sp.Matrix([[Q(1, 2), -Q(1, 10)], [-Q(1, 10), Q(1, 2)]])
    A0 = sp.Matrix([[Q(1, 2), Q(1, 5)], [Q(1, 5), Q(1, 2)]])
    theta = Q(1, 2)
    out_plus = sp.simplify(theta * K_plus + (1 - theta) * A0)
    out_minus = sp.simplify(theta * K_minus + (1 - theta) * A0)
    laws: dict[str, list[sp.Expr]] = {}
    inclusions: dict[str, list[sp.Expr]] = {}
    for name, K in {
        "K_plus": K_plus,
        "K_minus": K_minus,
        "A0": A0,
        "Phi_K_plus": out_plus,
        "Phi_K_minus": out_minus,
    }.items():
        strict_contraction_certificate(K, name)
        laws[name], inclusions[name] = event_law_from_inclusions(K)
        sum_law(laws[name], name)
    if laws["K_plus"] != laws["K_minus"]:
        raise AssertionError("K_plus and K_minus input event laws differ")
    if laws["Phi_K_plus"] == laws["Phi_K_minus"]:
        raise AssertionError("quasi-free outputs did not separate event laws")
    if laws["Phi_K_plus"][3] != Q(91, 400):
        raise AssertionError(f"Phi_K_plus full event probability is {laws['Phi_K_plus'][3]}")
    if laws["Phi_K_minus"][3] != Q(99, 400):
        raise AssertionError(f"Phi_K_minus full event probability is {laws['Phi_K_minus'][3]}")
    payload = {
        "status": "PASS",
        "inputs": {
            "K_plus": matrix_to_str(K_plus),
            "K_minus": matrix_to_str(K_minus),
            "A0": matrix_to_str(A0),
            "theta": sstr(theta),
        },
        "outputs": {
            "Phi_K_plus": matrix_to_str(out_plus),
            "Phi_K_minus": matrix_to_str(out_minus),
        },
        "state_label_convention": state_label_convention(),
        "event_laws_four_probabilities": {
            name: [event_record(mask, 2, law[mask]) for mask in range(4)]
            for name, law in laws.items()
        },
        "inclusion_determinants": {
            name: [event_record(mask, 2, inc[mask]) for mask in range(4)]
            for name, inc in inclusions.items()
        },
        "checks": {
            "input_laws_equal": True,
            "expected_input_law_author_mask_order": [sstr(x) for x in [Q(6, 25), Q(13, 50), Q(13, 50), Q(6, 25)]],
            "Phi_K_plus_full_event_mask_3": "91/400",
            "Phi_K_minus_full_event_mask_3": "99/400",
            "conclusion": "No single classical channel depending only on the input occupation event law can realize this correlated quasi-free covariance decay for all inputs.",
        },
    }
    write_json(out_dir / "certificates" / "quantum_obstruction.json", payload)
    checkpoint(out_dir, section, "done", {"states": 4})
    return payload


def reversible_obstruction_verification(out_dir: Path) -> dict[str, Any]:
    section = "reversible_obstruction"
    checkpoint(out_dir, section, "started")
    C = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    V = sp.eye(2)
    strict = strict_contraction_certificate(C, "reversible_C")
    mu, inclusions = event_law_from_inclusions(C)
    sum_law(mu, "reversible_C")
    expected_mu = [Q(6, 25), Q(13, 50), Q(13, 50), Q(6, 25)]
    if mu != expected_mu:
        raise AssertionError(f"reversible obstruction event law mismatch: {mu}")
    moment = sp.Integer(0)
    rows: list[dict[str, Any]] = []
    for mask, p in enumerate(mu):
        Y = event_matrix(C, mask)
        G = sp.simplify(V.T * Y.inv() * V)
        d = sp.factor(G.det())
        signed_identity = sp.factor(p * d)
        expected_sign = (-1) ** (2 - mask.bit_count())
        contribution = sp.factor(p * d * G[0, 1])
        moment += contribution
        rows.append({
            "mask": mask,
            "author_state_label": author_state_label(mask, 2),
            "bits_by_matrix_coordinate": mask_bits(mask, 2),
            "mu": sstr(p),
            "Y": matrix_to_str(Y),
            "G_Y_inverse": matrix_to_str(G),
            "detG": sstr(d),
            "mu_times_detG": sstr(signed_identity),
            "expected_mu_times_detG_sign": sstr(expected_sign),
            "contribution_mu_d_G12": sstr(contribution),
        })
        if signed_identity != expected_sign:
            raise AssertionError(f"mu*d sign identity failed at mask {mask}: {signed_identity}")
    moment = sp.factor(moment)
    if moment != -Q(125, 78):
        raise AssertionError(f"reversible obstruction moment is {moment}, not -125/78")
    payload = {
        "status": "PASS",
        "inputs": {
            "C": matrix_to_str(C),
            "V": matrix_to_str(V),
        },
        "state_label_convention": state_label_convention(),
        "strict_contraction": strict,
        "inclusion_determinants": [event_record(mask, 2, inclusions[mask]) for mask in range(4)],
        "event_law_mu": [event_record(mask, 2, mu[mask]) for mask in range(4)],
        "resolvent_rows": rows,
        "moment_E_mu_d_G12": sstr(moment),
        "two_line_selfadjoint_orthogonality_check": [
            "If Q is self-adjoint in L2(mu), Q G12 = theta G12, and Q d = theta^2 d, then theta <d,G12> = <d,QG12> = <Qd,G12> = theta^2 <d,G12>.",
            "For 0 < theta < 1 this forces <d,G12> = 0, contradicting the exact value -125/78, so only the reversible exterior-noise mechanism is excluded.",
        ],
        "scope_guard": "This bounded check does not certify all PR proofs and does not produce an entropy counterexample.",
    }
    write_json(out_dir / "certificates" / "reversible_obstruction.json", payload)
    checkpoint(out_dir, section, "done", {"states": 4, "moment": "-125/78"})
    return payload


def command_for_log(cmd: list[str]) -> list[str]:
    if not cmd:
        return cmd
    shown = cmd[:]
    shown[0] = Path(shown[0]).name
    return shown


def run_command(cmd: list[str], cwd: Path, label: str) -> dict[str, Any]:
    start = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )
    return {
        "label": label,
        "cwd_label": cwd.name if cwd.name else str(cwd),
        "command": command_for_log(cmd),
        "exit_code": proc.returncode,
        "duration_seconds": round(time.time() - start, 3),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def author_replay(out_dir: Path, source_root: Path | None) -> dict[str, Any]:
    section = "author_replay"
    checkpoint(out_dir, section, "started")
    if source_root is None:
        payload = {
            "status": "UNRESOLVED",
            "reason": "source_root was not supplied; author scripts were not replayed",
        }
        write_json(out_dir / "certificates" / "author_replay.json", payload)
        checkpoint(out_dir, section, "unresolved", {"reason": payload["reason"]})
        return payload
    continuation = source_root / "continuation"
    requirements = continuation / "requirements.txt"
    script1 = continuation / "code" / "verify_continuation.py"
    script2 = continuation / "code" / "verify_continuation_v2.py"
    missing = [str(p) for p in [requirements, script1, script2] if not p.exists()]
    if missing:
        payload = {
            "status": "FAIL",
            "missing": missing,
        }
        write_json(out_dir / "certificates" / "author_replay.json", payload)
        checkpoint(out_dir, section, "failed", {"missing_count": len(missing)})
        return payload

    python = sys.executable
    commands = [
        ([python, "-m", "pip", "install", "--disable-pip-version-check", "-r", "requirements.txt"], continuation, "pip_install_requirements"),
        ([python, "code/verify_continuation.py"], continuation, "author_verify_continuation_py"),
        ([python, "code/verify_continuation_v2.py"], continuation, "author_verify_continuation_v2_py"),
    ]
    runs = [run_command(cmd, cwd, label) for cmd, cwd, label in commands]
    checks = {
        "pip_exit_0": runs[0]["exit_code"] == 0,
        "verify_continuation_exit_0": runs[1]["exit_code"] == 0,
        "verify_continuation_last_line": runs[1]["stdout"].strip().splitlines()[-1] if runs[1]["stdout"].strip() else "",
        "verify_continuation_v2_exit_0": runs[2]["exit_code"] == 0,
        "verify_continuation_v2_last_line": runs[2]["stdout"].strip().splitlines()[-1] if runs[2]["stdout"].strip() else "",
    }
    status = "PASS"
    if not checks["pip_exit_0"]:
        status = "FAIL"
    if not checks["verify_continuation_exit_0"] or checks["verify_continuation_last_line"] != "ALL CONTINUATION CHECKS PASSED":
        status = "FAIL"
    if not checks["verify_continuation_v2_exit_0"] or checks["verify_continuation_v2_last_line"] != "ALL CONTINUATION V2 CHECKS PASSED":
        status = "FAIL"
    payload = {
        "status": status,
        "source_root_label": "provided immutable PR43 source tree",
        "scripts_replayed": [
            "continuation/code/verify_continuation.py",
            "continuation/code/verify_continuation_v2.py",
        ],
        "root_author_code_replayed": False,
        "root_author_code_reason": "Coordination withdrew the optional root replay to avoid duplicate C1 work.",
        "runs": runs,
        "checks": checks,
    }
    write_json(out_dir / "certificates" / "author_replay.json", payload)
    checkpoint(out_dir, section, "done" if status == "PASS" else "failed", {"status": status})
    return payload


def metadata(out_dir: Path, source_root: Path | None) -> dict[str, Any]:
    payload = {
        "status": "STARTED",
        "pid": os.getpid(),
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "sympy_version": sp.__version__,
        "start_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_pr_commit": FROZEN_PR_COMMIT,
        "doc_only_head_not_used": DOC_ONLY_HEAD_NOT_USED,
        "scope": "Only continuation task B/C bounded computation: author nested verifier replay plus independent event reconstruction and reversible mechanism obstruction.",
        "resource_limits_requested": {
            "arithmetic_threads": "1",
            "memory": "<=4GiB when launched by remote_run.sh",
            "gpu": "disabled by CUDA_VISIBLE_DEVICES",
            "wall_clock_ceiling": "45 minutes",
        },
        "environment_thread_values": {
            key: os.environ.get(key, "")
            for key in [
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
                "BLIS_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "CUDA_VISIBLE_DEVICES",
            ]
        },
        "source_root_supplied": source_root is not None,
        "source_references": SOURCE_REFERENCES,
        "state_label_convention": state_label_convention(),
    }
    write_json(out_dir / "certificates" / "metadata.json", payload)
    return payload


def write_inputs(out_dir: Path) -> dict[str, Any]:
    A, C, B, t_values = active_sector_inputs()
    c_diag = [Q(1, 3), Q(1, 2), Q(2, 3)]
    V_refresh = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    C_rev = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    K_plus = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    K_minus = sp.Matrix([[Q(1, 2), -Q(1, 10)], [-Q(1, 10), Q(1, 2)]])
    A0 = sp.Matrix([[Q(1, 2), Q(1, 5)], [Q(1, 5), Q(1, 2)]])
    payload = {
        "status": "FROZEN",
        "rational_inputs": {
            "active_sector_3plus5": {
                "A": matrix_to_str(A),
                "C": matrix_to_str(C),
                "B": matrix_to_str(B),
                "t_values": [sstr(t) for t in t_values],
            },
            "diagonal_refresh": {
                "C_diagonal": [sstr(x) for x in c_diag],
                "V": matrix_to_str(V_refresh),
                "theta": "2/5",
            },
            "quasi_free_measurement_obstruction": {
                "K_plus": matrix_to_str(K_plus),
                "K_minus": matrix_to_str(K_minus),
                "A0": matrix_to_str(A0),
                "theta": "1/2",
            },
            "reversible_obstruction": {
                "C": matrix_to_str(C_rev),
                "V": matrix_to_str(sp.eye(2)),
            },
        },
        "event_coordinate_convention": state_label_convention(),
    }
    write_json(out_dir / "certificates" / "frozen_inputs.json", payload)
    return payload


def write_checklist(out_dir: Path, results: dict[str, Any], final_status: str) -> None:
    items = [
        ("author verify_continuation.py replay", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_exit_0") is True),
        ("author verify_continuation.py last line", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_last_line") == "ALL CONTINUATION CHECKS PASSED"),
        ("author verify_continuation_v2.py replay", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_v2_exit_0") is True),
        ("author verify_continuation_v2.py last line", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_v2_last_line") == "ALL CONTINUATION V2 CHECKS PASSED"),
        ("3+5 fixture all 256 events at t=1/5,1/2,1", results.get("active_sector_3plus5", {}).get("status") == "PASS"),
        ("8 left configurations x 32 conditional events at each t", results.get("active_sector_3plus5", {}).get("status") == "PASS"),
        ("strict fixture legality by exact rational criteria", results.get("active_sector_3plus5", {}).get("status") == "PASS"),
        ("diagonal refresh 8 states and 64 transitions", results.get("diagonal_refresh", {}).get("status") == "PASS"),
        ("two-mode quasi-free obstruction four probabilities", results.get("quantum_obstruction", {}).get("status") == "PASS"),
        ("four reversible obstruction G matrices", results.get("reversible_obstruction", {}).get("status") == "PASS"),
        ("E_mu[d G12] = -125/78", results.get("reversible_obstruction", {}).get("moment_E_mu_d_G12") == "-125/78"),
        ("scope guard: no entropy counterexample certification", final_status == "PASS"),
    ]
    payload = {
        "status": final_status,
        "items": [
            {"item": item, "passed": bool(passed)}
            for item, passed in items
        ],
        "source_references": SOURCE_REFERENCES,
    }
    write_json(out_dir / "certificates" / "checklist.json", payload)


def write_report(out_dir: Path, results: dict[str, Any], final_status: str, error: str | None = None) -> None:
    lines = [
        "# PR43 Events Verification Report",
        "",
        f"STATUS: {final_status}",
        "",
        f"Frozen PR commit: `{FROZEN_PR_COMMIT}`.",
        f"Later doc-only PR head noted but not used for this frozen run: `{DOC_ONLY_HEAD_NOT_USED}`.",
        "",
        "Scope: continuation task B/C bounded computation only. This report replays the two nested author exact scripts and independently reconstructs the requested event certificates from inclusion determinants by Boolean Mobius inversion. It does not certify the full analytic proof package, the LP task, novelty, or any entropy counterexample.",
        "",
        "Resource envelope: one arithmetic thread, no GPU visibility, 45 minute ceiling. The remote runner applies a 4 GiB virtual-memory cap before launching Python.",
        "",
        "Event convention: internal mask bit `i` is matrix coordinate `i+1`. Author-style labels print bits in descending coordinate order, so the rightmost label bit is matrix coordinate 1.",
        "",
        "## Results",
        "",
    ]
    result_rows = [
        ("Author `continuation/code/verify_continuation.py`", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_last_line", "missing")),
        ("Author `continuation/code/verify_continuation_v2.py`", results.get("author_replay", {}).get("checks", {}).get("verify_continuation_v2_last_line", "missing")),
        ("Independent 3+5 event/conditional reconstruction", results.get("active_sector_3plus5", {}).get("status", "missing")),
        ("Independent diagonal refresh state/transition table", results.get("diagonal_refresh", {}).get("status", "missing")),
        ("Independent two-mode quasi-free obstruction", results.get("quantum_obstruction", {}).get("status", "missing")),
        ("Independent reversible obstruction", results.get("reversible_obstruction", {}).get("moment_E_mu_d_G12", "missing")),
    ]
    for label, value in result_rows:
        lines.append(f"- {label}: `{value}`")
    lines.extend([
        "",
        "## Certificates",
        "",
        "- `certificates/frozen_inputs.json`: frozen rational inputs and coordinate convention.",
        "- `certificates/author_replay.json`: commands, stdout, stderr, exit codes, and last-line checks for the two nested author scripts.",
        "- `certificates/active_sector_3plus5.json` plus `active_sector_t_*.json`: all 256 full events for each requested `t`, all 8 x 32 conditional events, exact inclusion determinants, exact Schur residuals, and exact principal-minor legality certificates.",
        "- `certificates/diagonal_refresh.json`: all 8 states, all 64 transition probabilities, stationarity, detailed balance, and exact exterior-degree eigenrelations.",
        "- `certificates/quantum_obstruction.json`: four-event input equality and output separation (`91/400` versus `99/400`).",
        "- `certificates/reversible_obstruction.json`: four `Y_T^{-1}` matrices and exact `E_mu[d G12] = -125/78`.",
        "- `certificates/checklist.json`: machine-readable task checklist and source-line map.",
        "",
        "## Reversible Mechanism Note",
        "",
        "If `Q` is self-adjoint in `L2(mu)`, `Q G12 = theta G12`, and `Q d = theta^2 d`, then `theta <d,G12> = <d,QG12> = <Qd,G12> = theta^2 <d,G12>`. For `0 < theta < 1`, this forces `<d,G12> = 0`, contradicting the exact value `-125/78`. This excludes the reversible exterior-noise mechanism only.",
        "",
        "## Source Lines",
        "",
    ])
    for ref in SOURCE_REFERENCES:
        lines.append(f"- `{ref['file']}` lines {ref['lines']}: {ref['role']}.")
    if error:
        lines.extend(["", "## Failure", "", "```text", error, "```"])
    atomic_write_text(out_dir / "REPORT.md", "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=45 * 60)
    parser.add_argument("--skip-author", action="store_true")
    args = parser.parse_args()

    ensure_thread_environment()
    configure_timeout(args.timeout_seconds)
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "certificates").mkdir(parents=True, exist_ok=True)
    (out_dir / "checkpoints").mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}
    final_status = "FAIL"
    try:
        checkpoint(out_dir, "run", "started")
        results["metadata"] = metadata(out_dir, args.source_root)
        results["frozen_inputs"] = write_inputs(out_dir)
        if args.skip_author:
            results["author_replay"] = {
                "status": "UNRESOLVED",
                "reason": "author replay skipped by command line",
            }
            write_json(out_dir / "certificates" / "author_replay.json", results["author_replay"])
        else:
            results["author_replay"] = author_replay(out_dir, args.source_root)
        results["active_sector_3plus5"] = active_sector_verification(out_dir)
        results["diagonal_refresh"] = diagonal_refresh_verification(out_dir)
        results["quantum_obstruction"] = quantum_obstruction_verification(out_dir)
        results["reversible_obstruction"] = reversible_obstruction_verification(out_dir)

        mandatory_pass = [
            results["author_replay"].get("status") == "PASS",
            results["active_sector_3plus5"].get("status") == "PASS",
            results["diagonal_refresh"].get("status") == "PASS",
            results["quantum_obstruction"].get("status") == "PASS",
            results["reversible_obstruction"].get("status") == "PASS",
        ]
        final_status = "PASS" if all(mandatory_pass) else "UNRESOLVED"
        write_checklist(out_dir, results, final_status)
        write_report(out_dir, results, final_status)
        checkpoint(out_dir, "run", "done", {"status": final_status})
        write_json(out_dir / "certificates" / "run_status.json", {
            "status": final_status,
            "pid": os.getpid(),
            "end_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        return 0 if final_status == "PASS" else 2
    except Exception as exc:
        tb = traceback.format_exc()
        write_json(out_dir / "certificates" / "failure.json", {
            "status": "FAIL",
            "exception": repr(exc),
            "traceback": tb,
            "pid": os.getpid(),
            "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        write_checklist(out_dir, results, "FAIL")
        write_report(out_dir, results, "FAIL", tb)
        checkpoint(out_dir, "run", "failed", {"exception": repr(exc)})
        return 1
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
