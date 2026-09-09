# W1 round2 independent review

Status: `ACCEPTED_SCOPED`.

This is a separate review of PR32 round2 update commit `a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8`. It does not alter the earlier W1 first-round review or its `ACCEPTED_SCOPED` judgment for the rank-one theorem.

## Scope

I reviewed the supplied round2 author manuscript in `sources/pr32_round2`:

- `frozen_statement.part01.md`
- `frozen_statement.part02.md`
- `proof.part01.md` through `proof.part07.md`
- `RESULT.part01.md`
- `RESULT.part02.md`

I did not use older review opinions or PR30 material. The accepted round2 scope is:

1. the `m x 2` cross-block radial theorem for fixed strict real symmetric `A`, strict real symmetric `C in Sym_2`, and arbitrary real `B in R^{m x 2}`;
2. the symmetric version with the left block of size at most two;
3. the arbitrary-right-dimension extension when the cross block has at most two actual nonzero coordinate columns, and its row-supported analogue;
4. the rank-two exterior-power identities and the two stated obstruction examples, as scoped evidence and boundary information.

The review does not accept any claim of arbitrary finite-dimensional real-kernel affine concavity, arbitrary `m,l>2` rank-two radial concavity with dense row and column support, complex Hermitian concavity, stationary entropy-rate concavity, novelty, or publication priority. These exclusions match `frozen_statement.part02.md:82-90` and `RESULT.part02.md:40-49`.

## Main Proof Check

The conditional Schur factorization is correct. `proof.part01.md:57-99` derives, for every complete left/right event `(S,T)`,

```text
p_K(t)(S,T) = p_A(S) p_{C-t^2 M_S}(T),
M_S = B^T (A-E_{S^c})^{-1} B.
```

The signs agree with the event determinant formula in `proof.part01.md:5-51`, and no event layer is dropped. `proof.part01.md:101-124` and `proof.part02.md:1-8` correctly show the conditional object is a genuine strict DPP kernel on the strict legal interval, not just a formal signed determinant.

The entropy chain rule in `proof.part02.md:12-27` is exact because the left marginal is fixed. The zero-mean identity in `proof.part02.md:31-55` is also correct and explains why `H''(0)=0` in these even radial paths.

The self-contained real `2 x 2` entropy lemma is acceptable. The four probabilities and Hessian formula in `proof.part02.md:61-124` are correct. The determinant-pencil reduction and scalar inequalities in `proof.part03.md:1-108` close the nonzero-offdiagonal case, while `proof.part03.md:117-123` handles the diagonal case and correctly distinguishes semidefinite instantaneous Hessian from strict Jensen concavity along nontrivial chords.

The radial lift is sound. Once each conditional line `s -> H(C-sM_S)` is concave, `G(s)=H(K(sqrt(s)))` is concave. `proof.part04.md:37-82` then uses fixed marginals to get `G(0)-G(s)=I(left;right)>=0`, strict for `B!=0` and `s>0`, and combines strict monotonicity of `G` with strict convexity of `t^2`. This covers same-sign, opposite-sign, and centered chords. It proves strict Jensen concavity; it does not claim `H''<0` at `t=0`, where the second derivative is zero.

The endpoint treatment in `proof.part07.md:40-51` is adequate. Interior Jensen inequalities pass to the closed legal interval by continuity of finite event probabilities and of `-x log x` at zero; no boundary derivative is used.

For strictness on the closed legal interval, the proof is not relying on a merely nonstrict continuous limit. The strict interior argument in `proof.part04.md:37-82` gives `G(0)>G(s)` for every legal `s>0` when `B!=0`, hence `G` is strictly decreasing on `[0,tau^2]`; combined with the strict convexity of `t^2`, this gives strict Jensen inequality for distinct endpoints as well. Continuity is then used only to pass the already strict value inequality to spectral-boundary points.

## Coordinate-Column Extension

The two-coordinate support lift is valid. `proof.part03.md:125-140` and `proof.part04.md:1-26` prove that an affine direction supported on a real coordinate principal block of size at most two has concave full entropy in arbitrary ambient dimension. Then `proof.part05.md:23-31` applies this to `B` with at most two actual nonzero coordinate columns.

This is not the same as arbitrary `rank(B)<=2`. The manuscript correctly keeps the distinction: `proof.part06.md:10` and `proof.part07.md:55-59` state that a non-coordinate rank-two range cannot be rotated into observed coordinates, since full-configuration entropy is basis dependent. My earlier first-round rotation check also confirmed this numerically from exact kernels with the same eigenvalues but different full-configuration entropy.

There is one editorial issue: `frozen_statement.part02.md:1` has a corrupted glyph in "columns all zero" (`雰`). The proof text at `proof.part05.md:25-31` makes the intended condition unambiguous. This should be fixed before integration, but it is not a mathematical gap.

