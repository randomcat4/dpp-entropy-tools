# I05-W4-20260909: real three-point DPP entropy subdomain theorem

This directory freezes the submitted result source and a separate verification pass.

The originally returned archive had SHA-256
`b408d1e8faa8bd99e2df33e03dc00548ff42c4e22ef3e814838049820000c308`.
Git tracks the complete expanded source; run `python build_result_zip.py` to create a
new self-contained archive from that source.  ZIP container metadata may make the
rebuilt byte hash differ from the originally returned archive.

## Status

- Original global target: **PARTIAL**.  General strict real three-dimensional
  `K`-affine entropy concavity remains unresolved.
- Frozen subdomain theorem T1--T3: **CORRECT within its stated scope**, under
  the review recorded in `review/INDEPENDENT_REVIEW.md`.
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
-H''(K;D) >= (7/10) (S + U + V) >= 0,
```

with `S`, `U`, and `V` defined in `submission/frozen_statement.md`.  It also
proves concavity on the convex domain and its closure, and negative definiteness
when the nonzero-edge graph is connected.

## Layout

- `submission/`: exact text/code/output snapshot from the submitted result.
- `build_result_zip.py`: rebuilds `I05-W4-20260909_result.zip` from the tracked submission tree.
- `review/INDEPENDENT_REVIEW.md`: mathematical audit and bounded verdict.
- `review/independent_verify.py`: fresh determinant/Mobius reconstruction; it
  imports no submission code.
- `review/independent_verify_output.json`: fixed-seed full-Hessian stress output.
- `review/RUN_LOG.md`: commands, hashes, the near-boundary float failure, and
  its high-precision resolution.
- `REVIEW_MANIFEST.sha256`: hashes for the complete integrated object.

The statement in `submission/verification.md` that the submission had not yet
been independently reviewed is retained as historical source metadata.  The
new review status is recorded only in this wrapper and the review directory.
