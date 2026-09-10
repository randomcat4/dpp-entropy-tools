# C4 finite-response repair at the original `p>4` threshold

Status: **PROVED AS AN AUTHOR PROOF / PENDING_REVIEW**.

This file supersedes the threshold conclusion of `c4_response_p8.md` but preserves that file as the earlier coarse attempt.  The old estimate

\[
\mathcal R:\mathcal B_b\to\mathcal B_{b-2}
\]

is valid but non-sharp.  Tracking the first generated disagreement and then using the complete-connection relaxation during the remaining time gives the sharper bound

\[
\boxed{\mathcal R:\mathcal B_b\to\mathcal B_{b-1}},\qquad b>1.
\]

Two Poisson inverses therefore require only the DPP memory exponent `a=p/2` to satisfy `a>2`, exactly `p>4`.  This bypasses the inapplicable Dobrushin A1/A2 import.  It uses the true affine kernel `K_t=T(c)+tT(g)`, all complete events through the PR66 conditional, and the true stationary configuration entropy rate.

The result is an author theorem dependent on the conditionally retained PR66 complete-event inverse/two-leg lemmas and the independently accepted regularity-free PR53 matching bound.  It is not yet an independent acceptance, and novelty is not assessed.

## 1. Exact theorem and inherited inputs

Let

