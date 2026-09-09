from fractions import Fraction
from itertools import combinations


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def inv2(m):
    d = det2(m)
    return [[m[1][1] / d, -m[0][1] / d],
            [-m[1][0] / d, m[0][0] / d]]


def event_matrix_2(k, bits):
    out = [[k[i][j] for j in range(2)] for i in range(2)]
    for i, bit in enumerate(bits):
        if bit == 0:
            out[i][i] -= 1
    return out


def p_complete_2(k, bits):
    zeros = 2 - sum(bits)
    sign = -1 if zeros % 2 else 1
    return sign * det2(event_matrix_2(k, bits))


def rank_3x3(m):
    nonzero_2_minor = False
    for rows in combinations(range(3), 2):
        for cols in combinations(range(3), 2):
            minor = [[m[r][c] for c in cols] for r in rows]
            if det2(minor) != 0:
                nonzero_2_minor = True
    det3 = (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )
    if det3 != 0:
        return 3
    return 2 if nonzero_2_minor else 1


def main():
    print("INPUT commit_current=7bd5962bbb2020ce47fbe286adda7dfe02f9645d")
    print("INPUT commit_historical_proof=4e1369ef2a59ccfaba3ca8fce95d85e78857bf78")
    print("ALGORITHM exact Fraction arithmetic from complete-event determinant p(S)=(-1)^(n-|S|) det(K-E_{S^c}); no author code import")

    c = [[Fraction(1, 2), Fraction(1, 10)],
         [Fraction(1, 10), Fraction(1, 2)]]
    order = [(0, 0), (1, 0), (0, 1), (1, 1)]
    probs = [p_complete_2(c, bits) for bits in order]
    print("CHECK M mu_00_10_01_11=", probs)
    print("CHECK M mu_sum=", sum(probs))

    signed = []
    for bits in order:
        y = event_matrix_2(c, bits)
        inv = inv2(y)
        sign = -1 if (2 - sum(bits)) % 2 else 1
        signed.append(sign * inv[0][1])
    print("CHECK M signed_inverse_offdiag=", signed)
    print("CHECK M inner_d_G12=", sum(signed))

    k_plus = [[Fraction(1, 2), Fraction(1, 10)],
              [Fraction(1, 10), Fraction(1, 2)]]
    k_minus = [[Fraction(1, 2), Fraction(-1, 10)],
               [Fraction(-1, 10), Fraction(1, 2)]]
    p_plus = [p_complete_2(k_plus, bits) for bits in order]
    p_minus = [p_complete_2(k_minus, bits) for bits in order]
    print("CHECK N input_p_plus=", p_plus)
    print("CHECK N input_p_minus=", p_minus)
    a0 = [[Fraction(1, 2), Fraction(1, 5)],
          [Fraction(1, 5), Fraction(1, 2)]]
    theta = Fraction(1, 2)
    out_plus_offdiag = theta * k_plus[0][1] + (1 - theta) * a0[0][1]
    out_minus_offdiag = theta * k_minus[0][1] + (1 - theta) * a0[0][1]
    out_plus_p11 = Fraction(1, 4) - out_plus_offdiag * out_plus_offdiag
    out_minus_p11 = Fraction(1, 4) - out_minus_offdiag * out_minus_offdiag
    print("CHECK N output_offdiag_plus_minus=", [out_plus_offdiag, out_minus_offdiag])
    print("CHECK N output_p11_plus_minus=", [out_plus_p11, out_minus_p11])

    b_int = [[1, 1, 2],
             [2, 0, 3],
             [1, -1, 1]]
    print("CHECK I active_B_rank=", rank_3x3(b_int))
    print("CHECK I row2_minus_row1_minus_row3=", [b_int[1][j] - b_int[0][j] - b_int[2][j] for j in range(3)])
    active_columns_nonzero = [any(b_int[i][j] != 0 for i in range(3)) for j in range(3)]
    print("CHECK I first_three_active_columns_nonzero=", active_columns_nonzero)
    frob_sq_unscaled = sum(x * x for row in b_int for x in row)
    print("CHECK I frobenius_sq_unscaled=", frob_sq_unscaled)
    print("CHECK I frobenius_sq_scaled=", Fraction(frob_sq_unscaled, 10000))
    print("STOPPING_CONDITION completed fixed four-state and low-cost fixture checks")


if __name__ == "__main__":
    main()
