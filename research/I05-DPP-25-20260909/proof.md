# Proof of the polynomial-class theorem

Throughout, complete DPP configuration probabilities are used. Inclusion probabilities alone never enter the entropy calculation.

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

For a Toeplitz compression, `\|T_I(u)\|_{S_q}\le\|u\|_{\mathcal A_q}`.

## 2. Uniform polynomial localization of all complete-event inverses

Let `I\subset\mathbb Z` be finite and let `x\in\{0,1\}^I`. Put

\[
Z_x=\{i\in I:x_i=0\},
\qquad
M_{I,x}:=T_I(c)-I_{Z_x}.
\]

The complete-event formula is

\[
\mathbf P_c(X_I=x)=(-1)^{|Z_x|}\det M_{I,x}.
\]

### 2.1 Dimension-free singular-value gap

After ordering occupied coordinates before vacant coordinates, write

\[
M=\begin{pmatrix}K_{SS}&K_{SZ}\\K_{ZS}&K_{ZZ}-I\end{pmatrix},
\qquad
J=I_S\oplus(-I_Z).
\]

Since `\delta I\le T_I(c)\le(1-\delta)I`, for `v=(u,w)` one has

\[
\operatorname{Re}\langle v,JMv\rangle
=
\langle u,K_{SS}u\rangle+
\langle w,(I-K_{ZZ})w\rangle
\ge\delta\|v\|_2^2.
\]

The cross terms cancel in the real part. Since `J` is unitary,

\[
\|Mv\|_2\ge\delta\|v\|_2,
\qquad
\|M^{-1}\|_{2\to2}\le\delta^{-1}.
\]

Also

\[
-(1-\delta)I\le M\le(1-\delta)I,
\qquad
\|M\|_{2\to2}\le1-\delta.
\]

These estimates are uniform in `I` and `x`.

### 2.2 Band truncation and a weighted inverse bound

Let

\[
c^{(W)}(\theta)=\sum_{|m|\le W}\widehat c(m)e^{2\pi i m\theta},
\qquad
B_{I,x}^{(W)}=T_I(c^{(W)})-I_{Z_x},
\]

and `E_I^{(W)}=T_I(c-c^{(W)})`, so that `M=B+E`.
Choose `W` first so that

\[
\|E\|_{2\to2}
\le\sum_{|m|>W}|\widehat c(m)|
\le\frac\delta4.
\]

Put `\eta=3\delta/4`. Then

\[
\sigma_{\min}(B)\ge\eta,
\qquad
\|B\|_{2\to2}\le1-\eta.
\]

Because `B` is Hermitian,

\[
B^{-1}=B\sum_{r\ge0}(I-B^2)^r,
\qquad
\|I-B^2\|_{2\to2}\le\rho:=1-\eta^2<1.
\]

The `r`-th term has bandwidth at most `(2r+1)W` and every entry is bounded by `\rho^r`. Consequently, for a constant depending only on `\delta,q`,

\[
\|B^{-1}\|_{S_q}
\le
C_{\delta,q}W^{q+1}
\sum_{r\ge0}(r+1)^{q+1}\rho^r
=:L_{\delta,q}(W).
\]

The tail satisfies

\[
\|E\|_{S_q}
\le
\sum_{|m|>W}v_q(m)|\widehat c(m)|
\le
(1+W)^{q-p}\|c\|_{\mathcal A_p}.
\]

Thus

\[
\|B^{-1}E\|_{S_q}
\le
C(c,\delta,p)W^{2q+1-p}.
\]

The exponent is negative. Increase the fixed `W`, independently of `I,x`, until the last quantity is at most `1/2`. The weighted Neumann series then gives

\[
\boxed{
\sup_{I,x}\|M_{I,x}^{-1}\|_{S_q}\le B_q<\infty.
}
\tag{2.1}
\]

This is the first point where the polynomial threshold is used.

### 2.3 A common complex parameter disk

For `f_z=c+zg`,

\[
M_{I,x}(z)=M_{I,x}(0)+zT_I(g).
\]

Since `g\in\mathcal A_p\subset\mathcal A_q`, (2.1) and another weighted Neumann series imply that, for

\[
r_0<\frac1{2B_q\|g\|_{\mathcal A_q}},
\]

