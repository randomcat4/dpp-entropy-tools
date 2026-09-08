INCOMPLETE

# P4-03 audit: n=3 equicorrelation midpoint

Task audited the frozen candidate

```text
K0 = (a-c) I3 + c 11^T,      0 < K0 < I,
gap = [H(K0-tV)+H(K0+tV)]/2 - H(K0) <= 0
```

for arbitrary real symmetric `V` and strictly feasible endpoints.  I used
only complete event probabilities obtained by Boolean Mobius inversion from
the DPP inclusion probabilities.  Principal minors were not treated as exact
events.

I did not find a strict counterexample, but I also did not obtain an
all-parameter symbolic proof.  Therefore the frozen finite midpoint theorem is
not certified by this audit.

## Inputs read

- `R1/phase4_scope.md`
- `R1/frozen_n3_equicorrelation_v1.md`
- certified `n=2` proof at commit
  `603300c06059518961766c724377c3b9d1198fc5:research/R1/proofs/n2_concavity.md`,
  used only as a tool/reference pattern.

No public proof files were modified.

## Exact event coordinates at the equicorrelation center

Let

```text
x = lambda_1 = a+2c,        y = lambda_2 = a-c,
0 < x < 1,                  0 < y < 1,
a = (x+2y)/3,               c = (x-y)/3.
```

Boolean Mobius inversion gives four orbit probabilities:

```text
p0 = P(000)              = (1-x)(1-y)^2
p1 = each singleton      = (y-1)(3xy-x-2y)/3
p2 = each pair           = -y(3xy-2x-y)/3
p3 = P(111)              = x y^2
```

These are the probabilities used in every Hessian and finite-gap computation.

## S3 Hessian decomposition obtained

The six-dimensional real symmetric direction space decomposes as

```text
Sym_3 = (trivial copy)^2  ⊕  (standard copy)^2.
```

I used the following basis:

```text
Td = I3
To = J3-I3
Sd = diag(1,-1,0)
So = offdiag copy from z=(1,-1,0), with So_ij=z_i+z_j
     so e12=0, e13=1, e23=-1.
```

The symbolic replay in `logs/symbolic_s3_identities.json` verifies exactly:

```text
H''(Td,Sd)=H''(Td,So)=H''(To,Sd)=H''(To,So)=0.
```

Thus the center Hessian reduces to two explicit `2 x 2` blocks:

```text
B_T on span{Td,To},     B_S on span{Sd,So}.
```

The log also records the first and second derivatives of every exact event
probability for `Td,To,Sd,So`, plus the polarized second derivatives needed to
reconstruct the two blocks by

```text
(B_R)ij =
  - sum_S p'_S(Bi) p'_S(Bj) / p_S
  - sum_S log(p_S) p''_S(Bi,Bj).
```

This is the most compact certificate-shaped form I reached.  The fully
expanded entries exist but are much less reviewable.

## Finite probes

All probes were bounded, single-process, and run with BLAS/thread environment
variables capped at 2.  No dependency was installed and no GPU was used.

Machine-readable logs:

- `logs/symbolic_s3_identities.json`
- `logs/probe_small.json`
- `logs/probe_hessian_medium.json`
- `logs/chord_probe_small.json`
- `logs/chord_probe_medium.json`
- `logs/opt_hessian.json`
- `logs/opt_gap.json`
- `logs/opt_gap_minfrac.json`
- `logs/run_summary.json`

Summary:

| Probe | Work | Positive candidate |
| --- | ---: | ---: |
| Hessian grid/random small | 2441 centers | 0 |
| Hessian grid/random medium | 14601 centers | 0 |
| Random finite chords small | 10000 chords | 0 |
| Random finite chords medium | 30000 chords | 0 |
| Hessian differential-evolution probe | max `~2.3e-14` at `c≈0` | numerical zero only |
| finite-gap differential-evolution probe | best `~3.3e-15` with tiny `t` | numerical noise only |
| finite-gap probe with fraction ≥ 0.05 | best `~-9.0e-17` | none |

The largest apparent positive values occurred only at `c=0` or near spectral
boundary/tiny-`t` regimes and remained at floating roundoff scale.  They were
not treated as counterexamples.

## Why this is not a proof

Two gaps remain.

First, for the local Hessian at the equicorrelation center, the symbolic
burden has been reduced but not discharged.  One still needs to prove, for all
`0<x,y<1`, that both explicit blocks are negative semidefinite:

```text
B_T(x,y) <= 0,       B_S(x,y) <= 0.
```

Equivalently, for each block, prove the two diagonal signs and determinant
condition after substituting the Mobius probabilities above and the derivative
tables in `symbolic_s3_identities.json`.

Second, the frozen theorem is a finite midpoint statement.  Even a complete
proof of `H''(K0)[V,V] <= 0` at the symmetric center would only certify the
infinitesimal version.  A finite chord proof still needs either:

```text
gap = 1/2 ∫_{-t}^{t} (t-|s|) H''(K0+sV)[V,V] ds <= 0
```

by a valid line argument, or a direct finite-event inequality.  The sampled
finite chords did not find a violation, but finite scans are not a proof.

The `c=0` branch is especially degenerate: the Hessian has null directions for
pure off-diagonal perturbations at a diagonal center.  This is not a numerical
counterexample, but it does require a separate finite/higher-order argument or
a permitted invocation of an already certified block-diagonal result.

## Reproduction

Run from `R1/certificate/phase4` with the bundled Python used in this
workspace:

```text
python scripts/symbolic_s3_identities.py > logs/symbolic_s3_identities.json
python scripts/equicorr_hessian_probe.py --samples 2000 --grid 21 --seed 20260908 --stop-on-positive --out logs/probe_small.json
python scripts/equicorr_hessian_probe.py --samples 12000 --grid 51 --seed 2026090802 --out logs/probe_hessian_medium.json
python scripts/equicorr_chord_probe.py --trials 10000 --seed 2026090801 --stop-on-positive --out logs/chord_probe_small.json
python scripts/equicorr_chord_probe.py --trials 30000 --seed 2026090803 --out logs/chord_probe_medium.json
python scripts/equicorr_optimize_probe.py --mode hessian --seed 4403 --maxiter 60 --popsize 8 --local-iter 300 --out logs/opt_hessian.json
python scripts/equicorr_optimize_probe.py --mode gap --seed 4404 --maxiter 80 --popsize 8 --local-iter 500 --out logs/opt_gap.json
python scripts/equicorr_optimize_probe.py --mode gap --seed 4405 --maxiter 120 --popsize 8 --local-iter 500 --min-fraction 0.05 --eps 1e-5 --out logs/opt_gap_minfrac.json
```

All recorded runs exited with code `0`.
