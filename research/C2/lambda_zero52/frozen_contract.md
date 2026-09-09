# Frozen computation contract

The exact matrices, all variables and the direction map are preserved in `inputs/frozen_issue52.md`. The source assertion is rational and complete; the suggested command name is a new interface to implement, not an existing author script.

## Independent reconstruction gate

Construct all eight exact event probabilities by inclusion determinants and Mobius inversion. Differentiate along an arbitrary physical affine direction with six fixed coordinates. Reconstruct both the complete Fisher and the acceleration/log contribution before differentiating the negative entropy Hessian with respect to the center parameter u. Verify `M = Fmat'(u) + Q` as exact identities, including all signs and factors, the J/L event denominator assignment, and the initial matrix `diag(v,w,4,0,0,0)`.

The marginal Fisher `diag(v,w,0,0,0,0)` remains in the negative entropy Hessian; only its u derivative vanishes. The fixed-in-u direction congruence is invertible throughout the open parameter domain. An alternative congruence applied to the already formed M may be used to study inertia, but differentiating after a moving direction change computes a different object.

## Sign acceptance

- A global positive result needs an exact certificate valid on the entire stated four-parameter open domain, including explicit denominator signs and treatment of limiting faces. Factorization, positive coefficients, Bernstein, SOS or another proof object must carry a reproducible domain argument.
- Inertia continuation requires an exact global determinant nonvanishing certificate plus a positive seed. A positive seed by itself is insufficient.
- A negative result requires rational mu, nu, r, u and a rational six-vector zeta, all strict domain checks, and an exactly negative rational `zeta^T M zeta`. This refutes only radial Hessian monotonicity.
- A claimed entropy counterexample separately needs actual entropy curvature and a genuine full-event positive Jensen interval certificate; it cannot be inferred from negative M.
- A result at r=0 alone is PARTIAL. A timeout, floating non-hit, or local determinant attempt is not evidence for global positivity.

## Single computation budget

The implementation unit alone launches arithmetic. One process, one CPU thread, at most 16 GiB, no GPU. The derive, r=0 and full-r stages share one 2700-second wall ceiling, enforced by the durable runner. There is no automatic second 45-minute allocation. Two other children perform bounded analytic work without arithmetic jobs.

Start with event/identity verification, then r=0 factor/domain arithmetic and finally full r within the remaining budget. Retain positive denominator factors, degrees, completed elimination steps and all failures. A scout, if needed, must first record a fixed finite list of at most 64 rational candidate points and its sampling convention; only exact reconstructed negatives can be accepted. No repetition of the author's previous 1500-point non-hit is required.

Write PID, invocation, environment, stdout/stderr and exit status before computation; save completed objects atomically. Check the owned PID before restart. Do not repeat an elimination merely to recover metadata. Stop at a valid global proof, exact obstruction or the shared ceiling; any extension needs a new publicly recorded plan.

Initial environment: Python 3.12.3 and SymPy 1.14.0 in the existing isolated C2 environment. Resource preflight and absence of prior recorded C2 jobs were checked before claim. No global software or environment changes are part of this task.
