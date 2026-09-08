# Main execution record

All runs below actually completed on the allocated CPU server, with no randomness, no GPU, and OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1. Python was 3.12.3, NumPy 2.1.2 and mpmath 1.3.0 where applicable. Source/input hashes and dependency versions are in the JSON files. Each process exited 0. Later residual/certificate invocations imposed a 4 GiB virtual-memory limit; all observed RSS peaks were below 61 MiB.

Run the following from the repository root using that Python environment:

```text
python research/S1/main/baseline_unit.py --candidate research/S1/baseline_candidate.json --output research/S1/main/baseline_result.json --max-n 12
python research/S1/main/boundary_residual.py --candidate research/S1/baseline_candidate.json --output research/S1/main/boundary_residual_result.json --M 48
python research/S1/main/boundary_residual.py --candidate research/S1/baseline_candidate.json --output research/S1/main/boundary_residual_M64.json --M 64
python research/S1/main/rational_rate_certificate.py --candidate research/S1/baseline_candidate.json --boundary research/S1/main/boundary_residual_M64.json --output research/S1/main/rational_rate_n8.json --n 8
python research/S1/main/boundary_residual.py --candidate research/S1/main/phase_candidate.json --output research/S1/main/phase_boundary_M64.json --M 64
python research/S1/main/variational_boundary.py --candidate research/S1/main/phase_candidate.json --input research/S1/main/phase_boundary_M64.json --output research/S1/main/phase_variational_M64.json
python research/S1/main/rational_rate_certificate.py --candidate research/S1/main/phase_candidate.json --boundary research/S1/main/phase_variational_M64.json --output research/S1/main/phase_rate_n8.json --n 8
```

| Process PID | Unit | Actual coverage | Seconds |
|---:|---|---|---:|
|157942|B0 finite/coarse-rate|24,754 event evaluations including conjugation checks|0.045|
|159058|B0 residual M48|4 cases, 612 complex residual entries|1.880|
|159085|B0 residual M64|4 cases, 804 complex residual entries|4.016|
|159305|B0 n8 strict rate|3,072 exact determinants|2.099|
|159805|P0 residual M64|4 cases, 804 complex residual entries|3.902|
|159861|P0 variational refinement|4 exact rational residual/corner recalculations|0.074|
|159860|P0 n8 strict rate|3,072 exact determinants|5.202|

The residual solve's saved git head is the starting server checkout, while its source SHA256 identifies the actual uploaded version; it is not represented as already committed at runtime. The final local/public frozen-object mappings identify the reviewed source snapshots. An inventory after these runs found no listed main or phase PID alive. No other workload was terminated.
