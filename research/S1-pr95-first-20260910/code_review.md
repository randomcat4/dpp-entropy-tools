# Static checker and evidence review

Reviewed file: `research/I05-29-maximal-rank2-chord-20260910/code/verify_maximal_chord.py` at PR95 commit `54d9803b29f73669b9028e3519d17493e1b81be3`.

**STATIC STATUS: NO CRITICAL CODE-LOGIC DEFECT FOUND.** No execution was performed.

The checker:

- uses `Fraction` arithmetic for every sign-bearing comparison;
- reconstructs each principal-minor polynomial by a determinant permutation sum, then applies the full 64-event Mobius sum;
- checks that the law is even and quadratic in `s=t^2` and separately compares all event `a,b` coefficients with the Schur construction;
- checks both conditional cancellation families;
- evaluates every quadratic interval extremum using endpoints plus an in-interval vertex;
- applies the full `2 epsilon`, `280 epsilon`, and `421 epsilon` robustness penalties before testing the published interval rows;
- handles the full event separately on the last interval and checks its monotonicity reserves;
- encloses logarithms by a rational atanh series with an explicit geometric tail;
- isolates `s_*` and `t_*` by exact rational bisection;
- uses explicit `require` calls rather than optimization-disableable `assert` statements;
- writes exact rational JSON and the full coefficient CSV.

The saved CSV has the expected 64 event rows plus one header and the retained outputs report 417 explicit author checks. Those are packaging/source observations only. The checker trusts `input/fixture.json` as its input and is an author implementation; neither the source-entry binding nor the arithmetic is independent merely because the code is exact or replayed under `python -O`.

The independent finite role must use a separately written reconstruction and compare exact outputs. This static report does not upgrade either author execution to independent evidence.
