# I05-22: unequal-strength half-filled missing-edge centers

**Status: PROVED (author proof), not independently reviewed.** This is a scoped theorem, not a proof of general real three-point concavity. All logarithms are natural. Novelty and publication priority are not assessed.

## 1. Exact statement

Let

\[
K(b,c)=\begin{pmatrix}1/2&0&b\\0&1/2&c\\b&c&1/2\end{pmatrix},\qquad bc\ne0,\quad 4(b^2+c^2)<1.
\]

For every nonzero real symmetric three-by-three matrix \(D\),

\[
\left.\frac{d^2}{dt^2}H(K(b,c)+tD)\right|_{t=0}<0. \tag{T}
\]

Here \(H\) is the entropy of the eight complete configurations, not the entropy of the cardinality. The derivative is on the true affine kernel line in the fixed observation coordinates. The theorem permits all six direction coordinates, including the missing-edge direction \(D_{12}\), PSD/NSD directions, and full-rank directions. It places no restriction on \(|b|/|c|\).

The eigenvalues of the center are \(1/2,1/2\pm\sqrt{b^2+c^2}\), so the stated center is strictly between zero and identity. This spectral calculation is used for legality only, never to replace configuration entropy by a rotated-basis entropy.

At \(bc=0\) and \(4(b^2+c^2)<1\), continuity gives the non-strict version of (T); strictness on these axes is not claimed. Arbitrary chords whose intermediate centers leave the stated family are not covered.

## 2. Complete events and the cofactor identity

For a general real symmetric kernel \(K=\left(\begin{smallmatrix}x&a&b\\a&y&c\\b&c&z\end{smallmatrix}\right)\), put \(q_{12}=xy-a^2,q_{13}=xz-b^2,q_{23}=yz-c^2\), and \(q_{123}=\det K\). In bit-mask order \(0,1,2,12,3,13,23,123\), the atoms are

\[
\begin{aligned}
p_0&=1-x-y-z+q_{12}+q_{13}+q_{23}-q_{123},\\
p_1&=x-q_{12}-q_{13}+q_{123},\\
p_2&=y-q_{12}-q_{23}+q_{123},\\
p_{12}&=q_{12}-q_{123},\\
p_3&=z-q_{13}-q_{23}+q_{123},\\
p_{13}&=q_{13}-q_{123},\quad p_{23}=q_{23}-q_{123},\quad p_{123}=q_{123}.
\end{aligned} \tag{1}
\]

These are precisely Boolean inclusion-exclusion. At the strict centers used below all eight atoms are positive, as is also explicit in (4). For \(K+tD\), normalization implies

