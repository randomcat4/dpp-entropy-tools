# D10-U10i verdict

LIMITING PROBLEM: PROOF CANDIDATE SOLVED, PENDING INDEPENDENT REVIEW.
FULL PATH DOMAIN: INCOMPLETE.
NUMERICAL CHECKS: SCOUT / AUTHOR SANITY ONLY.

The exact proposed exponential limit is

```text
phi(beta)=(beta+log2+2)(beta+log2)^4/[2 beta^2(log2)^2], beta>0.
```

[proof_candidate.md](proof_candidate.md) proves it by identifying the stable
Schur scalar as a constrained energy minimum. Singleton Fisher penalties
force the two diagonal coordinates to zero, the full-atom penalty forces
its derivative to zero, and the remaining weighted-trace constraint fixes
the two offdiagonal coordinates. Uniform coercivity controls the true
minimizer and yields an actual O_J(sqrt x) remainder for every compact
beta interval J contained in (0,infinity).

## What is newly closed

- phi(beta)>0 for EVERY beta>0, with the global lower bound
  phi(beta)>8(log2+2), about 21.5452.
- Both beta endpoints diverge, with explicit leading coefficients.
- The unique minimizing beta is the positive root of
  3beta^2+(log2+4)beta-2log2(log2+2)=0:
  beta_star=0.5802776352924056... and phi_min=26.60376012063093... .
- For each fixed compact beta interval there is a genuine sufficiently
  small-x continuous exponential wedge in which the FULL Sym(3) Hessian is
  strictly negative. This is not merely positivity on the path tangents.

The earlier profile's approximately 26.581 minimum was evaluated at finite
x=1e-4, not at the limit. At beta=.58 the independent stable calculation
reproduces that finite scale and then gives sigma=26.60353703684734... at
x=1e-6, approaching phi(.58)=26.60376358740434... . The closed limit was
derived analytically, not fitted to those values.

## What is still open

The uniform remainder is only for beta in a FIXED compact subset of
(0,infinity). No implication is claimed for all beta=beta(x) tending to
zero or infinity, or for the whole original path domain. The divergence of
phi at its endpoints does not by itself permit exchanging those limits.
Uniform noncompact two-scale control is still needed to combine all other
boundary regimes into a full-domain theorem.

## Evidence and review gate

[sanity.py](sanity.py) uses no imported author gate or profile cache. It
implements a positive-matrix Sherman--Morrison evaluation distinct from the
source's potentially indefinite auxiliary-block implementation.

- 3/3 rational small-dimensional gates independently build Möbius atoms and
  all even Hessian jets, verify exact LDL feasibility, and compare the direct
  Schur value with the new stable form at 180-digit precision.
- 28/28 fixed exponential points check the closed formula, moving minimizers,
  trial upper bound, and convergence. They remain SCOUT.
- One initial runtime type-mixing failure was repaired and fully recorded;
  all final cases pass. No mathematical input was discarded or retuned.

Independent review should inspect constrained normalization, uniform
coercivity and bounded minimizers, the two Fisher forcing estimates, the
constraint determinant, the V-atom factor eight, and the final cofactor
cancellation. The author does not self-label these new results CORRECT.
