# Proof of the polynomial-class theorem

Throughout, complete DPP configuration probabilities are used. Inclusion probabilities alone never enter the entropy calculation. The only non-elementary imported response result is stated precisely in Section 6.

## 1. Choice of exponents

Fix `p>4` and set

\[
q:=\frac{p+2}{4}.
\]

Then

\[
q>\frac32,
\qquad
2q+1-p=\frac{4-p}{2}<0.
\]

Write `v_q(m)=(1+|m|)^q`. This weight is submultiplicative:

\[
v_q(i-j)\le v_q(i-r)v_q(r-j).
\]

For a matrix `A=(A_{ij})` indexed by a finite set `I\subset\mathbb Z`, define the weighted Schur norm

\[
\|A\|_{S_q}
:=
\max\left\{
\sup_{i\in I}\sum_{j\in I}v_q(i-j)|A_{ij}|,
\sup_{j\in I}\sum_{i\in I}v_q(i-j)|A_{ij}|
\right\}.
\]

Submultiplicativity of `v_q` gives

\[
\|AB\|_{S_q}\le\|A\|_{S_q}\|B\|_{S_q}.
\]

For every Toeplitz compression,

\[
\|T_I(u)\|_{S_q}\le\|u\|_{\mathcal A_q}.
\]

## 2. Uniform polynomial localization of every complete-event inverse

Let `I\subset\mathbb Z` be finite and `x\in\{0,1\}^I`. Put

\[
Z_x=\{i\in I:x_i=0\},
\qquad
M_{I,x}:=T_I(c)-I_{Z_x}.
\]

The full atom is

\[
\mathbf P_c(X_I=x)=(-1)^{|Z_x|}\det M_{I,x}.
\]

### 2.1 Dimension-free singular-value gap

Order occupied coordinates before vacant coordinates and write

\[
M=\begin{pmatrix}K_{SS}&K_{SZ}\\K_{ZS}&K_{ZZ}-I\end{pmatrix},
\qquad
J=I_S\oplus(-I_Z).
\]

Since `\delta I\le T_I(c)\le(1-\delta)I`, for `v=(u,w)` the mixed terms cancel in the real part and

\[
\operatorname{Re}\langle v,JMv\rangle
=
\langle u,K_{SS}u\rangle+
\langle w,(I-K_{ZZ})w\rangle
\ge\delta\|v\|_2^2.
\]

Because `J` is unitary,

\[
\|Mv\|_2\ge\delta\|v\|_2,
\qquad
\|M^{-1}\|_{2\to2}\le\delta^{-1}.
\tag{2.1}
\]

Also

\[
-(1-\delta)I\le M\le(1-\delta)I,
\qquad
\|M\|_{2\to2}\le1-\delta.
\tag{2.2}
\]

Both estimates are uniform in `I` and `x`, and they remain valid for complex Hermitian Toeplitz kernels arising from real non-even symbols.

### 2.2 Band truncation and weighted inverse bound

Let

\[
c^{(W)}(\theta)=\sum_{|m|\le W}\widehat c(m)e^{2\pi i m\theta},
\qquad
B_{I,x}^{(W)}=T_I(c^{(W)})-I_{Z_x},
\]

and `E_I^{(W)}=T_I(c-c^{(W)})`, so `M=B+E`. Choose `W` so that

\[
\|E\|_{2\to2}
\le\sum_{|m|>W}|\widehat c(m)|
\le\frac\delta4.
\]

Put `\eta=3\delta/4`. Weyl's inequality and (2.1)–(2.2) give

\[
\sigma_{\min}(B)\ge\eta,
\qquad
\|B\|_{2\to2}\le1-\eta.
\]

Since `B` is Hermitian,

\[
B^{-1}=B\sum_{r\ge0}(I-B^2)^r,
\qquad
\|I-B^2\|_{2\to2}\le\rho:=1-\eta^2<1.
\tag{2.3}
\]

The `r`-th term has bandwidth at most `(2r+1)W`; every entry is bounded by `\rho^r`. A row or column has at most `O((r+1)W)` entries in that band. Hence

