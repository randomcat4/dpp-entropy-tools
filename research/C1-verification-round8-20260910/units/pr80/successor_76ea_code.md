# Successor 76ea code and evidence review

Scoped verdict: code was read but not executed. The two scripts are plausible author finite-check drivers, but the saved output files are not evidence-ready as raw transcripts of the current scripts. Every finite sign, count, and fixture-identity assertion remains pending a future independent C2 reconstruction, if separately authorized.

## Findings

### P1 - Saved outputs do not match the scripts as raw stdout

`verify_s09_fiber_window_bound.py` lines 2-4 imports `verify_s09_signed_fibers.py`, and the imported file has top-level print statements at lines 219-233. Therefore a plain run of the fiber-window script should first emit the signed-fiber certificate output unless the import output is suppressed externally. The saved `verify_s09_fiber_window_bound.txt` lines 1-25 contain only the fiber-window output.

There are additional transcript mismatches. `verify_s09_signed_fibers.py` line 221 prints `strict legal, min q approx:` followed by a float, while the saved output line 3 says only `strict legal, min q > 0`. The saved output files also contain explanatory final lines that are not printed by the scripts: `verify_s09_fiber_window_bound.txt` line 25 and `verify_s09_signed_fibers.txt` line 31.

Minimum repair: label the output files as edited summaries unless a separate reproduction run is explicitly authorized and raw outputs are regenerated from the exact committed scripts. If the intended design is that importing `verify_s09_signed_fibers.py` reruns assertions silently, move its printing behind a main guard and expose a callable verification function for the importer.

### P2 - The fiber-window script labels a nonessential companion value as an upper endpoint

`verify_s09_fiber_window_bound.py` lines 24-35 form an interval for `c`, use an upper bound `delta_hi`, and compute both `lo` and `hi` with the same subtractive `delta_hi` penalty. The lower endpoint `lo` is the quantity needed for the proof and is conservative. The reported `hi` is not, from the source alone, a rigorous upper enclosure for the theorem's right side because an upper enclosure would need the opposite endpoint for the negative `-2 delta E|z|` term.

Minimum repair: if only positivity is being certified, stop labeling the second column as an upper endpoint and call it a companion conservative value. If an actual enclosure is intended, compute and report a true upper endpoint with the appropriate lower bound for `delta`.

### P2 - Fixture identity is asserted but not independently bound in the successor delta

`ADDENDUM_S09_SIGNED_FIBERS.md` line 25 says the script uses exactly the public PR58 fixture. The script embeds rational matrices at lines 10-27, but this successor delta does not itself bind the PR58 source file or prove that these matrices are the same fixture.

Minimum repair: provide an immutable PR58 fixture source binding for C2, or phrase the finite theorem as applying to the embedded rational matrices and leave PR58 identity as a separately checked provenance claim.

## Evidence accepted in this FIRST review

Accepted at source level only:

- The scripts encode the intended formulas in recognizable form: the original ratio-cone `F`, the square-completed one-event integrand, the product-reference fiber averages, and the fiber-window lower bound.
- The scripts include assertions for strict legality, block marginal normalization, conditional coefficient cancellations, ratio-cone bad-pair counts, Cauchy slack identity checks, negative event list, positive fiber averages, and positive fiber-window lower endpoints.

Not accepted without C2:

- The 75/66 bad-pair counts.
- Any worst negative `F` enclosure.
- Any positive fiber average or positive fiber-window lower endpoint.
- The equality of the embedded fixture with PR58.
- The claim that saved outputs are reproducible transcripts of the current scripts.

## Future C2 gates

This is a future suggestion only, not authorization to start C2 and not an expansion of any PR70 or PR77 budget. A fresh C2 should independently reconstruct the finite certificate from the frozen mathematical identities and literal embedded rational fixture, then report:

1. The independently reconstructed event table, coefficients, block marginal weights, fiber moments, strict log intervals, and signs.
2. For ratio-cone failure, a complete table or checksum-backed certificate of every checked pair, including zero-`Delta u` exclusions and the certified negative witnesses.
3. For fiber-window coverage, per-fiber exact inputs `q_-`, `q_+`, `E[v^2]`, `E[z]`, `E|z|`, lambda endpoint enclosures, and the final lower endpoint.
4. Separate gates for mathematical formula implementation, finite arithmetic correctness, fixture provenance, and strictness.
5. Optional author-material comparison: the author scripts and saved outputs may be compared against the independent reconstruction, but must not be imported, executed, or used as the independent computational source. Raw stdout matching can be statically classified from source/output mismatch, or reproduced later only under separate explicit authorization; it is not a C2 acceptance prerequisite.

No author-module execution as independent evidence, long whole-chord job, formal check, or PR70/77 budget expansion is authorized or needed for this bounded successor evidence check.
