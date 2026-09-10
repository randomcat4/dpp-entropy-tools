# Scope 1a32 document delta review

Scoped verdict: the 1a32 document revision closes the source-wording and evidence-packaging gates identified in my earlier PR80 FIRST/successor reports. It does not close any finite arithmetic, pair-count, sign, fixture-identity, or formal-evidence gate. All new finite claims remain author finite claims pending future independent reconstruction.

## Gates closed by source text

### Original RESULT wording

`RESULT.md` now fixes the main ratio-cone statement defects:

- Lines 153-159 write the lower-kernel relation as `J >= Q = (Delta u)^2 F(q,q',r)`, closing the earlier `Q >= ...` notation issue.
- Lines 167-171 state the theorem at `s=t^2>0` and explicitly derive `H''(t)<=0` using `t!=0`.
- Line 171 gives the correct diagonal strictness witness: a positive-mass one-copy atom with nonzero `u` or `y` yields the diagonal pair `T=T'` with `J=4(u^2+y^2)/q>0`; pair-local reserve-square strictness is kept separate.
- Lines 181-191 add `0<q_-<=q_+`, restrict the conclusion to physical parameters with `t^2` in the interval and `t!=0`, and state concavity only on connected `t`-intervals covered by the hypotheses.

These edits close the prior source wording gates for `s>0`, positive q windows, connected `t`-bands, diagonal strictness, off-diagonal reserve separation, and `J >= Q = ...`.

### Signed-fiber addendum strictness

`ADDENDUM_S09_SIGNED_FIBERS.md` now separates the two strictness ideas correctly:

- Line 5 says the addendum clarifies pair-local strictness and preserves the original theorem-level diagonal witness.
- Lines 44-70 prove the exact reserve identity and describe off-diagonal pair-local strictness without replacing the diagonal witness.
- Lines 100-102 add `s=t^2>0` before concluding `H''(t)<=0` from `t^2 I''(t)>=0`.
- Line 160 states the status as pair-local strictness together with the diagonal witness.

This closes the earlier overstatement that the original first-line strictness condition was erroneous. The source now says the correct thing: off-diagonal Cauchy-reserve strictness is a sharper pair-local test, while the theorem-level diagonal witness remains valid under the cone hypothesis.

### Fiber-window addendum wording

`ADDENDUM_FIBER_WINDOW_MOMENT.md` now closes the normalization and endpoint wording issues:

- Line 19 explicitly uses product-reference block marginal weights `p_C` or `p_A`, and says these are not the q-reweighted conditional law of the full DPP.
- Lines 51-53 retain the positive q-window hypothesis.
- Line 145 states the strict curvature conclusion at `s=t^2>0` and uses `t!=0`.
- Line 147 removes the earlier "old erroneous" framing and says pair-local equality is governed by the exact identities while the original ratio-cone theorem keeps its valid diagonal witness.

The analytic fiber-window/moment theorem remains source-level correct, and its general statement now has the needed scope words.

### README evidence packaging

The new README closes the code/output packaging objections at document level:

- Lines 7-11 state that both output files are edited author summaries, not literal raw stdout, and explicitly withdraw the saved "lower/upper" label as an interval claim for the window columns. The `hi` value is now only a companion conservative value; only `lo` is relevant to the proposed positivity certificate.
- Line 13 gives an immutable PR58 fixture link and distinguishes the literal matrices embedded in the author script from the still-pending proof that they equal the cited fixture.
- Lines 13-15 say that pair counts, signs, window-moment bounds, fixture equality, and all finite claims still require independent source/arithmetic binding; no old global-curvature certificate verifies the new per-pair or per-fiber claims.
- Line 15 states that no new C2 contract is supplied, no author module is an independent implementation, and no whole-chord job, PR70/77 budget expansion, formal check, or novelty claim follows.

This closes the earlier "output transcript" objection as a disclosure problem. It does not transform the unchanged scripts or edited summaries into independent computational evidence.

## Gates still open

The following remain pending exactly as before:

- The 75/66 negative ratio-pair counts in `ADDENDUM_S09_SIGNED_FIBERS.md` lines 33-40.
- The four negative one-event integrands in lines 118-128.
- The 16 positive signed conditional fiber averages and global point value in lines 130-146.
- The positive fiber-window lower endpoints in `ADDENDUM_FIBER_WINDOW_MOMENT.md` lines 99-141.
- The equality of the embedded rational matrices to the cited PR58 fixture.
- Any use of the unbound PR76 consistency sentence as evidence for new per-pair or per-fiber claims.
- Any general dense correlated rank-two whole-chord concavity claim.
- Any novelty or formal-verification claim.

`RESULT.md` lines 217-233 still conservatively leave the original ratio-cone coverage question pending in the initial packet. The successor addendum supplies author finite evidence that the ratio cone fails on the fixture, but that finite evidence is still not independently accepted.

## Final 1a32 status

- Source-wording repairs from the original FIRST review: CLOSED.
- Successor strictness-overstatement repair: CLOSED.
- Product-reference weight clarification: CLOSED.
- Edited-summary and `hi`-column disclosure: CLOSED as documentation; not computational evidence.
- Immutable PR58 fixture provenance disclosure: CLOSED as a source link; fixture equality still pending independent binding.
- New finite claims: PENDING.
- Author scripts/output as independent certificates: NOT ACCEPTED.
- Whole chord, formal status, novelty: INCOMPLETE / not assessed.
