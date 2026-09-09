# Reproduction and verification boundary

Status: **AUTHOR EXACT PASS; independent nonauthor review not yet performed.** This is a finite computer-assisted proof certificate combined with the analytic argument in proof.md, not an inference from samples. No CI run, formal proof-assistant check, or novelty review is claimed.

## Complete input and command

The whole certificate input is the literal four-dimensional matrix in `reduced_matrix()` and the six factored integer coefficient polynomials in `residual_polynomial()` in `certificate.py`. There is no downloaded or private data dependency and no need to trust an archived r=0 theorem.

The implementation uses Python 3.11 or later and SymPy 1.14.0. Run from this directory:

```sh
python -m pip install 'sympy==1.14.0'
python certificate.py --out outputs
```

The output directory contains the complete P and Q coefficient arrays and the compact summary. The exact arithmetic stops with an assertion failure on any nonzero determinant residual, wrong degree/count, failed symmetry, nonpositive seed minor, or nonpositive transformed coefficient. No tolerance or numerical rounding is used.

## Actual author run

The complete exact construction, 24-term polynomial determinant, seed, and four integer coefficient transforms completed in a bounded local invocation in 9.053 seconds. The recorded mathematical output was:

```text
P_degrees = [4,4,10,6]
P_nonzero_terms = 279
determinant_coefficient_residual = 0
Q_nonzero_terms = 1731
Q_negative_terms = 0
Q_min_positive = 192
Q_constant = 432
seed_Rbar_leading_minors = [1009/7200,743633/6480000,
                           1137143/12150000,9016/253125]
sympy = 1.14.0
ALL EXACT CERTIFICATE CHECKS PASSED
```

The matrix was rebuilt from the accepted short Schur formula. Its cleared determinant was computed in a rational polynomial ring by enumerating the 24 permutations, not by evaluating a finite set of parameter points. The complete coefficient identity therefore has zero arithmetic error. The binomial chart transform is over exact integers, also with zero arithmetic error. Analytic errors are not excluded merely by exact arithmetic; they remain a subject for independent review.

P was initially suggested by the public full-r factor archived in `research/C2/lambda_zero52/resume/outputs/full/minor_4_factored.txt`. This discovery source was not itself treated as verified. The new zero polynomial residual binds the literal P to the newly reconstructed matrix. In particular neither the old r=0 389-positive coefficient chain nor a floating eigenvalue is a premise of the theorem.

## Finite exploration, excluded from the proof

A bounded double-precision differential-evolution probe of the normalized four-dimensional matrix used seed 22552, population factor 10 and maximum 100 iterations (4040 function evaluations). It approached a degenerate boundary, with an eigenvalue estimate about 8.7e-12; it produced no strict negative candidate. This is SCOUT only, neither a uniform margin nor a global sign certificate. The positive polynomial proof does not depend on that probe.

A first chart on the whole -1<r<1 interval still had 38 negative coefficients after t=u^4. This was a failure of that particular coefficient certificate only. The exact leaf-exchange fundamental domain 0<=r<1, rather than further sampling, produced the successful chart. No processes are left running by these local invocations.

## Frozen dependency and review contract

The starting main was `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`. Its `docs/verification_round3_20260909/accepted_pr51.md` accepts the half-filled theorem and the general arrow identities, not the general arrow inequality. Its `archived_pr55.md` accepts the specified M/Rstar algebra and seed, but explicitly leaves both r=0 and full-r positivity unproved. Those statuses are preserved.

An independent reviewer should verify, in order:

1. The complete-event formula, fixed-u direction map and M=Fmat'+Q; the accepted proofs can be used at their exact scope.
2. The change t=u^4 and Rbar=(u/4)Rstar, including both rank-one Schur subtractions in (16).
3. The determinant identity (17) from the short matrix, independently of the supplied determinant code and old archive.
4. The integer chart transform (19)–(21), its full coefficient array, constant 432 and exact domain coverage through actual leaf exchange.
5. Global nonsingularity before inertia continuation, the positive seed, and integration of the true affine Hessian in a physical direction fixed in u.

The r=0 independent computation was explicitly handed to C2/Codex in issue52, with one process/thread, 16 GiB, no GPU, a shared 2700-second ceiling, exact Rstar→det→P→Q reconstruction, and stop-on-success/discrepancy/deadline. That handoff was REQUESTED, not claimed running. The present all-r author proof was completed without waiting for or assuming its result. Any nonauthor all-r reconstruction must be recorded as a separate review object rather than relabeling this author self-check.

This publication is a checkpoint. Work on the remaining Lambda-nonzero missing-edge Schur inequality continues in the same task and will be appended separately without weakening the quantifiers of Theorems 1–2.
