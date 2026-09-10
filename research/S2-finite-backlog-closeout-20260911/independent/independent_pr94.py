#!/usr/bin/env python3
"""Independent standard-library reconstruction of the PR94 channel arithmetic."""

from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json


def trim(poly):
    out = list(map(Q, poly))
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def p_add(left, right, sign=1):
    out = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += sign * value
    return trim(out)


def p_mul(left, right):
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return trim(out)


def p_scale(poly, scalar):
    return trim([Q(scalar) * value for value in poly])


def p_pow(poly, exponent):
    out = (Q(1),)
    for _ in range(exponent):
        out = p_mul(out, poly)
    return out


def parity(perm):
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inversions & 1 else 1


def determinant(matrix):
    n = len(matrix)
    total = (Q(0),)
    for perm in permutations(range(n)):
        term = (Q(1),)
        for row, column in enumerate(perm):
            term = p_mul(term, matrix[row][column])
        total = p_add(total, term, parity(perm))
    return total


def fixed_det(matrix):
    return determinant([[(Q(value),) for value in row] for row in matrix])[0]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def matadd(left, right, sign=1):
    return [[left[i][j] + sign * right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def scale(matrix, scalar):
    return [[Q(scalar) * value for value in row] for row in matrix]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    rows = [list(map(Q, matrix[i])) + eye(n)[i] for i in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(n):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [rows[row][j] - factor * rows[column][j] for j in range(2 * n)]
    return [row[n:] for row in rows]


def outer(vector):
    return [[x * y for y in vector] for x in vector]


def positive_definite(matrix):
    return all(fixed_det([row[:size] for row in matrix[:size]]) > 0 for size in range(1, len(matrix) + 1))


def event_polynomials(matrix):
    n = len(matrix)
    answer = []
    for mask in range(1 << n):
        shifted = [[tuple(matrix[i][j]) for j in range(n)] for i in range(n)]
        for i in range(n):
            if not (mask & (1 << i)):
                shifted[i][i] = p_add(shifted[i][i], (Q(1),), -1)
        answer.append(p_scale(determinant(shifted), -1 if (n - mask.bit_count()) & 1 else 1))
    return answer


def fixed_event_probabilities(matrix):
    return [poly[0] for poly in event_polynomials([[(value,) for value in row] for row in matrix])]


def joint_polynomials(A, C, B):
    left, right = len(A), len(C)
    matrix = []
    for i in range(left + right):
        row = []
        for j in range(left + right):
            if i < left and j < left:
                row.append((A[i][j],))
            elif i >= left and j >= left:
                row.append((C[i - left][j - left],))
            elif i < left:
                row.append((Q(0), B[i][j - left]))
            else:
                row.append((Q(0), B[j][i - left]))
        matrix.append(row)
    events = event_polynomials(matrix)
    return {(i, j): events[i + (j << left)] for i in range(1 << left) for j in range(1 << right)}


def refine(q0, q1):
    difference = [q1[i] - q0[i] for i in range(len(q0))]
    positive = [i for i, value in enumerate(difference) if value > 0]
    negative = [i for i, value in enumerate(difference) if value < 0]
    mass = sum((difference[i] for i in positive), Q(0))
    rows = []
    for p, n in product(positive, negative):
        gamma = difference[p] * (-difference[n]) / mass
        alpha = [Q(0)] * len(q0)
        alpha[p], alpha[n] = gamma / difference[p], gamma / (-difference[n])
        channel_mass = sum((q0[i] * alpha[i] for i in range(len(q0))), Q(0))
        a = q0[p] * alpha[p] / channel_mass
        theta = gamma / channel_mass
        rows.append((channel_mass, a, theta, p, n, alpha))
    assert sum((row[0] for row in rows), Q(0)) == 1
    return rows


def local_channel(eta):
    v = [Q(3, 5), Q(4, 5)]
    vv = outer(v)
    residual = scale(matadd(eye(2), vv, -1), eta)
    return [fixed_event_probabilities(matadd(residual, scale(vv, bit))) for bit in (0, 1)]


def log_interval(value, terms=48):
    value = Q(value)
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1

    def unit(x):
        z = (x - 1) / (x + 1)
        partial = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), Q(0))
        tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
        return partial, partial + tail

    lo, hi = unit(value)
    l2, u2 = unit(Q(2))
    if exponent >= 0:
        return lo + exponent * l2, hi + exponent * u2
    return lo + exponent * u2, hi + exponent * l2


def interval_scale(interval, scalar):
    scalar = Q(scalar)
    return ((scalar * interval[0], scalar * interval[1]) if scalar >= 0
            else (scalar * interval[1], scalar * interval[0]))


def main():
    # Asymmetric ternary refinement and all 16 affine identities.
    q0 = [Q(1, 2), Q(1, 3), Q(1, 6)]
    q1 = [Q(1, 4), Q(1, 4), Q(1, 2)]
    selectors = refine(q0, q1)
    selector_parameters = [(row[0], row[1], row[2]) for row in selectors]
    assert selector_parameters == [(Q(5, 8), Q(1, 5), Q(2, 5)),
                                   (Q(3, 8), Q(1, 9), Q(2, 9))]

    K = [[(Q(2, 5), Q(1, 10)), (Q(1, 10), Q(1, 20))],
         [(Q(1, 10), Q(1, 20)), (Q(3, 5), -Q(1, 15))]]
    input_events = event_polynomials(K)
    observed = []
    for y1, y2 in product(range(3), repeat=2):
        poly = (Q(0),)
        for mask in range(4):
            coefficient = (q0 if not (mask & 1) else q1)[y1] * (q0 if not (mask & 2) else q1)[y2]
            poly = p_add(poly, p_scale(input_events[mask], coefficient))
        observed.append(poly)

    refined_identities = 0
    for left, right in product(selectors, repeat=2):
        c1, a1, th1, p1, n1, alpha1 = left
        c2, a2, th2, p2, n2, alpha2 = right
        marginal1 = p_add((a1,), p_scale(K[0][0], th1))
        marginal2 = p_add((a2,), p_scale(K[1][1], th2))
        p11 = p_add(p_mul(marginal1, marginal2), p_scale(p_pow(K[0][1], 2), th1 * th2), -1)
        refined = [p_add(p_add(p_add((Q(1),), marginal1, -1), marginal2, -1), p11),
                   p_add(marginal1, p11, -1), p_add(marginal2, p11, -1), p11]
        for output_mask in range(4):
            y1 = p1 if output_mask & 1 else n1
            y2 = p2 if output_mask & 2 else n2
            lhs = p_scale(observed[3 * y1 + y2], alpha1[y1] * alpha2[y2])
            rhs = p_scale(refined[output_mask], c1 * c2)
            assert lhs == rhs
            refined_identities += 1
    assert refined_identities == 16

    # Base and two actual 64-event observed-mode laws.
    A = [[Q(1, 3), Q(1, 6)], [Q(1, 6), Q(1, 3)]]
    C = [[Q(2, 5), Q(1, 48)], [Q(1, 48), Q(3, 5)]]
    B = [[Q(1, 12), Q(1, 12)], [Q(1, 6), -Q(1, 12)]]
    W = [[Q(3, 5), Q(0)], [Q(4, 5), Q(0)], [Q(0), Q(1)]]
    base = joint_polynomials(A, C, B)
    mode_counts = []
    observed_matrices = None
    for eta_left, eta_right in ((Q(1, 2), Q(1, 2)), (Q(1, 4), Q(2, 3))):
        WWT = matmul(W, transpose(W))
        AL = matadd(scale(matadd(eye(3), WWT, -1), eta_left), matmul(matmul(W, A), transpose(W)))
        CL = matadd(scale(matadd(eye(3), WWT, -1), eta_right), matmul(matmul(W, C), transpose(W)))
        BL = matmul(matmul(W, B), transpose(W))
        assert positive_definite(AL) and positive_definite(matadd(eye(3), AL, -1))
        assert positive_definite(CL) and positive_definite(matadd(eye(3), CL, -1))
        actual = joint_polynomials(AL, CL, BL)
        qleft, qright = local_channel(eta_left), local_channel(eta_right)
        count = 0
        for (i, j), polynomial in actual.items():
            rhs = (Q(0),)
            for (x, y), base_poly in base.items():
                if (i >> 2) == (x >> 1) and (j >> 2) == (y >> 1):
                    weight = qleft[x & 1][i & 3] * qright[y & 1][j & 3]
                    rhs = p_add(rhs, p_scale(base_poly, weight))
            assert polynomial == rhs
            count += 1
        mode_counts.append(count)
        if eta_left == eta_right == Q(1, 2):
            observed_matrices = (AL, CL, BL)
    assert mode_counts == [64, 64]

    AL, CL, BL = observed_matrices
    expected_AL = [[Q(11, 25), -Q(2, 25), Q(1, 10)], [-Q(2, 25), Q(59, 150), Q(2, 15)], [Q(1, 10), Q(2, 15), Q(1, 3)]]
    expected_CL = [[Q(58, 125), -Q(6, 125), Q(1, 80)], [-Q(6, 125), Q(109, 250), Q(1, 60)], [Q(1, 80), Q(1, 60), Q(3, 5)]]
    expected_BL = [[Q(3, 100), Q(1, 25), Q(1, 20)], [Q(1, 25), Q(4, 75), Q(1, 15)], [Q(1, 10), Q(2, 15), -Q(1, 12)]]
    assert (AL, CL, BL) == (expected_AL, expected_CL, expected_BL)

    schur_K = matmul(matmul(transpose(B), inverse(A)), B)
    schur_I = matmul(matmul(transpose(B), inverse(matadd(eye(2), A, -1))), B)
    det_K = determinant([[(C[i][j], -schur_K[i][j]) for j in range(2)] for i in range(2)])
    det_I = determinant([[((eye(2)[i][j] - C[i][j]), -schur_I[i][j]) for j in range(2)] for i in range(2)])
    assert det_K == (Q(13799, 57600), -Q(4900, 57600), Q(300, 57600))
    assert det_I == (Q(13799, 57600), -Q(2092, 57600), Q(60, 57600))
    assert (Q(49, 6) - 4)**2 < Q(4657, 225) < (Q(49, 6) - 3)**2
    assert sum(det_K[i] * Q(3)**i for i in range(3)) > 0
    assert sum(det_K[i] * Q(4)**i for i in range(3)) < 0
    assert sum(det_I[i] * Q(4)**i for i in range(3)) > 0

    # Selected observed pattern, eight conditional laws, and signed fiber.
    shifted_AL = [row[:] for row in AL]
    shifted_AL[2][2] -= 1  # event mask 3: first two selected, third absent
    M = matmul(matmul(transpose(BL), inverse(shifted_AL)), BL)
    shifted_A = [row[:] for row in A]
    shifted_A[1][1] -= 1  # base event mask 1
    expected_M = matmul(matmul(W, matmul(matmul(transpose(B), inverse(shifted_A)), B)), transpose(W))
    assert M == expected_M
    assert matmul(matmul(transpose(B), inverse(shifted_A)), B) == [[Q(0), Q(1, 24)], [Q(1, 24), Q(0)]]

    conditional_polys = event_polynomials([[(CL[i][j], -M[i][j]) for j in range(3)] for i in range(3)])
    v = [Q(3, 5), Q(4, 5)]
    pstar, difference = [], []
    one_minus_two_s_squared = (Q(1), Q(-4), Q(4))
    for mask in range(8):
        h = 2 * sum((v[i]**2 for i in range(2) if mask & (1 << i)), Q(0)) - 1
        z = (mask >> 2) & 1
        p = (Q(3, 5) if z else Q(2, 5)) / 4 * (1 - h / 5)
        delta = Q(1, 48)**2 / 2 * (1 - 2 * z) * h
        expected = p_add((p,), p_scale(one_minus_two_s_squared, delta))
        assert conditional_polys[mask] == expected and p > 0 and p + delta > 0
        derivative_at_half = conditional_polys[mask][1] + 2 * conditional_polys[mask][2] * Q(1, 2)
        assert derivative_at_half == 0
        pstar.append(p)
        difference.append(delta)
    assert sum(pstar, Q(0)) == 1 and sum(difference, Q(0)) == 0 and any(difference)
    fiber = (Q(0), Q(0))
    for p, delta in zip(pstar, difference):
        term = interval_scale(log_interval((p + delta) / p), -8 * delta)
        fiber = (fiber[0] + term[0], fiber[1] + term[1])
    assert fiber[1] < 0

    constant = 4 * Q(1, 6)**4 * Q(337, 625)
    assert constant == Q(337, 202500)

    U = [[Q(7, 40), -Q(22, 125)], [Q(339, 1000), Q(13, 250)], [Q(229, 500), -Q(231, 500)]]
    V = [[Q(141, 200), Q(981, 1000)], [-Q(343, 1000), Q(113, 250)], [Q(187, 250), Q(577, 1000)]]
    pair_minors = []
    for matrix in (U, V):
        group = []
        for i, j in combinations(range(3), 2):
            group.append(matrix[i][0] * matrix[j][1] - matrix[i][1] * matrix[j][0])
        pair_minors.append(group)
    assert all(value != 0 for group in pair_minors for value in group)

    result = {
        "status": "PASS",
        "head": "a9db9f98dc6dac766dd9b214f056ee9b30109b23",
        "asymmetric_selector_parameters": [[str(x) for x in row] for row in selector_parameters],
        "refined_polynomial_identities": refined_identities,
        "observed_mode_event_laws": mode_counts,
        "explicit_3_plus_3_matrices": {"A": [[str(x) for x in row] for row in AL],
                                        "C": [[str(x) for x in row] for row in CL],
                                        "B": [[str(x) for x in row] for row in BL]},
        "maximal_endpoint": "49/6 - sqrt(4657)/15",
        "maximal_endpoint_exactly_bracketed_3_4": True,
        "negative_fiber_interval": [str(fiber[0]), str(fiber[1])],
        "conditional_fisher_derivatives_at_half_all_zero": True,
        "curvature_coefficient": str(constant),
        "original_frame_pair_minors": [[str(x) for x in row] for row in pair_minors],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
