# D10-M4 verdict

AUTHOR STATUS: N2_PROVED_N3_BLOCKER_IDENTIFIED, pending non-author verification.

## Result

The \(n=2\) fixed-eigenvector PSD spectral-rate problem is closed on the author
side:

\[
K(t)=Q\operatorname{diag}(\lambda_1+tv_1,\lambda_2+tv_2)Q^T,
\qquad v_i\ge0,
\]

has exact-event entropy curvature

\[
H''(0)<0
\]

for every strict base point \(0<\lambda_i<1\) and every nonzero PSD rate vector
\((v_1,v_2)\ge0\).

Thus dimension two cannot provide a positive local R3 gap in the fixed
eigenvector PSD spectral-rate route.

## n=3 blocker

The \(n=2\) proof uses the fact that the two singleton atom probabilities
satisfy \(p_1''=p_2''=-2v_1v_2\le0\).  In \(n=3\), singleton atom second
derivatives are sign-indefinite.  A rational Householder example gives

\[
p_{\{1\}}''=2339/2450>0.
\]

This is only a proof-method blocker, not a positive entropy-curvature
candidate.

## Evidence

- `theorem.md`: self-contained \(n=2\) proof.
- `n3_blocker.md`: exact rational obstruction for lifting the proof.
- `n2_exact_check.py`: exact-event sanity script.
- `n2_probe.py`: finite scout, retained as non-proof evidence.

No server scan or shared README was used.  Finite probes are not promoted to
theorems.

## Status

`N2_PROVED_N3_BLOCKER_IDENTIFIED`
