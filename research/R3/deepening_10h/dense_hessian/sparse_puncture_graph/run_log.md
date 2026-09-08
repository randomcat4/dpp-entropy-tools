# U4 bounded run and scope ledger

Date: 2026-09-08. One author analytic unit, no subagents, no server/GPU,
no installations or random search. Only this assigned directory was written.

The standard-library script independently builds multivariate inclusion
determinants and Mobius atoms; it imports no U2/U3 implementation. It also
compares each atom polynomial with the signed shifted-determinant formula.
Mass and singleton polynomial identities justify cancelling entropy's linear
likelihood term. Entropy coefficients through degree six/eight are rational.

Run from the repository root with local bundled Python 3.12:

```
python research/R3/deepening_10h/dense_hessian/sparse_puncture_graph/sanity.py
```

Exit 0; elapsed 0.05308723449707031 seconds; no failed checks or omitted cases.
No seed was used: all parameters are explicit deterministic fractions.

Full finite denominator:

- General sixth-jet centers: n=2,3,4, with 4+8+16=28 atom polynomials. Every
  monomial through degree six is checked, including all zero fifth coefficients.
- n=3 single-edge-plus-isolated check: 8 atom polynomials, exact zero first
  cross-component derivative and exact constancy of all block event marginals.
- n=4 P4, endpoint-missing-edge probe: 16 atom polynomials, entropy through
  total degree eight in epsilon and the missing-edge variable.
- Total atom polynomials: 52. No numerical optimization or exhaustive graph
  enumeration was performed.

The n=3 path uses x=(1/5,2/5,4/5), A12=2/5, A23=-3/7. Its two supported
epsilon^2 curvature coefficients are -25 and -5625/196. Its missing-edge
epsilon^4 coefficient is -5625/196. The general theorem uses arbitrary strict
x and nonzero path weights; these fractions are sanity examples only.

The n=4 P4 probe uses x=(1/5,1/3,3/5,3/4) and successive path weights
(1/3,-2/5,3/7). The computed missing-edge Hessian has no epsilon^0 through
epsilon^5 term and coefficient -600/49 at epsilon^6. This is one exact local
jet, explicitly not evidence that the entire P4 Hessian or every connected
support has been classified.

The JSON saves all parameters, exact atom polynomials and entropy coefficients
with complete denominators. The script/result hashes can be checked directly;
the script additionally records its own SHA256 in the JSON. Analytic claims
remain pending non-author review, and all finite evidence remains SCOUT.

Script SHA256:
`aad8c8f061ebdfa8793515aa993ed0cd4b61c8fccf34b384ff706d1d61e4a07c`

Result SHA256:
`161d4cfe0b67102effb589c64a7dddcef06355cbc783df10d584185b7aef0acc`
