# Complete-event localization in the Fourier-Sobolev `H^1` class

Status: **AUTHOR PROOF / PENDING REVIEW**.

This file proves the uniform complete-event input for the `H^1_F` theorem. The main point is to place the entire countable event family into one **one-dimensional** block matrix before applying inverse closedness. This avoids both a familywise nonuniform inverse theorem and the artificial two-dimensional threshold that would arise from putting full copies of `Z` on `Z x N`.

## 1. Sequence notation and an elementary algebra estimate

For a sequence `a=(a_m)_{m in Z}`, put

\[
\|a\|_{h^1}^2
:=\sum_{m\in\mathbb Z}(1+|m|)^2|a_m|^2.
\tag{1.1}
\]

This is the Fourier coefficient norm of `H^1(T)`. It is a convolution algebra. Indeed

\[
1+|m|\le (1+|r|)+(1+|m-r|),
\]

so

\[
\begin{aligned}
\|a*b\|_{h^1}
&\le C\bigl(\|(1+|\cdot|)a\|_2\|b\|_1
+\|a\|_1\|(1+|\cdot|)b\|_2\bigr)\\
&\le C_1\|a\|_{h^1}\|b\|_{h^1}.
\end{aligned}
\tag{1.2}
\]

The last inequality uses

\[
\|a\|_1\le
\left(\sum_m(1+|m|)^{-2}\right)^{1/2}\|a\|_{h^1}.
\tag{1.3}
\]

All convolution majorants below are nonnegative, so no cancellation is used in (1.2).

## 2. Packing every finite complete event into one copy of `Z`

Let `E` be the countable collection of pairs

\[
e=(I,x),\qquad I\subset\mathbb Z\text{ finite},\quad x\in\{0,1\}^I.
\]

Enumerate it as `(e_n)`. Write `e_n=(I_n,x_n)`. Choose integer translations `tau_n` recursively so that the finite hulls

\[
\operatorname{hull}(\tau_n+I_n)
\]

are pairwise disjoint and separated by at least two integers. Put

\[
\Lambda_n=\tau_n+I_n,
\qquad
\Lambda=\bigcup_{n\ge1}\Lambda_n\subset\mathbb Z.
\tag{2.1}
\]

Then `Lambda` is relatively separated in `R`, with at most one point in each unit lattice site. Translation preserves every within-event difference:

\[
(\tau_n+i)-(\tau_n+j)=i-j.
\tag{2.2}
\]

For a word `x`, let `Z_x={i in I:x_i=0}` and define the complete-event matrix

\[
M_e(z)=T_I(c+zg)-I_{Z_x}.
\tag{2.3}
\]

On `ell^2(Lambda)` define the block diagonal matrices

\[
\mathbb M_0=\bigoplus_{e\in E}M_e(0),
\qquad
\mathbb G=\bigoplus_{e\in E}T_I(g),
\tag{2.4}
\]

using the translated coordinate labels in `Lambda_n`.

## 3. Exact map to the norm-controlled inverse theorem

For a matrix `A=(a_{lambda,lambda'})` on a relatively separated subset of `R^d`, let its diagonal envelope be

\[
a_A(k)=
\sup_{\lambda-\lambda'\in k+[0,1)^d}|a_{\lambda,\lambda'}|.
\tag{3.1}
\]

The convolution-dominated algebra used in Fang--Shin's norm-controlled inversion theorem has, for matrix exponent `p_mtx=2` and weight `r=1`, norm equivalent to

\[
\|A\|_{\mathcal C^{2,1}}^2
=\sum_{k\in\mathbb Z^d}(1+|k|)^2a_A(k)^2.
\tag{3.2}
\]

The primary theorem used here is their inverse-closedness/norm-control result for `C^{p,r}` matrices on relatively separated sets. Its relevant hypotheses are

\[
1\le p_{\rm mtx}\le\infty,
\qquad
r>d(1-1/p_{\rm mtx}),
\tag{3.3}
\]

and invertibility on `ell^2`. We apply it with

\[
d=1,\qquad p_{\rm mtx}=2,\qquad r=1>1/2.
\tag{3.4}
\]

