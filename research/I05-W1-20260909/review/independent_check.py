#!/usr/bin/env python3
"""Independent cross-check for I05-W1-20260909.

This checker deliberately does not import the submitted verifier.  It constructs
exact-event probabilities by Möbius inversion of the defining inclusion
probabilities det(K_T), rather than by the event-determinant formula used in the
submission.  Symbolic identities use SymPy rationals; entropy values are only a
secondary 100-digit numerical cross-check of signs already proved analytically.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path
import json
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[1] / "result"
INPUTS = json.loads((ROOT / "inputs" / "exact_inputs.json").read_text(encoding="utf-8"))

t = sp.symbols("t", real=True)


def subsets(n: int):
    for r in range(n + 1):
        yield from combinations(range(n), r)


def key(S, n: int) -> str:
    S = set(S)
    return "".join("1" if i in S else "0" for i in range(n))


def principal_det(K: sp.Matrix, S: tuple[int, ...]) -> sp.Expr:
    return sp.Integer(1) if not S else sp.factor(K.extract(S, S).det())


def exact_probabilities_by_mobius(K: sp.Matrix) -> dict[str, sp.Expr]:
    """Use p(S)=sum_{T superset S} (-1)^(|T|-|S|) det K_T."""
    n = K.rows
    all_sets = list(subsets(n))
    dets = {S: principal_det(K, S) for S in all_sets}
    out: dict[str, sp.Expr] = {}
    for S in all_sets:
        sset = set(S)
        val = sp.Integer(0)
        for T in all_sets:
            if sset.issubset(T):
                val += (-1) ** (len(T) - len(S)) * dets[T]
        out[key(S, n)] = sp.factor(val)
    assert sp.simplify(sum(out.values()) - 1) == 0
    return dict(sorted(out.items()))


def rat(x: str) -> sp.Expr:
    return sp.sympify(x, locals={"I": sp.I})


def matrix(rows) -> sp.Matrix:
    return sp.Matrix([[rat(x) for x in row] for row in rows])


def vector(xs) -> sp.Matrix:
    return sp.Matrix([rat(x) for x in xs])


def entropy_at(p: dict[str, sp.Expr], at: sp.Expr) -> mp.mpf:
    mp.mp.dps = 100
    total = mp.mpf("0")
    for expr in p.values():
        q = sp.factor(expr.subs(t, at))
        assert q.is_Rational and q > 0
        qmp = mp.mpf(int(q.p)) / mp.mpf(int(q.q))
        total -= qmp * mp.log(qmp)
    return total


def hessian_at(p: dict[str, sp.Expr], at: sp.Expr) -> mp.mpf:
    mp.mp.dps = 100
    total = mp.mpf("0")
    for expr in p.values():
        q = sp.factor(expr.subs(t, at))
        q1 = sp.factor(sp.diff(expr, t).subs(t, at))
        q2 = sp.factor(sp.diff(expr, t, 2).subs(t, at))
        assert q.is_Rational and q > 0 and q1.is_Rational and q2.is_Rational
        qm = mp.mpf(int(q.p)) / int(q.q)
        q1m = mp.mpf(int(q1.p)) / int(q1.q)
        q2m = mp.mpf(int(q2.p)) / int(q2.q)
        total -= q1m * q1m / qm + q2m * mp.log(qm)
    return total


def assert_pd_by_leading_minors(M: sp.Matrix) -> None:
    for j in range(1, M.rows + 1):
        assert sp.factor(M[:j, :j].det()) > 0


def block_marginal(p: dict[str, sp.Expr], left_bits: int, which: str) -> dict[str, sp.Expr]:
    result: dict[str, sp.Expr] = {}
    if which == "left":
        labels = sorted({bits[:left_bits] for bits in p})
        for label in labels:
            result[label] = sp.factor(sum(v for bits, v in p.items() if bits[:left_bits] == label))
    else:
        labels = sorted({bits[left_bits:] for bits in p})
        for label in labels:
            result[label] = sp.factor(sum(v for bits, v in p.items() if bits[left_bits:] == label))
    return result


def main() -> None:
    lines: list[str] = []
    add = lines.append
    add("Independent Möbius-inversion verification: I05-W1-20260909")
    add(f"SymPy {sp.__version__}; mpmath {mp.__version__}; entropy cross-check precision=100 dps")

    # Main real four-point witness.
    obj = INPUTS["real_rank_one_crossblock_4point"]
    A, C = matrix(obj["A"]), matrix(obj["C"])
    u, v = vector(obj["u"]), vector(obj["v"])
    B = u * v.T
    K4 = A.row_join(t * B).col_join((t * B.T).row_join(C))
    p4 = exact_probabilities_by_mobius(K4)
    pA = exact_probabilities_by_mobius(A)
    pC = exact_probabilities_by_mobius(C)
    z = sp.symbols("z", real=True)
    pAz = exact_probabilities_by_mobius(A + z * u * u.T)
    pCz = exact_probabilities_by_mobius(C + z * v * v.T)
    alpha = {k: sp.diff(q, z).subs(z, 0) for k, q in pAz.items()}
    gamma = {k: sp.diff(q, z).subs(z, 0) for k, q in pCz.items()}
    for bits, q in p4.items():
        l, r = bits[:2], bits[2:]
        assert sp.simplify(q - (pA[l] * pC[r] - t**2 * alpha[l] * gamma[r])) == 0
    assert block_marginal(p4, 2, "left") == pA
    assert block_marginal(p4, 2, "right") == pC
    D4 = sp.diff(K4, t)
    assert D4.rank() == 2
    assert K4.subs(t, 0) * D4 - D4 * K4.subs(t, 0) != sp.zeros(4)
    eta = sp.factor((u.T * A.inv() * u)[0] * (v.T * C.inv() * v)[0])
    zeta = sp.factor((u.T * (sp.eye(2) - A).inv() * u)[0] * (v.T * (sp.eye(2) - C).inv() * v)[0])
    tau2 = sp.factor(min(1 / eta, 1 / zeta))
    assert tau2 == sp.Rational(2599, 864)
    H4pp = hessian_at(p4, sp.Rational(1, 4))
    chord4 = (entropy_at(p4, sp.Rational(1, 8)) + entropy_at(p4, sp.Rational(3, 8))) / 2 - entropy_at(p4, sp.Rational(1, 4))
    assert H4pp < 0 and chord4 < 0
    add("4-point rank-one crossblock identity: PASS (16 events, both marginals, rank/noncommutation)")
    add(f"4-point exact tau^2={tau2}; H''(1/4)={mp.nstr(H4pp, 30)}")
    add(f"4-point chord(center=1/4, step=1/8)={mp.nstr(chord4, 30)}")

    # Verify the entropy identity H(P_s)=H(P_0)-D(P_s||P_0) numerically at a nonzero s,
    # using the independently constructed probabilities.
    mp.mp.dps = 100
    at = sp.Rational(1, 4)
    lhs = entropy_at(p4, at)
    H0 = entropy_at(p4, 0)
    kl = mp.mpf("0")
    for bits, expr in p4.items():
        q = sp.factor(expr.subs(t, at)); q0 = sp.factor(expr.subs(t, 0))
        qm = mp.mpf(int(q.p)) / int(q.q); q0m = mp.mpf(int(q0.p)) / int(q0.q)
        kl += qm * mp.log(qm / q0m)
    assert abs(lhs - (H0 - kl)) < mp.mpf("1e-90")
    add("fixed-marginal entropy/KL identity at t=1/4: PASS")

    # Three-point conditional obstruction, using Möbius inversion directly.
    obj = INPUTS["conditional_3point"]
    K3, D3 = matrix(obj["K"]), matrix(obj["D"])
    p3 = exact_probabilities_by_mobius(K3 + t * D3)
    expected = {
        "000": (27 - 200*t**2)/1000,
        "001": (213 - 200*t - 800*t**2)/1000,
        "010": (213 + 200*t - 800*t**2)/1000,
        "011": (47 + 1800*t**2)/1000,
        "100": (63 + 200*t**2)/1000,
        "101": (197 + 200*t + 800*t**2)/1000,
        "110": (197 - 200*t + 800*t**2)/1000,
        "111": (43 - 1800*t**2)/1000,
    }
    for k, q in expected.items():
        assert sp.simplify(p3[k] - q) == 0
    for at in (sp.Rational(-1, 100), sp.Rational(1, 100)):
        assert_pd_by_leading_minors(K3 + at * D3)
        assert_pd_by_leading_minors(sp.eye(3) - K3 - at * D3)
    H3pp = hessian_at(p3, 0)
    assert H3pp < 0
    # Exact positivity of the submitted conditional acceleration certificate.
    assert 27**6 * 43**86 * 213**88 > 197**72 * 47**94 * 63**14
    acc = (mp.mpf(1)/25) * mp.log(
        mp.mpf(27)**6 * mp.mpf(43)**86 * mp.mpf(213)**88 /
        (mp.mpf(197)**72 * mp.mpf(47)**94 * mp.mpf(63)**14)
    )
    assert acc > 0
    add(f"3-point probabilities/validity: PASS; conditional acceleration={mp.nstr(acc, 30)}")
    add(f"3-point complete H''(0)={mp.nstr(H3pp, 30)}")

    # Quantum-measurement bridge obstruction.
    obj = INPUTS["quantum_mixture_2point"]
    K2, D2 = matrix(obj["K"]), matrix(obj["D"])
    p2 = exact_probabilities_by_mobius(K2 + t * D2)
    h = sp.Rational(1, 20)
    center = {k: sp.factor(q.subs(t, 0)) for k, q in p2.items()}
    minus = {k: sp.factor(q.subs(t, -h)) for k, q in p2.items()}
    plus = {k: sp.factor(q.subs(t, h)) for k, q in p2.items()}
    mix = {k: sp.factor((minus[k] + plus[k]) / 2) for k in p2}
    assert [center[k] for k in sorted(center)] == [sp.Rational(9,100), sp.Rational(41,100), sp.Rational(41,100), sp.Rational(9,100)]
    assert [mix[k] for k in sorted(mix)] == [sp.Rational(37,400), sp.Rational(163,400), sp.Rational(163,400), sp.Rational(37,400)]
    def ent_of_rational_dict(d):
        mp.mp.dps = 100
        ans = mp.mpf("0")
        for q in d.values():
            qm = mp.mpf(int(q.p)) / int(q.q)
            ans -= qm * mp.log(qm)
        return ans
    mix_defect = ent_of_rational_dict(mix) - ent_of_rational_dict(center)
    true_chord = (ent_of_rational_dict(minus) + ent_of_rational_dict(plus)) / 2 - ent_of_rational_dict(center)
    assert mix_defect > 0 and true_chord < 0
    add(f"measurement-mixture defect={mp.nstr(mix_defect, 30)}; actual chord={mp.nstr(true_chord, 30)}")

    # Rank-two obstruction.
    obj = INPUTS["rank_two_crossblock_obstruction"]
    A2, C2, B2 = matrix(obj["A"]), matrix(obj["C"]), matrix(obj["B"])
    Kr2 = A2.row_join(t * B2).col_join((t * B2.T).row_join(C2))
    full = sp.expand(Kr2.det())
    assert full == sp.Rational(1,16) - t**2/sp.Integer(200) + t**4/sp.Integer(10000)
    s = sp.symbols("s", real=True)
    full_s = sp.expand(full.subs(t**2, s))
    assert sp.Poly(full_s, s).degree() == 2
    add(f"rank-two full-occupancy polynomial={full}; degree in s is 2")

    # Independent symbolic differentiation of the rank-two entropy formula.
    P0, R, Q = sp.symbols("P0 R Q", positive=True)
    # Treat P(s)=P0+sR+s^2Q for one summand; normalization removes +1 terms in the sum.
    P = P0 + s*R + s**2*Q
    per_event = -P * sp.log(P)
    d2dt = sp.simplify(2*sp.diff(per_event, s) + 4*s*sp.diff(per_event, s, 2))
    target = sp.simplify(-(2*R + 12*s*Q)*sp.log(P) - 4*s*(R + 2*s*Q)**2/P)
    # Difference is the normalization term -(2R+12sQ), which vanishes after summing events.
    assert sp.simplify(d2dt - target + (2*R + 12*s*Q)) == 0
    add("rank-two curvature coefficient 12sQ (hence -10s<Q,L> after J extraction): PASS")

    add("INDEPENDENT CHECKS PASSED")
    out = "\n".join(lines) + "\n"
    print(out, end="")
    (Path(__file__).resolve().parent / "independent_check_output.txt").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
