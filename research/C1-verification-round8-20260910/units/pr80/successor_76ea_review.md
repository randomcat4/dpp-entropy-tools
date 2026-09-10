# Successor 76ea mathematical review

Scoped verdict: the new analytic identities are correct at source level. The exact Cauchy-slack reserve identity, the one-event square completion, and the fiber-window moment lower bound all check out by ordinary algebra. The successor also changes the `s=9/10` story in the right logical direction: the original ratio-cone does not get certified; it is instead reported as failing on the fixture, while a different fiber-window/moment sufficient bound is proposed. All finite fixture claims remain author evidence pending C2, and the unchanged original `RESULT.md` wording gates remain open until source text is actually repaired.

## Analytic checks

### Exact reserve identity

Status: PASS.

`ADDENDUM_S09_SIGNED_FIBERS.md` lines 46-60 use the exact identity

`x^2/q+x'^2/q'=(x-x')^2/(q+q')+(q'x+qx')^2/[q q'(q+q')]`

for positive `q,q'`. Expanding the right side cancels the cross terms and recovers `x^2/q+x'^2/q'`. Applying this to both `x=u` and `x=y` in the original signed pair kernel gives the stated reserve form

`J=(Delta u)^2 F(q,q',r)+2[(q'u+qu')^2+(q'y+qy')^2]/[q q'(q+q')]`

whenever `Delta u!=0` and `r=Delta y/Delta u`. The coefficient of `F` and the square-reserve coefficient are correct.

The pair-local strictness conditions in lines 64-70 are also correct for an off-diagonal pair after Cauchy slack is exposed: strictness follows from `F>0`, or from either nonzero reserve square.

### One-event square completion and coefficient class

Status: PASS, with the same `s>0` wording repair as the original review.

`ADDENDUM_S09_SIGNED_FIBERS.md` lines 74-88 correctly rewrite

`Phi(u)+4y^2/q+y psi(u)=4(u+y)^2/q+2(u+5y)log q`.

Using `u=-sa+s^2b` and `y=s^2b`, this becomes the displayed expression in lines 80-86. The sign criterion in lines 92-116 is also correct: since `log q` has the same sign as `u=q-1`, the logarithmic term is nonnegative when `u(u+5y)>=0`, equivalently `(a-sb)(a-6sb)>=0` for positive `s`. The equality condition in lines 106-114 is the right pointwise condition under that sign hypothesis.

Minimum repair: line 102 should say `for t!=0` or `for s=t^2>0` before concluding `H''(t)<=0` from `t^2 I''(t)>=0`.

### Fiber-window moment theorem

Status: PASS analytically; finite application pending C2.

`ADDENDUM_FIBER_WINDOW_MOMENT.md` lines 15-31 correctly combine the square completion with `lambda(q)=log(q)/(q-1)` and `z=u(u+5y)`, giving

`C_f=E[4v^2/q+2z lambda(q)]`, where `v=u+y`.

The monotonicity lemma in lines 35-47 is correct: `lambda` is positive and strictly decreasing on `(0,infinity)`. Therefore the endpoint definitions in lines 51-65 give `lambda(q)=c+epsilon` with `|epsilon|<=delta` on the fiber window.

The theorem in lines 67-85 is a valid sufficient lower bound:

`4v^2/q >= 4v^2/q_+`

and

`z lambda(q)=cz+epsilon z >= cz-delta |z|`.

Averaging gives the displayed lower bound. The theorem uses the product-reference block marginal weights on the fixed fiber, matching the accepted complete-law curvature identity; it is not a true-law `p_C(T)q(S,T)` conditional expectation.

Minimum repair: line 145 should carry the same endpoint caveat as above: `t^2 I''>0` implies `H''<0` only for `t!=0`. The fixed application is at `s=9/10`, so the repair is wording for the general statement, not an objection to that point.

## Strictness wording

The successor addenda overstate the status of the original Theorem 4.1 strictness sentence.

`ADDENDUM_S09_SIGNED_FIBERS.md` lines 64-70 correctly explain that, for a particular off-diagonal pair, a nonzero original first line does not necessarily mean the Cauchy lower bound is strict; the mass may sit in the difference-square part. But this does not make the original first-line strictness condition false as a theorem-level sufficient condition. If a positive-mass one-copy atom has `u` or `y` nonzero, the diagonal pair `T=T'` has `Delta u=Delta y=0`, no mixed term, and exact value `J=4(u^2+y^2)/q>0`. All other pairs are nonnegative under the cone hypothesis, so the fiber expectation is strictly positive.

