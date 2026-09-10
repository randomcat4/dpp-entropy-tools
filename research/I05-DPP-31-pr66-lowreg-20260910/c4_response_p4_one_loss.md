# C4 response at the original threshold: one-power Poisson loss

Status: **PROVED AS AN AUTHOR REPAIR / PENDING INDEPENDENT REVIEW**.

This file supersedes the threshold conclusion of `c4_response_p8.md`.  It does not use the invalid Dobrushin A1/A2 import.  The earlier two-power Poisson estimate remains a valid coarse bound, but it is not sharp: following the Bressaud--Fernandez--Galves agreement-length chain through its whole excursion shows that one Poisson inverse loses only one polynomial memory power.  Since half-period parity reduces fourth order in `t` to second order in `s=t^2`, two Poisson inverses require only `p/2>2`, exactly `p>4`.

The full finite-memory second-derivative estimate (6.7) in `c4_response_p8.md` is **withdrawn as unproved and is not used here**.  This file gives instead a direct infinite-volume response proof and an explicit, proved cutoff error for the Poisson/correlation sums.  A quantitative spatial memory-truncation estimate is stated only in the stronger range where the displayed norm calculation closes.

The argument concerns the true stationary DPP configuration law for the physical affine symbol `c+t g`.  Every conditional is obtained from complete-event determinants.  No spectral entropy, fermionic entropy, rotated observation basis, or `L`-affine surrogate is used.

## 1. DPP input and the exact memory exponent

Fix `p>4` and put

\[
q=\frac{p+2}{4},
\qquad
a=2q-1=\frac p2>2.
\tag{1.1}
\]

Let real `c,g in A_p` satisfy the frozen PR66 assumptions:

\[
c(\theta+1/2)=c(\theta),
\qquad
g(\theta+1/2)=-g(\theta),
\qquad g\ne0,
\qquad \delta\le c\le1-\delta.
\tag{1.2}
\]

For the finite future `F_R={1,...,R}` and a complete future configuration `x`, write

\[
M_{R,x}(t)=T_{F_R}(c+tg)-I_{Z_x}.
\]

The conditionally accepted internal PR66 inverse lemma gives, on one common complex `t`-disk,

\[
\sup_{R,x,t}\|M_{R,x}(t)^{-1}\|_{S_q}<\infty.
\tag{1.3}
\]

The complete-event conditional at the origin is the Schur complement

\[
Q_{R,t}(x)=\mu-u_tM_{R,x}(t)^{-1}v_t,
\qquad \mu=\widehat c(0).
\tag{1.4}
\]

It converges uniformly to the true right-to-left conditional `G_t(1|x)`; `G_t(0|x)=1-G_t(1|x)`.  On a smaller common disk both values stay uniformly away from zero.

### Lemma 1.1 -- parameter derivatives retain the two-leg decay

For every fixed `r>=0`, and in particular for `0<=r<=4`, there is `C_r` such that, uniformly in the finite future and after passage to the infinite future,

\[
\sup_{x\stackrel{\ne j}=y}
\left|\partial_t^r\log G_t(b|x)-
\partial_t^r\log G_t(b|y)\right|
\le C_r(1+j)^{-2q},
\qquad b\in\{0,1\}.
\tag{1.5}
\]

Consequently

\[
\operatorname{var}_n(\partial_t^r\log G_t)
\le C_r'(1+n)^{-a}.
\tag{1.6}
\]

#### Proof

A flip at future coordinate `j` changes `M` by `plus_or_minus e_j e_j^*`.  The resolvent identity factors the conditional difference into an origin-to-`j` leg and a `j`-to-origin leg.  Each leg is `O((1+j)^(-q))` by (1.3).

For parameter derivatives,

\[
\partial_t^rM_t^{-1}
=(-1)^r r!M_t^{-1}(T(g)M_t^{-1})^r.
\tag{1.7}
\]

The weighted Schur class `S_q` is a Banach algebra and `T(g)` is uniformly bounded in it.  Differentiating the rank-one resolvent factorization therefore inserts only bounded `S_q` factors between the same two long legs.  Derivatives of `u_t,v_t` replace a Toeplitz row or column by the corresponding row or column of `T(g)` and obey the same weighted bound.  Thus every differentiated term is still `O((1+j)^(-2q))`.  Uniform non-nullness and the finite Faà di Bruno formula transfer this estimate from `G_t` to `log G_t`.

If two futures agree through `n`, flip the remaining coordinates one at a time and sum (1.5):

\[
\sum_{j>n}(1+j)^{-2q}=O((1+n)^{1-2q})=O((1+n)^{-a}).
\]

