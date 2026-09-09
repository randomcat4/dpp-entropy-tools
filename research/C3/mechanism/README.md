# Reproduction

From this directory, with Python 3.12, NumPy 2.5.3 and SymPy 1.14.0:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python check.py > run.log 2>&1
    echo $? > exit_status.txt

The script itself also fixes the four standard numerical thread environment variables before importing NumPy. It writes output.json, events_n8.csv and exact_n3.json. Actual input was input.json, with one n=8 window and one direction at one centre. Three endpoint/centre symbols are fixed independently of window size. Exact n=3 arithmetic checks the triangle formula and all event normalizations, not an extra symbol search.

The numerical values are diagnostic. They have no interval roundoff certificate. Their finite-window midpoint gap does not imply a rate-gap sign. mechanism.md contains the exact pointwise feasibility proof and the finite-scope analytic theorems.
