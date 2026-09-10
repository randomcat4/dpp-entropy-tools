# Reverse audit: noncommuting quasi-free KL bound and the absolute-loop `A_0` barrier

Status: **AUTHOR PROOF / SOURCE AUDIT / PENDING INDEPENDENT REVIEW.**

This note checks the two load-bearing points of the `L^infinity` second-difference theorem and records a precise obstruction to extending the PR117 absolute closed-walk mechanism beyond the Wiener algebra.

## 1. The quasi-free KL formula is valid without commutativity

For finite strict Hermitian contractions `0<A,B<I`, define

\[
\Phi(X)=\operatorname{Tr}\phi(X),\qquad
\phi(x)=x\log x+(1-x)\log(1-x).
\]

The finite-dimensional gauge-invariant quasi-free relative entropy satisfies

\[
D_q(\rho_A\|\rho_B)
=\operatorname{Tr}\left[
A(\log A-\log B)+(I-A)(\log(I-A)-\log(I-B))
\right].
\tag{1.1}
\]

Because `D Phi(B)[V]=Tr[(log B-log(I-B))V]`, cyclicity of the trace gives

\[
D_q(\rho_A\|\rho_B)
=\Phi(A)-\Phi(B)-D\Phi(B)[A-B]
\tag{1.2}
\]

without assuming `[A,B]=0`.

Diagonalize a point `X=U diag(lambda_i)U*` on the segment from `B` to `A`, and write `W=U*VU`. The standard second divided-difference calculation for a trace spectral function gives

\[
D^2\Phi(X)[V,V]
=\sum_i\phi''(\lambda_i)|W_{ii}|^2
+\sum_{i\ne j}
\frac{\phi'(\lambda_i)-\phi'(\lambda_j)}{\lambda_i-\lambda_j}
|W_{ij}|^2.
\tag{1.3}
\]

If all `lambda_i in [a,1-a]`, the scalar mean-value theorem and

\[
\phi''(x)=\frac1{x(1-x)}
\]

give

\[
0\le D^2\Phi(X)[V,V]
\le\frac1{a(1-a)}\|V\|_{HS}^2.
\tag{1.4}
\]

Taylor's integral formula for (1.2) therefore yields

\[
D_q(\rho_A\|\rho_B)
\le \frac1{2a(1-a)}\|A-B\|_{HS}^2.
\tag{1.5}
\]

Thus the PR125 constant does not hide a commuting-matrix assumption.

## 2. The occupation measurement really gives the complete DPP law

For a gauge-invariant quasi-free state with covariance `K`, joint occupation moments satisfy

\[
E_{\rho_K}\prod_{i\in S}N_i=\det K_S.
\]

These are exactly the DPP inclusion probabilities. The occupation-number measurement is a single projective measurement independent of `K`. Since a binary law is uniquely determined by all inclusion moments, Boolean Möbius inversion identifies every measured atom with the complete occupied/vacant DPP atom. Hence quantum data processing applies directly to the complete configuration laws:

\[
D(P_A\|P_B)\le D_q(\rho_A\|\rho_B).
\tag{2.1}
\]

No spectral entropy equality is used.

## 3. Exact non-`A_0` family

For example let

\[
c(\theta)=\frac13+\varepsilon\,\operatorname{sgn}(\cos 4\pi\theta),
\qquad
 g(\theta)=\varepsilon\,\operatorname{sgn}(\cos 2\pi\theta),
\tag{3.1}
\]

with `0<epsilon<1/12`. Then `c` is half-period even, `g` is half-period odd, and

\[
1/4<c<5/12
\]

a.e. Both symbols are bounded and have jump discontinuities. Their nonzero Fourier coefficients along the relevant parity subsequences are comparable to `1/(2j+1)`, so neither belongs to `A_0`. Nevertheless PR125 applies for all sufficiently small `|t|`, and `g_hat(1)` is nonzero, giving the explicit central second-difference sandwich.

This is a theorem family strictly outside PR117, not a limiting statement.

## 4. Why the PR117 absolute closed-walk route has a real `A_0` boundary

The issue is not the signed trace-log itself. Operator norm can control

\[
\operatorname{Tr}(RE)^m
\]

without absolute Fourier summation. The obstruction appears when one expands spatial displacements, takes absolute values to dominate complete-law derivatives uniformly, and then asks for one geometric constant in the walk length `m`.

The obstruction is already visible at a product reference, where `R_x` is diagonal. Let a real symmetric Fourier magnitude sequence be

\[
b_j=|\widehat e(j)|=b_{-j}\ge0.
\]

The absolute displacement sum of an even closed loop of length `2r` contains

\[
S_{2r}:=(b^{*2r})(0).
\tag{4.1}
\]

Let

\[
B_N(\theta)=\sum_{|j|\le N}b_j e^{2\pi i j\theta}.
\]

For finite support,

\[
S_{2r,N}=\int_T |B_N(\theta)|^{2r}d\theta.
\tag{4.2}
\]

Suppose an absolute-loop proof had one geometric constant `C<infinity` valid uniformly in the truncation and length:

\[
S_{2r,N}^{1/(2r)}\le C
\quad\text{for all }r,N.
\tag{4.3}
\]

Letting `r->infinity` at fixed `N` yields

\[
\|B_N\|_\infty\le C.
\tag{4.4}
\]

Apply the positive Fejer kernel at zero. Its convolution with `B_N` at zero is

\[
b_0+2\sum_{j=1}^N\left(1-\frac{j}{N+1}\right)b_j
\le\|B_N\|_\infty\le C.
\tag{4.5}
\]

Monotone convergence in `N` implies

\[
\sum_j b_j<\infty.
\tag{4.6}
\]

Therefore a uniform all-length **absolute** closed-loop geometric majorant forces the Wiener condition. Equivalently, if `e notin A_0`, then no proof which reduces all complete-law differentiated walks to absolute displacement sums of the form (4.1) can retain one length-geometric constant after all spatial sums.

This is a precise method obstruction. It is not an entropy counterexample: at a constant center, stronger entropy theorems may hold by a different argument.

## 5. HMM analyticity sources do not bridge this obstruction by themselves

Han--Marcus, arXiv `math/0507235`, defines a hidden Markov chain as a function of a finite-state first-order Markov chain. Its Theorem 1.1 assumes an analytically parameterized finite transition matrix and explicit positivity conditions on its columns before concluding entropy-rate analyticity.

Tadic--Doucet, arXiv `1806.09589`, treats a genuine state-space HMM with a Markov transition density `p_theta(x'|x)` and conditionally independent observations with density `q_theta(y|x)`. Its entropy theorem requires Assumptions 2.1--2.4, including a mixing/minorization condition, analytic parameterization/complex continuation, a uniform likelihood-ratio lower bound, and integrability conditions; these yield geometric ergodicity and exponential optimal-filter forgetting.

For a general Toeplitz DPP there is presently no proved finite-state Han--Marcus representation, nor a proved continuous-state Markov/filter representation satisfying the Tadic--Doucet assumptions uniformly in the physical affine parameter. Calling the DPP itself a hidden Markov model would therefore assume the missing bridge.

The HMM papers remain comparison sources only.

## 6. Consequence for the next open step

PR125 shows that strict `L^infinity` symbols already admit a nontrivial true entropy-rate second-difference theorem. To obtain `C^4` or local concavity outside `A_0`, one needs a mechanism that preserves cancellations after spatial summation, or an independently verified Markov/filter representation with uniform analytic stability. Re-running the PR117 absolute-displacement proof with weaker Fourier summability cannot accomplish this, by Section 4.