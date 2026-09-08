# D10-S8b author verdict

STATUS: `CORRECT` for `[-29/100,29/100]`; `INCOMPLETE` at `299/1000`,
the feasibility endpoint, and globally.  A fresh non-author audit is
preserved under `s8b_verifications/`.

S8b successfully expands the continuous full-Hessian negative-definiteness
certificate from

\[
[-6/25,6/25]
\]

to

\[
[-29/100,29/100].
\]

This covers `49/200`, `1/4`, and `7/25`, and reaches within `1/100` of the
first positive spectral degeneration at `t=3/10`.  The endpoint spectral margin
on the certified interval is `1/150`.

The proof method is stronger than the original raw-coordinate Gershgorin gate:
hard leaves are certified after a fixed rational upper-triangular
preconditioner \(P\), proving \(P^\top B(t)P\succ0\) by interval Gershgorin.
Because each stored \(P\) has positive rational diagonal, it is invertible, so
this proves \(B(t)\succ0\).

What is now certified as a proof candidate:

- full observation-coordinate `Sym(3)` directions;
- hence all PSD/NSD directions, including noncommuting directions;
- all `t` in the continuous interval `[-29/100,29/100]`;
- exact-event semantics and rigorous natural-log interval bounds.

What remains open:

- no claim beyond the independently checked interval;
- no proof at `299/1000` or up to the endpoint `3/10`;
- no global dense-Hessian theorem;
- no theorem for arbitrary M8 product-region kernels;
- no one-sided extension toward the negative feasibility endpoint `-1`.

The `299/1000` attempt timed out and is a cost/method blocker, not a
counterexample.  Float scouts near that radius remained negative, so no positive
curvature candidate is currently frozen.

The fresh audit independently reconstructed every rational `B(t)` interval,
every stored preconditioner, and every congruence/Gershgorin check without
importing the S8/S8b author modules.  All 67 leaves matched exactly (65
preconditioned, 2 plain), covered the closed interval without gaps, and had
minimum transformed row margin
`0.000409651436370431053043705705589...`.  Every upper-triangular P has
positive diagonal and is invertible.  The audit explicitly does not interpret
the transformed margin as the same numerical lower bound for raw B; only
positive definiteness is transferred, which is the theorem claimed here.
