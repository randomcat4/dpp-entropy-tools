# Rejected interval attempt

The first minimized decimal interval run completed with exit status 0, but its LDL interval implementation is not accepted as a strict enclosure certificate.

Reason: `minimal_w4_certificate.py` computed the reciprocal interval in `d_div_pos` as

```python
recip = (Decimal(1) / b[1], Decimal(1) / b[0])
```

without a local context using `PREC = 90` and directed floor/ceiling rounding. Python therefore used the default Decimal context for those divisions.

The rejected outputs and script are preserved in:

`rejected_interval_attempt_default_reciprocal/`

The corrected rerun keeps the same seven centers and does not redo the earlier full symbolic expansion.
