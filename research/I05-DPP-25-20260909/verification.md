# Verification ledger

## Status and review boundary

**Author status: PROVED. Independent review: pending.**

This ledger is a self-check, not an independent review. The only non-elementary imported step is the one-dimensional finite-first-moment analyticity theorem identified in `sources.md`.

## 1. Frozen quantifiers

Checked theorem quantifiers:

- one fixed exponent `p>4`;
- fixed real `c,g\in\mathcal A_p`;
- `c(\theta+1/2)=c(\theta)` and `g(\theta+1/2)=-g(\theta)` almost everywhere;
- fixed strict margin `\delta\le c\le1-\delta`;
- arbitrary nonzero direction `g`, with no small-norm hypothesis;
- any odd `k` with `\widehat g(k)\ne0`;
- an existential radius `\varepsilon(c,g,p,\delta,k)>0`;
- no claim of a radius uniform over the whole class.

No mean `\mu=1/2` assumption and no evenness of the real symbols was introduced.

## 2. Correct probability object

For a finite index set `I` and configuration `x`, with `Z_x=\{i:x_i=0\}`,

\[
\mathbf P_f(X_I=x)
=(-1)^{|Z_x|}\det(T_I(f)-I_{Z_x}).
\]

All conditionals in the proof are ratios of these complete-event probabilities. No inclusion probability `\det K_T` is used as a configuration atom. The final object is the limit of full configuration Shannon entropies per site.

## 3. Complete-event singular gap

With `M=T_I(c)-I_Z` and `J=I_S\oplus(-I_Z)`, direct block multiplication gives

\[
\operatorname{Re}\langle v,JMv\rangle
=\langle u,K_{SS}u\rangle
+\langle w,(I-K_{ZZ})w\rangle.
\]

The mixed terms are conjugates with opposite signs, so their real parts cancel. The spectral margin gives

\[
\|Mv\|_2\ge\delta\|v\|_2,
\qquad
\|M^{-1}\|_{2\to2}\le\delta^{-1}
\]

uniformly in window and configuration. Also

\[
-(1-\delta)I\le M\le(1-\delta)I.
\]

This check is valid for complex Hermitian Toeplitz compressions; real symmetry is not needed.

## 4. Polynomial inverse localization and exponent arithmetic

The chosen exponent is

\[
q=(p+2)/4.
\]

Then

\[
q>3/2,
\qquad
2q+1-p=(4-p)/2<0.
\]

For a bandwidth-`W` truncation `B`, the series

\[
B^{-1}=B\sum_{r\ge0}(I-B^2)^r
\]

is legitimate because the spectrum of `B` lies in

\[
[-(1-3\delta/4),-3\delta/4]
\cup
[3\delta/4,1-3\delta/4].
\]

The `r`-th term has bandwidth at most `(2r+1)W` and operator norm at most `\rho^r`, hence weighted Schur norm

\[
O\bigl(W^{q+1}(r+1)^{q+1}\rho^r\bigr).
\]

The weighted tail is

\[
\|E\|_{S_q}\le(1+W)^{q-p}\|c\|_{\mathcal A_p}.
\]

Their product is `O(W^{2q+1-p})`, which tends to zero. This proves a common inverse bound for every finite complete-event matrix. No infinite-section theorem is silently substituted for this finite-section uniform statement.

## 5. Common complex disk

The perturbation satisfies

\[
\|T_I(g)\|_{S_q}\le\|g\|_{\mathcal A_q}
\]

uniformly in `I`. The Neumann condition

\[
|z|B_q\|g\|_{\mathcal A_q}<1/2
\]

therefore gives a nonzero complex disk independent of the conditioning window and event. This is the common response neighborhood that bare approximation lacks.

For real `t`, legality follows separately from

\[
|t|\|g\|_\infty\le\delta/2.
\]

## 6. Conditional Schur complement and squared influence

For future event matrix `M_{R,x}`,

\[
q_{R,z}(x)=\mu-u_RM_{R,x}^{-1}v_R.
\]

If one conditioned bit at `j` is flipped, the event matrix changes by `\pm e_je_j^*`. The resolvent difference factors as

\[
M_y^{-1}-M_x^{-1}
=\mp M_y^{-1}e_je_j^*M_x^{-1}.
\]

Each origin-to-`j` effective coupling is `O(j^{-q})`; their product is `O(j^{-2q})`. This verifies that the decisive decay is squared. Merely summing a one-leg `O(j^{-q})` estimate would give a weaker and incorrect regularity threshold.

Adding the last conditioned site produces the same two-leg factorization by block inversion, so the finite-future conditionals converge uniformly and holomorphically.

## 7. Non-nullness

For real `z=0`, the occupied-site enlarged event matrix has inverse entry `q_{R,0}^{-1}`. The common inverse operator bound gives `q_{R,0}\ge\delta`. The vacant-site enlargement similarly gives `1-q_{R,0}\ge\delta`. Uniform parameter continuity permits a smaller common complex disk on which both logarithm branches are nonzero.

## 8. Interaction moment

The telescoping increment changes only coordinate `n`, hence

\[
\|\psi_{n,z}\|_\infty=O(n^{-2q}).
\]

For fixed `n`, exactly `n+1` translated intervals of diameter `n` contain the origin. Thus

\[
\sum_{A\ni0}\operatorname{diam}(A)\|U_{z,A}\|_\infty
\le C\sum_{n\ge1}n(n+1)n^{-2q}<\infty
\]

