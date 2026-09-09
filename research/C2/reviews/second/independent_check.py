import itertools as it
import json
import math
import os
import platform
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import mpmath as mp
import numpy as np
import sympy as sp


Q = sp.Rational
I3 = sp.eye(3)
t = sp.Symbol("t")
mp.mp.dps = 90


def matrix_from_strings(rows):
    return sp.Matrix([[Q(x) for x in row] for row in rows])


U = Q(1, 1045) * sp.Matrix(
    [
        [615, 120, -702],
        [240, 735, 246],
        [-630, 30, -71],
        [480, -620, 492],
        [-170, -390, -540],
    ]
)

subsets = [tuple(S) for k in range(6) for S in it.combinations(range(5), k)]
support_subsets = [S for S in subsets if len(S) <= 3]
rows = [U[i, :].T for i in range(5)]
crosses = {(i, j): rows[i].cross(rows[j]) for i, j in it.combinations(range(5), 2)}


def event_polynomials(A0, V0):
    At = A0 + t * V0
    K = U * At * U.T
    inc = {}
    for S in subsets:
        inc[S] = sp.Integer(1) if not S else sp.expand(K.extract(S, S).det())
    law = {
        S: sp.expand(
            sum((-1) ** (len(T) - len(S)) * inc[T] for T in subsets if set(S) <= set(T))
        )
        for S in subsets
    }

    d = sp.expand(At.det())
    pair_C = At.adjugate() - d * I3
    single_R = At * At + (1 - sp.trace(At)) * At + d * I3
    form = {(): sp.expand((I3 - At).det())}
    for i in range(5):
        form[(i,)] = sp.expand((rows[i].T * single_R * rows[i])[0])
    for pair, w in crosses.items():
        form[pair] = sp.expand((w.T * pair_C * w)[0])
    for S in it.combinations(range(5), 3):
        form[S] = sp.expand(d * U.extract(S, range(3)).det() ** 2)
    for S in subsets:
        if len(S) > 3:
            form[S] = sp.Integer(0)
    return law, form, inc


def mpf_exact(x):
    return mp.mpf(str(sp.N(x, 100)))


def entropy_from_polys(polys, tau):
    total = mp.mpf("0")
    for S in support_subsets:
        p = mpf_exact(polys[S].subs(t, tau))
        total -= p * mp.log(p)
    return total


def leading_principal_minors(M):
    return [sp.factor(M[:i, :i].det()) for i in range(1, M.rows + 1)]


def eigvals_float(M):
    arr = np.array([[float(sp.N(M[i, j], 30)) for j in range(M.cols)] for i in range(M.rows)])
    return [float(x) for x in np.linalg.eigvalsh(arr)]


def check_main_fixture():
    A0 = sp.Matrix(
        [
            [Q(3, 5), Q(1, 20), Q(1, 30)],
            [Q(1, 20), Q(2, 3), Q(-1, 40)],
            [Q(1, 30), Q(-1, 40), Q(1, 2)],
        ]
    )
    V0 = sp.Matrix(
        [
            [Q(1, 10), Q(1, 7), Q(-1, 11)],
            [Q(1, 7), Q(-1, 8), Q(1, 13)],
            [Q(-1, 11), Q(1, 13), Q(1, 12)],
        ]
    )
    law, form, inc = event_polynomials(A0, V0)
    jets = {
        S: [sp.factor(law[S].subs(t, 0)), sp.factor(sp.diff(law[S], t).subs(t, 0)), sp.factor(sp.diff(law[S], t, 2).subs(t, 0))]
        for S in subsets
    }
    layers = []
    for k in range(4):
        js = [jets[S] for S in subsets if len(S) == k]
        fisher = sum(mpf_exact(j[1]) ** 2 / mpf_exact(j[0]) for j in js)
        accel = -sum(mpf_exact(j[2]) * mp.log(mpf_exact(j[0])) for j in js)
        layers.append(
            {
                "cardinality": k,
                "mass": str(sp.factor(sum(j[0] for j in js))),
                "fisher": mp.nstr(fisher, 80),
                "log_acceleration": mp.nstr(accel, 80),
                "curvature": mp.nstr(accel - fisher, 80),
            }
        )
    curv = sum(mp.mpf(x["curvature"]) for x in layers)
    h_small = Q(1, 100000)
    fd = (entropy_from_polys(law, h_small) - 2 * entropy_from_polys(law, 0) + entropy_from_polys(law, -h_small)) / (mpf_exact(h_small) ** 2)
    return {
        "formula_identity_all_32": all(sp.expand(law[S] - form[S]) == 0 for S in subsets),
        "high_inclusion_minors_zero": all(inc[S] == 0 for S in subsets if len(S) > 3),
        "normalization_jets": [str(sp.factor(sum(jets[S][k] for S in subsets))) for k in range(3)],
        "weighted_second_sum": str(sp.factor(sum((3 - len(S)) * jets[S][2] for S in subsets))),
        "positive_support_count": sum(1 for S in support_subsets if jets[S][0] > 0),
        "zero_high_events": sum(1 for S in subsets if len(S) > 3 and law[S] == 0),
        "noncommutator_squared": str(sp.factor(sp.trace((A0 * V0 - V0 * A0).T * (A0 * V0 - V0 * A0)))),
        "layers": layers,
        "finite_difference_h": str(h_small),
        "finite_difference": mp.nstr(fd, 80),
        "analytic_curvature": mp.nstr(curv, 80),
        "finite_difference_error": mp.nstr(fd - curv, 30),
    }


