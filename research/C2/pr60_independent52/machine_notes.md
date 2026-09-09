# PR60 independent52 machine notes

Status: MACHINE_PASS for the scoped exact arithmetic certificate. This note
records C2 machine evidence only; it does not assert theorem acceptance.

## Source and runs

- Frozen PR60 input source: `f869fd251c0d6fdad737b6d5efa287307795a87d`.
- Frozen main structure input: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.
- Repaired independent checker source frozen by root:
  public `ee33372042d27911a97a14aefc6cb068404d190b`.
- Local Run01 source snapshot: `c05363a0c01e1820dbe1a2743960bc06d86afeff`.
- Local repaired Run02 source snapshot: `4620bf66b130af4948f371bbad1b11c372c08273`.
- Run01: PID 174230, 2026-09-09 15:28:03 UTC to 15:28:32 UTC,
  exit 1 after 28.569 s. It passed the Bernoulli Gram/reflection,
  the 16 Rstar/Rbar normalization identities, and all 16 Ahat polynomial
  entry checks. It then failed on a mechanical Python list indexing typo in
  the permutation determinant cross-check. No mathematical mismatch was
  reached. The repair changed only `mat[row, col]` to `mat[row][col]`.
- Run02: PID 174315, 2026-09-09 15:31:39 UTC to 15:32:32 UTC,
  exit 0 after 52.957 s. Deadline was the shared
  2026-09-09 16:13:03 UTC deadline; no reset was used.
- Runtime: Python 3.12.3, SymPy 1.14.0, Linux x86_64. Thread environment was
  set to one for OMP, OpenBLAS, MKL, NumExpr and VECLIB. The run applied a
  16 GiB address-space cap.

Public outputs are in `research/C2/pr60_independent52/outputs/run02`.
The operator separately retains the raw run artifacts.

## Machine coverage

The checker reconstructed the four-event Bernoulli Gram reduction and verified
the `q_ij dot zeta` reduction, all 16 Gram entries, and the reflection identity
`S Delta^(-1) S = Delta` exactly.

It built `Rstar(u)` from the displayed Gram/Schur ingredients and independently
built `Rbar(t)` from formula (16). All 16 entries of
`Rbar(t=u^4) = u Rstar(u)/4` passed exact rational identity checks. Full
`Rstar` and `Rbar` entries were saved in `Rstar_and_Rbar_entries.json`.

It formed `Ahat = 2 J^2 L^2 C Delta^(-1) Rbar` and verified all 16 entries are
polynomials over `QQ`. Entry summaries were saved in `Ahat_entries.json`.

It computed `det(Ahat)` using an independently implemented fraction-free
Bareiss calculation over the `QQ[mu,nu,r,t]` polynomial ring, then cross-checked
the result by the independent 24-product permutation determinant in the same
polynomial ring. The determinant had 1528 terms and degrees `(4,4,22,19)`.

It extracted a fresh quotient
`P = det(Ahat)/(8 t J^3 L^3 C^3)` by exact polynomial division with zero
remainder. The resulting `P` was stored over `QQ`, and every coefficient was
separately checked to be integral. The extracted `P` has 279 integer terms and
degrees `(4,4,10,6)`. The quotient, determinant expression, coefficient table,
and zero-remainder record are in `determinant_and_P.json`.

Only after the fresh determinant quotient existed, the checker parsed
`inputs/reference_P_components.json`, assembled the six author component
polynomials as in proof section 5, and verified exact equality to the fresh
`P`. It also verified the signflip and leaf-exchange identities for `P`.

For the positive chart, the checker produced `Q` in two independent exact ways:
bounded integer binomial coefficient loops and a termwise homogeneous
polynomial construction. The two constructions agreed. The full
`5 x 5 x 11 x 7` box has 1925 positions: 1731 positive coefficients and
194 zeros. The minimum positive coefficient is 192 and the constant coefficient
is 432. All 25 grouped counts and minima match proof display (20). The complete
box is saved in `Q_full_box.json`.

The checker verified the four displayed seed leading principal minors of
`Rbar` at `mu=nu=r=0, t=1/16`:
`1009/7200`, `743633/6480000`, `1137143/12150000`, and `9016/253125`.
It also verified the matrix leaf-swap congruence for `Rbar` and the determinant
scaling relation back to the stated `Rstar` determinant formula. These records
are in `seed_leafswap_scaling.json`.

## Limits

This is a machine arithmetic certificate for the short Schur matrix to
determinant to fresh `P` to positive-chart `Q` chain. It does not import or
execute `inputs/pr60/certificate.py` or `inputs/pr60/bridge_checks.py`, and it
does not use the older r=0 certificate as an input.

C1 owns the analytical bridge FIRST: the fixed-direction entropy-Hessian
meaning, all-domain coverage, nonvanishing-to-inertia continuation,
integration, and theorem acceptance. This C2 note does not certify novelty,
the Lambda-nonzero problem, PR58, PR59, entropy-rate claims, or any broader
statement outside the frozen PR60 machine scope.
