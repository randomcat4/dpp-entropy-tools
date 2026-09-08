# Second-order jet DP for the fixed-beta tau family

AUTHOR DERIVATION.  The later non-author verdict is `CORRECT`; see
`verifications/fresh_audit.md`.  This file remains the author-side derivation,
not the certificate itself.

## 1. Setup and affine coordinate

Fix nonzero path parameters \(\beta_1,\ldots,\beta_{n-1}\), and let \(R\) be
unit lower bidiagonal:

\[
R_{ii}=1,\qquad R_{i+1,i}=-\beta_i .
\]

For \(\tau\in\Omega_\beta\),

\[
S(\tau)=R^{-1}\operatorname{diag}(\tau)R^{-T},\qquad
K(\tau)=I-S(\tau),
\]

and

\[
L(\tau)=R^T\operatorname{diag}(1/\tau)R-I .
\]

Thus a line

\[
\tau(t)=\tau_0+t\delta
\]

is a true affine line in \(K\)-space:

\[
K(t)=K(0)-t\,R^{-1}\operatorname{diag}(\delta)R^{-T}.
\]

The perturbation rank is the support size of \(\delta\).  Rank-one directions
are blocked by the Gu rank-one concavity prior art recorded by the parent; the
implemented scout therefore records rank-two and full-rank directions.

## 2. Entrywise second-order jets

Write \(w_i(t)=1/\tau_i(t)\).  At \(t=0\),

\[
w_i=\tau_i^{-1},\qquad
w_i'=-\delta_i\tau_i^{-2},\qquad
w_i''=2\delta_i^2\tau_i^{-3}.
\]

The tridiagonal entries of \(L(t)\) have jets

\[
d_i(t)=w_i(t)+\beta_i^2w_{i+1}(t)-1\quad(1\le i<n),
\]

\[
d_n(t)=w_n(t)-1,
\]

and

\[
e_i(t)=-\beta_i w_{i+1}(t).
\]

