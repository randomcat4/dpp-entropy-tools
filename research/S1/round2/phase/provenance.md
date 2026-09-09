# Provenance and replay

Owner: the S1 phase sub-instance, reused for the two authorized round-two units. No descendants were spawned. The phase child is not the sole repository user and made no edits to others' work. New files are confined to `research/S1/round2/phase/` in its independent checkout. The authorized merge of the main round-one baseline `44ca50718b63ce5cb5d688bebe2dd6ef981cccc5` preserved history and old artifacts. Branch remains `research/S1-phase-20260909`.

The main frozen round-two contract was read without edits. The first unit's 12 rational-pattern centers were authored here and frozen in `28ef713e4b7f54f14f558a629061bb20fba28aa0`; the main instance then assigned the different spectral-factor unit, whose six explicit factors were authored here and frozen in `84588292ab2ab374fd058b9adf9801b6b0fed29e`. Main guidance suggested spectral factors and unit-circle root controls. No independent reviewer authored these objects. The former original-paper semantic check remains applicable; no fresh novelty or status survey was performed.

Replay from the child repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python research/S1/round2/phase/full_hessian.py --input research/S1/round2/phase/centers.json --output research/S1/round2/phase/results.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python research/S1/round2/phase/spectral_probe.py --input research/S1/round2/phase/spectral_centers.json --output research/S1/round2/phase/spectral_results.json
```

Standard output and error were redirected to `run.log` and `spectral_run.log`. Each process was launched once, sequentially, used one BLAS/OpenMP thread, limited address space to 4294967296 bytes, and used no GPU. Dependencies: Python 3.12.3, NumPy 2.1.2, SciPy 1.14.1. No installations or global configuration changes occurred. Seed is null, with no randomness used.

|Unit|PID|Exit|Elapsed seconds|Peak RSS KiB|Centers|Hessians|Events|
|---|---:|---:|---:|---:|---:|---:|---:|
|coefficient patterns|160982|0|0.224244|34892|12|24|3840|
|spectral factors|161415|0|0.109217|34880|6|12|1920|

Both processes wrote complete result files and their actual shell calls returned exit 0. Subsequent PID checks confirmed neither remained alive. No partial execution, numerical failure, retry or omitted point occurred. The main route's separate one-center/two-Hessian baseline is excluded from this child coverage.

SHA256 values at execution:

```text
centers.json          460e5e027c5e9ed05a4b0f18aa55f72ef6004c85934ee2524028b649589b7b19
spectral_centers.json e65da60830905fe646fc5515ff4219b3dd1f9c1a2c83b7031a01ec3e45be162d
full_hessian.py       591696cebaded001250760809b54e7810200a462b2e2086d61bb45f22fa1371b
spectral_probe.py     fcd449d289ea90ee7799b7edcd3adf12924ced1bcc6caea15170acfbefd4cc61
```

The spectral script records both its own source hash and the imported Hessian source hash. The exact Gaussian integer autocorrelations and rational feasibility checks are actual invoked assertions. Event normalization, derivative normalization and gauge identities are internal consistency checks, not independent review or interval certification. Machine metadata and complete arrays are stored in the JSON and log files. Connection details and private handoffs are intentionally not part of this artifact tree.
