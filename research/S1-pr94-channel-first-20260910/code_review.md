# Static code and evidence review

Frozen PR94 commit: `a9db9f98dc6dac766dd9b214f056ee9b30109b23`.

Reviewed statically: `code/exact_core.py`, `code/fixtures.py`, `code/verify_channels.py`, and the channel output artifacts. No program was executed.

**STATIC STATUS: NO CRITICAL CODE-LOGIC DEFECT FOUND.**

The final checker:

- constructs the selector refinement exactly and checks its fixed weights and legal affine parameters;
- compares the full moving-diagonal Shannon Hessian through rational Fisher terms and exact prime-log coefficients, rather than through finite differences;
- checks all 16 refined joint-law polynomials;
- checks all 64 observed complete-event polynomials for both half-filled and asymmetric mode backgrounds;
- preserves the explicit failure of uniform complement pairing away from half filling;
- verifies the displayed Schur endpoint polynomials, negative-fiber construction, curvature coefficient, and nonproportional PR58 frame minors;
- limits numerical libraries to one thread and labels all output as author evidence.

The two development stops are retained and consistent with the final changes: `Poly.diff(2)` was replaced by two derivative calls, and the asymmetric background was changed after an internal-edge nonzero assertion correctly failed. Neither stop changes a theorem hypothesis or the original PR58 input.

Unlike the PR95 exact checker, this script uses Python `assert`; its own README correctly forbids `python -O`. The recorded exit-zero run and JSON remain author-side artifacts. This review does not make them an independent implementation or arithmetic certificate.
