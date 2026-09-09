# N4 round-two support and lift proof v1

Status: `PROVED` for the scoped support, smoothness, Hessian-shell, and
positive-gap lift lemmas below. This file does not prove
`Hess H_face(A)[V,V] <= 0` and does not assert a positive candidate.

## Frozen local statement

Let `U` be a real `4 x 3` matrix with `U^T U = I_3`. Let `z` be a unit vector
spanning `ker U^T`, and assume `z_i != 0` for all four observed coordinates.
For `A in Sym(3)` with `0 < A < I_3`, set

```text
K(A) = U A U^T.
```

For `S subset [4]`, define the exact event mass by the frozen convention

```text
p_A(S) = (-1)^(4-|S|) det(K(A) - diag(1_{i notin S})).
```

Let `P` denote the 15 proper subsets of `[4]`. Define

```text
H_face(A;U) = - sum_{S in P} p_A(S) log p_A(S).
```

The claims proved here are:

1. `p_A([4]) = 0` identically on the fixed face, hence all derivatives of the
   full event along every `K`-affine face direction are zero.
2. `p_A(S) > 0` for every proper `S`.
3. `H_face` is real analytic on `{A: 0 < A < I_3}`.
4. In the six standard symmetric coordinates, its Hessian is

```text
H_{ab}(A)
  = - sum_{S in P} [ p_{S,ab}(A) log p_S(A)
                    + p_{S,a}(A) p_{S,b}(A) / p_S(A) ],
```

   where `p_{S,a}` and `p_{S,ab}` are the first and second coordinate
   derivatives of `p_S`.
5. If a fixed boundary chord has a certified positive face gap, the common
   shrink `K_j(e) = (1-2e)K_j + e I_4` is strictly feasible, preserves the
   midpoint, and has positive strict-kernel entropy gap for all sufficiently
   small positive `e`. A dimension-fixed explicit continuity gate is given.

## L-ensemble identity on the face

Put

```text
B = A (I_3 - A)^(-1),      L = U B U^T.
```

Since `0 < A < I_3`, `B` is positive definite. Also

```text
K(A) = L (I_4 + L)^(-1)
```

because both sides act as `U A U^T` on `range(U)` and as zero on `ker U^T`.

For any finite `L` and `K = L(I+L)^(-1)`, the frozen signed determinant event
formula equals the L-ensemble formula

```text
p_A(S) = det(I_4 + L)^(-1) det L_S.
```

Here `L_S` is the principal submatrix on `S`, with `det L_empty = 1`.
For completeness, multiply the event matrix on the left by `I+L`. With
`D_{S^c}=diag(1_{i notin S})`,

```text
(I+L)(K-D_{S^c}) = L - (I+L)D_{S^c}.
```

After ordering the coordinates as `S, S^c`, this has block form

```text
[ L_S          0 ]
[ L_{S^c,S}  -I ].
```

Its determinant is `(-1)^(4-|S|) det L_S`. Dividing by `det(I+L)` gives the
claimed formula. Since the nonzero eigenvalues of `L` are the eigenvalues of
`B`, this also gives

```text
det(I_4 + L)^(-1) = det(I_3 - A).
```

Thus, for every `S`,

```text
p_A(S) = det(I_3 - A) det(U_S B U_S^T).
```

This formula is interpreted with `det(U_empty B U_empty^T)=1`.

## Support proof

The nullspace of `U^T` is the one-dimensional space `span(z)`. Fix a proper
subset `S`. If `x in R^S` satisfies `U_S^T x = 0`, extend `x` to a vector
`tilde x in R^4` by putting zero outside `S`. Then

```text
U^T tilde x = 0,
```

so `tilde x = c z` for some scalar `c`. Since `S` is proper, choose
`i notin S`. The `i`th coordinate of `tilde x` is zero, while `z_i != 0`;
hence `c=0` and `x=0`.

Therefore `U_S` has full row rank for every proper `S`. For nonempty proper
`S` and nonzero `x in R^S`,

```text
x^T U_S B U_S^T x = (U_S^T x)^T B (U_S^T x) > 0,
```

