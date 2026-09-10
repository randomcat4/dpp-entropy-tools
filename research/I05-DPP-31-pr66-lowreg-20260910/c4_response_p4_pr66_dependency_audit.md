# Dependency audit: the PR66 inputs actually used by the `p>4` response repair

Status: **AUTHOR RE-DERIVATION / PENDING_REVIEW**.

This note isolates and checks the finite-volume/conditional lemmas inherited from PR66.  It deliberately stops before PR66's interval-interaction and Dobrushin response sections.  The new `p>4` proof uses none of the invalid A1/A2 import.

Frozen source: PR66 author head `af1edaad69c4e1f5e4bbd1239b8463b56bf64075`, file `research/I05-DPP-25-20260909/proof.md`, Sections 1--3 and the parity determinant identity only.

## 1. Uniform complete-event singular gap

For a finite index set `I` and complete configuration `x`, let

\[
M_{I,x}=T_I(c)-I_{Z_x},
\qquad Z_x=\{i:x_i=0\}.
\]

Order occupied sites before vacant sites and put `J=I_S\oplus(-I_Z)`.  Since

\[
\delta I\le T_I(c)\le(1-\delta)I,
\]

one has, for `v=(u,w)`,

\[
\operatorname{Re}\langle v,J M_{I,x}v\rangle
=\langle u,K_{SS}u\rangle+
\langle w,(I-K_{ZZ})w\rangle
\ge\delta\|v\|_2^2.
\tag{1.1}
\]

As `J` is unitary,

\[
\|M_{I,x}v\|_2\ge\delta\|v\|_2,
\qquad
\|M_{I,x}^{-1}\|_{2\to2}\le\delta^{-1}.
\tag{1.2}
\]

Also

\[
T_I(c)-I\le M_{I,x}\le T_I(c),
\]

so

\[
-(1-\delta)I\le M_{I,x}\le(1-\delta)I.
\tag{1.3}
\]

These bounds include every complete event, including rare words.  In particular all atom determinants are nonzero and the real complete-event probabilities are strictly positive.

## 2. Weighted inverse localization and the original threshold

Let

\[
q=\frac{p+2}{4},
\qquad v_q(n)=(1+|n|)^q,
\]

and use the two-sided weighted Schur norm `S_q`.  It is a Banach algebra because `v_q` is submultiplicative.

Truncate `c` at bandwidth `W`.  Write `M=B+E`, where `B` is Hermitian and banded.  Choose `W` so that `||E||_{2->2}<=delta/4`.  Then

\[
\sigma_{\min}(B)\ge\eta:=3\delta/4,
\qquad
\|B\|_{2\to2}\le1-\eta.
\tag{2.1}
\]

For each eigenvalue `lambda` of `B`, `|lambda|` lies in `[eta,1-eta]`; hence

\[
B^{-1}=B\sum_{r\ge0}(I-B^2)^r.
\tag{2.2}
\]

The `r`-th summand has bandwidth at most `(2r+1)W`, operator norm at most `rho^r` with `rho=1-eta^2<1`, and therefore weighted Schur norm at most

\[
C_{q,\delta}W^{q+1}(r+1)^{q+1}\rho^r.
\]

Thus

\[
\|B^{-1}\|_{S_q}\le C_{q,\delta,W}<\infty.
\tag{2.3}
\]

The tail has

\[
\|E\|_{S_q}
\le (1+W)^{q-p}\|c\|_{A_p}.
\tag{2.4}
\]

Since the banded inverse constant grows at most like `W^{q+1}` in this construction,

\[
\|B^{-1}E\|_{S_q}
\le C W^{2q+1-p}.
\tag{2.5}
\]

For `q=(p+2)/4`,

\[
2q+1-p=\frac{4-p}{2}<0
\]

exactly when `p>4`.  Increasing the fixed `W` gives a uniform Neumann inverse and

\[
\sup_{I,x}\|M_{I,x}^{-1}\|_{S_q}<\infty.
\tag{2.6}
\]

No volume, configuration or event probability enters the constant.

## 3. Common complex parameter disk

For the physical affine family

\[
M_{I,x}(z)=M_{I,x}(0)+zT_I(g),
\]

one has `||T_I(g)||_{S_q}<=||g||_{A_q}`.  Equation (2.6) therefore gives a radius

\[
r_0<\frac1{2B_q\|g\|_{A_q}}
\]

such that

\[
\sup_{|z|<r_0}\sup_{I,x}
\|M_{I,x}(z)^{-1}\|_{S_q}\le2B_q.
\tag{3.1}
\]

This is obtained by the weighted Neumann series around the real center; no Hermiticity is asserted for complex `z`.  The same disk works for every finite complete event.

## 4. Two-leg influence for a remote conditioned bit

For `F_R={1,...,R}`, the complete-event conditional at the origin is the Schur complement

\[
q_{R,z}(x)=\mu-u_R(z)M_{R,x}(z)^{-1}v_R(z),
\tag{4.1}
\]

where `mu=\widehat c(0)` because `\widehat g(0)=0`.

