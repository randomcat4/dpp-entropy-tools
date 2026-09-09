# Fresh FIRST reviewer checker

This directory is owned by the fresh nonauthor FIRST reviewer for PR57.

The checker source is `check_r0_first.py`.  It expects a candidate root
containing `inputs/`, `outputs/author01/`, `implementation/`, and
`author_proof.md`.

Root should run it under the existing arithmetic guard, with one thread and
the shared absolute deadline:

```bash
python research/C2/r0_independent52/review_first/check_r0_first.py \
  --candidate-root "$CANDIDATE_ROOT" \
  --out research/C2/r0_independent52/review_first/run01 \
  --deadline-epoch "$C2_ABSOLUTE_DEADLINE_EPOCH"
```

The script writes checkpoints before determinant and Q-transform work and
finishes by writing `RESULT.json` with a scoped CORRECT/FAIL status.
