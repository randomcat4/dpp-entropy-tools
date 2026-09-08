"""Finite standard-library replay for D10-U10k.

This checks the quartic identity against direct event differentiation at
frozen rational points.  It is a sanity check, not the universal proof.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json


class Jet:
    def __init__(self, value, gradient=(Q(0), Q(0)), hessian=None):
        self.v = Q(value)
        self.g = tuple(map(Q, gradient))
        self.h = hessian or ((Q(0), Q(0)), (Q(0), Q(0)))

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.v + other.v,
            tuple(self.g[i] + other.g[i] for i in range(2)),
            tuple(
                tuple(self.h[i][j] + other.h[i][j] for j in range(2))
                for i in range(2)
            ),
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet(
            -self.v,
            tuple(-x for x in self.g),
            tuple(tuple(-x for x in row) for row in self.h),
        )

    def __sub__(self, other):
        return self + (-other if isinstance(other, Jet) else -Q(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.v * other.v,
            tuple(self.g[i] * other.v + self.v * other.g[i] for i in range(2)),
            tuple(
                tuple(
                    self.h[i][j] * other.v
                    + self.g[i] * other.g[j]
                    + self.g[j] * other.g[i]
                    + self.v * other.h[i][j]
                    for j in range(2)
                )
                for i in range(2)
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, integer):
        return self * Q(1, integer)

    def __pow__(self, exponent):
        result = Jet(1)
        for _ in range(exponent):
            result *= self
        return result


def dec(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


def direct_hessian(alpha_value, beta_value):
    alpha = Jet(alpha_value, (1, 0))
    beta = Jet(beta_value, (0, 1))
    u = alpha + 2 * beta - 3 * alpha * beta
    v = 2 * alpha + beta - 3 * alpha * beta
    atoms = [
        (1 - alpha) * (1 - beta) ** 2,
        (1 - beta) * u / 3,
        beta * v / 3,
        alpha * beta**2,
    ]
    multiplicities = (1, 3, 3, 1)
    assert sum(m * atom.v for m, atom in zip(multiplicities, atoms)) == 1
    matrix = [[Decimal(0), Decimal(0)], [Decimal(0), Decimal(0)]]
    for m, atom in zip(multiplicities, atoms):
        p = dec(atom.v)
        for i in range(2):
            for j in range(2):
                matrix[i][j] += Decimal(m) * (
                    dec(atom.g[i]) * dec(atom.g[j]) / p
                    + dec(atom.h[i][j]) * p.ln()
                )
    return matrix


def quartic(alpha, beta):
    q = beta / (1 - beta)
    t = (alpha / (1 - alpha)) / q
    td = dec(t)
    qd = dec(q)
    one = Decimal(1)
    e = (one + (td - one) ** 2 / (3 * (2 * td + one))).ln()
    d = (one + (td - one) ** 2 / (3 * td * (td + 2))).ln()
    qpoly = (2 * td + one) * (td + 2)
    pd = 2 * td**4 - 7 * td**3 - 10 * td**2 - 12 * td
    pe = -12 * td**3 - 10 * td**2 - 7 * td + 2
    c0 = 2 * td * (2 * (td - one) ** 2 + 3 * e * (2 * td + one))
    c4 = 2 * td * (2 * (td - one) ** 2 + 3 * d * td * (td + 2))
    c3 = 2 * (
        2 * (td**2 - one) ** 2
        + d * td * qpoly * (3 - 2 * d)
        + e * td * (4 * td**2 + 7 * td - 2)
    )

    # c_1(t;d,e)=t^4 c_3(1/t;e,d).
    ti = one / td
    qi = (2 * ti + one) * (ti + 2)
    c1 = td**4 * 2 * (
        2 * (ti**2 - one) ** 2
        + e * ti * qi * (3 - 2 * e)
        + d * ti * (4 * ti**2 + 7 * ti - 2)
    )
    c2 = 2 * (
        4 * (td - one) ** 2 * (td**2 + td + one)
        - d * pd
        + e * (-pe - 4 * d * td * qpoly)
    )
    denominator = qd * td * (qd + one) ** 2 * (td + 2) * (2 * td + one)
    numerator = c0 + c1 * qd + c2 * qd**2 + c3 * qd**3 + c4 * qd**4
    return numerator / denominator, (c0, c1, c2, c3, c4)


def main():
    cases = [
        (Q(1, 5), Q(2, 5)),
        (Q(2, 5), Q(1, 5)),
        (Q(1, 1000), Q(3, 4)),
        (Q(3, 4), Q(1, 1000)),
        (Q(999, 1000), Q(1, 3)),
        (Q(1, 3), Q(999, 1000)),
        (Q(500001, 1000000), Q(499999, 1000000)),
    ]
    rows = []
    with localcontext() as context:
        context.prec = 100
        for alpha, beta in cases:
            matrix = direct_hessian(alpha, beta)
            direct = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
            replay, coefficients = quartic(alpha, beta)
            error = abs(direct - replay)
            assert direct > 0
            assert min(coefficients) > 0
            assert error < Decimal("1e-85") * max(Decimal(1), abs(direct))
            rows.append(
                {
                    "alpha": str(alpha),
                    "beta": str(beta),
                    "Delta_T": str(direct),
                    "identity_error": str(error),
                    "minimum_coefficient": str(min(coefficients)),
                }
            )
    print(json.dumps({"status": "PASS_SCOUT_NOT_PROOF", "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
