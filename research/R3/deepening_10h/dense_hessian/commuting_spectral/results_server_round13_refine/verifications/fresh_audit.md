# D10-H5 fresh audit: `results_server_round13_refine`

Layered status:

- round13 artifact bookkeeping and strongest-point gate: **CORRECT**;
- 20,000-proposal search interpretation: **SCOUT**;
- any continuous/global concavity conclusion: **INCOMPLETE**.

This audit is non-author.  I did not import the author `recheck_best_refine.py`
gate or its round-9 helper; the verification script here recomputes the ledger,
best NPZ consistency, exact-event Hessian, Decimal chords, Fraction LDL
feasibility, and rationalized commutator independently.

## Scope

Read within `results_server_round13_refine/`:

- four `candidate_ledger.csv` files;
- four `manifest.json` files;
- four `best_case.npz` files;
- four `best_case.json` files;
- four `run_*.log` files;
- `source.npz`;
- `spectral_basis_refine_run_version.py`;
- `README.md`;
- `recheck_best_refine.py`;
- `recheck_best_refine.json`.

Also read current corrected:

- `research/R3/deepening_10h/dense_hessian/commuting_spectral/spectral_basis_refine.py`.

New files written only under `results_server_round13_refine/verifications/`:

- `fresh_round13_verify.py`;
- `fresh_round13_verify.json`;
- `fresh_audit.md`.

No author file or main README was modified.

## 1. Proposal denominator and zero-hit status

The four shards are complete:

| shard | seed | rows | log max completed | manifest centers | best rho |
|---:|---:|---:|---:|---:|---:|
| 0 | 2026090840 | 5000 | 5000 | 5000 | 0.5652087255655611 |
| 1 | 2026090841 | 5000 | 5000 | 5000 | 0.5661464344718445 |
| 2 | 2026090842 | 5000 | 5000 | 5000 | 0.5673372478600881 |
| 3 | 2026090843 | 5000 | 5000 | 5000 | 0.5685905197415816 |

Total proposal rows: `20000`.

Status and gap checks:

- total `FLOAT_CANDIDATE` rows: `0`;
- total positive stored midpoint gaps: `0`;
- maximum stored midpoint gap over all proposals:
  `-5.5879650249224255e-05`;
- every shard manifest has `positive_count = 0`;
- every CSV status is `NO_HIT`.

So the README statement “20,000 proposals, 0 status hit, 0 positive gap” is
correct for the four proposal CSV files.

## 2. Best rho and NPZ / seed-chain consistency

The strongest proposal is:

- shard: `3`;
- seed: `2026090843`;
- index: `4901`;
- label: `one_basis_rotation`;
- row status: `NO_HIT`;
- stored step: `0.0035259410255616148`;
- stored float gap: `-0.00021369102076107538`;
- best rho: `0.5685905197415816`.

Each shard's `best_case.json` matches the corresponding max-rho CSV row after
normalizing JSON numeric/bool types against CSV strings.  Each shard's
`best_case.npz` was independently re-evaluated with exact-event float atoms:

| shard | NPZ rho recomputed | abs diff vs row | min atom |
|---:|---:|---:|---:|
| 0 | 0.5652087255655616 | 4.44e-16 | 1.4095747366688796e-08 |
| 1 | 0.5661464344718443 | 2.22e-16 | 5.702225958058168e-09 |
| 2 | 0.5673372478600881 | 0.0 | 8.34828354842896e-09 |
| 3 | 0.5685905197415819 | 3.33e-16 | 1.756834588818421e-08 |

The strongest NPZ hash matches the README/recheck record:

- strongest NPZ SHA-256:
  `4bda0a82ca642b5e804bca498107a89a1c81a3a7eb79ce6aca2712e4d594cb72`;
- source NPZ SHA-256:
  `807ac23ae9b0c54c39d909ca543b72f69d95a9cc986cb7d4ff8295444d73cc01`;
- producing run-version script SHA-256:
  `88c610074973f10c683f9d927be6ed077cc6319f11bcf8a954829df26c90f592`.

## 3. Old source/base bookkeeping defect does not change this batch

The producing script retained in this directory is the old hash.  It does not
write source/base as a ledger row and does not count source status in
`positive_count`.

For this batch, that defect does not change the reported proposal no-hit result:

1. all 20,000 proposal rows are present in the four CSV files;
2. all proposal statuses are `NO_HIT`;
3. all proposal midpoint gaps are negative;
4. every shard manifest reports the same source recomputation
   `source_rho_recomputed = 0.5464281988363302 < 1`;
5. the source is described in the README as the already verified negative
   round-9 source;
6. every saved shard best NPZ was independently checked above.

Thus the omitted source/base row is a real old-hash bookkeeping defect, but not
a hidden positive in the 20,000-proposal denominator of this batch.

## 4. Independent 90-digit exact-event directional gate

For the strongest NPZ, I symmetrized the stored float `kernel` and `direction`,
then interpreted entries as Decimal rationals via Python `str(float)`.

Precision: `90` decimal digits.