This proves (1.6).  The same bounds on a complex circle imply Banach-valued holomorphy in the polynomial-variation spaces below by the Cauchy formula.  QED.

The diagonal gauge `D_jj=(-1)^j` gives

\[
T(c-tg)=D T(c+tg)D.
\tag{1.8}
\]

Every complete-event diagonal commutes with `D`, hence every finite complete-event probability and every Schur-complement conditional is unchanged by `t -> -t`.  Thus `G_t` is an even Banach-holomorphic family.  It factors through `s=t^2`; write the factor as `G_s`.  After shrinking the disk, `G_s` is a positive normalized kernel also for a small real interval around `s=0`.  From (1.6),

\[
\sup_s\|\partial_s^j\log G_s\|_{B_a}<\infty,
\qquad j=0,1,2.
\tag{1.9}
\]

## 2. Polynomial variation spaces and transfer operators

Let `X={0,1}^N`.  Define

\[
\operatorname{var}_nF=
\sup\{|F(x)-F(y)|:x_1^n=y_1^n\}
\]

and, for `b>0`,

\[
B_b=\left\{F:\|F\|_b:=\|F\|_\infty+
\sup_{n\ge1}(1+n)^b\operatorname{var}_nF<\infty\right\}.
\tag{2.1}
\]

For a normalized kernel `G_s`, let

\[
(L_sF)(x)=\sum_{z=0}^1G_s(z|x)F(zx).
\tag{2.2}
\]

Let `nu_s` be its compatible stationary law.  For positive `s=t^2` this is the true DPP law; for the harmless negative-`s` extension it is the unique complete-connection law supplied by the coupling below.  Write

\[
\Pi_sF=F-\nu_sF.
\]

For `j=1,2`, set `A_{j,s}=partial_s^j L_s`.  Equation (1.9), multiplication, and the prepend map imply

\[
A_{j,s}:B_b\longrightarrow B_b
\quad\text{boundedly and locally uniformly whenever }0<b\le a.
\tag{2.3}
\]

## 3. The BFG agreement chain and a one-power potential bound

This section uses only the actual coupling objects in Bressaud--Fernandez--Galves, not an unstated higher-order response theorem.

Their condition (4.1) asks for a decreasing sequence `gamma_m`, `gamma_0<1`, such that histories agreeing through `m` satisfy

\[
\frac{G_s(z|x)}{G_s(z|y)}\ge1-\gamma_m.
\tag{3.1}
\]

By (1.9), for every fixed `b` with `1<b<a` one can choose a common decreasing majorant, uniform in small `s`, with

\[
0\le\gamma_m<1,
\qquad
\gamma_m\le C_b(1+m)^{-b}.
\tag{3.2}
\]

Indeed the canonical ratio loss is at most `1-exp(-C(1+m)^(-a))`; use a finite decreasing prefix below one and an exact polynomial tail of exponent `b`.

The BFG maximal coupling has a consecutive-agreement process `T_n`.  Their equations (4.18)--(4.20) show that `T_n` stochastically dominates the Markov chain `S_n` with

\[
S_{n+1}=\begin{cases}
S_n+1,&\text{with probability }1-\gamma_{S_n},\\
0,&\text{with probability }\gamma_{S_n}.
\end{cases}
\tag{3.3}
\]

The comparison works as well when the initial histories already agree through `m`: use (3.3) started from `S_0=m` in the same induction.

### Lemma 3.1 -- relaxation and occupation potential

Let `w_b(k)=(1+k)^(-b)`, `b>1`, and let `E_m` denote expectation for (3.3) started at `m`.  Uniformly in small `s`,

\[
E_0 w_b(S_n)\le C_b(1+n)^{-b},
\tag{3.4}
\]

and

\[
V_b(m):=\sum_{n\ge0}E_mw_b(S_n)
\le C_b'(1+m)^{1-b}.
\tag{3.5}
\]

#### Proof of (3.4)

Put `u_n=P_0(S_n=0)`.  BFG Proposition 2(iv) gives

\[
u_n=O((1+n)^{-b})
\tag{3.6}
\]

for a polynomially decreasing `gamma`.  At time `n`, the event `S_n=k` means that the chain was at zero at time `n-k` and then made `k` consecutive upward moves.  Therefore, with

\[
r_k=\prod_{j=0}^{k-1}(1-\gamma_j)\le1,
\]

one has the exact identity

\[
P_0(S_n=k)=u_{n-k}r_k,
\qquad0\le k\le n.
\tag{3.7}
\]

