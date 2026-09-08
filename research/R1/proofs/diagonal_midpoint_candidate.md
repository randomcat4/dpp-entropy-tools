Verification state: VERIFIED for `frozen_diagonal_midpoint_v1.md` as committed
at `a49051d2f768ec2b926a2e4d68d5286b054f9656`; see
`verification/diagonal_midpoint_commit_review.md`.

PRE-FREEZE PROMPT STATUS: DISPROVED

## Formal statement as written

The statement is false if `t=0` is allowed. For example, take `n=1`,
`D=[1/2]`, and any nonzero real symmetric `V=[1]`. Then
`D-tV=D+tV=D` are both strictly positive contractions when `t=0`, but

```text
(H(D-tV)+H(D+tV))/2 - H(D) = 0,
```

not a strict negative number.

Minimal missing hypothesis: require `tV != 0`; under the stated `V != 0`,
this is equivalently `t != 0`. Because the two endpoints are symmetric in
the sign of `t`, one may assume `t>0`.

The intended `t>0` statement is proved below.

## Frozen D1 statement and candidate proof

Let `D=diag(d_1,...,d_n)` with `0<d_i<1`. Let `V` be a nonzero real
symmetric matrix and let `t>0`. Assume

```text
K_- = D - tV,    K_+ = D + tV
```

are both strictly positive contractions, meaning all eigenvalues of each
kernel lie in `(0,1)`. Let `H(K)` denote the Shannon entropy of the full DPP
event distribution on subsets of `[n]`, with event probabilities computed
from inclusion probabilities by

```text
P_K(X=S) = sum_{B subset S^c} (-1)^|B| det K_{S union B}.
```

Then

```text
(H(K_-)+H(K_+))/2 - H(D) < 0.
```

## Proof of repaired statement

Let `X=(X_1,...,X_n)` be the indicator vector of the DPP sample. For any DPP
kernel `K`, the one-point inclusion probabilities give

```text
P_K(X_i=1) = K_ii.
```

This use of `K_ii` is only for the marginal bit `X_i`, not for the full event
probability of an arbitrary subset.

By Shannon subadditivity,

```text
H(X_1,...,X_n) <= sum_i H(X_i) = sum_i h(K_ii),
```

where `h(x)=-x log x-(1-x)log(1-x)`. Equality holds if and only if the bits
`X_1,...,X_n` are mutually independent. This follows from the chain rule

```text
H(X_1,...,X_n) = sum_i H(X_i | X_1,...,X_{i-1})
```

and the equality condition in conditioning-reduces-entropy.

For diagonal `D`, inclusion probabilities factor:

```text
P_D(A subset X) = det D_A = product_{i in A} d_i.
```

Applying the required inclusion-exclusion formula gives

```text
P_D(X=S)
 = sum_{B subset S^c} (-1)^|B| product_{i in S union B} d_i
 = product_{i in S} d_i product_{j notin S} (1-d_j).
```

Thus the DPP with kernel `D` is the independent Bernoulli product law, and

```text
H(D) = sum_i h(d_i).
```

Write `v_i=V_ii`. For the two endpoints,

```text
H(K_-) <= sum_i h(d_i - t v_i),
H(K_+) <= sum_i h(d_i + t v_i).
```

Because `K_-` and `K_+` are strict contractions, all numbers
`d_i +/- t v_i` lie in `(0,1)`. Since `h` is strictly concave on `(0,1)`,

```text
(h(d_i - t v_i)+h(d_i + t v_i))/2 <= h(d_i),
```

with equality if and only if `t v_i=0`.

Summing over `i` gives

```text
(H(K_-)+H(K_+))/2
 <= (1/2) sum_i [h(d_i - t v_i)+h(d_i + t v_i)]
 <= sum_i h(d_i)
 = H(D).
```

It remains only to check strictness.

If some diagonal entry `v_i` is nonzero, then `t v_i != 0`, so strict
concavity of `h` makes the second inequality strict. Hence the desired
midpoint gap is strictly negative.

Now suppose all diagonal entries of `V` are zero. Since `V != 0`, there are
indices `i<j` with `V_ij != 0`. The endpoint kernels have the same one-point
marginals as `D`, but their two-point inclusion probability is

```text
P_{K_+}(X_i=1, X_j=1)
 = det [[d_i, t V_ij], [t V_ij, d_j]]
 = d_i d_j - t^2 V_ij^2
 < d_i d_j,
```

and the same strict inequality holds for `K_-` because the off-diagonal entry
is `-t V_ij` and the square is unchanged.

If the bits were independent under either endpoint, the same two-point
probability would have to equal

```text
P(X_i=1) P(X_j=1) = d_i d_j.
```

The displayed DPP two-point inclusion probability contradicts this. Hence
both endpoint DPP laws are non-independent. By the equality condition in
Shannon subadditivity,

```text
H(K_-) < sum_i h(d_i) = H(D),
H(K_+) < sum_i h(d_i) = H(D).
```

Therefore their average is also strictly below `H(D)`.

Combining the diagonal and pure off-diagonal cases proves the repaired
statement for every nonzero real symmetric `V` with `t>0` and strict endpoint
feasibility.

## Equality conditions

For the weak inequality

```text
(H(D-tV)+H(D+tV))/2 <= H(D),
```

equality can occur only if:

1. `t V_ii = 0` for every `i`, by strict concavity of each Bernoulli entropy;
2. both endpoint DPP laws are independent, by equality in Shannon
   subadditivity.

For a DPP, endpoint independence with the given marginals forces every
off-diagonal endpoint entry to vanish: if `(K_\pm)_ij` were nonzero, then

```text
P(X_i=X_j=1) = K_ii K_jj - (K_ij)^2 < K_ii K_jj.
```

Thus equality is equivalent to `tV=0`. Under the repaired hypothesis `t>0`,
this means `V=0`, which is excluded. Under the formal original wording, `t=0`
gives equality even when `V` is nonzero, which is the counterexample above.

## Scope and dependencies

The proof uses only:

- the finite DPP inclusion definition for one-point and two-point inclusion
  probabilities;
- the required inclusion-exclusion formula to identify the full diagonal
  event law;
- Shannon subadditivity and its equality condition;
- strict concavity of binary entropy on `(0,1)`.

No main-instance proof draft was read or used.
