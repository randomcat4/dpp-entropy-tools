#!/usr/bin/env python3
"""Exact checks for I05-W1 rank-two continuation.

No floating-point sign decisions are used. SymPy Rational arithmetic verifies
all determinant, event-probability, conditioning, Markov, and obstruction
claims used by the continuation theorem package.
"""

from __future__ import annotations

from pathlib import Path
import json
import sympy as sp

Q = sp.Rational


def bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def event_probability(K: sp.Matrix, mask: int) -> sp.Rational:
    """Complete-event probability via the signed event determinant."""
    n = K.rows
    E = sp.zeros(n)
    for i in range(n):
        if not ((mask >> i) & 1):
            E[i, i] = 1
    return sp.factor((-1) ** (n - mask.bit_count()) * (K - E).det())


def event_law(K: sp.Matrix) -> list[sp.Rational]:
    return [event_probability(K, mask) for mask in range(1 << K.rows)]


def assert_strict_contraction(K: sp.Matrix) -> None:
    assert K == K.T
    n = K.rows
    I = sp.eye(n)
    for j in range(1, n + 1):
        assert sp.factor(K[:j, :j].det()) > 0
        assert sp.factor((I - K)[:j, :j].det()) > 0


def block_matrix(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix, t: sp.Rational) -> sp.Matrix:
    return A.row_join(t * B).col_join((t * B.T).row_join(C))


def active_sector_checks() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    A = sp.Matrix([
        [Q(2, 5), Q(1, 20), Q(1, 30)],
        [Q(1, 20), Q(1, 2), Q(1, 25)],
        [Q(1, 30), Q(1, 25), Q(3, 5)],
    ])
    C = sp.diag(Q(1, 3), Q(1, 2), Q(2, 3), 0, 0)
    C[3, 3], C[3, 4], C[4, 3], C[4, 4] = Q(2, 5), Q(1, 20), Q(1, 20), Q(3, 5)
    B = sp.Matrix([
        [Q(1, 100), Q(1, 100), Q(1, 50), 0, 0],
        [Q(1, 50), 0, Q(3, 100), 0, 0],
        [Q(1, 100), -Q(1, 100), Q(1, 100), 0, 0],
    ])

    assert_strict_contraction(A)
    assert_strict_contraction(C)
    assert B.rank() == 2
    assert all(any(B[i, j] != 0 for i in range(B.rows)) for j in range(3))
    assert all(B[i, j] == 0 for i in range(B.rows) for j in (3, 4))
    assert C[:3, :3].is_diagonal()
    assert C[:3, 3:] == sp.zeros(3, 2)

    law_A = event_law(A)
    assert all(x > 0 for x in law_A) and sum(law_A) == 1

    for t in (Q(1, 5), Q(1, 2), Q(1, 1)):
        K = block_matrix(A, B, C, t)
        assert_strict_contraction(K)
        law_K = event_law(K)
        assert all(x > 0 for x in law_K) and sum(law_K) == 1

        for s_mask in range(1 << A.rows):
            E = sp.zeros(A.rows)
            for i in range(A.rows):
                if not ((s_mask >> i) & 1):
                    E[i, i] = 1
            X = A - E
            assert X.det() != 0
            M = sp.simplify(B.T * X.inv() * B)
            C_cond = sp.simplify(C - t * t * M)
            law_cond = event_law(C_cond)
            assert all(x > 0 for x in law_cond) and sum(law_cond) == 1

            p_s = law_A[s_mask]
            marginal = sp.Integer(0)
            for t_mask in range(1 << C.rows):
                full_mask = s_mask | (t_mask << A.rows)
                lhs = law_K[full_mask]
                rhs = sp.factor(p_s * law_cond[t_mask])
                assert sp.factor(lhs - rhs) == 0
                marginal += lhs
            assert sp.factor(marginal - p_s) == 0

    print("ACTIVE SECTOR CHECKS PASSED")
    return A, C, B


