# Uniform complete-event localization without the old band-truncation loss

Status: **PROVED AS AN AUTHOR LEMMA / PENDING INDEPENDENT REVIEW**.

This file works with the physical affine Toeplitz kernel

\[
K_z=T(c+zg)
\]

and every complete-event matrix

\[
M_{I,x}(z)=T_I(c+zg)-I_{Z_x},
\qquad Z_x=\{i\in I:x_i=0\}.
\]

No inclusion-only probability, spectral entropy, observation-basis rotation, or
`L`-affine path is used.

## 1. Fourier class and conclusion

For `r>=0`, write

\[
\mathcal A_r=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^r
 |\widehat u(m)|<\infty\right\}.
\]

Assume throughout this file that `r>0`, `c,g in A_r` are real, and

\[
\delta\le c\le1-\delta
\]

almost everywhere.  The parity hypotheses are not needed until the entropy
argument.

The conclusion is stronger than a separate norm bound for each event matrix.
There are a radius `rho>0` and a single nonnegative sequence `d in l^1_r(Z)`
such that

\[
\sup_{|z|\le\rho}\sup_{I,x}\sup_{i,j\in I:\ i-j=m}
 |M_{I,x}(z)^{-1}(i,j)|\le d(m)
\tag{1.1}
\]

for every `m in Z`, and

\[
\sum_m(1+|m|)^r d(m)<\infty.
\tag{1.2}
\]

The fact that the envelope is common to all windows and all complete words is
load-bearing below.

## 2. Primary inverse theorem and exact assumptions map

The external input is Q. Fang and C. E. Shin, *Norm-Controlled Inversion of
Banach algebras of infinite matrices*, C. R. Math. 358 (2020), 407--414,
Theorem 2.

For a relatively separated `Lambda subset R^d`, their algebra
`C^{p_alg,r}(Lambda)` has norm