\[
\mathcal A_p=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^p|\widehat u(m)|<\infty\right\},\qquad p>4.
\]

Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and let `delta<=c<=1-delta`.  Put `mu=\widehat c(0)`.  For an odd `k` with `\widehat g(k)\ne0`, set

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there is `epsilon>0` such that `c+t g` is legal and

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`.

The inherited PR66 localization input is used only in the following form.  Set

\[
q=\frac{p+2}{4},\qquad a=2q-1=\frac p2>2.
\tag{1.1}
\]

On one common complex `z`-disk, every complete-event Schur complement is nonzero and the normalized one-sided conditional `G_z` satisfies

\[
\sup_{x\stackrel{\ne j}=y}
|\log G_z(\xi\mid x)-\log G_z(\xi\mid y)|
\le C(1+j)^{-2q}.
\tag{1.2}
\]

Here the two futures differ only at site `j`, and the bound is uniform in the emitted symbol `xi`, the future and the finite conditioning limit.  No Dobrushin interaction theorem is assumed below.

## 2. Parameter derivatives retain the memory exponent

Write `ell_z(\xi x)=log G_z(\xi|x)`.  On a smaller complex disk, the difference in (1.2) is a holomorphic function of `z` with the same uniform bound.  Cauchy's formula therefore gives, for every fixed `r=0,1,2,3,4`,

\[
\sup_{x\stackrel{\ne j}=y}
|\partial_z^r\ell_z(\xi x)-\partial_z^r\ell_z(\xi y)|
\le C_r(1+j)^{-2q}.
\tag{2.1}
\]

This is a shorter rigorous version of differentiating every resolvent product: parameter derivatives do not consume spatial decay because the complete-event complex disk is uniform.

If two futures agree in their first `n` coordinates, telescope one coordinate at a time beyond `n`.  Since `2q>1`,

\[
\operatorname{var}_n(\partial_z^r\ell_z)
\le C_r\sum_{j>n}(1+j)^{-2q}
\le C'_r(1+n)^{-a}.
\tag{2.2}
\]

The half-period gauge `D_{jj}=(-1)^j` gives

\[
T(c-zg)=D\,T(c+zg)\,D.
\]

Every event diagonal commutes with `D`, so every complete-event determinant and Schur complement is invariant under `z -> -z`.  Hence `G_z` and `ell_z` are even Banach-holomorphic functions and factor through

\[
s=z^2.
\]

For physical `s=t^2>=0`, write `G_s,ell_s,nu_s`.  Equation (2.2) implies that `ell_s` and its first two `s`-derivatives are locally uniformly bounded in the polynomial variation space `B_a` defined next.

## 3. Polynomial variation spaces and transfer operators

Let `X={0,1}^N`.  For `b>0`, define

\[
\operatorname{var}_nF=\sup\{|F(x)-F(y)|:x_1^n=y_1^n\},
\]

\[
\mathcal B_b=\left\{F\in C(X):
\|F\|_b:=\|F\|_\infty+\sup_{n\ge1}(1+n)^b\operatorname{var}_nF<\infty\right\}.
\tag{3.1}
\]

For physical `s`, define the normalized transfer operator

\[
(\mathcal L_sF)(x)=\sum_{\xi=0}^1G_s(\xi\mid x)F(\xi x).
\tag{3.2}
\]

The DPP future law satisfies `nu_s L_s=nu_s`, and `L_s 1=1`.  If

\[
A_{j,s}=\partial_s^j\mathcal L_s,\qquad j=1,2,
\]

then, for every `0<b<=a`, multiplication by the `B_a` coefficient and the prepend map give

\[
A_{j,s}:\mathcal B_b\to\mathcal B_b
\tag{3.3}
\]

uniformly.  Normalization gives `A_{j,s}1=0`.

The `B_a`-valued `C^2` dependence follows from the common complex disk and Cauchy remainders, not merely from pointwise differentiation.

## 4. BFG relaxation for an arbitrary `B_b` observable

This section uses Bressaud--Fernandez--Galves only at the exact coupling level, rather than citing summable variation as a response theorem.

Fix `1<b<=a`.  From (2.2), after changing a uniform constant,

\[
\frac{G_s(\xi\mid x)}{G_s(\xi\mid y)}
\ge \exp[-C_b(1+m)^{-b}]
=1-\gamma_m^{(b)}
\tag{4.1}
\]

whenever the two histories agree in their first `m` sites, where

\[
\gamma_m^{(b)}:=1-\exp[-C_b(1+m)^{-b}].
\tag{4.2}
\]

This is a decreasing sequence, `gamma_0<1`, it is summable for `b>1`, and it is comparable to `(1+m)^{-b}`.  It is a valid larger coupling majorant; the canonical choice in BFG is not required by their condition (4.1).

Let `S_n` be BFG's dominating chain and `gamma_n^*=P(S_n=0)`.  Their Proposition 1 gives a maximal coupling whose current-disagreement probability is bounded by `gamma_n^*`.  Their equation (5.11) gives the first-return law

\[
P(\tau=k+1)=\gamma_k^{(b)}\prod_{i=0}^{k-1}(1-\gamma_i^{(b)}).
\tag{4.3}
\]

Because the sequence is summable, the infinite product is positive, and therefore

\[
P(\tau=k+1)\asymp(1+k)^{-b}.
\tag{4.4}
\]

For `F in B_b`, BFG's coupling calculation (their equations (5.4)--(5.9)) applies with

\[
\operatorname{var}_kF\le \|F\|_b(1+k)^{-b}
\le C_b\|F\|_bP(\tau=k+1).
\tag{4.5}
\]

Their renewal convolution and Proposition 2(iv) then give

\[
\boxed{
\operatorname{osc}(\mathcal L_s^nF)
\le C_b\|F\|_b(1+n)^{-b}.}
\tag{4.6}
\]

The constants are common for `s` in a sufficiently small physical interval.  Integrating one endpoint against `nu_s` yields

\[
\|\mathcal L_s^n(F-\nu_sF)\|_\infty
\le C_b\|F\|_b(1+n)^{-b}.
\tag{4.7}
\]

This is a derived consequence of the printed BFG coupling proof.  It is not the false assertion that their displayed `V_phi` theorem already contains every `B_b` observable.

## 5. The first-disagreement refinement

The loss in the earlier `p>8` draft came from bounding all early times by the total probability of any coupling failure.  The following estimate retains when the first failure occurs.

### Lemma 5.1 (joint initial-memory/relaxation estimate)

Let `1<b<=a`.  Uniformly for small physical `s`,

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le C_b\|F\|_b\left[
(1+m+n)^{-b}
+\sum_{r=0}^{n-1}(1+m+r)^{-a}(1+n-r)^{-b}
\right].
\tag{5.1}
\]

#### Proof

Start two maximal-coupled chains from futures agreeing through coordinate `m`.  Let `sigma` be the first generated disagreement.  Conditional on agreement through generation `r-1`, the two current histories agree in at least `m+r` most recent sites.  By (4.1) with exponent `a`,

\[
P(\sigma=r)\le C(1+m+r)^{-a}.
\tag{5.2}
\]

On `sigma>=n`, all `n` generated symbols agree, so the terminal `F`-difference is at most `var_{m+n}F`.

On `sigma=r<n`, condition on the two histories immediately after that disagreement.  Each marginal of the remaining coupling is the correct chain from its own history.  Hence the conditional difference of the two terminal expectations is bounded by

\[
\operatorname{osc}(\mathcal L_s^{n-r-1}F)
\le C_b\|F\|_b(1+n-r)^{-b}
\]

by (4.6).  Summing over `r` proves (5.1).  QED.

### Lemma 5.2 (one-power Poisson loss)

For `1<b<=a`, define

\[
\Pi_sF=F-\nu_sF,
\qquad
\mathcal R_sF=\sum_{n=0}^\infty\mathcal L_s^n\Pi_sF.
\tag{5.3}
\]

Then the series converges uniformly and

\[
\boxed{
\mathcal R_s:\mathcal B_b\longrightarrow\mathcal B_{b-1}}
\tag{5.4}
\]

is uniformly bounded:

\[
\|\mathcal R_sF\|_{b-1}\le C_b\|F\|_b.
\tag{5.5}
\]

Moreover

\[
(I-\mathcal L_s)\mathcal R_sF=\Pi_sF,
\qquad
\nu_s(\mathcal R_sF)=0.
\tag{5.6}
\]

#### Proof

Uniform convergence follows from (4.7), since `b>1`.  Centering does not change variation.  Sum (5.1) over `n`.  The first term gives

\[
\sum_{n\ge0}(1+m+n)^{-b}=O((1+m)^{1-b}).
\]

For the second term, put `l=n-r` and exchange the two nonnegative sums:

\[
\sum_{n\ge1}\sum_{r=0}^{n-1}
(1+m+r)^{-a}(1+n-r)^{-b}
\le
\left(\sum_{r\ge0}(1+m+r)^{-a}\right)
\left(\sum_{l\ge1}(1+l)^{-b}\right).
\]

This is `O((1+m)^{1-a})`, hence `O((1+m)^{1-b})` because `b<=a`.  This proves (5.5).  Equation (5.6) follows by telescoping the partial sums and using (4.7); stationarity gives the centering identity.  QED.

The one-power loss is the load-bearing new mathematical conclusion.  It makes the original threshold possible:

\[
a>2\quad\Longleftrightarrow\quad p>4.
\tag{5.7}
\]

## 6. A finite second-order response lemma

### Lemma 6.1

Let `G_s`, `0<=s<s_0`, be a normalized, uniformly non-null finite-alphabet kernel family.  Assume

\[
\sup_s\|\partial_s^j\log G_s\|_{\mathcal B_a}<\infty,
\qquad j=0,1,2,
\tag{6.1}
\]

with `a>2`, and assume the ratio coupling bound used above uniformly in `s`.  Let `nu_s` be the unique compatible invariant law.  If `F_s` is a `C^2` family in `B_a`, then

\[
s\mapsto\nu_s(F_s)
\]

has two continuous right derivatives at `s=0` and is `C^2` for positive `s` in a smaller interval.

For a fixed observable `F`, suppressing the parameter in the notation,

\[
D\nu(F)=\nu(A_1\mathcal RF),
\tag{6.2}
\]

\[
D^2\nu(F)=
\nu(A_2\mathcal RF)
+2\nu\bigl(A_1\mathcal R(A_1\mathcal RF)\bigr).
\tag{6.3}
\]

The operator `R` always centers its argument as in (5.3).  For a moving observable,

\[
\begin{aligned}
\frac{d^2}{ds^2}\nu_s(F_s)
={}&\nu_s(F_s'')
+2\nu_s(A_{1,s}\mathcal R_sF_s')
+\nu_s(A_{2,s}\mathcal R_sF_s)\\
&+2\nu_s\bigl(A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF_s)\bigr).
\end{aligned}
\tag{6.4}
\]

#### Proof

The BFG uniqueness criterion applies because the polynomial continuity sequence is summable.  Weak continuity of `nu_s` follows from compactness: every weak subsequential limit is invariant for the uniform limit operator, and uniqueness identifies it with `nu_s`.

For nearby `u,s`, invariance and the Poisson identity give the exact formula

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{6.5}
\]

Indeed `Pi_sF=(I-L_s)R_sF` and `nu_uI=nu_uL_u`.  Since

\[
F\in B_a\xrightarrow{\mathcal R_s}B_{a-1}
\xrightarrow{A_{1,s}}B_{a-1},
\]

dividing (6.5) by `u-s` proves (6.2).

For the second derivative, write `u=s+h`,

\[
\frac{\mathcal L_{s+h}-\mathcal L_s}{h}
=A_{1,s}+\frac h2A_{2,s}+o(h)
\tag{6.6}
\]

as an operator on every `B_b`, `b<=a`.  Apply (6.5) once to `F` and once to the fixed observable `A_{1,s}R_sF`.  The second application is legal because

\[
A_{1,s}\mathcal R_sF\in B_{a-1},
\qquad
\mathcal R_s:B_{a-1}\to B_{a-2},
\]

and `a-1>1`.  Expanding (6.5) to second order gives (6.3).  Formula (6.4) is the ordinary Leibniz expansion.

For continuity, note first that the series defining `R_sF_s` is uniformly convergent in sup norm by (4.7), termwise continuous, and uniformly bounded in `B_{b-1}` by Lemma 5.2.  The elementary interpolation fact

\[
\|U_n\|_\infty\to0,\quad \sup_n\|U_n\|_{B_c}<\infty
\quad\Longrightarrow\quad
\|U_n\|_{B_{c-\eta}}\to0
\tag{6.7}
\]

for every `0<eta<c` follows by splitting variations at a fixed memory cutoff.  Hence `s -> R_sF_s` is continuous in every `B_{b-1-eta}`.  Apply this twice, choosing total interpolation loss smaller than `a-2`.  Every term in (6.4) is then continuous in sup norm, proving the stated `C^2` response.  QED.

This is the required finite response result: two response orders, two Poisson inverses, one polynomial memory power lost at each inverse, and no pressure analyticity theorem.

## 7. Canonical finite-memory boundary error

Freeze the future after coordinate `N` and define the normalized memory-`N` kernel

\[
G_s^{[N]}(\xi\mid x)
=G_s(\xi\mid x_1,\ldots,x_N,0,0,\ldots).
\tag{7.1}
\]

For `j=0,1,2` and every `b<a`, (6.1) gives

\[
\|\partial_s^j(\log G_s-\log G_s^{[N]})\|_{B_b}
\le C_{b,j}N^{b-a}.
\tag{7.2}
\]

For `m>=N`, use the `m^{-a}` variation of the untruncated function; for `m<N`, use twice the `N^{-a}` sup error.  This proves (7.2) directly.

Let `nu_s^{[N]}`, `R_s^{[N]}` denote the finite-memory objects.  On the quotient `B_b/constants`,

\[
\mathcal R_s^{[N]}-\mathcal R_s
=\mathcal R_s^{[N]}(\mathcal L_s^{[N]}-\mathcal L_s)\mathcal R_s.
\tag{7.3}
\]

Together with (6.5), (6.2)--(6.4), and the one-power maps, (7.3) gives the following explicit response boundary estimate.  If `2<b<a` and `F_s^{[N]}` approximates `F_s` with the same `B_b` rate through two derivatives, then

\[
\max_{0\le j\le2}
\left|\partial_s^j\left[
\nu_s^{[N]}(F_s^{[N]})-\nu_s(F_s)
\right]\right|
\le C_{b,F}N^{b-a}.
\tag{7.4}
\]

Equivalently, choosing `b=2+eta`, `0<eta<a-2`, gives

\[
O\bigl(N^{-(a-2-eta)}\bigr).
\tag{7.5}
\]

This is a canonical conditional-memory error, not an inference from a list of finite-volume curvature signs.  For the entropy application take `F_s=ell_s`; (7.2) supplies the observable hypothesis.

## 8. Entropy response without pressure analyticity

For every stationary finite-alphabet process with the displayed future conditional,

\[
h_s=-\nu_s(\ell_s).
\tag{8.1}
\]

At `s=0`, the half-period-even kernel has no cross-parity entries, so the even and odd sublattices are independent.  For every physical `s=t^2`, restriction to either parity is unchanged because `g` has only odd Fourier modes.  Moreover `ell_0` at the origin depends only on the origin's parity future.  Therefore

\[
\nu_s(\ell_0)=\nu_0(\ell_0).
\tag{8.2}
\]

Consequently the true entropy deficit has the exact conditional form

\[
D(s):=h_0-h_s
=\nu_s(\ell_s-\ell_0).
\tag{8.3}
\]

Lemma 6.1 makes `D` twice continuously right-differentiable at zero.  Since the observable in (8.3) vanishes at zero,

\[
D'(0)=\nu_0(\ell'_0).
\]

Normalization gives

\[
(\mathcal L_0\ell'_0)(x)
=\sum_\xi G_0(\xi\mid x)\frac{G'_0(\xi\mid x)}{G_0(\xi\mid x)}
=\sum_\xi G'_0(\xi\mid x)=0.
\]

Invariance hence yields

\[
D'(0)=0.
\tag{8.4}
\]

Write

\[
D(s)=A s^2+o(s^2).
\tag{8.5}
\]

The independently accepted PR53 matching/negative-association inequality is regularity-free and gives, for every physical legal `t`,

\[
D(t^2)\ge\frac12 d_{\rm Ber}
\left(\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2\right).
\tag{8.6}
\]

Expanding the binary relative entropy and comparing with (8.5),

\[
A\ge
\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}
=2\alpha_k.
\tag{8.7}
\]

Since `D` is `C^2` in `s`,

\[
\frac{d^2}{dt^2}h(c+t g)
=-2D'(t^2)-4t^2D''(t^2)
=-12A t^2+o(t^2).
\tag{8.8}
\]

Thus the centered fourth-order coefficient exists in the Peano/response sense and equals `-24A`, so equivalently

\[
h''(t)=\frac{h^{[4]}(0)}2t^2+o(t^2),
\qquad h^{[4]}(0)=-24A.
\tag{8.9}
\]

We do **not** overstate (8.9) as full classical `C^4` regularity at every nonzero parameter; the theorem only needs the `C^2` response in `s=t^2`, which rigorously supplies the curvature expansion.

Finally,

\[
\frac{d^2}{dt^2}\left[h(c+t g)+\alpha_k t^4\right]
=-12(A-\alpha_k)t^2+o(t^2)
\le-12\alpha_k t^2+o(t^2)<0
\]

for all sufficiently small nonzero `t`; the second derivative is zero at `t=0`.  Shrinking the legal interval proves the stated concavity.

## 9. Exact map to Tanaka 2205.12561

Tanaka's abstract perturbation paper is a useful assumptions check but is not the load-bearing theorem here.  At a fixed `s`, the natural identification is

\[
\lambda=1,\quad h=1,\quad P=1\otimes\nu_s,\quad Q=\mathcal L_s-P.
\]

Tanaka's reduced inverse `(Q-I)^{-1}` is the negative of the Poisson inverse on centered observables.  Theorem 2.10 requires this reduced inverse to be bounded on each strong space itself.  Our natural polynomial scale proves instead

\[
\mathcal R:B_b\to B_{b-1},
\]

so that same-space hypothesis is not met.  The Gouëzel--Liverani route quoted in Tanaka also assumes an exponentially contracting strong Lasota--Yorke term, which has not been proved here.  One could encode the two successive losses in recursive graph domains, but then the work is precisely the direct two-Poisson argument of Lemma 6.1.  No automatic application of Tanaka is claimed.

## 10. Source pins, scope and failure ledger

1. Bressaud--Fernandez--Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, EJP 4 (1999), arXiv:math/9806132: ratio condition and maximal coupling, printed pp. 5--8; equations (5.4)--(5.11), printed pp. 8--9; polynomial return estimate Proposition 2(iv), printed pp. 12--14.
2. H. Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:2205.12561: Theorem 2.8, printed pp. 12--13; same-space reduced-resolvent requirement in Theorem 2.10, pp. 13--14; GL.3 and Theorem 3.20, pp. 33--35.
3. The Dobrushin 1974 A1/A2 theorem is deliberately not used.  Its exponential-cardinality and null-state defects in PR66 remain exactly as recorded in `import_closure_review.md`.

The earlier `p>8` proof remains a useful coarse checkpoint but its two-power loss is superseded by Lemma 5.2.  The present author proof repairs the original `p>4` quantifier at the response level.  It does not claim a whole legal interval, `p<=4`, arbitrary measurable symbols, an entropy counterexample, independent verification, or novelty.