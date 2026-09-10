# PR113 mathematical/source FIRST report

## Status

`ACCEPTED_SCOPED` at frozen author head `a2bced01cc5de30943b20387b7e1d260c384661e`.

No load-bearing mathematical failure was identified.  The review units U1--U10 in the author contract are addressed below.

## U1 — small-Wiener interval and legality

Half-period oddness gives `g_hat(0)=0`.  Choosing `tau>0` with

\[
R=r_c+\tau\|\widehat g\|_1<\delta:=\min\{\mu,1-\mu\}
\]

gives `||f_t-mu||_infinity<=R` for every real `|t|<=tau`.  Hence both `f_t` and `1-f_t` are bounded below by `delta-R>0`.  Compression preserves the corresponding operator inequalities for every finite coordinate set.  Real non-even symbols cause no problem: their Toeplitz kernels are complex Hermitian because the symbols are real.

## U2 — every complete atom relative to Bernoulli

For a complete word `x`, with occupied set `S_x` and vacant set `Z_x`, the exact signed atom formula is

\[
p_{\Lambda,t}(x)=(-1)^{|Z_x|}\det(T_\Lambda(f_t)-I_{Z_x}).
\]

Writing `T_\Lambda(f_t)=mu I+A_t` and

\[
D_x(i,i)=\mu\quad(i\in S_x),
\qquad
D_x(i,i)=\mu-1\quad(i\in Z_x)
\]

gives the exact factorization

\[
p_{\Lambda,t}(x)=q_{\mu,\Lambda}(x)
\det(I+B_xA_t),\qquad B_x=D_x^{-1}.
\]

The vacant-site signs are correct, `A_t` has zero diagonal, and both absolute row and column sums of `B_xA_t` are bounded by `R/delta`.  Therefore

\[
\|B_xA_t\|_2
\le\sqrt{\|B_xA_t\|_1\|B_xA_t\|_\infty}
\le R/\delta<1.
\]

This explicit row/column estimate, supplied in the frozen self-audit, is the authoritative justification for the nonnormal matrix.  Positivity of the exact likelihood ratio along the real homotopy selects the ordinary real trace-log branch.  The `m=1` trace vanishes because `B_x` is diagonal and `A_t` has zero diagonal.

## U3 — complete-event derivative domination

The complete-event matrix `M=T_J(f_t)-I_Z` satisfies

\[
\|M^{-1}\|\le(\delta-R)^{-1}
\]

uniformly in the word and finite support.  Jacobi's formula gives logarithmic derivatives

\[
s_j=(-1)^{j-1}(j-1)!\operatorname{Tr}(M^{-1}T_J(g))^j,
\]

with `|s_j|<=C_j|J|`.  The Bell-polynomial formula therefore yields, for each fixed derivative order `r`,

\[
|\partial_t^rp_{J,t}(x)|
\le p_{J,t}(x)K_r|J|^rC_*^r.
\]

Summing a local observable uses `sum_x p_x=1`; it does not count the `2^|J|` words.  Rare atoms remain in the law, and no Fisher or acceleration contribution is discarded.

## U4 — differentiated closed walks

The length-`m` trace is correctly expanded over all closed walks, including repeated vertices.  A walk observable depends only on its distinct support `J(w)`, with

\[
|J(w)|\le m,
\qquad \|F_w\|_\infty\le\delta^{-m}.
\]

Adjacent repeats vanish because both `a_t(0)` and `g_hat(0)` are zero.  If `ell` derivatives hit distinct affine edge factors, the anchored absolute displacement sum is bounded by

\[
\|\widehat g\|_1^\ell R^{m-\ell}.
\]

Combining the at-most-polynomial derivative assignments with the local-expectation bound gives, for every fixed `r`,

\[
|\partial_t^rC_{m,\Lambda}(t)|
\le B_rm^{2r}\rho^{m-r},
\qquad \rho=R/\delta<1.
\]

The finitely many `m<r` cases are harmless and are absorbed into `B_r`.

## U5 — thermodynamic differentiation

For fixed walk length and displacement tuple, restriction consistency identifies every finite-volume local expectation exactly with the corresponding marginal of the infinite stationary DPP.  Translation invariance removes the anchor, and the fraction of admissible anchors tends to one.  The proof then takes limits in the safe order:

1. fixed walk length and derivative order;
2. displacement sum;
3. volume limit via the anchor fraction;
4. only then the walk-length sum.

