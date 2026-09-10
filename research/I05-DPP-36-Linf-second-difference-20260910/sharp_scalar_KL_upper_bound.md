# Sharp scalar-KL upper bound for the true configuration entropy deficit

Status: **AUTHOR THEOREM / PENDING INDEPENDENT REVIEW.**

This note strengthens the coarse Hilbert--Schmidt estimate in the first PR125 checkpoint. It keeps the same complete configuration Shannon object and uses quasi-free relative entropy only as an upper-bound device.

## 1. Statement

Let real measurable `c,f in L^infinity(T)` satisfy, for some `a>0`,

\[
a\le c(\theta),f(\theta)\le1-a
\quad\text{a.e.}
\tag{1.1}
\]

Let `P_{n,f}` and `P_{n,c}` be the complete occupation laws of the finite Toeplitz DPP kernels `T_n(f)` and `T_n(c)`. Then

\[
\boxed{
\limsup_{n\to\infty}\frac1n
D(P_{n,f}\|P_{n,c})
\le
\int_{\mathbb T}
 d_{\rm Ber}(f(\theta)\|c(\theta))\,d\theta.}
\tag{1.2}
\]

If `c` is half-period even and `g` is half-period odd, put `f_t=c+t g` and assume the whole small real interval stays in the strip (1.1). The exact parity identity gives

\[
D(P_{n,f_t}\|P_{n,c})=H_n(c)-H_n(f_t),
\]

so the limits exist and

\[
\boxed{
0\le h(c)-h(c+t g)
\le
\int_{\mathbb T}
 d_{\rm Ber}(c+t g\|c).}
\tag{1.3}
\]

Since the complete laws at `t` and `-t` coincide, one also has the symmetric upper bound

\[
h(c)-h(c+t g)
\le\frac12\int
\{d_{\rm Ber}(c+t g\|c)+d_{\rm Ber}(c-t g\|c)\}.
\tag{1.4}
\]

In particular, dominated Taylor expansion on the fixed spectral strip yields

\[
\limsup_{t\to0}
\frac{h(c)-h(c+t g)}{t^2}
\le
\frac12\int_{\mathbb T}\frac{g(\theta)^2}{c(\theta)(1-c(\theta))}\,d\theta.
\tag{1.5}
\]

This is a true entropy-rate second-order modulus for every strict `L^infinity` symbol. No Fourier absolute summability and no entropy derivative are assumed.

## 2. Finite complete-law data processing

Let `rho_A` denote the finite gauge-invariant quasi-free state with covariance `A`. Occupation-number measurement produces exactly the complete DPP law, as proved in the first PR125 file. Hence

\[
D(P_{n,f}\|P_{n,c})
\le D_q(\rho_{T_n(f)}\|\rho_{T_n(c)}).
\tag{2.1}
\]

For strict finite contractions `A,B`, without any commutativity assumption,

\[
D_q(\rho_A\|\rho_B)
=\operatorname{Tr}\{A(\log A-\log B)
 +(I-A)(\log(I-A)-\log(I-B))\}.
\tag{2.2}
\]

It remains only to compute the normalized Toeplitz limit of the four trace terms.

## 3. Mixed Toeplitz trace lemma for bounded symbols

### Lemma

Let real `u,v in L^infinity(T)` and suppose the spectrum of every `T_n(v)` lies in a fixed compact interval `I`. If `F` is continuous on `I`, then

\[
\boxed{
\lim_{n\to\infty}\frac1n
\operatorname{Tr}[T_n(u)F(T_n(v))]
=\int_{\mathbb T}u(\theta)F(v(\theta))\,d\theta.}
\tag{3.1}
\]

### Step 1: polynomial `F`

It suffices first to prove, for every fixed integer `r>=0`,

\[
\frac1n\operatorname{Tr}
[T_n(u)T_n(v)^r]
\longrightarrow\int u v^r.
\tag{3.2}
\]

If `u,v` are trigonometric polynomials, all Toeplitz matrices have fixed bandwidth. Expanding the normalized trace into Fourier indices shows that all closed index chains that stay farther than the total bandwidth from the two boundaries contribute exactly the zero Fourier coefficient of `u v^r`; only `O(1)` anchor indices touch a boundary. Hence (3.2) follows with an `O(1/n)` error.

For general bounded `u,v`, choose trigonometric polynomials `u_M,v_M` converging in `L^2`, with uniform `L^infinity` bounds after using bounded Fejer means. The exact Toeplitz Hilbert--Schmidt estimate gives

