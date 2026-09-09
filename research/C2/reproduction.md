# Reproduction

All mathematics, rational inputs and code are included. No private path, credential or temporary cloud file is required.

Tested environment: Python 3.12.3, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0. Use a local virtual environment and install the versions in requirements.txt. Set OPENBLAS_NUM_THREADS, OMP_NUM_THREADS and MKL_NUM_THREADS to 1. No GPU is used.

From a disposable copy of this package:

```text
python main_check.py
cd mechanism
python check.py
cd ../search
python search.py
cd ../reviews/first
python independent_c2_verify.py
```

Each script writes into its current or containing directory. Work from a copy to preserve the published evidence. The search rerun uses the same deterministic 24 center records; it is not an instruction for further exploration. The retained run.sh files document actual relative invocations on the compute host; direct Python invocation avoids assumptions about virtual-environment layout.

main_check.py independently constructs both the low-degree law and the inclusion-exclusion law, checks all jets, reconstructs the rational frame certificate and the explicit cone constants. mpmath high-precision finite differences are calibration only; all exact algebraic assertions use SymPy rational values.

search.py outputs full matrices/directions and two interval negative-chord certificates. All exact probabilities and Sylvester determinants are included. Its mpmath interval logarithms use 70 decimal digits and outward intervals. The interval endpoints, rather than rounded display values, determine the sign. These are computational certificates, not proof-assistant objects.

Reviewer output is separately identified. A non-author independently reconstructs the formulas before reading the main implementation. Further candidate-review checks, when completed, are named in verification.md.

Formal verification scope: the inherited unrelated research/A2/formal project pins Lean 4.32.0 and imports Std only. That version was probed locally; the compute host exposes no Lean command. This round contains no Lean/Mathlib encoding of its analytic matrix and entropy theorems and claims no mechanical proof. Recompiling the old A2 integer example would not verify C2. Exact rational verification and two human-readable model reviews are reported at their actual scope.
