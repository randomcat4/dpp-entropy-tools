# S1 closeout dispositions for the remaining author backlog

Status: **STOPPED_HANDOFF_READY**.

This report freezes the remaining S1 author backlog at the exact heads listed
below.  It reuses existing public FIRST/SECOND records where they already exist,
does not repeat accepted reviews, and separates analytic implications from
author-only finite certificates.  No checker or certificate program was run.

## Disposition table

| PR | Frozen author head | Disposition | Exact scope |
|---:|---|---|---|
| 124 | `344723af6affab240c9f87c395d4e8c1b7b19f6d` | **PASS_SCOPED / ALREADY_MAIN** | Reuse PR127 for the pointwise-resolvent method obstruction and PR132 plus the public S3 SECOND for the equal-strength and punctured small-edge positive theorems.  The obstruction is not an entropy counterexample.  Merged as `3729264b95208a92accd08a01a9b37ce41bb17f0`. |
| 120 | `83b89e8b9b4c542e5d1cd8b38b64b7ff2449ad41` | **MIXED: SUPERSEDED + EVIDENCE_INSUFFICIENT** | The equal-strength theorem is the same theorem already accepted from PR124 and is counted once; the pointwise obstruction is also superseded by PR124/PR127.  The later compact unequal-strength middle has a correct static reduction from the six-dimensional form and its Schur core to complete Shannon curvature, but its 1024-box interval/Gershgorin margin is author evidence only.  Without an independent finite audit, that new compact-middle theorem is not importable. |
| 115 | `dd52c147efc4a0908b8e9545628f031d1be97027` | **SUPERSEDED** | The unfinished Poisson/Neumann true-rate route and its `n=6,7,8` author certificates are replaced by PR136 at `39098dac760cea2d27f2955bed31f80c87913810`.  PR137 accepts the PR136 analytic interface, while the PR136 theorem remains conditional on its separate S2 finite-evidence gate.  Supersession does not promote the older PR115 finite signs. |
| 110 | `142420531ed7a41d1abc4c8040c6485bf21b1bc7` | **SUPERSEDED** | Its local corrected-concavity theorem is contained in the accepted arbitrary-strict-`A_0` theorem of PR117 at `70d69bf5c47282c953010518ff264cb2a7a09bf9`, reviewed in PR126 and merged as `2f66f1a67af9e23bf77ec04f1d6f716947072394`.  The Fang--Shin and BFG source conditions were spot-checked and revealed no contradiction, but no duplicate theorem import is needed. |
| 106 | `a175bf1d1b5a8c16537aa4924731de426dfc882d` | **MIXED: SUPERSEDED + PASS_SCOPED** | The `A_p`, `p>=1`, local-concavity theorem is strictly contained in accepted PR117 and is superseded.  A fresh bounded reconstruction accepts the separate centered full-conditional Fisher expansion for `p>=1/2`, including its matching lower bound, but not any nearby-curvature or local-concavity conclusion below `p=1`. |
| 104 | `d980dbb04840bd21e6c62cf88ffd45a9b0d1b4f8` | **PASS_SCOPED_ANALYTIC** | The actual fixed-ratio failure of the old parallel criterion, the common-leaf-diagonal sufficient criterion, and the compact-uniform double-boundary wedge are correct.  The shared-variable minimization gives the stated coefficient, the strictness argument retains the dropped nonnegative edge squares, and the limiting gap is the positive trapezoid gap for `log`.  The saved rational witness, Sylvester intervals, and displayed decimal margins remain author-only finite evidence and are excluded. |
| 94 | `a9db9f98dc6dac766dd9b214f056ee9b30109b23` | **MIXED: PASS_SCOPED + SUPERSEDED + EVIDENCE_INSUFFICIENT** | Reuse PR100 and the public S3 SECOND: the exact local-channel theorem and actual-coordinate mode-expansion construction pass structurally.  `WHOLE_CHORD.md` is superseded by accepted PR95 at `54d9803b29f73669b9028e3519d17493e1b81be3`, with S1 PR99 and S2 PR109.  The explicit PR94 3+3 rational/64-event arithmetic remains pending its own finite audit. |
| 66 | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | **SUPERSEDED** | Do not retry the invalid Dobrushin import.  Its earliest load-bearing defect is that the proved polynomial interval estimate does not establish class `A1`'s exponential support-cardinality summability, while class `A2` requires a controlled null-state interaction representation that the submitted telescope does not provide.  The theorem is replaced by the DPP-specific finite-response proof in accepted PR82 at `290a84064eaae2e857d637f58531e95f4ca3cb3b`, merged as `09e09086c0dc8b30d5859a7e1e2cba86623d2631`. |
| 97 | `03e0313a5802bfe52fba18fa01bf5ad97ab20d2f` | **MIXED: PASS_SCOPED_ANALYTIC_INTERFACE + EVIDENCE_INSUFFICIENT** | PR86 predecessor analytic units retain their existing scoped FIRST from PR90; the added missing certificate repairs publication provenance but is not independent arithmetic.  The matched-axis unit is a specialization of accepted PR88.  For the new wedge, strong chord, and strength-family units, the complete-law identities, exact endpoint-factor cancellations, total-variation transfers, Fisher lower bounds, and implications from the stated interval bounds are analytically sound.  The decisive base entropy/log bounds and 32/1024-box acceleration margins are author certificates only, so none of the new quantitative theorems is importable before an independent S2 audit. |
| 112 | `2ea07741114aa7cd20210dfc84becda378381e7b` | **MIXED: PASS_SCOPED + SUPERSEDED + EVIDENCE_INSUFFICIENT** | The already accepted `explicit_rate_interval.md` is reused from PR134 and not re-reviewed.  The corrected entrypoints and `interval_proof.md` correctly withdraw the unsupported wide interval.  The four `dependencies/pr91/` files are blob-identical copies of canonical accepted PR91 and are superseded as duplicate sources.  Precise state-cone and entropy-shape lemmas survive as described below; neither signs the full physical curvature. |

