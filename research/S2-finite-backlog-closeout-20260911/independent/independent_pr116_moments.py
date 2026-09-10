#!/usr/bin/env python3
"""Independent symbolic audit of PR116 moments and boundary coefficients."""

import json
import time
import sympy as sp

from independent_pr116_light import symbolic_types


def main():
    started = time.perf_counter()
    alpha = sp.symbols("alpha", positive=True)
    beta, rows, groups = symbolic_types(alpha)
    print(json.dumps({"stage": "general_64_events", "types": len(groups),
                      "elapsed_seconds": time.perf_counter() - started}), flush=True)

    D = (3*alpha*beta - 2*alpha - beta) * (3*alpha*beta - alpha - 2*beta)
    Na = (5*alpha**2*beta**2 - 5*alpha**2*beta + alpha**2
          - 2*alpha*beta**3 - 2*alpha*beta**2 + 2*alpha*beta + beta**3)
    Nab = 2*alpha*beta**2*(alpha - 1)*(alpha - beta)**2*(beta - 1)**2
    Nb = (7*alpha**2*beta**2 - 7*alpha**2*beta + 2*alpha**2
          - 4*alpha*beta**3 - alpha*beta**2 + alpha*beta + 2*beta**3)
    Ma = sp.cancel(sum(mu*a*a for mu, a, _ in rows))
    Mab = sp.cancel(sum(mu*a*b for mu, a, b in rows))
    Mb = sp.cancel(sum(mu*b*b for mu, _, b in rows))
    assert sp.cancel(Ma - 6*Na**2/D**2) == 0
    assert sp.cancel(Mab - Nab/D**2) == 0
    assert sp.cancel(Mb - Nb**2/D**2) == 0

    X = 2*alpha + beta - 3*alpha*beta
    Y = alpha + 2*beta - 3*alpha*beta
    Dpositive = sp.expand(X*Y)
    mb_factor = 2*beta*(1-beta)*((1-alpha)*(alpha+beta) + alpha*(1-beta))
    assert sp.factor(Dpositive - Nb - mb_factor) == 0

    denominator_special = (7*beta + 2)**2 * (17*beta + 1)**2
    expected_special = (
        6*(80*beta**3 - 15*beta**2 + 15*beta + 1)**2/denominator_special,
        -18*beta**2*(1-beta)**2*(10*beta-1)**2/denominator_special,
        (5*beta+1)**2*(32*beta**2 - 7*beta + 2)**2/denominator_special,
    )
    for actual, expected in zip((Ma, Mab, Mb), expected_special):
        assert sp.cancel(actual.subs(alpha, sp.Rational(1, 10)) - expected) == 0
    print(json.dumps({"stage": "global_moments", "elapsed_seconds": time.perf_counter() - started}), flush=True)

    epsilon, s = sp.symbols("epsilon s", positive=True)
    point_R = sp.Integer(0)
    point_F = sp.Integer(0)
    for (a, b), (weight, _) in groups.items():
        q = 1 - a*s + b*s*s
        z = (a - s*b)*(a - 6*s*b)
        velocity = a - 2*s*b
        point_R += weight*z/q
        point_F += 4*weight*velocity**2/q
    substitutions = {beta: 1-epsilon, s: 1-epsilon}
    ray_R = sp.factor(sp.limit(epsilon**2 * point_R.subs(substitutions), epsilon, 0, dir="+"))
    ray_F = sp.factor(sp.limit(epsilon * point_F.subs(substitutions), epsilon, 0, dir="+"))
    expected_R = -8*alpha**2*(alpha-1)**3/(alpha-3)
    expected_F = -16*alpha*(alpha-1)**2*(2*alpha-9)/((2*alpha-5)*(2*alpha-3))
    assert sp.cancel(ray_R - expected_R) == 0
    assert sp.cancel(ray_F - expected_F) == 0

    # Obtain the logarithmic coefficient directly from the 13 rebuilt types.
    # If q(epsilon) ~ c*epsilon^k, then lambda(q) contributes
    # k*log(1/epsilon); types with nonzero endpoint q contribute no log.
    ray_A = sp.Integer(0)
    for (a, b), (weight, _) in groups.items():
        q = 1 - a*s + b*s*s
        signed = (a - s*b)*(a - 6*s*b)
        qray = sp.cancel(q.subs(substitutions))
        if sp.limit(qray, epsilon, 0, dir="+") == 0:
            order = sp.limit(epsilon * sp.diff(qray, epsilon) / qray, epsilon, 0, dir="+")
            signed_limit = sp.limit((weight*signed).subs(substitutions), epsilon, 0, dir="+")
            ray_A += 2 * order * signed_limit
    ray_A = sp.factor(ray_A)
    expected_A = 8*alpha*(alpha-1)*(4*alpha**2-4*alpha-1)
    assert sp.factor(ray_A - expected_A) == 0
    assert expected_R.subs(alpha, sp.Rational(1, 10)) == -sp.Rational(729, 36250)
    assert expected_A.subs(alpha, sp.Rational(1, 10)) == sp.Rational(612, 625)
    print(json.dumps({"stage": "boundary_ray", "elapsed_seconds": time.perf_counter() - started}), flush=True)

    # Two-scale corner arithmetic, using the displayed endpoint groups and
    # rational crossover functions only.
    corner_A = (2*sp.Rational(729, 2500)*sp.Rational(14, 9)
                + 2*sp.Rational(9, 2500)*46
                + 4*sp.Rational(81, 5000)*(-4))
    assert corner_A == sp.Rational(612, 625)
    z = sp.symbols("z", nonnegative=True)
    f0 = sp.Rational(162, 125)/(1+5*z) + sp.Rational(12, 125)/(1+15*z) + sp.Rational(6, 125)
    f1 = sp.Rational(324, 125)/(3+5*z) + sp.Rational(162, 125)/(9+5*z) + sp.Rational(54, 125)
    assert f0.subs(z, 0) == f1.subs(z, 0) == sp.Rational(36, 25)
    assert sp.factor(f0 - sp.Rational(6, 125)).is_positive
    assert sp.factor(f1 - sp.Rational(54, 125)).is_positive

    result = {
        "status": "PASS",
        "head": "3f276c09fe4da3aded2ab6cf457adb7fdc4254d8",
        "general_complete_events": len(rows),
        "general_types": len(groups),
        "M_a_M_ab_M_b_closed_forms": True,
        "alpha_1_over_10_specializations": True,
        "M_b_le_1_factor_identity": True,
        "boundary_ray_leading_coefficients": {"R": True, "A_norm": True, "F_norm": True},
        "two_scale_corner_A_coefficient": "612/625",
        "f0_f1_forms_and_endpoints": True,
        "elapsed_seconds": time.perf_counter() - started,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
