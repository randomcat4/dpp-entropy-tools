#!/usr/bin/env python3
"""Independent exact Bernstein reconstruction for the alpha=1/10 kernel."""

from fractions import Fraction as F
from math import comb, gcd
from functools import reduce
import json
import time

import sympy as sp

from independent_pr116_light import symbolic_types


EXPECTED_MIN = 27030487060546875000000000000000000000000000000000000


def lcm(a, b):
    return abs(a // gcd(a, b) * b)


def transform_axis(data, degrees, axis):
    nx, ny, nz = degrees
    sizes = (nx + 1, ny + 1, nz + 1)
    out = [[[F(0) for _ in range(sizes[2])] for __ in range(sizes[1])] for ___ in range(sizes[0])]
    for i in range(sizes[0]):
        for j in range(sizes[1]):
            for k in range(sizes[2]):
                index = (i, j, k)[axis]
                degree = degrees[axis]
                total = F(0)
                for power in range(index + 1):
                    source = [i, j, k]
                    source[axis] = power
                    total += data[source[0]][source[1]][source[2]] * F(comb(index, power), comb(degree, power))
                out[i][j][k] = total
    return out


def main():
    started = time.perf_counter()
    beta, rows, groups = symbolic_types()
    delta, v, zeta = sp.symbols("delta v zeta")
    s = 1 - delta
    u = 1 - v

    rational_kernel = sp.Integer(0)
    for (a, b), (weight, _) in groups.items():
        q = 1 - a*s + b*s*s
        acceleration = (a - s*b) * (a - 6*s*b)
        denominator = 1 + u*(q - 1)
        rational_kernel += weight * acceleration / denominator

    numerator, denominator = sp.fraction(sp.cancel(sp.together(rational_kernel)))
    polynomial = sp.Poly(sp.expand(numerator), beta, delta, v, domain=sp.QQ)
    degrees = tuple(polynomial.degree(variable) for variable in (beta, delta, v))
    monomial_count = len(polynomial.terms())
    assert degrees == (18, 24, 11), degrees
    assert monomial_count == 1932, monomial_count
    print(json.dumps({"stage": "power_numerator", "degrees": degrees,
                      "monomials": monomial_count,
                      "elapsed_seconds": time.perf_counter() - started}), flush=True)

    affine = sp.Poly(sp.expand(polynomial.as_expr().subs(v, (1 + 15*zeta) / 16)),
                     beta, delta, zeta, domain=sp.QQ)
    common_denominator, integer_poly = affine.clear_denoms(convert=True)
    dense = [[[F(0) for _ in range(degrees[2] + 1)]
              for __ in range(degrees[1] + 1)] for ___ in range(degrees[0] + 1)]
    for exponents, coefficient in integer_poly.terms():
        dense[exponents[0]][exponents[1]][exponents[2]] = F(int(coefficient))

    for axis in range(3):
        dense = transform_axis(dense, degrees, axis)
        print(json.dumps({"stage": f"bernstein_axis_{axis}",
                          "elapsed_seconds": time.perf_counter() - started}), flush=True)

    coefficients = [dense[i][j][k] for i in range(degrees[0] + 1)
                    for j in range(degrees[1] + 1) for k in range(degrees[2] + 1)]
    assert len(coefficients) == 5700
    assert all(value >= 0 for value in coefficients)
    minimum = min(coefficients)
    denominators = [value.denominator for value in coefficients]
    bernstein_scale = reduce(lcm, denominators, 1)
    scaled = [value * bernstein_scale for value in coefficients]
    assert all(value.denominator == 1 for value in scaled)
    scaled_minimum = min(int(value) for value in scaled)

    # Report both normalizations.  The publication uses the integer
    # normalization obtained after clearing affine and Bernstein denominators.
    assert scaled_minimum == EXPECTED_MIN, (scaled_minimum, EXPECTED_MIN)
    result = {
        "status": "PASS",
        "head": "3f276c09fe4da3aded2ab6cf457adb7fdc4254d8",
        "generic_denominator_types": len(groups),
        "power_multidegree": list(degrees),
        "power_monomials": monomial_count,
        "tensor_bernstein_coefficients": len(coefficients),
        "all_nonnegative": True,
        "strict_minimum_integer_normalization": str(scaled_minimum),
        "reported_minimum_matches": True,
        "affine_power_denominator": str(common_denominator),
        "bernstein_denominator_scale": str(bernstein_scale),
        "elapsed_seconds": time.perf_counter() - started,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
