#!/usr/bin/env bash
set -u
cd -- "$(dirname -- "$0")" || exit 2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
ulimit -v 8388608 || exit 3
printf 'WRAPPER_PID=%s\n' "$$" > channels_execution.txt
date -Is >> channels_execution.txt
printf 'THREADS=1\nVMEM_KIB=8388608\nTIMEOUT_SECONDS=600\n' >> channels_execution.txt
timeout --signal=TERM --kill-after=10s 600 "${PYTHON:-python3}" -u -c 'import os,runpy,sys; print("ARITHMETIC_PID="+str(os.getpid()),flush=True); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name="__main__")' short_exact_checks.py > channels_stdout.txt 2> channels_stderr.txt
job_status=$?
printf 'ACTUAL_EXIT=%s\n' "$job_status" >> channels_execution.txt
date -Is >> channels_execution.txt
exit "$job_status"
