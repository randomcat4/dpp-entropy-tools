# Exact bridge premise checker

Input JSON has `K` and `A` square matrices. Entries must be integers or rational strings such as `"1/20"`; D is interpreted as iA. Floating-point JSON numbers are rejected. Vertex indices in output are zero-based.

```sh
python3 bridge_certificate.py examples/two_triangles.json
python3 -m unittest -v test_bridge_certificate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 diagnostic.py
```

The checker performs exact rational LDL decompositions and graph bridge checks and evaluates zero event probabilities. Its sign conclusion invokes frozen theorem v1, whose independent review is pending in this artifact. `NOT_APPLICABLE` reports no curvature conclusion. An invalid strict-interior premise returns `INVALID_INPUT`. The diagnostics enumerate only four fixed small examples to check the two formulas; their floating-point logarithm values are not interval certificates or a theorem proof. There are no third-party dependencies. The diagnostic determinant derivatives, masses, and Schur complements are exact rational calculations; only logarithms and final sums use floating point.