## PR104 analytic reconstruction

The PR104 positive result is the only new author theorem in this closeout that
does not depend on a finite certificate.  For the common horizontal variable,
minimizing the two retained completed squares gives

`H_A (u+v)^2`,

and combining it with the two vertical endpoint residuals gives exactly

`C_A=[H_A(beta_plus+beta_minus)+beta_plus*beta_minus]/[4H_A+beta_plus+beta_minus]`.

Thus `C_A>J/(32AB)` makes the retained `(u,v)` quadratic positive definite.
The marginal block forces the common diagonal directions to vanish at equality,
and the remaining completed edge squares then force every corner coordinate to
vanish.  Along `B=epsilon`, `q=rho*epsilon`, the old parallel coefficient stays
finite while `J/(32AB)` grows logarithmically.  The strengthened gap converges
to a positive interior edge coefficient plus the strict concave-trapezoid gap
of `log` on `[rho,rho+1]`.  The expansions are joint and uniform on compact
subsets of `a in (0,1)` and `rho in (0,infinity)`.

This proves only a method obstruction for the old criterion and a positive
complete-Shannon wedge for the repaired criterion.  It proves no entropy
counterexample and no universal half-leaf theorem.

## PR106 centered Fisher reconstruction

The standalone theorem in `center_quartic_p_half.md` is
**PASS_SCOPED_ANALYTIC** at the frozen PR106 head.  Its exact accepted scope is:

`h(c+t g)=h(c)-(1/2) I_s(0)t^4+o(t^4)`

for real half-period-even/odd `c,g in A_p`, `p>=1/2`, at a strict center,
where `I_s(0)` is the full emitted-state, full-future conditional Fisher
information for `s=t^2`.  The accepted PR53 matching floor gives the stated
lower bound on `(1/2)I_s(0)`.

The reconstruction closes as follows.  The single direct-sum Fang--Shin
inverse envelope is uniform over all complete events.  Squaring its two
conditional legs doubles the Fourier moment, so `2p>=1` gives summable
variations for `ell_s` and its first `s` derivative.  The explicit BFG
defective-renewal estimate then supplies `R_s:V_0->C` and continuous one-step
response.  For `U_s=partial_s ell_s`, normalization gives `L_s U_s=0` and
`nu_s U_s=0`.  Therefore `R_0U_0=U_0`, and the exact deficit identity yields

