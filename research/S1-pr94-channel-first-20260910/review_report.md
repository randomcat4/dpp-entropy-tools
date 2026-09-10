# Independent mathematical FIRST report: local-channel lift

**STATUS: CORRECT_WITHIN_SCOPE**

No critical logical gap was found in the frozen local-channel source proof. The structural theorem is accepted within scope. The explicit rational example remains separately gated by independent finite/source reconstruction.

## Disposition by unit

| Unit | Mathematical FIRST | Remaining gate |
|---|---|---|
| Finite binary-channel refinement and entropy identity | CORRECT_WITHIN_SCOPE | None |
| DPP closure under refined channels | CORRECT_WITHIN_SCOPE | None |
| Actual-coordinate mode expansion | CORRECT_WITHIN_SCOPE | None |
| Higher-dimensional whole-chord lift from accepted m-by-2 theorem | CORRECT_WITHIN_SCOPE | Exact imported blob remains the unbroadened premise |
| Quantitative curvature transfer and half-filled formula | CORRECT_WITHIN_SCOPE | None |
| Explicit rational 3+3 mode family and negative fiber | Source proof correct | Independent exact reconstruction pending |

## Proof reconstruction

### Selector refinement

For a finite channel `Q_x(y)`, the difference vector `d=Q_1-Q_0` has equal positive and negative mass. A coupling `gamma_{pn}` between these masses gives conditional selector probabilities

`alpha_(p,n)(p)=gamma_{pn}/d_p`, `alpha_(p,n)(n)=gamma_{pn}/(-d_n)`.

Their sum is one at each output. Direct substitution shows

`P(J=(p,n)|X=x)=gamma_{pn}[Q_0(p)/d_p+Q_0(n)/(-d_n)]`,

independent of `x`, while the oriented binary output has success probability `a_j+theta_j x` with `0<=a_j<a_j+theta_j<=1`. Zero-difference outputs and the entirely uninformative channel are correctly handled by deterministic selectors.

For independent coordinate channels, the selector tuple is independent of the entire input law. The two chain-rule evaluations of `H(Y,J)` then give the displayed identity: selector entropy minus a term affine in the one-coordinate input marginals, plus a fixed positive mixture of conditional binary-output entropies. Equality, not data processing, is used.

### Refined DPP laws

For a selector tuple, determinant multilinearity gives

`E prod_(i in S)(a_i+theta_i X_i)=det((A+D K D)_S)`.

Thus the entire refined binary law is the DPP with kernel `A+D K D`. Positivity follows from `A>=0`, and

`I-A-DKD=(I-A-D^2)+D(I-K)D>=0`

because `a_i+theta_i<=1`. Along a true affine path, every transformed kernel remains truly affine. The affine marginal correction has zero second and mixed affine derivatives, so the identity preserves the complete Fisher plus acceleration expression. No `L`-affine or spectral entropy path is substituted.

### Actual-coordinate realization

With disjoint-support isometry `W` and block background `R`, the observed kernel splits spectrally into the base kernel on `Ran W` and fixed strict backgrounds on its orthogonal complement. Hence its legal interval is exactly the base interval.

For a fixed observed configuration, the determinant lemma gives

`det(E+WKW^T)=prod_i det(E_i) det(I+K diag(g_i))`.

Principal-minor expansion identifies this with the expectation of the product of local complete-event determinants under the base DPP. Multiplying complete-event signs proves the product-channel law in the actual observed coordinates. Since both sides are polynomial in the entries, singular `E_i` are covered without dividing by a zero event probability.

The local empty output for input one and full output for input zero vanish, whereas the opposite probabilities are positive. Their paired selector therefore has positive weight and exactly `a=0, theta=1`. This is the required all-revealing strictness witness.

### Whole-chord lift and strictness

After conditioning on any selector tuple, the transformed base path still has the real m-by-2 radial form covered by the exact accepted premise. The diagonal entropy correction is constant on a cross-block radial path. Each summand is therefore concave throughout the base legal interval, and legality equivalence shows this is the expanded path's maximal interval.

The positive all-revealing selector contributes the unchanged base entropy with positive weight. When `B!=0`, this one summand is strictly Jensen-concave, so the whole fixed positive mixture is strict, including boundary chords. Concavity in `s=t^2` transfers in the same way.

### Quantitative curvature

For any nonzero base cross entry, the joint inclusion event changes from its decoupled probability by `-s B_ij^2`. Log-sum reduction to that binary event and the binary KL second derivative bound `1/[p(1-p)]>=4` give

`I(s)>=2s^2 B_ij^4`.

Concavity of `G(s)=H(K(sqrt(s)))` yields `G'(s)<=-I(s)/s`; therefore

`H''(t)=2G'(s)+4sG''(s)<=-4B_ij^4 t^2`.

Inside a selector summand the cross entry is multiplied by `sqrt(theta_i theta_j)`. Averaging the fourth power gives the exact factors `kappa_i=sum_j c_ij theta_ij^2`, proving the displayed output bound. Mode channels have `kappa_i>0` because of the revealing selector.

### Half filling and the explicit mode family

For background `(I-vv^T)/2`, direct complete-event expansion gives

`Q(T|x)=2^(-d)[1+(2x-1)h(T)]`.

Complement pairs have fixed weight and oriented parameter `theta=|h|`, so the general identity reduces to the stated explicit mixture. Averaging `h^2` over fair signs gives `kappa=sum_a v_a^4`; for `v=(3/5,4/5)` this is `337/625`.

The formulas in `MODE_FAMILY.md` are consistent with this theorem. In particular the selected conditional probabilities have the form `p_star+(1-2s)^2 d`; at `s=1/2` every Fisher term vanishes, while

`-8 sum_T d_T log(1+d_T/p_star(T))<0`

because each summand before the leading minus is nonnegative and at least one is strict. This is a conditional-relative-entropy mechanism obstruction, not a negative full Shannon-curvature or entropy counterexample. The exact displayed matrices, endpoint, interval enclosure, and row-pair minors still require independent finite reconstruction.

## Boundary and scope checks

- Deterministic coordinates are legitimate continuous limits; informative selector pairs have `theta>0` and remain legal.
- The affine correction remains valid when input diagonals move, but is constant in the radial application.
- Strictness is not inferred from arbitrary marginalization; it is carried by a positive unchanged-base summand.
- General filling uses the refined selector theorem. The uniform complement-pair rule is used only at half filling.
- The construction is coordinate-based and imposes proportional observed rows or columns; it does not cover the original PR58 frame with all pair minors nonzero.
- The explicit negative fiber is not the full entropy Hessian.

## Remaining independent obligation

The structural channel theorem needs no new numerical gate. A separate finite/source role should independently reconstruct the asymmetric selector example, the 16 refined polynomial identities, both 64-event observed laws, the explicit 3+3 matrices and endpoint, the negative-fiber exact sign enclosure, the curvature coefficient, and the original-frame representation obstruction. Merely rerunning the author SymPy checker is not independent certification.
