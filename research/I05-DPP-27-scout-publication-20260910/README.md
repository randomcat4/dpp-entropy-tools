# PR91 original polynomial trial publication

Data-only successor, based on main at branch creation `8f4acd31d0ce4d37defafbfcff22fa2b21356f72`. Tracks issue74 and PR91. PR91's frozen proofs and evidence at `c7a072ec4eea0c5b0f445bca5796873a9e234948` are not modified.

## Restored original data, not refitted coefficients

The source is the original 14-file `DPP27_PR91_raw_execution.zip` supplied in the research chat. The three trials were generated at t=5/4 on 2026-09-10, with original end timestamps 02:52:30.658172Z (degree6), 02:52:43.330002Z (degree8), and 02:52:46.587913Z (degree10). Original reported elapsed times are retained. No new scout run was performed for this publication.

`scout_degree6.json` and `scout_degree8.json` contain every original field, coefficient and diagnostic, with whitespace compacted only. Degree10 is split into FOUR ordinary JSON objects: `degree10/meta.json` contains the original non-coefficient fields, `u.json` contains exponents,c0,u, `v.json` contains c1,v, and `w.json` contains c2,w. `read_trials.py` reconstructs precisely the original object. There is no compressed/base64 transcription and no omitted coefficient.

The three bases contain 83,164,285 nonconstant monomials respectively. Including u,v,w and c0,c1,c2, they contain 252,495,858 numeric coefficients. The coordinate order is Q11,Q22,Q12. A monomial is `(8 Q11)^i (8 Q22)^j (8 Q12)^k`; `exponents` is an explicit ordered array. Constants c0,c1,c2 are Poisson equation constants, NOT constant monomial coefficients of u,v,w. All original decimals are parsed exactly as Decimal; the reader can evaluate them as rational numbers. Turning these decimals into exact rational trial coefficients does not certify any residual supremum.

The original executed `poisson_scout.py` is restored byte for byte (6229 bytes). It uses NumPy floating least squares and sampled finite differences. The original environment reported NumPy2.3.5 and CPython3.13.5. A rerun on another BLAS or environment need not reproduce identical fitted coefficients; these archived coefficients are the frozen inputs. The archived sampling count is1800 training/600 test, seed270074. Their UTC/elapsed fields are original run records, not new execution claims.

## Read, write, compare

Run from this directory:

```
python read_trials.py
python read_trials.py --write-dir /a/new/nonexistent-output-directory
python read_trials.py --compare-zip /path/to/DPP27_PR91_raw_execution.zip
```

The reader checks basis order, all coefficient counts and parse/write/parse exact numeric equality. The optional ZIP comparison checks every field against the original archived records. It does not run NumPy or recompute a DPP. The publication staging files were actually checked against the original ZIP, and the corresponding public Git objects were read back and matched to those staging files. No numerical or mathematical acceptance follows from data-transfer integrity.

For a new diagnostic run, copy the directory first: the original generator writes a same-name scout file. Then use `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python poisson_scout.py 6` (or8/10). This is a new execution, not reproduction of the original timestamps.

## Non-certification and failures

Every trial remains SCOUT_ONLY_NOT_A_CERTIFICATE. Sampled maxima and finite-difference Hessians do not bound suprema on the state ball or any parameter interval. These coefficients are not yet an S2 input verdict or an S3 mathematical acceptance. The current scope of PR91's first review remains an analytic implication with constant and residual gates.

The two earlier corrupted compressed-text fragments were withdrawn and remain in PR91 Git history. They are not the source for this restoration. The private Drive fallback is no longer necessary to obtain any of these three full trial records. The original ZIP remains a provenance backup; no access to it is needed to read or run the public parser and trial data.

This publication is a short checkpoint. The next mathematical unit uses a separate successor branch/PR and does not overwrite the proof under review. No server computation or old budget is claimed or restarted here.
