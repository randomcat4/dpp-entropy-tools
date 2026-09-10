# Review-contract addendum for later author files

State: **PENDING_REVIEW / NOT COVERED BY ANY EARLIER FREEZE.**

Any reviewer binding a head that contains this file should add the following two units to `review_contract.md`.

## U9 — reverse audit corrections

Read `author_self_audit.md` and verify independently:

1. the nonnormal contraction
   \[
   \|B_xA_t\|_2\le
   \sqrt{\|B_xA_t\|_1\|B_xA_t\|_\infty}<1;
   \]
2. positivity of the exact likelihood ratio selects the real trace-log branch;
3. repeated walk vertices are handled on their distinct support and adjacent repeats vanish because both the diagonal edge and its parameter derivative are zero;
4. the order of limits is fixed walk length, displacement sum, volume limit, and only then the walk-length sum.

The self-audit is author evidence only and must not be counted as an independent opinion.

## U10 — `C^infinity` response corollary

Audit `smoothness_extension.md`. For each arbitrary but fixed integer `r`, reproduce:

```text
|partial_t^r p_{J,t}(x)| <= p_{J,t}(x) K_r |J|^r,
|partial_t^r C_{m,Lambda}(t)| <= B_r m^(2r) rho^(m-r),
rho<1.
```

Check local uniform thermodynamic passage through order `r`, and confirm the conclusion is exactly `C^infinity` on the real interval. Do not promote the result to real/complex analyticity: the packet supplies no uniform factorial radius in `r`.

A review that freezes an earlier head may ignore U9--U10 but must say so explicitly. No prior verdict transfers automatically.