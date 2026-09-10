# Multiscale spatial-memory response convergence at every `p>4`

Status: **PROVED AS AN AUTHOR LEMMA / PENDING INDEPENDENT REVIEW**.

This supplement strengthens the optional boundary theory.  It is not needed for the qualitative local-concavity theorem in `c4_response_p4_repair.md`.

The direct same-space resolvent comparison in `c4_response_spatial_truncation_p6.md` uses an additional strong-space Poisson inverse and therefore asks for `a=p/2>3`.  The present proof avoids that third strong inverse: first truncate each response correlation sum at time `M`, compare the resulting finite algebra at memory cutoff `N`, and only then let `M` grow with `N`.  This yields quantitative convergence of the full first and second responses for every

\[
a=\frac p2>2.
\]

No finite-window DPP curvature sign is used.  The approximants below are normalized finite-memory conditional chains, and all errors are errors in the genuine infinite correlation/Poisson formulas.

## 1. Uniform family and spatial error

Let `G_s` be the normalized full-future kernel from the complete-event DPP conditional and let

\[
G_{s,N}(\xi\mid x)
=G_s(\xi\mid x_1,\ldots,x_N,0,0,\ldots)
\tag{1.1}
\]

be its canonical memory-`N` freezing.  Denote the transfer operators, invariant laws and parameter derivatives by

\[
L_s,\ \nu_s,\ A_{j,s}=\partial_s^jL_s,
\qquad
L_{s,N},\ \nu_{s,N},\ A_{j,s,N}=\partial_s^jL_{s,N},
\quad j=1,2.
\]

The common complete-event disk and the `B_a` Cauchy estimate give, uniformly on a smaller physical `s` interval,

\[
\max_{0\le j\le2}
\|\partial_s^j(\log G_{s,N}-\log G_s)\|_\infty
\le C N^{-a}.
\tag{1.2}
\]

Uniform non-nullness transfers (1.2) to `G` and its first two derivatives.  Hence, on `C(X)` with the sup norm,

\[
\delta_N:=
\max_{0\le j\le2}
\|\partial_s^j(L_{s,N}-L_s)\|_{\infty\to\infty}
\le C N^{-a}.
\tag{1.3}
\]

For the entropy observable

\[
F_s=\ell_s=\log G_s,
\qquad F_{s,N}=\ell_{s,N}=\log G_{s,N},
\]

and more generally for any moving observable satisfying the same truncation estimate,

\[
\max_{0\le j\le2}
\|\partial_s^j(F_{s,N}-F_s)\|_\infty
\le C_F N^{-a}.
\tag{1.4}
\]

Both the full and frozen kernels have common non-nullness and common `B_a` bounds.  Therefore the BFG/first-disagreement proof applies with constants independent of `N`:

\[
\|L_{s,N}^n(H-\nu_{s,N}H)\|_\infty
+\|L_s^n(H-\nu_sH)\|_\infty
\le C_b(1+n)^{-b}\|H\|_{B_b},
\tag{1.5}
\]

and

\[
R_{s,N},R_s:B_b\longrightarrow B_{b-1}
\quad\text{uniformly},\qquad 1<b\le a.
\tag{1.6}
\]

## 2. Two elementary perturbation bounds

### Lemma 2.1 -- finite-time operator comparison

For every bounded `H` and every `n>=0`,

\[
\|L_{s,N}^nH-L_s^nH\|_\infty
\le n\delta_N\|H\|_\infty.
\tag{2.1}
\]

#### Proof

Use the telescoping identity

\[
L_{s,N}^n-L_s^n
=\sum_{r=0}^{n-1}
L_{s,N}^{n-1-r}(L_{s,N}-L_s)L_s^r
\]

and the fact that both normalized transfer operators are sup-norm contractions.  QED.

### Lemma 2.2 -- invariant-law comparison on `B_b`

For every `b>1` and `H in B_b`,

\[
|\nu_{s,N}H-\nu_sH|
\le C_b\delta_N\|H\|_{B_b}.
\tag{2.2}
\]

#### Proof

The exact invariance/Poisson identity gives

\[
(\nu_{s,N}-\nu_s)H
=\nu_{s,N}(L_{s,N}-L_s)R_sH.
\tag{2.3}
\]

