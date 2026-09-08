# D10-M3 exact sanity report

Script: `channel_sanity.py`

Run from
`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research/R3/deepening_10h/dense_hessian/commuting_spectral/analytic_channel/channel_sanity.py
```

Exit code: `0`.  Decimal precision for displayed logarithmic \(H''\): `80`.
The exact atom-polynomial comparisons are rational `Fraction` checks.

## What was checked

For each small case, the script compared every exact atom polynomial in \(t\)
computed in two independent ways:

1. signed determinant atoms
   \[
   p_t(S)=(-1)^{n-|S|}\det(K(t)-Q_S);
   \]
2. spectral-channel mixture atoms
   \[
   p_t(S)=\sum_R T_Q(S\mid R)\mu_t(R).
   \]

The polynomial coefficients agreed exactly in all cases.

## Cases

| case | n | atoms | max coefficient difference | min atom at t=0 | sum p | sum p' | sum p'' | H'' at t=0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| n2_rational_rotation | 2 | 4 | 0 | 10/77 | 1 | 0 | 0 | -0.08167680994261452 |
| n3_signed_permutation_control | 3 | 8 | 0 | 1/35 | 1 | 0 | 0 | -0.04181063814272820 |
| n3_block_hadamard_plus_coordinate | 3 | 8 | 0 | 2/35 | 1 | 0 | 0 | -0.03504616956552288 |

Total atom polynomials checked: `20`.

The `n2_rational_rotation` case is a genuinely non-permutation rational
orthogonal basis.  The `n3_block_hadamard_plus_coordinate` case is also
non-permutation; although the eigenvectors use \(1/\sqrt2\), the kernel,
direction, and squared-minor channel probabilities are rational.

These two non-permutation checks directly exercise the \(2\times2\) block
proof and its block-sum extension.

These checks validate the channel identity and derivative bookkeeping on small
instances.  They do not prove the general fixed-\(Q\) concavity problem.
