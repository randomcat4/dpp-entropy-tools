# S20 / PR116 successor recovery checkpoint

Status: **AUTHOR CANDIDATE / PENDING INDEPENDENT REVIEW.**

This directory is a successor checkpoint to merged PR #116. It does not rewrite the PR116 archive and does not claim that the missing continuum certificate has been independently reproduced.

The strongest candidate carried by this checkpoint is

`H''(t) <= -64 [alpha(1-alpha)]^2 t^2`

for the natural exchangeable `3+3` physical affine family described in `CANDIDATE_THEOREM.md`.

The new reproducibility artifact is `exact_model.py`, which uses only Python 3.9+ standard-library rational arithmetic. It reconstructs all 64 complete events directly from signed determinants and checks normalization, fixed marginals, the `t=0` product law, an independent interpolation point, a small explicit collection of exact joint-kernel points, and the center sharpness datum. The retained execution returned exit code 0 with no negative reserve among the 60 sampled points.

These are finite exact checks, not a continuum certificate. They do not substitute for the reported four-subregion proof, and no general dense rank-two theorem, entropy-rate theorem, novelty claim, formal verification, independent review, or merge authorization is made here.

Reproduce the finite check with:

```sh
python research/S20-pr116-successor-20260917/exact_model.py \
  --output /tmp/s20-exact-model.json
```

Literal retained execution summaries are under `output/`.
