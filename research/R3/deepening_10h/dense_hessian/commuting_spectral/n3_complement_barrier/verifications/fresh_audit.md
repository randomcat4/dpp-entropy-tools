# D10-M7 fresh non-author audit

LAYERED STATUS:

- GLOBAL \(B(\theta,Q;v)\ge0\) for all \(Q,\theta,v\ge0\): **INCOMPLETE**,
  exactly as the author states.
- Theorem A, uniform conditional layers: **CORRECT**.
- Theorem B, real \(n=3\) uniform-layer classification: **CORRECT**.
- Corollary C/D, symmetry-preserving chords and compact fixed-\(Q\) one-sign
  neighborhood: **CORRECT**, with the stated commuting/fixed-eigenvector
  direction quantifier only.
- Theorem E, near-uniform conditional-layer barrier and rational interval
  certificate: **CORRECT**.

I did not modify author files and did not execute author `sanity.py`, because
that script writes the author `sanity_results.json`.  I instead wrote and ran
an independent exact-event checker in this `verifications/` directory.

Independent artifacts:

- `fresh_m7_verify.py`
- `fresh_m7_verify.json`

Command run from the repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\commuting_spectral\n3_complement_barrier\verifications\fresh_m7_verify.py
```

Result:

```text
status: PASS
exit code: 0
case_count: 3
interval_constraints: 12
min_interval_bound: 3133489/37800000
chord_count: 3
all_chord_gap_upper_bounds_negative: true
```

## A. Exact layer identity, jets, and uniform-layer barrier

For \(K(t)=Q\operatorname{diag}(\theta+tv)Q^\top\), I reconstructed all eight
exact atom polynomials by inclusion-determinant Möbius inversion.  Independently,
I reconstructed the spectral-subset channel:

\[
p=(e,\ Pr,\ Ps,\ f),
\]

where \(e=\prod_i(1-\theta_i)\), \(f=\prod_i\theta_i\),

\[
r_i=\theta_i\prod_{j\ne i}(1-\theta_j),
\qquad
s_i=(1-\theta_i)\prod_{j\ne i}\theta_j,
\]

and \(P_{ai}=q_{ai}^2\).  In dimension three, complementary \(2\times2\)
minors of an orthogonal matrix have the same squared values \(q_{ai}^2\), so
the same \(P\) acts on the pair layer.  The independent script checks direct
Möbius atoms and channel atoms coefficientwise.

The listed jets for \(r_i,s_i\), including

\[
r_i''=2(\theta_i v_jv_k-v_iv_j(1-\theta_k)-v_iv_k(1-\theta_j)),
\quad
r_i'''=6v_1v_2v_3,
\]

and

\[
s_i''=2((1-\theta_i)v_jv_k-v_iv_j\theta_k-v_iv_k\theta_j),
\quad
s_i'''=-6v_1v_2v_3,
\]

are correct.  The complement sign convention

\[
s^{(m)}(\theta;v)=(-1)^m r^{(m)}(1-\theta;v)
\]

is also correct; the odd signs are essential.

The entropy decomposition is exact:

\[
H(Y)=H(N)+G_P(r)+G_P(s),
\]

because it is just Shannon's chain rule over cardinality layers.  Differentiating
the weighted conditional entropy gives

\[
G_P(x)''
=-\mathcal D_P(x)-\langle Px'',\log(Px/\pi)\rangle,
\]

with

\[
\mathcal D_P(x)=
\sum_a\frac{y_a'^2}{y_a}-\frac{\pi'^2}{\pi}
=
\sum_{a<b}\frac{(y_by_a'-y_ay_b')^2}{\pi y_ay_b}\ge0.
\]

The script independently verified the direct exact-event curvature
\[
B=\sum_Sp_S'^2/p_S+\sum_Sp_S''\log p_S=-H(Y)''
\]
against the decomposed formula to below \(10^{-75}\) Decimal error on the
checked rational cases.

At uniform singleton and pair conditional layers, the residual
\(\langle Pr'',\log(3Pr/R)\rangle+\langle Ps'',\log(3Ps/T)\rangle\) vanishes.
The baseline

\[
2\log3\sum_{i<j}v_iv_j
\]

has the correct sign and coefficient because
\[
(R+T)''=-2\sum_{i<j}v_iv_j.
\]

Single-rate strictness is also handled correctly: if only one \(v_j\) is
nonzero, the cross term vanishes, but the count distribution is a nonconstant
affine one-parameter mixture, so
\[
-H(N)''=\sum_n \pi_n'^2/\pi_n>0.
\]

This covers the boundary of the nonnegative cone; the proof does not secretly
assume all rates are strictly positive.

## B. Real uniform-layer classification

The classification is correct.  If the three singleton exact atoms are equal
and the three pair exact atoms are equal, then all diagonals \(K_{ii}\) are
equal and all pair inclusion determinants are equal.  Since

\[
\det K_{\{i,j\}}=K_{ii}K_{jj}-K_{ij}^2,
\]

all off-diagonal magnitudes are equal.  A diagonal sign conjugacy makes the
three off-diagonal entries equal to a common \(c\), giving

\[
K=S\left[bI+\frac{a-b}{3}J\right]S,
\qquad 0<a,b<1.
\]

The scalar case \(a=b\) is disconnected.  The fully connected cases are exactly
\(a\ne b\).  Conversely, permutation symmetry plus sign conjugacy preserves
principal minors and therefore exact-event probabilities, so the layers are
uniform.

The proof also correctly allows PSD commuting directions that split the
repeated eigenspace.  Such paths leave the exchangeable base family immediately,
but their second derivative at the base is still covered by Theorem A because
the direction is fixed-\(Q\) spectral one-sign.

## C. Compact neighborhood quantifier

The compact-neighborhood claim is correct only in the author's stated
parameterization:

\[
K=Q\operatorname{diag}(\theta)Q^\top,\qquad
D=Q\operatorname{diag}(v)Q^\top,\qquad v\ge0
\]

or \(v\le0\) by sign reversal.  It is not a theorem about arbitrary PSD
directions at nearby kernels.

The compactness argument is sound.  On
\(\theta_i\in[\epsilon/2,1-\epsilon/2]\), all exact atoms are uniformly
positive.  The spectral-mixture proof of this lower bound is valid: for any
observed subset \(S\) of size \(k\), the latent spectral weights are at least
\((\epsilon/2)^3\), and the squared \(k\times k\) minors over all latent
\(k\)-sets sum to one by Cauchy--Binet.  Thus \(B\) is uniformly continuous on
the compact base/rate product, so the positive margin on the base set extends
to a single open neighborhood.

The connectedness add-on is also scoped correctly: imposing \(\delta\le\eta/12\)
keeps nearby off-diagonal magnitudes away from zero.  This is a local
neighborhood statement, not a global finite reduction over \(O(3)\).

## D. Theorem E: paired \(L^1\) bound and coefficient

The paired \(L^1\) estimate is correct.  For the rate pair \(\{j,k\}\) with
remaining index \(i\), the contribution to \(r''\) has \(L^1\)-norm

\[
2v_jv_k(\theta_i+2(1-\theta_i)),
\]

and the contribution to \(s''\) has \(L^1\)-norm

\[
2v_jv_k((1-\theta_i)+2\theta_i).
\]

Their sum is exactly \(6v_jv_k\).  Summing over pairs gives

\[
\|r''\|_1+\|s''\|_1\le 6\sum_{i<j}v_iv_j
\]

for one-sign rates.  Since \(P\) is nonnegative and column stochastic,
\(\|Px\|_1\le\|x\|_1\).  Therefore the residual obeys

\[
|\mathcal R|\le
6\delta\sum_{i<j}v_iv_j
\]

under
\[
\left|\log\frac{3(Pr)_a}{R}\right|,
\left|\log\frac{3(Ps)_a}{T}\right|\le\delta.
\]

The coefficient

\[
2\log3-6\delta
\]

is therefore correct.  The rational interval

\[
\frac14\le (Pr)_a/R,\ (Ps)_a/T\le \frac49
\]

implies \(3(Pr)_a/R,3(Ps)_a/T\in[3/4,4/3]\), hence
\(\delta=\log(4/3)<\log3/3\), and

\[
2\log3-6\log(4/3)=2\log(81/64).
\]

The one-rate boundary in Theorem E is not lost: when
\(\sum_{i<j}v_iv_j=0\), the count-Fisher term gives strict positivity.  With
\(\theta_i\in[\epsilon,1-\epsilon]\), the two-region count-score argument gives
the claimed lower bound

\[
B\ge
\frac{\kappa\epsilon(1-\epsilon)}{9}\|v\|_2^2,
\qquad
\kappa=2\log3-6\delta.
\]

This is a sufficient region.  It does not assert \(\Psi''\le0\) globally, and
it does not cover noncommuting PSD directions.

## E. Explicit rational asymmetric interval certificate

The independent script rebuilt the author's frozen asymmetric example with

\[
\theta=(1/5,7/10,71/100),
\qquad
v=(1/5,1/3,2/3),
\]

using the rational projectors from \(U=J/3\), \(V=ww^\top/14\),
\(w=(1,2,-3)\), and \(W=I-U-V\).

It reproduced

\[
K_*=
\begin{pmatrix}
151/280&-6/35&-47/280\\
-6/35&94/175&-29/175\\
-47/280&-29/175&747/1400
\end{pmatrix},
\]

and

\[
D_*=
\begin{pmatrix}
307/630&-64/315&-53/630\\
-64/315&131/315&-4/315\\
-53/630&-4/315&187/630
\end{pmatrix}.
\]

The certificate checks:

- three distinct spectral eigenvalues;
- heterogeneous coordinate diagonal;
- all off-diagonal entries nonzero;
- rank-three PSD fixed-\(Q\) direction;
- non-thinning spectral rates;
- spectral margin \(19/100\) on \(|t|\le1/20\);
- all twelve exact polynomial inequalities for
  \(1/4\le p_{\text{cond}}\le4/9\) on the whole interval.

The smallest independent lower bound among the twelve interval inequalities is

\[
3133489/37800000>0.
\]

Thus Theorem E applies to the whole interval, not just sampled points.  The
chord coefficient with \(\epsilon=1/10\) and
\(\|v\|_2^2=134/225\) is correctly

\[
-\frac{134\log(81/64)}{22500}h^2.
\]

I also independently checked the three actual entropy chords recorded by the
author.  These chords are for the symmetric base of equation (12), not for the
asymmetric \(K_*\) interval in equation (19); the author's `run_log.md`
correctly states this separation.  For steps \(1/100,1/1000,1/10000\), rigorous
rational logarithm intervals give strictly negative midpoint-gap upper bounds.
The full fractions are stored in `fresh_m7_verify.json`.

## Imported count theorem and novelty boundary

The Shepp--Olkin/Hillion--Johnson input is used only for the entropy of the
sum of independent spectral Bernoulli variables \(N\).  In this setting
\(\theta+tv\) is an affine path in Bernoulli success parameters, so the count
theorem supplies \( -H(N)''\ge0\) and the PSD count Hessian used in the uniform
constant argument.  The author does not use it as a DPP event-entropy concavity
theorem.

The author also does not claim novelty certification: the verdict explicitly
says no novelty certification is made, and the global problem remains
incomplete.  No finite non-hit is promoted into a universal theorem.

## Final audit verdict

No critical mathematical gap found in the stated subsidiary results.  The
correct certification is:

- **CORRECT** for Theorem A/B/C/D/E within fixed-\(Q\), one-sign spectral
  direction scope.
- **INCOMPLETE** for the unchanged global \(n=3\) commuting spectral barrier.