because `B` is positive definite and `U_S^T x != 0`. Hence
`U_S B U_S^T` is positive definite. Its determinant is positive, and
`det(I_3-A)>0`, so `p_A(S)>0`. For `S=empty`, `p_A(empty)=det(I_3-A)>0`.

For the full event, `K(A)` has rank at most three, so

```text
p_A([4]) = det K(A) = 0.
```

This identity holds for every real symmetric `A`, not just for `0<A<I`.
Consequently, for every face-affine line `A(s)=A+sV`, the polynomial
`det(U A(s) U^T)` is identically zero. All first, second, and higher
derivatives of the full event along the fixed face are zero.

Two useful `n=4, r=3` checks follow from the same formula:

```text
p_A(empty) = det(I_3-A),
p_A([4]\{i}) = z_i^2 det A.
```

The second identity uses `det(U_{[4]\{i}})^2 = z_i^2` and
`det(I-A) det(A(I-A)^(-1)) = det A`. These checks are not used as a separate
entropy decomposition.

## Analyticity and six-coordinate Hessian

Let

```text
D = { A in Sym(3): 0 < A < I_3 }.
```

This is an open subset of the six-dimensional real vector space `Sym(3)`.
For every `S`, the frozen formula

```text
p_A(S)=(-1)^(4-|S|)det(U A U^T - diag(1_{i notin S}))
```

is a polynomial in the six independent entries of `A`. On `D`, every proper
event mass is positive by the support proof. Therefore `log p_A(S)` is real
analytic on `D` for every proper `S`, and the finite sum defining `H_face` is
real analytic on `D`.

Use the symmetric coordinate basis

```text
G_1=E_11, G_2=E_22, G_3=E_33,
G_4=E_12+E_21, G_5=E_13+E_31, G_6=E_23+E_32.
```

For `x in R^6`, write `A(x)=A+sum_a x_a G_a` and set

```text
p_{S,a}(A)  = d/dx_a p_{A(x)}(S) |_{x=0},
p_{S,ab}(A) = d^2/(dx_a dx_b) p_{A(x)}(S) |_{x=0}.
```

Since the full event is identically zero and the 16 event masses sum to one,

```text
sum_{S in P} p_S(A) = 1,
sum_{S in P} p_{S,a}(A) = 0,
sum_{S in P} p_{S,ab}(A) = 0.
```

Differentiating

```text
H_face(A) = - sum_{S in P} p_S(A) log p_S(A)
```

inside the strict domain gives

```text
dH_face[A](W) = - sum_{S in P} Dp_S[A](W) log p_S(A).
```

The `+1` terms cancel by `sum_{S in P} Dp_S[A](W)=0`. Differentiating once
more gives the bilinear Hessian formula

```text
D^2 H_face[A](V,W)
 = - sum_{S in P} D^2p_S[A](V,W) log p_S(A)
   - sum_{S in P} Dp_S[A](V) Dp_S[A](W) / p_S(A).
```

In the six-coordinate basis this is exactly

```text
H_{ab}(A)
  = - sum_{S in P} [ p_{S,ab}(A) log p_S(A)
                    + p_{S,a}(A) p_{S,b}(A) / p_S(A) ].
```

For a symmetric direction

```text
V = v_1 G_1 + ... + v_6 G_6,
```

the directional second derivative is `v^T H(A) v`. The sum is only over the
15 proper events. There is no divergent subtraction and no `0/0` full-event
term: the full event and all its face derivatives are exactly zero before the
entropy derivatives are formed.

## Strict-kernel lift from a positive boundary gap

Let a fixed boundary chord be

```text
K_j = U(A+j tV)U^T,        j=-1,0,+1,
```

with `0 < A +/- tV < I_3`, and suppose its face gap has a certified positive
lower bound

```text
Delta_face
 = (H_face(A-tV;U)+H_face(A+tV;U))/2 - H_face(A;U)
 >= g > 0.
```

For `0 < e < 1/2`, define

```text
K_j(e) = (1-2e)K_j + e I_4.
```

Strict feasibility is immediate from the spectrum. Each `K_j` has eigenvalues
`lambda_1, lambda_2, lambda_3 in (0,1)` on `range(U)` and eigenvalue zero on
`span(z)`. Hence `K_j(e)` has eigenvalues

