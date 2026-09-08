# Complement jets and the exact total barrier

STATUS: CORRECT_AFTER_INDEPENDENT_REVIEW for the stated identities and bounds.

## Exact events and derivatives

All primes below mean differentiation along θ+t v at t=0, with Q fixed.
For {i,j,k}={1,2,3}, write a_i=1−θ_i. Then

\[
r_i=\theta_i a_j a_k,\qquad
r_i'=v_i a_j a_k-\theta_i(v_j a_k+v_k a_j),
\]
\[
r_i''=2(\theta_i v_jv_k-v_iv_j a_k-v_iv_k a_j),
\qquad r_i'''=6v_1v_2v_3,
\]
\[
s_i=a_i\theta_j\theta_k,\qquad
s_i'=-v_i\theta_j\theta_k+a_i(v_j\theta_k+v_k\theta_j),
\]
\[
s_i''=2(a_i v_jv_k-v_iv_j\theta_k-v_iv_k\theta_j),
\qquad s_i'''=-6v_1v_2v_3.
\]

For m=0,1,2,3, complement duality is exactly

\[
s^{(m)}(\theta;v)=(-1)^m r^{(m)}(1-\theta;v).
\]

It is essential to retain the minus sign for odd jets: the complement path
is 1−θ−tv, not 1−θ+tv.

The cubic terms cancel coordinatewise:

\[
r_i+s_i=\theta_i-\theta_i\theta_j-\theta_i\theta_k+\theta_j\theta_k,
\]
\[
(r_i+s_i)''=2(v_jv_k-v_iv_j-v_iv_k).
\]

Writing R=Σr_i, T=Σs_i and e=∏a_i, f=∏θ_i gives

\[
e+f=1-\sum_i\theta_i+\sum_{i<j}\theta_i\theta_j,
\quad (R+T)''=-2\sum_{i<j}v_iv_j.
\tag{1}
\]

The exact atom vector, grouped by cardinality, is p=(e,y_1,y_2,y_3,z_1,z_2,z_3,f),
y=Pr, z=Ps, with a pair indexed by its missing coordinate. Complementary
2×2 minors of Q have squares q_ai²; this is the genuinely n=3 input.
The event formula equals inclusion-probability Möbius inversion, as checked
coefficientwise in the accompanying rational script.

## Fisher deficits are sums of squares

For any positive layer x, let y=Px and π=Σx=Σy. Define

\[
\mathcal D_P(x)=\sum_a\frac{y_a'^2}{y_a}-\frac{\pi'^2}{\pi}.
\]

Two useful exact SOS forms are

\[
\mathcal D_P(x)=\sum_a y_a\left(\frac{y_a'}{y_a}-\frac{\pi'}\pi\right)^2
=\sum_{a<b}\frac{(y_b y_a'-y_a y_b')^2}{\pi y_a y_b}\ge0.
\tag{2}
\]

Equality holds iff all y_a'/y_a are equal, equivalently
y'=(π'/π)y. This controls derivatives within a layer, not its changing mass.
Differentiating the weighted conditional entropy gives

\[
G_P(x)''=-\mathcal D_P(x)-\langle Px'',\log(Px/\pi)\rangle.
\tag{3}
\]

Let π=(e,R,T,f), h=H(N), and Ψ=G_P(r)+G_P(s). The total barrier is

\[
\boxed{B=-h''+\mathcal D_P(r)+\mathcal D_P(s)
+\langle Pr'',\log(Pr/R)\rangle
+\langle Ps'',\log(Ps/T)\rangle.}
\tag{4}
\]

For direct checking, −h''=Σ_n π_n'^2/π_n+Σ_n π_n''logπ_n.
Cancelling layer-mass terms in (4) produces the usual exact-event expression

