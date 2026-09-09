#!/usr/bin/env python3
"""Independent finite checker for the PR58 joint-additive section-3 witness.

The arithmetic data below are literal copies of the frozen request: the
checker does not import, read, or execute any author checker or verifier code.
"""

import argparse
import itertools
import json
import os
import sys
import time
from fractions import Fraction


sys.set_int_max_str_digits(0)


EXPECTED_SOURCE_COMMIT = "a4f05cc962985015b71635bf633acce9dfe76866"
EXPECTED_ISSUE_COMMENT = "5604861257"
ROOT_CLAIM = "5604889076"

S = Fraction(9, 10)
WIDTH_TARGET = Fraction(1, 10**18)
DECIMAL_PLACES = 24
INITIAL_LOG_TERMS = 80
MAX_LOG_TERMS = 5120

TARGETS = {
    "3.4": ("L", ">", "192.45644754663817"),
    "3.5": ("T", "<", "166.44125195305153"),
    "3.6": ("W", "<", "-2.253552138695407"),
    "3.7": ("true_curvature", ">", "4.653598245398841"),
}

A_LITERAL = [
    ["219/500", "-47/1000", "73/1000"],
    ["-47/1000", "461/1000", "23/1000"],
    ["73/1000", "23/1000", "43/100"],
]

C_LITERAL = [
    ["231/500", "1/50", "-49/1000"],
    ["1/50", "43/100", "11/200"],
    ["-49/1000", "11/200", "3/5"],
]

U_LITERAL = [
    ["7/40", "-22/125"],
    ["339/1000", "13/250"],
    ["229/500", "-231/500"],
]

V_LITERAL = [
    ["141/200", "981/1000"],
    ["-343/1000", "113/250"],
    ["187/250", "577/1000"],
]

DUAL_TABLE = [
    [-20, -14, -10, 9, -26, -9, 15, 55],
    [-15, -8, -9, 3, -13, 4, 8, 30],
    [-11, -5, 35, 16, -21, -23, 28, -19],
    [2, 1, 20, 7, -7, -17, 9, -15],
    [-10, 9, -13, -10, 14, 44, -17, -17],
    [-8, 7, -10, -8, 12, 33, -13, -13],
    [36, 6, -7, -10, 24, -18, -17, -14],
    [26, 4, -6, -7, 17, -14, -13, -7],
]


class CheckerFailure(Exception):
    def __init__(self, status, message, detail=None, exit_code=1):
        super().__init__(message)
        self.status = status
        self.message = message
        self.detail = detail or {}
        self.exit_code = exit_code


def F(text):
    return Fraction(text)


def parse_matrix(literal):
    return [[F(value) for value in row] for row in literal]


def frac_payload(value):
    return {"num": str(value.numerator), "den": str(value.denominator)}


def jsonable(value):
    if isinstance(value, Fraction):
        return frac_payload(value)
    if isinstance(value, float):
        raise TypeError("JSON floats are forbidden by this checker")
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def scaled_decimal_text(scaled, places):
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled))
    if places == 0:
        return sign + digits
    if len(digits) <= places:
        digits = "0" * (places + 1 - len(digits)) + digits
    whole = digits[:-places]
    frac = digits[-places:]
    return sign + whole + "." + frac


def floor_scaled(value, places):
    scale = 10**places
    return (value.numerator * scale) // value.denominator