\[
\|B^{-1}\|_{S_q}
\le
C_{\delta,q}W^{q+1}
\sum_{r\ge0}(r+1)^{q+1}\rho^r
=:L_{\delta,q}(W).
\tag{2.4}
\]

The tail obeys

\[
\|E\|_{S_q}
\le
\sum_{|m|>W}v_q(m)|\widehat c(m)|
\le
(1+W)^{q-p}\|c\|_{\mathcal A_p}.
\tag{2.5}
\]

Combining (2.4)–(2.5),

\[
\|B^{-1}E\|_{S_q}
\le C(c,\delta,p)W^{2q+1-p}.
\]

The exponent is negative. Increase the fixed `W`, independently of `I,x`, until the last quantity is at most `1/2`. The weighted Neumann series gives

\[
\boxed{
\sup_{I,x}\|M_{I,x}^{-1}\|_{S_q}\le B_q<\infty.
}
\tag{2.6}
\]

This is the first use of `p>4`.

### 2.3 A common complex parameter disk

For `f_z=c+zg`,

\[
M_{I,x}(z)=M_{I,x}(0)+zT_I(g).
\]

Since `g\in\mathcal A_p\subset\mathcal A_q`, (2.6) and a second weighted Neumann series imply that, for

\[
r_0<\frac1{2B_q\|g\|_{\mathcal A_q}},
\]

all complete-event matrices are invertible on `|z|<r_0` and

\[
\boxed{
\sup_{|z|<r_0}\sup_{I,x}
\|M_{I,x}(z)^{-1}\|_{S_q}\le2B_q.
}
\tag{2.7}
\]

The disk and bound are common to every conditioning window and configuration. This is precisely the kind of uniformity absent from bare smooth approximation.

## 3. One-sided complete-event conditionals and squared remote influence

Let `F_R=\{1,\ldots,R\}` and `x\in\{0,1\}^{F_R}`. Write

\[
M_{R,x}(z)=T_{F_R}(f_z)-I_{Z_x},
\]

and let `u_R(z)=K_{f_z}(0,F_R)`, `v_R(z)=K_{f_z}(F_R,0)`. Anti-periodicity gives `\widehat g(0)=0`, so the diagonal entry is the fixed number `\mu=\widehat c(0)`. The complete-event Schur complement is

\[
q_{R,z}(x)
:=\frac{\mathbf P_z(X_0=1,X_{F_R}=x)}
{\mathbf P_z(X_{F_R}=x)}
=
\mu-u_R(z)M_{R,x}(z)^{-1}v_R(z)
\tag{3.1}
\]

for real legal `z`; its right side is the holomorphic continuation for complex `z`.

### 3.1 Flipping one remote conditioned bit

If `x,y` differ only at `j\in F_R`, then

\[
M_{R,y}(z)-M_{R,x}(z)=\pm e_je_j^*.
\]

The resolvent identity gives

\[
M_{R,y}^{-1}-M_{R,x}^{-1}
=\mp M_{R,y}^{-1}e_je_j^*M_{R,x}^{-1}.
\]

The weighted row/column bound (2.7), the submultiplicativity of `v_q`, and the weighted Fourier norms of `c,g` imply

\[
\left|(u_RM_{R,y}^{-1})_j\right|
+
\left|(M_{R,x}^{-1}v_R)_j\right|
\le C(1+j)^{-q}.
\]

Thus

\[
\boxed{
|q_{R,z}(x)-q_{R,z}(y)|
\le C(1+j)^{-2q}
}
\tag{3.2}
\]

uniformly in `R,x,y` and on each smaller closed disk `|z|\le r_1<r_0`. The square is structural: a changed conditioned bit is a rank-one diagonal perturbation and the Schur complement propagates from the origin to `j` and back.

### 3.2 Adding the last conditioned site

Write the event matrix on `F_{R+1}` as

\[
\widetilde M=
\begin{pmatrix}M&e\\d&a\end{pmatrix},
\qquad
S=a-dM^{-1}e.
\]

Block inversion yields

\[
q_{R+1,z}-q_{R,z}
=-(b-u_RM^{-1}e)S^{-1}(c-dM^{-1}v_R),
\tag{3.3}
\]

