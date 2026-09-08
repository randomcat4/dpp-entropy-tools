# D10-M5 fresh non-author audit: n=3 fixed-\(Q\) PSD spectral target

Verification status for the author materials: **CORRECT**

Layered mathematical verdict:

- exact \(n=3\) layer reduction: **CORRECT**;
- \(r''\) blocker arithmetic: **CORRECT**;
- search ledger/reporting for `202000` evaluated PSD spectral directions:
  **CORRECT AS SCOUT**;
- universal \(n=3\) fixed-\(Q\) PSD spectral concavity theorem:
  **INCOMPLETE**.

The author correctly labels the work as `INCOMPLETE / SCOUT`; this audit does
not promote the finite non-hit to a theorem.

## Scope

Author files read in `n3_targeted/`:

- `frozen_problem.md`
- `derivation_and_blocker.md`
- `hazards.md`
- `search_report.md`
- `verdict.md`
- `n3_psd_search.py`
- `n3_search_results.json`

New verification files:

- `verifications/fresh_recompute.py`
- `verifications/fresh_recompute_results.json`

No author file and no main README was modified.  I did not run the author
search script, because it writes `n3_search_results.json` beside the author
files.  Instead I used an independent script to check exact identities and to
recompute the reported records from the author JSON.

## 1. Exact atom layer reduction

The author reduction
\[
H(Y_t)=H(|Y_t|)+G_P(r(t))+G_P(s(t))
\]
is correct for \(n=3\).

Let \(P_{ai}=q_{ai}^2\).  The spectral-channel formula gives:

\[
p_\varnothing=\prod_i(1-\theta_i),\qquad
p_{\{1,2,3\}}=\prod_i\theta_i .
\]

For singleton atoms,
\[
p_{\{a\}}=\sum_i q_{ai}^2\theta_i\prod_{j\ne i}(1-\theta_j)=(Pr)_a,
\]
where
\[
r_i=\theta_i\prod_{j\ne i}(1-\theta_j).
\]

For pair atoms, write the observed pair as the complement of row \(a\), and
the latent spectral pair as the complement of column \(i\).  In dimension
three,
\[
\det(Q_{\bar a,\bar i})=\pm\det(Q)q_{ai},
\]
so after squaring
\[
\det(Q_{\bar a,\bar i})^2=q_{ai}^2.
\]
Thus
\[
p_{\{1,2,3\}\setminus\{a\}}=(Ps)_a,\qquad
s_i=(1-\theta_i)\prod_{j\ne i}\theta_j.
\]

Since \(P\) is doubly stochastic,
\[
\sum_a(Pr)_a=\sum_i r_i,\qquad \sum_a(Ps)_a=\sum_i s_i.
\]
Therefore the singleton and pair contributions split as conditional layer
entropies:
\[
G_P(x)=-\sum_a(Px)_a\log\frac{(Px)_a}{\sum_i x_i},
\]
and hence
\[
H(Y_t)=H(|Y_t|)+G_P(r(t))+G_P(s(t)).
\]

Independent exact check: with rational Householder
\[
Q=I-\frac{1}{7}(1,2,3)(1,2,3)^\top
\]
and \(\theta=(2/7,3/5,5/11)\), `fresh_recompute.py` compared all eight atoms
from:

1. the reduced \(n=3\) formula above;
2. the full spectral-channel mixture;
3. the signed determinant exact-event formula.

Results:

- sum of atoms: `1`;
- minimum atom: `6/77`;
- max reduced-vs-full-channel difference: `0`;
- max reduced-vs-signed-atom difference: `0`.

This confirms exact-event semantics, not just inclusion-probability semantics.

## 2. \(G_P\) second derivative and sign-indefinite acceleration

