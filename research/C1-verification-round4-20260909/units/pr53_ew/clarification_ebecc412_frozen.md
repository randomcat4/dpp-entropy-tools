# Frozen scope for PR53 EW clarification closure

Reviewer: `C1 original EW first reviewer`
Role: independent first-review delta closure for the original EW review recommendations.

Frozen comparison:

```text
base: 73cdbd09ad9aa975354a116a01f1e0f4955a8c27
head: ebecc412467939591e018a295a18c49a0a341ce9
prefix: research/I05-DPP-21-20260909/
```

Public-ready source aliases:

- `HEAD_EW`: `source-snapshots/pr53_ebecc412/exponential_wiener_extension.md`, blob `8404d0ec0b36ec70ee2e25b2b7c6539a15aafd1f`
- `HEAD_SOURCES`: `source-snapshots/pr53_ebecc412/sources.md`, blob `31f4cd09eaa99aaff4286b057f624daa884d47e0`
- `PATCH`: `source-snapshots/pr53_ebecc412/clarification_ew_sources.patch`
- `BINDING`: `source-snapshots/pr53_ebecc412/SOURCE_BINDING.json`
- `BASE_EW`: `source-snapshots/pr53_ew_73cdbd09/exponential_wiener_extension.md`
- `BASE_SOURCES`: `source-snapshots/pr53_ew_73cdbd09/sources.md`

This closure reviews only `HEAD_EW` and `HEAD_SOURCES` changes owned by the original EW first reviewer. It does not reopen the full EW proof review, does not inspect any second-review artifact, does not review the FR clarification, and does not edit author/public source.

## Requests frozen for closure

1. EW Section 4 must replace the ambiguous statement around `S_F^{-1}` with the exact block-inverse identity

   ```text
   S_F^{-1}=[M_R^{-1}]_{FF}.
   ```

   The text should also clarify that any opposite-Schur-complement correction is a separate equivalent formula, not an added correction to the `FF` block.

2. EW Section 4 must replace scalar-only Holder convergence wording with a fixed weaker Holder norm argument: choose a fixed exponent below the decay rate, state the norm, explain variation/interpolation convergence, and use Cauchy's formula on nested disks to get Banach holomorphy.

3. `sources.md` must state the Cioletti-Silva role precisely: Theorem 2.1 supplies the Holder spectral gap for exponent in `(0,1)`, Lemma 2.4/Proposition 2.6/Corollary 2.7 supply operator/dual analyticity, the normalized operator is matched using the uniform prior and potential `log(2G_s)`, and the proof uses the Holder result rather than a general Walters-class gap.

4. The clarification must not change EW theorem hypotheses, conclusions, constants, code, output, or unrelated companion files.

## Explicit exclusions

This closure does not certify any new theorem, does not change the `ACCEPTED_SCOPED` EW verdict from the earlier first review, does not address whole-legal-interval concavity, and does not perform arithmetic, formal execution, source editing, or publication.

## Success standard

Each request is marked `CLOSED` or given an exact remaining issue. The scoped verdict is one of `ACCEPTED_SCOPED`, `NEEDS_FIX`, `INCOMPLETE`, or `REFUTED`.
