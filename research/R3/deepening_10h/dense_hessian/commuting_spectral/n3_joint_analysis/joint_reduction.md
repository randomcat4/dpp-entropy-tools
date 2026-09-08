# D10-M6 joint singleton/pair reduction

Author status: **DERIVATION_CANDIDATE_PENDING_FRESH_REVIEW**.

## Exact n=3 event law

Let \(P_{ai}=q_{ai}^2\).  Since \(Q\) is real orthogonal, \(P\) is
orthostochastic, hence doubly stochastic.  The exact-event probabilities are

\[
p_\varnothing=\prod_i(1-\theta_i),\qquad
p_{\{1,2,3\}}=\prod_i\theta_i,
\]

\[
p_{\{a\}}=(Pr)_a,\qquad
r_i=\theta_i\prod_{j\ne i}(1-\theta_j),
\]

and, indexing a two-point event by its missing observed coordinate \(a\),

\[
p_{\{1,2,3\}\setminus\{a\}}=(Ps)_a,\qquad
s_i=(1-\theta_i)\prod_{j\ne i}\theta_j.
\]

The pair formula uses the complementary-minor identity
\(\det(Q_{S,R})^2=q_{ai}^2\) when \(a\) is the missing row and \(i\) is the
missing column.

## Cardinality split and imported Shepp--Olkin scope

The projection-DPP spectral channel preserves cardinality.  Therefore

\[
H(Y_t)=H(N_t)+G_P(r(t))+G_P(s(t)),\qquad N_t=|Y_t|.
\]

Here \(N_t\) is the sum of three independent Bernoulli variables with
parameters \(\theta_i+t v_i\).  The only imported Shepp--Olkin input is:
the entropy of this Poisson-binomial count distribution is concave in the
Bernoulli parameters along the one-sign affine path, so

\[
H(N_t)''\le 0.
\]

This imported result controls only the count entropy.  It does not control the
conditional observation entropy inside the singleton and pair cardinality
layers.

## One-layer derivative formula

For a positive vector path \(x(t)\), set

\[
y=Px,\qquad \pi=\sum_i x_i,\qquad
G_P(x)=-\sum_a y_a\log(y_a/\pi).
\]

Differentiating gives

\[
\frac{d^2}{dt^2}G_P(x(t))
=-\sum_a\frac{(y_a')^2}{y_a}
  +\frac{(\pi')^2}{\pi}
  -\sum_a y_a''\log\frac{y_a}{\pi}.
\]

The first two terms are nonpositive by Cauchy--Schwarz:

\[
\sum_a\frac{(y_a')^2}{y_a}
\ge
\frac{(\sum_a y_a')^2}{\sum_a y_a}
=
\frac{(\pi')^2}{\pi}.
\]

Thus the only sign-indefinite part of one layer is the channel-acceleration
term

\[
-\sum_a y_a''\log(y_a/\pi).
\]

For the two layers together,

\[
\Psi''=
-D_P(r)-D_P(s)
-\langle P r'',\log(Pr/\pi_1)\rangle
-\langle P s'',\log(Ps/\pi_2)\rangle,
\]

where

\[
D_P(x)=\sum_a\frac{((Px)'_a)^2}{(Px)_a}
       -\frac{(\sum_i x_i')^2}{\sum_i x_i}\ge0,
\]

\(\pi_1=\sum_i r_i\), and \(\pi_2=\sum_i s_i\).

## Complement/pair duality

Let \(\bar\theta_i=1-\theta_i\).  The pair raw weights are singleton raw
weights for the complement eigenvalues:

\[
s_i(\theta)=\bar\theta_i\prod_{j\ne i}(1-\bar\theta_j)=r_i(\bar\theta).
\]

Along \(\theta(t)=\theta+t v\), the complement path has rate \(-v\).  Since
second derivatives are quadratic in the rate, the pair layer is the singleton
layer of the complement DPP with the opposite one-sign direction.  This explains
why a proof should pair the two layers, but it does not by itself prove a sign.

The previous singleton blocker remains active: \(r_i''\) can be positive even
for \(v\ge0\).  Therefore the valid target is a joint cancellation inequality,
not componentwise concavity of \(r\) and \(s\).

## Unclosed analytic inequality after review

The exact condition needed for total concavity is the barrier inequality

\[
\Psi''\le -H(N_t)'',
\]

which is equivalent to \(H(Y_t)''\le0\) because
\(H(Y_t)''=H(N_t)''+\Psi''\).

The stronger sufficient condition \(\Psi''\le0\) is not viable.  The original
scout already found sampled points with \(\Psi''>0\), and a subsequent
fresh-context review reported a strict interval-certified positive
conditional-curvature example.  Therefore the conditional layer is not concave
by itself; only the total barrier inequality remains a possible theorem target.

This work unit did not close the barrier inequality over all
\((Q,\theta,v\ge0)\).  The scripts in this directory instead reduce fixed
\((Q,\theta)\) checking to finite-dimensional cone probes and run scout
searches for a total-curvature violation.
