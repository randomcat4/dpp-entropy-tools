#!/usr/bin/env bash
set -euo pipefail

root=/root/i05-real-20260908/R3/noise_followup
code_root="$root/code"
ledger="$code_root/research/R3/structure/candidate_ledger.csv"
program="$code_root/research/R3/noise_followup/local_refine.py"
python=/opt/venv/bin/python

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

# Four single-threaded, independently checkpointed shards: two anchored at the
# ULP sign-flip record and two at the weakest-curvature record.
specs=(
  "raw_a 783 920783 150000"
  "raw_b 783 930783 150000"
  "weak_a 379 920379 250000"
  "weak_b 379 930379 250000"
)

for spec in "${specs[@]}"; do
  read -r name index seed trials <<<"$spec"
  out="$root/jobs/$name"
  mkdir -p "$out"
  if [[ -s "$out/pid" ]]; then
    old_pid=$(<"$out/pid")
    if kill -0 "$old_pid" 2>/dev/null; then
      echo "$name already running as PID $old_pid"
      continue
    fi
  fi
  nohup "$python" "$program" \
    --ledger "$ledger" \
    --index "$index" \
    --out "$out" \
    --seed "$seed" \
    --trials "$trials" \
    --checkpoint-every 100 \
    >"$out/stdout.log" 2>&1 &
  pid=$!
  printf '%s\n' "$pid" >"$out/pid"
  echo "launched $name as PID $pid ($trials trials, one thread)"
done
