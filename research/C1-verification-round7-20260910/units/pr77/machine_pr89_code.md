# PR89 machine finite-evidence static code review

Verdict: `STATIC_CODE_ACCEPTED_SCOPED` for the PR89 independent checker as a finite-evidence generator for the fixed PR77 object. I found no static implementation or evidence-packaging defect that prevents the PR89 raw outputs from closing the prior finite C2 obligations. This is a source/evidence code review, not a rerun and not a formal proof of the program.

## 1. Independence and input discipline

The implementation README states that the code was written from the original mathematical text and C3 contract, that no author checker or PASS output is imported, and that no compilation/import/test/pilot/arithmetic occurs before the single production clock (`source-snapshots/pr89_machine/implementation/README.md:3-4`). The request forbids author checker imports and says the later 8de8 additions are not executed input (`source-snapshots/pr89_machine/inputs/REQUEST.md:7-7`). The main program reads only `fixed.json`, writes `input_echo.json`, checks the exact frozen scope, and then runs phases A-D (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:532-565`).

Static result: no author module import, no live PR input, and no later delta dependency appears in the checker. The evidence is still only as independent as this one implementation plus its built-in cross-checks; PR89 is not a second independently written checker.

## 2. Phase A implementation

The code uses Python `Fraction` for rational arithmetic (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:16-16`). It builds uniform comparison residuals, derivative constants, Bregman/tail constants, point-specific tails, and exact covariance polynomials before comparing them to fixed literals (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:140-162`, `source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:165-270`). For Fisher covariance algebra, it computes each determinant by both recursive Laplace expansion and permutation expansion, then checks equality before using the polynomial (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:118-137`, `source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:237-268`).

Static result: Phase A meets the contract shape. It reconstructs the exact rational constants and Fisher covariance polynomial, then compares to author-displayed literals. The outputs and CHECKS rows retain enough evidence to review the comparison without relying on a PASS summary (`source-snapshots/pr89_machine/outputs/run01/A/covariances.json:2-63`; `source-snapshots/pr89_machine/outputs/run01/CHECKS.jsonl:57`; `source-snapshots/pr89_machine/outputs/run01/CHECKS.jsonl:60`).

## 3. Phase B complete-event and jet cross-checks

The direct determinant route uses a literal signed event matrix and pivoted Bareiss determinant with division-remainder checks (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:273-315`). The derivative cross-check route replaces determinant rows by derivative rows and includes the factor 2 for second derivatives (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:317-330`). The production-style route uses a four-bit frontier recurrence over six width-two masks and carries value, first derivative, and second derivative jets in physical `t` (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:333-370`).

The Phase B driver compares recurrence values with direct determinants through `n=8`, compares Mobius inversion through `n=6`, checks prefix harvesting, and compares jets through row derivatives through `n=6` (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:605-652`). The output coverage is exactly the requested 378 Mobius cases, 1530 direct cases, and 378 jet cases, with physical-t derivative scaling recorded (`source-snapshots/pr89_machine/outputs/run01/B/coverage.json:2-10`).

Static result: Phase B is a real independence check against the main recurrence for small sizes. Its limitation is also clear: it validates production logic by exhaustive small cases and exact identities, not by running a separate full-depth production implementation. That limitation matches the C2 contract.

## 4. Phase C production enumeration and raw retention

The production function traverses a depth-19 binary tree once for each fixed `t`, records depth 18 and 19 events, rejects nonpositive `N`, aggregates by integer `N`, accumulates `count`, `sum_Nprime`, `sum_Nsecond`, and `sum_Nprime_squared`, and records deterministic word-jet hashes (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:697-760`). It checks event counts, normalization, positivity, and aggregation normalization before writing histogram gzip chunks (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:739-757`).

