# Independent mathematical FIRST report

**STATUS: CORRECT_WITHIN_SCOPE**

No critical logical gap was found in the frozen source proof. This disposition certifies the mathematical implications and quantifier handling described below. It does **not** independently certify the large rational base comparisons on which the fixed numerical fixture and explicit radii depend.

## Disposition by claim

| Claim | Mathematical FIRST | Remaining gate |
|---|---|---|
| Fixed 3+3 full maximal chord | Source proof is correct and uses the physical affine `K(t)` and all 64 complete events | Exact base coefficients, interval extrema, logarithm bounds, and root isolation require independent finite/source reconstruction |
| Coefficient radius `10^-6` | Perturbation transfer is correct | Base strict margins and their application require independent finite reconstruction |
| Matrix-factor radius `10^-12` | Map into the coefficient neighborhood is correct | Exact reference margins and source entries require independent finite/source reconstruction |
| Uniform moving simple-endpoint theorem | Correct as an analytic implication under its frozen hypotheses | None beyond the seed margin and simple-endpoint hypotheses |
| Relative-open classes for every fixed `m,n>=3` | Correct, conditional on the accepted seed theorem | Inherits the seed's independent finite gate; radius remains existential |

## Proof reconstruction

### Complete law and curvature

For a complete event `(S,T)`, diagonal expansion gives the signed event determinant. Schur complementation with `B=UV^T` yields

`p_t(S,T)=mu(S,T) det(I_2-t^2 G_A(S)G_C(T))`

`=mu(S,T)(1-sa+s^2 b)`, with `s=t^2`, `a=tr(G_A G_C)` and `b=det(G_A)det(G_C)`.

Fixed block marginals give the conditional cancellations of both `a` and `b`. Hence the mutual-information difference is exactly `E_mu[q log q]`. Differentiating the genuine affine-`K` complete law, using `sum p''=0`, gives

`Gamma(s)=-H''(t)/t^2=E_mu[4(a-2sb)^2/q+2(a-sb)(a-6sb)lambda(q)]`.

This keeps the full Fisher and acceleration contributions. At `s=0`, the expression has the independently derived limit `6 E_mu a^2`, and the fourth-order expansion gives `H''(0)=0`.

### Continuum interval reduction and rare endpoint atom

The inequality

`z lambda(q) >= lambda_lo z-(lambda_hi-lambda_lo)(-z)_+`

is valid for both signs of `z` because `lambda` is positive and decreasing. The required `q`, `v^2`, `z`, and negative-part budgets reduce to exact extrema of quadratics on closed intervals. Thus the proof is genuinely continuum-wide and does not promote a time grid.

On the final interval the full event is correctly removed from the 63-event group and retained separately. From `v_e>1/4`, `|z_e|<3`, and `0<q_e<=1/300`, its complete contribution obeys

`4v_e^2/q_e+2z_e lambda(q_e) > 155/(1196 q_e)>0`.

The step uses `q log(1/q)<1/50` and the exact factor `1/(1-q)<=300/299`; no negative logarithmic acceleration term is dropped. This supplies a pointwise bound across the entire singular interval, not only an endpoint asymptotic.

### Legal endpoint and closed-chord conclusion

The interval rows keep the relevant event likelihoods strictly positive before the displayed full-event root. In particular `det K(t)` never vanishes earlier; continuity from the positive-definite center prevents an earlier loss of positive definiteness. The full-event quadratic has a simple first root because its derivative retains a strict sign. The empty-event determinant stays positive, so `I-K(t)` stays positive definite. Convexity of the affine contraction feasibility set and the immediate negative full determinant after the root exclude legal re-entry. The simple root gives a one-dimensional kernel.

The negative endpoint follows by block-sign conjugation. The normalized curvature bound gives concavity of `H+t^4/24` on the strict interior, and continuity of `x log x` extends it to the closed chord. Strict Jensen concavity of `H` follows from the strictly convex quartic gap for distinct chord points.

### Quantitative coefficient and matrix-factor neighborhoods

Under coordinatewise coefficient error `epsilon`, the source bounds imply

- `|Delta q|<=2 epsilon`, `|Delta v|<=3 epsilon`;
- `|Delta(v^2)|<=24 epsilon`, `|Delta z|<=37 epsilon`;
- `||Delta mu||_1<=16 epsilon`.

Combining these with `|v^2|<=16` and `|z|<=24` gives exactly `280 epsilon` and `421 epsilon`; the positive-part and interval-supremum operations are 1-Lipschitz. The same errors preserve the rare root and its derivative reserve, so the endpoint is allowed to move.

For the entrywise matrix-factor box, the operator perturbation is at most `3 eta`. If `A` has spectrum in `[1/4,3/4]` and `D` is a coordinate projection, the block Schur-complement argument excludes spectrum of `A-D` from `(-1/4,1/4)`, hence `||(A-D)^(-1)||<=4`. The resolvent and two-factor expansions give the stated `72 eta`, `240 eta`, `4224 eta`, and `270336 eta` bounds. The determinant, marginal-event, rank-two, dense-cross-entry, and internal-correlation persistence arguments then map `eta=10^-12` strictly inside `epsilon=10^-6`.

### Moving simple endpoints

The endpoint theorem orders its quantifiers correctly.

1. Strict separation of the leading rank-two Schur eigenvalue from the second eigenvalue and the complementary constraint first produces a continuously moving, simple, singly active endpoint and uniform spectral/coefficient bounds.
2. Along `t=rT`, affine interpolation gives `K(rT)>=kappa(1-r)I` and a uniform lower bound for `I-K(rT)`.
3. The exact identity `p_E=det(I-K)det L_E`, with `L=K(I-K)^{-1}>=K`, yields a lower bound for **every** complete atom and therefore a common logarithm bound even when spectator atoms vanish at the seed endpoint.
4. The full-event factorization `d(1-r^2)(1-gamma r^2)` supplies a uniform `c/(1-r)` Fisher pole. The bound on `sum_E |p_E''|` retains every acceleration term. The explicit positive `delta_0` makes Fisher dominance uniform.
5. Only after this endpoint width is fixed does joint continuity of the exact normalized curvature close the remaining compact interior.

Complementation covers the singly active `I-K` endpoint. The proof expressly excludes simultaneous and multiple endpoints.

Appending strict independent spectators preserves entropy additivity, the seed margin, and its simple active endpoint. Small generic perturbations inside the resulting relative-open neighborhood avoid the finitely many zero-entry polynomial hypersurfaces, so fully correlated marginal blocks and nonzero cross entries exist for each fixed `m,n>=3`. No dimension-uniform radius is inferred.

## Scope safeguards

- This is not an entropy counterexample; the common-window failure is only a method obstruction.
- No observed-basis rotation, projected entropy, quantum entropy, or affine-`L` path replaces the stated Shannon entropy.
- Finite PASS is not used as a universal theorem.
- The higher-dimensional theorem is an open-class existence result, not a universal moving-rank-two result.
- Novelty and formal verification were not assessed.

## Remaining independent obligation

An independent finite/source role must reconstruct, rather than merely rerun, the 30 source entries, 64 complete-event coefficients, Schur coefficients, exact continuum extrema, six directed logarithm bounds, robust perturbation margins, spectral/rank data, and both endpoint isolations. Until that closes, the numerical fixture and explicit radii remain `PENDING_INDEPENDENT_FINITE_SOURCE` even though their source-proof chain is `CORRECT_WITHIN_SCOPE`.
