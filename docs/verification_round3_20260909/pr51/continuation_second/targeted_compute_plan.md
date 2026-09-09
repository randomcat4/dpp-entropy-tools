# Targeted exact check plan

Purpose: independently check only the auxiliary conditional-resolvent obstruction in `continuation.md:254-298`, especially the sign of `Phi''(K_*;D_*)` and strict legality of the displayed center.

Non-goals:

- Do not reconstruct or eliminate the issue #52 multivariate matrix `M`.
- Do not import author code or private Drive material.
- Do not rerun the author's verifier.
- Do not check global entropy concavity or the original half-filled theorem.

Resource ceiling:

- One local process.
- One thread.
- No GPU.
- Target memory below 4 GiB.
- Stop after at most 15 minutes.

Method:

Use a short independent exact-rational script with integer fractions. Compute the first three Taylor coefficients at `t=0` for the four two-bit marginals `P_ij(K+tD)` and the four atoms `p_ij1(K+tD)`, then apply

\[
(P^2/R)''=2(P'-PR'/R)^2/R+2PP''/R-P^2R''/R^2.
\]

Also check the Schur-complement inequalities for `K_*` and `I-K_*` directly in rational arithmetic.

Acceptance:

The check supports only the method-obstruction sign if it reproduces a negative exact rational for `Phi''` and confirms strict legality. Any failure is reported as a review gap rather than patched in author files.