The one-dimensional packing in Section 2 is essential for this exact inequality.

For nonzero displacement `k`, the direct-sum envelope satisfies

\[
a_{\mathbb M_0}(k)\le|\widehat c(k)|,
\qquad
a_{\mathbb G}(k)\le|\widehat g(k)|,
\tag{3.5}
\]

while their zero diagonals are uniformly bounded. Hence

\[
\mathbb M_0,\mathbb G\in\mathcal C^{2,1}(\Lambda)
\tag{3.6}
\]

because `c,g in H^1_F`.

It remains to check invertibility, not merely blockwise nonsingularity. For a block `M=T_I(c)-I_Z`, order occupied coordinates before vacant coordinates and put `J=I_S direct_sum (-I_Z)`. The strict spectral margin gives

\[
\operatorname{Re}\langle v,J Mv\rangle
=\langle v_S,T_I(c)_{SS}v_S\rangle
+\langle v_Z,(I-T_I(c)_{ZZ})v_Z\rangle
\ge\delta\|v\|_2^2.
\tag{3.7}
\]

Therefore

\[
\|M^{-1}\|_{2\to2}\le\delta^{-1}
\tag{3.8}
\]

uniformly over every event. The direct sum `mathbb M_0` is thus invertible on `ell^2(Lambda)` with the same bound.

The cited inverse theorem now yields

\[
\mathbb M_0^{-1}\in\mathcal C^{2,1}(\Lambda).
\tag{3.9}
\]

Consequently the single sequence

\[
d_0(k):=
\sup_{e=(I,x)}\ 
\sup_{\substack{i,j\in I\\i-j=k}}
|(M_e(0)^{-1})_{ij}|
\tag{3.10}
\]

obeys

\[
\boxed{\sum_k(1+|k|)^2d_0(k)^2<\infty.}
\tag{3.11}
\]

There is no interchange of a supremum over events with an infinite sum: `d_0` is the actual diagonal envelope of one matrix to which the theorem is applied once.

## 4. A common complex disk with one common envelope

Let

\[
b(k)=|\widehat g(k)|+|\widehat g(-k)|,
\qquad
c_*(k)=|\widehat c(k)|+|\widehat c(-k)|.
\]

Both lie in `h^1`. Matrix multiplication is dominated diagonally by convolution of envelopes. Hence the envelope

\[
h=d_0*b
\]

lies in `h^1` by (1.2). Choose `r_0>0` so small that the convolution-algebra Neumann series below converges. For `|z|<=r_0`,

\[
(\mathbb M_0+z\mathbb G)^{-1}
=\sum_{n\ge0}(-z)^n
(\mathbb M_0^{-1}\mathbb G)^n\mathbb M_0^{-1}.
\tag{4.1}
\]

Taking absolute diagonal envelopes term by term gives the common majorant

\[
d:=\sum_{n\ge0}r_0^n h^{*n}*d_0\in h^1.
\tag{4.2}
\]

Thus

\[
\boxed{
\sup_{|z|\le r_0}
\sup_{e=(I,x)}
|(M_e(z)^{-1})_{ij}|
\le d(i-j),
\qquad d\in h^1.}
\tag{4.3}
\]

This explicit majorant is stronger than a mere uniform bound of the algebra norms: it legitimately permits later summation after taking the supremum over the complex disk and all events.

## 5. Two-leg conditional influence

For a finite future `F_R={1,...,R}` and complete future word `x`, the occupied-origin conditional is the exact Schur complement

\[
Q_{R,z}(x)
=\mu-u_R(z)M_{R,x}(z)^{-1}v_R(z),
\qquad \mu=\widehat c(0),
\tag{5.1}
\]

where `u_R,v_R` are the origin-to-future Toeplitz row and column of the physical kernel `T(c+zg)`.

Put

\[
a(k)=c_*(k)+r_0 b(k)\in h^1,
\qquad e=a*d\in h^1.
\tag{5.2}
\]

If two complete future words differ only at site `j`, then their event matrices differ by `plus_or_minus e_j e_j^*`. The resolvent identity gives