def diagonal_refresh_checks() -> None:
    c = [Q(1, 3), Q(1, 2), Q(2, 3)]
    V = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    theta = Q(2, 5)
    n = len(c)
    states = list(range(1 << n))

    def mu(mask: int) -> sp.Rational:
        out = sp.Integer(1)
        for i, ci in enumerate(c):
            out *= ci if ((mask >> i) & 1) else (1 - ci)
        return sp.factor(out)

    def z(mask: int, i: int) -> sp.Rational:
        return sp.factor((((mask >> i) & 1) - c[i]) / (c[i] * (1 - c[i])))

    def G(mask: int) -> sp.Matrix:
        out = sp.zeros(2)
        for i in range(n):
            vi = V[i, :].T
            out += z(mask, i) * vi * vi.T
        return sp.simplify(out)

    def d(mask: int) -> sp.Rational:
        direct = sp.factor(G(mask).det())
        mixed = sp.Integer(0)
        for i in range(n):
            for j in range(i + 1, n):
                two_rows = sp.Matrix.vstack(V[i, :], V[j, :])
                mixed += z(mask, i) * z(mask, j) * two_rows.det() ** 2
        assert sp.factor(direct - mixed) == 0
        return direct

    def transition(x: int, y: int) -> sp.Rational:
        p = sp.Integer(1)
        for i, ci in enumerate(c):
            xb, yb = (x >> i) & 1, (y >> i) & 1
            redraw = ci if yb else (1 - ci)
            p *= theta * int(xb == yb) + (1 - theta) * redraw
        return sp.factor(p)

    mus = [mu(x) for x in states]
    assert sum(mus) == 1
    Gs = [G(x) for x in states]
    ds = [d(x) for x in states]
    mean_G = sum((mus[x] * Gs[x] for x in states), sp.zeros(2))
    assert sp.simplify(mean_G) == sp.zeros(2)
    assert sp.factor(sum(mus[x] * ds[x] for x in states)) == 0

    for x in states:
        row = [transition(x, y) for y in states]
        assert sum(row) == 1 and all(p >= 0 for p in row)
        TG = sum((row[y] * Gs[y] for y in states), sp.zeros(2))
        Td = sum(row[y] * ds[y] for y in states)
        assert sp.simplify(TG - theta * Gs[x]) == sp.zeros(2)
        assert sp.factor(Td - theta ** 2 * ds[x]) == 0

    for y in states:
        incoming = sum(mus[x] * transition(x, y) for x in states)
        assert sp.factor(incoming - mus[y]) == 0
        for x in states:
            assert sp.factor(mus[x] * transition(x, y) - mus[y] * transition(y, x)) == 0

    print("DIAGONAL EXTERIOR-DEGREE CHECKS PASSED")


def quasi_free_obstruction_checks() -> None:
    Kp = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    Km = sp.Matrix([[Q(1, 2), -Q(1, 10)], [-Q(1, 10), Q(1, 2)]])
    A0 = sp.Matrix([[Q(1, 2), Q(1, 5)], [Q(1, 5), Q(1, 2)]])
    theta = Q(1, 2)
    for K in (Kp, Km, A0):
        assert_strict_contraction(K)
    assert event_law(Kp) == event_law(Km)
    assert event_law(Kp) == [Q(6, 25), Q(13, 50), Q(13, 50), Q(6, 25)]
    Op = sp.simplify(theta * Kp + (1 - theta) * A0)
    Om = sp.simplify(theta * Km + (1 - theta) * A0)
    assert event_probability(Op, 3) == Q(91, 400)
    assert event_probability(Om, 3) == Q(99, 400)
    assert event_law(Op) != event_law(Om)
    print("QUASI-FREE CLASSICAL-CHANNEL OBSTRUCTION CHECKED")


def generator_instance(output_path: Path) -> None:
    C = sp.Matrix([
        [Q(1, 2), Q(1, 12), Q(1, 15)],
        [Q(1, 12), Q(2, 5), Q(1, 20)],
        [Q(1, 15), Q(1, 20), Q(3, 5)],
    ])
    V = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    assert_strict_contraction(C)
    law = event_law(C)
    assert all(x > 0 for x in law) and sum(law) == 1

    rows = []
    for mask, p in enumerate(law):
        E = sp.zeros(3)
        for i in range(3):
            if not ((mask >> i) & 1):
                E[i, i] = 1
        Y = C - E
        G = sp.simplify(V.T * Y.inv() * V)
        rows.append({
            "state": "".join(str(b) for b in reversed(bits(mask, 3))),
            "mu": str(p),
            "G11": str(G[0, 0]),
            "G12": str(G[0, 1]),
            "G22": str(G[1, 1]),
            "detG": str(sp.factor(G.det())),
        })

    for key in ("G11", "G12", "G22", "detG"):
        moment = sum(sp.Rational(r["mu"]) * sp.Rational(r[key]) for r in rows)
        assert sp.factor(moment) == 0

    payload = {
        "C": [[str(C[i, j]) for j in range(3)] for i in range(3)],
        "V": [[str(V[i, j]) for j in range(2)] for i in range(3)],
        "state_rows": rows,
        "generator_target": {"G11": "-1", "G12": "-1", "G22": "-1", "detG": "-2"},
        "conductances": "w_xy=w_yx>=0; (Lf)(x)=mu_x^-1 sum_y w_xy(f_y-f_x)",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("GENERATOR LP INSTANCE WRITTEN")


def main() -> None:
    active_sector_checks()
    diagonal_refresh_checks()
    quasi_free_obstruction_checks()
    here = Path(__file__).resolve().parent
    generator_instance(here.parent / "inputs" / "generator_instance.json")
    print("ALL CONTINUATION CHECKS PASSED")


if __name__ == "__main__":
    main()