all complete-event matrices are invertible on `|z|<r_0` and

\[
\boxed{
\sup_{|z|<r_0}\sup_{I,x}
\|M_{I,x}(z)^{-1}\|_{S_q}\le2B_q.
}
\tag{2.2}
\]

The radius and bound are independent of the conditioning window and configuration.

## 3. One-sided complete-event conditionals and squared remote influence

Let `F_R=\{1,\ldots,R\}` and `x\in\{0,1\}^{F_R}`. With

\[
M_{R,x}(z)=T_{F_R}(f_z)-I_{Z_x},
\]

let `u_R(z)=K_{f_z}(0,F_R)` and `v_R(z)=K_{f_z}(F_R,0)`. Since the anti-periodicity of `g` gives `\widehat g(0)=0`, the diagonal entry is the fixed number `\mu=\widehat c(0)`. The Schur-complement formula for complete event probabilities gives

\[
q_{R,z}(x)
:=\frac{\mathbf P_z(X_0=1,X_{F_R}=x)}
{\mathbf P_z(X_{F_R}=x)}
=
\mu-u_R(z)M_{R,x}(z)^{-1}v_R(z)
\tag{3.1}
\]

for real legal `z`; the right-hand side defines its holomorphic continuation for complex `z`.

### 3.1 Flipping one remote conditioned bit

If `x,y` differ only at `j\in F_R`, then

\[
M_{R,y}(z)-M_{R,x}(z)=\pm e_je_j^*.
\]

The resolvent identity yields

\[
M_{R,y}^{-1}-M_{R,x}^{-1}
=\mp M_{R,y}^{-1}e_je_j^*M_{R,x}^{-1}.
\]

The weighted row bound (2.2), submultiplicativity of `v_q`, and the weighted Fourier norms of `c,g` imply

\[
\left|(u_RM_{R,y}^{-1})_j\right|
+
\left|(M_{R,x}^{-1}v_R)_j\right|
\le C(1+j)^{-q}.
\]

Therefore

\[
\boxed{
|q_{R,z}(x)-q_{R,z}(y)|
\le C(1+j)^{-2q}
}
\tag{3.2}
\]

uniformly in `R,x,y` and on a smaller closed disk `|z|\le r_1<r_0`.

The square is essential: changing the event at `j` is a rank-one diagonal perturbation, and the Schur complement must propagate from the origin to `j` and back.

### 3.2 Adding the last conditioned site

Write the event matrix on `F_{R+1}` in block form

\[
\widetilde M=
\begin{pmatrix}M&e\\d&a\end{pmatrix},
\qquad
S=a-dM^{-1}e.
\]

Block inversion gives

\[
q_{R+1,z}-q_{R,z}
=-(u_{R+1}-u_RM^{-1}e)
S^{-1}
(v_{R+1}-dM^{-1}v_R).
\tag{3.3}
\]

Each effective coupling in parentheses is `O((1+R)^{-q})` by (2.2), and `|S^{-1}|` is uniformly bounded because it is an entry of `\widetilde M^{-1}`. Hence

\[
\boxed{
|q_{R+1,z}-q_{R,z}|
\le C(1+R)^{-2q}.
}
\tag{3.4}
\]

Since `2q>1`, the finite-future conditionals converge uniformly on `|z|\le r_1` to a holomorphic function `q_z(x_1,x_2,\ldots)`.

Passing (3.2) to the limit gives the single-coordinate influence estimate

\[
\boxed{
\sup_{x\stackrel{\ne j}=y}
|q_z(x)-q_z(y)|
\le C(1+j)^{-2q}.
}
\tag{3.5}
\]

Consequently, if two futures agree through coordinate `n`,

\[
|q_z(x)-q_z(y)|
\le C\sum_{j>n}(1+j)^{-2q}
\le C'(1+n)^{1-2q}.
\tag{3.6}
\]

### 3.3 Uniform non-nullness and the logarithmic potential

At `z=0`, the Schur complement `q_{R,0}` is positive. In the complete-event matrix enlarged by an occupied site `0`, the `(0,0)` entry of the inverse is `q_{R,0}^{-1}`. The singular-value bound therefore gives `q_{R,0}\ge\delta`. Enlarging instead by a vacant site gives `1-q_{R,0}\ge\delta`. These bounds survive the limit.