\[
B=\sum_S\frac{p_S'^2}{p_S}+\sum_Sp_S''\log p_S=-H(Y)''.
\tag{5}
\]

(4) and (5) are identities, not solutions of the global sign question.

## Extracting the complement baseline

Using (1), write the acceleration part in (4) as

\[
2\log3\sum_{i<j}v_iv_j+\mathcal R(\theta,P;v),
\]
\[
\mathcal R=\langle Pr'',\log(3Pr/R)\rangle
+\langle Ps'',\log(3Ps/T)\rangle.
\tag{6}
\]

Consequently

\[
\boxed{B=-h''+\mathcal D_P(r)+\mathcal D_P(s)
+2\log3\sum_{i<j}v_iv_j+\mathcal R.}
\tag{7}
\]

The first four terms are nonnegative for one-sign v, using the count-entropy
theorem. The remaining problem is quantitative domination of a potentially
negative residual R, not an independent claim that the conditional entropy is
concave. The already verified Ψ''>0 example excludes that shortcut.

## A paired L1 estimate giving an explicit nonsymmetric subclass

For a rate pair {j,k} with remaining index i, its contribution to r'' is
2v_jv_k(θ_i e_i−(1−θ_i)e_j−(1−θ_i)e_k); its contribution to s'' is
2v_jv_k((1−θ_i)e_i−θ_i e_j−θ_i e_k). Their combined L1 norm is exactly
6v_jv_k. Triangle inequality over the three rate pairs proves

\[
\|r''\|_1+\|s''\|_1\le6\sum_{j<k}v_jv_k.
\tag{8}
\]

This uses v_jv_k≥0. Bounding the two layers separately and forgetting their
complementary coefficients gives a looser constant 12; the paired estimate
is the useful cancellation. Since P is nonnegative and column stochastic,
its action contracts L1. Let

\[
\delta_* = \max_a\left\{\left|\log\frac{3(Pr)_a}{R}\right|,
\left|\log\frac{3(Ps)_a}{T}\right|\right\}.
\]

Then |R|≤6δ_*Σ_{i<j}v_iv_j. Substitution in (7) yields the checked closed
lower bound

\[
B\ge-h''+\mathcal D_P(r)+\mathcal D_P(s)
+(2\log3-6\delta_*)\sum_{i<j}v_iv_j.
\tag{9}
\]

Thus δ_*<log3/3 closes a genuine continuous, generally nonsymmetric subclass.
Choosing δ_*=log(4/3) as an upper bound gives rational conditional-probability
tests 1/4≤(Pr)_a/R,(Ps)_a/T≤4/9 and positive coefficient
κ=2log(81/64). These conditions are not asserted for all DPPs; the positive
Ψ counterexample necessarily lies outside this sufficient region.

At uniform conditional layers y=(R/3)1 and z=(T/3)1, R=0 exactly, even if
their first and second jets are not uniform. This observation closes the
subclass proved in `proved_subclass_or_blocker.md`.

## What orthostochasticity has and has not accomplished

Column and row sums of P equal one. The complementary-minor identity makes
the same P act on both layers, enabling (1) and (6). However, the vectors
Pr'' and Ps'' can have mixed signs. Jensen cannot bound (6) with these signed
weights. Replacing the orthostochastic set by the Birkhoff polytope also does
not permit a vertex argument: P↦R and the Fisher terms are nonlinear rational
and logarithmic functions, with no established convexity of B in P.

No claim is made that permutation matrices, θ-boundary points, or finitely many
orthostochastic extremes control the global sign. The pointwise copositive
reduction from M6 remains an equivalent fixed-base test, not a proved finite
reduction over all (Q,θ).

## Imported theorem and scope

KNOWN: Hillion–Johnson, Theorem 1.2, proves joint concavity of the entropy of a
sum of independent Bernoulli variables in its success parameters. We use it
only for h(θ)=H(N), so C=−∇²h is PSD; it does not assert concavity of the DPP
event entropy. The [original paper](https://arxiv.org/pdf/1503.01570) explicitly
states the theorem on page 2. The count variables are the independent spectral
Bernoulli variables and θ+t v is affine, so its hypotheses hold.