def ceil_scaled(value, places):
    scale = 10**places
    return -((-value.numerator * scale) // value.denominator)


def decimal_floor(value, places=DECIMAL_PLACES):
    return scaled_decimal_text(floor_scaled(value, places), places)


def decimal_ceil(value, places=DECIMAL_PLACES):
    return scaled_decimal_text(ceil_scaled(value, places), places)


def interval_payload(interval, places=DECIMAL_PLACES):
    lo, hi = interval
    return {
        "lo": lo,
        "hi": hi,
        "width": hi - lo,
        "decimal_places": places,
        "lo_decimal_floor": decimal_floor(lo, places),
        "hi_decimal_ceil": decimal_ceil(hi, places),
    }


def exact_payload(value, places=DECIMAL_PLACES):
    return {
        "exact": value,
        "decimal_places": places,
        "decimal_floor": decimal_floor(value, places),
        "decimal_ceil": decimal_ceil(value, places),
    }


def atomic_json(out_dir, name, payload):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    tmp = path + ".tmp." + str(os.getpid())
    wrapped = dict(payload)
    wrapped["written_time_ns"] = str(time.time_ns())
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(jsonable(wrapped), handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def input_presence(input_root):
    names = [
        "REQUEST.md",
        "ADDENDUM_JOINT_ADDITIVE.md",
        "SOURCE_BINDING.json",
    ]
    result = {}
    for name in names:
        path = os.path.join(input_root, name)
        try:
            stat = os.stat(path)
            result[name] = {
                "present": True,
                "size_bytes": str(stat.st_size),
                "mtime_ns": str(stat.st_mtime_ns),
                "read_by_checker": False,
            }
        except FileNotFoundError:
            result[name] = {"present": False, "read_by_checker": False}
    return result


def reject_json_float(text):
    raise ValueError("SOURCE_BINDING.json must not contain floating JSON tokens: " + text)


def resolve_input_dir(input_root_arg):
    direct = os.path.join(input_root_arg, "SOURCE_BINDING.json")
    nested = os.path.join(input_root_arg, "inputs", "SOURCE_BINDING.json")
    if os.path.isfile(direct):
        return input_root_arg
    if os.path.isfile(nested):
        return os.path.join(input_root_arg, "inputs")
    return input_root_arg


def load_and_validate_binding(input_root_arg):
    input_dir = resolve_input_dir(input_root_arg)
    required_names = ["REQUEST.md", "ADDENDUM_JOINT_ADDITIVE.md", "SOURCE_BINDING.json"]
    missing = [
        name for name in required_names if not os.path.isfile(os.path.join(input_dir, name))
    ]
    if missing:
        raise CheckerFailure(
            "INPUT_FILES_MISSING",
            "Required handoff input files are missing",
            {"input_root_argument": input_root_arg, "resolved_input_dir": input_dir, "missing": missing},
            2,
        )
    binding_path = os.path.join(input_dir, "SOURCE_BINDING.json")
    with open(binding_path, "r", encoding="utf-8") as handle:
        binding = json.load(handle, parse_float=reject_json_float)
    observed_commit = binding.get("source_commit")
    require(
        observed_commit == EXPECTED_SOURCE_COMMIT,
        "SOURCE_COMMIT_MISMATCH",
        "SOURCE_BINDING.json does not match the frozen source commit",
        {
            "expected_source_commit": EXPECTED_SOURCE_COMMIT,
            "observed_source_commit": observed_commit,
            "resolved_input_dir": input_dir,
        },
        2,
    )
    return {
        "input_root_argument": input_root_arg,
        "resolved_input_dir": input_dir,
        "required_files": input_presence(input_dir),
        "source_binding": binding,
    }


def deadline_from_environment(wall_seconds):
    if wall_seconds <= 0 or wall_seconds > 600:
        raise CheckerFailure(
            "BAD_WALL_SECONDS",
            "--wall-seconds must be in the interval 1..600",
            {"wall_seconds": str(wall_seconds)},
            2,
        )
    env_value = os.environ.get("C2_ABSOLUTE_DEADLINE_EPOCH")
    if env_value is None:
        raise CheckerFailure(
            "MISSING_DEADLINE_ENV",
            "C2_ABSOLUTE_DEADLINE_EPOCH is required by the run contract",
            {},
            2,
        )
    try:
        absolute_deadline_ns = int(env_value) * 1_000_000_000
    except ValueError as exc:
        raise CheckerFailure(
            "BAD_DEADLINE_ENV",
            "C2_ABSOLUTE_DEADLINE_EPOCH must be an integer epoch second",
            {"value": env_value},
            2,
        ) from exc
    local_deadline_ns = time.time_ns() + wall_seconds * 1_000_000_000
    return min(absolute_deadline_ns, local_deadline_ns)


def check_deadline(ctx, label):
    if time.time_ns() + 500_000_000 >= ctx["deadline_ns"]:
        raise CheckerFailure(
            "DEADLINE_REACHED",
            "Stopped before starting another arithmetic layer",
            {"layer": label, "deadline_ns": str(ctx["deadline_ns"])},
            70,
        )


def require(condition, status, message, detail=None, exit_code=10):
    if not condition:
        raise CheckerFailure(status, message, detail or {}, exit_code)


def mask_bits(mask, n=3):
    return [index for index in range(n) if (mask >> index) & 1]


def identity(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def mat_add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_sub(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_scalar(scale, matrix):
    return [[scale * item for item in row] for row in matrix]


def submatrix(matrix, indices):
    return [[matrix[i][j] for j in indices] for i in indices]


def det_matrix(matrix):
    n = len(matrix)
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if work[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            determinant = -determinant
        pivot_value = work[col][col]
        determinant *= pivot_value
        for row in range(col + 1, n):
            if work[row][col] == 0:
                continue
            factor = work[row][col] / pivot_value
            for j in range(col, n):
                work[row][j] -= factor * work[col][j]
    return determinant


def inverse_matrix(matrix):
    n = len(matrix)
    work = [matrix[i][:] + identity(n)[i] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if work[row][col] != 0:
                pivot = row
                break
        require(
            pivot is not None,
            "SINGULAR_MATRIX",
            "A required matrix inverse does not exist",
            {"column": col},
        )
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
        pivot_value = work[col][col]
        for j in range(2 * n):
            work[col][j] /= pivot_value
        for row in range(n):
            if row == col or work[row][col] == 0:
                continue
            factor = work[row][col]
            for j in range(2 * n):
                work[row][j] -= factor * work[col][j]
    return [row[n:] for row in work]


def matrix_rank(matrix):
    work = [row[:] for row in matrix]
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
        for j in range(col, cols):
            work[rank][j] /= pivot_value
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            factor = work[row][col]
            for j in range(col, cols):
                work[row][j] -= factor * work[rank][j]
        rank += 1
        if rank == rows:
            break
    return rank


def principal_minors(matrix):
    n = len(matrix)
    entries = []
    for mask in range(1, 1 << n):
        indices = mask_bits(mask, n)
        entries.append(
            {
                "mask": mask,
                "indices": indices,
                "determinant": det_matrix(submatrix(matrix, indices)),
            }
        )
    return entries


def all_principal_minors_positive(matrix):
    minors = principal_minors(matrix)
    return all(item["determinant"] > 0 for item in minors), minors


def complete_probability_const(kernel, mask):
    n = len(kernel)
    matrix = [row[:] for row in kernel]
    excluded = 0
    for i in range(n):
        if ((mask >> i) & 1) == 0:
            matrix[i][i] -= 1
            excluded += 1
    sign = -1 if excluded % 2 else 1
    return sign * det_matrix(matrix)


def poly_trim(poly):
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left, right):
    n = max(len(left), len(right))
    result = [Fraction(0) for _ in range(n)]
    for i in range(len(left)):
        result[i] += left[i]
    for i in range(len(right)):
        result[i] += right[i]
    return poly_trim(result)


def poly_neg(poly):
    return [-item for item in poly]


def poly_mul(left, right):
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_item in enumerate(left):
        if left_item == 0:
            continue
        for j, right_item in enumerate(right):
            if right_item != 0:
                result[i + j] += left_item * right_item
    return poly_trim(result)


def poly_scalar(scale, poly):
    return poly_trim([scale * item for item in poly])


def poly_coeffs(poly, degree):
    result = poly[:] + [Fraction(0)] * (degree + 1 - len(poly))
    return result[: degree + 1]


def permutation_sign(permutation):
    inversions = 0
    for i in range(len(permutation)):
        for j in range(i + 1, len(permutation)):
            if permutation[i] > permutation[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def det_poly(matrix):
    n = len(matrix)
    total = [Fraction(0)]
    for permutation in itertools.permutations(range(n)):
        term = [Fraction(1)]
        for row, col in enumerate(permutation):
            term = poly_mul(term, matrix[row][col])
            if term == [0]:
                break
        if permutation_sign(permutation) == 1:
            total = poly_add(total, term)
        else:
            total = poly_add(total, poly_neg(term))
    return poly_trim(total)


def kernel_poly_6(A, C, B):
    result = [[None for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            if i < 3 and j < 3:
                result[i][j] = [A[i][j]]
            elif i >= 3 and j >= 3:
                result[i][j] = [C[i - 3][j - 3]]
            elif i < 3 and j >= 3:
                result[i][j] = [Fraction(0), B[i][j - 3]]
            else:
                result[i][j] = [Fraction(0), B[j][i - 3]]
    return result


def complete_event_poly(kernel_poly, S_mask, T_mask):
    mask = S_mask | (T_mask << 3)
    matrix = [[entry[:] for entry in row] for row in kernel_poly]
    excluded = 0
    for i in range(6):
        if ((mask >> i) & 1) == 0:
            matrix[i][i] = poly_add(matrix[i][i], [Fraction(-1)])
            excluded += 1
    sign = -1 if excluded % 2 else 1
    return poly_scalar(sign, det_poly(matrix))


def atanh_series_enclosure(r, terms):
    require(
        Fraction(0) <= r < Fraction(1),
        "BAD_ATANH_ARGUMENT",
        "atanh range reduction produced an invalid argument",
        {"r": r},
    )
    partial = Fraction(0)
    power = r
    r2 = r * r
    for n in range(terms):
        partial += power / (2 * n + 1)
        power *= r2
    if r == 0:
        tail = Fraction(0)
    else:
        tail = power / ((2 * terms + 1) * (1 - r2))
    return {"partial": partial, "tail_bound": tail, "interval": (partial, partial + tail)}


def interval_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def interval_mul_exact(scale, interval):
    if scale >= 0:
        return scale * interval[0], scale * interval[1]
    return scale * interval[1], scale * interval[0]


def interval_div_positive(interval, denominator):
    require(
        denominator > 0,
        "BAD_INTERVAL_DIVISOR",
        "Positive interval divisor expected",
        {"denominator": denominator},
    )
    return interval[0] / denominator, interval[1] / denominator


def interval_square(interval):
    lo, hi = interval
    if lo <= 0 <= hi:
        return Fraction(0), max(lo * lo, hi * hi)
    if hi < 0:
        return hi * hi, lo * lo
    return lo * lo, hi * hi


def normalize_by_powers_of_two(x):
    require(x > 0, "LOG_NONPOSITIVE", "Logarithm input must be positive", {"x": x})
    z = x
    k = 0
    while z >= 2:
        z /= 2
        k += 1
    while z < 1:
        z *= 2
        k -= 1
    return k, z


def log2_interval(terms):
    data = atanh_series_enclosure(Fraction(1, 3), terms)
    lo, hi = data["interval"]
    return 2 * lo, 2 * hi


def log2_enclosure(terms):
    data = atanh_series_enclosure(Fraction(1, 3), terms)
    lo, hi = data["interval"]
    return {
        "atanh_r": Fraction(1, 3),
        "atanh_partial": data["partial"],
        "atanh_tail_bound": data["tail_bound"],
        "interval": (2 * lo, 2 * hi),
    }


def log_fraction_enclosure(x, terms, log2_data=None):
    k, z = normalize_by_powers_of_two(x)
    r = (z - 1) / (z + 1)
    data = atanh_series_enclosure(r, terms)
    lo, hi = data["interval"]
    log_z = 2 * lo, 2 * hi
    if log2_data is None:
        log2_data = log2_enclosure(terms)
    interval = interval_add(
        log_z, interval_mul_exact(Fraction(k), log2_data["interval"])
    )
    return {
        "x": x,
        "power_of_two_exponent": k,
        "reduced_z": z,
        "atanh_r": r,
        "terms": terms,
        "atanh_partial": data["partial"],
        "atanh_tail_bound": data["tail_bound"],
        "log_z_interval": log_z,
        "log2_interval_used": log2_data["interval"],
        "interval": interval,
    }


def zero_form(count):
    return {"constant": Fraction(0), "coefficients": [Fraction(0) for _ in range(count)]}


def form_interval(form, log_intervals):
    interval = (form["constant"], form["constant"])
    for coeff, log_interval in zip(form["coefficients"], log_intervals):
        if coeff != 0:
            interval = interval_add(interval, interval_mul_exact(coeff, log_interval))
    return interval


def decimal_fraction(text):
    sign = -1 if text.startswith("-") else 1
    body = text[1:] if sign == -1 else text
    if "." not in body:
        return Fraction(sign * int(body), 1)
    whole, frac = body.split(".", 1)
    numerator = int(whole + frac)
    denominator = 10 ** len(frac)
    return Fraction(sign * numerator, denominator)


def compare_interval_to_target(interval, relation, target):
    lo, hi = interval
    if relation == ">":
        if lo > target:
            return "PASS"
        if hi <= target:
            return "CERTIFIED_FALSE_DISJOINT"
        return "INSUFFICIENT_PRECISION"
    if relation == "<":
        if hi < target:
            return "PASS"
        if lo >= target:
            return "CERTIFIED_FALSE_DISJOINT"
        return "INSUFFICIENT_PRECISION"
    raise ValueError(relation)


def compare_intervals(left, relation, right):
    left_lo, left_hi = left
    right_lo, right_hi = right
    if relation == ">":
        if left_lo > right_hi:
            return "PASS"
        if left_hi <= right_lo:
            return "CERTIFIED_FALSE_DISJOINT"
        return "INSUFFICIENT_PRECISION"
    raise ValueError(relation)


def first_nonpass(comparisons):
    for item in comparisons:
        if item["status"] != "PASS":
            return item
    return None


def build_scalar_enclosures(events, forms, exacts, terms):
    log2_data = log2_enclosure(terms)
    log_data = [log_fraction_enclosure(event["q"], terms, log2_data) for event in events]
    log_intervals = [item["interval"] for item in log_data]
    P0 = form_interval(forms["P0"], log_intervals)
    W = form_interval(forms["W"], log_intervals)
    direct = form_interval(forms["direct_curvature"], log_intervals)
    cpsi = form_interval(forms["sum_cpsi"], log_intervals)
    A2 = exacts["A2"]
    denominator = exacts["dual_denominator"]
    L = interval_div_positive(interval_square(cpsi), denominator)
    P0_plus_A2 = interval_add(P0, (A2, A2))
    T = interval_div_positive(interval_mul_exact(Fraction(4), interval_square(P0_plus_A2)), A2)
    true_curvature = interval_add(P0_plus_A2, W)
    widths_ok = all(
        interval[1] - interval[0] < WIDTH_TARGET
        for interval in [P0, W, direct, cpsi, L, T, true_curvature]
    )
    return {
        "terms": terms,
        "log2": log2_data,
        "logs": log_data,
        "P0": P0,
        "A2": (A2, A2),
        "W": W,
        "sum_cpsi": cpsi,
        "dual_denominator": (denominator, denominator),
        "L": L,
        "T": T,
        "direct_curvature": direct,
        "true_curvature": true_curvature,
        "widths_ok": widths_ok,
    }


def log_audit_payload(scalars):
    return {
        "formula": {
            "range_reduction": "x = 2^k z with 1 <= z < 2, r = (z - 1)/(z + 1)",
            "series": "log(z) = 2*sum_{n=0}^{N-1} r^(2n+1)/(2n+1) + R",
            "tail_bound": "0 <= R <= 2*r^(2N+1)/((2N+1)*(1-r^2)); log(2) uses r=1/3",
        },
        "log2": scalars["log2"],
        "logq_by_event_index": [
            {
                "event_index": index,
                "x": item["x"],
                "power_of_two_exponent": item["power_of_two_exponent"],
                "reduced_z": item["reduced_z"],
                "atanh_r": item["atanh_r"],
                "terms": item["terms"],
                "atanh_partial": item["atanh_partial"],
                "atanh_tail_bound": item["atanh_tail_bound"],
                "log_z_interval": interval_payload(item["log_z_interval"]),
                "log2_interval_used": interval_payload(item["log2_interval_used"]),
                "logq_interval": interval_payload(item["interval"]),
            }
            for index, item in enumerate(scalars["logs"])
        ],
    }


def scalar_payload(scalars, include_logs=False):
    names = [
        "P0",
        "A2",
        "W",
        "sum_cpsi",
        "dual_denominator",
        "L",
        "T",
        "direct_curvature",
        "true_curvature",
    ]
    payload = {
        "terms": scalars["terms"],
        "width_target": WIDTH_TARGET,
        "widths_ok": scalars["widths_ok"],
        "scalars": {name: interval_payload(scalars[name]) for name in names},
    }
    if include_logs:
        payload["log_audit"] = log_audit_payload(scalars)
    return payload


def comparison_payload(scalars):
    qualitative = [
        {
            "name": "L>T",
            "status": compare_intervals(scalars["L"], ">", scalars["T"]),
            "left": interval_payload(scalars["L"]),
            "right": interval_payload(scalars["T"]),
        },
        {
            "name": "W<0",
            "status": compare_interval_to_target(scalars["W"], "<", Fraction(0)),
            "left": interval_payload(scalars["W"]),
            "target": Fraction(0),
        },
        {
            "name": "true_curvature>0",
            "status": compare_interval_to_target(
                scalars["true_curvature"], ">", Fraction(0)
            ),
            "left": interval_payload(scalars["true_curvature"]),
            "target": Fraction(0),
        },
    ]

    literal = []
    for label in ["3.4", "3.5", "3.6", "3.7"]:
        scalar_name, relation, target_text = TARGETS[label]
        target = decimal_fraction(target_text)
        literal.append(
            {
                "equation": label,
                "scalar": scalar_name,
                "relation": relation,
                "target_literal": target_text,
                "target": target,
                "interval": interval_payload(scalars[scalar_name]),
                "status": compare_interval_to_target(
                    scalars[scalar_name], relation, target
                ),
            }
        )
    return {"qualitative": qualitative, "literal_ordered": literal}


def literal_input_payload(A, C, U, V, B):
    return {
        "source_commit": EXPECTED_SOURCE_COMMIT,
        "issue_comment": EXPECTED_ISSUE_COMMENT,
        "root_claim": ROOT_CLAIM,
        "s": S,
        "A_literal": A_LITERAL,
        "C_literal": C_LITERAL,
        "U_literal": U_LITERAL,
        "V_literal": V_LITERAL,
        "dual_table": DUAL_TABLE,
        "A": A,
        "C": C,
        "U": U,
        "V": V,
        "B": B,
    }


def check_linear_algebra(A, C, B):
    I3 = identity(3)
    IA = mat_sub(I3, A)
    IC = mat_sub(I3, C)
    BT = transpose(B)
    A_inv = inverse_matrix(A)
    IA_inv = inverse_matrix(IA)
    schur_K = mat_sub(C, mat_scalar(S, matmul(matmul(BT, A_inv), B)))
    schur_complement = mat_sub(IC, mat_scalar(S, matmul(matmul(BT, IA_inv), B)))

    pd_checks = {}
    for name, matrix in [
        ("A", A),
        ("I_minus_A", IA),
        ("C", C),
        ("I_minus_C", IC),
        ("C_minus_s_BT_Ainv_B", schur_K),
        ("I_minus_C_minus_s_BT_IminusAinv_B", schur_complement),
    ]:
        ok, minors = all_principal_minors_positive(matrix)
        pd_checks[name] = {"all_principal_minors_positive": ok, "principal_minors": minors}
        require(
            ok,
            "STRICT_POSITIVITY_FAILED",
            "A Schur or marginal positivity check failed",
            {"matrix": name, "principal_minors": minors},
        )

    rank = matrix_rank(B)
    dense = all(item != 0 for row in B for item in row)
    require(rank == 2, "B_RANK_FAILED", "B must have exact rank two", {"rank": rank})
    require(dense, "B_DENSITY_FAILED", "Every B entry must be nonzero", {"B": B})

    return {
        "B_rank": rank,
        "B_dense": dense,
        "positive_definite_checks": pd_checks,
        "A_inverse": A_inv,
        "I_minus_A_inverse": IA_inv,
        "schur_K": schur_K,
        "schur_complement": schur_complement,
    }


def build_events(A, C, B, p_A, p_C):
    six_kernel = kernel_poly_6(A, C, B)
    events = []
    for S_mask in range(8):
        for T_mask in range(8):
            event_index = 8 * S_mask + T_mask
            poly = complete_event_poly(six_kernel, S_mask, T_mask)
            require(
                len(poly) <= 7,
                "EVENT_POLY_DEGREE_TOO_HIGH",
                "A complete event polynomial exceeded degree six in t",
                {"S_mask": S_mask, "T_mask": T_mask, "poly": poly},
            )
            coeffs = poly_coeffs(poly, 6)
            mu = p_A[S_mask] * p_C[T_mask]
            require(
                coeffs[0] == mu,
                "EVENT_CONSTANT_MISMATCH",
                "The t=0 complete event coefficient does not equal the product marginal",
                {
                    "S_mask": S_mask,
                    "T_mask": T_mask,
                    "coefficient": coeffs[0],
                    "mu": mu,
                },
            )
            for degree in [1, 3, 5, 6]:
                require(
                    coeffs[degree] == 0,
                    "EVENT_POLY_SHAPE_MISMATCH",
                    "The normalized event polynomial is not quadratic in s=t^2",
                    {
                        "S_mask": S_mask,
                        "T_mask": T_mask,
                        "degree": degree,
                        "coefficient": coeffs[degree],
                    },
                )
            require(mu > 0, "ZERO_PRODUCT_MARGIN", "Product marginal must be positive")
            a = -coeffs[2] / mu
            b = coeffs[4] / mu
            q = 1 - S * a + S * S * b
            q_prime = -a + 2 * S * b
            q_second = 2 * b
            P = mu * q
            u = q - 1
            y = S * S * b
            sq_prime = S * q_prime
            fisher_core = 4 * sq_prime * sq_prime / q
            direct_logq_coeff_core = S * (2 * q_prime + 4 * S * q_second)
            phi_rational_core = 4 * u * u / q
            phi_logq_coeff_core = 2 * u
            A2_core = 4 * y * y / q
            W_rational_core = 8 * u * y / q
            W_logq_coeff_core = 10 * y

            require(
                fisher_core == phi_rational_core + A2_core + W_rational_core,
                "EVENTWISE_RATIONAL_IDENTITY_FAILED",
                "Direct Fisher core disagrees with the u,y decomposition",
                {"S_mask": S_mask, "T_mask": T_mask},
            )
            require(
                direct_logq_coeff_core == phi_logq_coeff_core + W_logq_coeff_core,
                "EVENTWISE_LOG_IDENTITY_FAILED",
                "Direct acceleration log coefficient disagrees with the u,y decomposition",
                {"S_mask": S_mask, "T_mask": T_mask},
            )
            require(
                q > 0 and P > 0,
                "EVENT_PROBABILITY_NOT_STRICT",
                "Complete event probability at s=9/10 must be positive",
                {"S_mask": S_mask, "T_mask": T_mask, "q": q, "P": P},
            )
            events.append(
                {
                    "event_index": event_index,
                    "S_mask": S_mask,
                    "T_mask": T_mask,
                    "S_bits": mask_bits(S_mask),
                    "T_bits": mask_bits(T_mask),
                    "p_A": p_A[S_mask],
                    "p_C": p_C[T_mask],
                    "mu": mu,
                    "probability_poly_t_coeffs_0_to_6": coeffs,
                    "normalized_q_s_coeffs_0_to_2": [Fraction(1), -a, b],
                    "a": a,
                    "b": b,
                    "q": q,
                    "P": P,
                    "q_prime": q_prime,
                    "q_second": q_second,
                    "u": u,
                    "y": y,
                    "direct_fisher_core": fisher_core,
                    "direct_logq_coeff_core": direct_logq_coeff_core,
                    "phi_rational_core": phi_rational_core,
                    "phi_logq_coeff_core": phi_logq_coeff_core,
                    "A2_core": A2_core,
                    "W_rational_core": W_rational_core,
                    "W_logq_coeff_core": W_logq_coeff_core,
                }
            )
    return events


def check_cancellations(events, p_A, p_C):
    total_P = sum(event["P"] for event in events)
    row_P = [Fraction(0) for _ in range(8)]
    col_P = [Fraction(0) for _ in range(8)]
    row_a = [Fraction(0) for _ in range(8)]
    row_b = [Fraction(0) for _ in range(8)]
    col_a = [Fraction(0) for _ in range(8)]
    col_b = [Fraction(0) for _ in range(8)]
    row_log_mu = [Fraction(0) for _ in range(8)]
    col_log_mu = [Fraction(0) for _ in range(8)]
    for event in events:
        i = event["S_mask"]
        j = event["T_mask"]
        row_P[i] += event["P"]
        col_P[j] += event["P"]
        row_a[i] += p_C[j] * event["a"]
        row_b[i] += p_C[j] * event["b"]
        col_a[j] += p_A[i] * event["a"]
        col_b[j] += p_A[i] * event["b"]
        row_log_mu[i] += event["mu"] * event["direct_logq_coeff_core"]
        col_log_mu[j] += event["mu"] * event["direct_logq_coeff_core"]

    require(total_P == 1, "TOTAL_PROBABILITY_FAILED", "Total probability is not one", {"total_P": total_P})
    require(row_P == p_A, "FIXED_ROW_MARGINAL_FAILED", "Rows do not preserve p_A", {"row_P": row_P, "p_A": p_A})
    require(col_P == p_C, "FIXED_COLUMN_MARGINAL_FAILED", "Columns do not preserve p_C", {"col_P": col_P, "p_C": p_C})
    for name, values in [
        ("row_a", row_a),
        ("row_b", row_b),
        ("col_a", col_a),
        ("col_b", col_b),
        ("row_log_mu", row_log_mu),
        ("col_log_mu", col_log_mu),
    ]:
        require(
            all(value == 0 for value in values),
            "CONDITIONAL_CANCELLATION_FAILED",
            "A fixed-marginal or log(mu) cancellation is not exact",
            {"name": name, "values": values},
        )

    row_c = [sum(row) for row in DUAL_TABLE]
    col_c = [sum(DUAL_TABLE[i][j] for i in range(8)) for j in range(8)]
    require(
        all(value == 0 for value in row_c),
        "DUAL_ROW_SUM_FAILED",
        "A dual table row sum is nonzero",
        {"row_sums": row_c},
    )
    require(
        all(value == 0 for value in col_c),
        "DUAL_COLUMN_SUM_FAILED",
        "A dual table column sum is nonzero",
        {"column_sums": col_c},
    )

    return {
        "total_P": total_P,
        "row_P": row_P,
        "col_P": col_P,
        "row_a_means": row_a,
        "row_b_means": row_b,
        "col_a_means": col_a,
        "col_b_means": col_b,
        "row_log_mu_coefficients": row_log_mu,
        "col_log_mu_coefficients": col_log_mu,
        "dual_row_sums": row_c,
        "dual_column_sums": col_c,
    }


def build_forms(events):
    count = len(events)
    P0 = zero_form(count)
    W = zero_form(count)
    direct = zero_form(count)
    sum_cpsi = zero_form(count)
    A2 = Fraction(0)
    dual_denominator = Fraction(0)

    for event in events:
        index = event["event_index"]
        i = event["S_mask"]
        j = event["T_mask"]
        c = DUAL_TABLE[i][j]
        mu = event["mu"]
        P0["constant"] += mu * event["phi_rational_core"]
        P0["coefficients"][index] += mu * event["phi_logq_coeff_core"]
        A2 += mu * event["A2_core"]
        W["constant"] += mu * event["W_rational_core"]
        W["coefficients"][index] += mu * event["W_logq_coeff_core"]
        direct["constant"] += mu * event["direct_fisher_core"]
        direct["coefficients"][index] += mu * event["direct_logq_coeff_core"]
        sum_cpsi["constant"] += Fraction(c) * (8 * event["u"] / event["q"])
        sum_cpsi["coefficients"][index] += Fraction(10 * c)
        dual_denominator += Fraction(c * c) / event["P"]

    combined_constant = P0["constant"] + A2 + W["constant"]
    combined_coefficients = [
        P0["coefficients"][i] + W["coefficients"][i] for i in range(count)
    ]
    require(
        direct["constant"] == combined_constant,
        "AGGREGATE_DIRECT_CONSTANT_FAILED",
        "Direct differentiated constant term disagrees with P0+A2+W",
        {"direct": direct["constant"], "combined": combined_constant},
    )
    require(
        direct["coefficients"] == combined_coefficients,
        "AGGREGATE_DIRECT_LOG_COEFFICIENT_FAILED",
        "Direct differentiated log coefficients disagree with P0+A2+W",
        {"direct": direct["coefficients"], "combined": combined_coefficients},
    )
    require(
        A2 > 0,
        "A2_NOT_POSITIVE",
        "A2 must be strictly positive",
        {"A2": A2},
    )
    require(
        dual_denominator > 0,
        "DUAL_DENOMINATOR_NOT_POSITIVE",
        "The dual Cauchy denominator must be strictly positive",
        {"dual_denominator": dual_denominator},
    )

    return {
        "forms": {
            "P0": P0,
            "W": W,
            "direct_curvature": direct,
            "sum_cpsi": sum_cpsi,
        },
        "exacts": {"A2": A2, "dual_denominator": dual_denominator},
        "combined_curvature_form": {
            "constant": combined_constant,
            "coefficients": combined_coefficients,
        },
    }


def run(ctx):
    check_deadline(ctx, "startup")
    binding = load_and_validate_binding(ctx["input_root"])
    A = parse_matrix(A_LITERAL)
    C = parse_matrix(C_LITERAL)
    U = parse_matrix(U_LITERAL)
    V = parse_matrix(V_LITERAL)
    B = matmul(U, transpose(V))

    atomic_json(
        ctx["out_dir"],
        "00_metadata.json",
        {
            "status": "STARTED",
            "pid": str(os.getpid()),
            "source_commit": EXPECTED_SOURCE_COMMIT,
            "issue_comment": EXPECTED_ISSUE_COMMENT,
            "root_claim": ROOT_CLAIM,
            "deadline_ns": str(ctx["deadline_ns"]),
            "wall_seconds": str(ctx["wall_seconds"]),
            "input_root_argument": ctx["input_root"],
            "resolved_input_dir": binding["resolved_input_dir"],
            "input_files": binding["required_files"],
            "source_binding": binding["source_binding"],
            "runtime_dependency": "Python standard library only",
            "author_checker_read_import_execute": False,
            "reference_files_accessed": False,
        },
    )
    atomic_json(ctx["out_dir"], "01_literal_inputs.json", literal_input_payload(A, C, U, V, B))

    check_deadline(ctx, "linear_algebra")
    linear = check_linear_algebra(A, C, B)
    atomic_json(ctx["out_dir"], "02_linear_algebra.json", linear)

    check_deadline(ctx, "block_marginals")
    p_A = [complete_probability_const(A, mask) for mask in range(8)]
    p_C = [complete_probability_const(C, mask) for mask in range(8)]
    require(sum(p_A) == 1, "A_MARGINAL_TOTAL_FAILED", "p_A does not sum to one", {"p_A": p_A})
    require(sum(p_C) == 1, "C_MARGINAL_TOTAL_FAILED", "p_C does not sum to one", {"p_C": p_C})
    require(all(item > 0 for item in p_A), "A_COMPLETE_EVENTS_NOT_STRICT", "All A complete events must be positive", {"p_A": p_A})
    require(all(item > 0 for item in p_C), "C_COMPLETE_EVENTS_NOT_STRICT", "All C complete events must be positive", {"p_C": p_C})
    atomic_json(
        ctx["out_dir"],
        "03_block_marginals.json",
        {
            "p_A": p_A,
            "p_C": p_C,
            "sum_p_A": sum(p_A),
            "sum_p_C": sum(p_C),
            "all_positive": all(item > 0 for item in p_A + p_C),
        },
    )

    check_deadline(ctx, "events")
    events = build_events(A, C, B, p_A, p_C)
    atomic_json(
        ctx["out_dir"],
        "04_events.json",
        {
            "event_count": len(events),
            "events": events,
            "all_q_positive": all(event["q"] > 0 for event in events),
            "all_P_positive": all(event["P"] > 0 for event in events),
        },
    )

    check_deadline(ctx, "cancellations")
    cancellations = check_cancellations(events, p_A, p_C)
    atomic_json(ctx["out_dir"], "05_cancellations.json", cancellations)

    check_deadline(ctx, "forms")
    form_data = build_forms(events)
    atomic_json(ctx["out_dir"], "06_forms.json", form_data)

    terms = INITIAL_LOG_TERMS
    last_scalars = None
    last_comparisons = None
    while terms <= MAX_LOG_TERMS:
        check_deadline(ctx, "scalar_enclosures")
        scalars = build_scalar_enclosures(events, form_data["forms"], form_data["exacts"], terms)
        atomic_json(
            ctx["out_dir"],
            f"07_scalar_enclosures_N{terms}.json",
            scalar_payload(scalars, include_logs=(terms == INITIAL_LOG_TERMS)),
        )
        comparisons = comparison_payload(scalars)
        atomic_json(ctx["out_dir"], f"08_comparisons_N{terms}.json", comparisons)
        last_scalars = scalars
        last_comparisons = comparisons

        literal_failure = first_nonpass(comparisons["literal_ordered"])
        qualitative_failure = first_nonpass(comparisons["qualitative"])
        if scalars["widths_ok"] and literal_failure is None and qualitative_failure is None:
            atomic_json(
                ctx["out_dir"],
                "final.json",
                {
                    "status": "SUCCESS",
                    "message": "All exact checks, qualitative signs, and literal decimal bounds passed.",
                    "log_terms": terms,
                    "comparisons": comparisons,
                    "scalar_summary": scalar_payload(scalars),
                },
            )
            print(json.dumps({"status": "SUCCESS", "log_terms": terms}, sort_keys=True))
            return 0

        if literal_failure and literal_failure["status"] == "CERTIFIED_FALSE_DISJOINT":
            raise CheckerFailure(
                "LITERAL_BOUND_CERTIFIED_FALSE",
                "A literal equation bound is disjoint from the certified scalar interval",
                {"first_failure": literal_failure, "log_terms": terms},
                20,
            )
        if qualitative_failure and qualitative_failure["status"] == "CERTIFIED_FALSE_DISJOINT":
            raise CheckerFailure(
                "QUALITATIVE_SIGN_CERTIFIED_FALSE",
                "A qualitative sign comparison is disjoint from the certified intervals",
                {"first_failure": qualitative_failure, "log_terms": terms},
                21,
            )
        terms *= 2

    raise CheckerFailure(
        "INSUFFICIENT_PRECISION",
        "The logarithm enclosure loop reached MAX_LOG_TERMS without certified comparisons",
        {
            "max_log_terms": MAX_LOG_TERMS,
            "last_scalars": scalar_payload(last_scalars) if last_scalars else None,
            "last_comparisons": last_comparisons,
        },
        30,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--wall-seconds", type=int, default=600)
    args = parser.parse_args()

    out_dir = args.out
    try:
        deadline_ns = deadline_from_environment(args.wall_seconds)
        ctx = {
            "input_root": args.input_root,
            "out_dir": out_dir,
            "wall_seconds": args.wall_seconds,
            "deadline_ns": deadline_ns,
        }
        return run(ctx)
    except CheckerFailure as failure:
        os.makedirs(out_dir, exist_ok=True)
        atomic_json(
            out_dir,
            "final.json",
            {
                "status": failure.status,
                "message": failure.message,
                "detail": failure.detail,
            },
        )
        print(
            json.dumps(
                {"status": failure.status, "message": failure.message},
                sort_keys=True,
            )
        )
        return failure.exit_code


if __name__ == "__main__":
    sys.exit(main())
