#!/usr/bin/env bash
set -uo pipefail

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export PYTHONHASHSEED=0
ulimit -v 8388608

{
  echo "run_shell_pid=$$"
  echo "workdir=$(pwd)"
  echo "ulimit_v=$(ulimit -v)"
  echo "command=timeout 600 /opt/venv/bin/python independent_w4_certificate.py"
  /opt/venv/bin/python --version
  /opt/venv/bin/python - <<'PY'
import platform, sys
import numpy, mpmath, sympy
print("python_executable", sys.executable)
print("platform", platform.platform())
print("numpy", numpy.__version__)
print("mpmath", mpmath.__version__)
print("sympy", sympy.__version__)
PY
} > run_metadata.txt 2>&1

echo $$ > run.pid
timeout 600 /opt/venv/bin/python independent_w4_certificate.py > run_stdout.txt 2> run_stderr.txt
status=$?
echo "$status" > exit_status.txt
exit "$status"
