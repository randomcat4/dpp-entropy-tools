# D10-S4 fresh non-author verification

STATUS: **CORRECT**

Scope audited: `scalar_kernel_psd_neighborhood/frozen_claim.md`,
`proof.md`, `hazards.md`, and `verdict.md`.  I did not modify the author
files and did not use the author sanity script as evidence.  The independent
check below rebuilds exact-event atoms from inclusion probabilities by
Möbius inversion.

## 1. Exact-event semantics and diagonal Hessian

For a DPP marginal kernel \(K\), the exact atom is

\[
p_S(K)=\sum_{A\supseteq S}(-1)^{|A|-|S|}\det K[A,A].
\]

At

\[
K_0=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1,
\]

this gives the heterogeneous product law

\[
p_S(0)=\prod_{i\in S}x_i\prod_{i\notin S}(1-x_i).
\]

For the affine line \(K(t)=K_0+tD\), the first derivative of an inclusion
determinant at a diagonal matrix only sees the diagonal entries of \(D\).  After
Möbius inversion, the atom score is

\[
\frac{p_S'(0)}{p_S(0)}
=
\sum_{i\in S}\frac{D_{ii}}{x_i}
-
\sum_{i\notin S}\frac{D_{ii}}{1-x_i}.
\]

Thus off-diagonal entries can enter \(p_S''(0)\), but not \(p_S'(0)\).

For a smooth positive probability vector,

\[
H''(0)=
-\sum_S\frac{p_S'(0)^2}{p_S(0)}
-\sum_S p_S''(0)\log p_S(0).
\]

The second term vanishes for the exact reason claimed by the author.  Namely

\[
\log p_S(0)
=
\sum_i\log(1-x_i)
+
\sum_{i\in S}\log\frac{x_i}{1-x_i}.
\]

The constant coefficient is killed by total mass:

\[
\sum_S p_S''(0)=0.
\]

Each singleton coefficient is killed by the exact DPP inclusion marginal

\[
\sum_{S\ni i}p_S(t)=\mathbb P(i\in Y)=K_{ii}(t)=x_i+tD_{ii},
\]

so

\[
\sum_{S\ni i}p_S''(0)=0.
\]

Therefore \(\sum_Sp_S''(0)\log p_S(0)=0\).  This is not an atomwise statement:
the independent zero-diagonal off-diagonal example below has nonzero
accelerations \(p_S''(0)\) while the logged sum cancels.

Under the product law \(p(0)\), the score variables for different coordinates
are independent and centered, with variance \(1/[x_i(1-x_i)]\).  Hence

\[
\sum_S\frac{p_S'(0)^2}{p_S(0)}
=
\sum_i\frac{D_{ii}^2}{x_i(1-x_i)},
\]

and consequently

\[
H''_{K_0}[D,D]
=
-\sum_i\frac{D_{ii}^2}{x_i(1-x_i)}.
\]

This proves the formula for arbitrary real symmetric \(D\), locally along
strict feasible affine lines.

## 2. PSD/NSD strictness and Frobenius bound

If \(D\succeq0\) and all diagonal entries vanish, then every \(2\times2\)
principal minor forces \(D_{ij}=0\); hence \(D=0\).  Thus a nonzero PSD
direction has \(\sum_iD_{ii}^2>0\), giving strict \(H''<0\).  The NSD case is
the same after replacing \(D\) by \(-D\).

For \(D\succeq0\),

\[
\|D\|_F^2=\sum_j\lambda_j(D)^2
\le\left(\sum_j\lambda_j(D)\right)^2
=(\operatorname{tr}D)^2
\le n\sum_iD_{ii}^2.
\]

Again NSD follows by sign reversal.  If \(x_i\in[a,b]\subset(0,1)\) and

\[
M=\max_{u\in[a,b]}u(1-u),
\]

then

\[
H''_{K_0}[D,D]
\le
-\frac{\|D\|_F^2}{nM}.
\]

The bound is correctly limited to PSD/NSD directions.  It is false as a
strict bound over all symmetric directions because zero-diagonal indefinite
directions are second-order flat.

## 3. Uniform neighborhood quantifiers

For fixed \(n\) and fixed compact box \([a,b]^n\subset(0,1)^n\), the diagonal
set is a positive distance from the boundary of the strict kernel domain
\(0\prec K\prec I\).  The normalized cone slice

\[
\{D:\|D\|_F=1,\ D\succeq0\ \text{or}\ D\preceq0\}
\]

is compact.  The exact-event entropy Hessian is continuous on strict kernels,
because all exact atoms remain positive on compact subsets of the strict
domain.  Therefore the diagonal-box estimate with

\[
m=\frac1{n\max_{u\in[a,b]}u(1-u)}
\]

extends, after shrinking to a sufficiently small neighborhood inside the
strict kernel domain, to

\[
H''_K[D,D]\le -c
\]

for all normalized PSD/NSD directions, e.g. \(c=m/2\).  Quadratic homogeneity
then gives \(H''_K[D,D]\le-c\|D\|_F^2\) for arbitrary nonzero PSD/NSD
directions.  The claim is existential; no computable radius is asserted.

This matches the frozen claim's quantifiers: the neighborhood is for fixed
\(n,a,b\), relative to the strict DPP kernel domain, and direction
normalization is used only to obtain compactness.

## 4. Independent exact rational checks

I wrote `fresh_scalar_verify.py`, which uses only the Python standard library
and exact `Fraction` arithmetic.  It:

- constructs every inclusion determinant polynomial for
  \(K(t)=\operatorname{diag}(x)+tD\);
- obtains exact atoms by Möbius inversion;
- checks \(p(0)\), \(p'(0)\), \(p''(0)\), mass and singleton derivative
  identities;
- computes the Fisher term exactly;
- checks the PSD/NSD Frobenius bound on cone examples;
- includes a zero-diagonal off-diagonal indefinite case to confirm that
  nonzero \(p_S''(0)\) can occur while the Hessian remains zero.

Command run from the repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\scalar_kernel_psd_neighborhood\verifications\fresh_scalar_verify.py
```

Output summary:

```text
status: PASS
```

Generated JSON: `fresh_scalar_verify.json`.

The four independent heterogeneous rational cases all passed:

| case | dimension | direction type | result |
| --- | ---: | --- | --- |
| `n2_heterogeneous_psd` | 2 | PSD | PASS |
| `n2_zero_diagonal_indefinite_offdiag` | 2 | indefinite | PASS |
| `n3_heterogeneous_spd` | 3 | PSD | PASS |
| `n3_heterogeneous_nsd` | 3 | NSD | PASS |

## 5. Layered verdict

- Diagonal exact-event Hessian formula: **CORRECT**.
- \(p''\log p\) cancellation mechanism: **CORRECT**; it follows from total
  mass and singleton inclusion marginals, not from atomwise vanishing.
- PSD/NSD strict negativity: **CORRECT**.
- PSD/NSD Frobenius lower bound on compact diagonal boxes: **CORRECT**.
- Uniform neighborhood claim: **CORRECT**, with existential radius and fixed
  \(n,a,b\); no global or indefinite-direction concavity is implied.

No critical gap found.
