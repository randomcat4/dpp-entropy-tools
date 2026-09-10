# I05-DPP-31 — PR66 low-regularity repair checkpoint

Status: **INCOMPLETE (the original p>4 theorem is not repaired yet).**

Role: theory reviser for PR66, not an independent reviewer. This branch starts from `main@65e59a46b49cd2dbb5c779a4cfae8cef26441984`, preserves PR66 at author head `af1edaad69c4e1f5e4bbd1239b8463b56bf64075`, and continues issue #44 / PR66 without treating the old author verdict or old RUNNING labels as acceptance.

The accepted exponential-regularity theorem PR53 is only background. The target here is the polynomial class

\[
\mathcal A_p=\left\{u:\sum_m(1+|m|)^p|\widehat u(m)|<\infty\right\},\qquad p>4,
\]

for real half-period-even `c` and half-period-odd `g`, with a strict spectral margin, and the true stationary DPP configuration Shannon entropy rate. No spectral/von-Neumann entropy substitution is used.

## 1. Exact inherited blocker

The full primary Dobrushin text is available and the source-access issue is closed. The remaining defect is applicability.

Primary source: R. L. Dobrushin, *Analyticity of the correlation functions for one-dimensional classical systems with power law decay of the potential*, Math. USSR-Sb. 23:1 (1974), 13–44, MathNet `https://www.mathnet.ru/eng/sm3631`.

The relevant hypotheses are located directly in the primary source at the following printed pages.

* pp. 14–15: classes A1/A2. A1 has an exponential factor in support cardinality in its D2 summability condition. A2 removes that factor only under the stronger null-state condition C2/(2.5).
* pp. 17–18: perturbation hypotheses and Theorems 1–2.
* pp. 24–25: Banach formulation/Theorem 6 and the corresponding A1/A2 spaces.

PR66 proves for its interval telescope

\[
U_{z,[i,i+n]}=-\psi_{n,z},\qquad \|\psi_{n,z}\|_\infty=O(n^{-2q}),\qquad q=(p+2)/4>3/2,
\]

and therefore

\[
\sum_{A\ni0}\operatorname{diam}(A)\|U_{z,A}\|_\infty<\infty.
\]

That ordinary first-moment estimate does **not** imply Dobrushin A1, because A1 carries an exponential support-cardinality weight. It also does **not** imply A2, because the submitted telescope only has the endpoint reference-state cancellation built into

\[
\psi_n(x_0,\dots,x_n)=\phi(x_0,\dots,x_n,0^\infty)-\phi(x_0,\dots,x_{n-1},0^\infty),
\]

whereas A2 requires the interaction to vanish whenever **any** coordinate in its support lies in the distinguished null state. A generic Boolean Möbius conversion can cost `2^|A|`; merely renaming the representation does not close the theorem.

The internal inverse/two-leg/equilibrium/parity lemmas of PR66 are separate source claims. This checkpoint neither repairs the external import nor enlarges the scope of those lemmas.

## 2. Route comparison

### Route (i): controlled A2 null-state potential

For a binary alphabet with null state `0`, an A2 interaction on a finite support `A` that vanishes whenever any coordinate is zero is necessarily of the form

\[
\Phi_A(x_A)=J_A\prod_{i\in A}x_i.
\]

Thus an A2 repair is not a cosmetic gauge choice: it requires quantitative control of the Boolean Möbius coefficients `J_A` of the relevant finite-volume/infinite-volume energy. A naive expansion of an arbitrary block function is exactly where the `2^{|A|}` loss occurs.

There is, however, DPP-specific determinant structure worth exploiting rather than expanding arbitrary `\psi_n`.

For any **finite** positive definite L-ensemble matrix `L` and occupied set `S`, the configuration weight is proportional to `det L_S`. If `mI\le L\le MI`, put

\[
\gamma=(m+M)/2,\qquad R=I-L/\gamma,\qquad \rho=\|R\|_{2\to2}\le\frac{M-m}{M+m}<1.
\]

Then, for every finite `S`,

\[
\log\det L_S=|S|\log\gamma-\sum_{k\ge1}\frac1k\operatorname{Tr}(R_S^k).
\tag{2.1}
\]

The series is absolutely convergent in operator norm. Use the Hamiltonian convention `H(S)=-log det L_S`, omitting only the common normalization constant, and define `J_A=sum_{B subseteq A} (-1)^(|A|-|B|) H(B)`. Thus `J_A` is the coefficient of the Hamiltonian, rather than of the log weight. Applying Boolean Möbius inversion over `B\subseteq A` to (2.1) cancels every closed-walk monomial whose visited vertex set is a proper subset of `A`. For `|A|\ge2`, the resulting null-state coefficient has the exact grouped closed-walk representation