For \(y=Px\) and \(\pi=\sum_i x_i\),
\[
G_P(x)=-\sum_a y_a\log(y_a/\pi)
      =-\sum_a y_a\log y_a+\pi\log\pi .
\]
Differentiating along \(x(t)\) gives
\[
\frac{d^2}{dt^2}G_P(x(t))
=-\sum_a\frac{(y'_a)^2}{y_a}
 +\frac{(\pi')^2}{\pi}
 -\sum_a y''_a\log\frac{y_a}{\pi}.
\]
The first two terms are nonpositive by Cauchy--Schwarz.  The last term is the
real blocker: it depends on the channel acceleration \(y''=Px''\) and has no
fixed sign.

The raw derivatives in the author file are correct:
\[
r_i''=
2\left[
\theta_i v_jv_k
-v_iv_j(1-\theta_k)
-v_iv_k(1-\theta_j)
\right],
\]
\[
s_i''=
2\left[
(1-\theta_i)v_jv_k
-v_iv_j\theta_k
-v_iv_k\theta_j
\right].
\]

## 3. Rational \(r''\) blocker

For the author blocker
\[
\theta=(3/5,1/5,1/5),\qquad
v=(1/100,1/10,1/10),
\]
independent Fraction arithmetic gives
\[
r''=(11/1250,-23/2500,-23/2500).
\]
So \(r_1''>0\) despite \(v_i\ge0\).  This correctly invalidates the tempting
proof strategy “prove \(r\) and \(s\) componentwise concave, then compose with
an increasing concave perspective entropy.”

The same exact calculation also gives
\[
s''=(9/1250,-27/2500,-27/2500),
\]
showing that pair raw weights are also not componentwise concave in general.
This supports, but does not prove, the need for singleton/pair cancellation.

## 4. Search denominator and no-hit ledger

The author script and result ledger agree on the denominator:

- seed: `2026090835`;
- random PSD spectral directions requested/completed: `180000 / 180000`;
- local perturbation proposals requested/completed: `22000 / 22000`;
- total completed proposals: `202000`;
- local accepted moves: `1590`;
- positive candidates recorded: `0`;
- result status: `SCOUT_NO_POSITIVE_FOUND`.

The positive-candidate threshold in the author script is \(H''>10^{-10}\), but
the script also tracks the best \(H''\) over all evaluated proposals.  Since
the recorded best total \(H''\) is negative, there is no evidence of a hidden
small positive \(0<H''\le10^{-10}\) proposal in the logged run.

I found no event-semantics mismatch in the search implementation: its eight
probabilities are exact configuration atoms ordered as empty, singleton layer,
pair layer, full, using the \(n=3\) spectral-channel reduction above.

## 5. Recomputed reported extrema

The independent script recomputed the four reported records from
`n3_search_results.json` without importing author code.  Discrepancies are at
ordinary floating roundoff scale.

Best total curvature record:

- label: `local_probe_21948`;
- recomputed \(H''\): `-1.3335172052461775`;
- recomputed count contribution: `-1.3334536000849802`;
- recomputed \(\Psi''\): `-6.360516119729986e-05`;
- recomputed minimum atom: `0.12303319954517386`;
- spectral \(v_i\ge0\): yes;
- orthogonality / \(P\)-row / \(P\)-column max errors: about `4e-15`;
- chord midpoint gap: `-6.66758648293353e-09`;
- central second difference: `-1.333517296586706`.

Best conditional \(\Psi''\) record:

- label: `random_104585`;
- recomputed \(\Psi''\): `-4.754838300868869e-09`;
- \(H''\): `-9998.088375350324`;
- this is still negative and occurs near the spectral boundary, so it is a
  scout datum only.

Layerwise positive conditional curvature was also confirmed:

- max singleton conditional \(G_P(r)''\):
  `3.6342121993267824`;
  at that point the pair layer was `-1581.138293130891`, so total
  \(\Psi''=-1577.5040809315642\);
- max pair conditional \(G_P(s)''\):
  `3.0505478033779925`;
  at that point the singleton layer was `-4968.276571221124`, so total
  \(\Psi''=-4965.226023417746\).

Thus the author statement “singleton/pair layers can each curve upward, but no
positive sum was found” is reproducible from the ledger and independent
recalculation.

## 6. Search limitations

The finite search remains only SCOUT:

- it does not prove \(n=3\) fixed-\(Q\) PSD spectral concavity;
- it does not certify a general singleton/pair cancellation theorem;
- it does not produce or freeze any positive \(H''\), \(\rho>1\), or chord-gap
  candidate.

The script has no analytic coverage guarantee over \(Q,\theta,v\).  The author
correctly states this limitation in `frozen_problem.md`, `hazards.md`,
`search_report.md`, and `verdict.md`.

## Command

Independent verification run:

```text
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_targeted/verifications/fresh_recompute.py'
```

Exit code: `0`.

## Final layered verdict

- **CORRECT:** exact atom layer reduction
  \(H=H(\mathrm{count})+G_P(r)+G_P(s)\).
- **CORRECT:** rational \(r''\) blocker arithmetic and the conclusion that
  componentwise layer concavity cannot be the proof.
- **CORRECT AS SCOUT:** `202000` proposal ledger, no positive candidate record,
  best \(H''\), best \(\Psi''\), and positive singleton/pair layer extrema.
- **INCOMPLETE:** the universal \(n=3\) fixed-\(Q\) PSD spectral concavity
  question remains unproved.
