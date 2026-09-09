#!/usr/bin/env python3
"""Independent high-precision diagnostics for sparse_proof.md.

The script rebuilds the six-coordinate Hessian objects from the eight atom
probabilities. It checks asymptotic coefficients and endpoint signs for fixed
test values only; the analytic review is in SPARSE_REVIEW.md.
"""

from __future__ import annotations

import json
import math
import os
import platform
import sys

import mpmath as mp


mp.mp.dps = 100
SIG = [-1, 1, 1, 1, -1, -1, -1, 1]


def st(x, digits=30):
    return mp.nstr(x, digits)


def outer(u, v):
    return u * v.T


def trace(M):
    return sum(M[i, i] for i in range(M.rows))


def det3(K):
    return (
        K[0, 0] * (K[1, 1] * K[2, 2] - K[1, 2] * K[2, 1])
        - K[0, 1] * (K[1, 0] * K[2, 2] - K[1, 2] * K[2, 0])
        + K[0, 2] * (K[1, 0] * K[2, 1] - K[1, 1] * K[2, 0])
    )


def coords(K):
    return [K[0, 0], K[1, 1], K[2, 2], K[0, 1], K[0, 2], K[1, 2]]


def mat_from_coords(v):
    x, y, z, a, b, c = v
    return mp.matrix([[x, a, b], [a, y, c], [b, c, z]])


def explicit_probs(v):
    x, y, z, a, b, c = v
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
    return [
        1 - x - y - z + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        z - q13 - q23 + r,
        q12 - r,
        q13 - r,
        q23 - r,
        r,
    ]


def zero66():
    return [[mp.mpf("0") for _ in range(6)] for __ in range(6)]


def add_hess(*items):
    out = zero66()
    for coeff, H in items:
        for i in range(6):
            for j in range(6):
                out[i][j] += coeff * H[i][j]
    return out


def add_grad(*items):
    return [sum(coeff * G[i] for coeff, G in items) for i in range(6)]


def p_derivatives(v):
    x, y, z, a, b, c = v
    gq12 = [y, x, 0, -2 * a, 0, 0]
    Hq12 = zero66()
    Hq12[0][1] = Hq12[1][0] = 1
    Hq12[3][3] = -2
    gq13 = [z, 0, x, 0, -2 * b, 0]
    Hq13 = zero66()
    Hq13[0][2] = Hq13[2][0] = 1
    Hq13[4][4] = -2
    gq23 = [0, z, y, 0, 0, -2 * c]
    Hq23 = zero66()
    Hq23[1][2] = Hq23[2][1] = 1
    Hq23[5][5] = -2
    gr = [
        y * z - c * c,
        x * z - b * b,
        x * y - a * a,
        2 * b * c - 2 * z * a,
        2 * a * c - 2 * y * b,
        2 * a * b - 2 * x * c,
    ]
    Hr = zero66()
    Hr[0][1] = Hr[1][0] = z
    Hr[0][2] = Hr[2][0] = y
    Hr[1][2] = Hr[2][1] = x
    Hr[0][5] = Hr[5][0] = -2 * c
    Hr[1][4] = Hr[4][1] = -2 * b
    Hr[2][3] = Hr[3][2] = -2 * a
    Hr[3][3] = -2 * z
    Hr[4][4] = -2 * y
    Hr[5][5] = -2 * x
    Hr[3][4] = Hr[4][3] = 2 * c
    Hr[3][5] = Hr[5][3] = 2 * b
    Hr[4][5] = Hr[5][4] = 2 * a

    lin0 = [-1, -1, -1, 0, 0, 0]
    lin1 = [1, 0, 0, 0, 0, 0]
    lin2 = [0, 1, 0, 0, 0, 0]
    lin3 = [0, 0, 1, 0, 0, 0]
    dp = [
        add_grad((1, lin0), (1, gq12), (1, gq13), (1, gq23), (-1, gr)),
        add_grad((1, lin1), (-1, gq12), (-1, gq13), (1, gr)),
        add_grad((1, lin2), (-1, gq12), (-1, gq23), (1, gr)),
        add_grad((1, lin3), (-1, gq13), (-1, gq23), (1, gr)),
        add_grad((1, gq12), (-1, gr)),
        add_grad((1, gq13), (-1, gr)),
        add_grad((1, gq23), (-1, gr)),
        gr,
    ]
    ddp = [
        add_hess((1, Hq12), (1, Hq13), (1, Hq23), (-1, Hr)),
        add_hess((-1, Hq12), (-1, Hq13), (1, Hr)),
        add_hess((-1, Hq12), (-1, Hq23), (1, Hr)),
        add_hess((-1, Hq13), (-1, Hq23), (1, Hr)),
        add_hess((1, Hq12), (-1, Hr)),
        add_hess((1, Hq13), (-1, Hr)),
        add_hess((1, Hq23), (-1, Hr)),
        Hr,
    ]
    return dp, ddp