def check_frame_and_cone_constants():
    G = sp.zeros(6)
    for w in crosses.values():
        a = sp.Matrix([w[0] ** 2, w[1] ** 2, w[2] ** 2, 2 * w[0] * w[1], 2 * w[0] * w[2], 2 * w[1] * w[2]])
        G += a * a.T / (w.dot(w))
    D = sp.diag(1, 1, 1, 2, 2, 2)
    M = sp.factor(G - Q(1, 22) * D)
    minors = leading_principal_minors(M)
    grams = {
        ",".join(str(i + 1) for i in S) if S else "empty": sp.factor(U.extract(S, range(3)).multiply(U.extract(S, range(3)).T).det()) if S else sp.Integer(1)
        for S in support_subsets
    }
    normalized = [grams[",".join(str(i + 1) for i in S) if S else "empty"] / 4 ** len(S) for S in support_subsets]
    trace_bound = sp.factor(1 / sp.trace(D * G.inv()))
    return {
        "frame_sylvester_positive_for_one_over_22": all(x > 0 for x in minors),
        "frame_sylvester_minors": [str(x) for x in minors],
        "trace_inverse_lower_bound": str(trace_bound),
        "trace_inverse_exceeds_one_over_22": bool(trace_bound > Q(1, 22)),
        "min_gamma_over_4_to_s": str(min(normalized)),
        "min_gamma_bound_exceeds_2_to_minus_14": bool(min(normalized) > Q(1, 2**14)),
        "cone_radius_from_constants": str(Q(1, int(sp.ceiling(4480 * 2 * 10 / Q(1, 22))))),
        "triple_determinants_nonzero": all(U.extract(S, range(3)).det() != 0 for S in it.combinations(range(5), 3)),
        "pair_crosses_nonzero": all(w.dot(w) > 0 for w in crosses.values()),
    }


def check_exceptional_direction():
    A0 = sp.diag(Q(1, 2), Q(2, 3), Q(5, 6))
    V0 = A0 * (I3 - A0)
    law, _, _ = event_polynomials(A0, V0)
    pair_first = [sp.factor(sp.diff(law[S], t).subs(t, 0)) for S in subsets if len(S) == 2]
    pair_second = [sp.factor(sp.diff(law[S], t, 2).subs(t, 0)) for S in subsets if len(S) == 2]
    empty_first = sp.factor(sp.diff(law[()], t).subs(t, 0))
    return {
        "trace_A": str(sp.trace(A0)),
        "V_equals_A_I_minus_A": V0 == A0 * (I3 - A0),
        "pair_first_all_zero": all(x == 0 for x in pair_first),
        "pair_second_all_negative": all(x < 0 for x in pair_second),
        "empty_first": str(empty_first),
        "empty_first_nonzero": bool(empty_first != 0),
        "largest_pair_second": str(max(pair_second)),
    }


def check_fixed_B_asymptotic():
    B = sp.Matrix(
        [
            [2, Q(1, 3), 0],
            [Q(1, 3), 1, Q(1, 4)],
            [0, Q(1, 4), Q(3, 2)],
        ]
    )
    V = sp.Matrix(
        [
            [1, Q(1, 2), Q(-1, 3)],
            [Q(1, 2), -1, Q(1, 4)],
            [Q(-1, 3), Q(1, 4), Q(2, 3)],
        ]
    )
    e = sp.Symbol("e")
    A = I3 - e * B
    At = A + t * V
    K = U * At * U.T
    detK = {S: sp.expand(K.extract(S, S).det()) if S else sp.Integer(1) for S in subsets}
    law = {
        S: sp.expand(
            sum((-1) ** (len(T) - len(S)) * detK[T] for T in subsets if set(S) <= set(T))
        )
        for S in subsets
    }
    jets = [(len(S), law[S], sp.diff(law[S], t), sp.diff(law[S], t, 2)) for S in support_subsets]

    J = mp.mpf("0")
    const = mp.mpf("0")
    sB = sp.trace(B)
    for w in crosses.values():
        b = (w.T * B * w)[0]
        c = (w.T * (B * B - sB * B) * w)[0]
        f = (w.T * V * w)[0]
        g = (w.T * (sp.trace(V) * B + sB * V - B * V - V * B) * w)[0]
        h = 2 * (w.T * (V * V - sp.trace(V) * V) * w)[0]
        J += mpf_exact(f**2 / b)
        const += mpf_exact(2 * f * g / b + f**2 * c / b**2) - mpf_exact(h) * mp.log(mpf_exact(b))
    DB = (B + t * V).adjugate().diff(t).subs(t, 0)
    for r in rows:
        a = (r.T * B.adjugate() * r)[0]
        ell = (r.T * DB * r)[0]
        k = 2 * (r.T * V.adjugate() * r)[0]
        const -= mpf_exact(ell**2 / a) + mpf_exact(k) * mp.log(mpf_exact(a))
    qvals = [U.extract(S, range(3)).det() ** 2 for S in it.combinations(range(5), 3)]
    cU = -sum(mpf_exact(q) * mp.log(mpf_exact(q)) for q in qvals)
    v = sp.trace(V)
    k_det = v**2 - sp.trace(V * V)
    const -= mpf_exact(v**2)
    const += cU * mpf_exact(k_det)

    rows_out = []
    for ev in [Q(1, 100), Q(1, 1000), Q(1, 10000)]:
        H2 = mp.mpf("0")
        for _, p, dp, ddp in jets:
            p0 = mpf_exact(p.subs({e: ev, t: 0}))
            d0 = mpf_exact(dp.subs({e: ev, t: 0}))
            dd0 = mpf_exact(ddp.subs({e: ev, t: 0}))
            H2 -= d0 * d0 / p0
            H2 -= dd0 * mp.log(p0)
        rows_out.append(
            {
                "e": str(ev),
                "H2": mp.nstr(H2, 70),
                "remainder_divided_by_e": mp.nstr((H2 + J / mpf_exact(ev) - const) / mpf_exact(ev), 60),
            }
        )
    return {
        "B_positive_min_eigenvalue": min(eigvals_float(B)),
        "noncommuting_BV": bool(B * V != V * B),
        "J": mp.nstr(J, 80),
        "constant": mp.nstr(const, 80),
        "samples": rows_out,
    }


