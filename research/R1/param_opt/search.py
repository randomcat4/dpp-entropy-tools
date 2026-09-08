"""Bounded real-interior DPP Hessian search; numerical candidates only."""
import os
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[name] = "1"
import argparse
import json
import math
import platform
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.special import expit


def basis(n):
    i, j = np.triu_indices(n)
    c = np.where(i == j, 0.5, 1 / math.sqrt(2))
    e = np.zeros((len(i), n, n))
    for a, (r, s) in enumerate(zip(i, j)):
        e[a, r, s] += c[a]
        e[a, s, r] += c[a]
    return i, j, c, e


def exact_events(k):
    """Full event probabilities via signed det(K-diag(1_{S^c}))."""
    n = len(k)
    absent = 1 - ((np.arange(2**n)[:, None] >> np.arange(n)) & 1)
    a = np.broadcast_to(k, (2**n, n, n)).copy()
    a[:, np.arange(n), np.arange(n)] -= absent
    sign, lp = np.linalg.slogdet(a)
    p = np.exp(lp) * sign * (-1.0) ** absent.sum(axis=1)
    if np.min(p) <= 0 or abs(p.sum() - 1) > 1e-9:
        raise FloatingPointError(f"invalid event probabilities: {p.min()}, {p.sum()}")
    return p, a


def entropy(k):
    p, _ = exact_events(k)
    return -np.dot(p, np.log(p))


def mobius_events(k):
    n = len(k)
    p = np.ones(2**n)
    for s in range(1, 2**n):
        idx = [j for j in range(n) if s >> j & 1]
        p[s] = np.linalg.det(k[np.ix_(idx, idx)])
    for j in range(n):
        for s in range(2**n):
            if not (s >> j & 1):
                p[s] -= p[s | 1 << j]
    return p


def hessian(k):
    n = len(k)
    i, j, c, e = basis(n)
    p, a = exact_events(k)
    ai = np.linalg.inv(a)
    lp = np.log(p)
    g = 2 * ai[:, i, j] * c
    # tr(A^-1 E_a A^-1 E_b), with E_a = c_a(e_i e_j^T+e_j e_i^T).
    t = 2 * c[None, :, None] * c[None, None, :] * (
        ai[:, j[:, None], i[None, :]] * ai[:, i[:, None], j[None, :]]
        + ai[:, j[:, None], j[None, :]] * ai[:, i[:, None], i[None, :]])
    h = -np.einsum("s,sa,sb->ab", p * (1 + lp), g, g) + np.einsum("s,sab->ab", p * lp, t)
    # Sum p'' must vanish; kept as an explicit numerical diagnostic.
    mass_second = np.einsum("s,sa,sb->ab", p, g, g) - np.einsum("s,sab->ab", p, t)
    return (h + h.T) / 2, float(np.max(np.abs(mass_second))), float(p.min()), e


def kernel(raw, margin):
    w, q = np.linalg.eigh((raw + raw.T) / 2)
    return (q * (margin + (1 - 2 * margin) * expit(w))) @ q.T


def evaluate(raw, margin):
    k = kernel(raw, margin)
    h, residual, pmin, e = hessian(k)
    w, q = np.linalg.eigh(h)
    v = np.einsum("a,aij->ij", q[:, -1], e)
    return float(w[-1]), k, v, residual, pmin


