#!/usr/bin/env bash
set -u

RUN_ROOT="${RUN_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SOURCE_ROOT="${SOURCE_ROOT:-$RUN_ROOT/source43/randomcat4-dpp-entropy-tools-4e1369e/research/I05-W1-20260909-R2}"
OUT_DIR="${OUT_DIR:-$RUN_ROOT/output}"
LOG_DIR="$RUN_ROOT/logs"

mkdir -p "$OUT_DIR" "$LOG_DIR"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export BLIS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=
export PYTHONHASHSEED=0

ulimit -v 4194304

INVOCATION_FILE="$LOG_DIR/invocation.json"
EXIT_FILE="$LOG_DIR/exit_status.json"
STDOUT_FILE="$LOG_DIR/standalone_pr43_events.stdout"
STDERR_FILE="$LOG_DIR/standalone_pr43_events.stderr"

cat > "$INVOCATION_FILE" <<EOF
{
  "run_root": "$RUN_ROOT",
  "python": "$PYTHON_BIN",
  "source_root": "$SOURCE_ROOT",
  "out_dir": "$OUT_DIR",
  "threads": {
    "OMP_NUM_THREADS": "$OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS": "$OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS": "$MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS": "$NUMEXPR_NUM_THREADS"
  },
  "memory_limit": "ulimit -v 4194304",
  "gpu": "CUDA_VISIBLE_DEVICES empty",
  "timeout": "45m"
}
EOF

START_EPOCH="$(date -u +%s)"
timeout 45m "$PYTHON_BIN" "$RUN_ROOT/standalone_pr43_events.py" \
  --source-root "$SOURCE_ROOT" \
  --out-dir "$OUT_DIR" \
  --timeout-seconds 2700 \
  > "$STDOUT_FILE" 2> "$STDERR_FILE"
EXIT_CODE="$?"
END_EPOCH="$(date -u +%s)"

cat > "$EXIT_FILE" <<EOF
{
  "exit_code": $EXIT_CODE,
  "start_epoch_utc": $START_EPOCH,
  "end_epoch_utc": $END_EPOCH,
  "duration_seconds": $((END_EPOCH - START_EPOCH)),
  "stdout_file": "$STDOUT_FILE",
  "stderr_file": "$STDERR_FILE"
}
EOF

exit "$EXIT_CODE"