where `b=K_{f_z}(0,R+1)` and `c=K_{f_z}(R+1,0)`. Each effective coupling in parentheses is `O((1+R)^{-q})` by (2.7), and `|S^{-1}|` is uniformly bounded because it is an entry of `\widetilde M^{-1}`. Therefore

\[
\boxed{
|q_{R+1,z}-q_{R,z}|
\le C(1+R)^{-2q}.
}
\tag{3.4}
\]

Since `2q>1`, the finite-future conditionals converge uniformly on smaller closed disks to a holomorphic function

\[
q_z(x_1,x_2,\ldots).
\]

Passing (3.2) to the limit gives the single-coordinate influence bound

\[
\boxed{
\sup_{x\stackrel{\ne j}=y}
|q_z(x)-q_z(y)|
\le C(1+j)^{-2q}.
}
\tag{3.5}
\]

If two futures agree through coordinate `n`, then

\[
|q_z(x)-q_z(y)|
\le C\sum_{j>n}(1+j)^{-2q}
\le C'(1+n)^{1-2q}.
\tag{3.6}
\]

### 3.3 Uniform non-nullness and logarithmic potential

At `z=0`, enlarge a future complete-event matrix by an occupied site at the origin. The `(0,0)` entry of the inverse is `q_{R,0}^{-1}`. The common inverse operator bound gives `q_{R,0}\ge\delta`. Enlarging by a vacant origin similarly gives `1-q_{R,0}\ge\delta`. These bounds survive the limit.

The formulas are uniformly Lipschitz in `z`. Shrink to `|z|<r_2` so that `q_z` and `1-q_z` remain in the right half-plane at distance at least `\delta/2` from zero. Define

\[
G_z(1x)=q_z(x),
\qquad
G_z(0x)=1-q_z(x),
\qquad
\phi_z=\log G_z,
\]

using the branches continuing the real logarithms at `z=0`. Then `G_z(0x)+G_z(1x)=1`, and (3.5)–(3.6) hold for `\phi_z` with changed constants.

## 4. A finite-first-moment interval interaction

Fix the reference future `0^\infty`. Define

\[
\phi_z^{[n]}(x_0,\ldots,x_n)
:=
\phi_z(x_0,\ldots,x_n,0,0,\ldots),
\]

and

\[
\psi_{0,z}=\phi_z^{[0]},
\qquad
\psi_{n,z}=\phi_z^{[n]}-\phi_z^{[n-1]}
\quad(n\ge1),
\]

where the second term ignores `x_n`. The two arguments differ only at coordinate `n`; hence the single-coordinate estimate gives

\[
\boxed{
\|\psi_{n,z}\|_\infty\le C(1+n)^{-2q}.
}
\tag{4.1}
\]

Moreover `\sum_{n\ge0}\psi_{n,z}=\phi_z` uniformly. Define

\[
U_{z,[i,i+n]}(x)
:=-\psi_{n,z}(x_i,\ldots,x_{i+n}),
\qquad
U_{z,A}=0
\quad\text{for other finite }A.
\tag{4.2}
\]

For each `n`, exactly `n+1` translates of an interval of diameter `n` contain the origin. Thus

\[
\boxed{
\sum_{A\ni0}\operatorname{diam}(A)\|U_{z,A}\|_\infty
\le
C\sum_{n\ge1}n(n+1)(1+n)^{-2q}<\infty.
}
\tag{4.3}
\]

This holds because `q>3/2`. It is stronger than the standard orbit-normalized finite-first-moment condition. The estimates are locally uniform on the complex disk, so the Weierstrass test proves that `z\mapsto U_z` is holomorphic in the Banach norm on the left of (4.3).

This is the second use of `p>4`: the inverse proof needs `p>2q+1`, while the convention-independent moment estimate needs `q>3/2`.

## 5. Exact identification of the DPP as the equilibrium state

Fix a small real `t` and write `\nu_t=\mathbf P_{c+tg}`. The finite Schur complements converge to its right-to-left conditional law:

\[
G_t(a\mid x_1,x_2,\ldots)
=
\nu_t(X_0=a\mid X_1=x_1,X_2=x_2,\ldots).
\tag{5.1}
\]