\[
J_A
=\sum_{k\ge1}\frac1k
\sum_{\substack{i_1,\ldots,i_k\in A\\
\{i_1,\ldots,i_k\}=A}}
R_{i_1i_2}R_{i_2i_3}\cdots R_{i_ki_1},
\tag{2.2}
\]

with the displayed positive sign for the Hamiltonian coefficient. The corresponding coefficient of `log det L_S` is `-J_A`. Group the walks at each fixed `k` before summing over `k`: this grouped series converges as a finite Boolean Möbius combination of the absolutely convergent trace series. This does not assert an absolutely summable bound after taking absolute values of individual walks or all supports. In particular every contributing walk visits all vertices, so `k\ge |A|`.

Equation (2.2) is the first nontrivial way found here to avoid a literal `2^{|A|}` bound: the cancellation is performed algebraically before absolute values are taken.

**But this is not yet a PR66 repair.** Two load-bearing points remain unproved:

1. the infinite stationary DPP must be represented by a translation-invariant null-state interaction whose coefficients are the appropriate infinite-volume limits of these determinant Möbius coefficients, with the correct boundary terms; finite marginals use `L_\Lambda=K_\Lambda(I-K_\Lambda)^{-1}`, which is not simply the compression of the global `L=K(I-K)^{-1}`;
2. Dobrushin A2 needs an absolute weighted sum of `|J_A|`. Operator-norm convergence of (2.1) alone does not control the sum of absolute values of all setwise coefficients. Replacing (2.2) by absolute walk weights introduces a Schur/`\ell^1` growth constant that need not be `<1` for an arbitrary strict-margin center.

So route (i) is a concrete DPP-specific candidate, not a completed theorem. A small-correlation subclass where the absolute off-diagonal walk norm is contractive may be accessible, but that would be a **new weaker theorem**, not a repair of the original arbitrary-center p>4 quantifier.

Primary-source cross-check: Georgii–Yoo, *Conditional Intensity and Gibbsianness of Determinantal Point Processes*, J. Stat. Phys. 118 (2005), arXiv:math/0401402, explicitly identifies Gibbsian conditional distributions in terms of the DPP `J=K(I-K)^{-1}` under continuity assumptions, and notes that a many-body potential can in principle be extracted. This supports investigating (2.2), but it does not by itself supply the Dobrushin A2 norm required here.

### Route (ii): prove enough stronger DPP decay for A1

The current inverse-localization spine cannot be upgraded to a uniform exponential localization statement under the bare `A_p` hypothesis. The following exact obstruction is independent of any unproved entropy claim.

#### Lemma 2.1 — polynomial `A_p` centers can have genuinely non-exponentially localized inverse kernels

Fix `p>4`. Put

\[
b_r=(1+r)^{-(p+2)},\qquad r\ge1,
\]

and define a real half-period-even function `a` by

\[
\widehat a(\pm 2r)=b_r,\qquad \widehat a(m)=0\ \text{otherwise}.
\]

Then `a\in\mathcal A_p`, because

\[
\sum_{r\ge1}(1+2r)^p b_r<\infty,
\]

and all Fourier coefficients of `a` are nonnegative. Let

\[
B:=2\sum_{r\ge1}b_r<\infty
\]

and choose `0<\varepsilon<1/(4B)`. Set

\[
c(\theta)=\frac12-\varepsilon a(\theta).
\]

Then `c` is real, half-period-even, belongs to `\mathcal A_p`, and

\[
\frac14<c(\theta)<\frac34
\]

for all `\theta` after decreasing `\varepsilon` if necessary.

On `\ell^2(\mathbb Z)`, `T(c)` is positive and invertible. Since `\|2\varepsilon a\|_\infty<1`, the scalar geometric series gives

\[
\frac1{c}=2\sum_{k\ge0}(2\varepsilon a)^k.
\]

All Fourier coefficients of every `a^k` are nonnegative. Therefore, for every `r\ge1`, the `k=1` term alone yields

\[
\widehat{(1/c)}(2r)
\ge 4\varepsilon b_r
=4\varepsilon(1+r)^{-(p+2)}.
\tag{2.3}
\]

Hence the infinite inverse Toeplitz kernel `T(c)^{-1}=T(1/c)` has no exponential off-diagonal bound.

Now let `I_N=[-N,N]` and take the **all-occupied** complete-event matrix `M_N=T_{I_N}(c)`. Suppose, contrary to the claimed obstruction, that there were constants `C,\beta>0`, independent of `N`, with

\[
|(M_N^{-1})_{ij}|\le Ce^{-\beta|i-j|}\qquad(i,j\in I_N).
\tag{2.4}
\]

