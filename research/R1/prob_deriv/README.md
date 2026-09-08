# R1 probability and derivative verifier

This directory contains an independent implementation for the real symmetric
DPP entropy task. It only uses full event probabilities obtained by
inclusion-exclusion from inclusion probabilities `det K_A`.

Run from the repository root:

```bash
python research/R1/prob_deriv/dpp_entropy_derivatives.py
```

The run writes `research/R1/prob_deriv/logs/checks.json` and prints a compact
verification table.
