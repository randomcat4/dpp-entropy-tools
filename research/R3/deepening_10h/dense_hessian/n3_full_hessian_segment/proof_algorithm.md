# Proof and certificate algorithm

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_FRESH_REVIEW.

## 1. Feasibility and nondegeneracy of the line

Because `U,V,W` are orthogonal projectors, the eigenvalues of `K(t)` are

\[
\frac15+\frac t5,\qquad \frac12+\frac t3,\qquad \frac45+\frac{2t}3.
\]

For \(|t|\le6/25\), all three eigenvalues and their complements are at least
`1/25`.  Hence

\[
0\prec K(t)\prec I
\]

throughout the closed certified interval.

The off-diagonal entries are affine and have zeros only at

\[
-153/128,\quad -171/106,\quad -45/8,
\]

all outside `[-6/25,6/25]`.  Thus the observation graph is connected on the
whole interval.  Diagonal equality can occur only at `t=-9/10`, also outside
the interval, so the diagonal remains heterogeneous.  The spectral collisions
are outside the interval as well.

## 2. Exact-event Hessian formula

For every event \(S\subseteq\{1,2,3\}\),

\[
p_S(K)=(-1)^{|S^c|}\det(K-I_{S^c})
\]

is the exact event probability, obtained from Möbius inversion of inclusion
probabilities.  Along the rational line \(K(t)\), each \(p_S(t)\) is a cubic
polynomial with rational coefficients.

For symmetric directions \(E,F\), put

\[
p^E_S(t)=Dp_S(K(t))[E],\qquad
p^{EF}_S(t)=D^2p_S(K(t))[E,F].
\]

Then \(p^E_S(t)\) is quadratic and \(p^{EF}_S(t)\) is affine in `t`.  With
natural logarithms and \(H=-\sum_S p_S\log p_S\),

\[
D^2H(K(t))[E,F]
=-\sum_S\frac{p^E_S(t)p^F_S(t)}{p_S(t)}
-\sum_S(1+\log p_S(t))p^{EF}_S(t).
\]

Since \(\sum_Sp_S(K)=1\), differentiating twice gives
\(\sum_Sp^{EF}_S(t)=0\).  Therefore the constant term drops and

\[
B_{EF}(t):=-D^2H(K(t))[E,F]
=\sum_S\frac{p^E_S(t)p^F_S(t)}{p_S(t)}
+\sum_Sp^{EF}_S(t)\log p_S(t).
\]

The script forms this bilinear matrix directly in the coordinate basis

\[
(E_{11},E_{22},E_{33},E_{12}+E_{21},E_{13}+E_{31},E_{23}+E_{32}).
\]

Strict positive definiteness of this `6 x 6` matrix is equivalent to strict
negative definiteness of the entropy Hessian on all of `Sym(3)`.

## 3. Interval certificate

On a rational subinterval \(I=[a,b]\):

- every polynomial \(p_S,p^E_S,p^{EF}_S\) is enclosed by exact rational interval
  Horner evaluation;
- positivity of all atom intervals is checked before taking logarithms;
- \(\log x\) is bounded by scaling \(x=2^k y\), \(1\le y<2\), and using

\[
\log y
=2\sum_{r=0}^{N-1}\frac{z^{2r+1}}{2r+1}+R_N,\qquad
z=\frac{y-1}{y+1},
\]

with exact tail

\[
0\le R_N\le
\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

The final run used `N=20` log terms.  All bounds are rational; Decimal values
in the report are display-only.

The resulting interval matrix \(\mathcal B(I)\) encloses \(B(t)\) for every
`t` in `I`.  For each row `i`, the script computes

\[
g_i(I)=\underline{B_{ii}}-\sum_{j\ne i}
\max\{|\underline{B_{ij}}|,|\overline{B_{ij}}|\}.
\]

If every \(g_i(I)>0\), then every enclosed real symmetric matrix is strictly
diagonally dominant with positive diagonal, hence positive definite.  This
proves \(B(t)\succ0\) on `I`.

## 4. Certified interval and failed expansion

The certified interval is

\[
[-6/25,6/25].
\]

It is covered by `173` rational subintervals.  The minimum certified Gershgorin
margin is positive; its Decimal display is approximately

\[
2.662575324700432790390645911\times10^{-4}.
\]

The minimum atom lower bound over the certified cover is

\[
63029/5000000.
\]

Smaller milestone radii were also certified:

| radius | passed leaves | minimum displayed margin |
|---:|---:|---:|
| `1/100` | 8 | `0.07622216490367943042115141782` |
| `1/50` | 16 | `0.06904614002077814078029786409` |
| `1/20` | 32 | `0.02484531521422611244830710811` |
| `1/10` | 62 | `0.00001391402191285990441462164889` |
| `1/5` | 142 | `0.00001391402191285990441462164889` |
| `6/25` | 173 | `0.0002662575324700432790390645911` |

The same Gershgorin certificate did not close at `49/200` or `1/4` with the
recorded depth.  Float grid probes at those failed radii still had positive
minimum eigenvalue for `B=-Hess H`; therefore these are method failures, not
positive-curvature candidates.

## 5. Boundary of the claim

The certificate is continuous in `t` because every rational subinterval is
covered.  It is not a grid theorem.  It proves full symmetric negative Hessian
only along this single explicit rational segment.  It does not prove that the
M8 product condition implies full-Hessian negativity, and it does not solve the
global dense-Hessian problem.
