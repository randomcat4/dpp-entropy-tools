# PR89 fixed finite machine evidence — frozen scope

## Reviewer position

Independent SECOND reviewer, non-author. This is a bounded static review of the PR89 fixed finite evidence package for the already-reviewed PR77 object. I preserved the earlier PR77 reports and did not rewrite them.

## Allowed inputs actually used

Allowed local package:

- `docs/verification_round4_20260909/pr77_second/machine_input/`
- `docs/verification_round4_20260909/pr77_second/machine_input_binding.json`

The delivered binding identifies PR89 head `1d805e094a0faf0018127ee832f5e1ac74996b41`, executable/preparation head `d68fec7f10f4451dd9a16c19000c35219db33400`, and PR77 author head `6ebe38dc6503120d47e9d644cfac78cfb43666f5`.

I did not read FIRST reviews, other SECOND reviews, C3 adjudication/status files, top-level README/STATUS/machine_notes/FINAL_HANDOFF, PR89 status material outside the allowed package, PR78, live successors, private handoffs, remote scripts, or `[excluded private directory]`.

## Operations performed

This review used only source reads, JSON parsing, byte hashing, static implementation inspection, raw log/schema inspection, and gzip manifest/line-count checks. I did not execute or import `independent_pr77_checker.py`; did not run author scripts, SymPy, determinant, logarithm, entropy, or interval arithmetic; and did not do independent numerical recomputation.

Static checks performed:

- matched the 196 delivered files in `machine_input/` against `machine_input_binding.json` by byte count and SHA-256;
- recomputed SHA-256 for every delivered file and the binding file into `machine_source_binding.json`;
- checked `outputs/run01/output_hashes.json` against public output files, excluding only the declared omitted private `invocation_private.txt`;
- checked all 12 gzip manifests, 102 gzip chunks, chunk byte sizes, SHA-256 digests, declared row counts, and first-row JSON parseability;
- counted and parsed all 2772 `CHECKS.jsonl` rows;
- read the request, implementation description/source, run guard/plan/ledger, environment/status/progress/exit/input echo, finite totals, and true-rate summary outputs.

## Binding result

Formal delivered binding result: `CORRECT`.

- `machine_input_binding.json`: 196 declared files, 196 files on disk, 0 missing, 0 extra, 0 byte/hash mismatches.
- `outputs/run01/output_hashes.json`: 179 declared run-output entries; 1 missing private entry, `invocation_private.txt`, exactly matching the ledger's declared private omission; 0 public hash/byte mismatches.
- gzip evidence: 12 manifests, 102 chunks, 2,363,904 declared rows; all chunk hashes, byte counts, row counts and first JSON rows checked cleanly.
- `CHECKS.jsonl`: 2772 rows, 0 parse failures, 0 failed checks.

Non-blocking packaging note: `inputs/PREPARATION_SHA256.json` lists 13 preparation-tree files. The delivered local package lacks `.gitattributes` and root `README.md`; these two are also absent from the formal `machine_input_binding.json`. This prevents verification of those two preparation-manifest entries from the local package, but it is not a mismatch of the PR89 delivered evidence binding and does not touch the fixed finite mathematical artifacts reviewed here.

## Mathematical scope reviewed

The reviewed machine object is only the fixed PR77 finite unit requested in `inputs/REQUEST.md`:

- fixed `t = 1/2, 1, 3/2`;
- conditioning depth `r = 18` and event lengths `n = 18, 19`;
- Toeplitz matrix with diagonal `1/2`, first off-diagonal `t/16`, second off-diagonal `1/8`;
- scaled signed event matrix convention and physical `t` jets;
- Requests A-D: exact analytic constants/covariance algebra, small independent event recurrences/crosschecks, full production enumeration/histograms/jets, and finite directed intervals/true-rate fixed-point bounds.

The reviewed machine object does not prove a whole-continuum curvature sign, does not close PR77 Section 9 true-rate derivative passages, does not assess novelty, and does not constitute a formal proof artifact.
