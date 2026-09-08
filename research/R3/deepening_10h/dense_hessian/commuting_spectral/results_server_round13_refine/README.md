# Round 13 joint spectrum/eigenbasis refinement

STATUS: `CORRECT` for the frozen-point arithmetic and ledger accounting,
`SCOUT` for the 20,000-proposal search, and `INCOMPLETE` for any continuous
or global concavity claim.  A fresh non-author audit is preserved under
`verifications/`.

## Scope

Starting from the verified round-9 fixed-basis point, four one-thread shards
evaluated 5,000 new centers each.  Every evaluated center still defines a
fixed-eigenbasis affine path; the outer search additionally makes small Givens
rotations of that fixed basis between centers and perturbs the center spectrum.
The positive spectral-rate direction is optimized separately at each center.

This is a float64 candidate search over 20,000 proposals, not a proof over the
continuous center space.

## Result

- new proposals: `20000`
- proposal rows with `FLOAT_CANDIDATE`: `0`
- proposal rows with positive stored midpoint gap: `0`
- maximum stored midpoint gap: about `-5.59e-5`
- best mechanism ratio: `rho=0.5685905197415816`
- strongest row: shard 3, index 4901, `one_basis_rotation`
- float gap at its stored step: `-0.00021369102076107538`

This moves the stable diagnostic record from about `0.5464` to about `0.5686`.
The counterexample threshold remains `rho>1`.

## Frozen strongest-point gate

At 70 decimal digits, the author-side mixed-event elimination gives

```text
Fisher       = 79.6727219320964920030753599425615499640644453282944...
acceleration = 45.3011543725972850033524711906070027766320175634107...
H''          = -34.3715675594992069997228887519545471874324277648836...
rho          = 0.5685905197415820173383874487113270724394593826596...
```

The actual 70-digit midpoint gaps are negative:

```text
t=0.0035259410255616148  gap=-2.13691020763065201751223339764e-4
t=0.001                  gap=-1.71859964312633581212226084079e-5
t=0.0001                 gap=-1.71857859061591123187382012394e-7
```

Exact rational LDL proves that the decimal-rationalized direction is positive
definite and that both `K(t)` and `I-K(t)` retain margin `1/2000` throughout
`|t|<=1/200`.  As in round 9, decimal-rationalizing the symmetrized float
matrices does not preserve an exact zero commutator; the exact certificate is
for a near-commuting PSD K-affine line, while the producing float construction
uses a common numerical eigenbasis.

A fresh non-author implementation did not import the author gate and repeated
the strongest-point calculation at 90 decimal digits.  It obtained the same
displayed `H''` and `rho`, the same three negative chords, and an independent
Fraction LDL certificate.  It also counted all four ledgers directly: 20,000
proposal rows, zero `FLOAT_CANDIDATE` rows, zero positive gaps, and maximum gap
`-5.5879650249224255e-05`.  The audit measured the rationalized commutator at
about `3.54e-16`; this is another reason the exact certificate is described as
near-commuting rather than exactly commuting.

## Bookkeeping defect caught before interpretation

The exact producing script is retained as `spectral_basis_refine_run_version.py`
with SHA-256
`88c610074973f10c683f9d927be6ed077cc6319f11bcf8a954829df26c90f592`.
Its initial source/base point participated in the best comparison but was not
written to the proposal ledger or included in `positive_count`.  The source is
the already verified negative round-9 point (`rho≈0.5464`), so this omission
does not change the current zero-hit result: all 20,000 new proposals are in
the four CSV files, every proposal status is `NO_HIT`, every proposal gap is
negative, and each saved best NPZ was checked separately.

The current `spectral_basis_refine.py` fixes this for future runs by:

- writing the source/base as ledger row `index=-1`;
- including its status in `positive_count`;
- freezing source and proposal candidates independently of whether they set a
  new rho record;
- separating `proposal_count` from `ledger_rows_including_source`.

The initial non-author `INCORRECT` preflight and both fix reviews are preserved
under `../refine_verifications/`.  The remaining optimizer is heuristic on the
positive cone, so all no-hit counts remain `SCOUT`.

## Integrity and boundary

- source NPZ SHA-256:
  `807ac23ae9b0c54c39d909ca543b72f69d95a9cc986cb7d4ff8295444d73cc01`
- strongest NPZ SHA-256:
  `4bda0a82ca642b5e804bca498107a89a1c81a3a7eb79ce6aca2712e4d594cb72`

All copied NPZ, manifest and log hashes matched the producing machine before
its temporary directory was removed.  The author and fresh non-author
high-precision gates certify only the frozen strongest point; the 20,000-row
outer search remains finite scout evidence and does not establish generic
commuting or PSD/NSD concavity.
