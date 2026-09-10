#!/usr/bin/env python3
"""Small independent symbolic differentiator for the issue-74 preflight.

This deliberately does not import or reuse the certificate Jet implementation.
It constructs an expression DAG, applies elementary differentiation rules, and
only then evaluates the resulting derivative expressions with Decimal.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache


@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple

    def __add__(self, other):
        return add(self, expression(other))

    def __radd__(self, other):
        return add(expression(other), self)

    def __neg__(self):
        return neg(self)

    def __sub__(self, other):
        return add(self, neg(expression(other)))

    def __rsub__(self, other):
        return add(expression(other), neg(self))

    def __mul__(self, other):
        return mul(self, expression(other))

    def __rmul__(self, other):
        return mul(expression(other), self)

    def __truediv__(self, other):
        return mul(self, power(expression(other), -1))

    def __pow__(self, exponent):
        return power(self, exponent)

    def log(self):
        return Expr("log", (self,))


ZERO = Expr("const", (Decimal(0),))
ONE = Expr("const", (Decimal(1),))


def expression(value):
    if isinstance(value, Expr):
        return value
    if hasattr(value, "numerator") and hasattr(value, "denominator"):
        value = Decimal(value.numerator) / Decimal(value.denominator)
    elif not isinstance(value, Decimal):
        value = Decimal(str(value))
    if value == 0:
        return ZERO
    if value == 1:
        return ONE
    return Expr("const", (value,))


def variable(name):
    return Expr("var", (name,))


def add(left, right):
    if left == ZERO:
        return right
    if right == ZERO:
        return left
    if left.op == right.op == "const":
        return expression(left.args[0] + right.args[0])
    return Expr("add", (left, right))


def neg(value):
    if value == ZERO:
        return ZERO
    if value.op == "const":
        return expression(-value.args[0])
    return Expr("neg", (value,))


def mul(left, right):
    if left == ZERO or right == ZERO:
        return ZERO
    if left == ONE:
        return right
    if right == ONE:
        return left
    if left.op == right.op == "const":
        return expression(left.args[0] * right.args[0])
    return Expr("mul", (left, right))


def power(base, exponent):
    if not isinstance(exponent, int):
        raise TypeError("only integer powers are supported")
    if exponent == 0:
        return ONE
    if exponent == 1:
        return base
    if base.op == "const":
        return expression(base.args[0] ** exponent)
    return Expr("pow", (base, exponent))


@lru_cache(maxsize=None)
def derivative(expr, name):
    if expr.op == "const":
        return ZERO
    if expr.op == "var":
        return ONE if expr.args[0] == name else ZERO
    if expr.op == "add":
        return derivative(expr.args[0], name) + derivative(expr.args[1], name)
    if expr.op == "neg":
        return -derivative(expr.args[0], name)
    if expr.op == "mul":
        left, right = expr.args
        return derivative(left, name) * right + left * derivative(right, name)
    if expr.op == "pow":
        base, exponent = expr.args
        return expression(exponent) * power(base, exponent - 1) * derivative(base, name)
    if expr.op == "log":
        base = expr.args[0]
        return derivative(base, name) / base
    raise ValueError(expr.op)


@lru_cache(maxsize=None)
def evaluate(expr, values):
    mapping = dict(values)
    if expr.op == "const":
        return expr.args[0]
    if expr.op == "var":
        return mapping[expr.args[0]]
    if expr.op == "add":
        return evaluate(expr.args[0], values) + evaluate(expr.args[1], values)
    if expr.op == "neg":
        return -evaluate(expr.args[0], values)
    if expr.op == "mul":
        return evaluate(expr.args[0], values) * evaluate(expr.args[1], values)
    if expr.op == "pow":
        return evaluate(expr.args[0], values) ** expr.args[1]
    if expr.op == "log":
        return evaluate(expr.args[0], values).ln()
    raise ValueError(expr.op)


def polynomial(coefficients, exponents, q):
    x, y, z = (expression(8) * coordinate for coordinate in q)
    result = ZERO
    for coefficient, (i, j, k) in zip(coefficients, exponents):
        result += expression(coefficient) * x**i * y**j * z**k
    return result


def residuals(exponents, uc, vc, wc, c2):
    x, y, z, t = (variable(name) for name in ("x", "y", "z", "t"))
    q = (x, y, z)
    source = ZERO
    lv = ZERO
    lw = ZERO
    for a, b in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        left = expression(a) / 2 - x
        right = expression(b) / 2 - y
        off = t / 16 - z
        determinant = left * right - off * off
        weight = expression(a * b) * determinant
        r00 = right / determinant
        r01 = -off / determinant
        r11 = left / determinant
        tx = expression(1) / 64 * r00
        tz = expression(1) / 128 * t * r00 + expression(1) / 64 * r01
        ty = t * t / 256 * r00 + t / 64 * r01 + expression(1) / 64 * r11
        image = (tx, ty, tz)
        source += -weight * weight.log() + weight * polynomial(uc, exponents, image)
        lv += weight * polynomial(vc, exponents, image)
        lw += weight * polynomial(wc, exponents, image)
    uq = polynomial(uc, exponents, q)
    vq = polynomial(vc, exponents, q)
    wq = polynomial(wc, exponents, q)
    r0 = source - uq
    r1 = derivative(source, "t") - vq + lv
    r2 = derivative(derivative(source, "t"), "t") + 2 * derivative(lv, "t") - expression(c2) - wq + lw
    return {"r0": r0, "r1": r1, "r2": r2}


def fixture_values(exponents, uc, vc, wc, c2, t_value):
    residual = residuals(exponents, uc, vc, wc, c2)
    at = tuple(sorted({"x": Decimal(0), "y": Decimal(0), "z": Decimal(0), "t": t_value}.items()))
    components = {
        "xx": ("x", "x"), "yy": ("y", "y"), "zz": ("z", "z"),
        "xy": ("x", "y"), "xz": ("x", "z"), "yz": ("y", "z"),
    }
    return {
        "r0_hessian": {name: evaluate(derivative(derivative(residual["r0"], i), j), at) for name, (i, j) in components.items()},
        "r1_hessian": {name: evaluate(derivative(derivative(residual["r1"], i), j), at) for name, (i, j) in components.items()},
        "r2": evaluate(residual["r2"], at),
    }
