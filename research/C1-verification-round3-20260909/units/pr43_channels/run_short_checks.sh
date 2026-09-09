#!/usr/bin/env bash
set -u
cd -- "$(dirname -- "cd [isolated owned execution directory] || exit 2")" || exit 2

{
  date -Is
  "${PYTHON:-python3}" --version
  "${PYTHON:-python3}" -c "import sympy, numpy, mpmath; print('sympy', sympy.__version__); print('numpy', numpy.__version__); print('mpmath', mpmath.__version__)"
} > short_exact_checks.version.txt 2> short_exact_checks.version.err

{
  date -Is
  "${PYTHON:-python3}" short_exact_checks.py
  ec=$?
  date -Is
  echo EXIT_CODE=$ec
  exit $ec
} > short_exact_checks.out 2> short_exact_checks.err
