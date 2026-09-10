# I05-30 successor: evidence repair, axis-to-wedge extension, and strong-middle work

Base: current `main@8f4acd31d0ce4d37defafbfcff22fa2b21356f72`. This is a successor packet; it does not change the frozen PR86 head `bd12e6094e098499fae7e01729a4b29f021a14e2` or the frozen PR88 head `6c8ad2eaedcc93c7dfc5417b2d71b4e826d9be5c`.

All entropies are natural-log Shannon entropies of the complete finite DPP law

\[
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T,
\qquad \det K_\varnothing=1,\qquad 0\log0=0.
\]

Every chord and midpoint below is affine in the physical kernel `K`. Complete Fisher and acceleration terms are retained whenever curvature is evaluated.

## Review state used here

The latest bounded PR88 review accepts the restricted analytic units: complete rank-two mixed-minor bookkeeping; the full-chord theorem for an indefinite rank-two difference supported on three actual coordinates; the common-mode specialization; and the fixed-affine multiple-boundary asymptotic. PR88 finite values remain source-only/pending machine review.

The latest PR86 FIRST accepts its analytic complete-event/sign identities, qualitative fixed-pair dilute theorem, thinning-star theorem and disjoint actual-coordinate-block theorem. It requires two source/evidence repairs: the promised `full_square_certificate.json` was absent, and the original README did not map later theorem/evidence files. PR86 finite angular/edge/diagonal/full-square/Fisher/lift claims remain source-only pending an independent server calculation.

## Repair of PR86 evidence and navigation

This successor supplies, without rewriting the reviewed source:

- `pr86_evidence_repair.md`: the complete theorem/evidence/reproduction map for all 18 files of frozen PR86;
- `certify_full_square.py`: the frozen self-contained 4096-box generator copied verbatim for reproducibility;
- `full_square_certificate.json`: the previously absent generated certificate;
- `full_square_stdout.txt`: the corresponding bounded author execution record.

The exact rerun passed and recorded a minimum lower bound `0.012067200390564330` on box `(63,63)`, hence the source claim `G>1/100` for that fixed canonical square. This remains an **author certificate**, not an independent C2/Sol acceptance.

## Previously unpublished local packet, compared with PR88

`axis_wedge_extension.md`, `audit_axis_wedge.py`, `audit_axis_wedge_certificate.json`, and `audit_axis_wedge_stdout.txt` publish the earlier local packet after scope correction.

Its matched-Schur axis statement is now explicitly classified as a corollary/specialization of PR88's more general reviewed three-actual-coordinate indefinite-rank-two theorem; it is not claimed as a separate new main theorem. Its quantitative complete-Fisher lower bound is retained.

The genuinely additional author result is the full-event continuity extension away from the matched surface. For the exact rank-two endpoint family specified in `axis_wedge_extension.md`, it proves continuous legal regions containing:

- common-line rank-three directions with `|q|<=3/100`, with `G>3/100`;
- zero-intersection rank-four directions with `0<=t_2<=1/10`, with `G>3/100`;
- `|q|<=1/5000`, `0<=t_2<=1/10`, with `G>1/100`;
- `|q|<=1/1000`, `0<=t_2<=1/20`, with `G>3/50`.

These bounds use all complete events through exact diagonal-transfer identities or finite Möbius variation. They do not settle strongly mismatched middle chords and are not counterexamples.

## Files and current verdicts

| File/object | Status |
|---|---|
| `pr86_evidence_repair.md` and full-square output | publication repair; author execution, PENDING_SERVER_REVIEW |
| `axis_wedge_extension.md` matched axis | reviewed PR88 theorem specialization plus new quantitative author bound |
| rank3/rank4 axis-to-wedge regions | PROVED by author, PENDING_REVIEW |
| strong-correlated middle investigation | IN PROGRESS in this successor; unrestricted target remains INCOMPLETE |
| entropy counterexample | none |
| method counterexample | PR62-style endpoint-law mixture bridge remains disproved only as a method |
| novelty/priority | NOT ASSESSED |

## Reproduction

From this directory, without Python `-O`:

```sh
python certify_full_square.py
python audit_axis_wedge.py
```

Both scripts use exact SymPy determinants and standard-library rational logarithm enclosures with written `atanh` tails. No random scan, omitted rare event, numerical probability floor, spectral entropy, L-affine path, or quantum entropy is used.

The upload of this checkpoint is not the end of the task. Subsequent commits in the same PR investigate strong-correlated, substantially Schur-mismatched rank-two endpoint chords in the full-rank middle, separated from the already safe matched-Schur, small-angle and dilute regions.
