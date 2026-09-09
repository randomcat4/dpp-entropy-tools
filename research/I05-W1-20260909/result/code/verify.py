#!/usr/bin/env python3
"""Exact algebra and rational logarithm enclosures for I05-W1-20260909.

Run from any working directory: python code/verify.py
The output directory is resolved relative to this script, not to a private path.
No network, random sampling, numerical eigensolver, or floating-point certificate.
"""
from __future__ import annotations

import json
import platform
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import Iterable

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
N_TERMS = 48
R = sp.Rational
t, z = sp.symbols("t z", real=True)
logs_cache: dict[F, tuple[F, F]] = {}
certificates: dict[str, dict[str, str]] = {}
report: list[str] = []


def emit(text: str = "") -> None:
    report.append(text)
    print(text)


def frac(x) -> F:
    x = sp.cancel(x)
    if not x.is_Rational:
        raise ValueError(f"Expected rational value, got {x}")
    return F(int(x.p), int(x.q))


def mul_interval(a: F, interval: tuple[F, F]) -> tuple[F, F]:
    lo, hi = interval
    return (a * lo, a * hi) if a >= 0 else (a * hi, a * lo)


def log_unit(y: F) -> tuple[F, F]:
    """For 1<=y<=2, log(y)=2 sum w^(2j+1)/(2j+1), w=(y-1)/(y+1)."""
    assert F(1) <= y <= F(2)
    w = (y - 1) / (y + 1)
    partial = sum((2 * w ** (2 * j + 1) / (2 * j + 1)
                   for j in range(N_TERMS)), F(0))
    tail = 2 * w ** (2 * N_TERMS + 1) / ((2 * N_TERMS + 1) * (1 - w * w))
    return partial, partial + tail


def log_interval(x: F) -> tuple[F, F]:
    if x <= 0:
        raise ValueError("Log argument must be positive")
    if x in logs_cache:
        return logs_cache[x]
    y, k = x, 0
    while y < 1:
        y *= 2
        k -= 1
    while y >= 2:
        y /= 2
        k += 1
    a, b = log_unit(y)
    c, d = mul_interval(F(k), log_unit(F(2)))
    result = a + c, b + d
    logs_cache[x] = result
    return result