Hence

\[
E_0w_b(S_n)
\le C\sum_{k=0}^n(1+k)^{-b}(1+n-k)^{-b}
\le C'(1+n)^{-b},
\]

because `b>1`.  This is (3.4).

#### Proof of (3.5)

Let `tau_m` be the first reset to zero for the chain started at `m`.  Before that reset the chain follows `m,m+1,...`, so

\[
\sum_{n<\tau_m}w_b(S_n)
\le\sum_{n\ge0}(1+m+n)^{-b}
\le C(1+m)^{1-b}.
\tag{3.8}
\]

Moreover

\[
P_m(\tau_m<\infty)
=1-\prod_{j=m}^{\infty}(1-\gamma_j)
\le\sum_{j=m}^{\infty}\gamma_j
\le C(1+m)^{1-b}.
\tag{3.9}
\]

By (3.4), `V_b(0)<infinity`.  The strong Markov property at `tau_m` now gives

\[
V_b(m)
\le C(1+m)^{1-b}
+P_m(\tau_m<\infty)V_b(0)
\le C'(1+m)^{1-b}.
\]

QED.

The point missed by the earlier two-power estimate is (3.9): a coupling failure is not charged independently at every later time.  Once the whole excursion is grouped, its reset probability already has the tail `m^(1-b)`.

## 4. Poisson inverse: exactly one lost power

If histories `x,y` agree through `m`, couple the two chains and use the stochastic domination above.  For `F in B_b`,

\[
|L_s^nF(x)-L_s^nF(y)|
\le\|F\|_b E_mw_b(S_n).
\tag{4.1}
\]

Taking `m=0`, integrating one endpoint against `nu_s`, and using (3.4) gives

\[
\|L_s^n\Pi_sF\|_\infty
\le C_b(1+n)^{-b}\|F\|_b.
\tag{4.2}
\]

Define the reduced Poisson inverse

\[
Q_sF=\sum_{n=0}^{\infty}L_s^n\Pi_sF.
\tag{4.3}
\]

The series is uniformly convergent for `b>1`.  Constants disappear when taking variations, so (4.1) and (3.5) give

\[
\operatorname{var}_m(Q_sF)
\le C_b(1+m)^{1-b}\|F\|_b.
\]

Thus

\[
\boxed{Q_s:B_b\longrightarrow B_{b-1}\quad\text{boundedly for every }b>1.}
\tag{4.4}
\]

Also

\[
(I-L_s)Q_sF=\Pi_sF,
\qquad \nu_s(Q_sF)=0.
\tag{4.5}
\]

This is the load-bearing improvement over `c4_response_p8.md`.

### Proved correlation-sum boundary error

For the time cutoff

\[
Q_s^{[M]}F=\sum_{n=0}^{M}L_s^n\Pi_sF,
\]

(4.2) gives the uniform error

\[
\boxed{
\|Q_sF-Q_s^{[M]}F\|_\infty
\le C_b(M+1)^{1-b}\|F\|_b.
}
\tag{4.6}
\]

If a second Poisson inverse is applied to an observable in `B_{b-1}`, its corresponding cutoff error is

\[
O((M+1)^{2-b}),
\qquad b>2.
\tag{4.7}
\]

Equations (4.6)--(4.7) are the boundary/remainder estimates used for finite response.  They control the actual infinite correlation sums and do not extrapolate a finite-window curvature sign.

## 5. A finite second-order response lemma

### Lemma 5.1 -- `C^2` response with two one-power Poisson losses

Let `G_s` be a normalized uniformly non-null finite-alphabet kernel family on a real interval, with compatible stationary laws `nu_s`.  Assume:

1. for some `a>2`, `partial_s^j log G_s`, `j=0,1,2`, are locally uniformly bounded in `B_a`;
2. `s -> G_s` is `C^2` in that Banach scale;
3. `s -> nu_s` is weakly continuous.  This follows either from uniqueness under the coupling above or, in the DPP application, directly from the complete-event determinant formulas.

Choose any

\[
2<b<a.
\tag{5.1}
\]

Then, for every `B_b`-valued `C^2` family `F_s`, the scalar map

\[
s\longmapsto\nu_s(F_s)
\]

is `C^2`.

For a fixed observable `F`, suppressing `s` from notation,

\[
D\nu_s(F)=\nu_s(A_1QF),
\tag{5.2}
\]

and

\[
D^2\nu_s(F)
=\nu_s(A_2QF)
+2\nu_s(A_1Q A_1QF).
\tag{5.3}
\]

Every `Q` in (5.3) includes its own centering `Pi_s`.  For a moving observable,