The formulas above are uniformly Lipschitz in `z` on a smaller disk. Shrink to `|z|<r_2` so that both `q_z` and `1-q_z` stay at distance at least `\delta/2` from zero. Define

\[
G_z(1x)=q_z(x),
\qquad
G_z(0x)=1-q_z(x),
\qquad
\phi_z=\log G_z,
\]

using the branches continuing the real logarithms at `z=0`. Then `G_z(0x)+G_z(1x)=1`, and (3.5)–(3.6) also hold for `\phi_z`, with changed constants.

## 4. A finite-first-moment interaction

Fix the reference future `0^\infty`. For `n\ge0`, define

\[
\phi_z^{[n]}(x_0,\ldots,x_n)
:=
\phi_z(x_0,\ldots,x_n,0,0,\ldots).
\]

Put

\[
\psi_{0,z}=\phi_z^{[0]},
\qquad
\psi_{n,z}=\phi_z^{[n]}-\phi_z^{[n-1]}
\quad(n\ge1),
\]

where the second term ignores `x_n`. The two arguments in this difference vary only at coordinate `n`; hence the single-coordinate estimate, not merely the tail-variation estimate, gives

\[
\boxed{
\|\psi_{n,z}\|_\infty\le C(1+n)^{-2q}.
}
\tag{4.1}
\]

Moreover `\sum_{n\ge0}\psi_{n,z}=\phi_z` uniformly.

Define a translation-invariant interval interaction by

\[
U_{z,[i,i+n]}(x)
:=-\psi_{n,z}(x_i,\ldots,x_{i+n}),
\qquad
U_{z,A}=0
\quad\text{for other finite }A.
\tag{4.2}
\]

For each `n`, exactly `n+1` translates of an interval of diameter `n` contain the origin. Therefore

\[
\sum_{A\ni0}\operatorname{diam}(A)\|U_{z,A}\|_\infty
\le
C\sum_{n\ge1}n(n+1)(1+n)^{-2q}<\infty,
\tag{4.3}
\]

because `q>3/2`. This is a deliberately strong, convention-independent finite-first-moment bound.

All estimates hold uniformly on compact subdisks. The Weierstrass test in the Banach norm on the left of (4.3) shows that

\[
z\longmapsto U_z
\]

is holomorphic as a finite-first-moment interaction-valued map.

This is the second point where the threshold `p>4` is used: the inverse proof requires `p>2q+1`, while (4.3) requires `q>3/2`.

## 5. Identification with the DPP and the chain-to-Gibbs bridge

For real sufficiently small `t`, the finite conditionals (3.1) are genuine DPP complete-event conditional probabilities. Their uniform limit is therefore a version of the right-to-left conditional law

\[
G_t(a x_1x_2\ldots)
=
\mathbf P_{c+tg}(X_0=a\mid X_1=x_1,X_2=x_2,\ldots).
\]

The process is non-null, and (3.6) is summable because `q>1`. Thus its right-to-left left-interval specification lies in the summable-variation class of Fernández–Maillard.

For completeness, the interaction identification can also be seen directly. If two two-sided configurations `x,y` differ only on a finite interval, then

\[
\sum_{i\in\mathbb Z}
\bigl[\phi_t(T^ix)-\phi_t(T^iy)\bigr]
\]

converges absolutely: terms to the right vanish, while terms with starting point `m` sites to the left are `O(m^{1-2q})`, which is summable. Expanding `\phi_t=\sum_n\psi_{n,t}` and using (4.3) permits absolute rearrangement; the result is exactly minus the interaction-energy difference generated by (4.2). On the other hand, multiplying the one-sided conditional probabilities from right to left gives the same exponential ratio. Hence the DPP is a Gibbs state for `U_t`.

This is the concrete bridge behind the general LIS-to-specification construction in Fernández–Maillard, Theorem 4.12. No spectral entropy formula is used.

## 6. Imported one-dimensional analyticity theorem

We use the following classical result in precisely this form.

> **Dobrushin–Cassandro–Olivieri theorem.** For a finite-alphabet, translation-invariant one-dimensional interaction with finite first moment, the Gibbs state, specific pressure/free energy, and finite correlations depend analytically on interaction parameters in a neighborhood of every real interaction. No smallness or high-temperature assumption is required. The conclusion applies to holomorphic finite-first-moment Banach-valued parameter curves.

