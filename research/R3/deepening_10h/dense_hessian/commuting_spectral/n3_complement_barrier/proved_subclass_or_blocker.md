# Uniform-layer complement barrier

STATUS: CORRECT_AFTER_INDEPENDENT_REVIEW for Theorems A/B/E and Corollaries
C/D, with the fixed-Q, one-sign spectral-direction scope stated below.

The general n=3 claim remains INCOMPLETE. The statements below are a
continuous subclass and an open-neighborhood consequence, not a replacement
of that claim. All kernels are strictly between 0 and I.

## Theorem A: uniform layers, arbitrary one-sign spectral rates

Suppose the three singleton exact-event probabilities of K are equal and the
three pair exact-event probabilities are equal. For any fixed orthogonal
eigenbasis Q of K and v≥0,

\[
B=-h''+\mathcal D_P(r)+\mathcal D_P(s)
+2\log3\sum_{i<j}v_iv_j\ge0.
\tag{8}
\]

Moreover B>0 for v≠0. If θ_i∈[ε,1−ε], 0<ε<1/2, then

\[
B\ge c_\varepsilon\|v\|_2^2,
\qquad c_\varepsilon=\frac{2\varepsilon(1-\varepsilon)\log3}{9}>0.
\tag{9}
\]

The same statements hold for v≤0 by sign reversal. No statement is made here
for arbitrary mixed-sign v or for D not commuting with K.

### Proof of (8) and strictness

At the base point Pr/R=Ps/T=1/3 coordinatewise. Thus the residual in (6) of
`derivation.md` is zero. The two Fisher deficits are nonnegative by the explicit
SOS identity, and −h''≥0 by the count theorem. This proves (8).

If v has at least two positive entries, Σ_{i<j}v_iv_j>0, giving B>0 directly.
If only v_j>0, the count distribution is affine in this one parameter:
π_n=(1−θ_j)g_n+θ_jg_{n−1}, where g is the law of the other two Bernoulli
variables. Hence h''=−Σπ_n'^2/π_n<0. Indeed Σ_n nπ_n'=v_j≠0, so not all
π_n' vanish. This includes the one-rate boundary of the nonnegative cone;
it is not obtained by assuming all rates strictly positive.

The equality case for B≥0 is exactly v=0. For the conditional inequality
Ψ''≤0 at these bases, equality holds precisely when Σ_{i<j}v_iv_j=0 and
Pr'=(R'/3)1, Ps'=(T'/3)1; this follows by checking equality in each SOS.

### Proof of the explicit uniform constant

Put C=−∇²h(θ). The full Shepp–Olkin theorem implies C is PSD. Because the
count probabilities are affine in each individual θ_j,

\[
C_{jj}=\sum_n\frac{(\partial_j\pi_n)^2}{\pi_n}.
\]

The score has zero mean and its covariance with N is ∂_j E[N]=1. Cauchy–Schwarz
therefore gives C_jj≥1/Var(N)≥4/3. Conversely, the count score is the
conditional expectation, given N, of the j-th Bernoulli score. Conditional
expectation contracts squared L² norm, so

\[
\frac43\le C_{jj}\le\frac1{\theta_j(1-\theta_j)}\le L,
\qquad L=\frac1{\varepsilon(1-\varepsilon)}.
\tag{10}
\]

PSD implies |C_ij|≤sqrt(C_ii C_jj)≤L. Normalize ||v||_2=1 and let
m=v_j=max_i v_i, s=Σ_{i≠j}v_i, so m²≥1/3. The complementary principal block
of C is PSD. Thus

\[
v^TCv\ge\frac43m^2-2Lms.
\]

If s≤m/(3L), this is at least 2m²/3≥2/9. Otherwise
Σ_{i<j}v_iv_j≥ms>m²/(3L)≥1/(9L), and the last term in (8) is greater than
2log3/(9L). Since L≥4 and log3<4, the latter constant is at most 2/9.
This proves (9) for unit v, and quadratic homogeneity proves it for all v.

Only the count theorem is imported. In particular, neither a conjectured PSD
DPP theorem nor a general conditional-layer concavity assumption is used.

## Theorem B: exact description of the real base family

The strict real symmetric 3×3 kernels with uniform singleton and pair layers
are precisely

\[
K=S\left[bI+\frac{a-b}{3}J\right]S,
\quad S=\operatorname{diag}(\sigma_1,\sigma_2,\sigma_3),\quad\sigma_i\in\{\pm1\},
\quad 0<a,b<1.
\tag{11}
\]

Here J=11^T. They are fully connected when a≠b; the scalar case a=b is listed
separately as disconnected, not used to claim nondegeneracy.

### Proof

Write the common singleton probability y, common pair probability z, and
full probability f. Marginal inclusion gives K_ii=y+2z+f, so all diagonal
entries equal some d. Pair inclusion gives det K_{ij}=z+f, hence all
off-diagonal magnitudes equal some r≥0.