\[
\frac{d^2}{ds^2}\nu_s(F_s)
=D^2\nu_s(F_s)+2D\nu_s(F_s')+\nu_s(F_s'').
\tag{5.4}
\]

#### Proof

For fixed `s` and small `h`, invariance and (4.5) give the exact identity

\[
\nu_{s+h}F-\nu_sF
=\nu_{s+h}(L_{s+h}-L_s)Q_sF.
\tag{5.5}
\]

Because `Q_sF in B_{b-1}`, the operator Taylor expansion on that space and weak continuity yield (5.2).

To obtain the second derivative, write

\[
L_{s+h}-L_s=hA_1+\frac{h^2}{2}A_2+o(h^2)
\tag{5.6}
\]

as an operator on `B_{b-1}`.  Apply (5.5) once more, now to the fixed observable `A_1Q_sF`:

\[
\nu_{s+h}(A_1Q_sF)-\nu_s(A_1Q_sF)
=\nu_{s+h}(L_{s+h}-L_s)Q_s(A_1Q_sF).
\tag{5.7}
\]

The first `Q_s` maps `B_b` to `B_{b-1}`.  Since `b-1>1`, the second maps `B_{b-1}` to `B_{b-2}`.  Substituting (5.6)--(5.7) into (5.5) gives

\[
\nu_{s+h}F
=\nu_sF+h\nu_s(A_1Q_sF)
+\frac{h^2}{2}
\left[\nu_s(A_2Q_sF)+2\nu_s(A_1Q_sA_1Q_sF)\right]
+o(h^2).
\]

This is (5.3).

For continuity of the derivatives, split every `Q_s` series at a fixed `M`.  Finite sums are continuous in `s`.  Their tails are uniform by (4.6), and for the nested inverse by (4.7).  Thus all terms in (5.2)--(5.3) are continuous.  Ordinary Leibniz expansion gives (5.4).  No pressure analyticity theorem and no same-space spectral resolvent are used.  QED.

### Operator-theory comparison

Tanaka, arXiv:2205.12561, condition (II) requires the reduced inverse to preserve each space in his chosen scale.  Our concrete inverse instead has the loss (4.4).  Therefore this proof does not claim that Tanaka's Theorem 2.8 or 2.10 applies automatically.  It verifies the two required response coefficients and their remainders directly by (5.5)--(5.7).  The earlier `p>8` route used the coarser map `B_b -> B_{b-2}`; the present excursion estimate is structurally different, not a change of notation.

## 6. Application to the true DPP entropy rate

For the compatible DPP law,

\[
h(t)=-\nu_t(\ell_t),
\qquad
\ell_t(x)=\log G_t(x_0|x_1,x_2,...).
\tag{6.1}
\]

Let

\[
H(s)=h(\sqrt{s})=-\nu_s(\ell_s)
\]

for positive `s`, using the even extension near zero.  By (1.9), Lemma 5.1 applies whenever `a=p/2>2`.  Hence

\[
\boxed{H\text{ is }C^2\text{ near }s=0\text{ for every }p>4.}
\tag{6.2}
\]

### Lemma 6.1 -- the linear term in `s` vanishes without pressure theory

One has

\[
H'(0)=0.
\tag{6.3}
\]

#### Proof

Let `P_{s,n}` be the true complete-configuration law on a finite consecutive block.  Its even-coordinate and odd-coordinate marginals do not depend on `s`: restricting to either parity uses only even Fourier differences, while `g` has only odd Fourier support.  At `s=0` the two parity blocks are independent because `c` has only even Fourier support.  Therefore the exact finite-volume mutual-information identity is

\[
D(P_{s,n}\|P_{0,n})
=H(P_{0,n})-H(P_{s,n}).
\tag{6.4}
\]

Use the chain rule from right to left.  Each summand is the Bernoulli relative entropy between two finite-future complete-event conditionals.  Those conditionals are even analytic in `t`, uniformly non-null, and have a common complex disk.  Cauchy's estimate gives, uniformly in the window, conditioning configuration, and site,

\[
|q_s-q_0|\le C|s|.
\tag{6.5}
\]

For probabilities in a fixed compact subinterval of `(0,1)`,

\[
d_{Ber}(u\|v)\le C(u-v)^2.
\]

Consequently

\[
0\le D(P_{s,n}\|P_{0,n})\le Cn s^2.
\tag{6.6}
\]

Divide (6.4) by `n` and pass to entropy rates:

\[
0\le H(0)-H(s)\le Cs^2.
\tag{6.7}
\]

Since `H` is differentiable, (6.3) follows.  QED.

This proof retains every complete event.  It does not differentiate an inclusion probability or replace the classical entropy by a spectral quantity.

## 7. Quartic coefficient and local concavity

Since `H` is `C^2` and `H'(0)=0`, write

\[
H(s)=H(0)-A s^2+o(s^2),
\qquad A=-\frac12H''(0).
\tag{7.1}
\]

The accepted regularity-free parity/matching bound from PR53 gives, for any odd `k` with `widehat g(k) != 0`,

\[
H(0)-H(s)
\ge\frac12 d_{Ber}
\left(\mu^2-|\widehat g(k)|^2s\,\middle\|\,\mu^2\right).
\tag{7.2}
\]

Expanding the elementary Bernoulli divergence and using (7.1),

\[
A\ge C_k:=
\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}.
\tag{7.3}
\]