\[
\left(\sum_{k\in\mathbb Z^d}
 \sup_{\lambda-\lambda'\in k+[0,1)^d}
 |A(\lambda,\lambda')|^{p_{alg}}
 (1+|\lambda-\lambda'|)^{p_{alg}r}
\right)^{1/p_{alg}}
\]

with the usual supremum modification at infinity.  Their Theorem 2 says that,
when

\[
r>d(1-1/p_{alg}),
\]

an element of this algebra that is invertible on `l^{q_alg}(Lambda)` has its
inverse in the same algebra, with a norm bound depending only on the original
algebra norm and the operator inverse norm.

We use

\[
p_{alg}=1,\qquad q_{alg}=2,\qquad d=2.
\]

The theorem's strict condition then reduces to `r>0`.  It does not require the
matrix to be Toeplitz or self-adjoint, and its norm-control is what permits one
simultaneous direct-sum application below.  Mere inverse-closedness without
norm control would not supply a uniform family estimate.

## 3. Simultaneous direct sum of every complete event

The set

\[
\mathscr E=\{(I,x): I\Subset\mathbb Z,\ x\in\{0,1\}^I\}
\]

is countable.  Enumerate it by `e in N`.  On one copy of `l^2(Z)` define

\[
\widetilde M_e(0)
=P_I\{T(c)-I_{Z_x}\}P_I+(I-P_I).
\tag{3.1}
\]

This is the event matrix on `I`, extended by the identity and with no
cross-boundary entries.

Let

\[
\Lambda=\mathbb Z\times\mathbb N\subset\mathbb R^2,
\qquad
\mathbb M_0=\bigoplus_{e\in\mathscr E}\widetilde M_e(0)
\]

on `l^2(Lambda)`.  The half-plane lattice is relatively separated.

For a nonzero horizontal displacement `m`, every corresponding entry of every
block is either zero or `\widehat c(m)`.  For zero displacement the entries are
bounded by an absolute constant.  All vertical off-block entries vanish.
Consequently

\[
\|\mathbb M_0\|_{C^{1,r}(\Lambda)}
\le C_r\{1+\|c\|_{\mathcal A_r}\}.
\tag{3.2}
\]

### Uniform invertibility

For one event, order occupied coordinates before vacant coordinates and let
`J=I_S\oplus(-I_Z)`.  For `v=(u,w)`, the cross terms in the following real part
cancel:

\[
\operatorname{Re}\langle v,J M_{I,x}(0)v\rangle
=\langle u,K_{SS}u\rangle
 +\langle w,(I-K_{ZZ})w\rangle
\ge\delta\|v\|_2^2.
\tag{3.3}
\]

As `J` is unitary,

\[
\|M_{I,x}(0)v\|_2\ge\delta\|v\|_2,
\qquad
\|M_{I,x}(0)^{-1}\|_{2\to2}\le\delta^{-1}.
\tag{3.4}
\]

The extension (3.1) therefore has inverse norm at most
`max(1,delta^{-1})`, uniformly in `e`.  Hence the direct sum is invertible and

\[
\|\mathbb M_0^{-1}\|_{2\to2}
\le\max(1,\delta^{-1}).
\tag{3.5}
\]

Fang--Shin Theorem 2 applied to (3.2)--(3.5) gives

\[
\mathbb M_0^{-1}\in C^{1,r}(\Lambda),
\qquad
\|\mathbb M_0^{-1}\|_{C^{1,r}}
\le C(r,\delta,\|c\|_{\mathcal A_r}).
\tag{3.6}
\]

Because this is one direct-sum matrix, (3.6) already places the supremum over
all events **inside** the summation over diagonal displacements.  Thus, with

\[
d_0(m)=\sup_{e,i}|\widetilde M_e(0)^{-1}(i,i-m)|,
\]

one has

\[
\sum_m(1+|m|)^r d_0(m)<\infty.
\tag{3.7}
\]

Applying a separate inverse theorem to each block and only afterwards taking a
supremum would not justify (3.7); the direct sum is essential.

## 4. A common complex parameter disk

Define on the same direct sum

\[
\mathbb G=\bigoplus_e P_I T(g)P_I.
\]

Exactly as in (3.2),

\[
\|\mathbb G\|_{C^{1,r}(\Lambda)}
\le C_r\|g\|_{\mathcal A_r}.
\tag{4.1}
\]

The algebra `C^{1,r}` is a Banach algebra for `r>0`.  Choose `rho>0` so that

\[
|z|\,C_{alg}\|\mathbb M_0^{-1}\|_{C^{1,r}}
 \|\mathbb G\|_{C^{1,r}}<\frac12
\qquad(|z|\le\rho).
\tag{4.2}
\]

Then

\[
\mathbb M_z^{-1}
=\sum_{k\ge0}(-z\mathbb M_0^{-1}\mathbb G)^k
 \mathbb M_0^{-1}
\tag{4.3}
\]

converges in `C^{1,r}`, uniformly on the closed disk.  Taking the diagonal
suprema in this single direct sum gives (1.1)--(1.2), with one common envelope
`d` valid for all events and all complex parameters on a slightly smaller
disk.

This removes the old band-truncation restriction `2q+1<p`: no spatial
regularity is spent in obtaining a common complete-event inverse envelope.

## 5. Two long legs and a doubled moment

Consider a future interval `F_R={1,...,R}`.  Put `f_z=c+zg`, and let

\[
Q_{R,z}(x)
=\widehat c(0)-u_R(z)M_{R,x}(z)^{-1}v_R(z)
\tag{5.1}
\]

be the complete-event Schur complement for an occupied origin.  The diagonal
is independent of `z` because a half-period-odd direction has zero mean; for
the present localization lemma one may simply retain the corresponding affine
diagonal term if the mean is not fixed.

Let

\[
a(m)=|\widehat c(m)|+\rho|\widehat g(m)|,
\qquad e=a*d.
\tag{5.2}
\]

The polynomial weight is submultiplicative, so

\[
e\in\ell^1_r(\mathbb Z),
\qquad
\|e\|_{\ell^1_r}\le C_r\|a\|_{\ell^1_r}\|d\|_{\ell^1_r}.
\tag{5.3}
\]

Restriction to a finite future only deletes summands.  Therefore, uniformly in
`R,x,z`,

\[
|(u_RM_{R,x}^{-1})_j|+|(M_{R,x}^{-1}v_R)_j|
\le C e(j).
\tag{5.4}
\]

If two complete future words differ only at site `j`, the event matrices differ
by `plus_or_minus e_j e_j^*`.  The resolvent identity gives

\[
|Q_{R,z}(x)-Q_{R,z}(y)|
\le C e(j)^2.
\tag{5.5}
\]

The product retains the moments of both legs:

\[
\sum_{j\ge1}(1+j)^{2r}e(j)^2
\le
\left(\sup_j(1+j)^r e(j)\right)
\sum_j(1+j)^r e(j)
\le\|e\|_{\ell^1_r}^2.
\tag{5.6}
\]

This is the decisive estimate.  Replacing each leg separately by the pointwise
bound `O(j^{-r})` would lose the summability recorded in (5.6).

## 6. Infinite-future conditional and logarithm

Adding the last future site and using block inversion expresses
`Q_{R+1,z}-Q_{R,z}` as two effective endpoint couplings times a bounded scalar
Schur inverse.  The same envelope gives

\[
|Q_{R+1,z}-Q_{R,z}|\le C e(R+1)^2.
\tag{6.1}
\]

The right side is summable.  Hence the finite-future conditionals converge
uniformly, in the future word and on smaller complex disks, to a holomorphic
continuous conditional `G_z(1|x)`; put `G_z(0|x)=1-G_z(1|x)`.

At `z=0`, the complete-event inverse bound (3.4) gives

\[
G_0(\xi|x)\ge\delta
\]

for both emitted symbols.  Shrinking the disk keeps both conditional values in
a common simply connected region separated from zero.  Define

\[
\ell_z(\xi x)=\log G_z(\xi|x)
\]

with the continued real branch.  The logarithm is uniformly Lipschitz there,
so (5.5) gives a sequence `beta_j` satisfying

\[
\sup_{|z|\le\rho'}\sup_{x\stackrel{\ne j}=y,\xi}
|\ell_z(\xi x)-\ell_z(\xi y)|\le\beta_j,
\qquad
\sum_j(1+j)^{2r}\beta_j<\infty.
\tag{6.2}
\]

For real legal `z`, this continuous version is the true right-to-left DPP
conditional: finite Schur complements are exact complete-event conditionals,
and martingale convergence identifies their limit.

## 7. Parameter derivatives and the moment-variation scale

For each fixed `j,x,y,xi`, the difference in (6.2) is holomorphic in `z`.
Cauchy's formula on a smaller disk gives, for every fixed derivative order and
in particular for `k=0,...,4`, a common sequence `beta_j^{(k)}` with

\[
\sup_{z,x\stackrel{\ne j}=y,\xi}
|\partial_z^k\ell_z(\xi x)-\partial_z^k\ell_z(\xi y)|
\le\beta_j^{(k)},
\qquad
\sum_j(1+j)^{2r}\beta_j^{(k)}<\infty.
\tag{7.1}
\]

If two futures agree through coordinate `n`, change the remaining coordinates
one at a time and pass to the limit.  Then

\[
\operatorname{var}_n(\partial_z^k\ell_z)
\le\sum_{j>n}\beta_j^{(k)}.
\tag{7.2}
\]

In particular, when `r>=1`,

\[
\sum_{n\ge0}(n+1)
 \operatorname{var}_n(\partial_z^k\ell_z)
\le C\sum_{j\ge1}(1+j)^2\beta_j^{(k)}<\infty.
\tag{7.3}
\]

Thus all derivatives needed for second-order response in `s=z^2` lie in the
first-moment variation space.  This conclusion includes the endpoint `r=1`;
it does not replace the weighted moment by a borderline pointwise
`O(n^{-2})` assertion.

## 8. Parity factorization

If, in addition,

\[
c(\theta+1/2)=c(\theta),
\qquad g(\theta+1/2)=-g(\theta),
\]

then with `D_{jj}=(-1)^j`,

\[
T(c-zg)=D T(c+zg)D.
\]

Every complete-event diagonal commutes with `D`, so all complete-event
determinants and Schur complements are invariant under `z -> -z`.  Hence
`G_z` and `ell_z` are even Banach-holomorphic families and factor through
`s=z^2`.  For `r>=1`, their first two `s` derivatives satisfy the uniform
first-moment variation estimate (7.3).

## 9. Scope

The proof establishes the common complete-event envelope and its doubled
influence moment.  It does not by itself prove entropy response; that is done in
`moment_response_and_entropy.md`.

The only external theorem used here is Fang--Shin's norm-controlled inversion,
with all of its parameters mapped above.  The proof does not use the invalid
Dobrushin A1/A2 import, and it does not infer a common family envelope by
interchanging a supremum and an infinite sum.  The direct-sum construction is
what makes that step legitimate.