def basis():
    mats = []
    for i in range(6):
        E = mp.zeros(3)
        if i < 3:
            E[i, i] = 1
        elif i == 3:
            E[0, 1] = E[1, 0] = 1
        elif i == 4:
            E[0, 2] = E[2, 0] = 1
        else:
            E[1, 2] = E[2, 1] = 1
        mats.append(E)
    return mats


E_BASIS = basis()


def quadratic(A, x, y):
    return sum(x[i] * A[i, j] * y[j] for i in range(6) for j in range(6))


def dot(x, y):
    return sum(x[i] * y[i] for i in range(len(x)))


def qdata(K):
    v = coords(K)
    p = explicit_probs(v)
    dp, ddp = p_derivatives(v)
    F = mp.zeros(6)
    g = [mp.mpf("0") for _ in range(6)]
    Z = mp.mpf("0")
    for r in range(8):
        Z += 1 / p[r]
        for i in range(6):
            g[i] += SIG[r] * dp[r][i] / p[r]
            for j in range(6):
                F[i, j] += dp[r][i] * dp[r][j] / p[r]
    Fpair = mp.matrix(F)
    for i in range(6):
        for j in range(6):
            Fpair[i, j] -= g[i] * g[j] / Z

    ell12 = mp.log(p[0] * p[4] / (p[1] * p[2]))
    ell13 = mp.log(p[0] * p[5] / (p[1] * p[3]))
    ell23 = mp.log(p[0] * p[6] / (p[2] * p[3]))
    Lam = mp.log(p[7] * p[1] * p[2] * p[3] / (p[0] * p[4] * p[5] * p[6]))
    N = -Lam * K
    N[0, 0] -= ell23
    N[1, 1] -= ell13
    N[2, 2] -= ell12
    d = det3(N)
    W = mp.inverse(N)
    eta = [trace(W * Ei) for Ei in E_BASIS]
    G = mp.zeros(6)
    for i, Ei in enumerate(E_BASIS):
        for j, Ej in enumerate(E_BASIS):
            G[i, j] = trace(W * Ei * W * Ej)
    M = Fpair + d * G
    h = mp.lu_solve(M, mp.matrix(eta))
    alpha = dot(eta, h)
    raw = dot(g, h)
    beta = raw / mp.sqrt(Z)
    return {"p": p, "dp": dp, "F": F, "Fpair": Fpair, "g": g, "Z": Z, "N": N, "d": d, "eta": eta, "G": G, "M": M, "h": h, "alpha": alpha, "raw": raw, "beta": beta}


def direction_vectors(s):
    w = mp.matrix([mp.sqrt(s), mp.sqrt(1 - s), 0])
    n = mp.matrix([mp.sqrt(1 - s), -mp.sqrt(s), 0])
    e = mp.matrix([0, 0, 1])
    dirs = {
        "U": outer(w, w),
        "T": outer(w, n) + outer(n, w),
        "Q": outer(n, n),
        "V": outer(w, e) + outer(e, w),
        "W": outer(n, e) + outer(e, n),
        "Z0": outer(e, e),
    }
    return {name: coords(D) for name, D in dirs.items()}, dirs


def sparse_K(lam, s, eps, kap):
    weights = [s * (1 - kap * eps), (1 - s) * (1 - kap * eps), kap * eps]
    u = mp.matrix([mp.sqrt(x) for x in weights])
    return eps * mp.eye(3) + lam * outer(u, u)


def coeffs(lam, kap):
    a = 1 - lam
    A = a + lam * kap
    R = 1 + lam * kap
    m = mp.log(A / a)
    D = a + lam * lam * kap
    J = 2 * lam * kap + m * D
    C = kap * ((2 * lam - 1) - lam * a * m) / (a * J)
    return a, A, R, m, D, J, C


