# Three global routes and the exact smooth-approximation obstruction

## 1. Nonanalytic Gibbs / chain-continuity route — selected and completed

The accepted PR53 proof obtains parameter regularity from a Hölder normalized prediction potential and a Ruelle–Perron–Frobenius spectral gap. That route naturally asks for exponential locality.

The polynomial theorem uses a different bridge. For `c,g\in\mathcal A_p`, `p>4`, complete-event matrices have a dimension- and configuration-uniform inverse bound in a polynomial weighted Schur algebra. A remote conditioned bit changes the event matrix by a rank-one diagonal perturbation. The conditional at the origin therefore contains two long propagators, yielding

\[
\operatorname{Inf}_j(\log G_z)=O(j^{-2q}),
\qquad q=\frac{p+2}{4}>\frac32.
\]

Telescoping the one-sided log conditional by the last revealed future coordinate produces interval interactions `U_[i,i+n]` of size `O(n^{-2q})`. The deliberately strong bound

\[
\sum_{A\ni0}\operatorname{diam}(A)\|U_A\|_\infty<\infty
\]

then follows. Dobrushin's one-dimensional theorem, in the many-body finite-first-moment formulation proved by Cassandro and Olivieri, supplies analytic pressure and analytic Gibbs expectations without a high-temperature or small-coupling hypothesis.

The DPP is identified as the equilibrium state of this interaction by a direct conditional cross-entropy inequality, not by spectral entropy. The parity gauge makes the interaction even in `t`, so it is analytic in `s=t^2`; the specific relative entropy has zero first derivative at `s=0`. This gives the uniform response statement

\[
h(c)-h(c+t g)=A t^4+O(t^6).
\]

Only after this response statement is available is the accepted negative-association/matching inequality used to show `A` has a strictly positive lower bound. This route therefore produces a genuine nonempty local interval for the true entropy rate.

## 2. Spectral approximation plus uniform quantitative estimates

Let `c_N,g_N` be smooth or finite-range approximants. For each `N`, the accepted exponential theorem may yield an interval `[-\varepsilon_N,\varepsilon_N]`. Convergence of the entropy-rate values, even uniform convergence in `t`, does not stop `\varepsilon_N` from tending to zero.

### 2.1 Analytic scalar obstruction

This failure already occurs for entire real-analytic functions. On any fixed real interval, set

\[
F_N(t)=t^4+N^{-2}e^{-N^2t^2},
\qquad
F(t)=t^4.
\]

Then

\[
\|F_N-F\|_\infty\le N^{-2}.
\]

Moreover

\[
F_N''(t)
=12t^2+e^{-N^2t^2}(4N^2t^2-2).
\]

For `N\ge2` and `|t|\le(2N)^{-1}`,

\[
F_N''(t)
\le \frac3{N^2}-e^{-1/4}<0.
\]

Thus every `F_N` is locally strictly concave, but the certified interval shrinks to zero. The uniform limit `F(t)=t^4` is not concave on any neighborhood of zero.

For the corrected-entropy form, fix any `\alpha\ge0` and define

\[
h_N(t)=-\alpha t^4+F_N(t),
\qquad
h(t)=-\alpha t^4+F(t).
\]

Then `h_N+\alpha t^4` is locally concave for every `N`, `h_N\to h` uniformly, while `h+\alpha t^4=t^4` is not locally concave. This is a counterexample to the **approximation mechanism**, not a DPP entropy-rate counterexample.

### 2.2 Minimal estimates that would make approximation valid

Any one of the following genuinely uniform statements is sufficient.

**Common finite-Jensen interval.** There is an `\varepsilon>0`, independent of `N`, such that for every `x,y\in[-\varepsilon,\varepsilon]` and `\lambda\in[0,1]`,

\[
F_N(\lambda x+(1-\lambda)y)
\ge
\lambda F_N(x)+(1-\lambda)F_N(y).
\]

Uniform value convergence then passes the inequality to the limit.

**Uniform curvature remainder.** For the deficit `R_N(t)=h_N(0)-h_N(t)`, there are constants `C>0`, `\varepsilon>0` and a modulus `\omega(r)\downarrow0`, all independent of `N`, such that

\[
R_N''(t)=12A_Nt^2+E_N(t),
\qquad
A_N\ge C,
\qquad
|E_N(t)|\le\omega(|t|)t^2
\]

for `|t|\le\varepsilon`. A common smaller interval follows immediately.

**Uniform complex response disk.** A common complex disk, a locally uniform bound there, evenness in `t`, and convergence of the analytic entropy deficits imply convergence of derivatives by Cauchy estimates. Together with a uniform positive quartic coefficient floor, this also gives a common interval.

Ordinary entropy continuity provides none of these. In DPP terms, the missing object is a volume- and approximant-uniform control of the complete-event inverse/conditional response, not merely convergence of symbols or entropy values.

## 3. Negative association / variational direct Jensen route

The exact parity decomposition and negative association yield a robust lower bound for the **centered deficit**

\[
h(c)-h(c+t g).
\]

The matching argument is valuable because it survives the regularity reduction and gives the explicit quartic floor

\[
\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}.
\]

It does not, by itself, compare two arbitrary parameters `t_1,t_2` with their midpoint. A pointwise lower bound on the deficit cannot be differentiated, and a bound of order `ct^4` does not determine the sign of the second derivative away from the center. Therefore it cannot supply local concavity without an additional uniform response principle.

The Gibbs variational method used in the proof is narrower and exact: it turns the normalized one-sided conditional into a finite-first-moment interaction and identifies the DPP as its equilibrium state. The Dobrushin–Cassandro–Olivieri response theorem then supplies the missing differentiability. A purely negative-association midpoint inequality for arbitrary `t_1,t_2` remains open; no fermionic von Neumann entropy inequality is substituted for the classical configuration Shannon entropy.

## Outcome of the comparison

The first route proves the polynomial-class theorem. The second route is valid only after adding one of the displayed uniform estimates; bare smooth approximation is rigorously insufficient, even for analytic scalar functions. The third route supplies the strict quartic coefficient but not the curvature sign on its own.