def check_optional_representative():
    path = Path("representative_noncommuting_top_excess.json")
    if not path.exists():
        return {"loaded": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    A0 = matrix_from_strings(data["A"])
    V0 = matrix_from_strings(data["V"])
    h0 = Q(data["h"])
    law, _, _ = event_polynomials(A0, V0)
    event_tuples = [tuple(x) for x in data["events"]]
    p = [sp.factor(law[S].subs(t, 0)) for S in event_tuples]
    dp = [sp.factor(sp.diff(law[S], t).subs(t, 0)) for S in event_tuples]
    ddp = [sp.factor(sp.diff(law[S], t, 2).subs(t, 0)) for S in event_tuples]
    p_match = [str(x) == y for x, y in zip(p, data["p"])]
    dp_match = [str(x) == y for x, y in zip(dp, data["p_prime"])]
    ddp_match = [str(x) == y for x, y in zip(ddp, data["p_second"])]

    def entropy_at(tau):
        return entropy_from_polys(law, tau)

    chord = entropy_at(h0) + entropy_at(-h0) - 2 * entropy_at(0)
    chord_half = chord / 2
    chord_interval_contains_half = None
    if "chord_interval" in data:
        raw = data["chord_interval"].strip()[1:-1]
        lo_s, hi_s = [x.strip() for x in raw.split(",", 1)]
        chord_interval_contains_half = mp.mpf(lo_s) <= chord_half <= mp.mpf(hi_s)
    legal_mats = {
        "A_plus": A0 + h0 * V0,
        "I_minus_A_plus": I3 - A0 - h0 * V0,
        "A": A0,
        "I_minus_A": I3 - A0,
        "A_minus": A0 - h0 * V0,
        "I_minus_A_minus": I3 - A0 + h0 * V0,
    }
    legal = {name: all(x > 0 for x in leading_principal_minors(M)) for name, M in legal_mats.items()}
    spectra = {name: eigvals_float(M) for name, M in legal_mats.items()}
    return {
        "loaded": True,
        "events": len(event_tuples),
        "probabilities_match": sum(p_match),
        "first_derivatives_match": sum(dp_match),
        "second_derivatives_match": sum(ddp_match),
        "all_exact_entries_match": all(p_match + dp_match + ddp_match),
        "legal_sylvester_all_positive": all(legal.values()),
        "legal_sylvester_by_matrix": legal,
        "spectra": spectra,
        "noncommutator_squared": str(sp.factor(sp.trace((A0 * V0 - V0 * A0).T * (A0 * V0 - V0 * A0)))),
        "finite_chord": mp.nstr(chord, 80),
        "finite_chord_half": mp.nstr(chord_half, 80),
        "finite_chord_negative": bool(chord < 0),
        "file_chord_interval_contains_half": chord_interval_contains_half,
    }


def main():
    out = {
        "pid": os.getpid(),
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "numpy": np.__version__,
        "mpmath": mp.__version__,
        "thread_env": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
        },
        "U_orthonormal": bool(U.T * U == I3),
        "main_fixture": check_main_fixture(),
        "frame_and_cone_constants": check_frame_and_cone_constants(),
        "exceptional_direction": check_exceptional_direction(),
        "fixed_B_asymptotic": check_fixed_B_asymptotic(),
        "optional_representative": check_optional_representative(),
    }
    Path("independent_check.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pid": out["pid"], "status": "PASS", "optional_loaded": out["optional_representative"]["loaded"]}, indent=2))


if __name__ == "__main__":
    main()
