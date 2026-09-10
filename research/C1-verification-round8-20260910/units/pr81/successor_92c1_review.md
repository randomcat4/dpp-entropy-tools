# PR81 successor 92c1 delta FIRST review

Scoped verdict: ACCEPTED_SCOPED for the new analytic inequalities in `coupled_gram_fixed_shape.md`: Lemma 2.1, the four-scalar rectangle Gram inequalities (4)-(7), and the same-q edge-placement/secant inequalities (12)-(15). These follow from the original PR81 four-scalar definitions when `x=y=1/2` and the rectangle is strict.

This successor does not prove `det E_H>=0` for the fixed shape, does not prove the general missing-edge determinant sign, and does not certify general real three-point entropy concavity. Large rational determinant/minor displays and approximate fixed-point sensitivity diagnostics are source evidence only under this review; they were not independently arithmetically reconstructed.

## Source binding

Reviewed delta source:

- `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md`, 393 lines, blob `d4ce531dcbe8aabc6ea0224b0642ac045d829987`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac/`

Allowed context:

- Original PR81 proof at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md`
- Scoped PR70 proof and post-checkpoint at `source-snapshots/pr70/proof.md` and `source-snapshots/pr70/post_checkpoint.md`

The delta metadata says this successor adds only `coupled_gram_fixed_shape.md`; the original `proof.md` is outside this delta review.

## Accepted analytic points

ACCEPTED_SCOPED: the fixed half-leaf shape is legal and correctly tied to the original PR81 variables. The source fixes `x=y=1/2`, `A=1/4`, `B=4/9`, `r=11/36`, and `0<q<r` at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:9-18`. With `v=w=1/4`, the displayed `b=1/4`, `c=1/3`, and `z=q+25/72` at `:20-26` agree with the original PR81 arrow definitions. This is a fixed-shape slice, not a new general parameter theorem.

ACCEPTED_SCOPED: the q-derivative identities at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:28-37` are correct consequences of original PR81. For `x=y=1/2`, `ell=(h_A(q+B)+h_A(q))/2`, `k=(h_B(q+A)+h_B(q))/2`, and `lambda=h_A(q+B)-h_A(q)=h_B(q+A)-h_B(q)`. Differentiating these identities gives the displayed formulas for `ell'`, `k'`, `lambda'=J''(q)`, and `J'=lambda`. The specific large rational derivative values at `:39-54` were not recomputed; their use here is limited to source-level sign diagnostics.

ACCEPTED_SCOPED: Lemma 2.1 is analytically correct. The source defines `h_A(t)=int_0^A f(t+a) da` at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:56-66`. The binary-logit identity `f''=2 f'^2/f+2 f^2` at `:72-78`, Cauchy-Schwarz in the positive measure `f(t+a) da` at `:80-93`, and the strict positivity of `2 h_A h_A''-3 h_A'^2` at `:95-107` prove `u_A=h_A^(-1/2)` is strictly concave at `:110-116`. Strictness uses `A>0` and the positive integral `I_A`; it is not a uniform margin near degenerations.

ACCEPTED_SCOPED: the four-scalar rectangle Gram inequalities are valid on strict half-leaf rectangles. Strict concavity gives the interior chord inequality at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:118-145`; integrating the reciprocal-square affine bound gives `J < B sqrt(h_A(q) h_A(q+B))`. Substituting `h_A(q)=ell-lambda/2` and `h_A(q+B)=ell+lambda/2` at `:147-158` yields `J^2 < B^2(ell^2-lambda^2/4)`. Swapping axes gives `J^2 < A^2(k^2-lambda^2/4)` at `:160-170`. These are necessary coupled-realizability constraints for actual strict DPP rectangles with `x=y=1/2`; they are not sufficient for determinant positivity or for realizing arbitrary four-tuples.

