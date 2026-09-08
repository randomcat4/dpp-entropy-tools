from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def popcount(x: int) -> int:
    return x.bit_count()


def perm_sign(p: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_fraction(M: list[list[Fraction]]) -> Fraction:
    n = len(M)
    if n == 0:
        return Fraction(1)
    total = Fraction(0)
    for p in permutations(range(n)):
        prod = Fraction(1)
        for i, j in enumerate(p):
            prod *= M[i][j]
        total += perm_sign(p) * prod
    return total


def principal_det(K: list[list[Fraction]], mask: int) -> Fraction:
    idx = [i for i in range(len(K)) if (mask >> i) & 1]
    return det_fraction([[K[i][j] for j in idx] for i in idx])


def atom_by_mobius(K: list[list[Fraction]], S: int) -> Fraction:
    n = len(K)
    C = ((1 << n) - 1) ^ S
    total = Fraction(0)
    A = C
    sub = A
    while True:
        total += ((-1) ** popcount(sub)) * principal_det(K, S | sub)
        if sub == 0:
            break
        sub = (sub - 1) & A
    return total


def atom_by_A(K: list[list[Fraction]], S: int) -> Fraction:
    n = len(K)
    A = [[K[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        if not ((S >> i) & 1):
            A[i][i] -= 1
    return ((-1) ** (n - popcount(S))) * det_fraction(A)


def poly_add(a: list[Fraction], b: list[Fraction], maxdeg: int) -> list[Fraction]:
    out = [Fraction(0)] * (maxdeg + 1)
    for i in range(maxdeg + 1):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return out


def poly_mul(a: list[Fraction], b: list[Fraction], maxdeg: int) -> list[Fraction]:
    out = [Fraction(0)] * (maxdeg + 1)
    for i, ai in enumerate(a[: maxdeg + 1]):
        if ai == 0:
            continue
        for j, bj in enumerate(b[: maxdeg + 1 - i]):
            if bj:
                out[i + j] += ai * bj
    return out


def det_poly(A: list[list[list[Fraction]]], maxdeg: int) -> list[Fraction]:
    n = len(A)
    total = [Fraction(0)] * (maxdeg + 1)
    for p in permutations(range(n)):
        prod = [Fraction(1)] + [Fraction(0)] * maxdeg
        for i, j in enumerate(p):
            prod = poly_mul(prod, A[i][j], maxdeg)
        if perm_sign(p) == 1:
            total = poly_add(total, prod, maxdeg)
        else:
            total = poly_add(total, [-c for c in prod], maxdeg)
    return total


def atom_poly_A(K: list[list[Fraction]], D: list[list[Fraction]], S: int, maxdeg: int) -> list[Fraction]:
    n = len(K)
    A: list[list[list[Fraction]]] = []
    for i in range(n):
        row = []
        for j in range(n):
            const = K[i][j] - (1 if i == j and not ((S >> i) & 1) else 0)
            row.append([const, D[i][j]] + [Fraction(0)] * (maxdeg - 1))
        A.append(row)
    p = det_poly(A, maxdeg)
    sign = (-1) ** (n - popcount(S))
    return [sign * c for c in p]


def frob2(D: list[list[Fraction]]) -> Fraction:
    return sum(D[i][j] * D[i][j] for i in range(len(D)) for j in range(len(D)))


def diagonal_H2_symbolic_check(x: list[Fraction], D: list[list[Fraction]]) -> dict:
    n = len(x)
    K = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i, xi in enumerate(x):
        K[i][i] = xi
    rational_part = Fraction(0)
    total_p2 = Fraction(0)
    log_x = [Fraction(0) for _ in range(n)]
    log_1mx = [Fraction(0) for _ in range(n)]
    for S in range(1 << n):
        coeff = atom_poly_A(K, D, S, 2)
        p0, p1, p2 = coeff[0], coeff[1], 2 * coeff[2]
        rational_part += -p1 * p1 / p0 - p2
        total_p2 += p2
        for i in range(n):
            if (S >> i) & 1:
                log_x[i] += -p2
            else:
                log_1mx[i] += -p2
    formula = -sum(D[i][i] * D[i][i] / (x[i] * (1 - x[i])) for i in range(n))
    return {
        "n": n,
        "total_p2_zero": total_p2 == 0,
        "log_x_coeffs_zero": all(c == 0 for c in log_x),
        "log_1_minus_x_coeffs_zero": all(c == 0 for c in log_1mx),
        "rational_part_equals_formula": rational_part == formula,
        "formula": str(formula),
        "frob2": str(frob2(D)),
    }


def dec(fr: Fraction) -> Decimal:
    return Decimal(fr.numerator) / Decimal(fr.denominator)


def entropy_H2_decimal(K: list[list[Fraction]], D: list[list[Fraction]], prec: int = 80) -> Decimal:
    n = len(K)
    total = Decimal(0)
    with localcontext() as ctx:
        ctx.prec = prec
        for S in range(1 << n):
            coeff = atom_poly_A(K, D, S, 2)
            p0, p1, p2 = coeff[0], coeff[1], 2 * coeff[2]
            dp0, dp1, dp2 = dec(p0), dec(p1), dec(p2)
            total += -(dp1 * dp1) / dp0 - (Decimal(1) + ctx.ln(dp0)) * dp2
    return +total


def explicit_delta(n: int, a: Fraction, b: Fraction, prec: int = 80) -> dict:
    with localcontext() as ctx:
        ctx.prec = prec
        s = min(dec(a), Decimal(1) - dec(b))
        q = s ** n
        m = q / Decimal(2)
        ell = max(Decimal(1), abs(Decimal(1) + ctx.ln(m)))
        L = (Decimal(2) ** n) * (
            (Decimal(n) ** 3) / (m * m)
            + (Decimal(3) * (Decimal(n) ** 2) * Decimal(n - 1)) / m
            + Decimal(n) * Decimal(n - 1) * Decimal(n - 2) * ell
        )
        delta = min(q / (Decimal(2) * Decimal(n)), Decimal(2) / (Decimal(n) * L))
        return {"s": str(s), "q": str(q), "m": str(m), "ell": str(ell), "L": str(L), "delta": str(delta)}


def theorem_bound_sample(n: int) -> dict:
    if n == 2:
        x = [Fraction(1, 3), Fraction(2, 5)]
        E = [[Fraction(1, 10**8), Fraction(-1, 2 * 10**8)],
             [Fraction(-1, 2 * 10**8), Fraction(-1, 10**8)]]
        D = [[Fraction(1), Fraction(1, 3)], [Fraction(1, 3), Fraction(1, 2)]]
        psd_principal_minors = [str(D[0][0]), str(det_fraction(D))]
    elif n == 3:
        x = [Fraction(1, 4), Fraction(2, 5), Fraction(3, 5)]
        E = [
            [Fraction(1, 10**10), Fraction(1, 2 * 10**10), Fraction(-1, 3 * 10**10)],
            [Fraction(1, 2 * 10**10), Fraction(-1, 10**10), Fraction(1, 4 * 10**10)],
            [Fraction(-1, 3 * 10**10), Fraction(1, 4 * 10**10), Fraction(1, 2 * 10**10)],
        ]
        v = [Fraction(1), Fraction(2), Fraction(-1)]
        D = [[v[i] * v[j] for j in range(n)] for i in range(n)]
        psd_principal_minors = ["rank_one_vvt"]
    else:
        raise ValueError(n)
    K = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i, xi in enumerate(x):
        K[i][i] = xi
    for i in range(n):
        for j in range(n):
            K[i][j] += E[i][j]
    a, b = Fraction(1, 5), Fraction(4, 5)
    delta_info = explicit_delta(n, a, b)
    with localcontext() as ctx:
        ctx.prec = 80
        e_norm = ctx.sqrt(dec(frob2(E)))
        h2 = entropy_H2_decimal(K, D)
        norm2 = dec(frob2(D))
        rhs = -(Decimal(2) / Decimal(n)) * norm2
    return {
        "n": n,
        "a": str(a),
        "b": str(b),
        "E_norm": str(e_norm),
        "delta": delta_info["delta"],
        "E_norm_le_delta": e_norm <= Decimal(delta_info["delta"]),
        "D_psd_certificate": psd_principal_minors,
        "H2": str(h2),
        "minus_2_over_n_frob2": str(rhs),
        "bound_holds": h2 <= rhs,
        "atom_floor_min_p": str(min(atom_by_A(K, S) for S in range(1 << n))),
    }


def generic_K(n: int) -> list[list[Fraction]]:
    K = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        K[i][i] = Fraction(i + 2, n + 5)
    for i in range(n):
        for j in range(i + 1, n):
            val = ((-1) ** (i + j)) * Fraction(i + 1, 1000 * (j + 1))
            K[i][j] = K[j][i] = val
    return K


def main() -> None:
    mobius = {}
    for n in (2, 3, 4):
        K = generic_K(n)
        mobius[f"n={n}"] = all(atom_by_A(K, S) == atom_by_mobius(K, S) for S in range(1 << n))

    diag_checks = [
        diagonal_H2_symbolic_check(
            [Fraction(1, 3), Fraction(2, 5)],
            [[Fraction(2), Fraction(3, 7)], [Fraction(3, 7), Fraction(-1, 2)]],
        ),
        diagonal_H2_symbolic_check(
            [Fraction(1, 4), Fraction(2, 5), Fraction(3, 5)],
            [
                [Fraction(1), Fraction(1, 2), Fraction(-1, 3)],
                [Fraction(1, 2), Fraction(-2, 3), Fraction(1, 4)],
                [Fraction(-1, 3), Fraction(1, 4), Fraction(3, 2)],
            ],
        ),
        diagonal_H2_symbolic_check(
            [Fraction(1, 5), Fraction(1, 3), Fraction(2, 5), Fraction(3, 5)],
            [
                [Fraction(1), Fraction(1, 3), Fraction(0), Fraction(-1, 4)],
                [Fraction(1, 3), Fraction(-1), Fraction(1, 5), Fraction(1, 6)],
                [Fraction(0), Fraction(1, 5), Fraction(2), Fraction(-1, 7)],
                [Fraction(-1, 4), Fraction(1, 6), Fraction(-1, 7), Fraction(1, 2)],
            ],
        ),
    ]

    samples = [theorem_bound_sample(2), theorem_bound_sample(3)]
    out = {
        "status": "PASS" if all(mobius.values()) and all(
            c["total_p2_zero"]
            and c["log_x_coeffs_zero"]
            and c["log_1_minus_x_coeffs_zero"]
            and c["rational_part_equals_formula"]
            for c in diag_checks
        ) and all(s["E_norm_le_delta"] and s["bound_holds"] for s in samples) else "FAIL",
        "mobius_equals_A_formula": mobius,
        "diagonal_H2_symbolic_checks": diag_checks,
        "explicit_radius_samples": samples,
    }
    (ROOT / "fresh_sanity_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
