# Arbitrary strict `A_0` center: finite-range preconditioning and `C^4` true entropy rate

Status: **AUTHOR PROOF / PENDING INDEPENDENT REVIEW.**

This note closes the regularity bridge announced in the first PR117 checkpoint. It deliberately does **not** require a norm-controlled inverse theorem in the unweighted convolution-dominated algebra. The load-bearing estimate separates:

1. an operator-norm contraction, which only sees the small Wiener **tail** of a finite-range truncation; and
2. exponential configuration localization of the inverse of the finite-range reference, which is used only to approximate normalized trace observables by finite-support observables.

This separation is what removes the false requirement that an inverse `ell^1` envelope norm multiplied by the truncation tail must tend to zero.

All finite laws below are complete occupied/vacant DPP laws.

## 1. Setup and finite-range reference

Let real `c,g in A_0` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and assume a strict spectral margin

\[
\delta\le c(\theta)\le1-\delta\quad\text{a.e.}
\tag{1.1}
\]

for some `0<delta<1/2`. Since `c in A_0`, its Fourier series converges uniformly. Choose a half-period-even finite Fourier truncation `c^0` keeping the zero mode and satisfying

\[
\|c-c^0\|_W<\varepsilon_0,
\qquad
\delta_0:=\delta-\varepsilon_0>0.
\tag{1.2}
\]

Then

\[
\delta_0\le c^0\le1-\delta_0.
\tag{1.3}
\]

Write

\[
r=c-c^0,\qquad e_t=r+t g.
\tag{1.4}
\]

We shall decrease `epsilon_0` and then choose `tau>0` so that

\[
\eta:=\sup_{|t|\le\tau}\|e_t\|_W
\tag{1.5}
\]

is as small as required below. This is always possible because finite Fourier truncations converge in the Wiener norm and `g in A_0`.

For a finite interval `Lambda` and complete word `x`, let

\[
M^0_{\Lambda,x}=T_\Lambda(c^0)-I_{Z_x},
\qquad
R^0_{\Lambda,x}=(M^0_{\Lambda,x})^{-1}.
\tag{1.6}
\]

The standard complete-event coercivity proof is repeated here because it is needed uniformly. If `S=Z_x^c` and `J=I_S\oplus(-I_{Z_x})`, then the cross terms in

\[
\operatorname{Re}\langle v,J M^0_{\Lambda,x}v\rangle
\]

cancel, while the two diagonal blocks contribute `T_S(c^0)` and `I-T_{Z_x}(c^0)`. Hence

\[
\operatorname{Re}\langle v,J M^0_{\Lambda,x}v\rangle
\ge\delta_0\|v\|_2^2,
\]

so

\[
\boxed{\|R^0_{\Lambda,x}\|_{2\to2}\le\delta_0^{-1}}
\tag{1.7}
\]

for every volume and every complete word.

Let `w` be the Fourier range of `c^0`. Since `M^0` is Hermitian, `\|M^0\|\le1`, and its spectrum avoids `(-delta_0,delta_0)`, one may write

\[
(R^0) = M^0\sum_{q\ge0}(I-(M^0)^2)^q.
\tag{1.8}
\]

The `q`-th term has bandwidth `(2q+1)w` and operator norm at most `(1-delta_0^2)^q`. Therefore there are constants `C_0,a_0>0`, depending on `c^0,delta_0` but not on `Lambda,x`, such that

\[
|(R^0_{\Lambda,x})_{ij}|\le C_0e^{-a_0|i-j|}.
\tag{1.9}
\]

No positivity of `M^0` is used; self-adjointness plus the two-sided spectral gap is enough.

## 2. A finite-support operator approximation of every event inverse

For an integer `R>=2w`, and each pair `i,j in Lambda`, let

\[
N_R(i,j)=\{k\in\Lambda:\operatorname{dist}(k,\{i,j\})\le R\}.
\]

Let `R^{[R]}_{\Lambda,x}(i,j)` be the `(i,j)` entry of the inverse of the complete-event matrix restricted to `N_R(i,j)` when `|i-j|<=R`, and set it to zero when `|i-j|>R`. This entry depends only on the spins in `N_R(i,j)`.

Compare the full matrix with the block-diagonal matrix obtained by deleting the couplings across the boundary of `N_R(i,j)`. The deleted coupling has uniformly bounded operator norm and, because `c^0` has range `w`, is supported in `O(w)` boundary coordinates. The resolvent identity together with (1.9) on the full and block inverses yields