def linear_logs(terms: Iterable[tuple[F, F]], const: F = F(0)) -> tuple[F, F]:
    lo = hi = const
    for coef, arg in terms:
        a, b = mul_interval(coef, log_interval(arg))
        lo += a
        hi += b
        # Outward enclosure on a rational 10^-44 grid keeps certificates compact.
        # These are exact integer floor/ceiling operations, not floating rounding.
        grid = 10**44
        lo = F((lo.numerator * grid) // lo.denominator, grid)
        hi = F(-((-hi.numerator * grid) // hi.denominator), grid)
    return lo, hi


def outward_decimal(x: F, places: int, upper: bool) -> str:
    scale = 10 ** places
    a = x.numerator * scale
    q = -((-a) // x.denominator) if upper else a // x.denominator
    sign = "-" if q < 0 else ""
    q = abs(q)
    return f"{sign}{q // scale}.{q % scale:0{places}d}"


def record(name: str, interval: tuple[F, F], sign: str | None = None) -> None:
    lo, hi = interval
    assert lo <= hi
    if sign == "+":
        assert lo > 0, (name, "failed positive certificate")
    if sign == "-":
        assert hi < 0, (name, "failed negative certificate")
    width = hi - lo
    assert width < F(1, 10**38), (name, "insufficient log precision")
    a = outward_decimal(lo, 15, False)
    b = outward_decimal(hi, 15, True)
    emit(f"{name}: [{a}, {b}], exact rational width < 1e-38; sign={sign or 'not requested'}")
    certificates[name] = {
        "lower_exact": str(lo), "upper_exact": str(hi),
        "lower_decimal_outward": a, "upper_decimal_outward": b,
        "width_exact": str(width), "certified_sign": sign or "",
    }


def probabilities(K: sp.Matrix) -> dict[str, sp.Expr]:
    n = K.rows
    out = {}
    for bits in product((0, 1), repeat=n):
        M = K - sp.diag(*[1 - b for b in bits])
        out[''.join(map(str, bits))] = sp.factor((-1)**(n-sum(bits))*M.det())
    assert sp.simplify(sum(out.values()) - 1) == 0
    return out


def check_inclusion_exclusion(K: sp.Matrix, p: dict[str, sp.Expr]) -> None:
    n = K.rows
    for bits in product((0, 1), repeat=n):
        T = [i for i, b in enumerate(bits) if b]
        moment = K.extract(T, T).det() if T else sp.Integer(1)
        total = sum(v for key, v in p.items() if all(key[i] == '1' for i in T))
        assert sp.simplify(total - moment) == 0


def eval_prob(p: dict[str, sp.Expr], at: sp.Rational) -> dict[str, F]:
    result = {key: frac(value.subs(t, at)) for key, value in p.items()}
    assert all(value > 0 for value in result.values())
    assert sum(result.values(), F(0)) == 1
    return result


def entropy(prob: dict[str, F]) -> tuple[F, F]:
    return linear_logs([(-value, value) for value in prob.values() if value])


def gradient_terms(K: sp.Matrix, V: sp.Matrix) -> list[tuple[F, F]]:
    p = probabilities(K + t*V)
    return [(-frac(sp.diff(value, t).subs(t, 0)), frac(value.subs(t, 0)))
            for value in p.values()]


def curvature(p: dict[str, sp.Expr], at: sp.Rational):
    fisher = F(0)
    terms = []
    for value in p.values():
        a = frac(value.subs(t, at))
        b = frac(sp.diff(value, t).subs(t, at))
        c = frac(sp.diff(value, t, 2).subs(t, at))
        assert a > 0
        fisher += b*b/a
        terms.append((-c, a))
    geometric = linear_logs(terms)
    return fisher, geometric, (geometric[0]-fisher, geometric[1]-fisher)


def prime_log_coefficients(terms: Iterable[tuple[F, F]]) -> dict[int, F]:
    """Canonical prime-log coefficients, using exact integer factorization only."""
    result: dict[int, F] = {}
    for coefficient, argument in terms:
        if argument <= 0:
            raise ValueError("Log argument must be positive")
        for integer, sign in ((argument.numerator, 1), (argument.denominator, -1)):
            for prime, power in sp.factorint(integer).items():
                key = int(prime)
                result[key] = result.get(key, F(0)) + coefficient * int(power) * sign
    return {prime: coefficient for prime, coefficient in result.items() if coefficient}


def curvature_log_terms(p: dict[str, sp.Expr], at: sp.Rational) -> list[tuple[F, F]]:
    return [(-frac(sp.diff(value, t, 2).subs(t, at)), frac(value.subs(t, at)))
            for value in p.values()]


def dump_polynomials(name: str, p: dict[str, sp.Expr]) -> None:
    obj = {bits: {
        "expression": str(value),
        "coefficients_ascending_t": [str(c) for c in reversed(sp.Poly(value, t).all_coeffs())]
    } for bits, value in p.items()}
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main() -> None:
    emit("I05-W1-20260909 exact verification")
    emit(f"Python {platform.python_version()}; SymPy {sp.__version__}; atanh terms={N_TERMS}")
    emit("All asserted signs use exact rational interval endpoints, not floating-point values.")

    C = sp.Matrix([[R(1,2), R(2,5)], [R(2,5), R(1,2)]])
    u, v = sp.Matrix([1,1]), sp.Matrix([1,-1])
    record("Loewner mixed Hessian", linear_logs([(F(8), F(41,9))], F(-200,41)), "+")
    assert F(8)*F(32,25)-F(200,41) > 0

    K3 = sp.Matrix([[R(1,2),R(1,10),R(1,10)],
                    [R(1,10),R(1,2),R(2,5)],
                    [R(1,10),R(2,5),R(1,2)]])
    D3 = sp.Matrix([[0,1,-1],[1,0,0],[-1,0,0]])
    p3 = probabilities(K3+t*D3)
    check_inclusion_exclusion(K3+t*D3, p3)
    dump_polynomials("conditional_3point_probabilities.json", p3)
    emit("\nThree-point exact probabilities (bits x1x2x3):")
    for bits, value in p3.items():
        emit(f"  {bits}: {value}")
    minors_k = [frac(K3[:i,:i].det()) for i in (1,2,3)]
    minors_ik = [frac((sp.eye(3)-K3)[:i,:i].det()) for i in (1,2,3)]
    assert all(q > 0 for q in minors_k+minors_ik)
    emit(f"Sylvester K: {list(map(str,minors_k))}; I-K: {list(map(str,minors_ik))}")
    for at in (R(-1,100), R(1,100)):
        for M in (K3+at*D3, sp.eye(3)-K3-at*D3):
            assert all(M[:i,:i].det() > 0 for i in (1,2,3))
    emit("K3+tD3 is strictly valid on [-1/100,1/100] by endpoint Sylvester and convexity.")
    C1, C0 = C-R(1,50)*u*u.T, C+R(1,50)*u*u.T
    acc_terms = [(2*a,b) for a,b in gradient_terms(C0,v*v.T)]
    acc_terms += [(-2*a,b) for a,b in gradient_terms(C1,v*v.T)]
    acc = linear_logs(acc_terms)
    record("Conditional nonaffine acceleration A", acc, "+")
    integer_formula_terms = [(F(k,25),F(b)) for b,k in
                             ((27,6),(43,86),(213,88),(197,-72),(47,-94),(63,-14))]
    assert prime_log_coefficients(acc_terms) == prime_log_coefficients(integer_formula_terms)
    assert 27**6 * 43**86 * 213**88 > 197**72 * 47**94 * 63**14
    emit("Positive conditional acceleration also certified by an exact integer-product inequality.")
    fisher, geom, hess3 = curvature(p3, R(0))
    assert fisher == F(32800,41961)
    emit(f"Complete 3-point Fisher = {fisher}")
    record("Complete 3-point geometric term", geom, "-")
    record("Complete 3-point H_second", hess3, "-")
    V1, V0 = sp.diag(R(-2,5),R(2,5)), sp.diag(R(2,5),R(-2,5))
    f1,g1,h1 = curvature(probabilities(C1+t*V1), R(0))
    f0,g0,h0 = curvature(probabilities(C0+t*V0), R(0))
    record("Conditional H1 tangent Hessian", h1, "-")
    record("Conditional H0 tangent Hessian", h0, "-")
    assert fisher == (f1+f0)/2
    reconstructed = ((h1[0]+h0[0])/2+acc[0], (h1[1]+h0[1])/2+acc[1])
    assert max(reconstructed[0],hess3[0]) <= min(reconstructed[1],hess3[1])
    conditional_logs = [(a/2,b) for a,b in curvature_log_terms(probabilities(C1+t*V1),R(0))]
    conditional_logs += [(a/2,b) for a,b in curvature_log_terms(probabilities(C0+t*V0),R(0))]
    conditional_logs += acc_terms
    assert prime_log_coefficients(curvature_log_terms(p3,R(0))) == prime_log_coefficients(conditional_logs)
    emit("Conditional chain-rule Hessian equals the direct Hessian: exact prime-log coefficients and rational Fisher match.")
    # Pure rational bound used in proof.md for the global geometric term.
    assert F(256,985)-F(72,235) == F(-2152,46295) < 0

    p2 = probabilities(C+t*sp.eye(2))
    check_inclusion_exclusion(C+t*sp.eye(2), p2)
    dump_polynomials("quantum_2point_probabilities.json", p2)
    center = eval_prob(p2,R(0))
    minus, plus = eval_prob(p2,R(-1,20)), eval_prob(p2,R(1,20))
    mixture = {bits:(minus[bits]+plus[bits])/2 for bits in center}
    emit("\nQuantum bridge obstruction: probabilities in order 00,01,10,11")
    for name, prob in (("center",center),("minus",minus),("plus",plus),("mixture",mixture)):
        emit(f"  {name}: {[str(q) for q in prob.values()]}")
    hc, hm, hp, hq = map(entropy,(center,minus,plus,mixture))
    record("Measured mixture H(q)-H(center)", (hq[0]-hc[1], hq[1]-hc[0]), "+")
    record("Actual 2-point midpoint chord", ((hm[0]+hp[0])/2-hc[1],(hm[1]+hp[1])/2-hc[0]), "-")
    record("2-point H_second at center", curvature(p2,R(0))[2], "-")

    # Analytic two-point coherence curvature, also verified by symbolic differentiation.
    K_coh=sp.Matrix([[R(1,2),t],[t,R(1,2)]])
    p_coh=probabilities(K_coh)
    h_coh=-sum(q*sp.log(q) for q in p_coh.values())
    hb=lambda q:-q*sp.log(q)-(1-q)*sp.log(1-q)
    spectral_coh=2*hb(R(1,2)+t)
    assert sp.simplify(sp.diff(h_coh,t,2).subs(t,0))==0
    assert sp.simplify(sp.diff(spectral_coh,t,2).subs(t,0))==-8
    assert sp.simplify(sp.diff(h_coh-spectral_coh,t,2).subs(t,0))==8
    emit("Two-point coherence correction has exact second derivative +8 at t=0.")

    A = sp.Matrix([[R(2,5),R(1,10)],[R(1,10),R(3,5)]])
    Bblock = sp.Matrix([[R(1,3),R(1,20)],[R(1,20),R(2,3)]])
    a, b = sp.Matrix([R(1,5),R(1,10)]), sp.Matrix([1,R(1,2)])
    cross = a*b.T
    K4 = A.row_join(t*cross).col_join((t*cross.T).row_join(Bblock))
    D4 = sp.diff(K4,t)
    p4 = probabilities(K4)
    check_inclusion_exclusion(K4,p4)
    pA, pB = probabilities(A), probabilities(Bblock)
    dA = {k:sp.diff(val,t).subs(t,0) for k,val in probabilities(A+t*a*a.T).items()}
    dB = {k:sp.diff(val,t).subs(t,0) for k,val in probabilities(Bblock+t*b*b.T).items()}
    for bits,value in p4.items():
        ss,tt = bits[:2], bits[2:]
        assert sp.simplify(value-pA[ss]*pB[tt]+t*t*dA[ss]*dB[tt]) == 0
    for ss in pA:
        assert sp.simplify(sum(val for bits,val in p4.items() if bits[:2]==ss)-pA[ss]) == 0
    for tt in pB:
        assert sp.simplify(sum(val for bits,val in p4.items() if bits[2:]==tt)-pB[tt]) == 0
    dump_polynomials("rank_one_crossblock_4point_probabilities.json",p4)
    assert D4.rank() == 2
    commutator = sp.simplify(K4*D4-D4*K4)
    assert commutator != sp.zeros(4)
    emit("\nFour-point theorem example:")
    emit(f"A={A.tolist()}; C={Bblock.tolist()}; u={a.T.tolist()}; v={b.T.tolist()}")
    emit(f"D rank={D4.rank()}, commutator={commutator.tolist()}")
    alpha = (a.T*A.inv()*a)[0]*(b.T*Bblock.inv()*b)[0]
    beta = (a.T*(sp.eye(2)-A).inv()*a)[0]*(b.T*(sp.eye(2)-Bblock).inv()*b)[0]
    tau2 = min(1/alpha,1/beta)
    emit(f"Exact maximal strict interval: |t|<sqrt({tau2})")
    assert tau2 > R(1,4)
    for at in (R(-1,2),R(1,2)):
        V = K4.subs(t,at)
        for M in (V,sp.eye(4)-V):
            assert all(M[:i,:i].det() > 0 for i in range(1,5))
    emit("All 16 probability identities, both fixed marginals, and strict validity checked exactly.")
    record("4-point H_second at t=1/4",curvature(p4,R(1,4))[2],"-")
    em,ec,ep = [entropy(eval_prob(p4,at)) for at in (R(1,8),R(1,4),R(3,8))]
    record("4-point midpoint chord center=1/4 step=1/8",((em[0]+ep[0])/2-ec[1],(em[1]+ep[1])/2-ec[0]),"-")
    # Exact quartic coefficient factorization at the independent-block center.
    coeffs = {bits:frac(sp.expand(value).coeff(t,2)) for bits,value in p4.items()}
    fisher_a=sum((frac(dA[k])**2/frac(pA[k]) for k in pA),F(0))
    fisher_b=sum((frac(dB[k])**2/frac(pB[k]) for k in pB),F(0))
    quartic=-sum((coeffs[k]**2/frac(p4[k].subs(t,0)) for k in p4),F(0))/2
    assert quartic == -fisher_a*fisher_b/2 < 0
    emit(f"Exact leading quartic entropy coefficient = {quartic}")

    # The same probability identity for a nonreal Hermitian example.
    I = sp.I
    Ac=sp.Matrix([[R(1,2),I/10],[-I/10,R(3,5)]])
    Cc=sp.Matrix([[R(2,5),R(1,20)],[R(1,20),R(11,20)]])
    uc=sp.Matrix([R(1,10),I/10]);vc=sp.Matrix([1,I/2])
    Bc=uc*vc.conjugate().T
    Kc=Ac.row_join(t*Bc).col_join((t*Bc.conjugate().T).row_join(Cc))
    pc=probabilities(Kc)
    check_inclusion_exclusion(Kc,pc)
    pAc,pCc=probabilities(Ac),probabilities(Cc)
    dAc={k:sp.diff(q,t).subs(t,0) for k,q in probabilities(Ac+t*uc*uc.conjugate().T).items()}
    dCc={k:sp.diff(q,t).subs(t,0) for k,q in probabilities(Cc+t*vc*vc.conjugate().T).items()}
    for bits,q in pc.items():
        left,right=bits[:2],bits[2:]
        assert sp.simplify(q-pAc[left]*pCc[right]+t*t*dAc[left]*dCc[right])==0
    assert all(sp.Poly(value,t).degree() <= 2 and sp.expand(value).coeff(t,1)==0 for value in pc.values())
    for at in (R(-1,2),R(1,2)):
        V=Kc.subs(t,at)
        for M in (V,sp.eye(4)-V):
            assert all(M[:i,:i].det() > 0 for i in range(1,5))
    dump_polynomials("complex_crossblock_4point_probabilities.json",pc)
    record("Complex-Hermitian restricted example H_second at t=1/4",curvature(pc,R(1,4))[2],"-")

    A2=C2=sp.eye(2)/2;B2=sp.eye(2)/10
    K_rank2=A2.row_join(t*B2).col_join((t*B2.T).row_join(C2))
    full=sp.factor(K_rank2.det())
    assert sp.expand(full)==R(1,16)-t*t/200+t**4/10000
    emit(f"\nRank-two crossblock exact obstruction to s-affinity: p(1111)={full}")
    emit("This is an obstruction to the affine-in-s method, not an entropy counterexample.")
    (DATA/'certificates.json').write_text(json.dumps(certificates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    emit("\nALL EXACT CHECKS PASSED")
    (DATA/'verification_output.txt').write_text('\n'.join(report)+'\n',encoding='utf-8')
    (DATA/'versions.json').write_text(json.dumps({"python":platform.python_version(),"sympy":sp.__version__,"atanh_terms":N_TERMS},indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
