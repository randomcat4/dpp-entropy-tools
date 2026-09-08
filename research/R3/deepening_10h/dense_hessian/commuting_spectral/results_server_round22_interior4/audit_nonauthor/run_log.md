# D10-H14 / round22_interior4 non-author audit run log

Scope:

- Wrote only `results_server_round22_interior4/audit_nonauthor/`.
- Did not modify author files, shared indexes, or prior audit directories.
- Did not import author recheck/search/gate implementation.
- Did not use a server or spawn subagents.
- Did not access, search, traverse, or modify `C:\canglan\`.

## Commands

From `audit_nonauthor/`:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe audit.py
```

Thread-related environment variables were set to one for the run:

```text
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```

Final exit code: `0`.

Output:

```text
audit_results.json
```

## Independent checks performed

- Parsed all four ledgers, manifests and run logs.
- Matched final log JSON lines against manifests.
- Located the strongest row by `rho_psd` across all rows.
- Matched strongest row against shard-0 `best_case.json`.
- Hashed source and strongest NPZ files and compared with README hashes.
- Reconstructed fixed-`Q` spectral-rate line semantics from NPZ arrays.
- Rebuilt the strongest point's `4096` exact events by Mobius inversion of
  inclusion determinants.
- Computed high-precision Fisher, acceleration, `H''`, `rho`, and actual
  midpoint chords.
- Certified `D>0` and `K(t), I-K(t)` strict feasibility on `|t|<=1/200` with
  `1/2000` margin by Fraction LDL.
- Parsed H10--H14 README profile values for finite-evidence comparison.

## Generated files

- `audit.py`
- `audit_results.json`
- `verdict.md`
- `run_log.md`

Artifact hashes, excluding this self-referential run log:

| file | SHA256 |
| --- | --- |
| `audit.py` | `1B39A3F57347788171D16A53456B5FAAE183DC558C4A3B12F0C6D0DB5FE69EFF` |
| `audit_results.json` | `047743A1A7D9C919CA77C7C015BC78DF6BCEC05ADCCE622C1CA6246E82D73C71` |
| `verdict.md` | `7301F675BCA379BAAF3B5F08AA4A5E9A611073B5E023D25C82C0CE825648BDD3` |
