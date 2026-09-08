#!/usr/bin/env python3
"""Symbolic S3 identities for the n=3 equicorrelation Hessian audit.

The output is a compact JSON certificate of algebraic setup:

* exact event probabilities by event size after Boolean Mobius inversion;
* first and second line derivatives for the four S3 block basis directions;
* exact vanishing of cross terms between trivial and standard isotypic parts;
* a recipe for reconstructing the two 2x2 Hessian blocks.

It intentionally avoids printing the fully expanded block entries, which are
large and less reviewable than the derivative table.
"""

from __future__ import annotations

import json
import sympy as sp


x, y, t = sp.symbols("x y t")
L0, L1, L2, L3 = sp.symbols("L0 L1 L2 L3")
a = (x + 2 * y) / 3
c = (x - y) / 3
K = sp.simplify((a - c) * sp.eye(3) + c * sp.ones(3))


def bits(mask: int) -> list[int]:
    return [i for i in range(3) if (mask >> i) & 1]


def det_sub(M: sp.Matrix, mask: int) -> sp.Expr:
    idx = bits(mask)
    if not idx:
        return sp.Integer(1)
    return sp.factor(M.extract(idx, idx).det())


def event_poly(V: sp.Matrix, mask: int) -> sp.Expr:
    M = K + t * V
    total = 0
    for sup in range(8):
        if (sup & mask) == mask:
            sign = -1 if ((sup.bit_count() - mask.bit_count()) & 1) else 1
            total += sign * det_sub(M, sup)
    return sp.factor(sp.expand(total))


def event_derivatives(V: sp.Matrix) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for mask in range(8):
        p = event_poly(V, mask)
        out[f"{mask:03b}"] = {
            "size": str(mask.bit_count()),
            "p_prime": str(sp.factor(sp.diff(p, t).subs(t, 0))),
            "p_double_prime": str(sp.factor(sp.diff(p, t, 2).subs(t, 0))),
        }
    return out


def h2_expr(V: sp.Matrix) -> sp.Expr:
    total = 0
    logs = [L0, L1, L2, L3]
    for mask in range(8):
        p = event_poly(V, mask)
        p0 = sp.factor(p.subs(t, 0))
        dp = sp.factor(sp.diff(p, t).subs(t, 0))
        dd = sp.factor(sp.diff(p, t, 2).subs(t, 0))
        total += -dp**2 / p0 - logs[mask.bit_count()] * dd
    return sp.factor(sp.cancel(total))


def cross_expr(V: sp.Matrix, W: sp.Matrix) -> sp.Expr:
    return sp.factor(sp.cancel((h2_expr(V + W) - h2_expr(V) - h2_expr(W)) / 2))


def second_cross(V: sp.Matrix, W: sp.Matrix) -> dict[str, str]:
    out: dict[str, str] = {}
    for mask in range(8):
        p_v = event_poly(V, mask)
        p_w = event_poly(W, mask)
        p_sum = event_poly(V + W, mask)
        dd = (
            sp.diff(p_sum, t, 2).subs(t, 0)
            - sp.diff(p_v, t, 2).subs(t, 0)
            - sp.diff(p_w, t, 2).subs(t, 0)
        ) / 2
        out[f"{mask:03b}"] = str(sp.factor(dd))
    return out


def main() -> int:
    Td = sp.eye(3)
    To = sp.ones(3) - sp.eye(3)
    vec = [1, -1, 0]
    Sd = sp.diag(*vec)
    So = sp.zeros(3)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        So[i, j] = So[j, i] = vec[i] + vec[j]

    bases = {"Td": Td, "To": To, "Sd": Sd, "So": So}
    zero_crosses = {
        "Td_Sd": str(cross_expr(Td, Sd)),
        "Td_So": str(cross_expr(Td, So)),
        "To_Sd": str(cross_expr(To, Sd)),
        "To_So": str(cross_expr(To, So)),
    }
    payload = {
        "status": "SYMBOLIC_IDENTITIES",
        "variables": {
            "lambda1": "x=a+2c",
            "lambda2": "y=a-c",
            "domain": "0<x<1 and 0<y<1",
            "a": "(x+2*y)/3",
            "c": "(x-y)/3",
        },
        "event_probabilities_by_size": {
            "p0_empty": str(sp.factor(event_poly(sp.zeros(3), 0).subs(t, 0))),
            "p1_each_singleton": str(sp.factor(event_poly(sp.zeros(3), 1).subs(t, 0))),
            "p2_each_pair": str(sp.factor(event_poly(sp.zeros(3), 3).subs(t, 0))),
            "p3_triple": str(sp.factor(event_poly(sp.zeros(3), 7).subs(t, 0))),
        },
        "basis": {
            "Td": "I3",
            "To": "J3-I3",
            "Sd": "diag(1,-1,0)",
            "So": "offdiag entries O_ij=x_i+x_j for x=(1,-1,0), i.e. e13=1,e23=-1,e12=0",
        },
        "derivatives": {name: event_derivatives(V) for name, V in bases.items()},
        "second_derivative_cross_for_intra_blocks": {
            "Td_To": second_cross(Td, To),
            "Sd_So": second_cross(Sd, So),
        },
        "trivial_standard_hessian_cross_terms": zero_crosses,
        "block_entry_recipe": (
            "For basis vectors Bi,Bj in {Td,To} or {Sd,So}, "
            "B_ij = -sum_S p'_S(Bi)p'_S(Bj)/p_S - sum_S log(p_S) p''_S(Bi,Bj), "
            "where p_S is chosen by |S| from p0,p1,p2,p3 and "
            "p''_S(Bi,Bj) is the polarized second derivative. "
            "The two resulting 2x2 blocks give H'' on the trivial and standard isotypic components."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