\[
\frac1{\sqrt n}\|T_n(a)\|_{HS}\le\|a\|_2,
\qquad
\|T_n(a)\|_{op}\le\|a\|_\infty.
\tag{3.3}
\]

The telescoping identity for powers and Cauchy--Schwarz for the trace imply, with constants depending only on `r` and the common `L^infinity` bounds,

\[
\begin{aligned}
\frac1n|\operatorname{Tr}\{T_n(u)T_n(v)^r
-T_n(u_M)T_n(v_M)^r\}|
\le C_r(\|u-u_M\|_2+\|v-v_M\|_2).
\end{aligned}
\tag{3.4}
\]

The same `L^2` approximation controls `\int uv^r-\int u_Mv_M^r`. Taking `n->infinity` first and `M->infinity` second proves (3.2).

By linearity, (3.1) follows for polynomial `F`.

### Step 2: continuous `F`

Choose polynomials `p_M` uniformly approximating `F` on `I`. Then

\[
\frac1n|\operatorname{Tr}T_n(u)(F(T_n(v))-p_M(T_n(v)))|
\le\|u\|_\infty\|F-p_M\|_{\infty,I},
\tag{3.5}
\]

while

\[
\left|\int u(F(v)-p_M(v))\right|
\le\|u\|_1\|F-p_M\|_{\infty,I}.
\tag{3.6}
\]

Let `n->infinity` for fixed `M`, then `M->infinity`. This proves the lemma.

No Toeplitz matrices are asserted to commute.

## 4. Thermodynamic limit of the quasi-free relative entropy

Apply (3.1) repeatedly on the fixed strip `[a,1-a]`.

First, ordinary Szego trace limits (which are the special case `u=1`) give

\[
\frac1n\operatorname{Tr}[T_n(f)\log T_n(f)]
\to\int f\log f,
\tag{4.1}
\]

and

\[
\frac1n\operatorname{Tr}[(I-T_n(f))\log(I-T_n(f))]
\to\int(1-f)\log(1-f).
\tag{4.2}
\]

The mixed lemma gives

\[
\frac1n\operatorname{Tr}[T_n(f)\log T_n(c)]
\to\int f\log c,
\tag{4.3}
\]

and, using `I-T_n(f)=T_n(1-f)`,

\[
\frac1n\operatorname{Tr}[(I-T_n(f))\log(I-T_n(c))]
\to\int(1-f)\log(1-c).
\tag{4.4}
\]

Therefore

\[
\boxed{
\lim_{n\to\infty}\frac1n
D_q(\rho_{T_n(f)}\|\rho_{T_n(c)})
=
\int d_{\rm Ber}(f\|c).}
\tag{4.5}
\]

Combining (2.1) and (4.5) proves (1.2).

## 5. Symmetric second-order consequence

For scalar `p in [a,1-a]` and bounded `z` with `p\pm tz` in the same strip,

\[
d_{\rm Ber}(p+t z\|p)
=\frac{t^2z^2}{2p(1-p)}+O_a(|t|^3|z|^3).
\tag{5.1}
\]

Averaging the `+t` and `-t` expressions cancels odd powers and, because `g in L^infinity`, dominated convergence gives

\[
\frac1{2t^2}\int
\{d_{\rm Ber}(c+t g\|c)+d_{\rm Ber}(c-t g\|c)\}
\to
\frac12\int\frac{g^2}{c(1-c)}.
\tag{5.2}
\]

Together with exact complete-law evenness this proves (1.5).

The estimate does not assert that the actual entropy deficit has a second derivative. It is a limsup modulus obtained before any derivative exchange.

## 6. Relation to the earlier coarse bound

Since `c,f` stay in `[a,1-a]`, scalar Taylor bounds recover

\[
\int d_{\rm Ber}(f\|c)
\le \frac{1}{2a(1-a)}\|f-c\|_2^2,
\]

so the first PR125 Hilbert--Schmidt theorem remains a valid coarse corollary. The new statement keeps the full spatially varying scalar Fisher weight `1/[c(1-c)]` and is strictly sharper in general.

## 7. Evidence boundary

This is an author analytic theorem pending independent review. No numerical computation, finite-window sign extrapolation, HMM representation, spectral-entropy substitution, `C^2/C^4` claim, whole-legal-interval concavity claim, or entropy counterexample is made.