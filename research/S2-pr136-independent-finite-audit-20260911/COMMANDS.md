# Commands and environment

Interpreter:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
Python 3.12.14
Windows-11-10.0.26200-SP0
```

Executed input command:

```text
python certificate/make_inputs.py
```

Executed saved-data audits:

```text
python run_frozen_check.py
python independent_audit.py
```

The first independent audit failed at its own `cos(pi)` endpoint assertion;
after the endpoint-only repair, the same command passed. Full stdout and stderr
for both attempts are archived.

Required but blocked production command:

```text
g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp certificate/certify_nodes.cpp -o certificate/certify_nodes
certificate/certify_nodes certificate/nodes.tsv certificate/fresh_output.tsv 4 -1 1800
```

Compiler probes:

```text
where.exe g++       -> no match
where.exe clang++   -> no match
where.exe c++       -> no match
where.exe cl.exe    -> no match
```

Every executed process used `OMP_NUM_THREADS=4`, `OPENBLAS_NUM_THREADS=4`,
`MKL_NUM_THREADS=4`, `CUDA_VISIBLE_DEVICES=-1`, and CPU affinity `0xF`.
