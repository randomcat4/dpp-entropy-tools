# Execution evidence and artifact scope

The retained author execution ran `python code/verify_maximal_chord.py` using Python 3.13.5 and standard-library exact fractions. It passed 417 checks. Its literal stdout is `output/verify_maximal_chord.stdout.txt`; the elapsed time printed there is observed runtime, not a promised computation budget or independent-review record.

The code builds every principal-minor polynomial by the determinant permutation formula, applies the defining Mobius sum to all 64 complete events, and separately checks the two Schur coefficients using exact matrix inverses. The three interval rows use endpoints and quadratic vertices only; the full legal root is isolated by rational bisection. No entropy time grid supplies any proof claim.

Only six fixed logarithm inequalities are used. For 1<=x<=2 and z=(x-1)/(x+1), the code uses

`2 sum_{k=0}^{N-1} z^(2k+1)/(2k+1) <= log x`

` <= 2 sum_{k=0}^{N-1} z^(2k+1)/(2k+1) + 2 z^(2N+1)/[(2N+1)(1-z^2)]`, N=40.

Power-of-two range reduction handles the original six rational arguments. This is a directed rational enclosure with a proved remainder, not floating arithmetic. Decimal displays are rounded outward from exact fractions. JSON and CSV retain exact rational values.

The first complete certificate execution passed; no exact mismatch was suppressed. Earlier exploratory floating moment bounds were used to find and discard an insufficient one-window estimate. That mathematical failure is retained in SOURCES_AND_FAILURES rather than reported as a true entropy sign.

The accompanying moving-endpoint stability theorem is analytic and was completed after the first local checkpoint/publication attempt; it does not depend on a separate numerical job. Author computation is not independent verification. No checksum files or font files are included.

## Isolated packaging replay

After assembling the proof notes, the unchanged input and checker were copied to a fresh temporary directory and executed with `python -O code/verify_maximal_chord.py`. All 417 explicit `require` checks still ran and passed. The generated rational JSON and complete-event CSV were byte-for-byte identical to the retained first-run evidence. The separate replay stdout is retained as `output/packaging_replay.stdout.txt`. This is another author execution for packaging QA, not an independent reviewer, independent implementation, or independent C2 run. The runtime line naturally differs between the two executions.
