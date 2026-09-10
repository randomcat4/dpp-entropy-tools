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

No inclusion-only probability, spectral entropy, observation-basis rotation,
or `L`-affine path is used.

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

almost everywhere. The parity hypotheses are not needed until Section 8.

There are a radius `rho>0` and a single nonnegative sequence
`d in l^1_r(Z)` such that

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

The envelope is common to all windows, complete words and complex parameters.

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

with the usual supremum modification at infinity. Their Theorem 2 states that,
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

The theorem's strict condition becomes `r>0`. It does not require Toeplitz or
self-adjoint structure. Its norm control is essential: bare inverse-closedness
applied separately to each event would not give a common summable envelope.

## 3. Simultaneous direct sum of every complete event

The set

\[
\mathscr E=\{(I,x):I\Subset\mathbb Z,\ x\in\{0,1\}^I\}
\]

is countable. Enumerate it by `e in N`. On one copy of `l^2(Z)` define

\[
\widetilde M_e(0)
=P_I\{T(c)-I_{Z_x}\}P_I+(I-P_I).
\tag{3.1}
\]

This is the event matrix on `I`, extended by the identity with zero
cross-boundary entries.

Let

\[
\Lambda=\mathbb Z\times\mathbb N\subset\mathbb R^2,
\qquad
\mathbb M_0=\bigoplus_{e\in\mathscr E}\widetilde M_e(0)
\]

on `l^2(Lambda)`. The half-plane lattice is relatively separated. For a
nonzero horizontal displacement `m`, a corresponding entry of a block is
zero or `\widehat c(m)`. Diagonal entries are uniformly bounded and vertical
off-block entries vanish. Hence

\[
\|\mathbb M_0\|_{C^{1,r}(\Lambda)}
\le C_r\{1+\|c\|_{\mathcal A_r}\}.
\tag{3.2}
\]

### Uniform invertibility

For one event, order occupied coordinates before vacant coordinates and let
`J=I_S\oplus(-I_Z)`. For `v=(u,w)`, the cross terms cancel in the real part:

\[
\operatorname{Re}\langle v,J M_{I,x}(0)v\rangle
=\langle u,K_{SS}u\rangle
 +\langle w,(I-K_{ZZ})w\rangle
\ge\delta\|v\|_2^2.
\tag{3.3}
\]

Since `J` is unitary,

\[
\|M_{I,x}(0)v\|_2\ge\delta\|v\|_2,
\qquad
\|M_{I,x}(0)^{-1}\|_{2\to2}\le\delta^{-1}.
\tag{3.4}
\]

The extension (3.1) has inverse norm at most
`max(1,delta^{-1})`. Thus the direct sum is invertible and

\[
\|\mathbb M_0^{-1}\|_{2\to2}
\le\max(1,\delta^{-1}).
\tag{3.5}
\]

Fang--Shin Theorem 2 applied once to this single direct sum gives

\[
\mathbb M_0^{-1}\in C^{1,r}(\Lambda),
\qquad
\|\mathbb M_0^{-1}\|_{C^{1,r}}
\le C(r,\delta,\|c\|_{\mathcal A_r}).
\tag{3.6}
\]

For

\[
d_0(m)=\sup_{e,i}|\widetilde M_e(0)^{-1}(i,i-m)|,
\]

the geometry of the block direct sum turns (3.6) into

\[
\sum_m(1+|m|)^r d_0(m)<\infty.
\tag{3.7}
\]

The supremum over events is already inside the BGS diagonal sum; it is not
interchanged with that sum afterwards.

## 4. A common complex parameter disk

Define on the same direct sum

\[
\mathbb G=\bigoplus_e P_I T(g)P_I.
\]

Then

\[
\|\mathbb G\|_{C^{1,r}(\Lambda)}
\le C_r\|g\|_{\mathcal A_r}.
\tag{4.1}
\]

The algebra `C^{1,r}` is a Banach algebra for `r>0`. Choose `rho>0` so that

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

converges in `C^{1,r}`, uniformly on the closed disk. Taking the horizontal
diagonal envelope of this one direct sum gives (1.1)--(1.2). Equivalently, if
`b` is the horizontal envelope of `mathbb G`, an explicit common majorant is

\[
d=\sum_{k\ge0}\rho^k(d_0*b)^{*k}*d_0,
\tag{4.4}
\]

which belongs to `l^1_r` after decreasing `rho` if necessary.

This removes the old band-truncation restriction `2q+1<p`: no Fourier moment
is spent in obtaining the common complete-event inverse envelope.

## 5. Two long legs and a doubled moment

Consider a future interval `F_R={1,...,R}`. Put `f_z=c+zg`, and let

\[
Q_{R,z}(x)
=\widehat f_z(0)-u_R(z)M_{R,x}(z)^{-1}v_R(z)
\tag{5.1}
\]

be the complete-event Schur complement for an occupied origin.

Let

\[
a(m)=|\widehat c(m)|+\rho|\widehat g(m)|,
\qquad
\lambda=a*d,
\qquad
 e=a+\lambda+a*d*a.
\tag{5.2}
\]

All three sequences belong to `l^1_r`. Restriction to a finite future only
deletes summands, so uniformly in `R,x,z`,