Minimum repair: revise `ADDENDUM_S09_SIGNED_FIBERS.md` line 5 and lines 64-70, and `ADDENDUM_FIBER_WINDOW_MOMENT.md` line 147, to distinguish the valid diagonal first-line witness from the off-diagonal Cauchy-reserve strictness test. The addenda should say they clarify or sharpen the strictness rationale, not that the original first-line sufficient condition was erroneous.

## Ratio-cone coverage at s=9/10

Analytic status: the successor no longer claims the original ratio-cone covers the PR58 `s=9/10` fixture. Instead, `ADDENDUM_S09_SIGNED_FIBERS.md` lines 23-42 reports a finite falsification: if independently verified, the PR80 ratio-cone fails on both conditional orientations for that fixture. That is a method failure, not an entropy counterexample.

Evidence status: pending C2. This FIRST review did not verify the embedded matrices against PR58, did not rerun the scripts, and did not independently certify the claimed 75/66 bad-pair counts or worst negative enclosures. The fixture identity in line 25 needs either an immutable PR58 source binding or a C2 check that explicitly treats the embedded matrices in `verify_s09_signed_fibers.py` lines 10-27 as the frozen fixture under review.

## Fiber-window application at s=9/10

Analytic status: the fiber-window/moment theorem is a valid sufficient theorem and can cover a fixed point if every fixed-side fiber has a positive certified lower endpoint.

Evidence status: pending C2. `ADDENDUM_FIBER_WINDOW_MOMENT.md` lines 99-141 and the two output files report positive author lower endpoints, but those finite signs are not accepted by this source-only FIRST review. If C2 confirms them, the new mechanism covers the fixed `s=9/10` point by fiber averages even though eventwise positivity and the original ratio-cone fail. Until then, the status is author finite certificate / pending independent verification.

The reference in `ADDENDUM_S09_SIGNED_FIBERS.md` line 146 to an accepted PR76 complete-curvature enclosure is not part of this frozen successor input. This review does not use it as a premise.

## Future C2 contract

This is a future suggestion only, not authorization to start C2 and not an expansion of any PR70 or PR77 budget. Every finite or numerical claim should be handed to a fresh independent C2 with this bounded contract:

- Inputs: the frozen mathematical identities, the original PR80 formula for `F`, the accepted complete-law identity, and the literal embedded rational fixture from the successor source. If the claim is that this embedded fixture is exactly the PR58 fixture, C2 also needs an immutable PR58 fixture binding.
- Independence rule: C2 must independently reconstruct the events, coefficients, block marginal weights, fiber moments, strict log intervals, and signs from the frozen mathematics and literal rational data. The author scripts and output files may be compared against the independent reconstruction, but they must not be imported, executed, or treated as a computational source for the independent certificate.
- Ratio-cone failure outputs: all fixed-left and fixed-right conditional pairs with `Delta u!=0`, rigorous enclosures for `F`, the full negative-pair count, and at least one failing witness per orientation. PASS for ratio-cone failure only if the independent reconstruction certifies a negative upper endpoint in each claimed orientation.
- Fiber-window outputs: for every fixed-side fiber, independently reconstructed `q_-`, `q_+`, `E[v^2]`, `E[z]`, `E|z|`, rigorous endpoint enclosures for `lambda(q_-)` and `lambda(q_+)`, the certified lower endpoint in the theorem, and the normalization/cancellation checks used by the source.
- Strictness outputs: separate strictness gates for positive fiber-window lower endpoints and for any exact diagonal or reserve-square witness.
- Author-script comparison: transcript consistency for the saved output files may be classified statically, or reproduced later under separate explicit authorization. It is not a prerequisite for C2 mathematical acceptance.
- Non-goals: no author-module execution as independent evidence, no whole-chord computation, no PR70/77 budget expansion, no formalization, and no inheritance from old PR58 PASS output.

## Final successor status

- Signed-fiber exact reserve identity: PROVED at source level.
- One-event square completion and coefficient sign family: PROVED at source level, with `s>0` wording required for `H''`.
- Fiber-window moment theorem: PROVED as an analytic sufficient criterion.
- Original PR80 ratio-cone coverage of `s=9/10`: not proved; successor finite evidence instead claims the cone fails on the fixture, pending C2.
- New fiber-window coverage of `s=9/10`: author finite certificate only; pending C2.
- General whole chord: still INCOMPLETE.
- Novelty/formal status: not assessed.
