#!/usr/bin/env bash
set -u

cd /root/i05-seven-fronts-20260909/C2/verification2/hessian || exit 97

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

PY=/root/i05-seven-fronts-20260909/C2/.venv/bin/python
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
INVOCATION_DIR=output/server_invocations
mkdir -p "$INVOCATION_DIR"

META="$INVOCATION_DIR/minimal_nonscalar_${STAMP}.meta"
LOG="$INVOCATION_DIR/minimal_nonscalar_${STAMP}.log"
EXIT_FILE="$INVOCATION_DIR/minimal_nonscalar_${STAMP}.exit"

{
  echo "started_utc=$STAMP"
  echo "runner_pid=$$"
  echo "python_version=$($PY -V 2>&1)"
  echo "working_dir=$(pwd)"
  echo "input=inputs.json"
  echo "radius_plan=server_radius_plan.json"
  echo "only_center=R12_boundary_mid"
  echo "max_total_attempts=1"
  echo "log_terms=from_inputs"
  echo "checkpoint=accepted_box_attempt_*.json"
} > "$META"

"$PY" scripts/strict_hessian_certificate.py --input inputs.json --output-root output --radius-plan server_radius_plan.json --only-center R12_boundary_mid --max-attempts 1 > "$LOG" 2>&1
CODE=$?

{
  echo "exit_code=$CODE"
  echo "finished_utc=$(date -u +%Y%m%dT%H%M%SZ)"
} > "$EXIT_FILE"

exit "$CODE"
