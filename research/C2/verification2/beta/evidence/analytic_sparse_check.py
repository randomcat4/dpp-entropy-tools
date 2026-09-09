from __future__ import annotations

import json
import math
import os
import platform
import sys
from pathlib import Path

import mpmath as mp


mp.mp.dps = 90

COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
SIGNS = [(-1) ** (3 - int(mask).bit_count()) for mask in range(8)]


def det3(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def cofactor(A, i, j):
    rows = [r for r in range(3) if r != i]
    cols = [c for c in range(3) if c != j]
    return ((-1) ** (i + j)) * (
        A[rows[0]][cols[0]] * A[rows[1]][cols[1]]
        - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
    )


def mmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def transpose(A):
    return [list(row) for row in zip(*A)]


def basis_mats():
    mats = []
    for i, j in COORDS:
        E = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
        E[i][j] = mp.mpf("1")
        E[j][i] = mp.mpf("1")
        mats.append(E)
    return mats


E_STD = basis_mats()


def coords(D):
    return [D[0][0], D[1][1], D[2][2], D[0][1], D[0][2], D[1][2]]


def quad(A, u, v):
    return sum(u[i] * A[i][j] * v[j] for i in range(6) for j in range(6))


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def event_data(K):
    p = []
    J = []
    for mask in range(8):
        M = [list(row) for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] -= 1
        sign = mp.mpf(SIGNS[mask])
        p.append(sign * det3(M))
        J.append([sign * (cofactor(M, i, j) + (cofactor(M, j, i) if i != j else 0)) for i, j in COORDS])
    return p, J


def eval_data(K):
    p, J = event_data(K)
    logp = [mp.log(x) for x in p]
    Z = sum(1 / x for x in p)
    g = [sum(mp.mpf(SIGNS[k]) * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    F = [[sum(J[k][i] * J[k][j] / p[k] for k in range(8)) for j in range(6)] for i in range(6)]
    Fpair = [[F[i][j] - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell12 = mp.log(p[0] * p[3] / (p[1] * p[2]))
    ell13 = mp.log(p[0] * p[5] / (p[1] * p[4]))
    ell23 = mp.log(p[0] * p[6] / (p[2] * p[4]))
    lam_log = mp.log(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-lam_log * K[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= ell23
    N[1][1] -= ell13
    N[2][2] -= ell12
    d = det3(N)
    W = mp.inverse(mp.matrix(N))
    Wl = [[W[i, j] for j in range(3)] for i in range(3)]
    eta = [trace(mmul(Wl, E)) for E in E_STD]
    G = [[trace(mmul(mmul(Wl, E_STD[i]), mmul(Wl, E_STD[j]))) for j in range(6)] for i in range(6)]
    M = [[Fpair[i][j] + d * G[i][j] for j in range(6)] for i in range(6)]
    h = mp.lu_solve(mp.matrix(M), mp.matrix(eta))
    h = [h[i] for i in range(6)]
    alpha = dot(eta, h)
    beta = dot([x / mp.sqrt(Z) for x in g], h)
    return {
        "p": p,
        "g": g,
        "Z": Z,
        "N": N,
        "detN": d,
        "eta": eta,
        "Fpair": Fpair,
        "dG": [[d * G[i][j] for j in range(6)] for i in range(6)],
        "M": M,
        "h": h,
        "alpha": alpha,
        "beta": beta,
        "g_dot_h": dot(g, h),
        "dalpha": d * alpha,
    }


def mat_from_cols(cols):
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def outer(u, v):
    return [[u[i] * v[j] for j in range(3)] for i in range(3)]


def plus(A, B):
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]


def basis_for_s(s):
    w = [mp.sqrt(s), mp.sqrt(1 - s), mp.mpf("0")]
    n = [mp.sqrt(1 - s), -mp.sqrt(s), mp.mpf("0")]
    e = [mp.mpf("0"), mp.mpf("0"), mp.mpf("1")]
    U = outer(w, w)
    T = plus(outer(w, n), outer(n, w))
    Q = outer(n, n)
    V = plus(outer(w, e), outer(e, w))
    W = plus(outer(n, e), outer(e, n))
    Z0 = outer(e, e)
    return {"P": mat_from_cols([w, n, e]), "U": U, "T": T, "Q": Q, "V": V, "W": W, "Z0": Z0}


def transform_N_to_basis(N, P):
    return mmul(transpose(P), mmul(N, P))


def h_coeffs(h_std, P):
    H = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
    for val, E in zip(h_std, E_STD):
        for i in range(3):
            for j in range(3):
                H[i][j] += val * E[i][j]
    Hb = mmul(transpose(P), mmul(H, P))
    return {
        "U": Hb[0][0],
        "T": Hb[0][1],
        "Q": Hb[1][1],
        "V": Hb[0][2],
        "W": Hb[1][2],
        "Z0": Hb[2][2],
    }


def family(eps, kappa, lam, s):
    u = [mp.sqrt(s * (1 - kappa * eps)), mp.sqrt((1 - s) * (1 - kappa * eps)), mp.sqrt(kappa * eps)]
    return [[(eps if i == j else 0) + lam * u[i] * u[j] for j in range(3)] for i in range(3)]


def expected(lam, kappa):
    a = 1 - lam
    A = a + lam * kappa
    R = 1 + lam * kappa
    m = mp.log(A / a)
    D = a + lam**2 * kappa
    J = 2 * lam * kappa + m * D
    H = 1 / A + 1 / lam
    Fav = -2 * mp.sqrt(kappa) * R**2 / A + 2 * mp.sqrt(kappa) / a
    Faz = R * (1 - a / A)
    v = mp.sqrt(kappa) * lam * kappa * (lam + (1 - 2 * lam) / (a * m)) / J
    z = (lam * kappa * R + m * A - 2 * lam**2 * kappa**2 / (a * m)) / J
    C = kappa * ((2 * lam - 1) - lam * a * m) / (a * J)
    return {
        "a": a,
        "A": A,
        "R": R,
        "m": m,
        "D": D,
        "J": J,
        "C": C,
        "gU": -kappa - R / A + 1 / a,
        "sqrt_eps_gV": 2 * mp.sqrt(kappa) * R / A,
        "eps_gZ0": -lam * kappa / A,
        "Fvv": 4 * lam**2 * kappa * H,
        "Fvz": 2 * lam * mp.sqrt(kappa) * (a / A - 1),
        "Fzz": a**2 / A + lam,
        "Fav": Fav,
        "Faz": Faz,
        "dG_UU_over_L": 1 / a,
        "dG_VV": 2 * m,
        "dG_UV_over_sqrt_eps": 2 * m * lam * mp.sqrt(kappa) / a,
        "v": v,
        "z": z,
    }


def as_str(x, digits=30):
    return mp.nstr(x, digits)


def run_case(eps_str, kappa_str):
    eps = mp.mpf(eps_str)
    kappa = mp.mpf(kappa_str)
    lam = mp.mpf(7) / 10
    s = mp.mpf(2) / 5
    L = mp.log(1 / eps)
    B = basis_for_s(s)
    K = family(eps, kappa, lam, s)
    D = eval_data(K)
    E = expected(lam, kappa)
    c = {name: coords(B[name]) for name in ["U", "T", "Q", "V", "W", "Z0"]}
    h_b = h_coeffs(D["h"], B["P"])
    N_b = transform_N_to_basis(D["N"], B["P"])
    return {
        "eps": eps_str,
        "kappa": kappa_str,
        "min_p": as_str(min(D["p"])),
        "N_basis": {
            "Nww": as_str(N_b[0][0]),
            "Nnn": as_str(N_b[1][1]),
            "Nwn": as_str(N_b[0][1]),
            "Nwe_over_sqrt_eps": as_str(N_b[0][2] / mp.sqrt(eps)),
            "Nne": as_str(N_b[1][2]),
            "Nee_minus_L": as_str(N_b[2][2] - L),
            "detN_over_L": as_str(D["detN"] / L),
            "Z_times_lam_eps2": as_str(D["Z"] * lam * eps**2),
        },
        "g_scaled": {
            "gU": [as_str(dot(D["g"], c["U"])), as_str(E["gU"])],
            "sqrt_eps_gV": [as_str(mp.sqrt(eps) * dot(D["g"], c["V"])), as_str(E["sqrt_eps_gV"])],
            "eps_gZ0": [as_str(eps * dot(D["g"], c["Z0"])), as_str(E["eps_gZ0"])],
        },
        "Fpair_scaled": {
            "Fvv": [as_str(quad(D["Fpair"], c["V"], c["V"])), as_str(E["Fvv"])],
            "Fvz": [as_str(mp.sqrt(eps) * quad(D["Fpair"], c["V"], c["Z0"])), as_str(E["Fvz"])],
            "Fzz": [as_str(eps * quad(D["Fpair"], c["Z0"], c["Z0"])), as_str(E["Fzz"])],
            "Fav": [as_str(quad(D["Fpair"], c["U"], c["V"]) / mp.sqrt(eps)), as_str(E["Fav"])],
            "Faz": [as_str(quad(D["Fpair"], c["U"], c["Z0"])), as_str(E["Faz"])],
        },
        "dG_scaled": {
            "dG_UU_over_L": [as_str(quad(D["dG"], c["U"], c["U"]) / L), as_str(E["dG_UU_over_L"])],
            "dG_VV": [as_str(quad(D["dG"], c["V"], c["V"])), as_str(E["dG_VV"])],
            "dG_UV_over_sqrt_eps": [
                as_str(quad(D["dG"], c["U"], c["V"]) / mp.sqrt(eps)),
                as_str(E["dG_UV_over_sqrt_eps"]),
            ],
        },
        "unused_direction_orders": {
            "gQ": as_str(dot(D["g"], c["Q"])),
            "gT": as_str(dot(D["g"], c["T"])),
            "sqrt_eps_gW": as_str(mp.sqrt(eps) * dot(D["g"], c["W"])),
            "MTT_over_2L": as_str(quad(D["M"], c["T"], c["T"]) / (2 * L)),
            "eps_MQQ_over_lambda": as_str(eps * quad(D["M"], c["Q"], c["Q"]) / lam),
            "MUQ": as_str(quad(D["M"], c["U"], c["Q"])),
            "MUT_over_epsL": as_str(quad(D["M"], c["U"], c["T"]) / (eps * L)),
            "MTV_over_eps32L": as_str(quad(D["M"], c["T"], c["V"]) / (eps ** mp.mpf("1.5") * L)),
            "MTW_over_sqrt_eps": as_str(quad(D["M"], c["T"], c["W"]) / mp.sqrt(eps)),
            "MTZ0_over_epsL": as_str(quad(D["M"], c["T"], c["Z0"]) / (eps * L)),
            "sqrt_eps_MQV_over_L": as_str(mp.sqrt(eps) * quad(D["M"], c["Q"], c["V"]) / L),
            "sqrt_eps_MQW_over_L": as_str(mp.sqrt(eps) * quad(D["M"], c["Q"], c["W"]) / L),
            "MQZ0": as_str(quad(D["M"], c["Q"], c["Z0"])),
            "MWW": as_str(quad(D["M"], c["W"], c["W"])),
            "MUW_over_eps32L": as_str(quad(D["M"], c["U"], c["W"]) / (eps ** mp.mpf("1.5") * L)),
            "sqrt_eps_MZ0W": as_str(mp.sqrt(eps) * quad(D["M"], c["Z0"], c["W"])),
            "hQ_over_eps": as_str(h_b["Q"] / eps),
            "L2_hT": as_str((L**2) * h_b["T"]),
            "L2_hW_over_sqrt_eps": as_str((L**2) * h_b["W"] / mp.sqrt(eps)),
        },
        "h_and_scalars": {
            "L_m_hU": as_str(L * E["m"] * h_b["U"]),
            "L_hV_over_sqrt_eps": [as_str(L * h_b["V"] / mp.sqrt(eps)), as_str(E["v"])],
            "L_hZ0_over_eps": [as_str(L * h_b["Z0"] / eps), as_str(E["z"])],
            "L_g_dot_h": [as_str(L * D["g_dot_h"]), as_str(E["C"])],
            "beta_relation": as_str(D["beta"] * mp.sqrt(D["Z"]) - D["g_dot_h"]),
            "dalpha": as_str(D["dalpha"]),
            "dalpha_minus_model": as_str(D["dalpha"] - (1 - 1 / (lam * L))),
        },
    }


def main():
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    lam = mp.mpf(7) / 10
    kappa_star = (mp.mpf(3) / 7) * (mp.e ** (mp.mpf(40) / 21) - 1)
    result = {
        "status": "NUMERIC_ASYMPTOTIC_SPOT_CHECK_ONLY",
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "kappa_star": as_str(kappa_star, 40),
        "cases": [
            run_case("1e-8", "1"),
            run_case("1e-8", as_str(kappa_star, 50)),
            run_case("1e-8", "10"),
            run_case("1e-10", as_str(kappa_star, 50)),
            run_case("1e-20", as_str(kappa_star, 50)),
        ],
        "note": "This script independently rebuilds the eight atom Jacobian in six K coordinates and checks the displayed leading terms numerically; it is not a formal proof of uniform remainders.",
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "pid": result["pid"], "output": str(out), "kappa_star": result["kappa_star"]}))


if __name__ == "__main__":
    main()
