# PR53 EW clarification closure review

Reviewer: `C1 original EW first reviewer`
Scope: bounded delta closure for `73cdbd09ad9aa975354a116a01f1e0f4955a8c27 -> ebecc412467939591e018a295a18c49a0a341ce9`.
Frozen scope: `clarification_ebecc412_frozen.md`.

## Verdict

Scoped verdict: `ACCEPTED_SCOPED`.

All three assigned EW-owned clarification items are closed by the `ebecc412` clarification. I found no theorem-hypothesis, theorem-conclusion, constant, code, output, or companion-file scope change in the EW-owned delta. This is a clarification closure only; it does not reopen or extend the earlier EW theorem review.

| Request | Status | Disposition |
| --- | --- | --- |
| Exact `S_F^{-1}=[M_R^{-1}]_{FF}` identity | `CLOSED` | `HEAD_EW` line 209 states the exact identity and separates the opposite Schur correction formula. |
| Fixed weaker Holder norm and Banach holomorphy | `CLOSED` | `HEAD_EW` line 220 now chooses `0<b<min(a',1)`, defines `||.||_b`, gives variation/interpolation convergence, and applies Cauchy's formula on nested disks. |
| Cioletti-Silva source role restricted to Holder theorem | `CLOSED` | `HEAD_SOURCES` line 35 names Theorem 2.1, Lemma 2.4, Proposition 2.6, Corollary 2.7, the uniform-prior `log(2G_s)` match, and excludes a general Walters-class gap claim. |
| No theorem/data/code drift | `CLOSED` | The EW/sources patch changes only the clarification lines above; `BINDING` marks code/output and unrelated companions unchanged. |

## Patch Check

`PATCH` lines 4-20 replace the old EW Section 4 wording. The first hunk leaves the displayed Schur identity itself unchanged (`HEAD_EW` lines 196-207) and replaces the ambiguous prose with:

```text
S_F^{-1}=[M_R^{-1}]_{FF}
```

plus the clarification that restricting rows/columns cannot increase the weighted Schur norm and that the opposite Schur formula gives a separate correction representation (`HEAD_EW` line 209). This exactly closes the original line-209 recommendation. It adds no new assumption; it only states the standard block inverse identity supporting the already accepted estimate.

The second EW hunk in `PATCH` lines 13-20 replaces the scalar Holder-limit sentence. `HEAD_EW` line 220 now fixes a weaker Holder exponent `0<b<min(a',1)`, defines

```text
||F||_b=||F||_infinity+sup_{m>=0} exp(bm) var_m(F),
```

uses shorter-truncation variation bounds plus interpolation to get `||q_{r,z}-q_z||_b<=C exp(-(a'-b)r)`, and applies Cauchy's formula on `|z|<=r_1<r_2<r_0` for derivative convergence in the same norm. This closes the original Holder/Banach-holomorphy recommendation without changing the theorem statement or adding a theorem hypothesis.

`HEAD_EW` lines 222-231 remain the same mathematical conclusion as before: strict real-slice positivity, normalized Holder `g`-function, evenness in `t`, holomorphy in `s=t^2`, and inheritance of the analytic input used by the finite-range proof.

## Source Role Check

`PATCH` lines 23-31 replace only the Cioletti-Silva role sentence in `sources.md`. The final text (`HEAD_SOURCES` lines 33-35) now says:

- Theorem 2.1 supplies the simple maximal eigenvalue and spectral gap for Holder potentials with exponent in `(0,1)`.
- Lemma 2.4, Proposition 2.6, and Corollary 2.7 give the operator/dual analyticity framework.
- With the uniform prior on `{0,1}` and potential `log(2G_s)`, the source's integral operator equals the normalized sum operator used in the proof.
- The proof uses the Holder result, not a gap for the general Walters class.
- A contour Riesz projection around the simple isolated eigenvalue gives the holomorphic normalized eigenmeasure.

This matches the primary reference previously inspected for the EW first review: [Cioletti-Silva, arXiv:1511.01579](https://arxiv.org/html/1511.01579). Walters remains a separate bibliography/source-role citation in `HEAD_SOURCES` lines 29-31, not a substitute for the directly checked Holder theorem.

## No Drift

The patch does not touch EW theorem hypotheses or constants: the theorem statement remains in `HEAD_EW` lines 31-43, with the same `alpha_k=gamma^2/[8mu^2(1-mu^2)]` from lines 24-29. The local completion step and curvature constant remain in `HEAD_EW` lines 233-262.

`BINDING` lines 3-31 show that the full source delta contains three changed files, but only `exponential_wiener_extension.md` and `sources.md` are owned by this EW closure; `finite_range_local_theorem.md` is assigned to the original FR first reviewer. `BINDING` lines 33-99 show all code, output, README, RESULT, verification, and original bridge proof companions unchanged from the prior EW-reviewed head. `BINDING` line 2 records `all_code_output_unchanged: true`, and line 101 records exact repository delta verification.

No arithmetic, code execution, Lean check, or new source audit was run for this closure.

## Remaining Scope

No remaining issue for the EW-owned clarification delta. The broader whole-legal-interval problem remains outside this closure and remains open exactly as in the earlier EW review.