If r=0, K=dI. If r>0, set c=sign(K_12 K_13 K_23)r. Choosing σ_1=1,
σ_2=K_12/c, σ_3=K_13/c makes SKS have all off-diagonal entries c and all
diagonal entries d. Thus SKS=(d−c)I+cJ, with eigenvalues a=d+2c and b=d−c
(multiplicity two). Strictness is exactly 0<a,b<1, giving (11).

Conversely, the kernel inside brackets is invariant under all coordinate
permutations. Its inclusion determinants, and hence its exact-event law by
Möbius inversion, are permutation invariant; the two layers are uniform.
Diagonal sign conjugation leaves every principal determinant unchanged and
therefore leaves the law unchanged. This proves both directions.

For a≠b, an arbitrary symmetric commuting PSD direction is αU+V on the
orthogonal decomposition span(S1)⊕(S1)^⊥, where α≥0, U=(S1)(S1)^T/3,
V is PSD on the two-dimensional perpendicular space. Diagonalize V to obtain
the fixed Q and three nonnegative rates required by Theorem A. In particular,
the two rates on the repeated eigenspace may differ: the affine path then
leaves (11) immediately, but its curvature at the base point is still covered.
At scalar K, every symmetric PSD D commutes, so Theorem A covers it as well.

### A rational, non-symmetry-preserving example

Take U=J/3, w=(1,2,−3)^T, V=ww^T/14, W=I−U−V. These are exact rational
orthogonal rank-one projectors. Set

\[
K=\tfrac15U+\tfrac7{10}(V+W),\qquad
D=\tfrac15U+\tfrac13V+\tfrac23W.
\tag{12}
\]

K has every off-diagonal entry −1/6, so it is genuinely connected. D>0 has
three distinct positive eigenvalues, commutes with K, and is not proportional
to K. For t≠0 the two initially repeated eigenvalues split. The corresponding
orthostochastic matrix has columns

\[
P=\begin{pmatrix}1/3&1/14&25/42\\1/3&2/7&8/21\\1/3&9/14&1/42\end{pmatrix},
\]

with no zero entries and no repeated rows. This is not a direct sum or a
rank-one/thinning construction. All matrices and exact events are checked by
the sanity script; those checks do not substitute for the proof.

## Corollary C: full feasible chords in a symmetry-preserving subfamily

If a(t)=a+tα, b(t)=b+tβ in (11), with α,β both nonnegative (or both
nonpositive), not both zero, then H(K(t)) is strictly concave throughout every
strict feasible interval. At each t it satisfies Theorem A with spectral rates
(α,β,β). Therefore each nontrivial symmetric chord in that interval has
(H(K_-)+H(K_+))/2−H(K_0)<0. A crossing a(t)=b(t) is allowed; it causes no
loss of the uniform-layer property or strictness.

This global-in-t corollary does not apply to arbitrary directions splitting
the repeated eigenspace; those receive the local and neighborhood statements.

## Corollary D: uniform open-neighborhood exclusion

Fix 0<ε<1/2 and 0<η<1−2ε. In the parameter space O(3)×(0,1)^3, take the
compact base set A consisting of θ=(a,b,b), a,b∈[ε,1−ε], |a−b|≥η, and
Q whose first column is σ/√3 for a sign vector σ. This includes all
perpendicular eigenbases, not a finite orientation sample. Give the parameter
space metric d((Q,θ),(Q0,θ0))=||Q−Q0||_F+||θ−θ0||_2.

There is δ>0, independent of the base point and of the nonnegative direction,
such that d((Q,θ),A)≤δ implies

\[
B(\theta,Q;v)\ge\frac{c_\varepsilon}{2}\|v\|_2^2
\quad\text{for every }v\ge0.
\tag{13}
\]

### Proof and all quantifiers

The unit nonnegative rate set V_+={v≥0:||v||_2=1} is compact, including its
boundary supports. All eight event atoms are positive on strict kernels; on
O(3)×[ε/2,1−ε/2]^3 they are uniformly bounded below by (ε/2)^3. This follows
from the spectral-mixture formula: each latent Bernoulli pattern has weight
at least (ε/2)^3, and the relevant squared minors sum to one by Cauchy–Binet.
Thus the finite-sum curvature B is continuous, and uniformly continuous on
that compact parameter/rate product.

By (9), B≥c_ε throughout A×V_+. Uniform continuity yields a single δ for
which (13) holds on the closed δ-neighborhood; shrink δ if needed to keep
θ∈[ε/2,1−ε/2]. Quadratic homogeneity restores all nonzero rates, and v=0 is
automatic. This proves uniformity in a,b, Q's entire perpendicular O(2)
freedom, and every normalized nonnegative direction.

We may also require δ≤η/12. If a nearby parameter pair is δ-close to a base
pair, then ||K−K0||_op≤2δ, while every base off-diagonal magnitude is at least
η/3. Hence every nearby off-diagonal magnitude is at least η/6: the neighborhood
stays genuinely connected, not merely near a decoupled face.

