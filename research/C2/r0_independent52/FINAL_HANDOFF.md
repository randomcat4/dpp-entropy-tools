# C2 final hand-off: independent r=0 chain

Fresh nonauthor FIRST is **CORRECT** for the frozen r=0 candidate. C2 has
completed the independently authorized supplement. C3 alone owns the
unseen SECOND assignment and integration decision.

## Review binding

| Stage | Public commit |
|---|---|
| Frozen main formulas | `9dcb6e9079ca57f94e0e30d63161cda89ca61fae` |
| Independent author executable before run | `0bb970ef0a9d81ff79d4e0f38c28d2922067740e` |
| Complete author candidate reviewed by FIRST | `ba890f6294272849fa0a20d5c7e0e9f97d171d51` |
| Independent FIRST checker before run | `591c65bdc354e2880c6ccb2506822275b0e45a12` |

The final packet adds the fresh FIRST review/results and current status and
execution metadata. The reviewed author proof, implementation, frozen inputs
and mathematical artifacts have not been changed.

## Accepted FIRST scope

For `|mu|<1`, `|nu|<1`, `0<u<1`, `r=0`, the independently reconstructed
four-dimensional `Rstar` is positive definite. Using the already-accepted
main Schur reduction, this yields positivity of `M` on all six original
fixed physical directions. The new review does not replay the accepted
old eight-event-to-Schur derivation.

The exact chain is:

```text
formula-built Rstar -> determinant -> integer P -> integer Q
 -> positive P and nonzero determinant -> positive seed + constant inertia
 -> Rstar positive -> accepted Schur lift -> six-direction M positive.
```

Both implementations independently rebuilt the matrix and polynomial chain.
The determinant checks use Bareiss/Leibniz in the author and
permutation/Berkowitz in FIRST. Each implementation separately cross-checks
the direct Q substitution and the integer-binomial transform.

Fresh P has 26 integer terms, degree box `(4,4,16)`, and exactly matches the
archive. Every one of the 425 Q positions was checked, including the 36
zeros: 389 positive coefficients, minimum 192, maximum 99220032. Both the
archived and candidate tables match. The fresh seed at `(0,0,1/2)` has
scale 14400 and strict row margins `(10068,88320,88320,40053)`.

## Evidence entry points

- [Author proof](author_proof.md)
- [Author exact artifacts](outputs/author01/RESULT.json)
- [Fresh nonauthor FIRST narrative](review_first/REVIEW.md)
- [FIRST machine-readable verdict](review_first/verdict.json)
- [FIRST independent execution](review_first/run01/RESULT.json)
- [Runtime and resource ledger](execution/LEDGER.md)

The FIRST narrative explains the harmless literal-text diagnostic and the
reviewer's tighter internal deadline; raw records remain available.

## Execution closed

The new guard window started at 2026-09-09 13:32:37 UTC with the hard deadline
14:17:37 UTC. Author and FIRST arithmetic completed at 13:32:47 and 13:48:17
respectively; both PIDs exited and were confirmed absent. No jobs remain.
All work stayed within one live process, one CPU/thread, 16 GiB and no GPU.
No failed mathematical layer, rerun, extension or full-r arithmetic occurred.

The old PR55 FIRST INCOMPLETE is preserved as its historical outcome.
This packet supplies a separate new FIRST acceptance. SECOND is not claimed.
No full-r theorem, entropy counterexample, novelty or Lean certification is
claimed; C3's full-r work does not depend on this supplement.