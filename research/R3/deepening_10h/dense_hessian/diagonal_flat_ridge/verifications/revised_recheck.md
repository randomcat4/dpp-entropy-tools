# D10-U2 revised Taylor-display recheck

STATUS: PASS

I performed only the requested narrow recheck.  I did not rerun the full Fraction audit.

Checked file:

- `research/R3/deepening_10h/dense_hessian/diagonal_flat_ridge/proof.md`

New proof SHA-256:

- `e3bc5a365a56801fdd192e909656b4b8167b77c773eee24e516f081a3a3c5e22`

Result:

- `proof.md:234-239` now explicitly displays the intended additive Taylor expansion:
  \[
  h(a_S+\Delta)
  =
  h(a_S)
  +(-\log a_S-1)\Delta
  -\frac{\Delta^2}{2a_S}
  +O(\Delta^3).
  \]
- The downstream entropy expansion and constants remain in the same checked structure:
  - `proof.md:242-251` still gives the intended \(H(t)-H(0)\) expansion with the \(-q_S^2/(8a_S)t^4\) term.
  - `proof.md:264-281` still gives the total/singleton log-linear cancellation and \(H^{(4)}(0)=-3\sum_S q_S^2/a_S\).

Conclusion: the sole nonfatal display issue identified in `fresh_audit.md` has been locally repaired.  The prior `STATUS: CORRECT` verdict remains unchanged.
