#!/bin/sh
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python_bin=${1:-python3}
"$python_bin" main_check.py > main_check.log 2>&1
run_status=$?
printf '%s\n' "$run_status" > main_check.exit
cat main_check.log
exit "$run_status"