\[
|R^0_{\Lambda,x}(i,j)-R^{[R]}_{\Lambda,x}(i,j)|
\le C_1e^{-a_1R}
\quad(|i-j|\le R),
\tag{2.1}
\]

with constants independent of `Lambda,x,i,j`. For `|i-j|>R`, (1.9) gives the same form after decreasing `a_1`.

Taking row and column sums and using the exponential spatial bound gives

\[
\boxed{
\sup_{\Lambda,x}
\|R^0_{\Lambda,x}-R^{[R]}_{\Lambda,x}\|_{2\to2}
\le C_2e^{-a_2R}.}
\tag{2.2}
\]

After increasing a fixed `R_*`, we may and do assume

\[
\sup_{R\ge R_*,\Lambda,x}\|R^{[R]}_{\Lambda,x}\|
\le B:=\delta_0^{-1}+1.
\tag{2.3}
\]

The crucial feature is that `B` is independent of the Fourier range `w`. The rate `a_2` and the starting radius `R_*` may be very poor; only their positivity/ finiteness is needed.

If `R>=R_*`, each diagonal entry of a product of `m` matrices `R^{[R]}` and deterministic shifts depends on at most

\[
C m(R+1)
\tag{2.4}
\]

binary coordinates. This cardinality bound is independent of the sizes of the shift displacements.

## 3. Exact non-product complete-event factorization

Let

\[
E_{\Lambda,t}=T_\Lambda(e_t).
\]

For every complete word,

\[
M_{\Lambda,x}(t)=M^0_{\Lambda,x}+E_{\Lambda,t},
\]

and hence

\[
\boxed{
p_{\Lambda,t}(x)
=p^0_\Lambda(x)
\det(I+R^0_{\Lambda,x}E_{\Lambda,t}).}
\tag{3.1}
\]

Choose the truncation and `tau` so that

\[
B\eta<\rho<1
\tag{3.2}
\]

for some fixed `rho`. This is possible because `B=delta_0^{-1}+1` stays bounded as `epsilon_0` is made small; for example first require `epsilon_0<delta/2`, so `B<=2/delta+1`, and then make `eta` smaller than `(2B)^{-1}`.

By (1.7), after possibly shrinking further,

\[
\|R^0E_t\|\le\delta_0^{-1}\eta<1.
\tag{3.3}
\]

Thus the ordinary real log likelihood ratio has the exact trace series

\[
L_{\Lambda,t}(x)
:=\log\frac{p_{\Lambda,t}(x)}{p^0_\Lambda(x)}
=\sum_{m\ge1}\frac{(-1)^{m+1}}m
\operatorname{Tr}(R^0_{\Lambda,x}E_{\Lambda,t})^m.
\tag{3.4}
\]

The `m=1` term need not vanish and is retained.

## 4. Complete-event differentiation for finite-support observables

For the actual path `c+t g`, choose `tau` also so that

\[
\delta/2\le c+t g\le1-\delta/2
\quad(|t|\le\tau).
\tag{4.1}
\]

For a complete event on a distinct finite support `J`, put

\[
M_{J,x}(t)=T_J(c+t g)-I_{Z_x},\qquad G_J=T_J(g).
\]

The coercivity argument gives `\|M^{-1}\|<=2/delta`. Jacobi's formula and its Bell-polynomial iterates therefore imply, for every fixed `0<=q<=4`,

\[
|\partial_t^q p_{J,t}(x)|
\le p_{J,t}(x) A_q |J|^q,
\tag{4.2}
\]

where `A_q` depends on `delta,g,q` but not on `J,x,t`. Consequently every bounded `t`-independent local observable `F` satisfies

\[
|\partial_t^q E_tF|
\le A_q|J|^q\|F\|_\infty.
\tag{4.3}
\]

For a local observable polynomial of degree at most four in `t`, Leibniz gives the analogous bound with its first four sup norms. This retains the full score/Fisher and atom-acceleration contributions because it differentiates the complete atom before summation.

## 5. Operator-localized trace observables

Write the Toeplitz perturbation as the absolutely convergent shift sum

\[
E_{\Lambda,t}=\sum_{d\in\mathbb Z} e_t(d)S_{d,\Lambda},
\qquad
\sum_d|e_t(d)|\le\eta,
\tag{5.1}
\]

