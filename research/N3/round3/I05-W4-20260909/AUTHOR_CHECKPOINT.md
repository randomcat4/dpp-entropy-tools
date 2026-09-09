# I05-W4 author checkpoint before round 2

Date: 2026-09-09. This note is the author-side checkpoint. It is distinct from the later independent audit in `review/`.

## Proved by the author in the frozen round-1 submission

For a real symmetric three-point kernel `K`, write `x_i=K_ii`, `v_i=x_i(1-x_i)`. On the domain

```text
0 < x_i < 1,
|K_ij| <= (1/4) sqrt(v_i v_j)  for every i<j,
```

the conditions themselves imply `0<K<I`, and for every real symmetric direction `D`,

```text
-H''(K;D) >= (7/10)(S+U+V) >= 0.
```

Here `S`, `U`, and `V` are the explicit nonnegative quadratic forms defined in the frozen submission. The proof keeps all eight events, the complete Fisher term, all six real `K` coordinates, and the three-point Fisher component. It also proves concavity on the convex domain and its closure, plus negative definiteness when the nonzero-edge graph is connected.

The exact complete author submission is already stored under `payload/` and reconstructed by `build_result_zip.py`. It contains `RESULT.md`, `frozen_statement.md`, `proof.md`, `attempts.md`, `sources.md`, `verification.md`, `HANDOFF.md`, exact inputs, code, and archived outputs.

## Claims reviewed independently after submission

The separate audit in `review/INDEPENDENT_REVIEW.md` accepts the round-1 theorem only within the frozen normalized-interaction subdomain and accepts execution/reproducibility. That audit does not establish novelty, the general real-three-dimensional theorem, an external human peer review, or proof-assistant formalization.

## Claims not proved

The following remain open in this branch:

- full `K`-affine Shannon-entropy concavity for every strict real symmetric `3 x 3` contraction;
- any strict entropy counterexample;
- novelty of the round-1 subdomain theorem.

## Failed proof routes retained as failures, not counterexamples

1. Pointwise nonnegativity of the uniformly shifted logarithmic-integral integrand is false at an explicit rational valid kernel and direction, while the actual entropy curvature there remains negative.
2. Loewner antitonicity of the conditional two-point entropy gradient is false at another explicit rational valid kernel. This does not make the complete conditional-entropy Hessian positive.
3. Separating a global lower bound for the relative density `R` from upper bounds for the conditional log ratios loses the eventwise Fisher/log compensation outside weak coupling.

## Round-2 target

Round 2 keeps the exact eight-event identities and attempts event-adaptive denominators. The primary structural target is a full-six-direction theorem at acyclic real three-point centers (one kernel edge equal to zero), allowing the remaining edge or edges to be arbitrarily strong subject only to `0<K<I`. A second route studies a one-strong-edge tube with weak edges controlled by eventwise conditional slack. Any new statement will be marked author-derived and unreviewed until Codex performs a separate audit.