Dobrushin proved analyticity for one-dimensional power-law interactions; Cassandro and Olivieri gave the many-body finite-first-moment formulation and a decimation/cluster-expansion proof. The stronger bound (4.3) places `U_z` inside their hypothesis without relying on a convention about orbit normalization.

Let `P(U)` denote pressure with finite-volume weights `\exp(-H_U)`. The theorem implies that `P(U_z)` and its directional derivatives are holomorphic for `z` near zero.

## 7. Evenness and analyticity in `s=t^2`

Let `D` be the diagonal gauge `D_{jj}=(-1)^j`. Half-period parity of the Fourier coefficients gives

\[
K_{c-zg}=DK_{c+zg}D.
\]

Every event diagonal `I_Z` commutes with `D`. Therefore every finite Schur complement in (3.1) is unchanged under `z\mapsto-z`, and

\[
G_{-z}=G_z,
\qquad
\phi_{-z}=\phi_z,
\qquad
U_{-z}=U_z.
\]

An even holomorphic Banach-valued function factors holomorphically through `s=z^2`; write the resulting interaction as `U_s`.

For an auxiliary scalar `\lambda`, define

\[
F(s,\lambda)=P(\lambda U_s).
\]

The imported theorem makes `F` holomorphic near `(0,1)`. For real `s=t^2\ge0`, the DPP is the Gibbs state of `U_s`. The variational principle and pressure differentiation give

\[
P(U_s)=h_s-\nu_s(e_{U_s}),
\qquad
\partial_\lambda F(s,1)=-\nu_s(e_{U_s}),
\]

so

\[
\boxed{
h_s=F(s,1)-\partial_\lambda F(s,1).
}
\tag{7.1}
\]

Thus the true configuration entropy rate is analytic in `s`, hence even and real analytic in `t`.

## 8. The quadratic term in `s` is absent

Let `\nu_t=\mathbf P_{c+tg}` and `\nu_0=\mathbf P_c`. In every finite window, the even-coordinate and odd-coordinate marginals of `\nu_t` are independent of `t`, because their kernel entries use only even Fourier indices and `\widehat g` vanishes there. At `t=0`, the cross-parity kernel entries vanish because `\widehat c` vanishes at odd indices, so the two parity sublattices are independent. Hence, exactly at every finite volume,

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

where the right side is the specific relative entropy.

The Gibbs pressure identity, with `\Delta_s=U_s-U_0`, is

\[
d(\nu_s\|\nu_0)
=P(U_0)-P(U_s)+DP(U_s)[\Delta_s].
\tag{8.2}
\]

It is analytic in `s`. Differentiating at zero, the two first-order terms cancel:

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

This cancellation is the required uniform response statement. It is not a consequence of entropy continuity alone.

## 9. Matching lower bound and strict quartic floor

The accepted PR53 matching argument uses only parity, fixed marginals, negative association, and the variational characterization of mutual information. It does not use exponential regularity. For every legal `t` and every odd `k` with `\widehat g(k)\ne0`, it gives

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

Analyticity now gives

\[
\mathcal R''(t)=12A t^2+O(t^4).
\]

Choose `\varepsilon>0` small enough that the symbol remains legal and

\[
\mathcal R''(t)\ge6C_k t^2
\qquad(|t|\le\varepsilon).
\]

For `\alpha_k=C_k/2`,

\[
\frac{d^2}{dt^2}
\left[h(c+tg)+\alpha_k t^4\right]
=-\mathcal R''(t)+12\alpha_k t^2
\le0.
\]

Thus `t\mapsto h(c+tg)+\alpha_k t^4` is concave on the nonempty interval `[-\varepsilon,\varepsilon]`.

## 10. What has and has not been proved

The theorem concerns the true infinite-volume configuration Shannon entropy rate. It does not replace it by spectral entropy, a finite-window entropy, or a scalar eigenvalue formula. It proves an existential local interval for each fixed `c,g,k`; it does not claim a radius uniform over the whole `\mathcal A_p` class. The proof is complete modulo the explicitly imported classical finite-first-moment analyticity theorem and awaits independent review.
