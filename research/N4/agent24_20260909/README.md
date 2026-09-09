# Agent 24: moving frames and correlated multi-ring chords

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.
Issue lineage: repository issue #21.  This work does not duplicate issue #52.

## Final status

**PROVED (scoped author theorem) / INCOMPLETE (general target).**

The scoped theorem is `moving_rank1_theorem.md`: every true affine midpoint of
two real rank-one DPP kernels satisfies configuration-entropy midpoint
concavity, strictly unless the kernels coincide.  Both the physical direction
and nonzero eigenvalue may move.  A common independent-bit-flip operation
produces explicit strict interior affine chords, with a quantitative
Fannes--Audenaert margin certificate.  The theorem applies in all dimensions,
including the requested `n=4,5,6` range.

No strict real counterexample was found.  The unrestricted real problem is not
claimed solved.

## Two structural routes

- `moving_rank1_theorem.md` gives the completed moving-frame route.  Its bridge
  transfers empty/singleton mass in the average endpoint law to the pair atoms
  opened by the rank-two matrix midpoint, and proves entropy increases along
  the transfer.
- `multiring_fixture.md` freezes a different dense `3+3` signed-triangle route.
  It has strong internal correlations, a dense rank-two coupling, exact
  legality, all 64 complete-event polynomials, and motivated finite probes.
  The positive cardinality-three layer is compensated by the other layers.
  Continuous sign certification remains delegated and is not presumed.

`prior_art.md` separates these routes from accepted R2/A2/PR43/W3 scope and
records the primary literature checked.  `failure_ledger.md` records stopped
or non-closing mechanisms without reclassifying them as counterexamples.

## Reproduction

```bash
python research/N4/agent24_20260909/code/verify_rank1_midpoint.py
python research/N4/agent24_20260909/code/probe_multiring_fixture.py
```

Expected outputs are stored verbatim under `output/`.

The first program uses exact SymPy rationals for all 64 atoms and for the
bit-flip channel identity; only the displayed entropy values use high
precision.  Its strict lifted sign is decided by the explicit continuity
bound in the proof.  The second program uses exact rationals for the 64 atom
polynomials, derivatives, normalization, legality, and endpoint bracket; its
logarithmic curvature values are 110-digit diagnostics only.

## Review boundary

All new proofs are author proofs pending independent review.  Novelty is not
certified.  The repository's accepted statements are used only within their
recorded scopes; old issue status labels and finite search summaries are not
used as current mathematical verdicts.
