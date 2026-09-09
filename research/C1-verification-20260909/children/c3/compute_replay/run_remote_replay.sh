#!/usr/bin/env bash
set -u

BASE="/root/i05-seven-fronts-20260909/C1/verification/c3/replay_20260909_c3"
PY="/opt/venv/bin/python"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=""

ulimit -v 8388608

mkdir -p "$BASE/logs" "$BASE/replay_rate/artifacts"

"$PY" - <<'PY' > "$BASE/logs/version.json" 2> "$BASE/logs/version.stderr"
import json
import os
import platform
import sys

import mpmath
import numpy
import sympy

print(json.dumps({
    "python": sys.version,
    "platform": platform.platform(),
    "versions": {
        "numpy": numpy.__version__,
        "mpmath": mpmath.__version__,
        "sympy": sympy.__version__,
    },
    "pid": os.getpid(),
}, indent=2))
PY
echo "$?" > "$BASE/logs/version.exit"

run_step() {
  name="$1"
  shift
  meta="$BASE/logs/${name}.meta"
  out="$BASE/logs/${name}.stdout"
  err="$BASE/logs/${name}.stderr"
  start_epoch="$(date -u +%s)"
  start_iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  {
    echo "name=$name"
    echo "start_utc=$start_iso"
    echo "workdir=$(pwd)"
    echo "command=$*"
  } > "$meta"
  timeout 600 "$@" > "$out" 2> "$err" &
  pid="$!"
  echo "pid=$pid" >> "$meta"
  wait "$pid"
  status="$?"
  end_epoch="$(date -u +%s)"
  end_iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  {
    echo "end_utc=$end_iso"
    echo "elapsed_seconds=$((end_epoch - start_epoch))"
    echo "exit_status=$status"
  } >> "$meta"
  echo "$status" > "$BASE/logs/${name}.exit"
  if [ "$status" -ne 0 ]; then
    exit "$status"
  fi
}

cd "$BASE/replay_rate" || exit 90
run_step boundary "$PY" scripts/c3_m1_variational_boundary.py --candidate candidate.json --output artifacts/c3_m1_boundary_M64.replay.json --M 64 --bits 160
run_step rate "$PY" scripts/c3_m1_rate_certificate.py --candidate candidate.json --boundary artifacts/c3_m1_boundary_M64.replay.json --output artifacts/c3_m1_rate_n4.replay.json --n 4
run_step audit "$PY" scripts/c3_m1_audit.py --candidate candidate.json --true-symbol candidate_true_symbol.json --boundary artifacts/c3_m1_boundary_M64.replay.json --rate artifacts/c3_m1_rate_n4.replay.json --output artifacts/c3_m1_audit_result.replay.json

cd "$BASE" || exit 91
run_step reviewer "$PY" reviewer_rate_checker.py --original-rate-dir original_rate --replay-rate-dir replay_rate --output logs/reviewer_rate_checker_result.json
