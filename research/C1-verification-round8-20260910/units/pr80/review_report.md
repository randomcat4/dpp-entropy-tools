# PR80 FIRST source review

Scoped verdict: the signed conditional-pair decomposition and the DPP-constrained ratio-cone sufficient criterion are mathematically sound at the intended source-only level, provided the source makes the small quantifier repairs listed below. I found no algebraic sign or coefficient error in Theorem 2.1, no flaw in the free-vector PSD obstruction, and no improper upgrade to general whole-chord concavity. PR58 `s=9/10` coverage remains unproved, as the PR80 source itself says.

## Source-level checks

### Theorem 2.1: exact signed conditional-pair decomposition

Status: source-level PASS.

The accepted premises allow PR80 to fix a left configuration and work under `nu=p_C`: the accepted addendum proves `E_nu a=E_nu b=0`, hence `E_nu u=E_nu y=0`. PR80 invokes exactly this at `source-snapshots/pr80/research/I05-29-rank2-signed-pairing-20260910/RESULT.md` lines 35-38 and 73-83.

Expanding the one-copy integrand gives

`Phi(u)+4y^2/q+y psi(u)=4u^2/q+4y^2/q+2u log q+10y log q+8yu/q`.

The independent-copy identities in PR80 lines 73-99 have the correct coefficients:

- `E[(u-u')(log q-log q')]=2E[u log q]`, using `E u=0`, so the coefficient of `L(Delta u)^2` is `1`.
- `10E[y log q]=5E[(y-y')(log q-log q')]`, using `E y=0`, so the signed mixed logarithmic coefficient is `5L Delta y Delta u`.
- Since `u/q=1-1/q`, `(u/q-u'/q')=Delta u/(q q')`, so `8E[y u/q]=4E[Delta y Delta u/(q q')]`.
- The nonlogarithmic square terms symmetrize to the first line of `J` with coefficient `2`.

Thus the mixed coefficient in PR80 line 67, `[5L(q,q')+4/(q q')] Delta u Delta y`, has the correct sign and coefficient. The diagonal convention is also harmless: `q=q'` is equivalent to `Delta u=0`, so both terms carrying `L` vanish even if `Delta y` does not. The first line remains finite and nonnegative because the strict source scope has `q,q'>0`.

The symmetric left-fiber version follows from the accepted right-fiber cancellation in the addendum lines 23-41.

### Proposition 3.1: free-vector PSD obstruction

Status: source-level PASS.

The lower quadratic obtained from the pairwise Cauchy bounds is correctly written at PR80 lines 113-123:

`A=2/(q+q')+L`, `B=2/(q+q')`, and `C=5L+4/(q q')`.

At the diagonal `q'=q>0`, PR80 lines 131-139 correctly give `A=2/q`, `B=1/q`, and `C=5/q+4/q^2`, so free-vector PSD would require `(5+4/q)^2<=8`. This is impossible for every positive `q`. PR80 line 141 correctly limits the conclusion to the over-relaxed method and does not present it as evidence against entropy concavity.

### Theorem 4.1: DPP-constrained ratio cone

Status: source-level PASS after the wording repairs below.

PR80 correctly identifies the point lost by the free-vector route: actual event pairs satisfy `Delta u=-s Delta a+Delta y`, so `(Delta u,Delta y)` is constrained rather than freely chosen. Substituting the actual ratio `r=Delta y/Delta u` into the lower quadratic gives

`F(q,q',r)=L+2(1+r^2)/(q+q')+r[5L+4/(q q')]`,

matching PR80 lines 149-160. If `Delta u=0`, the mixed terms vanish and the exact pair kernel reduces to the nonnegative first line, as stated in PR80 lines 161-163.

The quantifier in Theorem 4.1 is sufficient with only one fixed side: if every right-fiber pair over each left `S` satisfies `F>=0`, then every pair contribution has a nonnegative lower bound, and averaging first over `T,T'` and then over `S` gives `t^2 I''(t)>=0`. The stated first-line strictness condition is also valid. If some one-copy atom has `u(S,T)` or `y(S,T)` nonzero and the strict DPP fiber gives `nu(T)>0`, then the diagonal pair `T=T'` has `Delta u=Delta y=0`, no mixed term, and exact pair value `J=4(u^2+y^2)/q>0`. All other pairs are nonnegative under the cone hypothesis, so the pair expectation is strictly positive. The left/right-interchanged version is also justified by the accepted symmetric conditional cancellations.

## Required source repairs