The gzip helper writes deterministic gzip files with mtime 0, ASCII JSONL, explicit schema, chunk sizes, byte sizes, and SHA-256 hashes (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:654-694`). The C manifests and totals are present for all six production pairs and use the schema required for value, Fisher, and acceleration reconstruction (`source-snapshots/pr89_machine/outputs/run01/C/t1_n18_histogram_manifest.json:2-49`; `source-snapshots/pr89_machine/outputs/run01/C/t3_n19_totals.json:2-12`).

Static result: Phase C closes the original raw event/aggregation packaging gap. I did not decompress the full 158 MB evidence or recompute any histogram sums; I inspected the manifests, totals, output hashes, and representative schema rows only.

## 5. Phase D directed interval arithmetic

The Decimal contexts are precision 100 with floor, ceiling, and half-even nearest modes, and `FloatOperation` traps are enabled (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:25-31`). Integer logs use `Decimal(N).ln(context=NEAR)`, treat `N=1` exactly, enforce the production domain, and widen by `1e-90` under directed contexts (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:416-422`). The official Python Decimal documentation says `Decimal.ln` is correctly rounded with `ROUND_HALF_EVEN`; the PR89 decimal contract cites the same rule (`source-snapshots/pr89_machine/outputs/run01/D/decimal_contract.json:10-15`).

The finite entropy routine keeps weighted entropy, Fisher numerator, and acceleration numerator separately; then it forms `H` and `Hsecond` with directed arithmetic and records each component (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:425-460`). Phase D forms `h18` and `h18second` as `n=19` minus `n=18`, subtracts `E18` only at the midpoint Jensen lower bound, and uses each point's own `Tail18` for the true-curvature interval (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:463-529`).

Static result: the code implements the C2 contract's error direction, tail separation, and Fisher/acceleration separation. The D outputs retain finite intervals, conditional intervals, true-rate Jensen margin, and all three point-curvature margins (`source-snapshots/pr89_machine/outputs/run01/D/true_rate_Jensen.json:1-29`; `source-snapshots/pr89_machine/outputs/run01/D/true_curvature_t1.json:1-22`; `source-snapshots/pr89_machine/outputs/run01/D/true_curvature_t2.json:1-22`; `source-snapshots/pr89_machine/outputs/run01/D/true_curvature_t3.json:1-22`).

## 6. Ledger and failure handling

Every `check` call writes a JSONL row with sequence, phase, gate, boolean result, and data; a failed gate writes `FIRST_FAILURE.json` and halts (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:68-77`). Deadline checks are called before checks and progress writes (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:63-70`, `source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:80-85`). The main exception handling distinguishes timeout, memory limit, and mechanical exception, writes exit contexts and final status, and builds an output hash manifest (`source-snapshots/pr89_machine/implementation/independent_pr77_checker.py:566-588`).

The final ledger records `MACHINE_PASS`, exit 0, 2772 ordered checks, zero repairs, zero prior arithmetic attempts, and no deadline reset/extension/rerun (`source-snapshots/pr89_machine/execution/RUN_LEDGER.json:27-35`). Static parsing of `CHECKS.jsonl` found 2772 rows and no failed row. The load-bearing final rows are the log-widening gate, finite/conditional width gates, Jensen margin gate, and point curvature margin gates (`source-snapshots/pr89_machine/outputs/run01/CHECKS.jsonl:2750` through `source-snapshots/pr89_machine/outputs/run01/CHECKS.jsonl:2772`).

Static result: failure handling and output retention are adequate for this C1 finite-evidence gate. I did not read or expose the private invocation file; only its existence as a hashed internal manifest entry and public omission are relevant.

## 7. Remaining code-review limits

This code review does not certify whole-interval curvature, Section 9 true-rate derivative passage, formal correctness of the Python interpreter/libmpdec, or absence of all possible shared conceptual mistakes between the contract and implementation. It accepts the checker as a scoped finite-evidence generator because the source, cross-checks, raw outputs, manifests, execution ledger, and strict margins match the precise C2 contract for the fixed PR77 claims.
