# Diagonal-kernel real Hessian exclusion

Status: candidate proof. A pre-commit independent review found no critical
gap; final status is tied to a frozen Git commit and commit-bound review.

Let

```text
K = diag(p_1,...,p_n),        0 < p_i < 1,
```

and let V be any real symmetric matrix. For the full-event DPP entropy

```text
H(K) = - sum_S p_K(S) log p_K(S),
```

with exact event probabilities computed by Mobius inversion, the second
directional derivative at K is

```text
D^2 H(K)[V,V] = - sum_i V_ii^2 / (p_i (1-p_i)) <= 0.
```

In particular no strictly positive Hessian counterexample can have a diagonal
center K. All off-diagonal real-symmetric directions are flat to second order
at a diagonal center.

## Proof

At a diagonal K the DPP is the independent Bernoulli product measure

```text
p_K(S) = prod_{i in S} p_i prod_{i notin S} (1-p_i).
```

Write `a_i(S)=1_{i in S}/p_i - 1_{i notin S}/(1-p_i)`. The first event
derivative is

```text
p'_S = p_K(S) sum_i V_ii a_i(S),
```

because first derivatives of principal minors of a diagonal matrix only see
diagonal entries.

The Fisher part of the entropy Hessian is therefore

```text
- sum_S (p'_S)^2/p_S
= - E[(sum_i V_ii a_i(X))^2]
= - sum_i V_ii^2 / (p_i(1-p_i)).
```

The cross terms vanish by independence and `E[a_i(X)]=0`.

It remains to check the acceleration term

```text
- sum_S p''_S (log p_S + 1).
```

The total mass identity gives `sum_S p''_S=0`, so the constant `1` drops. The
diagonal-diagonal part of `p''_S` is exactly the second derivative of the
independent Bernoulli product under the diagonal perturbation
`p_i -> p_i + t V_ii`; its contribution to `-sum p''_S log p_S` is zero
because each one-coordinate score has mean zero and there is no second
coordinate acceleration.

For an off-diagonal pair i<j, determinant differentiation at a diagonal matrix
has only the transposition contribution. After summing by Mobius inversion, the
coefficient of `V_ij^2` in `p''_S` is:

```text
-2 p_S/(p_i p_j)                         if i,j in S,
 2 p_S/(p_i(1-p_j))                      if i in S, j notin S,
 2 p_S/((1-p_i)p_j)                      if i notin S, j in S,
-2 p_S/((1-p_i)(1-p_j))                  if i,j notin S.
```

Equivalently, after factoring out the other coordinates, the pair
probabilities

```text
p_i p_j,  p_i(1-p_j),  (1-p_i)p_j,  (1-p_i)(1-p_j)
```

receive second derivatives

```text
-2V_ij^2,  +2V_ij^2,  +2V_ij^2,  -2V_ij^2.
```

Their log contribution is

```text
2V_ij^2 [ log(p_i p_j)
        - log(p_i(1-p_j))
        - log((1-p_i)p_j)
        + log((1-p_i)(1-p_j)) ] = 0.
```

All factors from the other coordinates cancel because their total signed
second-derivative coefficient for this pair is zero. Therefore the whole
acceleration term vanishes, and only the negative Fisher diagonal expression
above remains.

This proof uses exact event probabilities. Principal minors enter only through
the Mobius-inversion derivative calculation.
