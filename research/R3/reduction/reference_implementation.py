"""Reference implementation for grouped low-rank DPP event entropy.

This file is intentionally small and dependency-free.  It is meant to be
auditable before it is fast: exact rational determinants are used for the
small comparison tests, and the grouped formula avoids enumerating all 2^n
events when the kernel has repeated row types.

Main convention:
    A marginal-kernel DPP is defined by P(A subset Y) = det(K_A).
    Exact atom probabilities are obtained either by Mobius inversion or,
    for 0<K<I, by the L-ensemble formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from math import comb
from typing import Iterable, Sequence


Matrix = list[list[Fraction]]


def q(x) -> Fraction:
    """Convert ints, strings, or Fractions to Fraction."""

    return x if isinstance(x, Fraction) else Fraction(x)


def as_matrix(a: Sequence[Sequence[object]]) -> Matrix:
    return [[q(x) for x in row] for row in a]


def eye(n: int) -> Matrix:
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def zeros(rows: int, cols: int) -> Matrix:
    return [[Fraction(0) for _ in range(cols)] for _ in range(rows)]


def transpose(a: Matrix) -> Matrix:
    if not a:
        return []
    return [list(row) for row in zip(*a)]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def scalar_mul(c: Fraction, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    if not a or not b:
        return zeros(len(a), len(b[0]) if b else 0)
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def outer(x: Sequence[Fraction], y: Sequence[Fraction]) -> Matrix:
    return [[xi * yj for yj in y] for xi in x]


def det_bareiss(a: Matrix) -> Fraction:
    """Exact determinant by fraction-preserving Gaussian/Bareiss elimination."""

    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = Fraction(1)
    previous = Fraction(1)
    for k in range(n - 1):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pivot_value - m[i][k] * m[k][j]) / previous
        previous = pivot_value
        for i in range(k + 1, n):
            m[i][k] = Fraction(0)
    return sign * m[n - 1][n - 1]


def inverse(a: Matrix) -> Matrix:
    """Exact inverse by Gauss-Jordan elimination."""

    n = len(a)
    m = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for k in range(n):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            raise ValueError("matrix is singular")
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
        scale = m[k][k]
        m[k] = [x / scale for x in m[k]]
        for i in range(n):
            if i == k:
                continue
            factor = m[i][k]
            if factor:
                m[i] = [x - factor * y for x, y in zip(m[i], m[k])]
    return [row[n:] for row in m]


def principal_submatrix(a: Matrix, indices: Sequence[int]) -> Matrix:
    return [[a[i][j] for j in indices] for i in indices]


def indices_from_mask(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def popcount(mask: int) -> int:
    return mask.bit_count()


def event_probabilities_mobius(k: Matrix) -> list[Fraction]:
    """Direct Mobius inversion from inclusion probabilities.

    This is the deliberately slow checker:

        p(S) = sum_{T subset S^c} (-1)^|T| det K_{S union T}.

    Use only for small n, normally n<=8 in this project.
    """

    n = len(k)
    full = (1 << n) - 1
    inclusion = []
    for mask in range(1 << n):
        inclusion.append(det_bareiss(principal_submatrix(k, indices_from_mask(mask, n))))

    atoms: list[Fraction] = []
    for s_mask in range(1 << n):
        comp = full ^ s_mask
        total = Fraction(0)
        t_mask = comp
        while True:
            sign = -1 if popcount(t_mask) & 1 else 1
            total += sign * inclusion[s_mask | t_mask]
            if t_mask == 0:
                break
            t_mask = (t_mask - 1) & comp
        atoms.append(total)
    return atoms


def event_probabilities_l_ensemble(k: Matrix) -> list[Fraction]:
    """Exact atom probabilities via L=K(I-K)^(-1).

    Preconditions are not checked here: callers must certify 0<K<I.  If
    I-K is singular the inverse routine raises ValueError.
    """

    n = len(k)
    i_minus_k = mat_sub(eye(n), k)
    det_i_minus_k = det_bareiss(i_minus_k)
    l_kernel = mat_mul(k, inverse(i_minus_k))
    atoms = []
    for mask in range(1 << n):
        idx = indices_from_mask(mask, n)
        atoms.append(det_i_minus_k * det_bareiss(principal_submatrix(l_kernel, idx)))
    return atoms


def validate_grouped_input(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
) -> tuple[Fraction, Matrix, tuple[int, ...], Matrix]:
    a_q = q(a)
    c_q = as_matrix(c)
    sizes = tuple(int(x) for x in group_sizes)
    features = as_matrix(feature_rows)
    if not sizes or any(x < 0 for x in sizes):
        raise ValueError("group sizes must be nonnegative and not all omitted")
    if len(features) != len(sizes):
        raise ValueError("one feature row is required for each group")
    r = len(c_q)
    if any(len(row) != r for row in c_q):
        raise ValueError("C must be square")
    if any(len(row) != r for row in features):
        raise ValueError("each feature row must have length rank r")
    if any(c_q[i][j] != c_q[j][i] for i in range(r) for j in range(r)):
        raise ValueError("C must be symmetric for the real-symmetric certificate")
    return a_q, c_q, sizes, features


def group_labels(group_sizes: Sequence[int]) -> list[int]:
    labels: list[int] = []
    for g, size in enumerate(group_sizes):
        labels.extend([g] * size)
    return labels


def total_gram(group_sizes: Sequence[int], feature_rows: Matrix) -> Matrix:
    r = len(feature_rows[0]) if feature_rows else 0
    gram = zeros(r, r)
    for size, row in zip(group_sizes, feature_rows):
        gram = mat_add(gram, scalar_mul(Fraction(size), outer(row, row)))
    return gram


def count_gram(counts: Sequence[int], feature_rows: Matrix) -> Matrix:
    r = len(feature_rows[0]) if feature_rows else 0
    gram = zeros(r, r)
    for count, row in zip(counts, feature_rows):
        gram = mat_add(gram, scalar_mul(Fraction(count), outer(row, row)))
    return gram


def bilinear(x: Sequence[Fraction], c: Matrix, y: Sequence[Fraction]) -> Fraction:
    return sum(x[i] * c[i][j] * y[j] for i in range(len(c)) for j in range(len(c)))


def build_grouped_k(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
) -> Matrix:
    """Build the full K=aI+UCU^T from repeated feature rows."""

    a_q, c_q, sizes, features = validate_grouped_input(a, c, group_sizes, feature_rows)
    labels = group_labels(sizes)
    rows = [features[g] for g in labels]
    n = len(rows)
    k = zeros(n, n)
    for i in range(n):
        for j in range(n):
            k[i][j] = (a_q if i == j else Fraction(0)) + bilinear(rows[i], c_q, rows[j])
    return k


@dataclass(frozen=True)
class ReducedLKernel:
    """L = alpha I + U M U^T for grouped repeated feature rows."""

    alpha: Fraction
    m_matrix: Matrix
    det_i_minus_k: Fraction
    group_sizes: tuple[int, ...]
    feature_rows: Matrix

    @property
    def n(self) -> int:
        return sum(self.group_sizes)

    @property
    def rank(self) -> int:
        return len(self.m_matrix)


def reduced_l_from_grouped(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
) -> ReducedLKernel:
    """Return reduced L-ensemble parameters for K=aI+UCU^T.

    Requires 0<a<1 and det(I-K) != 0.  Positive contraction should be
    certified separately; this routine only performs algebra.
    """

    a_q, c_q, sizes, features = validate_grouped_input(a, c, group_sizes, feature_rows)
    if not (0 < a_q < 1):
        raise ValueError("the reduced L formula in this file requires 0<a<1")
    b = 1 - a_q
    n = sum(sizes)
    r = len(c_q)
    gram = total_gram(sizes, features)
    small = mat_sub(eye(r), scalar_mul(1 / b, mat_mul(c_q, gram)))
    det_i_minus_k = (b**n) * det_bareiss(small)
    solve_matrix = mat_sub(scalar_mul(b, eye(r)), mat_mul(c_q, gram))
    m_matrix = scalar_mul(1 / b, mat_mul(inverse(solve_matrix), c_q))
    return ReducedLKernel(
        alpha=a_q / b,
        m_matrix=m_matrix,
        det_i_minus_k=det_i_minus_k,
        group_sizes=sizes,
        feature_rows=features,
    )


def det_l_for_counts(reduced: ReducedLKernel, counts: Sequence[int]) -> Fraction:
    """Compute det L_S from only the group counts c_g=|S cap G_g|."""

    if len(counts) != len(reduced.group_sizes):
        raise ValueError("count vector has wrong length")
    if any(count < 0 or count > size for count, size in zip(counts, reduced.group_sizes)):
        raise ValueError("count outside group size")
    alpha = reduced.alpha
    if alpha <= 0:
        raise ValueError("alpha must be positive for this determinant reduction")
    s = sum(counts)
    gram_c = count_gram(counts, reduced.feature_rows)
    small = mat_add(eye(reduced.rank), scalar_mul(1 / alpha, mat_mul(reduced.m_matrix, gram_c)))
    return (alpha**s) * det_bareiss(small)


def event_probability_for_counts(reduced: ReducedLKernel, counts: Sequence[int]) -> Fraction:
    return reduced.det_i_minus_k * det_l_for_counts(reduced, counts)


def iter_count_vectors(group_sizes: Sequence[int]) -> Iterable[tuple[int, ...]]:
    return product(*(range(size + 1) for size in group_sizes))


def count_multiplicity(group_sizes: Sequence[int], counts: Sequence[int]) -> int:
    out = 1
    for size, count in zip(group_sizes, counts):
        out *= comb(size, count)
    return out


def reduced_count_masses(reduced: ReducedLKernel) -> list[tuple[tuple[int, ...], int, Fraction]]:
    """Return (counts, multiplicity, atom_probability_per_subset)."""

    masses = []
    for counts in iter_count_vectors(reduced.group_sizes):
        masses.append(
            (
                counts,
                count_multiplicity(reduced.group_sizes, counts),
                event_probability_for_counts(reduced, counts),
            )
        )
    return masses


def counts_for_mask(mask: int, group_sizes: Sequence[int]) -> tuple[int, ...]:
    counts = [0] * len(group_sizes)
    offset = 0
    for g, size in enumerate(group_sizes):
        local = 0
        for j in range(size):
            if (mask >> (offset + j)) & 1:
                local += 1
        counts[g] = local
        offset += size
    return tuple(counts)


def probabilities_by_count(reduced: ReducedLKernel) -> dict[tuple[int, ...], Fraction]:
    return {counts: prob for counts, _, prob in reduced_count_masses(reduced)}


def decimal_from_fraction(x: Fraction, precision: int) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def entropy_from_event_probabilities(atoms: Sequence[Fraction], precision: int = 80) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        total = Decimal(0)
        for prob in atoms:
            if prob == 0:
                continue
            if prob < 0:
                raise ValueError(f"negative atom probability: {prob}")
            p_dec = decimal_from_fraction(prob, precision)
            total -= p_dec * p_dec.ln()
        return +total


def entropy_from_count_masses(
    masses: Sequence[tuple[tuple[int, ...], int, Fraction]], precision: int = 80
) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        total = Decimal(0)
        for _, multiplicity, prob in masses:
            if prob == 0:
                continue
            if prob < 0:
                raise ValueError(f"negative atom probability: {prob}")
            p_dec = decimal_from_fraction(prob, precision)
            total -= Decimal(multiplicity) * p_dec * p_dec.ln()
        return +total


def entropy_grouped(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
    precision: int = 80,
) -> Decimal:
    reduced = reduced_l_from_grouped(a, c, group_sizes, feature_rows)
    return entropy_from_count_masses(reduced_count_masses(reduced), precision=precision)


@dataclass(frozen=True)
class DecimalInterval:
    lo: Decimal
    hi: Decimal

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("invalid interval")


def chord_gap_interval(
    h0: DecimalInterval,
    h1: DecimalInterval,
    ht: DecimalInterval,
    theta: object = Fraction(1, 2),
    precision: int = 80,
) -> DecimalInterval:
    """Combine entropy enclosures into the concavity Jensen-gap enclosure.

    The sign convention is

        J = H(K_t) - (1-theta)H(K_0) - theta H(K_1).

    Thus J<0 certifies a concavity violation.
    """

    theta_q = q(theta)
    with localcontext() as ctx:
        ctx.prec = precision
        td = decimal_from_fraction(theta_q, precision)
        one_minus = Decimal(1) - td
        lo = ht.lo - one_minus * h0.hi - td * h1.hi
        hi = ht.hi - one_minus * h0.lo - td * h1.lo
        return DecimalInterval(+lo, +hi)


def chord_gap_reduced(
    a0: object,
    c0: Sequence[Sequence[object]],
    a1: object,
    c1: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
    theta: object = Fraction(1, 2),
    precision: int = 80,
) -> Decimal:
    """Compute the compatible real-symmetric chord Jensen gap.

    K_0 and K_1 must share the same repeated feature rows and group sizes:

        K_i = a_i I + U C_i U^T.
    """

    theta_q = q(theta)
    c0_q = as_matrix(c0)
    c1_q = as_matrix(c1)
    at = (1 - theta_q) * q(a0) + theta_q * q(a1)
    ct = mat_add(scalar_mul(1 - theta_q, c0_q), scalar_mul(theta_q, c1_q))
    h0 = entropy_grouped(a0, c0_q, group_sizes, feature_rows, precision)
    h1 = entropy_grouped(a1, c1_q, group_sizes, feature_rows, precision)
    ht = entropy_grouped(at, ct, group_sizes, feature_rows, precision)
    with localcontext() as ctx:
        ctx.prec = precision
        td = decimal_from_fraction(theta_q, precision)
        return +(ht - (Decimal(1) - td) * h0 - td * h1)


def positive_definite_sylvester(a: Matrix) -> tuple[bool, list[Fraction]]:
    minors = [det_bareiss(principal_submatrix(a, list(range(k)))) for k in range(1, len(a) + 1)]
    return all(x > 0 for x in minors), minors


def positive_contraction_certificate_grouped(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
) -> dict[str, object]:
    """Small exact certificate for 0<K<I when U^T U is nonsingular.

    Let G=U^T U.  If G is positive definite and 0<a<1, then

        K>0      iff C + a G^(-1) > 0,
        I-K>0    iff (1-a) G^(-1) - C > 0,

    because the orthogonal complement of col(U) has eigenvalue a for K and
    1-a for I-K, while the column space reduces to these two r by r forms.
    """

    a_q, c_q, sizes, features = validate_grouped_input(a, c, group_sizes, feature_rows)
    gram = total_gram(sizes, features)
    cert: dict[str, object] = {
        "a": str(a_q),
        "n": sum(sizes),
        "rank": len(c_q),
        "scalar_margin_ok": 0 < a_q < 1,
    }
    gram_ok, gram_minors = positive_definite_sylvester(gram)
    cert["gram_leading_minors"] = [str(x) for x in gram_minors]
    cert["gram_positive_definite"] = gram_ok
    if not (0 < a_q < 1 and gram_ok):
        cert["status"] = "UNSUPPORTED"
        return cert
    gram_inv = inverse(gram)
    k_form = mat_add(c_q, scalar_mul(a_q, gram_inv))
    ik_form = mat_sub(scalar_mul(1 - a_q, gram_inv), c_q)
    k_ok, k_minors = positive_definite_sylvester(k_form)
    ik_ok, ik_minors = positive_definite_sylvester(ik_form)
    cert.update(
        {
            "K_reduced_form_leading_minors": [str(x) for x in k_minors],
            "I_minus_K_reduced_form_leading_minors": [str(x) for x in ik_minors],
            "K_positive_definite": k_ok,
            "I_minus_K_positive_definite": ik_ok,
            "status": "STRICT_POSITIVE_CONTRACTION" if k_ok and ik_ok else "FAILED",
        }
    )
    return cert


def probability_sum_from_count_masses(
    masses: Sequence[tuple[tuple[int, ...], int, Fraction]]
) -> Fraction:
    return sum(Fraction(mult) * prob for _, mult, prob in masses)


def minimum_atom_from_count_masses(
    masses: Sequence[tuple[tuple[int, ...], int, Fraction]]
) -> Fraction:
    return min(prob for _, _, prob in masses)


def compare_mobius_to_reduced(
    a: object,
    c: Sequence[Sequence[object]],
    group_sizes: Sequence[int],
    feature_rows: Sequence[Sequence[object]],
) -> dict[str, object]:
    """Small-n audit helper used by the tests."""

    k = build_grouped_k(a, c, group_sizes, feature_rows)
    atoms = event_probabilities_mobius(k)
    reduced = reduced_l_from_grouped(a, c, group_sizes, feature_rows)
    by_count = probabilities_by_count(reduced)
    mismatches = []
    for mask, atom in enumerate(atoms):
        counts = counts_for_mask(mask, group_sizes)
        if atom != by_count[counts]:
            mismatches.append((mask, counts, atom, by_count[counts]))
    masses = reduced_count_masses(reduced)
    return {
        "n": len(k),
        "count_states": len(masses),
        "events": len(atoms),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:5],
        "mobius_sum": str(sum(atoms)),
        "reduced_sum": str(probability_sum_from_count_masses(masses)),
        "minimum_atom": str(min(atoms)),
    }


if __name__ == "__main__":
    # A tiny smoke example.  The full test suite has the real comparisons.
    sizes = (2, 3, 1)
    rows = ((1, 0), (0, 1), (1, 1))
    c_mat = ((Fraction(1, 30), Fraction(1, 70)), (Fraction(1, 70), Fraction(-1, 40)))
    print(compare_mobius_to_reduced(Fraction(1, 3), c_mat, sizes, rows))
