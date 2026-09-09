#!/usr/bin/env python3
"""Independent PR58 finite corridor and s=10 machine certificate.

This verifier is intentionally self-contained. It reconstructs the 64 complete
event determinant polynomials directly from the displayed rational matrices in
RESULT.md, then derives every later quantity from those polynomials.

It does not import, read, or execute author_checker_reference.py.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import os
import re
import sys
import tempfile
import time
import traceback
from fractions import Fraction
from pathlib import Path


try:
    sys.set_int_max_str_digits(0)
    INT_STR_DIGITS = "disabled"
except AttributeError:
    INT_STR_DIGITS = "unavailable_before_python_3_11"


for _thread_var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ[_thread_var] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""


EXPECTED_SOURCE_COMMIT = "1770ed29e8487b8f39aebb4c9466406c7493e580"
PUBLIC_CLAIM = "https://github.com/randomcat4/dpp-entropy-tools/issues/50#issuecomment-5604628245"
EXCLUDED_SCOPE = (
    "a4f05cc joint-additive fixture",
    "different s=9/10 fixture",
    "issue63 whole-chord task",
)
INTERVALS = [(3, 9), (8, 12), (11, 14), (14, 15)]
S10 = 10
DEFAULT_LOG_TERMS = 80
MAX_WALL_SECONDS = 2700
DECIMAL_DIGITS = 90
W_WIDTH_TARGET = "5.83e-83"
CURVATURE_WIDTH_TARGET = "8.71e-79"
CURVATURE_LOWER_TARGET = "0.17037745196806863130550498470533808479721333392335"
EXPECTED_S10_Q_MIN = Fraction(121400093597, 249280204050)
FORBIDDEN_MODULE_PREFIXES = ("sympy", "numpy", "scipy", "mpmath")


class CertificateFailure(Exception):
    pass


class DeadlineExceeded(CertificateFailure):
    pass


def fail(message: str) -> None:
    raise CertificateFailure(message)


def reject_forbidden_modules() -> None:
    loaded = []
    for name in sys.modules:
        for prefix in FORBIDDEN_MODULE_PREFIXES:
            if name == prefix or name.startswith(prefix + "."):
                loaded.append(name)
    if loaded:
        fail("forbidden CAS/numeric module loaded: " + ", ".join(sorted(loaded)))


def parse_decimal_fraction(text: str) -> Fraction:
    s = text.strip().lower()
    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if "e" in s:
        mantissa, exponent_text = s.split("e", 1)
        exponent = int(exponent_text)
    else:
        mantissa = s
        exponent = 0
    if "." in mantissa:
        whole, frac = mantissa.split(".", 1)
    else:
        whole, frac = mantissa, ""
    digits = (whole + frac).lstrip("0") or "0"
    denominator_power = len(frac) - exponent
    numerator = sign * int(digits)
    if denominator_power >= 0:
        return Fraction(numerator, 10**denominator_power)
    return Fraction(numerator * (10 ** (-denominator_power)), 1)


def floor_scaled(x: Fraction, digits: int) -> int:
    scale = 10**digits
    return (x.numerator * scale) // x.denominator


def ceil_scaled(x: Fraction, digits: int) -> int:
    scale = 10**digits
    return -((-x.numerator * scale) // x.denominator)


def scaled_int_to_decimal(value: int, digits: int) -> str:
    sign = "-" if value < 0 else ""
    n = abs(value)
    scale = 10**digits
    whole = n // scale
    frac = n % scale
    if digits == 0:
        return sign + str(whole)
    return sign + str(whole) + "." + str(frac).zfill(digits)


def outward_decimal_lower(x: Fraction, digits: int = DECIMAL_DIGITS) -> str:
    return scaled_int_to_decimal(floor_scaled(x, digits), digits)


def outward_decimal_upper(x: Fraction, digits: int = DECIMAL_DIGITS) -> str:
    return scaled_int_to_decimal(ceil_scaled(x, digits), digits)


def fraction_json(x: Fraction) -> dict[str, str]:
    if not isinstance(x, Fraction):
        fail("internal non-Fraction reached fraction_json")
    return {"num": str(x.numerator), "den": str(x.denominator)}


def fraction_value_json(x: Fraction) -> dict[str, object]:
    return {
        "fraction": fraction_json(x),
        "decimal_floor": outward_decimal_lower(x),
        "decimal_ceiling": outward_decimal_upper(x),
    }


def interval_json(lo: Fraction, hi: Fraction) -> dict[str, object]:
    if lo > hi:
        fail("invalid interval with lower endpoint above upper endpoint")
    return {
        "lower": fraction_json(lo),
        "upper": fraction_json(hi),
        "lower_outward_decimal": outward_decimal_lower(lo),
        "upper_outward_decimal": outward_decimal_upper(hi),
        "width": fraction_json(hi - lo),
        "width_decimal_ceiling": outward_decimal_upper(hi - lo),
    }


def assert_json_safe(value: object, path: str = "$") -> None:
    if isinstance(value, float):
        fail("float value reached JSON output at " + path)
    if isinstance(value, Fraction):
        fail("raw Fraction reached JSON output at " + path)
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                fail("non-string JSON key at " + path)
            assert_json_safe(child, path + "." + key)
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            assert_json_safe(child, path + "[" + str(index) + "]")
    elif value is None or isinstance(value, (str, int, bool)):
        return
    else:
        fail("unsupported JSON value at " + path + ": " + type(value).__name__)


def atomic_write_json(path: Path, value: object) -> None:
    assert_json_safe(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(value, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


class Deadline:
    def __init__(self, requested_wall_seconds: int) -> None:
        if requested_wall_seconds <= 0:
            fail("--wall-seconds must be positive")
        self.requested_wall_seconds = requested_wall_seconds
        self.used_wall_seconds = min(requested_wall_seconds, MAX_WALL_SECONDS)
        self.start_epoch_ns = time.time_ns()
        wall_deadline = self.start_epoch_ns + self.used_wall_seconds * 1_000_000_000
        env_text = os.environ.get("C2_ABSOLUTE_DEADLINE_EPOCH")
        self.env_deadline_epoch = env_text
        self.deadline_epoch_ns = wall_deadline
        if env_text:
            env_fraction = parse_decimal_fraction(env_text)
            env_ns = (env_fraction.numerator * 1_000_000_000) // env_fraction.denominator
            self.deadline_epoch_ns = min(self.deadline_epoch_ns, env_ns)

    def check(self, stage: str) -> None:
        if time.time_ns() > self.deadline_epoch_ns:
            raise DeadlineExceeded("deadline exceeded during " + stage)

    def json(self) -> dict[str, object]:
        return {
            "requested_wall_seconds": self.requested_wall_seconds,
            "used_wall_seconds_cap": self.used_wall_seconds,
            "start_epoch_ns": self.start_epoch_ns,
            "deadline_epoch_ns": self.deadline_epoch_ns,
            "env_C2_ABSOLUTE_DEADLINE_EPOCH": self.env_deadline_epoch,
        }


def poly_trim(poly: list[Fraction] | tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    if not out:
        return (Fraction(0),)
    return tuple(out)


def poly_const(x: Fraction | int) -> tuple[Fraction, ...]:
    return (Fraction(x),)


def poly_t_scaled(x: Fraction) -> tuple[Fraction, ...]:
    if x == 0:
        return (Fraction(0),)
    return (Fraction(0), x)


def poly_coeff(poly: tuple[Fraction, ...], degree: int) -> Fraction:
    if degree < len(poly):
        return poly[degree]
    return Fraction(0)


def poly_add(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(n):
        out[i] = poly_coeff(a, i) + poly_coeff(b, i)
    return poly_trim(out)


def poly_neg(a: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return poly_trim([-x for x in a])


def poly_sub(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return poly_add(a, poly_neg(b))


def poly_mul(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj != 0:
                out[i + j] += ai * bj
    return poly_trim(out)


def poly_scale(a: tuple[Fraction, ...], c: Fraction) -> tuple[Fraction, ...]:
    return poly_trim([x * c for x in a])


def poly_json(poly: tuple[Fraction, ...]) -> list[dict[str, object]]:
    return [
        {"degree": degree, "coeff": fraction_json(coeff)}
        for degree, coeff in enumerate(poly)
        if coeff != 0
    ]


_SIGNED_PERMS: dict[int, list[tuple[tuple[int, ...], int]]] = {}


def permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def signed_permutations(n: int) -> list[tuple[tuple[int, ...], int]]:
    if n not in _SIGNED_PERMS:
        _SIGNED_PERMS[n] = [(perm, permutation_sign(perm)) for perm in itertools.permutations(range(n))]
    return _SIGNED_PERMS[n]


def det_poly(matrix: list[list[tuple[Fraction, ...]]]) -> tuple[Fraction, ...]:
    n = len(matrix)
    if n == 0:
        return (Fraction(1),)
    total = (Fraction(0),)
    for perm, sign in signed_permutations(n):
        term = (Fraction(1),)
        for i, j in enumerate(perm):
            term = poly_mul(term, matrix[i][j])
            if term == (Fraction(0),):
                break
        if sign == 1:
            total = poly_add(total, term)
        else:
            total = poly_sub(total, term)
    return total


def det_fraction(matrix: list[list[Fraction]]) -> Fraction:
    as_poly = [[(entry,) for entry in row] for row in matrix]
    det = det_poly(as_poly)
    if len(det) != 1:
        fail("constant determinant unexpectedly has nonconstant terms")
    return det[0]


def mat_transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def mat_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    out = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            aik = a[i][k]
            if aik == 0:
                continue
            for j in range(cols):
                out[i][j] += aik * b[k][j]
    return out


def mat_trace(a: list[list[Fraction]]) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def mat_eye(n: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def mat_diag(values: list[Fraction]) -> list[list[Fraction]]:
    return [[values[i] if i == j else Fraction(0) for j in range(len(values))] for i in range(len(values))]


def mat_inv(a: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    aug = [list(row) + eye_row for row, eye_row in zip(a, mat_eye(n))]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            fail("singular 3x3 event block in posthoc resolvent check")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_value = aug[col][col]
        aug[col] = [x / pivot_value for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0:
                continue
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def matrix_rank(a: list[list[Fraction]]) -> int:
    work = [list(row) for row in a]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if work[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][col]
        work[rank] = [x / pivot_value for x in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][col]
            if factor != 0:
                work[row] = [x - factor * y for x, y in zip(work[row], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


class FractionAst(ast.NodeVisitor):
    def visit_Expression(self, node: ast.Expression) -> object:
        return self.visit(node.body)

    def visit_List(self, node: ast.List) -> list[object]:
        return [self.visit(child) for child in node.elts]

    def visit_Constant(self, node: ast.Constant) -> Fraction:
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            return Fraction(node.value)
        fail("matrix literal contains non-integer constant")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Fraction:
        value = self.visit(node.operand)
        if not isinstance(value, Fraction):
            fail("unary operator applied to non-scalar matrix literal")
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
        fail("matrix literal contains unsupported unary operator")

    def visit_BinOp(self, node: ast.BinOp) -> Fraction:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if not isinstance(left, Fraction) or not isinstance(right, Fraction):
            fail("binary operator applied to non-scalar matrix literal")
        if isinstance(node.op, ast.Div):
            if right == 0:
                fail("matrix literal contains division by zero")
            return left / right
        fail("matrix literal contains unsupported binary operator")

    def generic_visit(self, node: ast.AST) -> object:
        fail("matrix literal contains unsupported syntax " + type(node).__name__)


def parse_matrix_literal(text: str) -> list[list[Fraction]]:
    parsed = FractionAst().visit(ast.parse(text, mode="eval"))
    if not isinstance(parsed, list) or not parsed:
        fail("matrix literal is not a nonempty list")
    matrix: list[list[Fraction]] = []
    width = None
    for row in parsed:
        if not isinstance(row, list) or not row:
            fail("matrix literal row is invalid")
        out_row = []
        for value in row:
            if not isinstance(value, Fraction):
                fail("matrix literal value is not a Fraction")
            out_row.append(value)
        if width is None:
            width = len(out_row)
        elif len(out_row) != width:
            fail("matrix literal is not rectangular")
        matrix.append(out_row)
    return matrix


def extract_section(text: str, start_heading: str, end_heading: str) -> str:
    start = text.find(start_heading)
    if start < 0:
        fail("missing section " + start_heading)
    end = text.find(end_heading, start + len(start_heading))
    if end < 0:
        fail("missing section boundary " + end_heading)
    return text[start:end]


def extract_named_matrix(section: str, name: str) -> list[list[Fraction]]:
    match = re.search(r"\b" + re.escape(name) + r"\s*=\s*(\[\[.*?\]\])", section, re.DOTALL)
    if not match:
        fail("missing displayed matrix " + name + " in RESULT section 4")
    return parse_matrix_literal(match.group(1))


def matrix_json(matrix: list[list[Fraction]]) -> list[list[dict[str, str]]]:
    return [[fraction_json(value) for value in row] for row in matrix]


def build_b_from_u_vt(u: list[list[Fraction]], v: list[list[Fraction]]) -> list[list[Fraction]]:
    if len(u) != 3 or len(v) != 3 or len(u[0]) != 2 or len(v[0]) != 2:
        fail("U and V dimensions are not 3x2")
    vt = mat_transpose(v)
    return mat_mul(u, vt)


def complete_event_matrix_fraction(kernel: list[list[Fraction]], mask: int) -> list[list[Fraction]]:
    n = len(kernel)
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if mask & (1 << j):
                out[i][j] = kernel[i][j]
            else:
                out[i][j] = Fraction(1 if i == j else 0) - kernel[i][j]
    return out


def complete_event_matrix_poly(kernel: list[list[tuple[Fraction, ...]]], mask: int) -> list[list[tuple[Fraction, ...]]]:
    n = len(kernel)
    out = [[(Fraction(0),) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if mask & (1 << j):
                out[i][j] = kernel[i][j]
            else:
                out[i][j] = poly_sub(poly_const(1 if i == j else 0), kernel[i][j])
    return out


def build_kernel_poly(
    a: list[list[Fraction]], c: list[list[Fraction]], b: list[list[Fraction]]
) -> list[list[tuple[Fraction, ...]]]:
    kernel = [[(Fraction(0),) for _ in range(6)] for _ in range(6)]
    for i in range(3):
        for j in range(3):
            kernel[i][j] = poly_const(a[i][j])
            kernel[i + 3][j + 3] = poly_const(c[i][j])
            kernel[i][j + 3] = poly_t_scaled(b[i][j])
            kernel[j + 3][i] = poly_t_scaled(b[i][j])
    return kernel


def principal_submatrix_poly(
    kernel: list[list[tuple[Fraction, ...]]], indices: list[int]
) -> list[list[tuple[Fraction, ...]]]:
    return [[kernel[i][j] for j in indices] for i in indices]


def complementary_submatrix_poly(
    kernel: list[list[tuple[Fraction, ...]]], indices: list[int]
) -> list[list[tuple[Fraction, ...]]]:
    return [
        [poly_sub(poly_const(1 if i == j else 0), kernel[i][j]) for j in indices]
        for i in indices
    ]


def bit_string(mask: int, n: int) -> str:
    return "".join("1" if (mask & (1 << i)) else "0" for i in range(n))


def mask_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if mask & (1 << i)]


def event_block_matrix(kernel: list[list[Fraction]], mask: int) -> list[list[Fraction]]:
    return complete_event_matrix_fraction(kernel, mask)


def event_signs(mask: int, n: int) -> list[Fraction]:
    return [Fraction(1 if (mask & (1 << i)) else -1) for i in range(n)]


def posthoc_resolvent_ab(
    a_kernel: list[list[Fraction]],
    c_kernel: list[list[Fraction]],
    b_kernel: list[list[Fraction]],
    left_mask: int,
    right_mask: int,
) -> tuple[Fraction, Fraction]:
    a_event = event_block_matrix(a_kernel, left_mask)
    c_event = event_block_matrix(c_kernel, right_mask)
    inv_a = mat_inv(a_event)
    inv_c = mat_inv(c_event)
    d_left = mat_diag(event_signs(left_mask, 3))
    d_right = mat_diag(event_signs(right_mask, 3))
    bottom_left = mat_mul(mat_transpose(b_kernel), d_left)
    top_right = mat_mul(b_kernel, d_right)
    x = mat_mul(mat_mul(mat_mul(inv_c, bottom_left), inv_a), top_right)
    trace_x = mat_trace(x)
    trace_x2 = mat_trace(mat_mul(x, x))
    e2_x = (trace_x * trace_x - trace_x2) / 2
    return trace_x, e2_x


def q_value(a_coeff: Fraction, b_coeff: Fraction, s: Fraction) -> Fraction:
    return Fraction(1) - s * a_coeff + s * s * b_coeff


def quadratic_extrema(a_coeff: Fraction, b_coeff: Fraction, left: Fraction, right: Fraction) -> dict[str, object]:
    candidates = [left, right]
    if b_coeff != 0:
        vertex = a_coeff / (2 * b_coeff)
        if left <= vertex <= right:
            candidates.append(vertex)
    evaluations = []
    for s in candidates:
        evaluations.append((s, q_value(a_coeff, b_coeff, s)))
    min_s, min_q = min(evaluations, key=lambda item: item[1])
    max_s, max_q = max(evaluations, key=lambda item: item[1])
    return {
        "candidates": [(s, q) for s, q in evaluations],
        "min_s": min_s,
        "min_q": min_q,
        "max_s": max_s,
        "max_q": max_q,
    }


def interval_add(a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return a[0] + b[0], a[1] + b[1]


def interval_add_exact(a: tuple[Fraction, Fraction], x: Fraction) -> tuple[Fraction, Fraction]:
    return a[0] + x, a[1] + x


def interval_scale(c: Fraction, interval: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    lo, hi = interval
    if c >= 0:
        return c * lo, c * hi
    return c * hi, c * lo


def log_atanh_interval(q: Fraction, terms: int, store_terms: bool) -> dict[str, object]:
    if q <= 0:
        fail("log enclosure requested for nonpositive q")
    z = (q - 1) / (q + 1)
    z2 = z * z
    power = z
    total = Fraction(0)
    stored_terms: list[dict[str, str]] = []
    for k in range(terms):
        term = 2 * power / (2 * k + 1)
        total += term
        if store_terms:
            stored_terms.append(fraction_json(term))
        power *= z2
    abs_z = z if z >= 0 else -z
    if z2 >= 1:
        fail("atanh transform outside convergence radius")
    tail = 2 * (abs_z ** (2 * terms + 1)) / ((2 * terms + 1) * (1 - z2))
    if z > 0:
        lower = total
        upper = total + tail
        tail_mode = "one_sided_positive"
    elif z < 0:
        lower = total - tail
        upper = total
        tail_mode = "one_sided_negative"
    else:
        lower = total
        upper = total
        tail_mode = "exact_zero"
    return {
        "z": z,
        "series_sum": total,
        "tail_bound": tail,
        "tail_mode": tail_mode,
        "lower": lower,
        "upper": upper,
        "terms": stored_terms,
    }


def finite_fraction(text: str) -> Fraction:
    cleaned = text.replace(" ", "")
    if "/" in cleaned:
        num, den = cleaned.split("/", 1)
        return Fraction(int(num), int(den))
    return Fraction(int(cleaned), 1)


def normalize_reference_key(text: str) -> str:
    return re.sub(r"[^a-z0-9_\-\+\[\],]", "", text.lower())


def parse_reference_exact_fractions(text: str) -> dict[str, Fraction]:
    exacts: dict[str, Fraction] = {}
    current_interval = None
    interval_tokens = {"[" + str(l) + "," + str(r) + "]": "[" + str(l) + "," + str(r) + "]" for l, r in INTERVALS}
    fraction_re = r"(-?\d+(?:\s*/\s*\d+)?)"
    global_patterns = [
        (re.compile(r"^\s*Amax\s*=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "moments.Amax"),
        (re.compile(r"^\s*Bmax\s*=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "moments.Bmax"),
        (re.compile(r"^\s*s=10\s+min\s+q\s*=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "s10.q_min"),
    ]
    piece_pattern = re.compile(
        r"^\s*piece\s+(\d+)\s+(\d+)\s+qminus\s+"
        + fraction_re
        + r"\s+qplus\s+"
        + fraction_re
        + r"\s*$",
        re.IGNORECASE,
    )
    interval_patterns = [
        (re.compile(r"^\s*Psi\s*<=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "Psi"),
        (re.compile(r"^\s*M2\s*>=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "M2lower"),
        (re.compile(r"^\s*left\s*=\s*" + fraction_re + r"\s*$", re.IGNORECASE), "left"),
        (
            re.compile(r"^\s*squared\s+strict\s+margin\s*=\s*" + fraction_re + r"\s*$", re.IGNORECASE),
            "squared_margin",
        ),
    ]

    for line in text.splitlines():
        compact = line.replace(" ", "")
        for token, label in interval_tokens.items():
            if token in compact:
                current_interval = label
        piece = piece_pattern.match(line)
        if piece:
            current_interval = "[" + piece.group(1) + "," + piece.group(2) + "]"
            exacts["intervals." + current_interval + ".q_minus"] = finite_fraction(piece.group(3))
            exacts["intervals." + current_interval + ".q_plus"] = finite_fraction(piece.group(4))
            continue
        for pattern, target in global_patterns:
            match = pattern.match(line)
            if match:
                exacts[target] = finite_fraction(match.group(1))
        if current_interval is None:
            continue
        for pattern, short_key in interval_patterns:
            match = pattern.match(line)
            if match:
                exacts["intervals." + current_interval + "." + short_key] = finite_fraction(match.group(1))
    return exacts


def required_corridor_reference_keys() -> list[str]:
    keys = ["moments.Amax", "moments.Bmax"]
    for left, right in INTERVALS:
        label = "[" + str(left) + "," + str(right) + "]"
        for key in ("q_minus", "q_plus", "Psi", "M2lower", "left", "squared_margin"):
            keys.append("intervals." + label + "." + key)
    return keys


def required_reference_keys() -> list[str]:
    return required_corridor_reference_keys() + ["s10.q_min"]


def flatten_own_corridor_values(moments: dict[str, Fraction], intervals: list[dict[str, object]]) -> dict[str, Fraction]:
    out = {
        "moments.Ea2": moments["Ea2"],
        "moments.Eab": moments["Eab"],
        "moments.Eb2": moments["Eb2"],
        "moments.Amax": moments["Amax"],
        "moments.Bmax": moments["Bmax"],
    }
    for entry in intervals:
        label = entry["label"]
        if not isinstance(label, str):
            fail("internal interval label is not a string")
        for key in ("q_minus", "q_plus", "Psi", "M2lower", "left", "squared_margin"):
            value = entry[key]
            if not isinstance(value, Fraction):
                fail("internal interval value " + key + " is not a Fraction")
            out["intervals." + label + "." + key] = value
    return out


class CertificateRun:
    def __init__(self, input_root: Path, out_root: Path, deadline: Deadline, log_terms: int, store_log_terms: bool) -> None:
        self.input_root_arg = input_root
        self.inputs_dir = self.resolve_inputs_dir(input_root)
        self.out_root = out_root
        self.deadline = deadline
        self.log_terms = log_terms
        self.store_log_terms = store_log_terms
        self.completed_layers: list[str] = []
        self.failures: list[dict[str, object]] = []
        self.context: dict[str, object] = {}

    def resolve_inputs_dir(self, root: Path) -> Path:
        if (root / "RESULT.md").is_file():
            return root
        if (root / "inputs" / "RESULT.md").is_file():
            return root / "inputs"
        fail("--input-root must point either to inputs/ or to the PR58 packet root")

    def state(self, status: str = "RUNNING") -> dict[str, object]:
        return {
            "status": status,
            "completed_layers": list(self.completed_layers),
            "failures": list(self.failures),
            "deadline": self.deadline.json(),
            "resource_bound": {
                "processes": 1,
                "cpu_threads": 1,
                "memory_gib": 16,
                "gpu": False,
                "memory_note": "not_os_enforced_by_this_stdlib_script",
            },
            "int_string_conversion_limit": INT_STR_DIGITS,
            "forbidden_modules": list(FORBIDDEN_MODULE_PREFIXES),
            "source_commit": EXPECTED_SOURCE_COMMIT,
            "claim": PUBLIC_CLAIM,
            "excluded_scope": list(EXCLUDED_SCOPE),
        }

    def checkpoint(self, layer: str, value: object) -> None:
        reject_forbidden_modules()
        atomic_write_json(self.out_root / (layer + ".json"), value)
        if layer not in self.completed_layers:
            self.completed_layers.append(layer)
        atomic_write_json(self.out_root / "state.json", self.state())
        print("PROGRESS " + layer, flush=True)

    def run(self) -> None:
        self.out_root.mkdir(parents=True, exist_ok=True)
        atomic_write_json(self.out_root / "state.json", self.state())
        self.load_inputs()
        self.build_events()
        self.verify_identities()
        self.compute_corridor()
        self.compute_s10()
        self.compare_reference_output()
        final = self.state(status="MACHINE_PASS")
        final["pass_files"] = [
            "inputs.json",
            "events.json",
            "identities.json",
            "corridor.json",
            "s10.json",
            "reference_compare.json",
        ]
        atomic_write_json(self.out_root / "MACHINE_PASS.json", final)
        atomic_write_text(self.out_root / "MACHINE_PASS.txt", "MACHINE_PASS\n")
        atomic_write_json(self.out_root / "state.json", final)

    def load_inputs(self) -> None:
        self.deadline.check("load_inputs")
        binding_path = self.inputs_dir / "SOURCE_BINDING.json"
        result_path = self.inputs_dir / "RESULT.md"
        addendum_path = self.inputs_dir / "ADDENDUM_CONDITIONAL_CENTERING.md"
        checker_path = self.inputs_dir / "author_checker_reference.py"
        with binding_path.open("r", encoding="utf-8") as fh:
            binding = json.load(fh)
        if binding.get("source_commit") != EXPECTED_SOURCE_COMMIT:
            fail("SOURCE_BINDING source_commit does not match frozen PR58 commit")
        result_text = result_path.read_text(encoding="utf-8")
        addendum_text = addendum_path.read_text(encoding="utf-8")
        section4 = extract_section(result_text, "## 4.", "## 5.")
        a_kernel = extract_named_matrix(section4, "A")
        c_kernel = extract_named_matrix(section4, "C")
        u_matrix = extract_named_matrix(section4, "U")
        v_matrix = extract_named_matrix(section4, "V")
        b_kernel = build_b_from_u_vt(u_matrix, v_matrix)
        if matrix_rank(b_kernel) != 2:
            fail("constructed B=UV^T does not have rank 2")
        if any(b_kernel[i][j] == 0 for i in range(3) for j in range(3)):
            fail("constructed B=UV^T has a zero entry")
        self.context.update(
            {
                "binding": binding,
                "result_text": result_text,
                "addendum_text": addendum_text,
                "A": a_kernel,
                "C": c_kernel,
                "U": u_matrix,
                "V": v_matrix,
                "B": b_kernel,
            }
        )
        self.checkpoint(
            "inputs",
            {
                "status": "OK",
                "input_root_argument": str(self.input_root_arg),
                "inputs_dir": str(self.inputs_dir),
                "source_commit": binding.get("source_commit"),
                "claim": binding.get("claim"),
                "literal_matrices_source": "RESULT.md section 4",
                "A": matrix_json(a_kernel),
                "C": matrix_json(c_kernel),
                "U": matrix_json(u_matrix),
                "V": matrix_json(v_matrix),
                "B_equals_UVt": matrix_json(b_kernel),
                "B_rank": matrix_rank(b_kernel),
                "author_checker_reference": {
                    "path": str(checker_path),
                    "opened": False,
                    "executed": False,
                    "imported": False,
                },
                "addendum_loaded_for_contract_context": bool(addendum_text),
            },
        )

    def build_events(self) -> None:
        self.deadline.check("build_events")
        a_kernel = self.context["A"]
        c_kernel = self.context["C"]
        b_kernel = self.context["B"]
        if not isinstance(a_kernel, list) or not isinstance(c_kernel, list) or not isinstance(b_kernel, list):
            fail("input matrices missing")
        p_a: dict[int, Fraction] = {}
        p_c: dict[int, Fraction] = {}
        for mask in range(8):
            p_a[mask] = det_fraction(complete_event_matrix_fraction(a_kernel, mask))
            p_c[mask] = det_fraction(complete_event_matrix_fraction(c_kernel, mask))
            if p_a[mask] <= 0:
                fail("nonpositive 3x3 A complete-event weight")
            if p_c[mask] <= 0:
                fail("nonpositive 3x3 C complete-event weight")
        if sum(p_a.values(), Fraction(0)) != 1:
            fail("A complete-event weights do not sum to 1")
        if sum(p_c.values(), Fraction(0)) != 1:
            fail("C complete-event weights do not sum to 1")

        kernel_poly = build_kernel_poly(a_kernel, c_kernel, b_kernel)
        events = []
        for left_mask in range(8):
            for right_mask in range(8):
                self.deadline.check("build_events")
                full_mask = left_mask | (right_mask << 3)
                event_poly = det_poly(complete_event_matrix_poly(kernel_poly, full_mask))
                mu = p_a[left_mask] * p_c[right_mask]
                if mu <= 0:
                    fail("nonpositive product event weight")
                q_poly_t = poly_scale(event_poly, Fraction(1, 1) / mu)
                bad_terms = []
                for degree, coeff in enumerate(q_poly_t):
                    if coeff != 0 and (degree % 2 == 1 or degree > 4):
                        bad_terms.append((degree, coeff))
                if bad_terms:
                    fail("event q(t) has odd or higher-degree terms")
                if poly_coeff(q_poly_t, 0) != 1:
                    fail("event q(t) constant coefficient is not 1")
                a_coeff = -poly_coeff(q_poly_t, 2)
                b_coeff = poly_coeff(q_poly_t, 4)
                trace_x, e2_x = posthoc_resolvent_ab(a_kernel, c_kernel, b_kernel, left_mask, right_mask)
                if trace_x != a_coeff or e2_x != b_coeff:
                    fail("posthoc Schur-resolvent a,b cross-check failed")
                events.append(
                    {
                        "left_mask": left_mask,
                        "right_mask": right_mask,
                        "full_mask": full_mask,
                        "left_bits": bit_string(left_mask, 3),
                        "right_bits": bit_string(right_mask, 3),
                        "full_bits": bit_string(full_mask, 6),
                        "pA": p_a[left_mask],
                        "pC": p_c[right_mask],
                        "mu": mu,
                        "event_probability_t_poly": event_poly,
                        "q_t_poly": q_poly_t,
                        "a": a_coeff,
                        "b": b_coeff,
                        "posthoc_resolvent_trace": trace_x,
                        "posthoc_resolvent_e2": e2_x,
                    }
                )
        sum_event_poly = (Fraction(0),)
        for event in events:
            sum_event_poly = poly_add(sum_event_poly, event["event_probability_t_poly"])
        if sum_event_poly != (Fraction(1),):
            fail("64 complete-event determinant polynomials do not normalize to 1")
        self.context.update({"pA": p_a, "pC": p_c, "kernel_poly": kernel_poly, "events": events})
        self.checkpoint(
            "events",
            {
                "status": "OK",
                "method": "direct 6x6 complete-event determinant polynomials over QQ[t], followed by extraction q(t)=1-a*t^2+b*t^4",
                "posthoc_ab_cross_check": "Schur-complement trace/e2 check run only after direct event construction",
                "left_3x3_events": [
                    {"mask": mask, "bits": bit_string(mask, 3), "pA": fraction_value_json(p_a[mask])}
                    for mask in range(8)
                ],
                "right_3x3_events": [
                    {"mask": mask, "bits": bit_string(mask, 3), "pC": fraction_value_json(p_c[mask])}
                    for mask in range(8)
                ],
                "event_count": len(events),
                "events": [
                    {
                        "left_mask": event["left_mask"],
                        "right_mask": event["right_mask"],
                        "full_mask": event["full_mask"],
                        "left_bits": event["left_bits"],
                        "right_bits": event["right_bits"],
                        "full_bits": event["full_bits"],
                        "pA": fraction_value_json(event["pA"]),
                        "pC": fraction_value_json(event["pC"]),
                        "mu": fraction_value_json(event["mu"]),
                        "event_probability_t_poly": poly_json(event["event_probability_t_poly"]),
                        "q_t_poly": poly_json(event["q_t_poly"]),
                        "a": fraction_value_json(event["a"]),
                        "b": fraction_value_json(event["b"]),
                    }
                    for event in events
                ],
            },
        )

    def verify_identities(self) -> None:
        self.deadline.check("verify_identities")
        events = self.context["events"]
        kernel_poly = self.context["kernel_poly"]
        p_a = self.context["pA"]
        p_c = self.context["pC"]
        if not isinstance(events, list) or not isinstance(kernel_poly, list) or not isinstance(p_a, dict) or not isinstance(p_c, dict):
            fail("event context missing")

        global_a = sum((event["mu"] * event["a"] for event in events), Fraction(0))
        global_b = sum((event["mu"] * event["b"] for event in events), Fraction(0))
        if global_a != 0 or global_b != 0:
            fail("global a,b cancellations failed")

        left_fibers = []
        right_fibers = []
        for left_mask in range(8):
            a_sum = sum((p_c[event["right_mask"]] * event["a"] for event in events if event["left_mask"] == left_mask), Fraction(0))
            b_sum = sum((p_c[event["right_mask"]] * event["b"] for event in events if event["left_mask"] == left_mask), Fraction(0))
            if a_sum != 0 or b_sum != 0:
                fail("left fiber cancellation failed")
            left_fibers.append({"left_mask": left_mask, "a_sum": a_sum, "b_sum": b_sum})
        for right_mask in range(8):
            a_sum = sum((p_a[event["left_mask"]] * event["a"] for event in events if event["right_mask"] == right_mask), Fraction(0))
            b_sum = sum((p_a[event["left_mask"]] * event["b"] for event in events if event["right_mask"] == right_mask), Fraction(0))
            if a_sum != 0 or b_sum != 0:
                fail("right fiber cancellation failed")
            right_fibers.append({"right_mask": right_mask, "a_sum": a_sum, "b_sum": b_sum})

        mobius_checks = []
        for subset_mask in range(64):
            self.deadline.check("verify_identities")
            indices = mask_indices(subset_mask, 6)
            principal_direct = det_poly(principal_submatrix_poly(kernel_poly, indices))
            principal_sum = (Fraction(0),)
            complementary_direct = det_poly(complementary_submatrix_poly(kernel_poly, indices))
            complementary_sum = (Fraction(0),)
            for event in events:
                full_mask = event["full_mask"]
                if full_mask & subset_mask == subset_mask:
                    principal_sum = poly_add(principal_sum, event["event_probability_t_poly"])
                if full_mask & subset_mask == 0:
                    complementary_sum = poly_add(complementary_sum, event["event_probability_t_poly"])
            if principal_sum != principal_direct:
                fail("principal Mobius identity failed")
            if complementary_sum != complementary_direct:
                fail("complementary Mobius identity failed")
            mobius_checks.append(
                {
                    "subset_mask": subset_mask,
                    "subset_bits": bit_string(subset_mask, 6),
                    "principal_minor_t_poly": principal_direct,
                    "complementary_minor_t_poly": complementary_direct,
                }
            )

        ea2 = sum((event["mu"] * event["a"] * event["a"] for event in events), Fraction(0))
        eab = sum((event["mu"] * event["a"] * event["b"] for event in events), Fraction(0))
        eb2 = sum((event["mu"] * event["b"] * event["b"] for event in events), Fraction(0))
        amax = max((abs(event["a"]) for event in events), default=Fraction(0))
        bmax = max((abs(event["b"]) for event in events), default=Fraction(0))
        if ea2 <= 0:
            fail("Ea2 is not positive")
        if eb2 <= 0:
            fail("Eb2 is not positive")
        if eab <= 0:
            fail("Eab is not positive, but displayed M2 lower bound uses Eab>0")
        moments = {"Ea2": ea2, "Eab": eab, "Eb2": eb2, "Amax": amax, "Bmax": bmax}
        self.context["moments"] = moments
        self.checkpoint(
            "identities",
            {
                "status": "OK",
                "normalization": {
                    "sum_mu": fraction_value_json(sum((event["mu"] for event in events), Fraction(0))),
                    "sum_mu_a": fraction_value_json(global_a),
                    "sum_mu_b": fraction_value_json(global_b),
                },
                "moments": {key: fraction_value_json(value) for key, value in moments.items()},
                "fiber_cancellations": {
                    "left": [
                        {
                            "left_mask": item["left_mask"],
                            "a_sum": fraction_value_json(item["a_sum"]),
                            "b_sum": fraction_value_json(item["b_sum"]),
                        }
                        for item in left_fibers
                    ],
                    "right": [
                        {
                            "right_mask": item["right_mask"],
                            "a_sum": fraction_value_json(item["a_sum"]),
                            "b_sum": fraction_value_json(item["b_sum"]),
                        }
                        for item in right_fibers
                    ],
                },
                "mobius_identity": {
                    "status": "all principal and complementary identities verified as QQ[t] polynomial equalities",
                    "subset_count": len(mobius_checks),
                    "subsets": [
                        {
                            "subset_mask": item["subset_mask"],
                            "subset_bits": item["subset_bits"],
                            "principal_minor_t_poly": poly_json(item["principal_minor_t_poly"]),
                            "complementary_minor_t_poly": poly_json(item["complementary_minor_t_poly"]),
                        }
                        for item in mobius_checks
                    ],
                },
            },
        )

    def compute_corridor(self) -> None:
        self.deadline.check("compute_corridor")
        events = self.context["events"]
        moments = self.context["moments"]
        if not isinstance(events, list) or not isinstance(moments, dict):
            fail("corridor context missing")
        ea2 = moments["Ea2"]
        eab = moments["Eab"]
        eb2 = moments["Eb2"]
        interval_outputs = []
        coverage_left = Fraction(INTERVALS[0][0])
        coverage_right = coverage_left
        for left_int, right_int in INTERVALS:
            left = Fraction(left_int)
            right = Fraction(right_int)
            if left > coverage_right:
                fail("intervals do not cover [3,15]")
            if right > coverage_right:
                coverage_right = right
            per_event = []
            q_minus = None
            q_plus = None
            for event in events:
                extrema = quadratic_extrema(event["a"], event["b"], left, right)
                min_q = extrema["min_q"]
                max_q = extrema["max_q"]
                if not isinstance(min_q, Fraction) or not isinstance(max_q, Fraction):
                    fail("internal extrema are not rational")
                if q_minus is None or min_q < q_minus:
                    q_minus = min_q
                if q_plus is None or max_q > q_plus:
                    q_plus = max_q
                per_event.append(
                    {
                        "left_mask": event["left_mask"],
                        "right_mask": event["right_mask"],
                        "full_mask": event["full_mask"],
                        "left_bits": event["left_bits"],
                        "right_bits": event["right_bits"],
                        "candidates": extrema["candidates"],
                        "min_s": extrema["min_s"],
                        "min_q": min_q,
                        "max_s": extrema["max_s"],
                        "max_q": max_q,
                    }
                )
            if q_minus is None or q_plus is None:
                fail("empty event list")
            if q_minus <= 0:
                fail("nonpositive event q encountered on corridor interval")
            u_max = max(Fraction(1) - q_minus, q_plus - Fraction(1))
            psi = 8 * u_max / q_minus + 10 * max((Fraction(1) - q_minus) / q_minus, q_plus - Fraction(1))
            m2_parenthesis = ea2 - 2 * right * eab
            m2_lower = left * left * m2_parenthesis
            if m2_parenthesis <= 0 or m2_lower <= 0:
                fail("M2 lower bound is not positive")
            left_side = 4 * m2_lower / q_plus
            squared_margin = left_side * left_side - (right**4) * psi * psi * eb2 * q_plus / q_minus
            if left_side <= 0:
                fail("left side lower bound is not positive")
            if squared_margin <= 0:
                fail("squared compensation margin is not strictly positive")
            interval_outputs.append(
                {
                    "label": "[" + str(left_int) + "," + str(right_int) + "]",
                    "L": left,
                    "R": right,
                    "q_minus": q_minus,
                    "q_plus": q_plus,
                    "u_max": u_max,
                    "Psi": psi,
                    "M2_parenthesis": m2_parenthesis,
                    "M2lower": m2_lower,
                    "left": left_side,
                    "squared_margin": squared_margin,
                    "per_event_extrema": per_event,
                }
            )
        if coverage_left != 3 or coverage_right < 15:
            fail("interval union failed to cover [3,15]")
        self.context["corridor_intervals"] = interval_outputs
        self.checkpoint(
            "corridor",
            {
                "status": "OK",
                "coverage": {
                    "target": "[3,15]",
                    "intervals": ["[" + str(l) + "," + str(r) + "]" for l, r in INTERVALS],
                    "verified_no_gaps": True,
                },
                "moments": {key: fraction_value_json(value) for key, value in moments.items()},
                "intervals": [
                    {
                        "label": entry["label"],
                        "L": fraction_value_json(entry["L"]),
                        "R": fraction_value_json(entry["R"]),
                        "q_minus": fraction_value_json(entry["q_minus"]),
                        "q_plus": fraction_value_json(entry["q_plus"]),
                        "u_max": fraction_value_json(entry["u_max"]),
                        "Psi": fraction_value_json(entry["Psi"]),
                        "M2_parenthesis": fraction_value_json(entry["M2_parenthesis"]),
                        "M2lower": fraction_value_json(entry["M2lower"]),
                        "left": fraction_value_json(entry["left"]),
                        "squared_margin": fraction_value_json(entry["squared_margin"]),
                        "strict_q_positive": entry["q_minus"] > 0,
                        "strict_squared_margin_positive": entry["squared_margin"] > 0,
                        "per_event_extrema": [
                            {
                                "left_mask": item["left_mask"],
                                "right_mask": item["right_mask"],
                                "full_mask": item["full_mask"],
                                "left_bits": item["left_bits"],
                                "right_bits": item["right_bits"],
                                "candidates": [
                                    {
                                        "s": fraction_value_json(candidate_s),
                                        "q": fraction_value_json(candidate_q),
                                    }
                                    for candidate_s, candidate_q in item["candidates"]
                                ],
                                "min_s": fraction_value_json(item["min_s"]),
                                "min_q": fraction_value_json(item["min_q"]),
                                "max_s": fraction_value_json(item["max_s"]),
                                "max_q": fraction_value_json(item["max_q"]),
                            }
                            for item in entry["per_event_extrema"]
                        ],
                    }
                    for entry in interval_outputs
                ],
                "legality_bridge": {
                    "event_q_positive_on_all_four_intervals": True,
                    "product_weights_positive": True,
                    "mobius_identities_verified_in_identities_json": True,
                    "conclusion": "principal and complementary minors are positive on [3,15] as sums of positive complete-event probabilities",
                },
            },
        )

    def compute_s10(self) -> None:
        self.deadline.check("compute_s10")
        events = self.context["events"]
        if not isinstance(events, list):
            fail("s10 context missing")
        s = Fraction(S10)
        log_entries = []
        w_interval = (Fraction(0), Fraction(0))
        curvature_interval = (Fraction(0), Fraction(0))
        q_min = None
        q_min_event = None
        derivative_log_linear_sum = Fraction(0)
        derivative_log_normalform_diff_sum = Fraction(0)
        derivative_rational_normalform_diff_sum = Fraction(0)
        left_derivative_log_coeff_sums = {mask: Fraction(0) for mask in range(8)}
        right_derivative_log_coeff_sums = {mask: Fraction(0) for mask in range(8)}
        for event in events:
            self.deadline.check("compute_s10")
            q = q_value(event["a"], event["b"], s)
            if q <= 0:
                fail("s=10 q is nonpositive")
            if q_min is None or q < q_min:
                q_min = q
                q_min_event = event["full_mask"]
            u = q - 1
            y = s * s * event["b"]
            log_data = log_atanh_interval(q, self.log_terms, self.store_log_terms)
            log_interval = (log_data["lower"], log_data["upper"])
            exact_8u_over_q = 8 * u / q
            psi_interval = interval_add_exact(interval_scale(10, log_interval), exact_8u_over_q)
            w_coeff = event["mu"] * event["b"]
            w_contrib = interval_scale(w_coeff, psi_interval)
            w_interval = interval_add(w_interval, w_contrib)

            q_t2 = s * (-2 * event["a"] + 12 * s * event["b"])
            log_coeff_derivative = event["mu"] * q_t2
            log_coeff_normal = event["mu"] * (2 * u + 10 * y)
            derivative_log_linear_sum += log_coeff_derivative
            left_derivative_log_coeff_sums[event["left_mask"]] += log_coeff_derivative
            right_derivative_log_coeff_sums[event["right_mask"]] += log_coeff_derivative
            derivative_log_normalform_diff_sum += log_coeff_derivative - log_coeff_normal
            rational_derivative = event["mu"] * 4 * (u + y) * (u + y) / q
            rational_normal = event["mu"] * (4 * u * u / q + 4 * y * y / q + 8 * y * u / q)
            derivative_rational_normalform_diff_sum += rational_derivative - rational_normal
            curvature_contrib = interval_add_exact(interval_scale(log_coeff_derivative, log_interval), rational_derivative)
            curvature_interval = interval_add(curvature_interval, curvature_contrib)

            log_entries.append(
                {
                    "left_mask": event["left_mask"],
                    "right_mask": event["right_mask"],
                    "full_mask": event["full_mask"],
                    "left_bits": event["left_bits"],
                    "right_bits": event["right_bits"],
                    "mu": event["mu"],
                    "a": event["a"],
                    "b": event["b"],
                    "q": q,
                    "u": u,
                    "y": y,
                    "log": log_data,
                    "psi_interval": psi_interval,
                    "W_coefficient_mu_b": w_coeff,
                    "W_contribution": w_contrib,
                    "curvature_log_coefficient_from_derivatives": log_coeff_derivative,
                    "curvature_log_coefficient_normalform": log_coeff_normal,
                    "curvature_rational_from_derivatives": rational_derivative,
                    "curvature_rational_normalform": rational_normal,
                    "curvature_contribution": curvature_contrib,
                }
            )
        if q_min is None:
            fail("s=10 q minimum missing")
        if q_min != EXPECTED_S10_Q_MIN:
            fail("s=10 q_min does not match frozen exact value")
        if derivative_log_linear_sum != 0:
            fail("derivative +1 log-linear cancellation failed")
        for mask, value in left_derivative_log_coeff_sums.items():
            if value != 0:
                fail("left fiber derivative log(mu) cancellation failed at mask " + str(mask))
        for mask, value in right_derivative_log_coeff_sums.items():
            if value != 0:
                fail("right fiber derivative log(mu) cancellation failed at mask " + str(mask))
        if derivative_log_normalform_diff_sum != 0:
            fail("derivative log coefficient did not match normal form")
        if derivative_rational_normalform_diff_sum != 0:
            fail("derivative rational Fisher term did not match normal form")
        w_width = w_interval[1] - w_interval[0]
        curvature_width = curvature_interval[1] - curvature_interval[0]
        if w_interval[1] >= 0:
            fail("W(10) upper endpoint is not negative")
        if w_width >= parse_decimal_fraction(W_WIDTH_TARGET):
            fail("W(10) interval width target failed")
        if curvature_interval[0] <= parse_decimal_fraction(CURVATURE_LOWER_TARGET):
            fail("true curvature lower endpoint target failed")
        if curvature_width >= parse_decimal_fraction(CURVATURE_WIDTH_TARGET):
            fail("true curvature interval width target failed")
        self.context["s10"] = {
            "q_min": q_min,
            "q_min_event": q_min_event,
            "W_interval": w_interval,
            "curvature_interval": curvature_interval,
        }
        self.checkpoint(
            "s10",
            {
                "status": "OK",
                "s": S10,
                "log_terms": self.log_terms,
                "log_enclosure": "log(q)=2*sum_{k=0}^{N-1} z^(2k+1)/(2k+1) with one-sided signed remainder: z>0 gives [sum,sum+tail], z<0 gives [sum-tail,sum], tail=2*|z|^(2N+1)/((2N+1)*(1-z^2))",
                "q_min": fraction_value_json(q_min),
                "expected_q_min": fraction_value_json(EXPECTED_S10_Q_MIN),
                "q_min_matches_expected": q_min == EXPECTED_S10_Q_MIN,
                "q_min_event_full_mask": q_min_event,
                "W": {
                    "interval": interval_json(w_interval[0], w_interval[1]),
                    "upper_endpoint_negative": w_interval[1] < 0,
                    "width_less_than": W_WIDTH_TARGET,
                    "width_check_passed": w_width < parse_decimal_fraction(W_WIDTH_TARGET),
                },
                "true_scaled_curvature_t2Ipp_equals_t2_minus_Hpp": {
                    "interval": interval_json(curvature_interval[0], curvature_interval[1]),
                    "lower_greater_than": CURVATURE_LOWER_TARGET,
                    "lower_check_passed": curvature_interval[0] > parse_decimal_fraction(CURVATURE_LOWER_TARGET),
                    "width_less_than": CURVATURE_WIDTH_TARGET,
                    "width_check_passed": curvature_width < parse_decimal_fraction(CURVATURE_WIDTH_TARGET),
                    "derivative_log_linear_plus_one_cancellation_sum": fraction_value_json(derivative_log_linear_sum),
                    "derivative_log_mu_cancellation": {
                        "explanation": "For p=mu*q, log(mu)=log(pA(left))+log(pC(right)). The per-left and per-right sums of mu*t^2*q'' vanish at s=10 by the exact fiber cancellations for a and b, so no log(mu) term remains.",
                        "left_fiber_sums": [
                            {
                                "left_mask": mask,
                                "left_bits": bit_string(mask, 3),
                                "coefficient_sum": fraction_value_json(left_derivative_log_coeff_sums[mask]),
                            }
                            for mask in range(8)
                        ],
                        "right_fiber_sums": [
                            {
                                "right_mask": mask,
                                "right_bits": bit_string(mask, 3),
                                "coefficient_sum": fraction_value_json(right_derivative_log_coeff_sums[mask]),
                            }
                            for mask in range(8)
                        ],
                    },
                    "derivative_log_normalform_diff_sum": fraction_value_json(derivative_log_normalform_diff_sum),
                    "derivative_rational_normalform_diff_sum": fraction_value_json(derivative_rational_normalform_diff_sum),
                    "normal_form_note": "curvature was reconstructed from q(t) derivatives before checking equality with the displayed u,y normal form",
                },
                "events": [
                    {
                        "left_mask": item["left_mask"],
                        "right_mask": item["right_mask"],
                        "full_mask": item["full_mask"],
                        "left_bits": item["left_bits"],
                        "right_bits": item["right_bits"],
                        "mu": fraction_value_json(item["mu"]),
                        "a": fraction_value_json(item["a"]),
                        "b": fraction_value_json(item["b"]),
                        "q": fraction_value_json(item["q"]),
                        "u": fraction_value_json(item["u"]),
                        "y": fraction_value_json(item["y"]),
                        "log": {
                            "z": fraction_value_json(item["log"]["z"]),
                            "series_sum": fraction_value_json(item["log"]["series_sum"]),
                            "tail_bound": fraction_value_json(item["log"]["tail_bound"]),
                            "tail_mode": item["log"]["tail_mode"],
                            "interval": interval_json(item["log"]["lower"], item["log"]["upper"]),
                            "terms": item["log"]["terms"],
                        },
                        "psi_interval": interval_json(item["psi_interval"][0], item["psi_interval"][1]),
                        "W_coefficient_mu_b": fraction_value_json(item["W_coefficient_mu_b"]),
                        "W_contribution": interval_json(item["W_contribution"][0], item["W_contribution"][1]),
                        "curvature_log_coefficient_from_derivatives": fraction_value_json(item["curvature_log_coefficient_from_derivatives"]),
                        "curvature_log_coefficient_normalform": fraction_value_json(item["curvature_log_coefficient_normalform"]),
                        "curvature_rational_from_derivatives": fraction_value_json(item["curvature_rational_from_derivatives"]),
                        "curvature_rational_normalform": fraction_value_json(item["curvature_rational_normalform"]),
                        "curvature_contribution": interval_json(item["curvature_contribution"][0], item["curvature_contribution"][1]),
                    }
                    for item in log_entries
                ],
            },
        )

    def compare_reference_output(self) -> None:
        self.deadline.check("compare_reference_output")
        reference_path = self.inputs_dir / "author_output_reference.txt"
        required_keys = required_reference_keys()
        corridor_required_keys = required_corridor_reference_keys()
        if not reference_path.is_file():
            self.checkpoint(
                "reference_compare",
                {
                    "status": "MISSING_REFERENCE",
                    "reason": "author_output_reference.txt not present",
                    "required_keys": required_keys,
                    "decimal_note": "printed decimal endpoints are not treated as exact outward endpoints",
                },
            )
            fail("required author_output_reference.txt comparison file is missing")
            return
        reference_text = reference_path.read_text(encoding="utf-8")
        reference_values = parse_reference_exact_fractions(reference_text)
        own_values = flatten_own_corridor_values(self.context["moments"], self.context["corridor_intervals"])
        s10 = self.context["s10"]
        if not isinstance(s10, dict) or not isinstance(s10.get("q_min"), Fraction):
            fail("s10 q_min missing before reference comparison")
        own_values["s10.q_min"] = s10["q_min"]
        comparisons = []
        mismatches = []
        missing_required_reference = []
        missing_required_own = []
        for key in required_keys:
            if key not in reference_values:
                missing_required_reference.append(key)
                comparisons.append({"key": key, "status": "MISSING_REFERENCE_VALUE"})
                continue
            if key not in own_values:
                missing_required_own.append(key)
                comparisons.append({"key": key, "status": "MISSING_OWN_VALUE", "reference": fraction_value_json(reference_values[key])})
                continue
            reference_value = reference_values[key]
            own_value = own_values[key]
            same = own_value == reference_value
            comparisons.append(
                {
                    "key": key,
                    "status": "MATCH" if same else "MISMATCH",
                    "ours": fraction_value_json(own_value),
                    "reference": fraction_value_json(reference_value),
                }
            )
            if not same:
                mismatches.append(key)
        extra_reference_keys = sorted(key for key in reference_values if key not in required_keys)
        status = (
            "MATCHED_REQUIRED_EXACT_FRACTIONS"
            if not mismatches and not missing_required_reference and not missing_required_own
            else "FAILED_REQUIRED_EXACT_FRACTIONS"
        )
        self.checkpoint(
            "reference_compare",
            {
                "status": status,
                "reference_path": str(reference_path),
                "mandatory_corridor_key_count": len(corridor_required_keys),
                "mandatory_total_key_count_including_s10_q_min": len(required_keys),
                "required_keys": required_keys,
                "missing_required_reference_keys": missing_required_reference,
                "missing_required_own_keys": missing_required_own,
                "mismatched_required_keys": mismatches,
                "matched_count": sum(1 for item in comparisons if item["status"] == "MATCH"),
                "extra_reference_keys": extra_reference_keys,
                "comparisons": comparisons,
                "decimal_note": "printed W and curvature endpoint decimals, if any, are treated as rounded display text only; exact signs and widths come from rational interval endpoints above",
            },
        )
        if missing_required_reference or missing_required_own or mismatches:
            parts = []
            if missing_required_reference:
                parts.append("missing reference values: " + ", ".join(missing_required_reference))
            if missing_required_own:
                parts.append("missing own values: " + ", ".join(missing_required_own))
            if mismatches:
                parts.append("mismatches: " + ", ".join(mismatches))
            fail("required reference exact fraction comparison failed; " + "; ".join(parts))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Independent PR58 corridor and s=10 exact certificate")
    parser.add_argument("--input-root", required=True, help="Path to pr58_corridor50 or its inputs directory")
    parser.add_argument("--out", required=True, help="Output directory for atomic JSON checkpoints")
    parser.add_argument("--wall-seconds", type=int, default=MAX_WALL_SECONDS, help="Wall-clock cap, capped again at 2700")
    parser.add_argument("--log-terms", type=int, default=DEFAULT_LOG_TERMS, help="atanh terms per event log enclosure")
    parser.add_argument("--no-store-log-terms", action="store_true", help="store only per-event sums and tails, not every atanh term")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    reject_forbidden_modules()
    args = parse_args(argv)
    out_root = Path(args.out)
    run = None
    try:
        if args.log_terms <= 0:
            fail("--log-terms must be positive")
        deadline = Deadline(args.wall_seconds)
        run = CertificateRun(
            input_root=Path(args.input_root),
            out_root=out_root,
            deadline=deadline,
            log_terms=args.log_terms,
            store_log_terms=not args.no_store_log_terms,
        )
        run.run()
        reject_forbidden_modules()
        return 0
    except Exception as exc:
        failure = {
            "status": "FAILED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc().splitlines(),
        }
        state = failure
        if run is not None:
            run.failures.append({"error_type": type(exc).__name__, "error": str(exc)})
            state = run.state(status="FAILED")
            state["last_failure"] = failure
        try:
            out_root.mkdir(parents=True, exist_ok=True)
            atomic_write_json(out_root / "FAILURE.json", failure)
            atomic_write_json(out_root / "state.json", state)
        except Exception:
            pass
        print("FAILED " + type(exc).__name__ + ": " + str(exc), file=sys.stderr, flush=True)
        if isinstance(exc, DeadlineExceeded):
            return 124
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
