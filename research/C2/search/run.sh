#!/bin/sh
set -u
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
printf '%s\n' '../.venv/bin/python search.py' > command.txt
../.venv/bin/python search.py > run.log 2>&1
result=$?
printf '%s\n' "$result" > exit_status.txt
exit "$result"