because `q>3/2`. The singleton term `n=0` is separately bounded, so absolute summability and the first moment both hold. Local uniformity on the complex disk proves Banach-valued holomorphy by the Weierstrass test.

## 9. Exact DPP equilibrium identification

For any invariant `\rho`, future conditional cross entropy gives

\[
h(\rho)+\rho(\phi_t)
=-\int D_{\rm KL}(r_\rho\|G_t)\,d\rho\le0.
\]

Stationarity and the `1/|A|` specific-energy normalization give exactly

\[
\rho(e_{U_t})=-\rho(\phi_t).
\]

Therefore

\[
h(\rho)-\rho(e_{U_t})\le0,
\]

with equality for the DPP because its future conditional is `G_t`. Hence `P(U_t)=0` and the DPP is an equilibrium state. This is written in full in `equilibrium_bridge.md` and supersedes the informal chain-to-Gibbs paragraph in `proof.md`.

## 10. Imported analyticity theorem

The constructed interaction satisfies a stronger first-moment norm than the usual orbit-normalized convention. Dobrushin and Cassandro–Olivieri are invoked for:

- uniqueness of the one-dimensional Gibbs/equilibrium state;
- analytic pressure/free energy;
- analytic local expectations and pressure derivatives;
- analytic dependence along a holomorphic finite-first-moment interaction curve.

This invocation, rather than the elementary DPP algebra, is the main item requiring independent literature-level audit.

## 11. Parity and even analytic parameter

Half-period support gives

\[
K_{c-zg}=DK_{c+zg}D,
\qquad D_{jj}=(-1)^j.
\]

Since every event diagonal commutes with `D`, all complete-event determinants and Schur complements are invariant under `z\mapsto-z`. Therefore `G_z,\phi_z,U_z` are even and factor holomorphically through `s=z^2`.

## 12. Entropy and relative-entropy sign check

Under

\[
P(U)=\sup_\rho[h(\rho)-\rho(e_U)],
\]

pressure differentiation is

\[
DP(U)[V]=-\nu_U(e_V).
\]

Thus, with `F(s,\lambda)=P(\lambda U_s)`, 

\[
h_s=F(s,1)-\partial_\lambda F(s,1).
\]

For `\Delta_s=U_s-U_0`, the specific relative entropy is

\[
d(\nu_s\|\nu_0)
=P(U_0)-P(U_s)+DP(U_s)[\Delta_s].
\]

At `s=0`, the two first derivatives cancel. This proves an analytic expansion beginning at `s^2=t^4`.

## 13. Exact finite-volume KL identity

Within every finite block, the even-coordinate and odd-coordinate marginals do not depend on `t`. At `t=0`, the kernel is block diagonal across parity, so these two marginals are independent. Therefore

\[
D(\nu_t^{(n)}\|\nu_0^{(n)})
=H(\nu_0^{(n)})-H(\nu_t^{(n)})
\]

exactly, before taking limits. This is not a window extrapolation or a numerical observation.

## 14. Matching coefficient

The accepted matching bound gives

\[
\mathcal R(t)
\ge\frac12 d_{\rm Ber}
(\mu^2-|\widehat g(k)|^2t^2\|\mu^2).
\]

Using

\[
d_{\rm Ber}(q-u\|q)
=\frac{u^2}{2q(1-q)}+O(u^3)
\]

with `u=|\widehat g(k)|^2t^2` gives

\[
C_k=\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}.
\]

The correction coefficient is `\alpha_k=C_k/2`. The second derivative of `\alpha_k t^4` is `12\alpha_k t^2=6C_k t^2`, matching the retained curvature floor.

## 15. Strictness of the regularity extension

For the displayed power-law example, the weighted Fourier sum behaves as

\[
\sum_{m\ge1}m^p m^{-(p+2)}=\sum_{m\ge1}m^{-2}<\infty.
\]

Every exponential weight makes the corresponding sum diverge because the coefficients are nonzero at infinitely many indices and decay only polynomially. Supremum-norm estimates preserve a strict spectral margin. Hence the example lies in `\mathcal A_p` but in no exponential weighted Wiener class.

## 16. Approximation obstruction check

For

\[
F_N(t)=t^4+N^{-2}e^{-N^2t^2},
\]

one has `\|F_N-t^4\|_\infty\le N^{-2}` and

\[
F_N''(t)=12t^2+e^{-N^2t^2}(4N^2t^2-2).
\]

On `|t|\le(2N)^{-1}`, `N\ge2`, this is at most

\[
3/N^2-e^{-1/4}<0.
\]

Every approximant is therefore locally concave on a shrinking interval, while the uniform limit `t^4` is locally convex. This verifies the claimed mechanism obstruction even within real-entire approximants. It is not asserted to be a DPP counterexample.

## 17. Code and numerical consistency

No code, floating-point computation, interval arithmetic, enumeration, or external numerical certificate is used. There are no numerical inputs or error tolerances to reconcile with the text.

## Remaining review obligations

1. Audit the exact Banach-neighborhood formulation of the Dobrushin–Cassandro–Olivieri theorem against the strong norm in (4.3).
2. Independently reproduce the finite-section weighted inverse estimate and the two-leg conditional influence bound.
3. Check the accepted PR53 matching lemma is imported only in its regularity-free form.

These are review obligations, not unstated mathematical gaps in the author proof.