## Rank-Two Bridge And Obstacles

The exterior-power likelihood identity in `proof.part05.md:33-83` is correct:

```text
P_s/P_0 = det(I_2 - s G_A G_C),
R/P_0 = -tr(G_A G_C),
Q/P_0 = det(G_A) det(G_C).
```

The moment cancellations in `proof.part05.md:85-97` and `proof.part06.md:1-8` follow from applying the rank-one/rank-two determinant lemma to the single-block distribution and comparing coefficients.

The proof does not rely on the false sign claim for the `Q` term. `proof.part06.md:14-35` states the real control comes from `G'<=0` and `G''<=0`. The harmful-`Q` example in `proof.part06.md:37-104` and `proof.part07.md:1-5` is consistent with this: the `Q` log term can make the last term of the old three-term formula positive, while full curvature remains negative.

The block-refresh obstruction in `proof.part07.md:7-38` is also correct: `(1-lambda)P_s+lambda P_0` differs from `P_{(1-lambda)s}` by `lambda(1-lambda)s^2 Q`, so the rank-one refresh intuition cannot be reused once `Q` is nonzero.

## Independent Compute Evidence

I updated `children/w1/round2_frozen_scope.md` and `children/w1/ROUND2_COMPUTE_PLAN.md` before round2 computation. I then ran `children/w1/w1_round2_check.py` in W1's isolated compute directory with one numerical thread.

Returned records:

- `children/w1/round2_job_record.txt`: Python 3.12.3, SymPy 1.13.3, NumPy 2.1.2, mpmath 1.3.0, PID 168104, exit code 0.
- `children/w1/round2_stdout.txt`: complete JSON output.
- `children/w1/round2_stderr.txt`: empty.
- `children/w1/compute_outputs/w1_round2_check_results.json`: structured result.

Key checks:

- `m x 2` fixed rational case: all 32 complete-event conditional identities passed; `rank(B)=2`; all conditional kernels checked strict at `t=1/5`; the exact log-coefficient cancellation at `t=0` passed; the central chord with step `1/5` was strictly negative.
- Two actual coordinate columns in a four-dimensional right block: all 64 complete-event conditional identities passed; `M_S` remained supported inside the actual two columns; `rank(B)=2`.
- `2 x 2` Hessian lemma: direct Hessian and formula matched on a fixed rational nonzero-offdiagonal case; the determinant-pencil identity was checked exactly; at a diagonal center with pure offdiagonal direction `H''(0)=0`, but the same line has negative Hessian away from the center and a strictly negative central chord.
- Harmful `Q` example: `det(B)=-39/50`, minimum event probability at `t=1/10` was `24173/12500000`, `<Q,log(P_s/P_0)>` was negative, `-10s` times that term was positive, and the full `H''` was approximately `-73.2371290529134`.

These computations are consistency and certificate checks for the manuscript's named proof obligations. They are not used as a substitute for the general proof.

## Determinant-Pencil Supplement

After the initial review, I added a separate bounded check for the general determinant-pencil identity (3.9), because the first round2 JSON had only recorded a fixed-rational instance.

I wrote `children/w1/ROUND2_PENCIL_PLAN.md` before running it, then executed `children/w1/w1_round2_pencil_symbolic.py` with symbolic variables `A0,A1,A2`, `A3=1-A0-A1-A2`, and `lambda`. The script constructs `G` and `Q` from the manuscript formulas, with `a=A1+A3`, `b=A2+A3`, `r=A1*A2-A0*A3`, `P=A0*A1*A2*A3`, and `E=A0*A3*(A0+A3)+A1*A2*(A1+A2)`. It then expands

```text
det(G-lambda Q) - (16r+4lambda E-lambda^3 P)/(16rP)
```

as a single rational expression.

Returned records:

- `children/w1/round2_pencil_job_record.txt`: Python 3.12.3, SymPy 1.13.3, PID 168340, exit code 0.
- `children/w1/round2_pencil_stdout.txt`: complete JSON output.
- `children/w1/round2_pencil_stderr.txt`: empty.
- `children/w1/compute_outputs/w1_round2_pencil_symbolic_results.json`: `difference_numerator_factor` is `0`, `difference_denominator_factor` is `1`, and `verified_zero` is `true`.

This upgrades my determinant-pencil check from a fixed rational spot-check to a general symbolic verification of the manuscript's equation (3.9).

## Verdict

`ACCEPTED_SCOPED`: the round2 `m x 2` theorem and the actual two-coordinate-column extension are proved in the stated real finite-dimensional scope, with strictness understood as strict Jensen concavity on nondegenerate legal intervals. At `t=0`, `H''(0)=0` remains expected and correctly handled.

Integration note: fix the corrupted zero glyph in `frozen_statement.part02.md:1` before publishing or merging the round2 statement.
