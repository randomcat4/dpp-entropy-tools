# D10-M5 author verdict

STATUS: **INCOMPLETE_SCOUT_NO_HIT**

No strict positive \(H''\) or \(\rho>1\) candidate was found for \(n=3\)
fixed-eigenvector PSD spectral-rate directions.  No candidate is frozen.

## What was reduced

For \(P=q^2\), exact atoms are

\[
p_\varnothing=\prod_i(1-\theta_i),\quad
p_{\{1,2,3\}}=\prod_i\theta_i,\quad
p_{\{a\}}=(Pr)_a,\quad
p_{\{1,2,3\}\setminus\{a\}}=(Ps)_a.
\]

Thus

\[
H(Y_t)=H(|Y_t|)+G_P(r(t))+G_P(s(t)).
\]

The count term is concave by Shepp--Olkin.  The unresolved target is the
conditional term \(G_P(r(t))+G_P(s(t))\).

## What blocked a proof

The raw singleton weights are not componentwise concave.  An exact example is

\[
\theta=(3/5,1/5,1/5),\quad v=(1/100,1/10,1/10),
\]

for which

\[
r''=(11/1250,-23/2500,-23/2500).
\]

The positive first entry blocks the most natural perspective-composition proof.
Search also found positive singleton and pair conditional curvature separately,
but no positive sum.

## Run record

`n3_psd_search.py` ran with exit code `0`, seed `2026090835`.

Denominator:

- `180000` random n=3 PSD spectral directions;
- `22000` local perturbation proposals;
- `202000` total evaluated directions;
- `8` exact atoms per direction.

Best total \(H''\): `-1.3335172052461775`.
Best observed \(\Psi''\): `-4.754838300868869e-09`.
Positive candidates: `0`.

## Bottom line

The n=3 route remains open.  The evidence points to a possible singleton/pair
cancellation theorem, but this work unit did not prove it.  Finite non-hit is
recorded only as SCOUT.
