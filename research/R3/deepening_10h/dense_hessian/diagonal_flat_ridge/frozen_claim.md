# D10-U2 frozen claim: heterogeneous diagonal flat ridge

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.

Let \(n\ge 2\),

\[
X=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1,
\]

and let \(H(K)\) be the natural-log Shannon entropy of the exact-event DPP
law, with atoms obtained from inclusion probabilities by Möbius inversion:

\[
p_S(K)=\sum_{A\supseteq S}(-1)^{|A|-|S|}\det K[A,A].
\]

The frozen claims are:

1. **Global fixed-diagonal maximum.**  Among all strict real DPP kernels
   \(K\) with the same diagonal \(K_{ii}=x_i\),

   \[
   H(K)\le \sum_{i=1}^n h(x_i)=H(X),
   \qquad
   h(u)=-u\log u-(1-u)\log(1-u).
   \]

   Equality holds if and only if \(K=X\).  Equivalently, the diagonal kernel is
   the unique entropy maximizer on the strict feasible fixed-diagonal section.

For the local contact claims, let \(D=D^\top\) be a real symmetric direction
with zero diagonal,

\[
D_{ii}=0\quad\text{for every }i,
\]

and set

\[
K(t)=X+tD
\]

for all sufficiently small \(t\) inside the strict real DPP kernel domain
\(0\prec K(t)\prec I\).

2. **Zero-diagonal contact order.**  Along this line every exact atom has zero
   first derivative at the diagonal base:

   \[
   p_S'(0)=0\qquad(S\subseteq[n]).
   \]

   The entropy has no first-, second-, or third-order variation:

   \[
   H'(0)=H''(0)=H'''(0)=0.
   \]

Write

\[
q_S=p_S''(0).
\]

For \(S\subseteq[n]\), define the centered singleton score

\[
\zeta_i(S)=
\begin{cases}
1/x_i,& i\in S,\\
-1/(1-x_i),& i\notin S.
\end{cases}
\]

3. **Explicit exact-event second atom jet.**

   \[
   \frac{q_S}{p_S(0)}
   =
   -2\sum_{i<j}D_{ij}^2\,\zeta_i(S)\zeta_j(S).
   \]

4. **Explicit fourth derivative.**

   \[
   H^{(4)}(0)
   =
   -3\sum_{S\subseteq[n]}\frac{q_S^2}{p_S(0)}
   =
   -12\sum_{i<j}
   \frac{D_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
   \]

   Consequently, if \(D\ne0\), then \(H^{(4)}(0)<0\).

5. **Uniform compact-box fourth-order bound.**  If
   \(x_i\in[a,b]\subset(0,1)\) and

   \[
   M=\max_{u\in[a,b]}u(1-u),
   \]

   then for every
   zero-diagonal symmetric \(D\),

   \[
   H^{(4)}(0)
   \le
   -\frac{6\,\|D\|_F^4}{n(n-1)M^2}.
   \]

   In particular, on the normalized slice \(\|D\|_F=1\), the fourth derivative
   is uniformly bounded away from zero over the compact diagonal box.

6. For fixed \(n\) and \(0<a\le b<1\), there is a number \(\rho>0\) such that
   for every \(x\in[a,b]^n\), every zero-diagonal symmetric \(D\) with
   \(\|D\|_F=1\), and every \(0<|t|\le\rho\), the kernel \(X+tD\) is strict and

   \[
   H(X+tD)<H(X).
   \]

   More explicitly, after shrinking \(\rho\) if necessary,

   \[
   H(X+tD)
   \le
   H(X)-\frac{t^4}{8n(n-1)M^2}.
   \]

   Independently of this local quantitative radius, the global fixed-diagonal
   maximum implies \(H(X+tD)<H(X)\) for every strict feasible \(t\ne0\) whenever
   \(D\ne0\).

This is a fourth-order radial descent theorem at heterogeneous diagonal
kernels in zero-diagonal directions.  It does not assert that the Hessian is
negative on a full neighborhood, and it does not cover arbitrary nonzero
directions after leaving the diagonal ridge.
