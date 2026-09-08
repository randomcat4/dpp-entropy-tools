# Reproducibility, scope, and failure denominator

Date: 2026-09-08. Standard-library Python, no randomness (seed null), no server,
no GPU, no installations. Six deterministic centers in one rational spectral
frame; no general search. All parameters, denominators, K/D/P, event cubics,
coefficient certificates and attempted interval bounds are retained in JSON.

Run from the repository root:

```
python research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_complement_barrier_refine/sanity.py
```

The actual interpreter was the local bundled Python 3.12 runtime. Final run:
exit 0, 0.0571675300598145 seconds. No failed assertions.

Frozen script SHA256:
`f713bce00dee34698737829406a95194f184d07292dcd6c24f3554aff0870a55`

Frozen result SHA256:
`4b5e411103f316776816e2b53223dea433a68e87b0e442e2b19d428a2020f8c1`

Six centers give 48 exact event polynomials, 192 exact scalar coefficients,
each compared to inclusion-Mobius inversion. The combined acceleration
identity is also checked at 80-digit Decimal precision with discrepancy below
1e-65. Three coefficients at each center have exact rational sign certificates
after clearing exponent denominators, plus rational logarithm enclosures.

Results: 0/6 in the old rectangle; 1/6 in the new one-fifth region; 5/6 pass
the product criterion; 6/6 pass the exact positive-coefficient test. These
fractions describe only the six chosen cases, not coverage percentages.

For each center the product condition is attempted on steps 1/100 and 1/1000,
using three degree-six coefficient bounds. There are 12 interval attempts:
10 pass and 2 fail. Both failures are at index 4, which already fails the
product condition at its center. The exact failed coefficient bounds remain
in the JSON. They are not positive-curvature examples or numerical errors.

The first five centers were tried together and retained. The sixth was then
chosen explicitly to illustrate the simpler one-fifth region; it did not
replace or conceal a rejected case. The final JSON extends the initial
five-center run. Initial five-center result: product 4/5, coefficient 5/5,
one-fifth 0/5, old 0/5, exit 0. A later run added exponent-clearing certificates
and the sixth center, exit 0; the final rerun only corrected the docstring.

Before the script existed, one shell-inline inspection command failed with a
Python SyntaxError caused by nested shell quoting (exit 1, zero evaluated
centers). It produced no mathematical data. The durable script avoided this
failure and all subsequent computation ran successfully. This is a tooling
failure, not a rejected mathematical candidate.

External dependency: the full count-entropy concavity theorem was re-opened
at https://arxiv.org/pdf/1503.01570 . A small targeted web query concerning
three-dimensional DPP complement entropy did not establish an identical prior
result; novelty remains unconfirmed. No unrelated search result is used as a
mathematical premise.

Role: M8 author derivation and self-sanity only. Independent certification is
delegated to another context. The math-theorem workflow was used to keep the
global target, sufficient subclass, finite probes and review status separate.
