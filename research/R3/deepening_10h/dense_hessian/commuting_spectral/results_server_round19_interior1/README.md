# D10-H11 / round19_interior1

This batch asks whether the strongest fixed-eigenvector spectral-rate mechanism
seen in H10 disappears once the kernel is kept visibly away from the spectral
boundary. It is a finite diagnostic, not a proof of global concavity.

## Frozen design

- dimension: `n=12`;
- source spectrum: the H10 strongest spectrum contracted toward `1/2` until
  its spectral margin is approximately `0.03`;
- enforced proposal floor: `min(lambda_i,1-lambda_i) >= 0.02`;
- four independent shards, seeds `2026090865` through `2026090868`;
- `5,000` proposals per shard, plus one explicitly ledgered source copy;
- fixed-Q one-sign positive spectral-rate directions, with the same joint
  spectrum/basis refinement semantics as H10.

The copied source hash is
`56e289047bc527697b1511763b8c50809445063ee32ed85d26dd0b8d15719e7d`.
The producing search script hash is
`28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`.

## Author gate result

All `20,000` proposal rows and four source rows are present. No positive gap
was reported. The strongest stored row is shard `0`, index `4853`, labelled
`one_basis_rotation`, with

```text
rho                 = 0.5745947308664667
spectrum margin     = 0.02171078114876157
H'' (80 digit gate) = -47.236908517635153569552257734749333428952577403297...
```

Its frozen NPZ hash is
`4c316f4515bfc1b8c0284e60bb724080f61d523e91d5d9e3299d24f709babebe`.
The exact-decimal-rational endpoint LDL checks certify strict feasibility with
margin `1/2000` throughout `|t|<=1/200`, and certify that the direction is
positive definite. Three high-precision symmetric chords have negative
midpoint gaps.

The H10 strongest value was `0.5746069386526107`. The present visibly interior
best is lower by only about `1.22078e-5`, retaining about `99.9979%` of that
ratio while its actual spectral margin exceeds `0.02`. Thus this batch does
not support the simple explanation that the current high ratio is created only
by approaching a spectral endpoint. It also does not identify a positive
curvature direction: the true threshold remains `rho>1`, and every stored row
is still a finite `SCOUT` miss.

Independent non-author reconstruction under `verifications/` gives `CORRECT`
for the frozen accounting and strongest gate. It rebuilds all 4,096 exact
events at 120 digits, all three chords, and the Fraction LDL certificate
without importing either author module. Full seed regeneration of all 20,000
proposal matrices remains `INCOMPLETE`; the batch therefore remains `SCOUT` at
the global level.