Since `R_sH` is bounded by (1.6), (1.3) proves (2.2).  QED.

This estimate does not require total-variation convergence of the stationary laws.

## 3. Time-truncated Poisson operators

Put

\[
R_s^{<M}H=\sum_{n=0}^{M-1}L_s^n(H-\nu_sH),
\qquad
R_{s,N}^{<M}H=\sum_{n=0}^{M-1}L_{s,N}^n(H-\nu_{s,N}H).
\tag{3.1}
\]

The one-power proof gives two kinds of uniform bounds.

First, for every `b>1`,

\[
\sup_M
\left(
\|R_s^{<M}H\|_{B_{b-1}}
+\|R_{s,N}^{<M}H\|_{B_{b-1}}
\right)
\le C_b\|H\|_{B_b}.
\tag{3.2}
\]

Second, each fixed summand `L^n(H-nu H)` is uniformly bounded in `B_b` by the joint initial-memory estimate, so

\[
\|R_s^{<M}H\|_{B_b}
+\|R_{s,N}^{<M}H\|_{B_b}
\le C_b M\|H\|_{B_b}.
\tag{3.3}
\]

### Lemma 3.1 -- finite-time Poisson comparison

For a uniformly `B_a` moving observable `F_{s,N},F_s` satisfying (1.4),

\[
\|R_{s,N}^{<M}F_{s,N}-R_s^{<M}F_s\|_\infty
\le C_F\delta_N M^2.
\tag{3.4}
\]

#### Proof

For each summand, use (2.1), (1.4), and

\[
|\nu_{s,N}F_{s,N}-\nu_sF_s|
\le \|F_{s,N}-F_s\|_\infty
+|\nu_{s,N}F_s-\nu_sF_s|
\le C_F\delta_N
\]

by Lemma 2.2.  Summing `1+n` for `n<M` gives (3.4).  The same estimate holds with `F'` or `F''`.  QED.

## 4. Finite algebra for the first response

For a fixed observable, define

\[
S_{1,s}^{<M}(F)=
\nu_s(A_{1,s}R_s^{<M}F),
\]

and define the frozen analogue with every object carrying the index `N`.

The integrands are uniformly bounded in `B_{a-1}` by (3.2), while their sup-norm difference is `O(delta_N M^2)` by (3.4), (1.3), and the boundedness of `A_1`.  Applying Lemma 2.2 to the unperturbed integrand gives

\[
\boxed{
|S_{1,s,N}^{<M}(F_N)-S_{1,s}^{<M}(F)|
\le C_F\delta_N M^2.}
\tag{4.1}
\]

For a moving observable this controls all one-Poisson Leibniz terms.

## 5. Finite algebra for the nested second response

Put

\[
Y_s^{<M}=A_{1,s}R_s^{<M}F_s,
\qquad
Y_{s,N}^{<M}=A_{1,s,N}R_{s,N}^{<M}F_{s,N}.
\tag{5.1}
\]

Equations (3.2)--(3.4) imply

\[
\|Y_{s,N}^{<M}-Y_s^{<M}\|_\infty
\le C_F\delta_NM^2,
\tag{5.2}
\]

\[
\|Y_s^{<M}\|_{B_a}
+\|Y_{s,N}^{<M}\|_{B_a}
\le C_FM,
\tag{5.3}
\]

and, more sharply,

\[
\|Y_s^{<M}\|_{B_{a-1}}
+\|Y_{s,N}^{<M}\|_{B_{a-1}}
\le C_F.
\tag{5.4}
\]

Apply the outer time-truncated Poisson operator.  Since its sup operator norm is at most `2M`, the changed-input part is bounded by

\[
\|R_{s,N}^{<M}(Y_{s,N}^{<M}-Y_s^{<M})\|_\infty
\le C_F\delta_NM^3.
\tag{5.5}
\]

For the same input `Y_s^{<M}`, the proof of Lemma 3.1 gives

\[
\|(R_{s,N}^{<M}-R_s^{<M})Y_s^{<M}\|_\infty
\le C_F\delta_NM^2.
\tag{5.6}
\]

Here the centering difference is bounded by Lemma 2.2 and (5.3); its contribution is `O(delta_N M^2)`, while the telescoped operator contribution uses the uniform sup bound in (5.4).