The displacement majorant is summable by the `ell^1` convolution bound, and the walk-length majorant is geometric.  This proves locally uniform convergence of normalized KL derivatives.  The limiting KL density is exactly

\[
d(t)=h_{\rm Ber}(\mu)-h(c+t g),
\]

because the product Bernoulli reference has the same one-site marginals.  Thus the resulting regularity is for the true complete-configuration entropy rate.

## U6 — parity mutual information

Diagonal conjugation by `D_jj=(-1)^j` sends `T(c+tg)` to `T(c-tg)` and commutes with every vacant-set diagonal, so all complete atoms and the entropy rate are even in `t`.

The even and odd coordinate restrictions are independent of `t`, and at `t=0` the cross-parity block vanishes.  Therefore, first in finite intervals and then per lattice coordinate,

\[
J(t):=h(c)-h(c+t g)
=d(P_t\|P_0)=I_t(E;O)\ge0.
\]

This is an identity of complete laws, not an inclusion-probability identity.

## U7 — matching coefficient and the two curvature cases

The accepted PR53 matching argument gives

\[
J(t)\ge\frac12 d_{\rm Ber}
(q-a t^2\|q),
\quad q=\mu^2,
\quad a=|\widehat g(k)|^2.
\]

Since

\[
\frac12d_{\rm Ber}(q-a t^2\|q)
=\frac{a^2}{4q(1-q)}t^4+O(t^6),
\]

the floor coefficient is

\[
C_k=\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}
=2\alpha_k.
\]

The calculus split is exhaustive.  If `J''(0)>0`, continuity makes the corrected curvature strictly negative near zero.  If `J''(0)=0`, even `C^4` Taylor expansion and the matching floor give `J(t)=At^4+o(t^4)` with `A>=2alpha_k`, hence

\[
F''(t)=-12(A-\alpha_k)t^2+o(t^2)<0
\]

for sufficiently small nonzero `t`, with `F''(0)=0`.  No vanishing quadratic coefficient is assumed in advance.

## U8 — explicit zero-positive-moment family

For `w_n=1/[n(log(n+2))^2]`, the unweighted series converges, while `sum n^p w_n` diverges for every `p>0`.  The cosine constructions put the center on nonzero even modes and the direction on odd modes.  Their Fourier coefficients have the claimed absolute sums, the mean is `1/3`, and choosing the amplitude with `eta sum w_n<1/6` gives

\[
r_c<1/6<1/3=\min\{\mu,1-\mu\}.
\]

Both symbols fail every positive weighted Wiener condition.  Moreover `sum n^2w_n^2=sum 1/(log(n+2))^4` diverges, so the example also lies outside the stated Fourier `H^1` successor scope.

## U9--U10 — reverse audit and smoothness

The reverse-audit corrections are mathematically valid and are treated as author source, not as an independent opinion.  In particular they explicitly close the nonnormal contraction, repeated-vertex, real logarithm, and order-of-limits points.

For each arbitrary but fixed integer `r`, the Bell and walk estimates above remain finite and length-summable.  Applying the finite-order uniform-differentiation theorem for every fixed `r` proves

\[
h(c+t g)\in C^\infty(( -\tau,\tau)).
\]

The constants are not controlled by one factorial-radius estimate, so neither real nor complex analyticity follows or is accepted.

## Source audit

The primary sources support exactly the limited roles assigned to them:

- Lyons--Steif states the scalar stationary DPP entropy concavity problem as Conjecture 9.2 and defines the configuration process/entropy framework.
- Lyons proves conditional negative association for determinantal probability measures associated with positive contractions; this supports the accepted disjoint-matching input.
- Bressaud--Fernandez--Galves proves correlation and relaxation bounds for chains with summable variations.
- Fernandez--Maillard develops uniqueness, loss-of-memory, and Dobrushin sensitivity criteria for chains with complete connections.

The latter two sources do not state the required fourth-order parameter response under a zero-positive-moment `A_0` tail.  PR113 therefore correctly treats them as comparison sources and does not import a response theorem or the rejected Dobrushin A1/A2 route.

## Final disposition

The theorem, its explicit no-positive-moment family, and the real `C^infinity` corollary are accepted only in the frozen small-Wiener scope.  General `A_0` centers, whole-interval concavity, analyticity, a counterexample, and novelty remain outside this FIRST.