If a center is at distance at most δ/2 from A and |h|||v||_2≤δ/2, its entire
fixed-Q spectral segment stays in the δ-neighborhood. Integrating the bound
H''≤−(c_ε/2)||v||² twice gives the quantitative chord bound

\[
\frac{H(K-hD)+H(K+hD)}2-H(K)
\le-\frac{c_\varepsilon}{4}h^2\|v\|_2^2.
\tag{14}
\]

The radius δ is proved to exist, not numerically specified. No computed
sample radius is substituted for this uniform-continuity argument.

## Precise global blocker and novelty boundary

Away from uniform layers, the residual R in (6) is not controlled by the
present proof. Establishing its domination for all strict θ and all
orthostochastic P is still an equivalent remaining global barrier problem.
We have not reduced it to finitely many parameter extremes or found a positive
total-curvature example. The general Ψ''≤0 shortcut remains disproved.

## Theorem E: explicit near-uniform layers without spectral symmetry

This strengthens the sufficient subclass without changing the global target.
Let K=Q diag(θ)Q^T be any strict real three-dimensional DPP, and suppose
both conditional layers satisfy

\[
\left|\log\frac{3(Pr)_a}{R}\right|\le\delta,
\qquad
\left|\log\frac{3(Ps)_a}{T}\right|\le\delta
\quad(a=1,2,3),\qquad 0\le\delta<\frac{\log3}{3}.
\tag{15}
\]

For every nonzero fixed-Q one-sign spectral rate v, B>0. More precisely,
with κ=2log3−6δ>0,

\[
B\ge-h''+\mathcal D_P(r)+\mathcal D_P(s)+\kappa\sum_{i<j}v_iv_j.
\tag{16}
\]

If θ_i∈[ε,1−ε], then

\[
B\ge\frac{\kappa\varepsilon(1-\varepsilon)}9\|v\|_2^2.
\tag{17}
\]

Proof: the paired L1 bound and stochastic contraction in `derivation.md`
give (16). If at least two rates are nonzero, its last term is strictly
positive. If one rate is nonzero, the count-Fisher argument of Theorem A
applies. For (17), repeat the two-region argument following (10), replacing
2log3 by κ. Since κ≤2log3 and L≥4, κ/(9L)≤2/9. Equality in B≥0 occurs
only for v=0. This proves every stated rate quantifier without sampling it.

A particularly usable rational subregion is

\[
\frac14\le\frac{(Pr)_a}{R},\frac{(Ps)_a}{T}\le\frac49
\quad(a=1,2,3).
\tag{18}
\]

It implies (15) with δ=log(4/3), because the scaled probabilities lie in
[3/4,4/3]. Its positive coefficient is κ=2log(81/64). Strict versions of the
six interval conditions define an open parameter set containing every
uniform-layer base. Neither repeated eigenvalues, equal diagonal entries,
exchangeability, nor zero matrix entries are required in this subregion.

The restriction remains fixed Q / commuting D; (18) does not extend the
direction quantifier to arbitrary noncommuting PSD matrices. If a whole
feasible spectral segment stays in (18) with spectral margin ε, then its
entropy obeys the integrated chord inequality with the constant in (17).

### Exact whole-segment certificate, beyond a symmetric base

Use the rational projectors U,V,W in (12), but set

\[
K_* =\tfrac15U+\tfrac7{10}V+\tfrac{71}{100}W,
\qquad D_* =\tfrac15U+\tfrac13V+\tfrac23W.
\tag{19}
\]

K_* has three distinct eigenvalues, unequal diagonal entries, and no zero
off-diagonals. It commutes with the rank-three PSD direction D_*, which is
not proportional to K_*. The accompanying script checks exact rational
polynomial inequalities proving (18) throughout |t|≤1/20, not merely at
sampled t values. For each singleton/pair atom polynomial p(t) with layer
mass π(t), it bounds 4p−π and 4π−9p from below on that interval by
c_0−Σ_{j=1}^3|c_j|(1/20)^j, and all twelve lower bounds are positive.
It also checks all eigenvalues stay in [1/10,9/10].

Therefore Theorem E proves strict total-entropy concavity on this entire
interval. In particular its midpoint gap obeys

\[
\Delta_h\le-\frac{\log(81/64)}{100}\|v\|_2^2 h^2
=-\frac{134\log(81/64)}{22500}h^2<0
\quad(0<|h|\le1/20),
\tag{20}
\]

because ε=1/10, ||v||²=1/25+1/9+4/9=134/225 and half the constant
in (17) is log(81/64)/100. The numerical interval is justified by finitely
many exact polynomial coefficient bounds plus Theorem E, not by inferring
continuum coverage from sampled entropy chords.

The algebraic complement identity and symmetry argument are elementary;
the count theorem is known. The potentially useful outcome is an explicit
uniform one-sign spectral-curvature margin at connected symmetric bases,
including directions that break that symmetry, plus its uniformly quantified
open-neighborhood consequence. A small targeted literature check did not
establish novelty of this exact statement; no new-theorem/venue claim is made.
