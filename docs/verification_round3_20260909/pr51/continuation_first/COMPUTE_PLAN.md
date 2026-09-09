# PR51 continuation compute plan

This plan is frozen before any arithmetic execution.

Primary method: analytic review of `continuation.md`, with small exact checks only where they do not overlap issue52's heavy determinant/global certificate task.

Inputs:

- public `research/I05-22-missing-edge-20260909/continuation.md`;
- no private Drive scripts named `verify_exact.py` or `verify_general.py`;
- no old PR41/43 proof used as a black box.

Permitted exact checks:

1. Re-derive the product-domain equivalence through Schur complements and the conditional probabilities `t_ij`.
2. Re-derive the physical-direction inverse map (22) from the conditional derivative basis (21).
3. Check log identities, `Lambda=0` equivalence, and the trapezoid inequalities behind positive definiteness of `L`.
4. Check the displayed `L,C,R` log-acceleration identity by symbolic collection, without attempting global positivity of the remaining Schur complement.
5. Check the face-acceleration identity (31) by exact expansion.
6. Check the two method-obstruction examples: the conditional-resolvent `Phi''` rational value, legality/log-error signs for the entropy/Jensen intervals, and the coefficientwise `s^4=-1/18` obstruction with the fixed-vs-moving-direction caveat.

Strict criteria:

- exact symbolic identities must simplify to zero after using only the stated algebraic substitutions and positive-denominator domain assumptions;
- log interval claims must be checked by exact rational enclosures, not nearest floating estimates;
- finite examples can refute auxiliary methods but cannot prove or refute the open global theorem unless they violate a stated theorem claim;
- `S_full >= 0` and `M>0` remain `INCOMPLETE/OPEN` unless a complete public proof is supplied, which this review does not attempt.

Resource limits:

- initial arithmetic thread count: 1;
- no GPU;
- BLAS/OpenMP-style thread variables set to `1`;
- memory target at most 4 GiB;
- wall-clock target at most 15 minutes per bounded check;
- checkpoints saved as JSON/Markdown in this review directory.

Stop / recovery:

- report immediately on any exact sign, coefficient, quantifier, or source-scope mismatch;
- if a symbolic identity expands beyond the bounded plan, stop that check and mark only that identity `INCOMPLETE`, without launching determinant elimination or a scout;
- do not start duplicate jobs for metadata-only reruns.
