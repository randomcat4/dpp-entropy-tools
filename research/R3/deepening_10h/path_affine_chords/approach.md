# D10-B / FT-B：path-affine chords approach

Status: `DEEP` for the FT-B closure object.  No R3 entropy counterexample is
claimed.

## Scope read before acting

This work unit read the required local context:

- `repo/AGENTS.md`
- `research/R3/deepening_10h/problem.md`
- `research/R3/deepening_10h/assumptions.md`
- `research/R3/deepening_10h/frozen_theorem_v1.md`
- `research/R3/deepening_10h/hazards.md`
- `research/R3/deepening_10h/lemma_ledger.md`
- NS-1 sparse Schur route note, implementation, evidence, validation, and
  verdict.

No literature search was run.  The Gu prior-art notice supplied by the parent
task is recorded as a blocker below, not reproved.

## Frozen target being addressed

FT-B asks whether there exist three non-all-identical, connected,
heterogeneous, real symmetric positive definite tridiagonal matrices
`L_-, L_0, L_+` such that

```text
Phi(L_0) = (Phi(L_-) + Phi(L_+))/2,
Phi(L) = L(I+L)^(-1).
```

The midpoint is in marginal-kernel `K` space.  A straight line in `L` space
does not solve the frozen problem.

## Exact change of variables

For positive definite `L`, set

```text
P = I+L,
S = P^(-1) = (I+L)^(-1).
```

Then

```text
Phi(L) = L(I+L)^(-1)
       = (P-I)P^(-1)
       = I-S.
```

Therefore the required K-space midpoint condition is exactly equivalent to

```text
S_0 = (S_- + S_+)/2.
```

This is the core algebraic move: make `S` affine while keeping `S^(-1)-I`
tridiagonal.

## Fixed-beta innovation family

Fix nonzero rational parameters

```text
beta_1, ..., beta_{n-1}.
```

Let `R` be the unit lower-bidiagonal matrix

```text
R_ii = 1,
R_{i+1,i} = -beta_i,
all other off-band entries = 0.
```

For positive rational innovation variances `tau=(tau_1,...,tau_n)`, define

```text
S(tau) = R^(-1) diag(tau) R^(-T).
```

Then `S(tau)` is symmetric positive definite and affine in `tau`.  Its inverse
is

```text
P(tau) = S(tau)^(-1) = R^T diag(1/tau) R,
```

so `P(tau)` is symmetric tridiagonal.  Define

```text
L(tau) = P(tau)-I.
```

The tridiagonal entries are explicitly

```text
P_ii = 1/tau_i + beta_i^2/tau_{i+1}       for i<n,
P_nn = 1/tau_n,
P_{i,i+1} = -beta_i/tau_{i+1}.
```

Thus every adjacent edge of `L(tau)` is nonzero when every `beta_i` is
nonzero.  The diagonal is heterogeneous for generic rational choices; in the
deposited examples it is checked exactly.

If `tau_0=(tau_-+tau_+)/2`, then

```text
S(tau_0) = (S(tau_-) + S(tau_+))/2
```

by linearity.  Consequently

```text
Phi(L(tau_0))
= I-S(tau_0)
= (I-S(tau_-)+I-S(tau_+))/2
= (Phi(L(tau_-))+Phi(L(tau_+)))/2.
```

This is an exact K-space affine chord.  It is not an `L`-space line in the
examples: `L(tau_0) != (L(tau_-)+L(tau_+))/2`.

Positive definiteness of `L(tau)` is not assumed from floating point.  The
script certifies it by exact leading continuants, i.e. Sylvester's criterion
for the symmetric tridiagonal matrix.  Once `L>0`, `K=Phi(L)` is automatically
a strict real positive contraction because eigenvalues map as
`lambda -> lambda/(1+lambda)`.

## Explicit n=3 certificate

The script freezes the following rational data:

```text
beta = (1/3, -2/5)
tau_- = (1/40, 1/45, 1/50)
tau_0 = (19/880, 8/315, 11/600)
tau_+ = (1/55, 1/35, 1/60)
```

It constructs `L_*=S(tau_*)^(-1)-I`.  The resulting matrices are tridiagonal,
connected, have heterogeneous diagonals, and pass exact positive-definiteness
checks.

The exact perturbation rank is

```text
rank(K_+ - K_-) = 3.
```

So this is not a rank-one direction.

## Explicit n=4 certificate

The script also freezes:

```text
beta = (1/4, -1/3, 2/7)
tau_- = (1/30, 1/36, 1/42, 1/48)
tau_0 = (1/36, 23/792, 97/4620, 29/1248)
tau_+ = (1/45, 1/33, 1/55, 1/39)
```

Again, all FT-B shape and definiteness conditions pass exactly.  The exact
perturbation rank is

```text
rank(K_+ - K_-) = 4.
```

## Direct Möbius validation

For each of the six matrices in the n=3 and n=4 triples, the implementation
uses the existing NS-1 `path_schur.py` validator:

```text
p_K(S) from direct Möbius inversion of inclusion probabilities det K_A
```

is compared with

```text
det(L_S)/det(I+L)
```

and with the path-run factorization used by the Schur entropy dynamic program.
All comparisons are exact rational equalities.

Summary from `evidence.json`:

```text
n=3: 3 points, 8 atoms each, mismatch_count=0
n=4: 3 points, 16 atoms each, mismatch_count=0
```

This is deliberately tiny direct enumeration.  It validates event semantics
and the implementation path; it is not used as a theorem about all kernels.

## Entropy and gap convention

After the FT-B triples were found, the NS-1 path recursion was used to compute
three-point entropies.  The reported gap is

```text
Delta = (H(K_-)+H(K_+))/2 - H(K_0).
```

The Decimal scout values are:

```text
n=3: Delta = -0.00045556980402948637966202904966273876636359662215010218795433969502053929872088544141161521326441
n=4: Delta = -0.00084150938797292809775272697635216508407540691808349059968484019798488667772598963986582249100154
```

Both are negative, so neither triple is an R3 nonconcavity candidate.  No
outward-rounded interval sign certificate was attempted because there is no
positive scout gap to certify.

## Complexity

For the algebraic chord certificate:

```text
build tridiagonal L from beta,tau: O(n)
exact midpoint identity by construction: O(n^2) if matrices are materialized
exact rank or dense inverse cross-check in the script: O(n^3)
```

For entropy, the reused NS-1 path recursion costs:

```text
interval determinants: O(n^2) arithmetic
entropy dynamic program: O(n^2) arithmetic
memory in prototype: O(n^2)
```

For the direct Möbius comparison, this D10-B run uses only n=3 and n=4.  The
validator enumerates all atoms and is intentionally not the scalable route.

## Numerical and proof boundaries

- All midpoint identities, tridiagonal shape checks, ranks, leading-minor
  certificates, and direct atom comparisons are exact rational operations.
- Decimal logarithms are diagnostic only.
- No strict positive entropy gap is claimed.
- The construction gives exact path-sparse `L` triples with K-space affine
  midpoint closure.  It does not imply entropy nonconcavity.
- The supplied Gu blocker is respected: Gu's Theorem 7 / Corollary 6, as
  reported by the parent task, excludes rank-one K directions and chords from
  the origin as positive-gap routes.  The deposited perturbations have full
  rank in n=3 and n=4 and are not origin chords.

## Attempt denominator

```text
1. Fixed-beta innovation family: succeeds for FT-B closure in n=3 and n=4.
2. Exhaustive search/nonexistence: not run, no need after explicit examples.
3. Positive-gap certification: not attempted because the computed scout gaps
   are negative.
```