ACCEPTED_SCOPED: the source preserves the full Fisher/acceleration/marginal structure. The continuation explicitly states that it uses the accepted PR70 full core with complete eight-event entropy, true kernel-affine directions, complete paired Fisher `F`, positive update `R`, marginal Fisher `diag(1/v,1/w)`, and mixed directions at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:3-5`. Later sections correctly distinguish the rational Fisher block and full `L,C,R,Y=F+R,E_H` construction at `:222-259`. There is no replacement of the full DPP Hessian by an independent scalar or operator-mean argument.

ACCEPTED_SCOPED: the nonrealizability proof for the relaxed tuple is analytically valid. The source states that actual realizability would require `ell+lambda/2=h_A(q+B)` at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:261-266`. For the relaxed tuple this is `6`; on the actual interval `75/144 <= t <= 37/48`, `f` is increasing, so `h_A(q+B) <= A f(37/48)=576/407<2<6` at `:268-283`. This proves the displayed tuple is outside the actual same-q DPP curve. It is a useful structural exclusion, not an entropy counterexample.

ACCEPTED_SCOPED: the same-q secant inequalities are correct. Strict concavity of `u_A` implies the strict derivative/secant ordering at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:296-306`. The derivative formula `u_A'=-h_A'/(2h_A^(3/2))` and `h_A'=f(t+A)-f(t)` at `:306-311` give the explicit A-axis inequality at `:313-326`; swapping axes gives the B-axis companion at `:328-334`. These constraints add edge placement at the same `q`, but line `:366-379` correctly says separate A- and B-axis secants still do not enforce the shared four-corner logit representation.

ACCEPTED_SCOPED: strictness and parameter dependence are appropriately bounded. The Gram and secant inequalities are strict for `A,B>0` and `q>0`, `q+A+B<1`, but their quantitative gaps depend on the shape and endpoint distances. The source does not claim a uniform gap, a uniform tail threshold, or a determinant-positive endpoint certificate. It reserves the long-filament/interval work at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:391` and marks the fixed-shape/general determinant problem incomplete at `:393`.

## Evidence not independently certified

SOURCE_ONLY_DIAGNOSTIC: the approximate actual fixed-point values, eigenvalues, determinant sensitivities, and derivative-channel contributions at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:184-220` are clearly labelled diagnostic and ordinary high precision. This review did not recompute them and does not use them as a proof.

SOURCE_ONLY_ARITHMETIC: the exact relaxed negative determinant/minor display at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:222-259` rests on large rational formation of `Y` and `det E_H`. Under the current no-arithmetic-execution scope, I did not independently reconstruct those fractions. If the displayed rational algebra is correct, it shows that the Gram inequalities plus coarse bounds are not sufficient for determinant positivity. The accepted conclusion here is narrower: the source properly treats it as a relaxed non-DPP witness and not as an entropy counterexample.

SOURCE_ONLY_DIAGNOSTIC: the two-axis stress test at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:366-379` is explicitly diagnostic. It does not create a theorem, a C2 obligation, or a determinant-sign conclusion.

## Remaining gaps and boundaries

OPEN: actual fixed-shape `det E_H>=0` is still not proved. The successor narrows the realizability envelope, but its own next target at `source-snapshots/pr81_delta/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md:381-391` is still future work.

OPEN: general missing-edge `det E_H>=0` and general real three-point entropy concavity remain open.

PENDING_C2_UNCHANGED: the old PR70 finite paired-resolvent evidence remains independently pending and is not advanced or used here.

NOT_ASSESSED: novelty.

NOT_PERFORMED: formal verification, interval certification, entropy finite job, and arithmetic checker execution.

Final classification: ACCEPTED_SCOPED for the new analytic Gram and same-q inequalities, with fixed-shape and parameter-dependent scope; SOURCE_ONLY for fixed-point numeric/channel diagnostics and large rational relaxed determinant evidence; OPEN for actual fixed-shape and general `det E_H`; novelty NOT_ASSESSED; formal verification NOT_PERFORMED.