where each partial shift has operator norm at most one.

For a displacement tuple `d=(d_1,...,d_m)`, define the normalized trace observable

\[
F_{m,d,\Lambda}(x)
=\frac1{|\Lambda|}\operatorname{Tr}
R^0_xS_{d_1}\cdots R^0_xS_{d_m}.
\tag{5.2}
\]

Let `F^{[R]}_{m,d,\Lambda}` be obtained by replacing every `R^0` by `R^{[R]}`. Equations (2.2)-(2.3) and telescoping a product give

\[
\|F_{m,d,\Lambda}-F^{[R]}_{m,d,\Lambda}\|_\infty
\le m C_2 e^{-a_2R} B^{m-1}
\tag{5.3}
\]

for `R>=R_*`, uniformly in the displacement tuple and the volume. Here `|Tr A|/|Lambda|<=\|A\|` was used; no entrywise absolute path sum appears.

Set

\[
\Delta_R F=F^{[R]}-F^{[R-1]}
\quad(R>R_*),
\]

and use `F^{[R_*]}` as the base term. Then

\[
\|\Delta_R F_{m,d,\Lambda}\|_\infty
\le C_3mB^{m-1}e^{-a_3R}.
\tag{5.4}
\]

Each diagonal summand in `\Delta_R F` is a local observable on at most `C m(R+1)` spins by (2.4), regardless of the magnitude of the shifts `d_j`. Applying (4.3) to each translated diagonal summand and averaging anchors gives

\[
|\partial_t^q E_t\Delta_R F_{m,d,\Lambda}|
\le C_q m^{q+1}(R+1)^qB^{m-1}e^{-a_3R},
\tag{5.5}
\]

for `0<=q<=4`, before differentiating the deterministic coefficients `e_t(d_j)`.

Because

\[
\sum_{R\ge R_*}(R+1)^qe^{-a_3R}<\infty,
\tag{5.6}
\]

summing the localization shells costs only a constant `C_q`.

Now differentiate a length-`m` term in (3.4). If `ell` derivatives hit the affine coefficients `e_t(d_j)`, at most `m^ell` assignments occur, every marked coefficient contributes `|g_hat(d)|`, and every unmarked one contributes `|e_t(d)|`. Summing all displacement tuples uses only

\[
\sum_d|g_hat(d)|=\|g\|_W,
\qquad
\sum_d|e_t(d)|\le\eta.
\tag{5.7}
\]

Combining (5.5)-(5.7), for every `0<=q<=4`, gives

\[
\boxed{
\sup_{\Lambda,|t|\le\tau}
\left|\partial_t^q
\frac1{|\Lambda|}E_t\operatorname{Tr}(R^0E_t)^m\right|
\le C_q m^{2q+1} B^{m-1}\eta^{m-q}(1+\|g\|_W)^q.}
\tag{5.8}
\]

Finitely many `m<q` are absorbed in the constant. By (3.2), the right side is bounded by a polynomial in `m` times `rho^{m-q}`. Therefore

\[
\sum_{m\ge1}\frac1m
\sup_{\Lambda,|t|\le\tau}
\left|\partial_t^q
\frac1{|\Lambda|}E_t\operatorname{Tr}(R^0E_t)^m\right|<\infty
\tag{5.9}
\]

through order four.

This is the central estimate. It uses operator-norm localization to keep the geometric factor `B eta<1`; it never multiplies the Wiener tail by an `ell^1` norm of the reference inverse.

## 6. Thermodynamic limit of the relative entropy density

Define

\[
d_{0,\Lambda}(t)
=\frac1{|\Lambda|}D(p_{\Lambda,t}\|p^0_\Lambda)
=\frac1{|\Lambda|}E_tL_{\Lambda,t}.
\tag{6.1}
\]

Fix first `m`, a displacement tuple, and a localization radius `R`. The corresponding diagonal summand in `F^{[R]}` depends on finitely many translated coordinates. Away from the interval boundary its expectation is exactly translation invariant under the infinite stationary DPP with symbol `c+t g`. The fraction of admissible anchors tends to one. Thus each localized coefficient and its first four parameter derivatives has a thermodynamic limit.

The shell majorant (5.5), the displacement `ell^1` sums (5.7), and finally the length majorant (5.9) permit dominated convergence in the order