\[
\mathcal B_K(D):=-H''(K;D)=\underbrace{\sum_S(p'_S)^2/p_S}_{F_K(D)}+\sum_Sp''_S\log p_S. \tag{2}
\]

Set \(l_{ij}=\log(p_0p_{ij}/(p_ip_j))\) and \(\Lambda=\log(p_{123}p_1p_2p_3/(p_0p_{12}p_{13}p_{23}))\). Differentiating (1), using \(q_{ij}''=2\det D_{ij}\) and \((\det(K+tD))''|_0=2\operatorname{tr}(K\operatorname{adj}D)\), gives

\[
\mathcal B_K(D)=F_K(D)+2\sum_{i<j}l_{ij}\det D_{ij}+2\Lambda\operatorname{tr}(K\operatorname{adj}D). \tag{3}
\]

This identity includes all acceleration and mixed terms. It is also the R3 cofactor identity in the repository; the preceding derivation makes its use here independent of the status of any external author claim.

## 3. Atom weights and a genuine Hessian block decomposition

A diagonal sign conjugation can make \(b,c>0\). It preserves each principal minor and hence every complete-event probability, and maps all symmetric directions bijectively. We may therefore assume this sign choice without losing any direction. Define

\[
s=4(b^2+c^2),\quad d=4(b^2-c^2),\quad r=d/s,\quad k=8bc.
\]

Then \(0<s<1\), \(|r|<1\), and \(k=s\sqrt{1-r^2}\). Direct substitution in (1) gives

\[
(p_0,p_1,p_2,p_{12},p_3,p_{13},p_{23},p_{123})
=\tfrac18(1-s,1+d,1-d,1+s,1+s,1-d,1+d,1-s). \tag{4}
\]

Write

\[
g(u)=\log\frac{1+u}{1-u},\qquad W=\log\frac{1-d^2}{1-s^2}.
\]

In (3), \(\Lambda=0\), and

\[
N:=-\operatorname{diag}(l_{23},l_{13},l_{12})
=\operatorname{diag}(g(s)-g(d),g(s)+g(d),W)\succ0. \tag{5}
\]

Indeed \(|d|<s\), \(g\) is strictly increasing and odd, and \(W>0\). Thus \(\mathcal B=F-2\operatorname{tr}(N\operatorname{adj}D)\).

The map \(J(K)=S(I-K)S\), with \(S=\operatorname{diag}(1,1,-1)\), fixes this center and preserves entropy: complementation permutes atoms, and sign conjugation preserves them. Its derivative acts by \(L(D)=-SDS\). Hessian invariance gives \(\mathcal B(D,E)=\mathcal B(LD,LE)\), where the bilinear form is obtained by polarization. Consequently the \(+1\) and \(-1\) eigenspaces of \(L\) are orthogonal for the full Hessian. They are, respectively,

\[
\{D:D_{13},D_{23}\text{ possibly nonzero only}\},\qquad
\{D:D_{11},D_{22},D_{33},D_{12}\text{ possibly nonzero only}\}. \tag{6}
\]

This is an exact symmetry decomposition of the quadratic form, not a sum-of-good-directions argument. All cross terms between the two sectors vanish by invariance, not by omission.

In the two-dimensional sector, (3) and (5) give

\[
\mathcal B=F+2[g(s)+g(d)]D_{13}^2+2[g(s)-g(d)]D_{23}^2>0 \tag{7}
\]

for any nonzero vector. The entire Fisher form remains in this identity; only its nonnegative sign is needed for this particular sector.

## 4. All four remaining directions, with exact Fisher denominators

In the four-dimensional sector write

\[
P=D_{11}+D_{22},\quad E=D_{11}-D_{22},\quad Z=D_{33},\quad R=D_{12},\quad U=-sP/2+dE/2+kR.
\]

Direct differentiation of (1) yields

\[
4p'_{123}=P+Z+U,\quad 4p'_3=-P+Z+U,\quad
4p'_1=E-Z+U,\quad 4p'_2=-E-Z+U. \tag{8}
\]

The other four scores are the negatives of their complementary scores. Pairing the eight squares with their eight probabilities in (4), and completing squares, gives the full Fisher form

\[
F=2P^2+2E^2+\frac{2(V+kR)^2}{1-s^2}+\frac{2(V-kR)^2}{1-d^2},\qquad V=Z+(sP+dE)/2. \tag{9}
\]

The denominators \((1-s^2)\) and \((1-d^2)\) retain every rare-event contribution. There is no uniform probability lower bound in this proof. The full acceleration from (3) is

\[
A=-\frac W2(P^2-E^2)-2Z[g(s)P+g(d)E]+2WR^2. \tag{10}
\]

The diagonal mixed terms in (10) and the mixed squares in (9) must both be retained.

Introduce the invertible coordinate \(T=\sqrt{1-r^2}R\), and let \(G_s(r)\) be the real symmetric four-by-four matrix of (9)+(10) in \(v=(P,E,Z,T)^T\). Its complete defining quadratic form is

\[
\begin{aligned}
v^TG_s(r)v={}&2P^2+2E^2-\frac W2(P^2-E^2)-2Z[g(s)P+g(rs)E]\\
&+\frac{2(V+sT)^2}{1-s^2}+\frac{2(V-sT)^2}{1-r^2s^2}+\frac{2W}{1-r^2}T^2,\\
V={}&Z+s(P+rE)/2,\qquad W=\log\frac{1-r^2s^2}{1-s^2}.
\end{aligned} \tag{11}
\]

## 5. Exact shape-continuation certificate

For clarity, the rational derivative in the certificate can be formed without differentiating a long expanded matrix. Put \(A_s=1-s^2,B_s=1-r^2s^2\), \(a=(s/2,rs/2,1,s)^T\), \(b_*=(s/2,rs/2,1,-s)^T\), and \(J_{ij}=e_ie_j^T+e_je_i^T\). Then

\[
\begin{aligned}
G_s(r)={}&\operatorname{diag}(2-W/2,2+W/2,0,2W/(1-r^2))\\
&+2aa^T/A_s+2b_*b_*^T/B_s-g(s)J_{13}-g(rs)J_{23}. \tag{12}
\end{aligned}
\]

Here \(a'=(1/2,r/2,0,1)^T\), \(b_*'=(1/2,r/2,0,-1)^T\), and \(W'=2s(1-r^2)/(A_sB_s)\). Thus, holding \(r\) fixed,

\[
\begin{aligned}
\dot G={}&\operatorname{diag}(-W'/2,W'/2,0,2W'/(1-r^2))\\
&+2(a'a^T+aa'^T)/A_s+4saa^T/A_s^2\\
&+2(b_*'b_*^T+b_*b_*'^T)/B_s+4r^2s b_*b_*^T/B_s^2\\
&-2J_{13}/A_s-2rJ_{23}/B_s. \tag{13}
\end{aligned}
\]

Expansion of this explicit rational matrix gives

\[
\det\dot G_s(r)=\frac{48s^4(1-r^2)^2(1+r^2-2r^2s^2)}{(1-s^2)^4(1-r^2s^2)^4}>0. \tag{14}
\]

Equation (14) is an algebraic identity, not a numerical fit. One can verify it by clearing the displayed positive denominators in (13) and expanding its four-by-four determinant. `verify_exact.py` separately performs that polynomial identity check. The last numerator factor is \((1-r^2)+2r^2(1-s^2)>0\).

At \(r=0\), the four leading principal minors of \(\dot G_s(0)\), in the order \(P,E,Z,T\), are exactly

\[
\frac{s(s^4-s^2+1)}{(1-s^2)^2},\quad
\frac{s^2(s^4-s^2+1)}{(1-s^2)^3},\quad
\frac{s^3(s^4-s^2+4)}{(1-s^2)^4},\quad
\frac{48s^4}{(1-s^2)^4}. \tag{15}
\]

They are positive for \(0<s<1\): in particular \(s^4-s^2+1=(s^2-1/2)^2+3/4\). Sylvester's criterion gives \(\dot G_s(0)\succ0\).

We use the elementary inertia-continuation lemma: a continuous real symmetric matrix field on a connected interval, nonsingular everywhere and positive definite at one point, is positive definite everywhere. For completeness, the least eigenvalue is continuous, and any path from a positive-definite matrix to one with a nonpositive eigenvalue would contain a zero eigenvalue by the intermediate value theorem. This contradicts nonsingularity.

For each fixed \(s\in(0,1)\), (13) is continuous in \(r\in(-1,1)\), (14) excludes all zero eigenvalues, and (15) supplies the positive seed. Therefore

\[
\dot G_s(r)\succ0\quad(0<s<1,\ |r|<1). \tag{16}
\]

Finally (11) gives \(G_0(r)=\operatorname{diag}(2,2,4,0)\succeq0\). For fixed \(r\), integration in \(s\) yields

\[
G_s(r)=G_0(r)+\int_0^s\dot G_u(r)\,du\succ0. \tag{17}
\]

Indeed, every nonzero vector has strictly positive integrand for all \(0<u<s\). Combining (7), the exact orthogonal decomposition (6), and (17) proves (T). The changes of direction coordinates used above are invertible at every center covered by (T).

## 6. Exact input and error-controlled illustration

Take

\[
K_0=\begin{pmatrix}1/2&0&1/3\\0&1/2&1/4\\1/3&1/4&1/2\end{pmatrix},\quad
D_0=\begin{pmatrix}2&-1&3\\-1&1&-2\\3&-2&-1\end{pmatrix},\quad \tau=1/144.
\]

Here \(s=25/36,r=7/25\), the spectrum of \(K_0\) is \((1/12,1/2,11/12)\), and its atoms are \((11,43,29,61,61,29,43,11)/288\). Both determinant gaps equal \(11/288\). Since \(\|D_0\|_{\mathrm{op}}\le6\), the three exact kernels \(K_0-\tau D_0,K_0,K_0+\tau D_0\) have spectrum in \([1/24,23/24]\). The verifier additionally checks Sylvester minors exactly for each kernel and complement.

This triple is an illustration, **not a counterexample** and not a substitute for the theorem. Its complete-event Jensen difference \(\Delta=(H(K_0-\tau D_0)+H(K_0+\tau D_0))/2-H(K_0)\) is enclosed by

```
[-0.00413603603307918499086949813852939,
 -0.00413603603307918499086949813852938].
```

To reproduce the error bounds, reduce each rational log argument to \(2^m y\), \(1\le y<2\). With \(w=(y-1)/(y+1)\) and \(N=60\), use

\[
0\le\log y-2\sum_{j=0}^{N-1}\frac{w^{2j+1}}{2j+1}
\le\frac{2w^{2N+1}}{(2N+1)(1-w^2)}. \tag{18}
\]

This follows by bounding every remaining reciprocal odd integer by \(1/(2N+1)\) and summing the geometric tail. The same formula encloses \(\log2\). All accumulation uses exact rational arithmetic; multiplication by negative \(m\) reverses interval endpoints. The printed decimal endpoints are rounded outward, not nearest-rounded numerical estimates.

## 7. Dependencies and limits

The equal-strength rays \(b=\pm c\) overlap PR41's new author theorem. Our proof re-derives the eight events, cofactor identity, full Fisher, seed minors and shape extension, rather than importing PR41's theorem. PR43's rank-two theorem is not used in the proof of (T). Input audits and the exact literature-to-DPP bridges are in `sources_and_routes.md`.

This work does not prove general missing-edge centers with arbitrary \(x,y,z\), general three-point concavity, a universal positive margin, or any strict positive Jensen counterexample. Analytic correctness, independent review, exact algebra checks and novelty remain separate statuses.