1. PR80 line 171: the implication from `t^2 I''(t)>=0` to `H''(t)<=0` needs `t!=0`, equivalently `s>0`, unless a separate endpoint argument is explicitly invoked. As written, a strict legal `s` could include the decoupled endpoint `s=0`, where the displayed product by `t^2` cannot by itself imply a sign for `H''(0)`.

   Minimum repair: in Theorem 4.1, state `s=t^2>0` or change the conclusion to: `Then t^2 I''(t)>=0; for t!=0 this gives H''(t)<=0.` Apply the same repair to strict curvature language.

2. PR80 lines 181-191: Corollary 4.2 should explicitly require a positive likelihood window, for example `0<q_-<=q,q'<=q_+`, because `F` uses `L(q,q')` and `1/(q q')`.

   Minimum repair: add `0<q_-<=q_+` to the displayed envelope hypotheses.

3. PR80 line 191: “Strict positivity gives strict curvature away from degenerate equality cases” is too compressed for integration at the corollary level. This is not a flaw in Theorem 4.1's first-line strictness condition: that condition has the diagonal-pair witness described above, so it does not require an off-diagonal first-line term to survive possible mixed-term cancellation. The corollary should say which nondegeneracy is assumed uniformly or pointwise in the family: either positive mass of an actual `Delta u!=0` pair with strict `F`, or a positive-mass one-copy atom with `u` or `y` nonzero, witnessed by the diagonal pair. It also should be phrased as local curvature on the connected `t`-bands covered by the `s`-interval, not as global chord concavity outside those bands.

   Minimum repair: replace line 191 with a direct reference to the strictness condition in Theorem 4.1, including the diagonal-pair witness for first-line positivity, and state the conclusion as `H''(t)<=0 for all t with t^2 in the interval and t!=0`; hence concavity on each connected `t`-interval where those hypotheses hold.

4. PR80 lines 153-155 and 177: the notation around `Q` should be sharpened. The exact pair kernel `J` is bounded below by the lower quadratic `Q`, and after imposing `r`, `Q=(Delta u)^2 F(q,q',r)`. The displayed wording `Q >= (Delta u)^2 F` is weaker and slightly ambiguous, because after substitution this is equality.

   Minimum repair: write `J >= Q = (Delta u)^2 F(q,q',r)` for `Delta u!=0`.

## PR58 fixture coverage and C2 finite-check contract

PR80 lines 217-233 correctly keep the accepted PR58 `s=9/10` target open. The displayed values in lines 219-229 do not certify the pairwise ratio condition (4.4), and I did not treat them as acceptance evidence.

If PR80 wants to certify coverage of that fixture, the bounded C2 check should have this exact contract:

- Inputs: the accepted PR58 frozen 64-event rational fixture at `s=9/10`, including all product weights, all `a(S,T)` and `b(S,T)`, and the induced `q=1-sa+s^2b`, `u=q-1`, `y=s^2b` for the chosen fixed-side fibers.
- Computation target: for each fixed `S` and ordered pair `T,T'` with positive product mass and `Delta u!=0`, rigorously enclose `F(q,q',Delta y/Delta u)`. If using the right/left-interchanged theorem instead, perform the symmetric check over fixed `T`.
- Required outputs: the minimum certified lower endpoint for `F`, the attaining or worst witness pair if any lower endpoint is negative, counts of `Delta u=0` pairs, and a separate strictness/equality report. For first-line strictness, the report may use the diagonal witness `T=T'` whenever a positive-mass atom has `u` or `y` nonzero.
- Gates: PASS only if one fixed-side theorem has all required lower endpoints `>=0`. A strict-curvature claim additionally needs either a strict `F` witness on a positive-mass `Delta u!=0` pair or the diagonal first-line witness. FAIL if any upper endpoint is `<0`. INDETERMINATE if any interval straddles zero or if the fixture binding is not immutable.
- Non-goals: no whole-chord recomputation, no old additive-projection threshold comparison, and no promotion of author PASS output to positivity.

## Final scoped status

- Exact conditional pair identity: PROVED at source level from accepted premises.
- Free-vector PSD obstruction: PROVED as a method obstruction only.
- DPP-constrained ratio-cone sufficient criterion: PROVED as a pointwise sufficient criterion after the listed wording repairs.
- Corollary interval family form: acceptable only after adding the positive likelihood hypothesis and precise local-curvature/strictness wording.
- PR58 `s=9/10` coverage by the new cone: INCOMPLETE / pending finite check.
- General dense correlated rank-two whole-chord concavity: INCOMPLETE, and PR80 does not close it.
- Code/evidence status: no executable verification was run or accepted in this FIRST source review.
