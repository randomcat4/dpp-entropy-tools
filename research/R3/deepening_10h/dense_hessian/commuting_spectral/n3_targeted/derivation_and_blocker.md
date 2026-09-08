# D10-M5 n=3 derivation and blocker

Author status: **INCOMPLETE**.  The formulas below are the reduced certificate
target; the final inequality is not proved in this file.

## 1. n=3 channel coordinates

Let

\[
P_{ai}=q_{ai}^2.
\]

For \(3\times3\) real orthogonal \(Q\), \(P\) is doubly stochastic.  The
spectral-channel representation gives exact atoms in four cardinality layers:

\[
p_\varnothing=\prod_i(1-\theta_i),\qquad
p_{\{1,2,3\}}=\prod_i\theta_i,
\]

\[
p_{\{a\}}=(Pr)_a,\qquad
r_i=\theta_i\prod_{j\ne i}(1-\theta_j),
\]

and, indexing a pair by its missing observed coordinate \(a\),

\[
p_{\{1,2,3\}\setminus\{a\}}=(Ps)_a,\qquad
s_i=(1-\theta_i)\prod_{j\ne i}\theta_j.
\]

The pair-layer formula uses the \(3\times3\) complementary-minor identity
\(\det(Q_{S,R})^2=q_{a i}^2\), where \(a\) is the row missing from \(S\) and
\(i\) is the column missing from \(R\).

Thus

\[
H(Y_t)=H(N_t)+G_P(r(t))+G_P(s(t)),
\]

where \(N_t=|Y_t|\) and

\[
G_P(x)=-\sum_a (Px)_a\log\frac{(Px)_a}{\sum_i x_i}.
\]

The count entropy \(H(N_t)\) is concave by Shepp--Olkin.  Hence the \(n=3\)
problem is reduced to controlling

\[
\Psi''(t)=\frac{d^2}{dt^2}\left(G_P(r(t))+G_P(s(t))\right).
\]

## 2. Exact derivative target

For any positive vector path \(x(t)\), write \(y=Px\) and \(\pi=\sum_i x_i\).
Then

\[
\frac{d^2}{dt^2}G_P(x(t))
=-\sum_a\frac{(y_a')^2}{y_a}
  +\frac{(\pi')^2}{\pi}
  -\sum_a y_a''\log\frac{y_a}{\pi}.
\]

The first two terms are nonpositive by Cauchy--Schwarz.  The last term is the
sign-indefinite channel-acceleration term.

For singleton weights,

\[
r_i''=
2\left[
\theta_i v_jv_k
-v_iv_j(1-\theta_k)
-v_iv_k(1-\theta_j)
\right],
\qquad \{i,j,k\}=\{1,2,3\}.
\]

For pair weights,

\[
s_i''=
2\left[
(1-\theta_i)v_jv_k
-v_iv_j\theta_k
-v_iv_k\theta_j
\right].
\]

These quantities do not have a fixed sign even when every \(v_i\ge0\).

## 3. Exact positive singleton-blocker example

Take

\[
\theta=(3/5,1/5,1/5),\qquad
v=(1/100,1/10,1/10).
\]

Then

\[
r''=(11/1250,-23/2500,-23/2500),
\]

so a singleton raw weight has positive second derivative under a PSD spectral
rate direction.  This invalidates the tempting proof strategy:

> show \(r(t)\) and \(s(t)\) are componentwise concave, then compose with the
> increasing concave perspective entropy \(G_P\).

That strategy works in the \(2\times2\) block from D10-M3 because the analogous
two raw weights both have second derivative \(-2v_1v_2\le0\).  It fails in
dimension three.

## 4. What a direct proof would still need

The remaining possible proof target is not layerwise concavity.  It must prove
one of the following stronger cancellation statements for every orthostochastic
\(P=q^2\), strict \(\theta\), and \(v\ge0\):

\[
G_P(r(t))''+G_P(s(t))''\le0,
\]

or at least

\[
G_P(r(t))''+G_P(s(t))''\le -H(N_t)''.
\]

The finite search in this directory saw positive singleton-layer and pair-layer
second derivatives separately, but never a positive sum.  No analytic
inequality proving that cancellation is supplied here.