Therefore

\[
\|R_{s,N}^{<M}Y_{s,N}^{<M}-R_s^{<M}Y_s^{<M}\|_\infty
\le C_F\delta_NM^3.
\tag{5.7}
\]

The unperturbed final integrand

\[
H_s^{<M}=A_{1,s}R_s^{<M}Y_s^{<M}
\]

has the crude but sufficient strong bound

\[
\|H_s^{<M}\|_{B_a}\le C_FM^2
\tag{5.8}
\]

by (3.3) and (5.3).  Lemma 2.2 thus compares its two invariant expectations with error `O(delta_N M^2)`.  Combining this with (5.7) and the derivative-operator error yields

\[
\boxed{
\left|
\nu_{s,N}A_{1,s,N}R_{s,N}^{<M}
(A_{1,s,N}R_{s,N}^{<M}F_{s,N})
-
\nu_sA_{1,s}R_s^{<M}
(A_{1,s}R_s^{<M}F_s)
\right|
\le C_F\delta_NM^3.}
\tag{5.9}
\]

The non-nested second-response term with `A_2R` has the smaller bound `O(delta_N M^2)`.  Equations (4.1) and (5.9), applied also to `F_s'` and `F_s''`, prove the same `O(delta_N M^3)` estimate for the complete moving-observable second-response formula truncated at time `M`.

## 6. Restore the infinite correlation sums

The boundary correction for the one-power proof is uniform for the full and frozen kernels.  For every

\[
0<\eta<a-2,
\tag{6.1}
\]

the scalar error made by replacing the full moving-observable second response by the time-`M` formula is

\[
C_{\eta,F}M^{-\eta}.
\tag{6.2}
\]

Combining (1.3), (5.9), and (6.2) gives the explicit two-scale estimate

\[
\boxed{
|\partial_s^2\nu_{s,N}(F_{s,N})
-\partial_s^2\nu_s(F_s)|
\le C_{\eta,F}
\left(M^{-\eta}+N^{-a}M^3\right).}
\tag{6.3}
\]

The corresponding zeroth- and first-response estimates follow with no worse right-hand side.

Choose

\[
M=\left\lfloor N^{a/(3+\eta)}\right\rfloor.
\]

Then, uniformly on a smaller physical parameter interval,

\[
\boxed{
\max_{0\le j\le2}
\left|
\partial_s^j\{\nu_{s,N}(F_{s,N})-\nu_s(F_s)\}
\right|
\le C_{\eta,F}
N^{-a\eta/(3+\eta)},
\qquad0<\eta<a-2.}
\tag{6.4}
\]

For every `a>2` this is a strictly positive power.  Letting `eta` approach `a-2` shows that every exponent below

\[
\frac{a(a-2)}{a+1}
\tag{6.5}
\]

is available from this coarse finite-algebra count.  No optimality is claimed.

## 7. DPP entropy specialization

Take

\[
F_s=\ell_s=\log G_s,
\qquad F_{s,N}=\ell_{s,N}=\log G_{s,N}.
\]

All hypotheses follow from the complete-event common disk and differentiated two-leg memory bound.  Hence for every `p>4`, `a=p/2`, the entropy-rate response of the canonical finite-memory conditional chain converges through order two in `s=t^2` to the true DPP entropy-rate response, with (6.4).

This is a response certificate, not a finite DPP entropy identity: the memory-frozen compatible law need not itself be a finite-section DPP.  In particular no finite-volume Hessian sign is extrapolated.  The true affine DPP kernel, full event law and regularity-free matching coefficient remain the objects used in the qualitative theorem.

## 8. Relation to the other boundary files

- `c4_response_p4_boundary_correction.md` supplies the uniform time-correlation cutoff (6.2) and remains valid.
- `c4_response_spatial_truncation_p6.md` gives a cleaner direct resolvent comparison when `p>6`; it is still correct but no longer the widest quantitative range.
- The withdrawn raw rate in equations (7.3)--(7.5) of the old main file is not revived.  The proven rate here is the slower multiscale exponent in (6.4).

Current status of this addendum is author proof only.  It is not included in the earlier frozen FIRST at `6ecc004a...`; an independent reviewer must rebind the later head before accepting it.
