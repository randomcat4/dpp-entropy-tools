# PR88 C1 FIRST code/evidence review

Scoped verdict: `SOURCE_ONLY / PENDING_C2` for `verify.py` and `certificate_compact.json`; no source-blocking code defect found by static reading. I did not run, import, compile, or reconstruct the checker or certificate.

## Files reviewed

- `source-snapshots/pr88/research/N4/I05_20260910/verify.py`, 311 lines, blob `9b7282e9abb87d03057d6e36d3b28c75d63f03fa`.
- `source-snapshots/pr88/research/N4/I05_20260910/certificate_compact.json`, 1 line, blob `ca24722d147a060b9f052ddcca58b7224993b3a4`.
- Evidence documentation in `source-snapshots/pr88/research/N4/I05_20260910/fixtures.md`, 166 lines, blob `19b62f741d90db851d73fcd4c8e652aa41b60299`.

## Static findings

`verify.py` is an author-side exact rational/log-interval evidence script. It imports SymPy at line 15, defines logarithm bounds and entropy interval machinery around lines 60-88, constructs DPP laws by signed determinant/Mobius routines around lines 101-115, and then builds the three advertised fixtures in `method_fixture` (lines 139-174), `common_mode_fixture` (lines 184-210), and `multiring_fixture` (lines 219-281). The `main` routine at lines 292-311 writes a generated certificate and reports completion if the assertions survive.

By static reading, the script is organized around explicit rational kernels, exact symbolic determinants, outward log bounds, and assertion checks for signs and identities. The script does not appear to fetch network data or depend on hidden input beyond the optional output filename. If it is ever used as a verifier rather than an author evidence generator, it should be run in a normal assertion-enabled Python mode; its validation checks are expressed as `assert` statements throughout lines 42-281.

`fixtures.md` correctly states the evidence status. It labels the universal auxiliary bridge as disproved only as a method and says no entropy-concavity counterexample is obtained at lines 3 and 51-95. It also says finite certifications are author computations pending review at line 3, describes reproducible execution and log-enclosure choices at lines 138-165, and warns that an independent verifier should reconstruct from the kernels rather than trust the stored certificate at line 166.

`certificate_compact.json` is a compact generated evidence record, not a proof artifact by itself. It stores author runtime metadata, exact atom arrays, log-interval signs, lift bounds, multiring atom polynomials, endpoint coefficients, and finite probes all on line 1. Under this FIRST scope those entries remain source evidence only, even where their labels are internally consistent with `fixtures.md` and `verify.py`.

## Evidence classification

- Analytic proof text in `proof.md` and `continuation.md`: reviewed separately in `review_report.md` and accepted only within the stated scoped hypotheses.
- Author finite bridge/lift/multiring signs: `SOURCE_ONLY / PENDING_C2`.
- Author checker implementation: statically readable and coherent as an evidence generator, but not independently executed.
- Compact certificate: `SOURCE_ONLY / PENDING_C2`; not trusted as standalone verification.
- Issue #87 heavy continuous verification: documented by the author as requested/not running in `README.md` lines 5 and 74; no execution was authorized or performed in this FIRST.

No new finite-checking obligation or expanded C2 budget is created by this report.