def sample_record(eps, kap, lam=mp.mpf(7) / 10, s=mp.mpf(2) / 5):
    K = sparse_K(lam, s, eps, kap)
    q = qdata(K)
    dv, dmats = direction_vectors(s)
    L = -mp.log(eps)
    a, A, R, m, D, J, C = coeffs(lam, kap)
    U, V, Z0 = dv["U"], dv["V"], dv["Z0"]
    common = [0, 1, 2]
    rare = [3, 5, 6]
    def fisher_group(rows, X, Y):
        return sum(dot(q["dp"][r], X) * dot(q["dp"][r], Y) / q["p"][r] for r in rows)
    total_UV = quadratic(q["F"], U, V) / mp.sqrt(eps)
    common_UV = fisher_group(common, U, V) / mp.sqrt(eps)
    rare_UV = fisher_group(rare, U, V) / mp.sqrt(eps)
    proj_UV = dot(q["g"], U) * dot(q["g"], V) / q["Z"] / mp.sqrt(eps)
    hmat = sum(q["h"][i] * E_BASIS[i] for i in range(6))
    w = mp.matrix([mp.sqrt(s), mp.sqrt(1 - s), 0])
    e = mp.matrix([0, 0, 1])
    n = mp.matrix([mp.sqrt(1 - s), -mp.sqrt(s), 0])
    S11_actual = [
        [quadratic(q["M"], V, V), mp.sqrt(eps) * quadratic(q["M"], V, Z0)],
        [mp.sqrt(eps) * quadratic(q["M"], V, Z0), eps * quadratic(q["M"], Z0, Z0)],
    ]
    det_actual = S11_actual[0][0] * S11_actual[1][1] - S11_actual[0][1] ** 2
    return {
        "eps": st(eps),
        "kappa": st(kap),
        "C_closed": st(C),
        "L_raw_minus_C": st(L * q["raw"] - C),
        "scaled_beta_minus_C": st(q["beta"] * L / (eps * mp.sqrt(lam)) - C),
        "lambda_L_gap": st(lam * L * (1 - q["d"] * q["alpha"])),
        "beta": st(q["beta"]),
        "dalpha": st(q["d"] * q["alpha"]),
        "pmin": st(min(q["p"])),
        "F_UV_total_over_sqrt_eps": st(total_UV),
        "F_UV_common_over_sqrt_eps": st(common_UV),
        "F_UV_rare_over_sqrt_eps": st(rare_UV),
        "F_UV_projection_over_sqrt_eps": st(proj_UV),
        "F_UV_total_limit": st(-2 * mp.sqrt(kap) * R ** 2 / A + 2 * mp.sqrt(kap) / a),
        "S11_det_actual": st(det_actual),
        "S11_det_limit": st(2 * J / A),
        "S11_min_diag_actual": st(min(S11_actual[0][0], S11_actual[1][1])),
        "hU_times_L": st((w.T * hmat * w)[0] * L),
        "hV_times_L_over_sqrt_eps": st((w.T * hmat * e)[0] * L / mp.sqrt(eps)),
        "hZ_times_L_over_eps": st(hmat[2, 2] * L / eps),
        "hW_scaled_check": st((n.T * hmat * e)[0] * mp.sqrt(eps) ** -1 * L ** 2),
    }


def beta_at(eps, kap):
    return qdata(sparse_K(mp.mpf(7) / 10, mp.mpf(2) / 5, eps, kap))["beta"]


def bisect_root(eps):
    lo = mp.mpf(1)
    hi = mp.mpf(10)
    flo = beta_at(eps, lo)
    fhi = beta_at(eps, hi)
    for _ in range(80):
        mid = (lo + hi) / 2
        fm = beta_at(eps, mid)
        if flo * fm <= 0:
            hi = mid
            fhi = fm
        else:
            lo = mid
            flo = fm
    root = (lo + hi) / 2
    q = qdata(sparse_K(mp.mpf(7) / 10, mp.mpf(2) / 5, eps, root))
    kstar = (mp.mpf(3) / 7) * (mp.e ** (mp.mpf(40) / 21) - 1)
    L = -mp.log(eps)
    return {
        "eps": st(eps),
        "beta_at_1": st(beta_at(eps, mp.mpf(1))),
        "beta_at_10": st(beta_at(eps, mp.mpf(10))),
        "root_mid_after_80_bisections": st(root),
        "kappa_star": st(kstar),
        "L_times_root_minus_kstar": st(L * (root - kstar)),
        "root_beta": st(q["beta"]),
        "root_dalpha": st(q["d"] * q["alpha"]),
        "lambda_L_root_gap": st((mp.mpf(7) / 10) * L * (1 - q["d"] * q["alpha"])),
    }


def main():
    eps1 = mp.mpf("1e-12")
    eps2 = mp.mpf("1e-24")
    rows = [sample_record(eps1, mp.mpf(1)), sample_record(eps1, mp.mpf(10)), sample_record(eps2, mp.mpf(1)), sample_record(eps2, mp.mpf(10))]
    roots = [bisect_root(eps1), bisect_root(eps2)]
    c1 = coeffs(mp.mpf(7) / 10, mp.mpf(1))[-1]
    c10 = coeffs(mp.mpf(7) / 10, mp.mpf(10))[-1]
    pass_checks = [
        c1 > 0,
        c10 < 0,
        all(mp.mpf(row["pmin"]) > 0 for row in rows),
        beta_at(eps2, mp.mpf(1)) > 0,
        beta_at(eps2, mp.mpf(10)) < 0,
        all(mp.mpf(root["root_dalpha"]) < 1 for root in roots),
    ]
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "pid": os.getpid(),
        "exit_status_if_printed": 0 if all(pass_checks) else 1,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "digits": mp.mp.dps,
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "closed_form": {
            "C_1": st(c1),
            "C_10": st(c10),
            "kappa_star": st((mp.mpf(3) / 7) * (mp.e ** (mp.mpf(40) / 21) - 1)),
        },
        "rows": rows,
        "roots": roots,
        "non_coverage": [
            "Finite high-precision diagnostics only.",
            "No interval certificate or explicit epsilon threshold.",
            "No proof of global B0.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result["exit_status_if_printed"]


if __name__ == "__main__":
    raise SystemExit(main())
