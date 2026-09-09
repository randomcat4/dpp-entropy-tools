# I05-W4-20260909: real three-point DPP entropy subdomain theorem

This directory freezes the submitted result and records a separate reconstruction audit.

The exact originally returned archive is stored losslessly as split Base64 text under
`payload/`.  Restore it with:

```sh
python3 build_result_zip.py
```

The command refuses to write an archive unless its byte length is 42,902 and its
SHA-256 is
`b408d1e8faa8bd99e2df33e03dc00548ff42c4e22ef3e814838049820000c308`.
The restored ZIP contains the full submitted proof, frozen statement, attempts,
sources, verification notes, exact inputs, code, and archived outputs.

## Status

- Original global target: **PARTIAL**. General strict real three-dimensional
  `K`-affine entropy concavity remains unresolved, and no entropy counterexample
  is supplied.
- Frozen subdomain theorem T1--T3: **CORRECT within its stated scope**, under
  the audit in `review/INDEPENDENT_REVIEW.md`.
- Execution/reproducibility: **PASS**.
- Novelty: **NOT REVIEWED**.
- External human peer review or proof-assistant formalization: **NOT PROVIDED**.

The accepted domain is

```text
0 < x_i < 1,
|K_ij| <= (1/4) sqrt(x_i(1-x_i)x_j(1-x_j)).
```

For every real symmetric direction `D`, the frozen theorem proves

```text
-H''(K;D) >= (7/10) (S + U + V) >= 0.
```

`S`, `U`, and `V` are defined in `frozen_statement.md` inside the restored
archive.  The result also gives concavity on the convex domain and its closure,
and negative definiteness when the nonzero-edge graph is connected.

## Independent verifier

The independently written verifier imports no submitted code.  Its exact source
is stored as split Base64 under `review/verifier_payload/`; the small launcher
`review/independent_verify.py` reconstructs the source in memory, checks SHA-256
`02cb42c069fcf8b78cd441c4dcc2880d1dd909f90bc1af4230df7570e484c3b2`,
and only then executes it.

```sh
python3 -m pip install -r review/requirements.txt
python3 review/independent_verify.py \
  --seed 20260909 \
  --random-centers 3000 \
  --output review/independent_verify_output.reproduced.json
```

## Layout

- `payload/`: lossless chunks of the exact submitted result ZIP.
- `build_result_zip.py`: restores and hash-checks that ZIP.
- `review/INDEPENDENT_REVIEW.md`: analytic reconstruction audit and bounded verdict.
- `review/independent_verify.py`: hash-checking launcher for the independent verifier.
- `review/verifier_payload/`: lossless chunks of the verifier source.
- `review/independent_verify_output.json`: fixed-seed full-Hessian stress output.
- `review/RUN_LOG.md`: commands, hashes, and the resolved near-boundary float failure.
- `PAYLOAD_HASHES.sha256`: hashes of the reconstructed archive, verifier source, and output.

The historical `verification.md` inside the submitted archive says that the
submission had not yet been independently reviewed.  It is left unchanged as
source metadata; the later audit status is recorded only in this wrapper and
`review/`.
