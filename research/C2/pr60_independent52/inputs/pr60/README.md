# I05-22 R3 — final scoped author packet

This is the completed author packet for the current task, not a claim that general real three-point concavity is settled. It was created on a new branch from main `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`. Accepted PR51 and archived PR55 retain their exact main-side scopes. The r=0 389-positive-coefficient candidate is not a premise of any new theorem below.

## Verdict by precise claim

**PROVED — author complete computer-assisted proof, NOT independently reviewed.** For every `|mu|,|nu|,|r|<1, 0<u<1`, the full fixed-physical-direction M in issue52 is positive definite. Therefore every connected strict real missing-edge Lambda-zero center, with arbitrary unequal diagonal parameters and arbitrary nonzero edge ratio, has strictly negative complete-configuration entropy Hessian in all six real symmetric directions. `proof.md` supplies the exact domain, events, matrix, determinant, chart, seed and integration.

The new core is t=u^4 plus actual leaf-exchange symmetry, not a larger weak-coupling constant. The complete short-matrix determinant identity was reconstructed exactly. Its residual P has 279 monomials; on the symmetry fundamental domain the cleared Q has 1731 positive integer coefficients and positive constant432. Global nonvanishing is established before inertia continuation. Neither floating non-hits nor positivity of a saved r=0 polynomial is used as a global theorem.

**PROVED — author proof, NOT independently reviewed.** The same entire Lambda-zero family has full-six-direction strict concavity of H(X3|X1,X2). The explicit center-dependent radius in `continuation.md` (25) gives a genuine nonzero-Lambda band with a uniform-in-direction curvature bound for each fixed center. Its radius may vanish toward degeneracies; no global positive safety margin is asserted.

**DISPROVED — author exact certificate, NOT an entropy counterexample.** A direct extension that freezes all three diagonal entries and radially scales the two existing edges need not have positive derivative of the full negative Hessian. The exact K*,D*,C* in `continuation.md` (30) give Mtilde(D*,D*) in [-0.01912227459137764707182987490765265,-0.01912227459137764707182987490765264]. The same true entropy curvature is negative, and the strict legal three-kernel Jensen difference is negative. This does not refute the Lambda-zero theorem or DPP entropy concavity.

**INCOMPLETE.** The general Lambda-nonzero missing-edge Sfull inequality outside the explicit band, and the general real three-point theorem, remain open in this packet. A new exact one-sided perspective/scale reduction is provided in `continuation.md` (37)–(39), but its remaining coupled Fisher–cofactor inequality is not claimed proved. No positive-Jensen counterexample is certified.

Novelty and publication priority are not assessed. All verification here is author same-session work, not an independent review, CI result or formal proof-assistant certificate.

## Complete proof and code map

- `proof.md`: complete main theorem and its finite positive-chart certificate.
- `continuation.md`: work performed after the first PR checkpoint: conditional strictness, quantified Lambda-nonzero band, exact failure of a stronger radial method, and the one-sided scale bridge.
- `sources_routes.md`: primary literature with precise bridges and assumptions, two different routes, old and new failures, and the initial remaining target.
- `verification.md`: frozen main inputs, original exact run, limits of discovery probes and nonauthor review contract.
- `certificate.py`: full polynomial/matrix input, coefficient-level determinant identity, positive chart and seed; emits complete P/Q arrays.
- `bridge_checks.py`: exact score Gram reconstruction, all mixed direction couplings, the positive two-dimensional block and normalization from Rstar to Rbar.
- `continuation_exact.py`: independently reconstructs all eight two-parameter event polynomials for the method obstruction, all first/second/mixed third jets, legality, true curvature and the Jensen log-error certificate.

Use Python 3.11+ and SymPy1.14.0:

```sh
python -m pip install 'sympy==1.14.0'
python bridge_checks.py
python certificate.py --out outputs
python continuation_exact.py --out outputs
```

All three commands were actually run locally and completed with their exact PASS lines. In order, the mathematical terminal results are:

```text
ALL SCORE, FIXED-DIRECTION SCHUR AND NORMALIZATION IDENTITIES PASSED
ALL EXACT CERTIFICATE CHECKS PASSED
ALL POST-CHECKPOINT EXACT CHECKS PASSED
```

The first two use integer/rational symbolic identities with zero rounding error. The last uses rational atanh-series log enclosures with the explicit tail in continuation.md (34), then outward decimal rounding. Complete coefficients, atom jets and exact Sylvester minors are emitted by the commands. No private files, credentials, hidden search inputs or uploaded Drive objects are required.

The initial polynomial coefficient proposal came from the public archived full-r determinant. It became an author proof input only after the complete new matrix-to-polynomial residual was verified zero. The r=0 independent reconstruction was separately requested from C2 in issue52; no result or running job is assumed. Routine completion and review requests are recorded in PR60 and issue52. Uploading the first proof was followed by the additional mathematics listed above, not by waiting for a coordinator response.