\[
|(u_RM_{R,x}^{-1})_j|+|(M_{R,x}^{-1}v_R)_j|
\le C\lambda(j)\le C e(j).
\tag{5.3}
\]

If two complete future words differ only at site `j`, their event matrices
differ by `plus_or_minus e_j e_j^*`. The rank-one resolvent identity gives

\[
|Q_{R,z}(x)-Q_{R,z}(y)|
\le C e(j)^2.
\tag{5.4}
\]

The product keeps the moments of both legs:

\[
\sum_{j\ge1}(1+j)^{2r}e(j)^2
\le
\left(\sup_j(1+j)^r e(j)\right)
\sum_j(1+j)^r e(j)
\le\|e\|_{\ell^1_r}^2.
\tag{5.5}
\]

Replacing each leg by a bare pointwise power bound would discard (5.5).

## 6. Infinite-future conditional and logarithm

Adding site `R+1` and using block inversion gives

\[
Q_{R+1,z}-Q_{R,z}
=-(b-u_RM^{-1}c_R)S^{-1}(b'-r_RM^{-1}v_R),
\tag{6.1}
\]

where `c_R,r_R` are the two Toeplitz coupling vectors to the new site and
`S^{-1}` is an entry of the inverse enlarged complete-event matrix. The first
effective endpoint coupling is bounded by

\[
a(R+1)+(a*d*a)(R+1),
\]

and the same holds for the second. Thus the corrected common bound is

\[
|Q_{R+1,z}-Q_{R,z}|\le C e(R+1)^2.
\tag{6.2}
\]

The extra `a*d*a` term is required; writing only `a*d` for this endpoint
operation would omit the coupling from the old future to the newly added
site. It does not change the weighted moment because `e in l^1_r`.

The right side of (6.2) is summable. Hence the finite-future conditionals
converge uniformly, in the future word and on smaller complex disks, to a
holomorphic continuous conditional `G_z(1|x)`; put
`G_z(0|x)=1-G_z(1|x)`.

At `z=0`, the complete-event inverse bound (3.4) gives

\[
G_0(\xi|x)\ge\delta
\]

for both emitted symbols. Shrinking the disk keeps both conditional values in
a common simply connected region separated from zero. Define

\[
\ell_z(\xi x)=\log G_z(\xi|x)
\]

with the continued real branch. The logarithm is uniformly Lipschitz there,
so (5.4) gives a fixed sequence `beta_j` such that

\[
\sup_{|z|\le\rho'}\sup_{x\stackrel{\ne j}=y,\xi}
|\ell_z(\xi x)-\ell_z(\xi y)|\le\beta_j,
\qquad
\sum_j(1+j)^{2r}\beta_j<\infty.
\tag{6.3}
\]

For real legal `z`, finite Schur complements are exact complete-event
conditionals, and martingale convergence identifies their continuous limit
with the true right-to-left DPP conditional.

## 7. Parameter derivatives and the moment-variation scale

For each fixed `j,x,y,xi`, the difference in (6.3) is holomorphic in `z`.
Cauchy's formula on a smaller disk gives, for every fixed order and in
particular `k=0,...,4`, fixed envelopes `beta_j^{(k)}` with

\[
\sup_{z,x\stackrel{\ne j}=y,\xi}
|\partial_z^k\ell_z(\xi x)-\partial_z^k\ell_z(\xi y)|
\le\beta_j^{(k)},
\qquad
\sum_j(1+j)^{2r}\beta_j^{(k)}<\infty.
\tag{7.1}
\]

If two futures agree through coordinate `n`, change the remaining coordinates
one at a time and pass to the limit. Then

\[
\operatorname{var}_n(\partial_z^k\ell_z)
\le\sum_{j>n}\beta_j^{(k)}.
\tag{7.2}
\]

In particular, when `r>=1`, Tonelli gives

\[
\sum_{n\ge0}(n+1)
 \operatorname{var}_n(\partial_z^k\ell_z)
\le C\sum_{j\ge1}(1+j)^2\beta_j^{(k)}<\infty.
\tag{7.3}
\]

Thus all derivatives needed for second-order response in `s=z^2` lie in the
first-moment variation space. This includes the endpoint `r=1`; it does not
replace the weighted moment by a borderline pointwise `O(n^{-2})` assertion.

## 8. Parity factorization

Assume now

\[
c(\theta+1/2)=c(\theta),
\qquad g(\theta+1/2)=-g(\theta).
\]

With `D_{jj}=(-1)^j`,

\[
T(c-zg)=D T(c+zg)D.
\]

Every complete-event diagonal commutes with `D`, so all complete-event
determinants and Schur complements are invariant under `z -> -z`. Hence
`G_z` and `ell_z` are even Banach-holomorphic families and factor through
`s=z^2`. For `r>=1`, their first two `s` derivatives satisfy (7.3).

## 9. Scope

This proof establishes the common complete-event envelope and its doubled
influence moment. Entropy response is proved in
`moment_response_and_entropy.md`.

The only external theorem used here is Fang--Shin norm-controlled inversion,
with all parameters mapped above. The proof does not use the invalid
Dobrushin A1/A2 import and does not infer a family envelope by exchanging a
supremum with an infinite sum.