```text
(1-2e)lambda_i + e   for i=1,2,3,
e                    on span(z).
```

All are in `(0,1)`. Thus `0 < K_j(e) < I_4`. The midpoint is preserved because

```text
(K_-(e)+K_+(e))/2
 = (1-2e)(K_-+K_+)/2 + e I_4
 = (1-2e)K_0 + e I_4
 = K_0(e).
```

For each strict lifted kernel, all 16 exact event masses are positive: if
`0<K<I`, then `L=K(I-K)^(-1)` is positive definite, so every principal minor
of `L` is positive and

```text
p_K(S)=det(I+L)^(-1) det L_S > 0.
```

Continuity gives the sign lift. The exact event masses are polynomials in the
entries of `K`, so the distributions of `K_j(e)` converge to those of `K_j` as
`e downarrow 0`. The entropy function on a finite alphabet is continuous even
when a limiting mass is zero, since `x log x -> 0`. Therefore

```text
Delta(e)
 = (H(K_-(e))+H(K_+(e)))/2 - H(K_0(e))
```

converges to `Delta_face`, and some sufficiently small positive `e` has
`Delta(e)>0`.

The following explicit gate is available in this fixed four-point dimension.
Let `P_K` be the 16-event distribution of a boundary contraction `K`, and
`P_{K(e)}` the distribution after the common shrink. For every event `S`, set

```text
M_S(K)=K-diag(1_{i notin S}).
```

Both `M_S(K)` and `M_S(K(e))` have operator norm at most `2`, and

```text
||M_S(K(e))-M_S(K)||_2 = e ||I-2K||_2 <= e.
```

By multilinearity of the determinant in the four columns,

```text
|det M_S(K(e)) - det M_S(K)| <= 4 * 2^3 * e = 32 e.
```

Thus

```text
||P_{K(e)}-P_K||_1 <= 16 * 32 e = 512 e,
tau(e) := (1/2)||P_{K(e)}-P_K||_1 <= 256 e.
```

For `tau <= 15/16`, the Fannes-Audenaert entropy continuity bound on a
16-point alphabet, with natural logarithms, gives

```text
|H(P_{K(e)})-H(P_K)|
 <= omega(e)
 := tau(e) log 15 + h_2(tau(e)),
```

where `h_2(t)=-t log t-(1-t)log(1-t)`, with the usual value `h_2(0)=0`.
It is enough to impose

```text
0 < e <= 15/4096
and
2 omega(e) < g.
```

Indeed, applying the entropy bound to `j=-1,0,+1` gives

```text
|Delta(e)-Delta_face| <= 2 omega(e),
```

so `Delta(e) >= g - 2 omega(e) > 0`.

This gate is only a rigorous existence and screening criterion once a positive
boundary lower bound `g` is already certified. It does not create a candidate.
For a final strict rational certificate one should still freeze rational
`U,A,V,t,e` or rational `K_j,e`, compute the exact event masses for the lifted
kernels, and certify the strict entropy gap by rigorous logarithm enclosures.

## Optional general support lemma

The support argument has the following direct `n x r` form. Let
`U in R^(n x r)` satisfy `U^T U=I_r`, and assume `U` is full spark in the row
sense: every set of at most `r` rows is linearly independent, equivalently
every `r x r` row minor is nonzero. Let `0<A<I_r` and `K=UAU^T`. Then the
finite DPP exact event support is precisely

```text
{ S subset [n] : |S| <= r }.
```

Using `B=A(I-A)^(-1)` and `L=UBU^T`, the same L-ensemble formula gives

```text
p_K(S)=det(I_r-A) det(U_S B U_S^T).
```

If `|S|<=r`, full row rank of `U_S` makes `U_S B U_S^T` positive definite, so
`p_K(S)>0`. If `|S|>r`, `rank L <= r`, so `det L_S=0` and `p_K(S)=0`.

For `n=4,r=3`, the assumption that the null vector `z` has no zero coordinate
is equivalent to the nonvanishing of all three-row minors, since those minors
are the cofactors giving the one-dimensional null vector of `U^T`.

This appendix is only a support lemma. It does not change the frozen N4 target
and does not assert any five-point curvature result.
