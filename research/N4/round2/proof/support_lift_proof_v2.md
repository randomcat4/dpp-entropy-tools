# N4 round-two support and BSC-lift proof v2

Status: `PROVED` for the scoped support, smoothness, Hessian-shell, and
positive-gap lift lemmas below. Compared with v1, this version keeps the same
support and Hessian proof but replaces the determinant/Fannes lift gate by the
tighter bit-flip channel gate

```text
Delta(e) >= Delta_face - 4 h_b(e).
```

It does not prove `Hess H_face(A)[V,V] <= 0`, does not assert a positive
candidate, and does not use any five-point mechanism.

## Frozen local statement

Let `U` be a real `4 x 3` isometry, `U^T U=I_3`. Let `z` be a unit vector
spanning `ker U^T`, and assume `z_i != 0` for all four observed coordinates.
For `A in Sym(3)` with `0<A<I_3`, set `K(A)=UAU^T`. The exact event masses are

```text
p_A(S)=(-1)^(4-|S|) det(K(A)-diag(1_{i notin S})),   S subset [4].
```

Let `P` be the 15 proper subsets of `[4]` and

```text
H_face(A;U)=-sum_{S in P} p_A(S) log p_A(S).
```

This file proves:

1. `p_A([4])=0` identically on the fixed face, so all its derivatives along
   every `K`-affine face direction vanish.
2. `p_A(S)>0` for every proper `S`.
3. `H_face` is real analytic on the strict domain `{0<A<I_3}`.
4. In the six standard symmetric coordinates,

```text
H_{ab}(A)
  = - sum_{S in P} [ p_{S,ab}(A) log p_S(A)
                    + p_{S,a}(A) p_{S,b}(A)/p_S(A) ].
```

5. If a fixed boundary chord has certified positive face gap at least `g>0`,
   then the common shrink `K_j(e)=eI_4+(1-2e)K_j` gives a strict interior chord
   with positive entropy gap whenever `4 h_b(e)<g`.

All logarithms are natural, and `h_b(e)=-e log e-(1-e)log(1-e)`.

## Event support on the rank-three face

Put

```text
B=A(I_3-A)^(-1),       L=UBU^T.
```

Then `B` is positive definite and `K(A)=L(I_4+L)^(-1)`. For
`D_{S^c}=diag(1_{i notin S})`,

```text
(I+L)(K-D_{S^c})=L-(I+L)D_{S^c}.
```

After ordering the coordinates as `S,S^c`, the last matrix has block form

```text
[ L_S          0 ]
[ L_{S^c,S}  -I ].
```

Therefore the frozen signed determinant law is

```text
p_A(S)=det(I_4+L)^(-1) det L_S
      =det(I_3-A) det(U_S B U_S^T),
```

with `det L_empty=1`.

Now fix a proper subset `S`. If `x in R^S` and `U_S^T x=0`, extend `x` by zero
outside `S` to `tilde x in R^4`. Then `U^T tilde x=0`, so
`tilde x=c z`. Since `S` is proper and every coordinate of `z` is nonzero,
some coordinate outside `S` forces `c=0`; hence `x=0`. Thus `U_S` has full row
rank for every proper `S`.

For nonempty proper `S`,

```text
x^T U_S B U_S^T x=(U_S^T x)^T B(U_S^T x)>0
```

for every nonzero `x`, so `U_S B U_S^T` is positive definite. Since
`det(I_3-A)>0`, all proper event masses are positive. For `S=empty`,
`p_A(empty)=det(I_3-A)>0`.

For the full event, `rank K(A)<=3`, hence

```text
p_A([4])=det K(A)=0.
```

This is an identity in the entries of `A`; along any face-affine line
`A(s)=A+sV`, all derivatives of `p_{A(s)}([4])` vanish.

Useful checks in this `n=4,r=3` case are

```text
p_A(empty)=det(I_3-A),
p_A([4]\{i})=z_i^2 det A.
```

The second check uses the cofactor identity `det(U_{[4]\{i}})^2=z_i^2`. These
checks are only support facts here, not an entropy decomposition.

## Analyticity and six-coordinate Hessian

Each `p_A(S)` is a polynomial in the six independent symmetric entries of
`A`, by the frozen signed determinant formula. On the strict domain `0<A<I_3`,
all 15 proper masses are positive. Hence each `log p_A(S)` for proper `S` is
real analytic there, and so is `H_face`.

Use the coordinate basis

```text
G_1=E_11, G_2=E_22, G_3=E_33,
G_4=E_12+E_21, G_5=E_13+E_31, G_6=E_23+E_32.
```

For `A(x)=A+sum_a x_a G_a`, write

```text
p_{S,a}(A)  = partial_a p_{A(x)}(S)|_{x=0},
p_{S,ab}(A) = partial_a partial_b p_{A(x)}(S)|_{x=0}.
```

The full event is identically zero and the 16 event masses sum to one, so

```text
sum_{S in P} p_S=1,       sum_{S in P} p_{S,a}=0,
sum_{S in P} p_{S,ab}=0.
```

Differentiating only the finite sum over the 15 proper events gives

```text
dH_face[A](W)=-sum_{S in P} Dp_S[A](W) log p_S(A),
```

and

```text
D^2H_face[A](V,W)
 = -sum_{S in P} D^2p_S[A](V,W) log p_S(A)
   -sum_{S in P} Dp_S[A](V)Dp_S[A](W)/p_S(A).
```

Equivalently, the six-coordinate Hessian entries are

