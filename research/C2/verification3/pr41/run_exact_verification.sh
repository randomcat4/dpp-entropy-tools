#!/usr/bin/env bash
set -u

TASK_DIR="${1:-$(pwd)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SOURCE_ROUND2="${SOURCE_ROUND2:-$TASK_DIR/source41_round2}"
OUT_PATH="${OUT_PATH:-$TASK_DIR/evidence.json}"
LOG_DIR="$TASK_DIR/logs"

mkdir -p "$LOG_DIR" "$TASK_DIR/checkpoints"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0

{
  date -u +"started_at_utc=%Y-%m-%dT%H:%M:%SZ"
  echo "runner_pid=$$"
  echo "task_dir=$TASK_DIR"
  echo "python_bin=$PYTHON_BIN"
  echo "source_round2=$SOURCE_ROUND2"
  echo "out_path=$OUT_PATH"
  echo "memory_limit_kib=4194304"
  echo "timeout_seconds=2700"
  echo "command=$PYTHON_BIN $TASK_DIR/verify_pr41_independent.py --source-round2 $SOURCE_ROUND2 --out $OUT_PATH"
} > "$LOG_DIR/invocation.txt"

ulimit -v 4194304
timeout 2700 "$PYTHON_BIN" "$TASK_DIR/verify_pr41_independent.py" \
  --source-round2 "$SOURCE_ROUND2" \
  --out "$OUT_PATH" \
  > "$LOG_DIR/stdout.txt" \
  2> "$LOG_DIR/stderr.txt"
code=$?

{
  echo "$code"
} > "$LOG_DIR/exit_code.txt.tmp"
mv "$LOG_DIR/exit_code.txt.tmp" "$LOG_DIR/exit_code.txt"

date -u +"finished_at_utc=%Y-%m-%dT%H:%M:%SZ" > "$LOG_DIR/finished.txt"
exit "$code"
