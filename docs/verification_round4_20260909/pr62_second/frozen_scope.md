# PR62 Second Review Frozen Scope

## Verdict By Unit

| Unit | Status | Scope decision |
|---|---|---|
| Analytic rank-one midpoint theorem | CORRECT | Accepted for `n>=2`, unit `x,y in R^n`, and `0<a,b<1`, with `K_- = a xx^T`, `K_+ = b yy^T`, and true arithmetic midpoint `K_0=(K_-+K_+)/2`. |
| Strictness and equality cases | CORRECT | Accepted: equality occurs exactly when `K_-=K_+`; otherwise the midpoint gap is strict. |
| Common independent-bit-flip lift | CORRECT | Accepted for every distinct accepted rank-one chord and every `epsilon` satisfying the stated finite-alphabet continuity margin `2 omega_n(epsilon) < G`, with `delta_n(epsilon) <= 1-2^{-n}`. |
| Static code/output interface inspection | CORRECT | Accepted only as scope-coherence inspection: scripts and stored outputs label their numerical roles consistently with the markdown proof. |
| Finite execution and numerical certification | INCOMPLETE | No independent rerun, finite certification, interval certification, or promotion of printed decimal diagnostics was performed. |
| Correlated `3+3` multiring line | INCOMPLETE | Excluded from theorem acceptance; it remains a frozen finite setup plus diagnostics, not a family sign theorem or counterexample. |
| Formal verification | INCOMPLETE | No Lean, proof assistant, interval arithmetic, or formal certificate was run or accepted. |
| Novelty and priority | INCOMPLETE | No novelty, priority, or publication-strength claim is certified. |

## Accepted Public Scope

The accepted analytic theorem is exactly the moving real rank-one endpoint arithmetic-midpoint result in `input/moving_rank1_theorem.md`:

- Complete DPP atom entropy is defined by the atom formula and Shannon entropy in lines 5-10.
- The theorem quantifies `n>=2`, unit vectors `x,y`, and `0<a,b<1` in lines 15-22.
- The asserted midpoint concavity and equality condition are lines 24-32.
- The proof covers moving directions and unequal endpoint eigenvalues through the decomposition of the actual matrix midpoint, not a curved moving-frame path, in lines 68-80 and 167-187.
- Zero coordinates are allowed because the derivative proof ignores inactive pairs with `b_ij=0` and active pairs force strictly positive logarithm ratios; see lines 125-155.

The accepted lift is exactly the common independent-bit-flip construction:

- The affine kernel map and strict spectral legality are stated in lines 169-187.
- The exact probability generating function identity is in lines 223-244.
- The finite-alphabet total-variation continuity bound and explicit sufficient margin are in lines 246-256, with the margin condition stated in lines 189-220.

## Exclusions

This review does not accept or certify:

- arbitrary rank-two endpoint chords;
- moving rank-three or higher-rank frame theorems;
- unrestricted real DPP configuration-entropy concavity;
- large interior lifts beyond the explicit Fannes-Audenaert margin condition;
- any whole-multiring interval theorem;
- the six-coordinate numerical fixture as an independent finite certificate;
- the dense `3+3` multiring diagnostics as a theorem;
- any novelty, priority, formal-verification, or GitHub discussion claim.

These exclusions match the author packet's own limitations in `input/README.md` lines 18-19 and 53-58, `input/moving_rank1_theorem.md` lines 301-310, `input/multiring_fixture.md` lines 165-176, and `input/failure_ledger.md` lines 43-49.