`D'(s)/s -> nu_0(U_0^2)=I_s(0)`.

Integration gives the claimed coefficient.  No second Poisson inverse is
used.  The result gives no control of `D''(s)` for `s>0` and hence no local
concavity theorem in `1/2<=p<1`.

## PR112 file-level theory map

- `README.md` and `RESULT.md`: **PASS_SCOPED** as correction/scope records.
  They withdraw, rather than preserve as pending, the unsupported
  `[49/40,51/40]` certificate and retire the known-failing companion.
- `interval_proof.md`: **EVIDENCE_INSUFFICIENT / WITHDRAWN** for the former
  wide-interval theorem.  The earliest load-bearing failure is the absence of
  the advertised production program, certificate, original execution record,
  and separate checker; the remaining accessible checker also has the recorded
  complete-event label discrepancy.  No reconstruction can certify the old
  global residual suprema from the frozen public inputs alone.
- `dependencies/pr91/{proof,coding_and_fisher,curvature_certificate,post_handoff_cancellation}.md`:
  **SUPERSEDED_DUPLICATE**.  Their blob hashes exactly equal the canonical PR91
  files at accepted head `c7a072ec4eea0c5b0f445bca5796873a9e234948`,
  merged as `9043d8e2b763c974ff430b80505bbad5e79bf6c4`.
- `lifted_cone.md` Sections 1--5: **PASS_SCOPED_ANALYTIC** for the corrected
  determinant lift, exact convex hull, perspective preservation of state
  concavity, existence of the bounded entropy corrector, its state-Hessian
  lower bound `-D_Z^2 U_s >= I/8`, and the exact isolation of the still-unsigned
  mixed/stationary-law response.  A bounded reconstruction of the lift gives
  the stated numerators for `x',y',r',d'`, and the four two-cell score
  observables invert to the state coordinates with the claimed finite norm.
  These are state-variable statements, not a sign theorem for physical `h_tt`.
- `lifted_cone.md` Section 6 exact rational witnesses:
  **EVIDENCE_INSUFFICIENT** as frozen-source claims because the cited successful
  exact-lift checker is not present at the corrected head.  They remain method
  counterexamples only in any event.
- `entropy_shape.md`: **PASS_SCOPED_ANALYTIC_WITH_TEXT_FIX_REQUIRED** for the
  invariant reachable shape, the exact complete-table determinant
  `g_++g_---g_+-g_-+=-(q-z)^2`, the bound
  `partial_s B_s<-3s/4`, the fixed-lift Fisher and state-Hessian budgets, and
  the final inequality with the explicit unsolved `Gamma(t)`.  Its displayed
  `g_ac` line swaps the `a,c` labels relative to the corrected lift in
  `lifted_cone.md`; all load-bearing uses there sum over all four branches and
  are invariant under that branch-label permutation, so the stated bounds
  survive, but the line must be corrected before selective integration.

PR136 supersedes the attempted macroscopic true-rate route with a different
analytic/certificate interface, but it does not retroactively validate the
withdrawn PR112 interval evidence.  The surviving PR112 lemmas remain partial
method information only.

## Unreviewed blockers that must not enter a new main

- PR120 `compact_unequal_middle/`: independent exact interval/Gershgorin audit.
- PR136 finite Chebyshev-node evidence, on which the full PR136 theorem still depends.
- PR104 saved rational witness and numerical Sylvester/log intervals; these are unnecessary for the accepted analytic wedge.
- PR94 explicit 3+3 finite arithmetic.
- PR97 full-square repair arithmetic and every new quantitative wedge/chord/family margin.
- PR112's withdrawn wide interval and absent production evidence; Section 6
  rational method witnesses are also not source-closed at the corrected head.

No novelty or priority review, formal verification, SECOND, merge, or computation
is included here.  PR116 is intentionally excluded.  S3 remains the sole main
integrator; selective integration must preserve every scope boundary above.