Let `\rho` be any shift-invariant probability measure on `\{0,1\}^{\mathbb Z}` and let `r_\rho(\cdot\mid x_1^\infty)` be its future conditional. For a stationary finite-alphabet process,

\[
h(\rho)=H_\rho(X_0\mid X_1,X_2,\ldots).
\]

Therefore the conditional cross-entropy identity gives

\[
\boxed{
h(\rho)+\rho(\phi_t)
=-\int D_{\rm KL}
\bigl(r_\rho(\cdot\mid x_1^\infty)\|G_t(\cdot\mid x_1^\infty)\bigr)
\,d\rho(x)
\le0.}
\tag{5.2}
\]

Equality holds for `\rho=\nu_t`.

For the standard specific-energy representative

\[
e_{U_t}(x)=\sum_{A\ni0}\frac1{|A|}U_{t,A}(x),
\]

stationarity and absolute convergence give

\[
\begin{aligned}
\rho(e_{U_t})
&=
\sum_{n\ge0}\frac1{n+1}
\sum_{i=-n}^{0}\rho(U_{t,[i,i+n]})\\
&=-\sum_{n\ge0}\rho(\psi_{n,t})
=-\rho(\phi_t).
\end{aligned}
\tag{5.3}
\]

Combining (5.2)–(5.3),

\[
h(\rho)-\rho(e_{U_t})\le0,
\]

with equality at `\nu_t`. The variational principle for absolutely summable interactions therefore yields

\[
\boxed{P(U_t)=0,
\qquad
\nu_t\text{ is an equilibrium state for }U_t.}
\tag{5.4}
\]

This is the required chain-to-Gibbs bridge. It uses the true future conditional and the true configuration entropy rate; no spectral entropy identity is involved. A longer sign audit appears in `equilibrium_bridge.md`.

## 6. Imported one-dimensional response theorem

We use the following classical theorem in the restricted form needed here.

> **Dobrushin finite-first-moment analyticity theorem.** Let the single-site state space be finite and let `V_z` be a translation-invariant one-dimensional interaction depending holomorphically on one or finitely many complex parameters in a neighborhood of a real parameter value. Assume locally uniformly that the interaction has finite first moment. Then the real interaction has a unique Gibbs/equilibrium state, and the specific pressure and expectations of bounded local observables have holomorphic continuations in the parameters near that value.

Dobrushin's theorem is formulated for general one-dimensional classical lattice systems with power-law-decaying potentials and states that the specific free energy and correlation functions depend analytically on the potential. Modern literature records its threshold as finite first moment. Our stronger bound (4.3) places `U_z` inside that class regardless of whether a source uses orbit normalization.

Cassandro–Olivieri give a separate decimation proof for one-dimensional many-body finite-first-moment potentials and complex interaction parameters. Their concrete lattice-gas coordinate formulation is not used here to encode arbitrary block functions; it serves only as an independent mechanism check. The load-bearing general-spin input is Dobrushin's theorem.

Applying the theorem to `U_z` identifies the unique analytic equilibrium branch with the DPP branch from (5.4). It also applies jointly to the two-parameter family `\lambda U_z` near `\lambda=1`.

## 7. Evenness and analyticity in `s=t^2`

Let `D` be the diagonal gauge `D_{jj}=(-1)^j`. Half-period Fourier support gives

\[
K_{c-zg}=DK_{c+zg}D.
\]

Every event diagonal `I_Z` commutes with `D`. Consequently all finite complete-event determinants and Schur complements are invariant under `z\mapsto-z`, and

\[
G_{-z}=G_z,
\qquad
\phi_{-z}=\phi_z,
\qquad
U_{-z}=U_z.
\]

An even Banach-holomorphic function factors holomorphically through `s=z^2`; denote the resulting interaction by `U_s`. Define

\[
F(s,\lambda)=P(\lambda U_s).
\]

Section 6 makes `F` holomorphic near `(0,1)`. For real `s=t^2\ge0`, the DPP `\nu_s` is the equilibrium state of `U_s`. With the convention

\[
P(U)=\sup_\rho\{h(\rho)-\rho(e_U)\},
\]