1. volume;
2. localization radius;
3. displacement tuples;
4. walk length.

Hence

\[
\boxed{
d_0(t):=\lim_{n\to\infty}d_{0,\Lambda_n}(t)
\in C^4([ -\tau,\tau])}
\tag{6.2}
\]

and normalized finite-volume derivatives converge through order four.

## 7. The finite-range reference cross-entropy density

It remains to treat

\[
\ell_{0,\Lambda}(t)
=\frac1{|\Lambda|}E_t\log p^0_\Lambda(X_\Lambda).
\tag{7.1}
\]

For the strict finite-range reference DPP `c^0`, the exact one-sided complete-event conditional probability is a Schur complement involving `(M^0_{[1,R],x})^{-1}`. Equations (1.7)-(1.9) imply uniformly:

- the conditional probabilities stay in a compact subinterval of `(0,1)`;
- the length-`R` conditional converges exponentially to an infinite-future conditional `G_0`;
- `phi_0=log G_0` is bounded and has exponential variations.

For completeness, the second point follows by comparing two future lengths through a cut. The Schur-complement difference contains propagation from the origin coupling support to the cut and back; (1.9) supplies an exponential factor. The logarithm is Lipschitz because of uniform nonnullness.

Write a telescoping cylinder decomposition

\[
\phi_0=\phi_0^{[R_*]}+
\sum_{R>R_*}\Delta_R\phi_0,
\qquad
\|\Delta_R\phi_0\|_\infty\le C e^{-aR},
\tag{7.2}
\]

where `\Delta_R\phi_0` depends on at most `R+1` future coordinates. Equation (4.3) then yields

\[
|\partial_t^qE_t\Delta_R\phi_0|
\le C_q(R+1)^qe^{-aR},
\qquad0\le q\le4.
\tag{7.3}
\]

so

\[
\ell_0(t):=E_t\phi_0\in C^4([-\tau,\tau]).
\tag{7.4}
\]

The finite-volume chain rule

\[
\log p^0_{[1,n]}(x)
=\sum_{j=1}^n
\log P_0(X_j=x_j\mid X_{j+1},\ldots,X_n)
\tag{7.5}
\]

and exponential conditional convergence show that the total difference between (7.5) and `sum_j phi_0(shift^j x)` is `O(1)`, uniformly in `n,x`. The same cylinder-shell argument applies after differentiating the expectation under `p_t`. Therefore

\[
\boxed{
\lim_{n\to\infty}\ell_{0,[1,n]}^{(q)}(t)
=\ell_0^{(q)}(t),\qquad0\le q\le4,}
\tag{7.6}
\]

locally uniformly in `t`.

No Ruelle or Dobrushin parameter-response theorem is invoked here: the reference potential is fixed, and all `t` derivatives are taken through exact complete-event marginals using (4.2).

## 8. Identification with the true configuration entropy rate

The finite identity

\[
D(p_{\Lambda,t}\|p^0_\Lambda)
=-H_\Lambda(t)-E_t\log p^0_\Lambda
\tag{8.1}
\]

uses every complete atom. Divide by volume and pass to the limits from Sections 6-7:

\[
\boxed{
h(c+t g)=-d_0(t)-\ell_0(t).}
\tag{8.2}
\]

Consequently

\[
\boxed{h(c+t g)\in C^4([-\tau,\tau]).}
\tag{8.3}
\]

Moreover the first four normalized finite-volume entropy derivatives converge to those of the true entropy rate. Since the starting finite identity is the complete Shannon law, the usual finite curvature identity

\[
H''=-\sum_x\frac{(p'_x)^2}{p_x}-\sum_xp''_x\log p_x
\]

passes as a whole; Fisher and acceleration are not selectively omitted.

## 9. Scope and the inverse-control obstruction

The proof uses no positive Fourier moment. Its only Fourier sums are the Wiener sums of `r` and `g`; physical displacement never enters the Bell differentiation cost, because local approximants depend on neighborhoods of finitely many visited endpoints rather than on every site between them.

The unweighted BGS inverse-closedness issue is therefore bypassed rather than strengthened. In particular, no assertion is made that the arbitrary-center complete-event inverse family has a common `ell^1` diagonal envelope. Such an assertion does not follow from inverse-closedness and is unnecessary here.

No whole-legal-interval sign, arbitrary measurable-symbol theorem, spectral entropy identity, or entropy counterexample is claimed.