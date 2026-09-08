# D10-B run log

Date: 2026-09-08.

## Command

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONIOENCODING=utf-8
python search_or_algebra.py --out evidence.json --precision 100
```

The actual Python executable was the local bundled Codex runtime Python.

Exit code: `0`.

## Parameters frozen in the run

n=3:

```text
beta = (1/3, -2/5)
tau_- = (1/40, 1/45, 1/50)
tau_+ = (1/55, 1/35, 1/60)
tau_0 = (tau_- + tau_+)/2
```

n=4:

```text
beta = (1/4, -1/3, 2/7)
tau_- = (1/30, 1/36, 1/42, 1/48)
tau_+ = (1/45, 1/33, 1/55, 1/39)
tau_0 = (tau_- + tau_+)/2
```

## Result

`evidence.json` status: `PASS`.

All exact K-midpoint identities, shape checks, SPD certificates, and direct
Möbius validations passed for the n=3 and n=4 triples.

## Attempt denominator

```text
1. Fixed-beta innovation construction: succeeded.
2. Exhaustive finite search: not run.
3. Positive-gap interval certification: not run, because scout gaps were
   negative.
```

No remote computation was used.  No GPU, NumPy, SciPy, BLAS, or OpenMP job was
used.