Because `T(c)\ge \frac14 I`, the Galerkin finite-section solutions

\[
x_N=M_N^{-1}P_Ne_0
\]

converge in `\ell^2` to `x=T(c)^{-1}e_0`: coercivity gives the standard Céa estimate, since the finite-support subspaces increase densely. Therefore, for every fixed `r`,

\[
(M_N^{-1})_{0,2r}\longrightarrow (T(c)^{-1})_{0,2r}=\widehat{(1/c)}(2r).
\]

Passing (2.4) to the limit would give an exponential bound for `\widehat{(1/c)}(2r)`, contradicting (2.3).

So no theorem based only on `p>4`, a strict margin and the complete-event inverse family can replace PR66's polynomial inverse localization by a **uniform exponential** inverse localization estimate.

This lemma does **not** prove that the actual telescoped `\psi_n` fails A1: additional determinant cancellations could in principle make the interaction itself decay faster than the individual propagators. It proves the narrower and useful fact that the present inverse/two-leg mechanism cannot be upgraded to A1 merely by sharpening the same localization estimate.

### Route (iii): genuinely applicable polynomial-memory response, or only finite-order response

A potentially cheaper target than full complex pressure analyticity is fourth-order local response in the physical parameter. For the corrected entropy

\[
F(t)=h(c+tg)+\alpha t^4,
\]

write `H(t)=h(c+tg)`. The conditional calculus requires `H` to be `C^4` near zero and even, `H''(0)=0`, and the strict corrected quartic inequality `H^{(4)}(0)/24+alpha<0`. This is a condition on the corrected functional, including its `alpha t^4` term. Continuity of `H^{(4)}` then gives

\[
F''(t)=\left(\frac12 H^{(4)}(0)+12\alpha\right)t^2+o(t^2),
\]

so `F` is strictly concave for sufficiently small nonzero `t`, with `F''(0)=0`. A sixth-order analytic expansion is stronger than necessary for this conditional conclusion.

This observation narrows the external theorem search: one can replace the unsupported claim of full holomorphic pressure by a theorem giving enough differentiability/response of the stationary chain for the parameterized normalized one-sided conditional `G_t`, with a uniform remainder sufficient to differentiate the entropy identity twice.

Sources checked in this pass:

* Walters-type summable-variation `g`-measure theory and the Bressaud–Fernández–Galves coupling literature do supply uniqueness/convergence/mixing under summable or polynomial continuity rates, but the sources located in this pass do not state a fourth-parameter-derivative theorem with hypotheses already mapped to PR66.
* Fernández–Maillard, *Chains with complete connections: General theory, uniqueness, loss of memory and mixing properties*, provides uniqueness/mixing interfaces for chains with summable variations; it is not being cited here as a fourth-order response theorem.
* Recent linear-response papers for chains with unbounded memory are useful mechanism references but do not, from the checked statements, close the exact fourth-order uniform remainder needed here.

Therefore route (iii) remains **PENDING SOURCE/PROOF**, not imported by name.

## 3. Current verdict

**Original PR66 p>4 theorem: INCOMPLETE.** The Dobrushin import is still not repaired.

What is new and proved in this checkpoint:

1. the A1 branch cannot be rescued by simply upgrading the existing complete-event inverse localization to a uniform exponential bound: Lemma 2.1 gives an explicit legal half-period-even `A_p` center whose inverse Toeplitz kernel has a polynomial lower tail;
2. a DPP-specific null-state route exists at the finite determinant level: Möbius inversion of `log det L_S` can be reorganized as connected closed-walk sums before absolute values, avoiding the naive literal `2^{|A|}` estimate. The infinite-volume/Dobrushin-norm bridge is still missing;
3. only `C^4` physical-parameter response is structurally necessary for the local concavity conclusion; full pressure analyticity is sufficient but not minimal.

No DPP entropy counterexample is claimed. Lemma 2.1 is a method/localization obstruction only.

## 4. Next exact gaps

* **A2 gap:** construct the infinite-volume null-state interaction in the same complex `(s,lambda)` neighborhood and prove the actual Dobrushin A2 weighted absolute norm, or explicitly restrict to a quantitatively contractive subclass and label it as a new weaker theorem.
* **A1 gap:** if pursued despite Lemma 2.1, prove exponential support-cardinality decay of the *interaction itself* from cancellations not available at inverse-entry level.
* **finite-response gap:** prove or source a genuinely applicable `C^4` response theorem for the normalized polynomial-memory chain, including a uniform remainder strong enough for `h''(t)=\frac12h^{(4)}(0)t^2+o(t^2)`.

Independent arithmetic/review queue: **PENDING_REVIEW / REQUESTED only if later assigned; no independent recomputation is assumed to be running.**
