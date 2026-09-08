# D10-U10a scalar_direct audit run log

Scope:

- Wrote only `scalar_direct/audit_nonauthor/`.
- Did not modify author files, U8 files, self-review files, shared indexes, or
  other directories.
- Did not import or execute author `sanity.py` or `self_review`.
- Did not spawn subagents, use a server, install dependencies, or submit.
- Did not access, search, traverse, or modify `C:\canglan\`.

## Command

From `scalar_direct/audit_nonauthor/`:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe audit.py
```

Thread-related environment variables were set to one:

```text
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```

Exit code: `0`.

Output:

```text
audit_results.json
```

## Checks performed

- Read and hashed scalar_direct author text, frozen result JSON, and
  self_review files as frozen inputs.
- Independently rebuilt n=3 exact atoms by Mobius inversion of inclusion
  determinants.
- Recomputed atom gradients and exact direction jets with Fraction arithmetic.
- Checked Fisher positive definiteness on a dense and a path connected kernel.
- Checked `rho=min_g Q(g)` by direct Decimal quadratic minimization.
- Checked the unregularized inclusion-statistic capacity formula through an
  independent KKT solve.
- Checked five-category coarse Fisher and complement orientation.
- Rebuilt the rational path blocker with rational log intervals.
- Certified `D>0` and the whole `|t|<=1/100` chord margin by exact Fraction
  LDL at endpoints plus convexity.
- Verified the three nested rank-one Fisher additions exactly and the
  sequential Sherman-Morrison scalar corrections numerically at high precision.

## Generated files

- `audit.py`
- `audit_results.json`
- `verdict.md`
- `run_log.md`

Artifact hashes, excluding this self-referential run log:

| file | SHA256 |
| --- | --- |
| `audit.py` | `B5FBB1702AAE39AA8660CB30B681F7734AE201C91AD637A8CEC382293462BD2D` |
| `audit_results.json` | `E0DA080D4DBD305CF510C5A443EC63D284EADB99F647D8ABF5D2C84A09157E1C` |
| `verdict.md` | `086EA27C219755E92A4117352600BEBD8C2C8C81E4B3A31D5E05076D15CB4101` |
