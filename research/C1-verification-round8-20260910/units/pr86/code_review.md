# PR86 static code/evidence FIRST review

Verdict: **SOURCE_ONLY / PENDING_C2 for all executable evidence**. I read the frozen scripts, JSON certificates, and stdout artifacts statically. I did not run Python, import modules, regenerate JSON, compare raw outputs, compile, execute tests, perform arithmetic reconstruction, or validate any interval certificate.

Reviewed head: `bd12e6094e098499fae7e01729a4b29f021a14e2` over base `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. Source alias: `source-snapshots/pr86/`. Immutable compare: <https://github.com/randomcat4/dpp-entropy-tools/compare/65e59a46b49cd2dbb5c779a4cfae8cef26441984...bd12e6094e098499fae7e01729a4b29f021a14e2>.

## Static findings

### P1. `full_square_certificate.json` is referenced and generated, but not archived in the bound source set

`certify_full_square.py` writes `full_square_certificate.json` at lines 189-190 and prints the pass/summary lines at 191-193, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certify_full_square.py#L189-L193>. `full_canonical_square.md` says the compact certificate stores row minima and that the stored result is `full_square_certificate.json`; see lines 133-138 and 157-165, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/full_canonical_square.md#L133-L165>.

The frozen `SOURCE_BINDING.json` file list does not include `research/N4/I05_30_20260910/full_square_certificate.json` or `full_square_stdout.txt`. This leaves the full-square evidence package weaker than the text claims. Minimum repair: publish a separately frozen successor containing the generated full-square certificate with binding metadata, or remove the claim that it is stored in such a successor. A future independent finite review still must rebuild the cover rather than accepting the author-generated artifact as a certificate by itself.

### P2. Top-level reproduction/evidence instructions omit later verifier scripts

README lines 33-42 instruct reproducing only `certify.py` and `dilute.py`, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/README.md#L33-L42>. The frozen packet also contains `certify_full_square.py`, `extend_diagonal.py`, and `extend_edges.py`, which are the relevant generators for the full-square, equal-angle, and edge certificates. Minimum repair: update the README to identify all verifier scripts, all generated/archived outputs, and the evidence status of each theorem.

### P3. `dilute.py` reuses author helper code, so it is not independent evidence

`dilute.py` imports exact-log, law, gap, and legality helpers from `certify.py` at line 11, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/dilute.py#L1-L12>. The theorem text discloses this at `dilute_chord_theorem.md` line 156, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/dilute_chord_theorem.md#L156>. This is acceptable as an author fixture verifier, but it must not be treated as an independent computational source. Any future independent C2 gate should rebuild the event polynomials and log bounds from the frozen mathematics/literal rational fixtures and compare against these outputs only afterward. No such C2 run is authorized by this report.

## Evidence inventory

- `certify.py` reconstructs signed complete laws, checks Möbius equality, expands the 11 displayed midpoint minors, records affine midpoint jets, checks sign-transfer changes, and writes `certificate.json`; see lines 56-67, 79-107, 114-161, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certify.py#L56-L161>. Static status: author evidence only.
- `certificate.json` is a one-line author certificate with top keys `log_terms`, `log_remainder`, `cases`, and `angular_box`. It records the `intersection1` and `intersection0` cases, atom groups, jet intervals, and the angular-box constants. Static status: author evidence only.
- `certificate_stdout.txt` explicitly labels itself as author execution, not independent review, at lines 1-2 and reports PASS at lines 35-36, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certificate_stdout.txt#L1-L36>. Static status: annotated author transcript only.
- `certify_full_square.py` reconstructs all 16 complete midpoint atoms, regular factors, rational interval boxes, and scalar-term bounds, then writes the missing full-square certificate; see lines 92-193, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certify_full_square.py#L92-L193>. Static status: script-only evidence until generated output is archived and independently checked.
- `extend_diagonal.py` reconstructs the equal-angle atoms, regular factors, derivative identity, 256 box upper bounds, and anchor interval, then writes `diagonal_extension_certificate.json`; see lines 81-151, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/extend_diagonal.py#L81-L151>. Static status: author evidence only.
- `diagonal_extension_certificate.json` records status `AUTHOR EXACT INTERVAL CERTIFICATE; PENDING_EXTERNAL_REVIEW`, 16 atoms, 16 regular factors, 256 derivative boxes, maximum derivative upper bound, and anchor interval. Static status: author evidence only.
- `extend_edges.py` reconstructs edge laws, rechecks earlier PR86 fixed claims, certifies the common-line derivative boxes, certifies the zero-intersection Bernstein numerator, and writes `edge_extension_certificate.json`; see lines 94-123, 132-217, 255-304, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/extend_edges.py#L94-L304>. Static status: author same-session evidence only.
- `edge_extension_certificate.json` records status `FRESH SAME-SESSION RECHECK; NOT EXTERNAL REVIEW`, the rechecked PR86 fixed claims, 256 intersection-edge derivative boxes, and zero-intersection Bernstein data. Static status: author evidence only.
- `dilute.py` builds two dense equal-diagonal fixtures, checks equal diagonals/ranks/commutators, compares second-coefficient formulas, bounds third derivatives, chooses explicit lambda intervals, and writes `dilute_certificate.json`; see lines 73-115, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/dilute.py#L73-L115>. Static status: author evidence only.
- `dilute_certificate.json` is a one-line author certificate for `dense_intersection1` and `dense_intersection0`, with second-order intervals, rho, remainder bound, all-lambda interval, direct endpoint check, full-intensity sample value, and q-polynomial groups. Static status: author evidence only.
- `dilute_stdout.txt` contains two printed author result records for the dense fixtures, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/dilute_stdout.txt#L1-L2>. Static status: author stdout only.

## Static code observations

The script bodies are narrow and mostly aligned with the theorem text. They use rational SymPy expressions, standard-library `Fraction`, explicit atanh-series log enclosures, sign-aware interval operations, complete-law reconstruction, and assertions rather than search heuristics. The code is not packaged as a reusable verifier and should not be represented as one.

The main evidence risk is not an obvious static code contradiction; it is independence and packaging. Running the author scripts would at most reproduce author evidence unless a reviewer rebuilds the mathematics independently. The absent full-square certificate also means the most sweeping fixed-family finite result lacks the archived data file its prose promises.

## Test/execution status

No tests or scripts were run. No Python or SymPy process was started. No author module was imported. No finite, interval, entropy, Fisher, acceleration, or formal check was performed. All executable evidence remains pending independent review.
