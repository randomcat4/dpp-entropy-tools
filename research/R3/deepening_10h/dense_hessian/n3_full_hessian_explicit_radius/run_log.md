# D10-S7 bounded run log

Date: 2026-09-08. Author derivation plus exact standard-library sanity. No
randomness, server, GPU, dependency installation, or write outside this task's
directory. Existing S5/S6 materials were read only.

Command from the repository root, using the local bundled Python 3.12:

```
python research/R3/deepening_10h/dense_hessian/n3_full_hessian_explicit_radius/sanity.py
```

Exit code 0; elapsed 0.15561509132385254 seconds. No failed assertions. The
single final computation contains all 12 perturbation points and all 4
directions per point: 48 mixed-jet cases, 384 exact event-jet comparisons,
8 base atoms, and 3 exact distinct characteristic roots. The output retains
every point, direction, mixed jet, norm squared, and rational denominator.
No candidate or failed mathematical check was omitted.

The norm-dependent derivative inequalities are checked exactly after squaring
both nonnegative sides. The mixed derivatives themselves use exact Fraction
arithmetic, including the factor 2 for the u*t^2 coefficient. The 70-digit
Decimal H2/H3 evaluations are sanity only, whereas all constants and radius
comparisons are rational. Proof of continuous-ball coverage is in the draft,
not inferred from the 12 points.

An initial filename search returned no matches (exit 1), and an attempted
read of a nonexistent proof_candidate.md in the scalar-neighborhood directory
returned exit 1. Those were discovery/read misses with no evaluated candidates
or data writes. The actual S6 proof and its audit were then located and read.
The mathematical script ran once successfully.

Script SHA256:
`4d22c13059f3e19d13e83f3c0a46101293629cd13a966b73e9763ef446618941`

Result SHA256:
`e0ef92ca240a6076167d06bfb8ec036f08f2c71cb68d986f95e45a445d1d4ebf`

Read dependency hashes at handoff:

- S5 `n3_full_psd_local/verifications/revision_recheck.md`:
  `2575b183f617d0f36181156123a6646b1572ef7aea3748ebbad2e462a418d60c`.
- S6 `semidefinite_directions/explicit_diagonal_neighborhood/proof_candidate.md`:
  `69b64a93747db8c29f3f87061443ee40a470e5b8a956b21f3592ce4d16845d2e`.

These are dependency/provenance records, not claims that S7 has itself been
independently reviewed. The math-theorem workflow is used to separate verified
inputs, author proof, exact sanity, finite scope and pending certification.
