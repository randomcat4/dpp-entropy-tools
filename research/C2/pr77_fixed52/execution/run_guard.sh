#!/usr/bin/env bash
# One shared new 2700-second window; caller supplies its own isolated paths.
set -u
RUN_DIR="$1"
BUDGET_DIR="$2"
PYTHON_BIN="$3"
SCRIPT_PATH="$4"
shift 4
mkdir -p "$RUN_DIR" "$BUDGET_DIR"
command -v timeout >/dev/null || exit 42
command -v flock >/dev/null || exit 43
exec 9>"$BUDGET_DIR/owner.lock"
flock -n 9 || { echo 'An owned execution is already active.' >&2; exit 44; }
if [ -f "$BUDGET_DIR/active_arithmetic_pid.txt" ]; then
  prior=$(cat "$BUDGET_DIR/active_arithmetic_pid.txt")
  if kill -0 "$prior" 2>/dev/null; then
    echo 'Recorded owned arithmetic PID is still active.' >&2
    exit 45
  fi
fi
if [ ! -f "$BUDGET_DIR/deadline_epoch.txt" ]; then
  start=$(date -u +%s)
  deadline=$((start+2700))
  echo "$start" > "$BUDGET_DIR/start_epoch.txt"
  echo "$deadline" > "$BUDGET_DIR/deadline_epoch.txt"
  date -u -d "@$start" +'%Y-%m-%dT%H:%M:%SZ' > "$BUDGET_DIR/start_utc.txt"
  date -u -d "@$deadline" +'%Y-%m-%dT%H:%M:%SZ' > "$BUDGET_DIR/deadline_utc.txt"
fi
deadline=$(cat "$BUDGET_DIR/deadline_epoch.txt")
remaining=$((deadline-$(date -u +%s)))
if [ "$remaining" -le 3 ]; then echo 'Shared deadline reached.' >&2; exit 46; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export C2_ABSOLUTE_DEADLINE_EPOCH="$deadline"
ulimit -v 16777216
allowed=$(taskset -pc $$ | awk -F: '{gsub(/ /,"",$2); print $2}')
cpu=${allowed%%,*}
cpu=${cpu%%-*}
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$RUN_DIR/start_utc.txt"
cp "$BUDGET_DIR/deadline_utc.txt" "$RUN_DIR/deadline_utc.txt"
echo "$cpu" > "$RUN_DIR/cpu_affinity.txt"
printf '{"status":"RUNNING","available_seconds":%s}\n' "$remaining" > "$RUN_DIR/exit.json"
printf '%q ' "$PYTHON_BIN" "$SCRIPT_PATH" "$@" > "$RUN_DIR/invocation_private.txt"
printf '\n' >> "$RUN_DIR/invocation_private.txt"
timeout --signal=KILL "${remaining}s" taskset -c "$cpu" "$PYTHON_BIN" "$SCRIPT_PATH" "$@" > "$RUN_DIR/stdout.log" 2> "$RUN_DIR/stderr.log" &
guard=$!
echo "$guard" > "$RUN_DIR/timeout_pid.txt"
sleep 0.2
pgrep -P "$guard" > "$RUN_DIR/arithmetic_pid.txt" || true
if [ -s "$RUN_DIR/arithmetic_pid.txt" ]; then cp "$RUN_DIR/arithmetic_pid.txt" "$BUDGET_DIR/active_arithmetic_pid.txt"; fi
wait "$guard"
code=$?
printf '{"status":"EXITED","exit_code":%s,"finished_utc":"%s"}\n' "$code" "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" > "$RUN_DIR/exit.json"
exit "$code"
