# R1 dense real-interior parameter search

Status: INCOMPLETE. This package records 13,202 finite objective calls and no positive-Hessian candidate. It does not prove entropy concavity.

The event law, derivative, and spectral parameterization are explained in `derivation.md`; numerical outcomes and limitations are in `result.md`.

## Reproduce

Use Python 3.12 with NumPy 2.1.2 and SciPy 1.14.1 on Linux. The launcher and optimizer use Linux resource limits. All numerical work is CPU-only with one BLAS/OpenMP thread.

Copy `search.py`, `optimize.py`, and `launch.py` into a **new empty working directory** before running either batch. This preserves the frozen compact results shipped here.

From that new directory:

```sh
python search.py --out smoke --selftest-only
python search.py --out batch01 --seed 202609081 --samples 20 --steps 30 --nmin 3 --nmax 10 --seconds 900
python optimize.py
```

Alternatively, `python launch.py` starts batch 01 with CPU and memory limits and writes a process record. Do not invoke both the direct batch-01 command and the launcher for the same output directory.

Batch 02 is fixed to seed 202609082, n=3 through 10, two restarts per dimension, at most 600 actual objective calls per restart and a 300-second wall-time ceiling. CPU speed or numerical-library differences may affect optimizer trajectories and wall-time truncation.

The bundled JSON files are frozen compact outputs. Absolute execution paths in the batch-01 summary have been replaced with the relative output name `batch01`; numeric data are unchanged. Full per-evaluation logs and process records are retained only in the private task working directory. They are not included in this public package.

The batch-02 restart guard is not a complete automatic recovery system. Do not rerun it in an existing result directory without inspecting prior completion and reconciling any interrupted partial restart.
