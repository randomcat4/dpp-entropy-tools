#!/usr/bin/env python3
"""Independent exact PR60 auxiliary certificate.

This script reconstructs the fixed PR60 continuation certificate from the
literal rational matrices in the public request.  It deliberately does not
import or execute the author reference checker.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
import time
import traceback
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass

F = Fraction
N = 3
MASK_LABELS = ["0", "1", "2", "12", "3", "13", "23", "123"]


class DeadlineExceeded(RuntimeError):
    pass


def rat(n: int, d: int = 1) -> F:
    return F(n, d)


def rat_text(x: F) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def rat_parts(x: F) -> dict[str, str]:
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def pow2(k: int) -> F:
    if k >= 0:
        return F(1 << k, 1)
    return F(1, 1 << (-k))


def floor_log2_rational(x: F) -> int:
    if x <= 0:
        raise ValueError("floor_log2_rational requires a positive rational")
    n = x.numerator
    d = x.denominator
    k = n.bit_length() - d.bit_length()
    while x / pow2(k) < 1:
        k -= 1
    while x / pow2(k) >= 2:
        k += 1
    return k


@dataclass(frozen=True)
class Iv:
    lo: F
    hi: F

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError(f"bad interval: {self.lo} > {self.hi}")

    def __add__(self, other: "Iv") -> "Iv":
        return Iv(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Iv") -> "Iv":
        return Iv(self.lo - other.hi, self.hi - other.lo)

    def scale(self, c: F) -> "Iv":
        if c >= 0:
            return Iv(c * self.lo, c * self.hi)
        return Iv(c * self.hi, c * self.lo)

    def width(self) -> F:
        return self.hi - self.lo


def iv_point(x: F) -> Iv:
    return Iv(x, x)


class LogEngine:
    def __init__(self, terms: int) -> None:
        if terms <= 0:
            raise ValueError("terms must be positive")
        self.terms = terms
        self._log2: Iv | None = None

    def atanh_log_1_to_2(self, y: F) -> Iv:
        if not (F(1) <= y <= F(2)):
            raise ValueError(f"atanh input not in [1,2]: {y}")
        z = (y - 1) / (y + 1)
        if z == 0:
            return Iv(F(0), F(0))
        z2 = z * z
        acc = F(0)
        power = z
        for j in range(self.terms):
            acc += power / F(2 * j + 1)
            power *= z2
        tail = F(2) * power / (F(2 * self.terms + 1) * (F(1) - z2))
        lo = F(2) * acc
        return Iv(lo, lo + tail)

    def log2(self) -> Iv:
        if self._log2 is None:
            self._log2 = self.atanh_log_1_to_2(F(2))
        return self._log2

    def log(self, x: F) -> Iv:
        if x <= 0:
            raise ValueError(f"log requires positive rational, got {x}")
        k = floor_log2_rational(x)
        y = x / pow2(k)
        if not (F(1) <= y < F(2)):
            raise AssertionError(f"range reduction failed: x={x}, k={k}, y={y}")
        ly = self.atanh_log_1_to_2(y)
        if k == 0:
            return ly
        l2 = self.log2()
        if k > 0:
            return Iv(F(k) * l2.lo + ly.lo, F(k) * l2.hi + ly.hi)
        return Iv(F(k) * l2.hi + ly.lo, F(k) * l2.lo + ly.hi)


Poly = dict[tuple[int, int], F]


def poly_clean(p: Poly) -> Poly:
    return {k: v for k, v in p.items() if v}


def poly_const(x: F) -> Poly:
    if x == 0:
        return {}
    return {(0, 0): x}


def poly_add(a: Poly, b: Poly) -> Poly:
    out: Poly = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, F(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def poly_neg(a: Poly) -> Poly:
    return {k: -v for k, v in a.items()}


def poly_sub(a: Poly, b: Poly) -> Poly:
    return poly_add(a, poly_neg(b))


def poly_scale(a: Poly, c: F) -> Poly:
    if c == 0:
        return {}
    return {k: c * v for k, v in a.items() if c * v}


def poly_mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for (ea, da), va in a.items():
        for (eb, db), vb in b.items():
            k = (ea + eb, da + db)
            out[k] = out.get(k, F(0)) + va * vb
            if out[k] == 0:
                del out[k]
    return out


def permutation_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inv += 1
    return -1 if inv % 2 else 1


def det_poly(mat: list[list[Poly]]) -> Poly:
    n = len(mat)
    if n == 0:
        return poly_const(F(1))
    for row in mat:
        if len(row) != n:
            raise ValueError("det_poly requires a square matrix")
    out: Poly = {}
    for perm in itertools.permutations(range(n)):
        term = poly_const(F(permutation_sign(perm)))
        for i, j in enumerate(perm):
            term = poly_mul(term, mat[i][j])
        out = poly_add(out, term)
    return poly_clean(out)


def det_fraction(mat: list[list[F]]) -> F:
    n = len(mat)
    if n == 0:
        return F(1)
    for row in mat:
        if len(row) != n:
            raise ValueError("det_fraction requires a square matrix")
    total = F(0)
    for perm in itertools.permutations(range(n)):
        term = F(permutation_sign(perm))
        for i, j in enumerate(perm):
            term *= mat[i][j]
        total += term
    return total


def submatrix_poly(mat: list[list[Poly]], indices: list[int]) -> list[list[Poly]]:
    return [[mat[i][j] for j in indices] for i in indices]


def submatrix_fraction(mat: list[list[F]], indices: list[int]) -> list[list[F]]:
    return [[mat[i][j] for j in indices] for i in indices]


def matrix_poly(k: list[list[F]], d: list[list[F]], c: list[list[F]]) -> list[list[Poly]]:
    out: list[list[Poly]] = []
    for i in range(N):
        row: list[Poly] = []
        for j in range(N):
            p: Poly = {}
            if k[i][j]:
                p[(0, 0)] = k[i][j]
            if d[i][j]:
                p[(1, 0)] = d[i][j]
            if c[i][j]:
                p[(0, 1)] = c[i][j]
            row.append(poly_clean(p))
        out.append(row)
    return out


def event_poly_signed(mask: int, aff: list[list[Poly]]) -> Poly:
    mat: list[list[Poly]] = []
    for i in range(N):
        row: list[Poly] = []
        for j in range(N):
            entry = aff[i][j]
            if i == j and not (mask & (1 << i)):
                entry = poly_sub(entry, poly_const(F(1)))
            row.append(entry)
        mat.append(row)
    sign = F(-1 if (N - mask.bit_count()) % 2 else 1)
    return poly_scale(det_poly(mat), sign)


def event_poly_inclusion(mask: int, aff: list[list[Poly]]) -> Poly:
    base = [i for i in range(N) if mask & (1 << i)]
    free = [i for i in range(N) if not (mask & (1 << i))]
    out: Poly = {}
    for r in range(len(free) + 1):
        for extra in itertools.combinations(free, r):
            indices = sorted(base + list(extra))
            sign = F(-1 if r % 2 else 1)
            out = poly_add(out, poly_scale(det_poly(submatrix_poly(aff, indices)), sign))
    return poly_clean(out)


def event_prob_signed(mask: int, mat0: list[list[F]]) -> F:
    mat = [[mat0[i][j] for j in range(N)] for i in range(N)]
    for i in range(N):
        if not (mask & (1 << i)):
            mat[i][i] -= 1
    sign = F(-1 if (N - mask.bit_count()) % 2 else 1)
    return sign * det_fraction(mat)


def event_prob_inclusion(mask: int, mat0: list[list[F]]) -> F:
    base = [i for i in range(N) if mask & (1 << i)]
    free = [i for i in range(N) if not (mask & (1 << i))]
    out = F(0)
    for r in range(len(free) + 1):
        for extra in itertools.combinations(free, r):
            indices = sorted(base + list(extra))
            out += F(-1 if r % 2 else 1) * det_fraction(submatrix_fraction(mat0, indices))
    return out


def poly_eval(p: Poly, epsilon: F, delta: F) -> F:
    total = F(0)
    ep_powers = {0: F(1)}
    de_powers = {0: F(1)}
    max_e = max((e for e, _ in p), default=0)
    max_d = max((d for _, d in p), default=0)
    for i in range(1, max_e + 1):
        ep_powers[i] = ep_powers[i - 1] * epsilon
    for i in range(1, max_d + 1):
        de_powers[i] = de_powers[i - 1] * delta
    for (e, d), coeff in p.items():
        total += coeff * ep_powers[e] * de_powers[d]
    return total


def jet(p: Poly) -> dict[str, F]:
    return {
        "p": p.get((0, 0), F(0)),
        "pD": p.get((1, 0), F(0)),
        "pDD": F(2) * p.get((2, 0), F(0)),
        "pC": p.get((0, 1), F(0)),
        "pDC": p.get((1, 1), F(0)),
        "pDDC": F(2) * p.get((2, 1), F(0)),
    }


def mat_add(a: list[list[F]], b: list[list[F]], scale_b: F = F(1)) -> list[list[F]]:
    return [[a[i][j] + scale_b * b[i][j] for j in range(N)] for i in range(N)]


def mat_sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(N)] for i in range(N)]


def identity() -> list[list[F]]:
    return [[F(1 if i == j else 0) for j in range(N)] for i in range(N)]


def complement(a: list[list[F]]) -> list[list[F]]:
    return mat_sub(identity(), a)


def diag_part(a: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] if i == j else F(0) for j in range(N)] for i in range(N)]


def leading_sylvester(a: list[list[F]]) -> list[F]:
    return [det_fraction(submatrix_fraction(a, list(range(k)))) for k in range(1, N + 1)]


def all_principal_minors(a: list[list[F]]) -> dict[str, F]:
    out: dict[str, F] = {}
    for r in range(1, N + 1):
        for indices in itertools.combinations(range(N), r):
            label = "".join(str(i + 1) for i in indices)
            out[label] = det_fraction(submatrix_fraction(a, list(indices)))
    return out


def sylvester_packet(name: str, a: list[list[F]]) -> dict[str, Any]:
    leading = leading_sylvester(a)
    all_minors = all_principal_minors(a)
    return {
        "name": name,
        "leading_sylvester": [rat_text(x) for x in leading],
        "leading_sylvester_parts": [rat_parts(x) for x in leading],
        "all_principal_minors": {k: rat_text(v) for k, v in all_minors.items()},
        "strict_positive_leading": all(x > 0 for x in leading),
        "strict_positive_all_principal": all(x > 0 for x in all_minors.values()),
    }


def require_strict_positive_packet(packet: dict[str, Any]) -> None:
    if not packet["strict_positive_leading"]:
        raise AssertionError(f"{packet['name']} failed leading Sylvester positivity")
    if not packet["strict_positive_all_principal"]:
        raise AssertionError(f"{packet['name']} failed all-principal-minor positivity")


def decimal_to_fraction(text: str) -> F:
    s = text.strip()
    sign = -1 if s.startswith("-") else 1
    if s[0] in "+-":
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
        digits = whole + frac
        den = 10 ** len(frac)
    else:
        digits = s
        den = 1
    num = int(digits) if digits else 0
    return F(sign * num, den)


def floor_decimal(q: F, places: int) -> str:
    scale = 10 ** places
    n = q.numerator * scale // q.denominator
    return scaled_decimal(n, places)


def ceil_decimal(q: F, places: int) -> str:
    scale = 10 ** places
    n = -((-q.numerator * scale) // q.denominator)
    return scaled_decimal(n, places)


def scaled_decimal(n: int, places: int) -> str:
    sign = "-" if n < 0 else ""
    n = abs(n)
    scale = 10 ** places
    whole = n // scale
    frac = n % scale
    if places == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{frac:0{places}d}"


def interval_json(iv: Iv, places: int) -> dict[str, Any]:
    return {
        "lower": rat_parts(iv.lo),
        "upper": rat_parts(iv.hi),
        "width": rat_parts(iv.width()),
        "lower_text": rat_text(iv.lo),
        "upper_text": rat_text(iv.hi),
        "width_text": rat_text(iv.width()),
        "decimal_outward": {
            "places": str(places),
            "lower": floor_decimal(iv.lo, places),
            "upper": ceil_decimal(iv.hi, places),
        },
    }


def poly_json(p: Poly) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for (e, d), coeff in sorted(p.items()):
        rows.append(
            {
                "epsilon_degree": str(e),
                "delta_degree": str(d),
                "monomial": f"epsilon^{e}*delta^{d}",
                "coefficient": rat_text(coeff),
                "coefficient_numerator": str(coeff.numerator),
                "coefficient_denominator": str(coeff.denominator),
            }
        )
    return rows


def matrix_json(a: list[list[F]]) -> list[list[str]]:
    return [[rat_text(a[i][j]) for j in range(N)] for i in range(N)]


def check_no_float_atoms(x: Any, path: str = "$") -> None:
    if isinstance(x, float):
        raise TypeError(f"float atom at {path}")
    if isinstance(x, dict):
        for k, v in x.items():
            check_no_float_atoms(k, f"{path}.<key>")
            check_no_float_atoms(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            check_no_float_atoms(v, f"{path}[{i}]")
    elif isinstance(x, tuple):
        for i, v in enumerate(x):
            check_no_float_atoms(v, f"{path}[{i}]")


class Checkpointer:
    def __init__(self, out_arg: Path, input_root: Path, wall_seconds: int) -> None:
        if wall_seconds > 600:
            raise ValueError("--wall-seconds must not exceed the 600 second contract")
        self.start_epoch_ns = time.time_ns()
        self.deadline_epoch_ns = self.start_epoch_ns + wall_seconds * 1_000_000_000
        env_deadline = os.environ.get("C2_ABSOLUTE_DEADLINE_EPOCH")
        self.env_deadline_epoch = env_deadline
        if env_deadline:
            env_ns = int(Decimal(env_deadline) * Decimal(1_000_000_000))
            if env_ns < self.deadline_epoch_ns:
                self.deadline_epoch_ns = env_ns
        if out_arg.suffix.lower() == ".json":
            self.final_path = out_arg
            self.out_dir = out_arg.parent / f"{out_arg.stem}_checkpoints"
        else:
            self.out_dir = out_arg
            self.final_path = out_arg / "certificate.json"
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.final_path.parent.mkdir(parents=True, exist_ok=True)
        self.input_root = input_root
        self.wall_seconds = wall_seconds

    def check_deadline(self, label: str) -> None:
        if time.time_ns() >= self.deadline_epoch_ns:
            raise DeadlineExceeded(f"deadline reached before {label}")

    def base(self) -> dict[str, str]:
        return {
            "start_epoch_ns": str(self.start_epoch_ns),
            "deadline_epoch_ns": str(self.deadline_epoch_ns),
            "env_C2_ABSOLUTE_DEADLINE_EPOCH": self.env_deadline_epoch or "",
            "wall_seconds_requested": str(self.wall_seconds),
            "input_root": str(self.input_root),
        }

    def write(self, name: str, payload: dict[str, Any]) -> None:
        packet: dict[str, Any] = {
            "checkpoint": name,
            "checkpoint_epoch_ns": str(time.time_ns()),
            "run": self.base(),
            "payload": payload,
        }
        check_no_float_atoms(packet)
        path = self.out_dir / f"{name}.json"
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)

    def write_final(self, payload: dict[str, Any]) -> None:
        packet = dict(payload)
        packet["run"] = self.base()
        packet["completed_epoch_ns"] = str(time.time_ns())
        check_no_float_atoms(packet)
        tmp = self.final_path.with_suffix(self.final_path.suffix + ".tmp")
        tmp.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, self.final_path)


def resolve_inputs(input_root: Path) -> tuple[Path, Path, dict[str, Any]]:
    root = input_root.resolve()
    if (root / "inputs").is_dir():
        prefix = root
        inputs = root / "inputs"
    elif (root / "REQUEST.md").is_file() and (root / "continuation.md").is_file():
        prefix = root.parent
        inputs = root
    else:
        raise FileNotFoundError("input root must be pr60_aux52/ or pr60_aux52/inputs/")

    request_text = (inputs / "REQUEST.md").read_text(encoding="utf-8")
    continuation_text = (inputs / "continuation.md").read_text(encoding="utf-8")
    binding_path = inputs / "SOURCE_BINDING.json"
    binding: dict[str, Any] = {}
    if binding_path.is_file():
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
    required_snippets = [
        "f869fd251c0d6fdad737b6d5efa287307795a87d",
        "442775/434223",
        "65729622186464/3466472577089",
        "0.09085487822146532947682573934164664",
        "0.00000000000454275478584750276044882",
        "1/100000",
    ]
    combined = request_text + "\n" + continuation_text
    missing = [s for s in required_snippets if s not in combined]
    if missing:
        raise AssertionError(f"input snippets missing: {missing}")
    return prefix, inputs, {
        "prefix": str(prefix),
        "inputs": str(inputs),
        "source_binding": binding,
        "request_issue_comment": "5604536353",
        "claim_issue_comment": "5604627611",
        "forbidden_reference_path": str(inputs / "continuation_exact_reference.py"),
        "forbidden_reference_not_imported_or_executed": True,
        "construction_source": "literal rational matrices in this source, with input text used only for frozen target checks",
    }


def build_matrices() -> tuple[list[list[F]], list[list[F]], list[list[F]], F]:
    k = [
        [rat(11, 100), rat(0), rat(33, 500)],
        [rat(0), rat(1, 200), rat(3, 1000)],
        [rat(33, 500), rat(3, 1000), rat(199, 200)],
    ]
    d = [
        [rat(0), rat(-1), rat(0)],
        [rat(-1), rat(-1, 50), rat(2, 25)],
        [rat(0), rat(2, 25), rat(0)],
    ]
    c = [[k[i][j] if i != j else rat(0) for j in range(N)] for i in range(N)]
    h = rat(1, 100000)
    return k, d, c, h


def build_event_polynomials(k: list[list[F]], d: list[list[F]], c: list[list[F]]) -> tuple[list[Poly], list[dict[str, F]]]:
    aff = matrix_poly(k, d, c)
    signed: list[Poly] = []
    inclusion: list[Poly] = []
    for mask in range(8):
        ps = event_poly_signed(mask, aff)
        pi = event_poly_inclusion(mask, aff)
        if ps != pi:
            raise AssertionError(f"signed determinant and inclusion-exclusion differ for mask {mask}: {ps} != {pi}")
        signed.append(ps)
        inclusion.append(pi)
    total: Poly = {}
    for p in signed:
        total = poly_add(total, p)
    if total != {(0, 0): F(1)}:
        raise AssertionError(f"event polynomial normalization failed: {total}")
    jets = [jet(p) for p in signed]
    return signed, jets


def event_vector_from_matrix(mat0: list[list[F]]) -> list[F]:
    out: list[F] = []
    for mask in range(8):
        ps = event_prob_signed(mask, mat0)
        pi = event_prob_inclusion(mask, mat0)
        if ps != pi:
            raise AssertionError(f"numeric event formulas differ for mask {mask}: {ps} != {pi}")
        out.append(ps)
    if sum(out, F(0)) != F(1):
        raise AssertionError(f"numeric event law does not sum to 1: {sum(out, F(0))}")
    return out


def radial_legality(k: list[list[F]], c: list[list[F]]) -> dict[str, Any]:
    x = k[0][0]
    y = k[1][1]
    z = k[2][2]
    b0 = k[0][2]
    c0 = k[1][2]
    k_bound = z / (b0 * b0 / x + c0 * c0 / y)
    i_bound = (F(1) - z) / (b0 * b0 / (F(1) - x) + c0 * c0 / (F(1) - y))
    exact_bound = min(k_bound, i_bound)
    expected = F(442775, 434223)
    if exact_bound != expected:
        raise AssertionError(f"radial legality bound mismatch: {exact_bound} != {expected}")
    diag = diag_part(k)

    def radial_kernel(s: F) -> list[list[F]]:
        return mat_add(diag, c, s)

    endpoints = [F(999, 1000), F(1001, 1000)]
    endpoint_packets = []
    for s in endpoints:
        if s * s >= exact_bound:
            raise AssertionError(f"radial endpoint {s} outside strict bound {exact_bound}")
        ks = radial_kernel(s)
        k_packet = sylvester_packet(f"K_radial_{rat_text(s)}", ks)
        ik_packet = sylvester_packet(f"I_minus_K_radial_{rat_text(s)}", complement(ks))
        require_strict_positive_packet(k_packet)
        require_strict_positive_packet(ik_packet)
        endpoint_packets.append(
            {
                "s": rat_text(s),
                "s_squared": rat_text(s * s),
                "K": k_packet,
                "I_minus_K": ik_packet,
            }
        )
    return {
        "kernel_bound_s_squared": rat_text(k_bound),
        "complement_bound_s_squared": rat_text(i_bound),
        "complete_bound_s_squared": rat_text(exact_bound),
        "complete_bound_parts": rat_parts(exact_bound),
        "matches_442775_over_434223": exact_bound == expected,
        "contains_999_1000_to_1001_1000": all(s * s < exact_bound for s in endpoints),
        "endpoint_checks": endpoint_packets,
    }


def lambda_ratio(p: list[F]) -> F:
    return p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6])


def interval_sum(parts: list[Iv]) -> Iv:
    out = Iv(F(0), F(0))
    for part in parts:
        out = out + part
    return out


def radial_derivative_certificate(jets: list[dict[str, F]], logs: LogEngine, places: int) -> dict[str, Any]:
    expected_r = F(
        62198092976944951510582016487593946984085346423771060505,
        1445745402739430543847620534728498621094597199216967098368,
    )
    expected_log_coeff = F(-66, 3125)
    signs = [-1, 1, 1, -1, 1, -1, -1, 1]
    rational_terms: list[F] = []
    log_terms: list[Iv] = []
    events: list[dict[str, Any]] = []
    for mask, j in enumerate(jets):
        p = j["p"]
        a = j["pD"]
        b = j["pDD"]
        c = j["pC"]
        f = j["pDC"]
        g = j["pDDC"]
        if p <= 0:
            raise AssertionError(f"nonpositive base atom for mask {mask}: {p}")
        term_2af = F(2) * a * f / p
        term_a2c = -(a * a * c) / (p * p)
        term_bc = b * c / p
        rational = term_2af + term_a2c + term_bc
        rational_terms.append(rational)
        log_iv = logs.log(p)
        log_term = log_iv.scale(g)
        log_terms.append(log_term)
        events.append(
            {
                "mask": str(mask),
                "label": MASK_LABELS[mask],
                "p": rat_text(p),
                "pD": rat_text(a),
                "pDD": rat_text(b),
                "pC": rat_text(c),
                "pDC": rat_text(f),
                "pDDC": rat_text(g),
                "term_2_pD_pDC_over_p": rat_text(term_2af),
                "term_minus_pD_squared_pC_over_p_squared": rat_text(term_a2c),
                "term_pDD_pC_over_p": rat_text(term_bc),
                "rational_part": rat_text(rational),
                "log_coefficient": rat_text(g),
                "log_p_interval": interval_json(log_iv, places),
                "log_contribution_interval": interval_json(log_term, places),
            }
        )
    rational_sum = sum(rational_terms, F(0))
    if rational_sum != expected_r:
        raise AssertionError(f"R mismatch: {rational_sum} != {expected_r}")
    for mask, j in enumerate(jets):
        expected_g = expected_log_coeff * F(signs[mask])
        if j["pDDC"] != expected_g:
            raise AssertionError(f"log cube coefficient mismatch at mask {mask}: {j['pDDC']} != {expected_g}")
    total = iv_point(rational_sum) + interval_sum(log_terms)
    display = Iv(
        decimal_to_fraction("-0.01912227459137764707182987490765265"),
        decimal_to_fraction("-0.01912227459137764707182987490765264"),
    )
    if not (display.lo <= total.lo <= total.hi <= display.hi):
        raise AssertionError(f"radial derivative interval not within displayed (33): {total} vs {display}")
    if not total.hi < 0:
        raise AssertionError(f"radial derivative was not strictly negative: {total}")
    return {
        "formula": "sum[2 pD pDC/p - pD^2 pC/p^2 + pDDC log(p) + pDD pC/p]",
        "rational_R": rat_text(rational_sum),
        "rational_R_parts": rat_parts(rational_sum),
        "expected_R_matched": True,
        "lambda_log_coefficient": rat_text(expected_log_coeff),
        "logcube_coefficient_identity": "pDDC = (-66/3125)*[-1,+1,+1,-1,+1,-1,-1,+1] in mask order",
        "all_event_contributions": events,
        "interval": interval_json(total, places),
        "display_33": {
            "lower": "-0.01912227459137764707182987490765265",
            "upper": "-0.01912227459137764707182987490765264",
            "contains_independent_interval": True,
        },
        "strictly_negative": total.hi < 0,
    }


def true_curvature_certificate(jets: list[dict[str, F]], logs: LogEngine, places: int) -> dict[str, Any]:
    fisher_terms: list[F] = []
    log_terms: list[Iv] = []
    events: list[dict[str, Any]] = []
    for mask, j in enumerate(jets):
        p = j["p"]
        a = j["pD"]
        b = j["pDD"]
        fisher = a * a / p
        log_iv = logs.log(p)
        log_term = log_iv.scale(b)
        fisher_terms.append(fisher)
        log_terms.append(log_term)
        events.append(
            {
                "mask": str(mask),
                "label": MASK_LABELS[mask],
                "p": rat_text(p),
                "pD": rat_text(a),
                "pDD": rat_text(b),
                "fisher_pD_squared_over_p": rat_text(fisher),
                "log_coefficient_pDD": rat_text(b),
                "log_p_interval": interval_json(log_iv, places),
                "log_contribution_interval": interval_json(log_term, places),
            }
        )
    fisher_sum = sum(fisher_terms, F(0))
    total = iv_point(fisher_sum) + interval_sum(log_terms)
    display = Iv(
        decimal_to_fraction("0.09085487822146532947682573934164664"),
        decimal_to_fraction("0.09085487822146532947682573934164665"),
    )
    if not (display.lo <= total.lo <= total.hi <= display.hi):
        raise AssertionError(f"true curvature interval not within displayed (35): {total} vs {display}")
    if not total.lo > 0:
        raise AssertionError(f"true curvature was not strictly positive: {total}")
    return {
        "formula": "sum[pD^2/p + pDD log(p)]",
        "fisher_sum": rat_text(fisher_sum),
        "fisher_sum_parts": rat_parts(fisher_sum),
        "all_event_contributions": events,
        "interval": interval_json(total, places),
        "display_35": {
            "lower": "0.09085487822146532947682573934164664",
            "upper": "0.09085487822146532947682573934164665",
            "contains_independent_interval": True,
        },
        "strictly_positive": total.lo > 0,
    }


def entropy_interval(probabilities: list[F], logs: LogEngine, places: int) -> tuple[Iv, list[dict[str, Any]]]:
    parts: list[Iv] = []
    rows: list[dict[str, Any]] = []
    for mask, p in enumerate(probabilities):
        if p <= 0:
            raise AssertionError(f"entropy atom is nonpositive for mask {mask}: {p}")
        log_iv = logs.log(p)
        contribution = log_iv.scale(-p)
        parts.append(contribution)
        rows.append(
            {
                "mask": str(mask),
                "label": MASK_LABELS[mask],
                "p": rat_text(p),
                "log_p_interval": interval_json(log_iv, places),
                "minus_p_log_p_interval": interval_json(contribution, places),
            }
        )
    return interval_sum(parts), rows


def jensen_certificate(
    k: list[list[F]],
    d: list[list[F]],
    h: F,
    event_polys: list[Poly],
    logs: LogEngine,
    places: int,
) -> dict[str, Any]:
    k_plus = mat_add(k, d, h)
    k_minus = mat_add(k, d, -h)
    p0 = [poly_eval(p, F(0), F(0)) for p in event_polys]
    p_plus_poly = [poly_eval(p, h, F(0)) for p in event_polys]
    p_minus_poly = [poly_eval(p, -h, F(0)) for p in event_polys]
    p_plus_direct = event_vector_from_matrix(k_plus)
    p_minus_direct = event_vector_from_matrix(k_minus)
    if p_plus_poly != p_plus_direct:
        raise AssertionError("K+hD event law differs between polynomial and direct determinant")
    if p_minus_poly != p_minus_direct:
        raise AssertionError("K-hD event law differs between polynomial and direct determinant")
    h0, h0_rows = entropy_interval(p0, logs, places)
    hp, hp_rows = entropy_interval(p_plus_poly, logs, places)
    hm, hm_rows = entropy_interval(p_minus_poly, logs, places)
    jensen = (hp + hm).scale(F(1, 2)) - h0
    kernel_checks = [
        sylvester_packet("K_minus_hD", k_minus),
        sylvester_packet("I_minus_K_minus_hD", complement(k_minus)),
        sylvester_packet("K_base", k),
        sylvester_packet("I_minus_K_base", complement(k)),
        sylvester_packet("K_plus_hD", k_plus),
        sylvester_packet("I_minus_K_plus_hD", complement(k_plus)),
    ]
    for packet in kernel_checks:
        require_strict_positive_packet(packet)
    display = Iv(
        decimal_to_fraction("-0.00000000000454275478584750276044882"),
        decimal_to_fraction("-0.00000000000454275478584750276044881"),
    )
    if not (display.lo <= jensen.lo <= jensen.hi <= display.hi):
        raise AssertionError(f"Jensen interval not within displayed (36): {jensen} vs {display}")
    if not jensen.hi < 0:
        raise AssertionError(f"Jensen gap was not strictly negative: {jensen}")
    return {
        "h": rat_text(h),
        "kernel_checks": kernel_checks,
        "event_probabilities": {
            "K_minus_hD": [rat_text(x) for x in p_minus_poly],
            "K_base": [rat_text(x) for x in p0],
            "K_plus_hD": [rat_text(x) for x in p_plus_poly],
        },
        "entropy_intervals": {
            "K_minus_hD": interval_json(hm, places),
            "K_base": interval_json(h0, places),
            "K_plus_hD": interval_json(hp, places),
        },
        "entropy_event_contributions": {
            "K_minus_hD": hm_rows,
            "K_base": h0_rows,
            "K_plus_hD": hp_rows,
        },
        "jensen_interval": interval_json(jensen, places),
        "display_36": {
            "lower": "-0.00000000000454275478584750276044882",
            "upper": "-0.00000000000454275478584750276044881",
            "contains_independent_interval": True,
        },
        "strictly_negative": jensen.hi < 0,
    }


def base_probability_certificate(k: list[list[F]], event_polys: list[Poly]) -> dict[str, Any]:
    expected = [
        F(1069, 12500000),
        F(61006, 12500000),
        F(106, 12500000),
        F(319, 12500000),
        F(11068306, 12500000),
        F(1307119, 12500000),
        F(55519, 12500000),
        F(6556, 12500000),
    ]
    from_polys = [poly_eval(p, F(0), F(0)) for p in event_polys]
    direct = event_vector_from_matrix(k)
    if from_polys != direct:
        raise AssertionError("base event law differs between polynomial and direct determinant")
    if from_polys != expected:
        raise AssertionError(f"base event vector mismatch: {from_polys} != {expected}")
    ratio = lambda_ratio(from_polys)
    expected_ratio = F(65729622186464, 3466472577089)
    if ratio != expected_ratio:
        raise AssertionError(f"exp(Lambda) mismatch: {ratio} != {expected_ratio}")
    if not ratio > 1:
        raise AssertionError(f"exp(Lambda) was not greater than one: {ratio}")
    return {
        "mask_order": MASK_LABELS,
        "probabilities": [rat_text(x) for x in from_polys],
        "probability_parts": [rat_parts(x) for x in from_polys],
        "matches_displayed_vector": True,
        "sum": rat_text(sum(from_polys, F(0))),
        "exp_Lambda": rat_text(ratio),
        "exp_Lambda_parts": rat_parts(ratio),
        "exp_Lambda_displayed_match": True,
        "exp_Lambda_greater_than_one": ratio > 1,
        "exp_Lambda_formula": "p123*p1*p2*p3/(p0*p12*p13*p23) in mask order 0,1,2,12,3,13,23,123",
    }


def build_certificate(input_root: Path, out_arg: Path, wall_seconds: int, terms: int, places: int) -> dict[str, Any]:
    cp = Checkpointer(out_arg, input_root, wall_seconds)
    cp.write("00_start", {"status": "starting", "terms": str(terms), "decimal_places": str(places)})

    cp.check_deadline("input resolution")
    prefix, inputs, input_meta = resolve_inputs(input_root)
    cp.write("01_inputs_resolved", {"status": "done", "input_meta": input_meta})

    cp.check_deadline("matrix construction")
    k, d, c, h = build_matrices()
    matrices = {"K_star": matrix_json(k), "D_star": matrix_json(d), "C_star": matrix_json(c), "h": rat_text(h)}
    cp.write("02_matrices", {"status": "done", "matrices": matrices})

    cp.check_deadline("event polynomial construction")
    event_polys, jets = build_event_polynomials(k, d, c)
    polynomial_rows = [
        {
            "mask": str(mask),
            "label": MASK_LABELS[mask],
            "signed_determinant_polynomial": poly_json(event_polys[mask]),
            "jet": {name: rat_text(value) for name, value in jets[mask].items()},
        }
        for mask in range(8)
    ]
    cp.write("03_event_polynomials_and_jets", {"status": "done", "events": polynomial_rows})

    cp.check_deadline("base event law")
    base_events = base_probability_certificate(k, event_polys)
    cp.write("04_base_probability_and_lambda", {"status": "done", "base_events": base_events})

    cp.check_deadline("legality")
    k_star_packet = sylvester_packet("K_star", k)
    ik_star_packet = sylvester_packet("I_minus_K_star", complement(k))
    require_strict_positive_packet(k_star_packet)
    require_strict_positive_packet(ik_star_packet)
    legality = {
        "K_star": k_star_packet,
        "I_minus_K_star": ik_star_packet,
        "radial": radial_legality(k, c),
    }
    cp.write("05_legality", {"status": "done", "legality": legality})

    cp.check_deadline("log interval certificates")
    logs = LogEngine(terms)
    log_method = {
        "terms": str(terms),
        "tail": "0 <= log(y)-2*sum_{j=0}^{N-1} w^(2j+1)/(2j+1) <= 2*w^(2N+1)/((2N+1)*(1-w^2))",
        "range_reduction": "positive rational x = 2^k*y with 1 <= y < 2; negative k reverses k*log2 interval",
        "log2_interval": interval_json(logs.log2(), places),
    }
    cp.write("06_log_method", {"status": "done", "log_method": log_method})

    cp.check_deadline("radial derivative")
    radial = radial_derivative_certificate(jets, logs, places)
    cp.write("07_radial_derivative", {"status": "done", "radial": radial})

    cp.check_deadline("true curvature")
    curvature = true_curvature_certificate(jets, logs, places)
    cp.write("08_true_curvature", {"status": "done", "curvature": curvature})

    cp.check_deadline("Jensen gap")
    jensen = jensen_certificate(k, d, h, event_polys, logs, places)
    cp.write("09_jensen", {"status": "done", "jensen": jensen})

    certificate: dict[str, Any] = {
        "schema": "pr60_aux52_independent_certificate_v1",
        "status": "MACHINE_PASS",
        "scope": "auxiliary fixed-diagonal radial-method failure plus favorable true curvature and Jensen checks only",
        "not_claimed": [
            "entropy counterexample",
            "DPP entropy concavity refutation",
            "Lambda-zero M theorem refutation",
            "general Lambda-nonzero theorem",
            "novelty or theorem review",
        ],
        "input_meta": input_meta,
        "matrices": matrices,
        "event_polynomials_and_jets": polynomial_rows,
        "base_probability_and_lambda": base_events,
        "legality": legality,
        "log_method": log_method,
        "radial_derivative": radial,
        "true_negative_entropy_curvature": curvature,
        "complete_configuration_jensen_gap": jensen,
        "all_required_display_enclosures_contained": True,
        "float_atoms_rejected_before_json": True,
        "sympy": "not used",
    }
    cp.write_final(certificate)
    return certificate


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent exact PR60 auxiliary certificate")
    parser.add_argument("--input-root", required=True, help="Path to research/C2/pr60_aux52 or its inputs directory")
    parser.add_argument("--out", required=True, help="Output directory, or final .json path")
    parser.add_argument("--wall-seconds", type=int, default=600)
    parser.add_argument("--terms", type=int, default=80)
    parser.add_argument("--decimal-places", type=int, default=35)
    args = parser.parse_args()

    try:
        cert = build_certificate(
            input_root=Path(args.input_root),
            out_arg=Path(args.out),
            wall_seconds=args.wall_seconds,
            terms=args.terms,
            places=args.decimal_places,
        )
        final_path = Path(args.out)
        if final_path.suffix.lower() != ".json":
            final_path = final_path / "certificate.json"
        print(json.dumps({"status": cert["status"], "final": str(final_path)}, sort_keys=True))
        return 0
    except BaseException as exc:
        try:
            out_arg = Path(args.out)
            if out_arg.suffix.lower() == ".json":
                fail_path = out_arg.parent / f"{out_arg.stem}_failure.json"
            else:
                out_arg.mkdir(parents=True, exist_ok=True)
                fail_path = out_arg / "failure.json"
            packet = {
                "status": "MACHINE_FAIL",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "epoch_ns": str(time.time_ns()),
            }
            check_no_float_atoms(packet)
            tmp = fail_path.with_suffix(fail_path.suffix + ".tmp")
            tmp.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
            os.replace(tmp, fail_path)
        except BaseException:
            pass
        print(json.dumps({"status": "MACHINE_FAIL", "error_type": type(exc).__name__, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
