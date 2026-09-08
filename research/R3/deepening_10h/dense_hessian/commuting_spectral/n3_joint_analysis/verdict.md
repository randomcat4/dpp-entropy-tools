# D10-M6 author verdict

STATUS: **INCOMPLETE_SCOUT_NO_HIT_AFTER_REPAIR**

The n=3 fixed-\(Q\), one-sign spectral-rate route remains open.  I did not find
a strict positive \(H''\) candidate, and I did not prove global nonpositivity.

## What was added

- A joint singleton/pair reduction preserving the exact-event semantics:
  \(H(Y)=H(|Y|)+G_P(r)+G_P(s)\).
- A fixed-base Hessian cone reduction:
  for every fixed \((\theta,Q)\), one-sign spectral concavity is equivalent to
  copositivity of \(-M(\theta,Q)\), where
  \(H''=v^\top M(\theta,Q)v\).
- A repaired positive-simplex scan with singular KKT regression.  The original
  `joint_probe_results.json` is deprecated scout data only.
- A positive-orthant sphere scan that enumerates all support principal
  eigenvector candidates, as suggested by the parent instance.
- A clarification that \(\Psi''\le0\) is a stronger sufficient condition and is
  now false; only the total count-barrier inequality remains open.

## Evidence

`joint_copositive_probe.py` v3 exited with code `0`.

- result file: `joint_probe_results_v3.json`;
- script SHA256:
  `6d275dc10ffa5466f7ead81277fd622c64378f5e020eeb3dd8345aec3a085b9a`;
- base points checked: `60384`;
- sphere positive-gate candidates inside the run: `416691`;
- positive total candidates: `0`;
- best positive-simplex total value: `-1.333333333333333`;
- best sampled conditional value: `0.0006515928675194109`, still below the
  count barrier;
- singular verifier matrix regression value: approximately `0` for both
  simplex and sphere gates;
- \(10^{14}\)-scaled positive matrix regression: simplex
  `66666666666666.68` versus expected `66666666666666.664`, sphere
  `200000000000000.0` versus expected `200000000000000.0`;
- direct Möbius/channel atom sanity max error: `1.3877787807814457e-16`.

`sphere_support_probe.py` exited with code `0`.

- base points checked: `83456`;
- support eigenvector candidates evaluated: `574547`;
- positive total candidates: `0`;
- best positive-sphere total value: `-1.3375999999999997`;
- best \(\Psi''/(-H(|Y|)'')\): `-8.541913678890443e-08`.

## Most load-bearing remaining step

The unresolved step is an analytic proof that the paired acceleration term

\[
-\langle P r'',\log(Pr/\pi_1)\rangle
-\langle P s'',\log(Ps/\pi_2)\rangle
\]

is always dominated by the negative Fisher pieces and the count barrier, for
every strict \(\theta\) and every orthostochastic \(P=q^2\).

Equivalently, one can try to prove the 3x3 copositivity inequalities for
\(-M(\theta,Q)\) over the full continuous orthostochastic domain.  The finite
scans make this target look plausible, but they do not certify it.  Conditional
layer concavity by itself is no longer a viable target.