pressure differentiation gives

\[
\partial_\lambda F(s,1)=-\nu_s(e_{U_s}).
\]

Using the equilibrium identity,

\[
\boxed{
h_s=F(s,1)-\partial_\lambda F(s,1).}
\tag{7.1}
\]

Thus the true stationary configuration entropy rate is analytic in `s`, hence even and real analytic in `t`.

## 8. The entropy deficit starts at order `t^4`

Let `\nu_t=\mathbf P_{c+tg}` and `\nu_0=\mathbf P_c`. In every finite window, the even-coordinate and odd-coordinate marginals of `\nu_t` are independent of `t`, because restriction to either parity uses only even Fourier indices and `\widehat g` vanishes there. At `t=0`, the cross-parity kernel entries vanish because `\widehat c` vanishes at odd indices, so the parity sublattices are independent. Hence, exactly in every finite volume,

\[
D(\nu_t^{(n)}\|\nu_0^{(n)})
=H(\nu_0^{(n)})-H(\nu_t^{(n)}).
\]

After division by `n` and passage to the limit,

\[
\mathcal R(t):=h(c)-h(c+tg)
=d(\nu_t\|\nu_0),
\tag{8.1}
\]

where the right side is specific relative entropy.

Put `\Delta_s=U_s-U_0`. For equilibrium states, the pressure identity is

\[
d(\nu_s\|\nu_0)
=P(U_0)-P(U_s)+DP(U_s)[\Delta_s].
\tag{8.2}
\]

It is analytic in `s`. At `s=0`, `\Delta_0=0`, and differentiation gives

\[
\frac d{ds}d(\nu_s\|\nu_0)\bigg|_{s=0}
=-DP(U_0)[U'_0]+DP(U_0)[U'_0]=0.
\]

Therefore, for some real `A`,

\[
\boxed{
\mathcal R(t)=A t^4+O(t^6).
}
\tag{8.3}
\]

This cancellation is the uniform response statement that entropy continuity alone cannot supply.

## 9. Matching lower bound and strict quartic floor

The accepted PR53 matching argument uses parity, fixed marginals, negative association, and the variational characterization of mutual information; it does not use exponential Fourier decay. For every legal `t` and every odd `k` with `\widehat g(k)\ne0`, it gives

\[
\mathcal R(t)
\ge
\frac12\,d_{\mathrm{Ber}}
\left(
\mu^2-|\widehat g(k)|^2t^2
\,\middle\|\,
\mu^2
\right).
\tag{9.1}
\]

The binary relative-entropy expansion is

\[
\frac12\,d_{\mathrm{Ber}}(q-at^2\|q)
=
\frac{a^2}{4q(1-q)}t^4+O(t^6).
\]

With `q=\mu^2` and `a=|\widehat g(k)|^2`, (8.3) and (9.1) imply

\[
A\ge C_k
:=\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}>0.
\tag{9.2}
\]

Analyticity gives

\[
\mathcal R''(t)=12A t^2+O(t^4).
\]

Choose `\varepsilon>0` so small that the symbol remains legal and

\[
\mathcal R''(t)\ge6C_k t^2
\qquad(|t|\le\varepsilon).
\]

For

\[
\alpha_k=\frac{C_k}{2}
=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)},
\]

one has

\[
\frac{d^2}{dt^2}
\left[h(c+tg)+\alpha_k t^4\right]
=-\mathcal R''(t)+12\alpha_k t^2
\le0.
\]

Thus `t\mapsto h(c+tg)+\alpha_k t^4` is concave on the nonempty interval `[-\varepsilon,\varepsilon]`.

## 10. Scope and status

The proof concerns the true infinite-volume configuration Shannon entropy rate. It does not replace it by spectral entropy, a finite-window entropy, or a scalar eigenvalue formula. It proves an existential interval for each fixed `c,g,k`; it does not claim a radius uniform over the unbounded class `\mathcal A_p`.

The author proof is complete modulo the explicitly imported classical Dobrushin theorem, as is normal for a theorem built on a cited response result. Independent review must still audit the exact first-moment convention and the application of that theorem; author self-check is not independent acceptance.
