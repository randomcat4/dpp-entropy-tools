#!/usr/bin/env bash
set -u

task_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$task_root"
mkdir -p outputs/run01/execution

if [[ -e outputs/run01/execution/started_utc.txt ]]; then
  echo "refusing second run: start marker exists" >&2
  exit 90
fi

date -u +%Y-%m-%dT%H:%M:%SZ > outputs/run01/execution/started_utc.txt
date -u -d '+600 seconds' +%Y-%m-%dT%H:%M:%SZ > outputs/run01/execution/deadline_utc.txt
python3 --version > outputs/run01/execution/python_version.txt 2>&1

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

set +e
/usr/bin/time -v -o outputs/run01/execution/time_verbose.txt \
  timeout --signal=TERM --kill-after=5s 600s \
  taskset -c 0 \
  bash -c 'ulimit -v 2097152; echo $$ > outputs/run01/execution/arithmetic_pid.txt; exec python3 implementation/independent_pr95_finite_checker.py --fixture inputs/fixture.json --source inputs/PR58_ADDENDUM_JOINT_ADDITIVE.md --out outputs/run01' \
  > outputs/run01/stdout.txt 2> outputs/run01/stderr.txt
exit_code=$?
set -e

printf '%s\n' "$exit_code" > outputs/run01/execution/exit_code.txt
date -u +%Y-%m-%dT%H:%M:%SZ > outputs/run01/execution/finished_utc.txt

arithmetic_pid="$(cat outputs/run01/execution/arithmetic_pid.txt 2>/dev/null || true)"
if [[ -n "$arithmetic_pid" ]] && kill -0 "$arithmetic_pid" 2>/dev/null; then
  printf 'PRESENT\n' > outputs/run01/execution/pid_postcheck.txt
  exit 91
else
  printf 'ABSENT\n' > outputs/run01/execution/pid_postcheck.txt
fi

exit "$exit_code"
