# Round-two execution and correction ledger

| Research unit | PID | Exit | Centers | Hessians | Chords | Entropy calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Parent pilot | 160788 | 0 | 12 | 12 | 36 | 144 |
| F1 | 161087 | 0 | 72 | 72 | 216 | 504 |
| F2 | 161588 | 0 | 24 | 24 | 144 | 312 |
| Total | | | 108 | 108 | 396 | 960 |

Counts are evaluations, not unique matrices. Independent certificates,
the coordinator preflight, support/PD self-checks and read-only
postprocessing are separate. F1 has 72 chord directions (66 noncommuting,
six isotropic controls); F2 has 48 noncommuting directions.
All batches have zero failed centers and zero positive candidate files.
The pilot used NumPy binary64; F1/F2 used 60-digit mpmath for supported-event
Hessians/entropy, with exact rational feasibility.

Compute runtime: Python3.12.3, NumPy2.5.3, SciPy1.18.1, mpmath1.4.1.
OMP/OpenBLAS/MKL/NumExpr were restricted to one thread; no GPU.
The pilot elapsed 0.0255 s, F1 5.6261 s, F2 6.5119 s.
Original manifests bind source SHA256, settings and counters.
Final source_binding.json checks those bytes against the retained files.

The pilot also checked 192 rational event masses and 12 finite differences.
F1 evaluated 1080 proper-event jets, 7560 entropy determinants, 864 exact
Sylvester checks and one author's 16-event exact-jet self-check.
F2 evaluated 624 supported-event jets, 8112 entropy determinants, 576 exact
Sylvester checks, three frame checks and 48 exact determinant jets of A.
Postprocessing reads saved jets only; it adds no kernel evaluations.

## Independent verification

See review/run_ledger.md for local bundled Python3.12.14 runs:
q entropy gate PID54680, negative face/BSC certificate PID33400,
and coarsening polynomial comparison PID12864 all exited zero.
They used ten q logarithm intervals, 45 face and 48 lifted event logarithm
intervals, and 16 event-polynomial comparisons. No review server job ran.
The presentation supplement ran as local PID64800, exit0, and repeated the
same ten q / 45 face / 48 lifted logarithm intervals to save outward rational
endpoints. It introduced no new fixture, chord or scout evaluation. Its
script/output hashes and general identity-review annotation are in
review/presentation_and_identity_supplement.md. Thus the four successful
review executions include 206 log intervals and 16 event-polynomial checks.

## Corrections and failed attempts retained

1. The original pilot manifest erroneously says 120 entropy calls.
   The actual code performs 12 per center, hence 144. Original source and
   manifest are preserved; pilot/report.md makes the correction.
2. Early layer shorthand called C_k the layer entropy second derivative.
   Correctly C_k=-sum(p'^2/p+p''logp), while H_k''=C_k-P_k''.
   Search reports now retain both. Total H'' was unaffected.
3. Original independent certificates printed bounds through float conversion;
   rounded decimals are approximate displays, not outward enclosures.
   A separately retained exact-rational presentation supplement provides
   outward bounds. Original files and hashes are not overwritten.
4. Two review shell-alias attempts failed before arithmetic because the alias
   did not provide Python. They wrote no certificate. Successful scripted
   runs supersede them; no failed numeric center or candidate is hidden.
5. Administrative Git/network transport retries are not research evaluations.
   Exact final tree comparison guards against silent source changes.
6. The first raw-byte binding check detected four review-output hash mismatches;
   source_binding_initial.json preserves that failed archival check. All eight
   executed-source bindings and three reviewed proof blobs matched exactly.
   The four JSON outputs were generated with Windows CRLF and normalized to LF
   by Git. Reconstructing CRLF from each Git blob reproduces its recorded hash
   exactly. source_binding.json records both hashes and the reconstruction;
   no scientific source, proof or JSON value was changed.

All research batches and review processes ended. Final read-only process
checks verify this without stopping unrelated work.
