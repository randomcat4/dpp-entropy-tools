# Fresh nonauthor FIRST review for PR57

Verdict: **CORRECT** within the frozen r=0 scope.

Reviewed candidate public commit:
`ba890f6294272849fa0a20d5c7e0e9f97d171d51`.

Local equivalent reviewed:
`0e339c0a8b7ecfc263418fb64b3608298161e590`.

Reviewer checker frozen by root at public commit
`591c65bdc354e2880c6ccb2506822275b0e45a12`, local equivalent
`10d05f1ef0c9491da40bbe27c338bfd14ac97194`, then run once under the shared
guard.  I did not execute Python, SymPy, or CAS directly.

## Scope

This review covers only the issue52 r=0 contract:

```text
|mu| < 1, |nu| < 1, 0 < u < 1, r=0.
```

The accepted premise is the already-reviewed main Schur reduction from the
six fixed physical direction matrix `M` to the displayed four-by-four
`Rstar` in the frozen STRUCTURE source.  I did not re-audit the old
eight-event derivation or the full six-by-six-to-Schur construction.

This review does not claim anything about general `r`, entropy
counterexamples, novelty, or Lean/formal verification.

## Materials Inspected

- `frozen_contract.md`
- `inputs/SOURCE_BINDING.json`
- `inputs/source/structure/STRUCTURE.md`
- `inputs/source/structure/POSITIVE_SEED.md`
- `inputs/source/resume/R0_CANDIDATE.md`
- `author_proof.md`
- `implementation/verify_r0_chain_independent.py`
- author artifacts under `outputs/author01/`
- reviewer run outputs under `review_first/run01/`

## Executed Coverage

Root ran the reviewer checker:

```text
review_first/check_r0_first.py
```

The guarded run was PID `173840`, started at `2026-09-09T13:48:07Z`, ended at
`2026-09-09T13:48:17Z`, exited `0`, and wrote PASS in
`review_first/run01/RESULT.json`.  Runtime was `9.499` seconds.  `stdout.log`
and `stderr.log` were empty.

The public copied run contains checkpoints before determinant work and before
the Q transform:

- `0004_before_determinant.json`
- `0005_after_determinant.json`
- `0008_before_Q_transform.json`
- `0009_Q_built.json`
- `0012_result_written.json`

## Mathematical Checks

The reviewer checker reconstructed `Rstar` from the displayed r=0
specialization, not from the author checker or saved matrices.  It checked:

- reflection identity `S D^{-1} S = D`;
- r=0 invisible-block mixed coefficient cancellation;
- `d_alpha = u^3 v/J` and `d_beta = u^3 w/J`;
- simplified `ell_alpha`, `ell_beta` rows against the unsimplified coupling
  formulas from STRUCTURE.

All six displayed-formula identities were exactly zero.

For the determinant layer, the checker computed `det Rstar` by an explicit
24-term permutation expansion and checked it against SymPy's Berkowitz
determinant.  It then verified the rational identity

```text
det Rstar = (1-mu^2)^2 (1-nu^2)^2 P / (2(1-u^4)^5).
```

The extracted `P` is a `ZZ` polynomial with degree box `(4,4,16)` and 26
terms.  It matched both the archived `source_factor` and the candidate
`P_polynomial.json` artifact.

For the positive-orthant layer, the checker built

```text
Q = (1+X)^4 (1+Y)^4 (1+U)^16
    P((X-1)/(X+1), (Y-1)/(Y+1), U/(1+U)).
```

It used both direct homogeneous substitution and a separate coefficient-wise
binomial expansion.  The two transforms matched exactly.  The full
`5 x 5 x 17` degree box was checked:

```text
425 total entries, 389 positive nonzero entries, 36 zero entries,
minimum positive coefficient 192, maximum coefficient 99220032.
```

The completed box matched the archived coefficient table, treating omitted
archived entries as zero, and matched the candidate
`Q_polynomial_full_box.json` artifact.

For the seed, the checker evaluated the rebuilt `Rstar` at
`mu=nu=0, u=1/2`, scaled by `14400`, and obtained exactly

```text
[ 16144      0      0   6076 ]
[     0  94336   6016      0 ]
[     0   6016  94336      0 ]
[  6076      0      0  46129 ]
```

The strict diagonal dominance margins were

```text
10068, 88320, 88320, 40053.
```

This gives a positive interior seed for `Rstar`.

## Domain And Lift

The Cayley substitution

```text
mu=(X-1)/(X+1), nu=(Y-1)/(Y+1), u=U/(1+U)
```

is a bijection from `X,Y,U>0` to `|mu|<1, |nu|<1, 0<u<1`, with inverse

```text
X=(1+mu)/(1-mu), Y=(1+nu)/(1-nu), U=u/(1-u).
```

All clearing factors used in the determinant and Cayley transform are
strictly positive on the open domain.  Since every nonzero coefficient of
`Q` is positive and `Q` is not zero, `Q>0` on the positive orthant, hence
`P>0` on the original open domain.  The determinant identity then gives
`det Rstar != 0` throughout the r=0 domain.

The domain `(-1,1) x (-1,1) x (0,1)` is connected.  `Rstar` is real symmetric
and continuous wherever the positive denominator factors above are nonzero.
With one positive seed and no determinant zero anywhere in the connected
domain, no eigenvalue can cross zero, so the inertia remains four positive
eigenvalues throughout the domain.

Using the accepted Schur reduction premise, the eliminated
`alpha,beta` block has positive diagonal entries `d_alpha,d_beta`, and the
coordinate map back to the original six fixed physical directions is
invertible at r=0.  Therefore positivity of `Rstar` lifts to positive
definiteness of the original six-direction `M` assertion for this r=0
subfamily.

## Code Review Notes

The candidate implementation constructs the displayed `Rstar`, computes the
determinant/P/Q chain, and only opens the archived `source_factor` after fresh
P construction and the archived coefficient table after fresh Q construction.
Its import statements do not import the old PR55 checker, old matrix strings,
or archived coefficient data.

The author determinant path uses Bareiss after denominator clearing as an
exact symbolic division certificate, and separately checks against a 24-term
Leibniz determinant.  Neither the author proof nor my review uses Bareiss
pivots as domain-wide nonvanishing assumptions.

## Metadata Notes

The reviewer `RESULT.json` field
`source_scan.author_proof_mentions_scope=false` is not a mathematical or
scope gap.  It came from a brittle substring check in my checker.  The actual
`author_proof.md` begins its frozen statement with `Work only at r=0`, and
the broader `R0_CANDIDATE.md` explicitly says the result is only the r=0
subfamily and makes no full-r or entropy-counterexample claim.

The reviewer `run_manifest.json` records effective `deadline_epoch`
`1788962587`, which is earlier than the supplied shared guard epoch
`1788963457`.  This is because the checker defaulted to an internal
900-second wall cap and took the minimum of the internal cap and the supplied
absolute deadline.  The outer shared deadline remained `1788963457`
(`2026-09-09T14:17:37Z`), and the tighter internal cap was harmless because
the run finished at `2026-09-09T13:48:17Z`.

## Final Verdict

`CORRECT`: the candidate establishes the frozen r=0 chain

```text
displayed Rstar -> det -> P -> Q -> nonvanishing -> inertia -> six-direction M
```

for all `|mu|<1, |nu|<1, 0<u<1`, conditional on the already-accepted main
Schur reduction to the displayed four-by-four `Rstar`.  No SECOND review is
claimed or scheduled here.