```text
H_{ab}(A)
  = - sum_{S in P} [ p_{S,ab}(A) log p_S(A)
                    + p_{S,a}(A) p_{S,b}(A)/p_S(A) ].
```

For `V=sum_a v_a G_a`, the directional second derivative is `v^T H(A)v`.
There is no full-event entropy term, no divergent subtraction, and no boundary
limit exchange: the zero full event and all its face derivatives have already
been deleted exactly.

## Bit-flip channel representation of the lift

Let `X` be the `{0,1}^4` DPP with marginal kernel `K`, where `0<=K<=I`.
Let `N_1,...,N_4` be independent Bernoulli(`e`) variables, independent of `X`,
and define

```text
Y_i = X_i xor N_i,        0 <= e <= 1/2.
```

Then `Y` is a DPP with kernel

```text
K_e = e I_4 + (1-2e)K.
```

To prove this, use the DPP generating function

```text
E prod_i q_i^{X_i} = det(I + diag(q_i-1) K).
```

For `w_i=q_i-1`,

```text
E[q_i^{Y_i} | X_i]
 = 1 + e w_i + (1-2e) w_i X_i.
```

Therefore

```text
E prod_i q_i^{Y_i}
 = prod_i(1+e w_i)
   det(I + diag((1-2e)w_i/(1+e w_i)) K)
 = det(I + diag(w_i)(eI+(1-2e)K)).
```

The displayed calculation is first read where the temporary denominators are
nonzero; since both sides are polynomials in the `q_i`, the identity extends
to all values. This is exactly the generating function of the DPP with kernel
`K_e`.

If `0<K<I`, this is the usual strict DPP. If the original `K` is a boundary
contraction with eigenvalues in `[0,1]` and `0<e<1/2`, then every eigenvalue of
`K_e` lies in `(0,1)`, so `K_e` is strict. In particular, for the rank-three
face kernels `K_j=U(A+jtV)U^T`, `0<A+jtV<I_3`, the lifted kernels

```text
K_j(e)=eI_4+(1-2e)K_j
```

are strict for `j=-1,0,+1`.

For each strict lifted kernel, all 16 exact event masses are positive. Indeed,
if `0<K<I`, then `L=K(I-K)^(-1)` is positive definite, every principal minor
of `L` is positive, and

```text
p_K(S)=det(I+L)^(-1) det L_S > 0
```

for every `S subset [4]`.

The midpoint is preserved:

```text
(K_-(e)+K_+(e))/2
 = eI_4+(1-2e)(K_-+K_+)/2
 = eI_4+(1-2e)K_0
 = K_0(e).
```

## Entropy gate from the channel

Let `T_e` be the independent bit-flip channel on four bits. Its transition
matrix is doubly stochastic. By Birkhoff's theorem it is a convex combination
of permutation matrices, so Shannon entropy cannot decrease under `T_e`:

```text
H(Y) >= H(X).
```

The upper bound is also immediate because `Y` is a deterministic function of
`(X,N)` and `N` is independent of `X`:

```text
H(Y) <= H(X,N) = H(X)+H(N)
              = H(X)+4 h_b(e).
```

Thus, for every four-point DPP kernel `K`,

```text
0 <= H(K_e)-H(K) <= 4 h_b(e).
```

Now suppose a fixed boundary chord has certified positive face gap

```text
Delta_face
 = (H_face(K_-)+H_face(K_+))/2 - H_face(K_0)
 >= g > 0.
```

Here `H_face(K_j)` equals the ordinary finite entropy of the boundary DPP,
with the zero full-event contribution omitted exactly. Write

```text
eta_j(e)=H(K_j(e))-H(K_j).
```

The channel bound gives `eta_j(e)>=0` for the two endpoints and
`eta_0(e)<=4h_b(e)` for the center. Therefore

```text
Delta(e)
 = (H(K_-(e))+H(K_+(e)))/2 - H(K_0(e))
 = Delta_face + (eta_-(e)+eta_+(e))/2 - eta_0(e)
 >= Delta_face - 4 h_b(e)
 >= g - 4 h_b(e).
```

Consequently any rational `e` with

```text
0 < e < 1/2
and
4 h_b(e) < g
```

gives a strictly feasible interior chord with positive entropy gap. This is a
dimension-fixed explicit lift gate, but it only applies after the boundary
gap lower bound `g>0` has already been certified. It does not produce or
certify a positive boundary candidate.

For a final strict rational certificate, one should still freeze rational
`U,A,V,t,e` or rational `K_j,e`, compute the exact lifted event masses, and
certify the strict entropy gap with rigorous logarithm enclosures.

## Optional general support lemma

The support part has a direct `n x r` extension. Let `U in R^(n x r)` satisfy
`U^T U=I_r`, and assume it is full spark in the row sense: every set of at most
`r` rows is linearly independent, equivalently every `r x r` row minor is
nonzero. For `0<A<I_r` and `K=UAU^T`, put `B=A(I_r-A)^(-1)` and `L=UBU^T`.
Then

```text
p_K(S)=det(I_r-A) det(U_S B U_S^T).
```

If `|S|<=r`, the matrix `U_S B U_S^T` is positive definite, so `p_K(S)>0`.
If `|S|>r`, `rank L<=r`, so `p_K(S)=0`. Hence the exact support is

```text
{ S subset [n] : |S| <= r }.
```

For `n=4,r=3`, nonzero coordinates of the one-dimensional null vector are
equivalent to the nonvanishing of all three-row minors by the cofactor formula.

This appendix does not change the frozen N4 theorem and does not assert any
five-point curvature result.