The implementation stores a jet as \((x,x',x'')\); the third component is the
actual second derivative, not the coefficient of \(t^2\).

## 3. Interval determinant jets

For a selected contiguous run \([a,b]\), let

\[
\kappa(a,b;t)=\det L(t)_{\{a,\ldots,b\}} .
\]

The continuant recurrence is

\[
\kappa(a,b)=d_b\kappa(a,b-1)-e_{b-1}^2\kappa(a,b-2),
\]

with \(\kappa(a,a-1)=1\).  Replacing every scalar by a jet gives the derivative
recurrences automatically.  Written out, if \(\kappa_1=\kappa(a,b-1)\) and
\(\kappa_2=\kappa(a,b-2)\), then

\[
\kappa'
=d_b'\kappa_1+d_b\kappa_1'
-2e_{b-1}e_{b-1}'\kappa_2-e_{b-1}^2\kappa_2',
\]

and

\[
\kappa''
=d_b''\kappa_1+2d_b'\kappa_1'+d_b\kappa_1''
-2\left((e_{b-1}')^2+e_{b-1}e_{b-1}''\right)\kappa_2
-4e_{b-1}e_{b-1}'\kappa_2'
-e_{b-1}^2\kappa_2'' .
\]

This is the first \(O(n^2)\) layer: all interval determinants and their first
two directional derivatives are computed without enumerating events.

## 4. Entropy DP in jets

For an \(L\)-ensemble, the exact event probability is

\[
p(S)=\frac{\det L_S}{Z},\qquad Z=\det(I+L).
\]

On a path, \(\det L_S\) factors over the selected contiguous runs of \(S\).
Let \(Z_m\) be the total unnormalized weight on the first \(m\) vertices, and
let

\[
T_m=\sum_{S\subseteq \{1,\ldots,m\}}\det L_S\log\det L_S .
\]

The selected-run recurrence is

\[
Z_m=Z_{m-1}+\sum_{a=1}^m Z_{a-2}\kappa(a,m),
\]

\[
T_m=T_{m-1}
+\sum_{a=1}^m \kappa(a,m)T_{a-2}
+\sum_{a=1}^m Z_{a-2}\kappa(a,m)\log\kappa(a,m),
\]

with \(Z_0=1,T_0=0\) and \(Z_{-1}=Z_0,T_{-1}=T_0\) under the usual empty-prefix
convention.  The only nonlinear scalar jet rule beyond addition and
multiplication is

\[
(x\log x)'=x'(\log x+1),
\]

\[
(x\log x)''=x''(\log x+1)+\frac{(x')^2}{x}.
\]

Finally,

\[
H=\log Z-\frac{T}{Z}.
\]

The script evaluates this last expression by the same jet algebra rather than
by a hand-expanded quotient formula.

## 5. Complexity

For one direction \(\delta\):

- interval determinant jets: \(n(n+1)/2\) states;
- selected-run entropy jets: another triangular pass over the same intervals;
- arithmetic complexity: \(O(n^2)\);
- current memory: \(O(n^2)\), because all interval jets are stored for audit
  and reuse.

The memory can be reduced by streaming intervals ending at the current right
endpoint, but this implementation intentionally keeps the triangular table
visible for validation.

A full low-dimensional \(\tau\)-Hessian can be built by polarization from
directional calls:

\[
H_{ij}=\frac{Q(e_i+e_j)-Q(e_i)-Q(e_j)}2,\qquad Q(v)=\frac{d^2}{dt^2}H(\tau+tv)\bigg|_{t=0}.
\]

This naive full-Hessian construction costs \(O(n^4)\), so it is used only for
small \(n\) sanity checks.

## 6. K-direction norm and feasibility margin

Let \(u_i\) be the \(i\)-th column of \(R^{-1}\).  Then

\[
\dot K=-\sum_i \delta_i u_i u_i^T.
\]

The reported normalization is

\[
\|\dot K\|_F^2
=\sum_{i,j}\delta_i\delta_j(u_i^Tu_j)^2.
\]

For the unit lower-bidiagonal \(R\), if \(i\le j\),

\[
u_i^Tu_j=(\beta_i\beta_{i+1}\cdots\beta_{j-1})h_j,
\qquad
h_j=1+\beta_j^2h_{j+1},\quad h_n=1.
\]

This gives the norm in \(O(n^2)\).

For spectral margins, the script uses the tridiagonal matrix

\[
P=S^{-1}=I+L.
\]

Approximate margins are obtained by Sturm bisection on \(P\).  For the frozen
n=93 suspect case, the stored decimal float parameters are also interpreted as
exact rationals and an exact tridiagonal LDL check certifies

\[
4I\preceq P\preceq 50I.
\]

Therefore

\[
\frac1{50}I\preceq S=I-K\preceq \frac14 I,
\]

and the strict DPP margin is at least \(1/50\).

## 7. Numerical boundary discovered and fixed in this work unit

The first float implementation used a generic reciprocal jet for the final
normalization \(T/Z\).  Algebraically this is correct, but numerically it forms
\(Z^{-3}\).  In high dimension \(Z\) can be so large that \(Z^{-3}\) underflows
to zero even though the quotient derivative is moderate.

The n=93/rank2 scout at seed `20260908`, trial `15`, initially reported

\[
H''_{\rm legacy}\approx 184.7448188718266.
\]

The final implementation avoids this by evaluating the quotient \(C=A/B\) from
the identities \(A=CB\):

\[
C_0=A_0/B_0,\qquad
C_1=(A_1-B_1C_0)/B_0,
\]

\[
C_2=(A_2-2B_1C_1-B_2C_0)/B_0 .
\]

This stable quotient never forms \(B_0^{-3}\).

After freezing the complete parameters and recomputing with the stable float
quotient and with Decimal precision 50, 80, and 110, the value is stable at

\[
H''_{\rm stable\ float}\approx -0.007024918933640795,
\]

\[
H''_{\rm Decimal}
=-0.007024918933615582731289762931393827\ldots .
\]

The actual symmetric chord second differences computed from value-only Decimal
DP converge to the same negative number; for \(h=0.0005\), the recorded
midpoint gap is

\[
-8.78114868789936\ldots\times 10^{-10}.
\]

The failure is not overflow of the raw \(Z,T\) accumulators: both are finite in
float.  It is the reciprocal-cube term inside the old inverse jet that
underflows.  At Decimal precision 110,

\[
(\log Z)''\approx 0.2082391792394403,\qquad
(T/Z)''\approx 0.2152640981730559,
\]

so \(H''\approx -0.0070249189\).  The legacy reciprocal path instead produced
\((T/Z)''\approx -184.5365796926\), which flips the sign.  The stable float
quotient gives \((T/Z)''\approx0.21526409817308104\), matching Decimal to the
needed sign precision.

The corrected same-scope scout over n=5..100, 24 trials per n, rank2 and
full-rank buckets, produced no positive normalized \(H''>10^{-10}\).  This is
finite evidence only, not a proof of concavity.

Conclusion: the current stable float `H2` evaluator is usable for scouting, but
any future high-dimensional positive sign must still be replayed through the
Decimal branch or a log-scaled / interval-certified jet before becoming even a
`FLOAT_CANDIDATE`.