def selftest():
    rng = np.random.default_rng(80191)
    records = []
    for n in range(1, 7):
        raw = rng.normal(size=(n, n))
        k = kernel(raw, 0.08)
        p, _ = exact_events(k)
        h, residual, _, e = hessian(k)
        coeff = rng.normal(size=len(e)); coeff /= np.linalg.norm(coeff)
        v = np.einsum("a,aij->ij", coeff, e)
        analytic = coeff @ h @ coeff
        steps = [1e-3, 3e-4, 1e-4]
        fd = [(entropy(k+t*v)-2*entropy(k)+entropy(k-t*v))/t**2 for t in steps]
        err = float(np.max(abs(p-mobius_events(k))))
        assert err < 1e-12, (n, err)
        assert residual < 1e-10, (n, residual)
        assert min(abs(x-analytic) for x in fd) < 2e-5, (n, analytic, fd)
        records.append(dict(n=n, probability_abs_error=err, mass_second_residual=residual,
                            analytic=float(analytic), steps=steps, finite_difference=fd))
    # Diagonal independent Bernoulli law: diagonal coordinate second derivatives.
    k = np.diag([0.2, 0.45, 0.7])
    h, _, _, e = hessian(k)
    for a in range(len(e)):
        if np.count_nonzero(e[a]) == 1:
            j = np.flatnonzero(e[a].diagonal())[0]
            assert abs(h[a,a] + 1/(k[j,j]*(1-k[j,j]))) < 1e-12
    return dict(status="PASS", cases=records, numpy=np.__version__, scipy=scipy.__version__,
                python=platform.python_version(), threads=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=202609081)
    ap.add_argument("--samples", type=int, default=20)
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--seconds", type=int, default=900)
    ap.add_argument("--selftest-only", action="store_true")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    if (out / "summary.json").exists():
        raise RuntimeError("Completed output exists; refuse duplicate job")
    test = selftest()
    (out / "selftest.json").write_text(json.dumps(test, indent=2))
    if args.selftest_only:
        print(json.dumps(test), flush=True); return
    start = time.time()
    rng = np.random.default_rng(args.seed)
    total = failed = positive = 0
    best = None
    logpath = out / "evaluations.jsonl"
    checkpoint = out / "checkpoint.json"
    done = set()
    if checkpoint.exists():
        saved = json.loads(checkpoint.read_text())
        if saved["args"] != vars(args):
            raise RuntimeError("Resume arguments mismatch")
        rng.bit_generator.state = saved["rng_state"]
        done = set(tuple(x) for x in saved["done"])
        total, failed, positive, best = [saved[x] for x in ("total", "failed", "positive", "best")]
    with logpath.open("a", buffering=1) as log:
        for n in range(args.nmin, args.nmax + 1):
            for sample in range(args.samples):
                if (n, sample) in done:
                    continue
                if time.time() - start > args.seconds:
                    break
                # Four spectral scales, always full-dimensional symmetric coordinates.
                scale = (0.5, 1.5, 3.0, 6.0)[sample % 4]
                margin = (0.02, 0.005, 0.001)[sample % 3]
                raw = rng.normal(size=(n,n)) * scale / np.sqrt(n)
                raw = (raw + raw.T) / 2
                # Full-dimensional stochastic ascent, keeping restart path auditable.
                current = -float("inf")
                for step in range(args.steps + 1):
                    trial = raw if step == 0 else raw + rng.normal(size=(n,n)) * scale * (0.4 if step % 3 else 0.1) / np.sqrt(n)
                    trial = (trial + trial.T) / 2
                    total += 1
                    rec = dict(n=n, sample=sample, step=step, seed=args.seed, margin=margin, scale=scale)
                    try:
                        value,k,v,residual,pmin = evaluate(trial, margin)
                        rec.update(max_hessian=value, mass_second_residual=residual, probability_min=pmin)
                        if not np.isfinite(value) or residual > 1e-7:
                            raise FloatingPointError("Hessian diagnostic failed")
                        if value > current:
                            raw = trial; current = value
                            rec["accepted"] = True
                        if best is None or value > best["value"]:
                            eig = np.linalg.eigvalsh(k)
                            chord_t = 0.05 * min(eig[0], 1-eig[-1]) / np.linalg.norm(v, 2)
                            delta = (entropy(k-chord_t*v)+entropy(k+chord_t*v))/2 - entropy(k)
                            best = dict(value=value, K=k.tolist(), V=v.tolist(), raw=trial.tolist(),
                                        t=chord_t, delta=delta, record=rec, eigenvalues=eig.tolist())
                            (out / "best.json").write_text(json.dumps(best, indent=2))
                        if value > 1e-6:
                            positive += 1
                            (out / f"candidate_{total:08d}.json").write_text(json.dumps(dict(K=k.tolist(),V=v.tolist(),record=rec),indent=2))
                    except (ValueError, np.linalg.LinAlgError, FloatingPointError) as exc:
                        failed += 1; rec["failure"] = str(exc)
                    log.write(json.dumps(rec) + "\n")
                done.add((n,sample))
                checkpoint.write_text(json.dumps(dict(args=vars(args),rng_state=rng.bit_generator.state,
                    done=sorted(done),total=total,failed=failed,positive=positive,best=best)))
                print(json.dumps(dict(n=n,sample=sample,total=total,failed=failed,best=best["value"] if best else None)),flush=True)
    summary = dict(status="DISPROVED_CANDIDATE" if positive else "INCOMPLETE",args=vars(args),total=total,
                   failed=failed,positive_threshold=1e-6,positive=positive,completed_restarts=len(done),
                   requested_restarts=args.samples*(args.nmax-args.nmin+1),elapsed_seconds=time.time()-start,
                   exit_code=0,best=best,limitations="Finite numerical search only; no general theorem or certification.")
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k:v for k,v in summary.items() if k != "best"}),flush=True)


if __name__ == "__main__":
    main()
