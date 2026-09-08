"""Dependency-free exact certificate for the equicorrelation trivial block.

The script checks the rational reduction of the determinant to a quartic in
lambda, its Bernstein coefficients, and the algebraic rewrites used by the
positivity proof. Coefficients are Fractions; no floating point or external
computer-algebra package is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb


NVAR = 4  # lambda, rho, A=W, B=T+W


@dataclass(frozen=True)
class Poly:
    terms: dict[tuple[int, ...], Fraction]

    def __init__(self, value=0):
        if isinstance(value, Poly):
            object.__setattr__(self, "terms", dict(value.terms))
        elif isinstance(value, dict):
            object.__setattr__(
                self,
                "terms",
                {m: Fraction(c) for m, c in value.items() if c},
            )
        else:
            c = Fraction(value)
            object.__setattr__(self, "terms", {} if not c else {(0,) * NVAR: c})

    def __add__(self, other):
        if isinstance(other, Rat):
            return Rat(self) + other
        other = Poly(other)
        out = dict(self.terms)
        for m, c in other.terms.items():
            out[m] = out.get(m, Fraction(0)) + c
            if not out[m]:
                del out[m]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        if isinstance(other, Rat):
            return Rat(self) - other
        return self + (-Poly(other))

    def __rsub__(self, other):
        if isinstance(other, Rat):
            return other - Rat(self)
        return Poly(other) - self

    def __mul__(self, other):
        if isinstance(other, Rat):
            return Rat(self) * other
        other = Poly(other)
        out: dict[tuple[int, ...], Fraction] = {}
        for ma, ca in self.terms.items():
            for mb, cb in other.terms.items():
                m = tuple(a + b for a, b in zip(ma, mb))
                out[m] = out.get(m, Fraction(0)) + ca * cb
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        if exponent < 0:
            raise ValueError("negative polynomial exponent")
        result = Poly(1)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def __truediv__(self, other):
        if isinstance(other, Rat):
            return Rat(self) / other
        return Rat(self, Poly(other))

    def __eq__(self, other):
        return self.terms == Poly(other).terms


@dataclass(frozen=True)
class Rat:
    num: Poly
    den: Poly

    def __init__(self, num=0, den=1):
        object.__setattr__(self, "num", Poly(num))
        object.__setattr__(self, "den", Poly(den))

    @staticmethod
    def lift(value):
        return value if isinstance(value, Rat) else Rat(value)

    def __add__(self, other):
        other = Rat.lift(other)
        return Rat(self.num * other.den + other.num * self.den, self.den * other.den)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.num, self.den)

    def __sub__(self, other):
        return self + (-Rat.lift(other))

    def __rsub__(self, other):
        return Rat.lift(other) - self

    def __mul__(self, other):
        other = Rat.lift(other)
        return Rat(self.num * other.num, self.den * other.den)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rat.lift(other)
        return Rat(self.num * other.den, self.den * other.num)

    def __rtruediv__(self, other):
        return Rat.lift(other) / self

    def __pow__(self, exponent: int):
        if exponent < 0:
            return Rat(self.den ** (-exponent), self.num ** (-exponent))
        return Rat(self.num**exponent, self.den**exponent)

    def equals(self, other) -> bool:
        other = Rat.lift(other)
        return self.num * other.den == other.num * self.den


def variable(index: int) -> Poly:
    powers = [0] * NVAR
    powers[index] = 1
    return Poly({tuple(powers): Fraction(1)})


ell, rho, A, B = (variable(i) for i in range(NVAR))
T = B - A
S = 2 * rho**2 + 5 * rho + 2


def raw_bernstein_numerators() -> list[Poly]:
    """Return d_i b_i with d=(1,4,6,4,1)."""
    b0 = rho * (3 * A * rho**2 + 6 * A * rho + 2 * (rho - 1) ** 2)
    n1 = (
        4 * T * rho**3
        + 7 * T * rho**2
        - 2 * T * rho
        - 4 * A**2 * rho**3
        - 10 * A**2 * rho**2
        - 4 * A**2 * rho
        + 10 * A * rho**3
        + 22 * A * rho**2
        + 4 * A * rho
        + 2 * rho**4
        - 4 * rho**2
        + 2
    )
    n2 = -(
        8 * T * A * rho**3
        + 20 * T * A * rho**2
        + 8 * T * A * rho
        - 12 * T * rho**3
        - 10 * T * rho**2
        - 7 * T * rho
        + 2 * T
        + 8 * A**2 * rho**3
        + 20 * A**2 * rho**2
        + 8 * A**2 * rho
        + 2 * A * rho**4
        - 19 * A * rho**3
        - 20 * A * rho**2
        - 19 * A * rho
        + 2 * A
        - 4 * rho**4
        + 4 * rho**3
        + 4 * rho
        - 4
    )
    n3 = -(
        4 * T**2 * rho**3
        + 10 * T**2 * rho**2
        + 4 * T**2 * rho
        + 8 * T * A * rho**3
        + 20 * T * A * rho**2
        + 8 * T * A * rho
        - 6 * T * rho**3
        - 15 * T * rho**2
        - 6 * T * rho
        + 4 * A**2 * rho**3
        + 10 * A**2 * rho**2
        + 4 * A**2 * rho
        - 4 * A * rho**3
        - 22 * A * rho**2
        - 10 * A * rho
        - 2 * rho**4
        + 4 * rho**2
        - 2
    )
    b4 = rho * ((6 * rho + 3) * B + 2 * (rho - 1) ** 2)
    return [b0, n1, n2, n3, b4]


def check_rewrites(ns: list[Poly]) -> None:
    C = 12 * rho**3 + 10 * rho**2 + 7 * rho - 2
    D0 = (rho - 1) ** 2 * (rho**2 + rho + 1)
    expected = [
        rho * (3 * A * rho**2 + 6 * A * rho + 2 * (rho - 1) ** 2),
        rho * (4 * rho**2 + 7 * rho - 2) * B
        + rho * S * A * (3 - 2 * A)
        + 2 * (rho**2 - 1) ** 2,
        (C - 4 * rho * S * A) * B
        + rho * (-2 * rho**3 + 7 * rho**2 + 10 * rho + 12) * A
        + 4 * D0,
        2 * (rho**2 - 1) ** 2
        + 3 * rho * S * B
        - 2 * rho * S * B**2
        + rho * (-2 * rho**2 + 7 * rho + 4) * A,
        rho * ((6 * rho + 3) * B + 2 * (rho - 1) ** 2),
    ]
    assert all(left == right for left, right in zip(ns, expected))

    assert 3 * C - 4 * rho * S == 28 * rho**3 + 10 * rho**2 + 13 * rho - 6
    assert 12 * D0 + rho * (-2 * rho**3 + 7 * rho**2 + 10 * rho + 12) == (
        10 * rho**4 - 5 * rho**3 + 10 * rho**2 + 12
    )
    assert (
        3 * (2 * rho + 1) * (rho + 2) ** 2 * (rho + 1) ** 2
        - rho * S * (rho - 1) ** 2
        == 4 * rho**5
        + 38 * rho**4
        + 102 * rho**3
        + 110 * rho**2
        + 58 * rho
        + 12
    )


def check_determinant_reduction(ns: list[Poly]) -> None:
    """Check Phi=-2P/[lambda*rho*(lambda-1)*(rho+2)*(2rho+1)]."""
    mu = Rat(ell, rho * (1 - ell) + ell)
    x = ell
    m = mu
    a0neg = 3 * x * m - 2 * x - m
    b0neg = 3 * x * m - x - 2 * m

    fll_num = (
        5 * x**2 * m**2
        - 5 * x**2 * m
        + x**2
        - 2 * x * m**3
        - 2 * x * m**2
        + 2 * x * m
        + m**3
    )
    Fll = -4 * fll_num / (x * (x - 1) * a0neg * b0neg)
    Flm = 2 * (x**2 - 4 * x * m + x + 2 * m) / (a0neg * b0neg)
    fmm_num = (
        2 * x**4
        - 8 * x**3 * m
        + 9 * x**2 * m**2
        + 3 * x**2 * m
        - 9 * x * m**2
        + x * m
        + 2 * m**2
    )
    Fmm = -fmm_num / (m * (m - 1) * a0neg * b0neg)

    Nll = Fll - 2 * (A + m * T)
    Nlm = Flm - 2 * (A + x * T)
    phi = Nll * Fmm - Nlm**2

    bs = [Rat(n, d) for n, d in zip(ns, (1, 4, 6, 4, 1))]
    P = Rat(0)
    for i, bi in enumerate(bs):
        P += comb(4, i) * bi * x**i * (1 - x) ** (4 - i)
    expected = -2 * P / (x * rho * (x - 1) * (rho + 2) * (2 * rho + 1))
    assert phi.equals(expected)


def main() -> None:
    ns = raw_bernstein_numerators()
    check_rewrites(ns)
    check_determinant_reduction(ns)
    print("PASS: exact rational determinant reduction and positivity rewrites verified")


if __name__ == "__main__":
    main()
