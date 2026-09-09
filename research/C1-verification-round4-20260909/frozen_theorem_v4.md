# Frozen exponential-Wiener first-review contract v4

This is the newly assigned PR53 EW FIRST unit. The original bridge packet,
Theorem FR first review and PR54 Section 5 closure remain completed records.
C3 is independently second-reviewing FR and will own EW's second after
this first passes. C1 does not repeat FR first or inspect C3 second artifacts.

## Exact source object

Base `abdd660a6c7761c7a8a53cb8671b4d2543530a5c` to frozen head
`73cdbd09ad9aa975354a116a01f1e0f4955a8c27`.
All seven changed/added files under
[the immutable source directory](https://github.com/randomcat4/dpp-entropy-tools/tree/73cdbd09ad9aa975354a116a01f1e0f4955a8c27/research/I05-DPP-21-20260909)
are in scope:

- exponential_wiener_extension.md (268 lines)
- RESULT.md
- verification.md
- code/check_rudin_shapiro_example.py
- output/rudin_shapiro_exact.json
- README.md delta
- sources.md delta

All seven full files were downloaded as immutable Git blobs and hash-checked.
Their individual blob bindings are in units/pr53_ew/SOURCE_BINDING.json.
The original 473-line FR file is unchanged, with blob
`c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263`; it is consulted only as
author source for the exact inherited proof steps. No prior first report
is used as mathematical evidence by the EW reviewer.

## Frozen theorem and audit questions

For beta>0, real c,g in A_beta have exponentially weighted summable Fourier
coefficients. Assume c is half-period invariant, g is half-period
anti-invariant and nonzero, and `delta<=c<=1-delta` for delta>0. No norm
smallness or mean-one-half assumption is added. For any odd k with
`g_hat(k)!=0`, let `mu=integral c` and
`alpha_k=|g_hat(k)|^4/[8 mu^2(1-mu^2)]`.

Theorem EW claims an epsilon>0 such that the true entropy rate satisfies
concavity of `h(c+t g)+alpha_k t^4` on [-epsilon,epsilon], hence strict local
concavity. Verify all hypotheses, constants and the literal companion claims.

The new load-bearing steps are uniform band truncation and the weighted
inverse bound, including the linear-in-W bound and exponentially small
weighted tail; one common complex Neumann disk; correct near/far Schur
identities and direct Fourier-tail terms; uniform remote-condition decay;
holomorphy in a fixed Hölder space; and valid inheritance of RPF, rate-chain
formula, normalized first-derivative cancellation and matching/KL curvature.
No event deletion or volume derivative interchange is allowed.

The exact checker/output are source artifacts for example constants only.
Inspect their consistency and claimed coverage; do not treat author output
as a fresh C1 execution or an entropy theorem certificate. Verify sources.md
against precise primary hypotheses, including the Hölder versus broader
Walters-class spectral-gap distinction.

## Roles, evidence and stopping boundary

Reuse the eligible original PR53 non-author GPT-5.5/xhigh first context in a
separate EW output directory. It may not spawn descendants, edit author
sources or publish. It returns per-claim CORRECT or CRITICAL_GAPS and a
scoped verdict ACCEPTED_SCOPED / NEEDS_FIX / INCOMPLETE / REFUTED. It may
not silently add or reinterpret hypotheses. All mathematical failures and
version boundaries must remain visible.

This is source review only. No new arithmetic job is initially needed.
Any necessary tiny check requires an explicit exact bounded contract first:
input, algorithm/error criterion, one thread, at most 8 GiB, 600-second
initial timeout and stopping condition. C2 retains heavy computation and
issue52; no duplicate PR54 appendix work or second review is started.
There is no new formal or novelty certification. The entire legal interval
and arbitrary measurable-symbol problem remain OPEN.