If configurations `x,y` differ only at future site `j`, then

\[
M_{R,y}-M_{R,x}=\pm e_je_j^*,
\]

and

\[
M_{R,y}^{-1}-M_{R,x}^{-1}
=\mp M_{R,y}^{-1}e_je_j^*M_{R,x}^{-1}.
\tag{4.2}
\]

The row `u_R` and column `v_R` have uniform weighted `ell^1_q` norm because `c+zg in A_q`.  Multiplication by a matrix bounded in `S_q` preserves that norm.  Hence

\[
|(u_RM_{R,y}^{-1})_j|
+|(M_{R,x}^{-1}v_R)_j|
\le C(1+j)^{-q}.
\tag{4.3}
\]

Substitution in (4.2) gives the two-leg bound

\[
|q_{R,z}(x)-q_{R,z}(y)|
\le C(1+j)^{-2q},
\tag{4.4}
\]

uniformly in `R`, the complete future word and `z` on each smaller closed disk.  The square comes from the two independent propagator legs; it is not an inclusion-probability shortcut.

## 5. Uniform infinite-future limit

Adding the terminal conditioned site gives the block inverse identity

\[
q_{R+1,z}-q_{R,z}
=-(b-u_RM^{-1}e)S^{-1}(c-dM^{-1}v_R).
\tag{5.1}
\]

Each effective endpoint coupling is `O((1+R)^{-q})` by the same weighted convolution as (4.3).  The scalar `S^{-1}` is the terminal diagonal entry of the inverse enlarged complete-event matrix and is uniformly bounded by (3.1).  Therefore

\[
|q_{R+1,z}-q_{R,z}|
\le C(1+R)^{-2q}.
\tag{5.2}
\]

Since `2q>1`, the series of increments is uniformly summable on smaller complex disks.  Thus `q_{R,z}` converges uniformly in the future word to a holomorphic continuous function `q_z(x_1,x_2,...)`.  Passing (4.4) to the limit gives

\[
\sup_{x\stackrel{\ne j}=y}|q_z(x)-q_z(y)|
\le C(1+j)^{-2q}.
\tag{5.3}
\]

For real legal `z`, each finite `q_{R,z}` is exactly

\[
P_z(X_0=1\mid X_1,...,X_R).
\]

The martingale convergence theorem identifies the almost-sure limit with the true conditional on the full future.  Uniform convergence identifies the continuous version `q_z` with that conditional everywhere on the support.

## 6. Non-null logarithmic conditional

At `z=0`, enlarging a future event by an occupied origin gives

\[
(M_{\{0\}\cup F_R}^{-1})_{00}=q_{R,0}^{-1}.
\]

Equation (1.2) yields `q_{R,0}>=delta`; the analogous vacant-origin event yields `1-q_{R,0}>=delta`.  The bounds survive the infinite-future limit.

The common complex inverse disk also gives a uniform Lipschitz bound in `z`.  After shrinking the disk, both `q_z` and `1-q_z` stay in one simply connected region separated from zero.  Hence one may choose the continued logarithms

\[
G_z(1x)=q_z(x),
\qquad G_z(0x)=1-q_z(x),
\qquad \ell_z=\log G_z.
\]

The logarithm is uniformly Lipschitz on that compact range, so

\[
\sup_{x\stackrel{\ne j}=y}
|\ell_z(\xi x)-\ell_z(\xi y)|
\le C(1+j)^{-2q}.
\tag{6.1}
\]

Telescope future coordinates beyond `n` to obtain

\[
\operatorname{var}_n\ell_z
\le C\sum_{j>n}(1+j)^{-2q}
\le C'(1+n)^{1-2q}.
\tag{6.2}
\]

With `a=2q-1=p/2`, this is the locally uniform `B_a` bound used in the new response proof.  The companion Banach-valued Cauchy lemma then supplies `B_a`-holomorphy and identical memory exponents for the needed parameter derivatives.

## 7. Complete-event parity identity

Let `D_{jj}=(-1)^j`.  Half-period Fourier support gives

\[
T(c-zg)=D T(c+zg)D.
\]

For every complete event, its diagonal matrix `I_Z` commutes with `D`; hence

\[
\det(T_I(c-zg)-I_Z)
=\det(T_I(c+zg)-I_Z).
\tag{7.1}
\]

The same conjugacy applies to every Schur complement, so

\[
G_{-z}=G_z,
\qquad \ell_{-z}=\ell_z.
\tag{7.2}
\]

This proves evenness before any pressure or entropy manipulation and justifies factorization through `s=z^2` in the `B_a` space.

## 8. Exact dependency boundary

The `p>4` finite-response repair imports only Sections 1--7 above.  It does **not** import:

- PR66's interval interaction as a member of Dobrushin A1 or A2;
- the compressed “finite first moment implies analytic pressure” assertion;
- pressure differentiation in `(s,lambda)`;
- any author verdict attached to PR66.

The inherited complete-event calculation is therefore logically upstream of the rejected source bridge.  This note is an author re-derivation, not an independent review; the independent contract remains issue #92.