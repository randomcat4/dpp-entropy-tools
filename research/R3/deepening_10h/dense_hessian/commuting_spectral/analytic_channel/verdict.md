# D10-M3 author verdict

STATUS: **ANALYTIC_REDUCTION_COMPLETE_GENERAL_PROOF_INCOMPLETE**

This is an author deliverable and must go to a fresh non-author verifier before
any `CORRECT` label.

## What is proved as a candidate

- The fixed-eigenvector path
  \(K(t)=Q\operatorname{diag}(\lambda_i+tv_i)Q^\top\) has an exact latent
  representation: independent spectral subset \(Z_t\), followed by a fixed
  projection-DPP channel \(T_Q(Y\mid Z)\).
- The output \(H(Y_t)''\) has explicit checkable formulas through latent scores
  \(a_R,b_R\), and also the cardinality split
  \[
  H(Y_t)=H(|Z_t|)+H(Y_t\mid |Y_t|).
  \]
- The count term is controlled by Shepp--Olkin.  Therefore the only possible
  source of a commuting-spectral PSD/NSD flip is the conditional channel entropy
  \(H(Y_t\mid |Y_t|)\), equivalently the combined posterior/channel correction
  \(\mathbb E H(Y_t\mid Z_t)-H(Z_t\mid Y_t)\).
- A nontrivial closed subcase is proved for arbitrary real \(2\times2\) fixed
  spectral blocks with same-sign rates, hence for observation-coordinate direct
  sums of \(1\times1\) and \(2\times2\) such blocks when all spectral rates are
  globally nonnegative or globally nonpositive.
- A further sufficient class is proved when the projection-DPP channel is
  cardinality-uniform and spectral rates have one sign.  Signed-permutation
  \(Q\) is also closed, but is the diagonal/product case.

## What did not close

For generic fixed \(Q\), each cardinality block is only doubly stochastic.  That
does not control the second derivative of
\(H(T_{Q,k}(Z_t\mid |Z_t|=k))\).  This is the precise remaining gap; it is not a
numerical issue and not solved by existing finite scans.

## Sanity run

`channel_sanity.py` compared signed-determinant atoms and spectral-channel
mixture atoms as exact rational polynomials in \(t\).

Command exit code: `0`.

Checked cases:

- `n2_rational_rotation`: 4 atoms, max coefficient difference `0`,
  \(H''(0)\approx -0.08167680994261452\).
- `n3_signed_permutation_control`: 8 atoms, max coefficient difference `0`,
  \(H''(0)\approx -0.04181063814272820\).
- `n3_block_hadamard_plus_coordinate`: 8 atoms, max coefficient difference `0`,
  \(H''(0)\approx -0.03504616956552288\).

Total exact atom polynomials checked: `20`.

## Bottom line

No positive gap or \(\rho>1\) candidate is frozen here.  The deliverable is an
analytic reduction, a checkable Hessian/conditional-entropy certificate target,
and narrow sufficient channel/block subclasses.  General fixed-\(Q\),
heterogeneous positive spectral-rate concavity remains **INCOMPLETE**.
