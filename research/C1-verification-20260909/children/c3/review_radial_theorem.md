# C3 review of PR29 radial theorem

Verdict: `ACCEPTED_SCOPED`.

Covered version: PR29 frozen commit `648f1906468e3e548410f98a6b1a53a978f2ea11`.

Inputs used for this part:

- `sources/pr29/frozen_statement_v2.md`
- `sources/pr29/proof.md`

I did not use PR30 author acceptance, old review conclusions, or old verification conclusions for this decision. Novelty is not certified here.

## Claim checked

The frozen finite claim is the full feasible radial line through an interior diagonal DPP kernel: `B=diag(b_i)`, `0<b_i<1`, fixed Hermitian `A`, and `J={t:0<=B+tA<=I}`; the target is concavity of `H(B+tA)` on all of `J`, including boundaries (`frozen_statement_v2.md:8-15`). The frozen scalar-rate claim is the true entropy rate along symbols `p+t g`, with `p in (0,1)`, bounded measurable real `g`, legal interval `I`, and no zero-mean, smoothness, evenness, bandwidth, margin-at-boundary, or rate differentiability assumption (`frozen_statement_v2.md:17-24`). The proof interface specifically rules out cardinality/quantum entropy substitutes and requires finite event laws plus pointwise finite entropy limits (`frozen_statement_v2.md:28-32`).

## Checks

Product replacement lemma: the proof defines independent coordinate replacement on a finite product space with positive product reference `pi` (`proof.md:8-18`), notes interior positivity for `r in (0,1)^n` (`proof.md:20-22`), and derives `r_i partial_i F=J(nu_r,E_i nu_r)` without assuming the current law has reference marginals (`proof.md:34-42`). I checked the algebra in (1)-(3); the subtraction of `log(E_i nu_r/pi)` is valid because it depends only on `x_{-i}` and the two laws have the same `(-i)` marginal.

KL contraction to mixed derivatives: for `i!=j`, the factorization `Q_j(a)=Q_j(a/b)Q_j(b)` is stated and used with the same Markov channel on both arguments (`proof.md:44-55`). Since both directions of relative entropy contract, `J` is nondecreasing in `r_j`; differentiating `r_i partial_i F=J_i` gives `partial_j partial_i F>=0` for `r_i>0` (`proof.md:57-59`). The diagonal second derivative formula is the standard finite affine-law formula (`proof.md:61-63`).

Hessian scope: the proof explicitly uses entrywise nonnegativity only in the all-ones simultaneous retention direction (`proof.md:65-69`) and later repeats that this is not a PSD Hessian statement for signed nonuniform directions (`proof.md:173-176`). This matches the frozen radial scope.

Entropy concavity and endpoints: the entropy identity `H=-F-sum nu log pi` and product-reference structure make the second term affine in the retention vector (`proof.md:71-77`). Continuity of finite entropy extends the one-parameter result to `[0,1]`, including zero input masses (`proof.md:77-79`).

Exact DPP identification: the replacement channel keeps each original bit with probability `t` and otherwise inserts an independent Bernoulli `b_i` (`proof.md:83-87`). Inclusion moments are computed for every subset (`proof.md:89-93`) and matched to `det[tK_S+(1-t)B_S]` via the diagonal-plus-matrix determinant expansion (`proof.md:95-105`). Inclusion moments determine the full law on `{0,1}^n`, so this is the required event-law identification of the affine DPP family `B+t(K-B)`. The proof also explicitly avoids substituting an eigenvalue path or `L=K(I-K)^{-1}` path (`proof.md:111-112`).

Full feasible ray: for any positive feasible `T`, applying the `[0,1]` product-channel result to `K=B+TA` gives concavity on `[0,T]`; any negative feasible `T` gives concavity on `[T,0]` (`proof.md:116-122`). Because event masses are polynomial in the ray parameter and strictly positive near `0`, the one-sided derivatives at `0` agree (`proof.md:124-132`). The decreasing-secant argument then joins the two halves (`proof.md:133-137`). Boundary feasible kernels are included by continuity, without needing finite boundary derivatives (`proof.md:139-141`).

Diagonal changes and noncommutation: the finite proof starts from arbitrary finite Hermitian contractions `K` and diagonal product reference `B` (`proof.md:83-105`), so diagonal entries of `A` are included when `K=B+TA`; the later ray argument does not impose `diag(A)=0` or commutation. This matches the v2 change removing the old diagonal and zero-mean restrictions (`frozen_statement_v2.md:43-47`).

Scalar stationary rate: for every legal symbol `f_s=p+s g`, the Fourier quadratic form places each finite compression between `0` and `I` (`proof.md:145-152`). The finite compression is exactly `p I_n+s A_n`, and the proof explicitly includes nonzero integral of `g`, complex finite Toeplitz matrices, and symbols touching `0` or `1` (`proof.md:154-157`). Thus finite-block entropy is concave at each `n` for all `s_1,s_2 in I` (`proof.md:159-162`). Stationarity and Shannon subadditivity give `h(f_s)=lim H_n(s)/n=inf H_n(s)/n`, and the proof passes to three pointwise limits in an already established finite inequality (`proof.md:164-169`). I see no hidden differentiation under the entropy-rate limit.

## Remaining scope limits

This accepts only the frozen radial theorem and the constant-symbol scalar chord theorem. It does not certify arbitrary scalar chords, arbitrary affine directions at a non-diagonal finite kernel, the full Lyons-Steif conjecture, or novelty (`frozen_statement_v2.md:34-41`, `proof.md:171-178`).
