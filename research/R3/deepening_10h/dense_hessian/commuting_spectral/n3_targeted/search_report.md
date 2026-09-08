# D10-M5 n=3 targeted search report

Status: **SCOUT_NO_POSITIVE_FOUND**.

Script: `n3_psd_search.py`

Run from
`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_targeted/n3_psd_search.py
```

Exit code: `0`.  Seed: `2026090835`.  Runtime: `30.94173526763916` seconds.
No server, GPU, or external dependency was used.

## Denominators

- Random orthogonal \(Q\), strict \(\theta\), PSD spectral \(v\) draws:
  `180000`.
- Local PSD spectral perturbation proposals around the best draw:
  `22000`.
- Total evaluated n=3 PSD spectral directions: `202000`.
- Events per evaluation: `8` exact atoms via the n=3 spectral-channel formula.
- Positive candidates with \(H''>0\): `0`.

## Best total-curvature scout

The best observed total \(H''\) was still negative:

\[
H''=-1.3335172052461775.
\]

At that point:

- count contribution: `-1.3334536000849802`;
- conditional contribution \(\Psi''\): `-6.360516119729986e-05`;
- Fisher-positive term: `1.3335172052461854`;
- acceleration term: `7.852277745658742e-15`;
- \(\rho\): `5.88839627622885e-15`;
- minimum exact atom: `0.12303319954517386`.

The strict spectral chord gate used \(h=10^{-4}\) and gave midpoint gap
`-6.66758648293353e-09`, central second difference
`-1.333517296586706`.

## Conditional-layer extrema

The search found that individual conditional layers can curve upward:

- maximum singleton conditional \(G_P(r)''\): `3.6342121993267824`;
- maximum pair conditional \(G_P(s)''\): `3.0505478033779925`.

But in the recorded extrema, the opposite layer was strongly negative:

- at the max singleton point, pair conditional contribution was
  `-1581.138293130891`, total \(\Psi''=-1577.5040809315642\);
- at the max pair point, singleton conditional contribution was
  `-4968.276571221124`, total \(\Psi''=-4965.226023417746\).

The best observed total conditional contribution was still slightly negative:

\[
\max \Psi'' \approx -4.754838300868869\times10^{-9}.
\]

This suggests, but does not prove, a singleton/pair cancellation mechanism.

## Raw blocker

The script records the exact-pattern singleton blocker
\[
\theta=(3/5,1/5,1/5),\qquad v=(1/100,1/10,1/10),
\]
with
\[
r''=(11/1250,-23/2500,-23/2500).
\]

The first entry is positive despite \(v\ge0\).  This is why a direct
componentwise-concavity proof cannot close n=3.

Full numerical output is in `n3_search_results.json`.