The verifier recomputed all 4096 exact-event atoms, \(p'\), and \(p''\) from
\[
p(S)=(-1)^{n-|S|}\det(K-I_{S^c}),
\]
with
\[
p'(S)=p(S)\operatorname{tr}(M_S^{-1}D),
\]
and
\[
p''(S)=p(S)\left[
\operatorname{tr}(M_S^{-1}D)^2
-\operatorname{tr}(M_S^{-1}DM_S^{-1}D)
\right].
\]

Results:

- \(\sum p = 1.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000002\);
- \(\sum p' = 2.347136E-89\);
- \(\sum p'' = 1.430716E-88\);
- minimum atom:
  `1.75683458881841822508260264703497383819863606282305079733664691365086905359100023049266098E-8`;
- Fisher:
  `79.6727219320964920030753599425615499640644453282943583820109529899007345622728475500176280`;
- acceleration:
  `45.3011543725972850033524711906070027766320175634107357241380497289924867254672354824882399`;
- \(H''\):
  `-34.3715675594992069997228887519545471874324277648836226578729032609082478368056120675293881`;
- \(\rho\):
  `0.568590519741582017338387448711327072439459382659582355785353302716912909055705287352796475`.

This independently confirms the high-precision stable negative gate.

## 5. Three actual midpoint chords

The same independent Decimal exact-event entropy code checked three actual
chords:

| step | midpoint gap | central second difference |
|---:|---:|---:|
| 0.0035259410255616148 | -0.00021369102076303295548999123145459653561254483477153025222582860351318806934041268618769 | -34.3768580730567249672223264028236575392108939016070968424759754201686493324142694235057700 |
| 0.001 | -0.00001718599643125924689752077102686980258785527516412495086788814827859249976119693166019 | -34.37199286251849379504154205373960517571055032824990173577629655718499952239386332038 |
| 0.0001 | -1.7185785903022991871212656708500287033967494214768441113488274691276734983519429154E-7 | -34.371571806045983742425313417000574067934988429536882226976549382553469967038858308 |

All are negative.

## 6. Exact rational LDL feasibility

Using Fraction arithmetic on the symmetrized float entries interpreted through
`str(float)`, the verifier checked:

- \(D\succ0\);
- for both \(t=-1/200\) and \(t=1/200\),
  \[
  K+tD-\frac1{2000}I\succ0,\qquad
  I-K-tD-\frac1{2000}I\succ0.
  \]

LDL pivot summaries:

- \(D\): all 12 pivots positive; minimum float pivot
  `0.5552481721430836`;
- \(t=-1/200\):
  - \(K+tD-I/2000\): all positive; minimum float pivot
    `0.065308903558894`;
  - \(I-K-tD-I/2000\): all positive; minimum float pivot
    `0.0852294484067307`;
- \(t=1/200\):
  - \(K+tD-I/2000\): all positive; minimum float pivot
    `0.07937634678815328`;
  - \(I-K-tD-I/2000\): all positive; minimum float pivot
    `0.07533440868004457`.

So the rationalized strongest line has a strict feasibility certificate on
\(|t|\le 1/200\) with margin \(1/2000\).

## 7. Near-commuting limitation after rationalization

The producing float construction uses a common numerical eigenbasis, and the
stored strongest float matrices nearly commute:

- float commutator Frobenius for strongest NPZ:
  about `1.9662765384681346e-15`.

After decimal rationalization, exact commutation is not preserved:

- exact rational commutator zero: `false`;
- nonzero commutator entries: `132`;
- max absolute commutator entry as float:
  `3.535509958507361e-16`;
- max absolute commutator fraction:
  `4419387448134201231243/12500000000000000000000000000000000000`.

Therefore the exact Fraction feasibility/Hessian certificate is for a
near-commuting PSD \(K\)-affine line obtained by rationalizing the symmetrized
float matrices.  The producing scout mechanism is commuting/fixed-eigenbasis in
float arithmetic, but exact rationalization should not be overstated as an
exact commuting certificate.

## 8. Current corrected script and old-hash boundary

The current local `spectral_basis_refine.py` has the candidate-freezing fixes:

- source/base ledger row `index=-1`;
- `proposal_count` and `ledger_rows_including_source`;
- `candidate_source_base.{npz,json}`;
- per-proposal `candidate_INDEX.{npz,json}` for every `FLOAT_CANDIDATE`.

Current corrected script SHA-256:
`28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`.

This does not retroactively change round13, whose producing run-version script
has SHA-256
`88c610074973f10c683f9d927be6ed077cc6319f11bcf8a954829df26c90f592`.

Thus old round13 outputs must be interpreted with the old-hash caveat: if that
old run had contained a gap-only or source candidate not represented by final
`best_case.npz`, deterministic replay would be needed.  In this actual batch,
there are zero candidate rows and zero positive proposal gaps, so no such replay
is needed for a hidden candidate.

## Command

Independent verifier run:

```text
$env:PYTHONDONTWRITEBYTECODE='1'; $env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round13_refine/verifications/fresh_round13_verify.py'
```

Exit code: `0`.

## Final verdict

**CORRECT:** round13 ledger/accounting for the 20,000 proposal rows, zero status
hits, zero positive gaps, strongest row identity, best NPZ consistency, and
high-precision strongest-point negative gate.

**SCOUT:** the 20,000 proposal search is finite float64 evidence only.

**INCOMPLETE:** no continuous/global fixed-eigenbasis or PSD/NSD concavity
theorem follows from this batch.