\[
Q_{R,z}(x)-Q_{R,z}(y)
=\pm(u_RM_y^{-1})_j(M_x^{-1}v_R)_j.
\tag{5.3}
\]

Each factor is bounded by `e(j)` after harmless symmetrization. Therefore

\[
|Q_{R,z}(x)-Q_{R,z}(y)|
\le e(j)^2.
\tag{5.4}
\]

To pass to the infinite future, add site `R+1` and use block inversion. Each effective endpoint coupling is bounded by

\[
\widetilde e:=a+a*d*a\in h^1,
\tag{5.5}
\]

and the scalar inverse Schur complement is uniformly bounded by (4.3). Hence

\[
|Q_{R+1,z}-Q_{R,z}|
\le C\widetilde e(R+1)^2.
\tag{5.6}
\]

Since `e,tilde e in h^1`,

\[
\sum_{j\ge1}(1+j)^2
\bigl(e(j)^2+\widetilde e(j)^2\bigr)<\infty.
\tag{5.7}
\]

In particular (5.6) is uniformly summable. The finite conditionals converge uniformly on the common complex disk to a continuous holomorphic conditional `G_z`. For real legal `z`, martingale convergence identifies it with the true complete-event conditional.

At `z=0`, the same complete-event coercivity applied after adding an occupied or vacant origin gives

\[
G_0(\xi|x)\ge\delta,
\qquad \xi=0,1.
\tag{5.8}
\]

Shrink the disk so both conditional values stay in a common simply connected set separated from zero, and define

\[
\ell_z(\xi x)=\log G_z(\xi|x)
\tag{5.9}
\]

using the continued real logarithm.

There is a fixed nonnegative sequence

\[
\beta_j=C\bigl(e(j)^2+\widetilde e(j)^2\bigr)
\tag{5.10}
\]

such that

\[
\sup_{|z|\le r_1}
\sup_{x\stackrel{\ne j}=y}
|\ell_z(\xi x)-\ell_z(\xi y)|
\le\beta_j,
\tag{5.11}
\]

on every smaller disk, and

\[
\boxed{\sum_{j\ge1}(1+j)^2\beta_j<\infty.}
\tag{5.12}
\]

## 6. Parameter derivatives and the exact memory moment

Apply Cauchy's formula to the holomorphic difference in (5.11). For each fixed `m`, in particular `m=0,...,4`,

\[
\sup_{|z|\le r_2}
\sup_{x\stackrel{\ne j}=y}
|\partial_z^m\ell_z(\xi x)-
\partial_z^m\ell_z(\xi y)|
\le C_m\beta_j.
\tag{6.1}
\]

If two futures agree through coordinate `n`, telescope the remaining coordinates:

\[
\operatorname{var}_n(\partial_z^m\ell_z)
\le C_m\rho_n,
\qquad
\rho_n:=\sum_{j>n}\beta_j.
\tag{6.2}
\]

The second moment in (5.12) is exactly what is needed for a first moment of the variation tail:

\[
\begin{aligned}
\sum_{n\ge0}(n+1)\rho_n
&=\sum_{j\ge1}\beta_j\sum_{n=0}^{j-1}(n+1)\\
&=\frac12\sum_{j\ge1}j(j+1)\beta_j<\infty.
\end{aligned}
\tag{6.3}
\]

Half-period Fourier support gives the complete-event conjugacy

\[
T(c-zg)=D T(c+zg)D,
\qquad D_{jj}=(-1)^j.
\tag{6.4}
\]

Every event diagonal commutes with `D`, so every complete-event determinant and every Schur complement is invariant under `z -> -z`. Thus `G_z` and `ell_z` are even and factor holomorphically through

\[
s=z^2.
\]

For the resulting family `ell_s`, equations (6.1)--(6.3) hold for `ell_s`, `partial_s ell_s`, and `partial_s^2 ell_s`.

This finishes the complete-event localization and differentiated-memory input. It retains all events, including arbitrarily rare words, because the only uniform step is the single direct-sum inverse theorem applied to the complete-event matrices themselves.