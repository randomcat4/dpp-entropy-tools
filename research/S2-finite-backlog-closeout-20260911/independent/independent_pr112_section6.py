#!/usr/bin/env python3
"""Independent Fraction reconstruction of both Section 6 lift witnesses."""

from fractions import Fraction as Q
import json


class Jet:
    """Value, first derivative, and actual second derivative."""

    __slots__ = ("v", "d", "dd")

    def __init__(self, value, derivative=0, second=0):
        self.v, self.d, self.dd = Q(value), Q(derivative), Q(second)

    @staticmethod
    def lift(value):
        return value if isinstance(value, Jet) else Jet(value)

    def __add__(self, other):
        other = Jet.lift(other)
        return Jet(self.v + other.v, self.d + other.d, self.dd + other.dd)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.d, -self.dd)

    def __sub__(self, other):
        return self + (-Jet.lift(other))

    def __rsub__(self, other):
        return Jet.lift(other) - self

    def __mul__(self, other):
        other = Jet.lift(other)
        return Jet(self.v * other.v,
                   self.d * other.v + self.v * other.d,
                   self.dd * other.v + 2 * self.d * other.d + self.v * other.dd)

    __rmul__ = __mul__

    def inverse(self):
        return Jet(1 / self.v,
                   -self.d / self.v**2,
                   2 * self.d**2 / self.v**3 - self.dd / self.v**2)

    def __truediv__(self, other):
        return self * Jet.lift(other).inverse()


B = Q(1, 8)
SIGNS = ((-1, -1), (-1, 1), (1, -1), (1, 1))


def branch(s, x, y, r, d, a, c):
    """Return g and the four homogeneous numerators from formulas (1)-(2)."""
    g = Q(1, 4) - a * x / 2 - c * y / 2 + a * c * (d + 2 * r - s)
    nx = a * c * B**2 * (Q(c, 2) - y)
    ny = a * c * (B**2 * (Q(a, 2) - x) + s * (Q(c, 2) - y) - 2 * B * (s - r))
    nr = a * c * (B * s * (Q(c, 2) - y) - B**2 * (s - r))
    nd = a * c * B**4
    return g, nx, ny, nr, nd


def operator_negative_square(s, x, y, r, d, coefficients):
    total = Jet(0)
    for a, c in SIGNS:
        g, nx, ny, nr, nd = branch(s, x, y, r, d, a, c)
        numerator = coefficients[0] * nx + coefficients[1] * ny + coefficients[2] * nr + coefficients[3] * nd
        total -= numerator * numerator / g
    return total


def cone_interior(s, x, y, r, d):
    U, V, D = 4 * (x + y), 4 * (x - y), 64 * d
    w_squared = 64 * r * r / s
    scalars = [1 + D + 2 * U, 1 + D - 2 * U]
    block_diagonal = [1 - D + 2 * V, 1 - D - 2 * V]
    block_det = (1 - D)**2 - 4 * V**2 - 4 * w_squared
    return all(value > 0 for value in scalars + block_diagonal + [block_det]), scalars, block_diagonal, block_det


def plain_value(jet):
    return jet.v if isinstance(jet, Jet) else Q(jet)


def second_witness_value(s, x, y, r, d):
    return operator_negative_square(s, x, y, r, d, (0, 1, 0, 0)).v


def main():
    # First witness: differentiate the operator directly, without using the
    # displayed closed form as an implementation.
    s0 = Q(1, 128)
    probe = Q(1, 256)
    first = operator_negative_square(Jet(probe, 1), Jet(0), Jet(0), Jet(0), Jet(0),
                                     (-s0 / B, 0, 1, s0 / B**2))
    displayed_derivative = -Q(17, 128) * (probe - s0) * (1 - 16 * probe * s0) / (1 - 16 * probe**2)**2
    assert first.d == displayed_derivative > 0

    # Second witness: exact path derivative at the displayed rational point.
    star = (Q(1, 160), Q(0), -Q(1, 12), Q(0), Q(0))
    direction = (Q(1), Q(15), -Q(20), Q(1, 2), Q(14))
    s, x, y, r, d = [Jet(value, velocity) for value, velocity in zip(star, direction)]
    curved = operator_negative_square(s, x, y, r, d, (0, 1, 0, 0))
    expected_second = Q(62133760927002633199475, 123948511626037169227442)
    assert curved.dd == expected_second > 0

    epsilon = Q(1, 65536)
    plus = [value + epsilon * velocity for value, velocity in zip(star, direction)]
    minus = [value - epsilon * velocity for value, velocity in zip(star, direction)]
    center_value = second_witness_value(*star)
    finite_gap = (second_witness_value(*plus) + second_witness_value(*minus)) / 2 - center_value
    expected_gap = Q(83227040581365279974557560989255720223314146025,
                     1426167397794154630144461142089621826100832351402858643456)
    assert finite_gap == expected_gap > 0

    endpoint_checks = []
    for label, point in (("minus", minus), ("plus", plus)):
        interior, scalar_blocks, diagonal, determinant = cone_interior(*point)
        weights = [plain_value(branch(*point, a, c)[0]) for a, c in SIGNS]
        assert interior and all(weight > 0 for weight in weights) and sum(weights, Q(0)) == 1
        endpoint_checks.append({
            "endpoint": label,
            "cone_interior": True,
            "minimum_branch_weight": str(min(weights)),
            "minimum_scalar_block": str(min(scalar_blocks)),
            "minimum_2x2_diagonal": str(min(diagonal)),
            "2x2_block_determinant": str(determinant),
        })

    result = {
        "status": "PASS_NEW_RECONSTRUCTION_HISTORICAL_CHECKER_ABSENT",
        "head": "2ea07741114aa7cd20210dfc84becda378381e7b",
        "first_shortcut_derivative_at_s_1_over_256": str(first.d),
        "first_shortcut_exact_positive": True,
        "joint_second_derivative": str(curved.dd),
        "joint_second_derivative_matches_display_19": True,
        "finite_epsilon_gap": str(finite_gap),
        "finite_epsilon_gap_matches_display_20": True,
        "endpoint_checks": endpoint_checks,
        "historical_exact_lift_check_present_at_head": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