Set

\[
\alpha_k=\frac{C_k}{2}
=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\tag{7.4}
\]

Because `h(t)=H(t^2)`, continuity of `H''` gives

\[
h''(t)=2H'(t^2)+4t^2H''(t^2)
=6H''(0)t^2+o(t^2)
=-12At^2+o(t^2).
\tag{7.5}
\]

Equivalently,

\[
h^{(4)}(0)=-24A,
\qquad
h''(t)=\frac12h^{(4)}(0)t^2+o(t^2).
\tag{7.6}
\]

Therefore

\[
\frac{d^2}{dt^2}
\left[h(c+tg)+\alpha_k t^4\right]
=12(\alpha_k-A)t^2+o(t^2)
\le-12\alpha_k t^2+o(t^2)<0
\tag{7.7}
\]

for all sufficiently small nonzero `t`; at `t=0` the second derivative is zero.  After also imposing the strict legality interval for `c+tg`, the corrected entropy is concave on a nonempty symmetric neighborhood and strictly concave away from the center.

## 8. Quantitative truncation scope

The response proof above is direct in infinite volume and already has the correlation-sum cutoff estimates (4.6)--(4.7) for all `p>4`.

For a canonical memory-`N` freezing, (1.9) gives, for every `r<a`,

\[
\|\partial_s^j(\log G_s-\log G_s^{[N]})\|_{B_r}
\le C_{r,j}N^{r-a},
\qquad j=0,1,2.
\tag{8.1}
\]

A norm-by-norm comparison of the full second-response formulas spends one further power when comparing the two kernels.  The elementary resolvent comparison therefore gives a quantitative full second-response rate only after choosing `b>3`, hence `a>3` (`p>6`): for every `0<eta<a-3`, one obtains a rate no worse than

\[
O(N^{-(a-2-eta)}).
\tag{8.2}
\]

This stronger-range spatial rate is optional and is not used in the `p>4` theorem.  In the range `4<p<=6`, this file claims only the direct infinite-volume response and the proved time/correlation cutoff (4.6)--(4.7), not a polynomial rate for finite-memory second derivatives.

## 9. Exact verdict and preserved failures

**Original PR66 p>4 statement:** `PROVED` at the author-proof level by the finite-response route in this file, **PENDING_REVIEW** and not independently accepted.

**Dobrushin import as written in PR66:** still invalid.  No A1 exponential-cardinality estimate and no A2 null-state norm is asserted.

**Earlier p>8 file:** its two-power Poisson bound is a valid coarse estimate, but its threshold is superseded.  Its full finite-memory equation (6.7) remains an incomplete bridge and is explicitly not imported here.

**Novelty:** not assessed.

**Computation:** none.  There are no floating inputs or numerical certificates.

## 10. Primary-source map

1. X. Bressaud, R. Fernandez, A. Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, Electronic Journal of Probability 4 (1999), arXiv:math/9806132.  Condition (4.1) and Proposition 1 are on printed pp.4--5; maximal coupling and the agreement-length transitions (4.13)--(4.20) are on printed pp.6--7; Proposition 2(ii),(iv) and the defective-return renewal discussion are on printed pp.12--13.  The new estimate (3.5) is proved here from their chain; it is not quoted as a theorem of that paper.
2. H. Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:2205.12561.  Condition (II), printed p.5, requires the reduced inverse to preserve the specified spaces; Theorems 2.8 and 2.10 are on printed pp.12--14.  This file records the mismatch and does not use those theorems as a substitute for (5.5)--(5.7).
3. PR66 internal complete-event inverse, Schur-complement, non-nullness, parity and matching inputs are used only in their stated `A_p`, strict-margin range.  The rejected Dobrushin section is not used.
