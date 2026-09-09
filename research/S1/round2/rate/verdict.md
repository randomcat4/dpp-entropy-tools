# Verdict

Status: `CERTIFIED_NEGATIVE_PAIR_GAP`.

For the fixed non-even mixed-direction baseline `S1-R2-B1`,

```text
-3.0348902924818035e-05
<= (h(f_-)+h(f_+))/2 - h(f_0)
<= -7.3460456800473595e-06.
```

This is a strict entropy-rate exclusion of one fixed pair as a positive counterexample.  It evaluates all three symbols `f_-`, `f_0` and `f_+` separately and does not use endpoint equality.

The certificate used six variational extreme-past kernels and an exact/interval rate computation at past length `n=4`.  Since `n=4` already separated zero, no larger entropy window was run.

The result does not solve the full scalar stationary DPP entropy-rate conjecture and does not certify a family theorem for non-even centres or mixed cosine/sine directions.
