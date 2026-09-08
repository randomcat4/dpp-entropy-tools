# U8/M10 execution and failure ledger

Date: 2026-09-08. Only this new directory was written. No server, GPU, installation, random sampling, subagent or submission. OpenBLAS was limited to one thread. The math-theorem research workflow was used; the author leaves correctness certification to another reviewer.

Commands from the repository root, using the configured Python runtime:

```text
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/global_probe.py
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/rank_one_recheck.py
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/point_interval_gate.py
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symbolic_identity_gate.py
```

All executions returned exit 0. The first scout took 1.435096025466919 seconds. The initial rank-one recheck covered four frozen points and 18 boundary points; the final expanded recheck retains those records, adds all 420 connected original centers and 12 unequal-rate boundary points, and took 1.9114084243774414 seconds. The rational point gate took 0.21467876434326172 seconds. No run failed. Read-only diagnostic summaries and an exploratory N-sign check used the same 510 centers and did not create additional samples.

## Full finite denominator

The initial 510 cases comprise:

- 360 rational spectral constructions: six fixed quaternion orthogonal matrices; 20 eigenvalue profiles for each delta=1/20,1/1000,1/1000000. Profiles cover all eight near-corners, six permutations of (delta,1/4,3/4), three permutations of (delta,delta,1/2), and three permutations of (1-delta,1-delta,1/2).
- 150 rational boundary-ray constructions: five diagonal choices, five sparse/mixed-sign edge patterns, and six fixed fractions of an exactly bracketed spectral boundary. A 32-step rational bisection uses exact LDL tests of K and I-K. Every lower endpoint is strict, and every selected fraction is less than one.
- Exactly 420 centers have connected observation support, and 90 are disconnected. The disconnected cases retain their exact cross-block degeneracy rather than being counted as positive-curvature candidates.

Each record retains the complete K, generation parameters, boundary bracket if applicable, minimum exact atom, normalized-Hessian score, and status. No denominator is truncated. Initial Hessians use 80-digit Decimal logarithms and exact rational Fisher summands. Congruence by square roots of the positive active coordinate diagonals is used only for numerical scouting; it avoids confusing weak near-diagonal directions with a raw floating-point rounding floor. No FLOAT_CANDIDATE was found.

The rank-one recheck recomputes the exact conditional-odds square identities and the full cofactor decomposition, then solves the explicit six-dimensional positive system:

- 420 distinct connected original centers at 100 digits;
- four selected original centers again at 120 digits, not four additional samples;
- 18 equal-soft-eigenvalue boundary points: theta=1/10,1/2,9/10, u=(1,2,2)/3, epsilon=10^(-k), k=2,4,8,16,32,64;
- 12 unequal-rate boundary points: one fixed quaternion basis, eigenvalues (epsilon^r,epsilon^s,1/2), rate pairs (1,2),(1,3),(2,3), and k=2,4,8,16.

Boundary precision is max(120,3*k+80), or max(120,3*max(r,s)*k+80) for unequal rates, reaching 272 digits. All scalar records remained below one. These high-precision comparisons are SCOUT, not interval certificates or proofs of untested points.

## Exact gates

The symbolic gate proves six conditional-odds polynomial identities for all six kernel coordinates, not by sampling. It also verifies exact mass, first/second derivative mass and all diagonal rank-one zero atom accelerations.

The separate point gate freezes original index 241, with eigenvalues (1/1000000,1/1000000,1/2) in quaternion basis (1,2,3,4). Exact rational LDL verifies spectral margin 1/2000000. All eight atoms are positive, with minimum 1/2000000000000. A 32-term range-reduced rational logarithm enclosure and a rational upper-triangular inverse-Cholesky proposal of denominator cap 4096 yield positive Gershgorin row margins after congruence, minimum approximately 0.9996041547479007. The first cap passed, so no later cap was attempted. This is a point positive-definiteness certificate candidate, not a region/global certificate.

## Observed values and mathematical scope

The smallest original normalized-Hessian eigenvalue score was approximately 2.2499372909546757e-5 at index 241. Its Schur scalar is approximately 0.85962497253445165, also the maximum among the 420 connected original centers. The selected point passed the exact interval gate above.

The largest unequal-rate boundary scalar was approximately 0.96072019864354618. The largest equal-rate boundary scalar was approximately 0.99244770478402201 at theta=9/10, epsilon=10^(-64). The latter is close to one but still consistent with the analytically derived positive deficit, not a positive-curvature witness.

Two proof shortcuts were explicitly rejected:

- Positive N and positive Fisher alone do not prove the global bound; the artificial non-DPP pair N=I, Fisher=Frobenius identity has rho=3/2 and B(I,I)=-3.
- A universal strict constant rho<=c<1 is incompatible with the dense rank-one boundary asymptotic rho tending to one. The analytic boundary theorem is itself still an author candidate pending review.

No discarded float signal or finite non-hit was promoted to a theorem. The global questions remain INCOMPLETE.

## Frozen hashes

Sources:

- global_probe.py: `1b171442be0ffa070cfc535e6b3067ca8f3a13ac0861c717a4129d540d52d347`
- rank_one_recheck.py: `5121c566d621d7c66f374ebf9419364aa52f8649187751e7556b32b6d4ba6bd6`
- point_interval_gate.py: `5baff127ef57e369597dcec228f47a0065acda0f3d0ce1190cb9be348895a876`
- symbolic_identity_gate.py: `cc750bf832db9751fb6ce430a1c992c4ba9db52de80c4806b8b53b374b038511`

Results:

- scout_results.json: `eec04bb7a6f6f92ccf757ac01e79cac4a74ab081d4001b915dda70a3fd4686d3`
- rank_one_results.json: `7ead2cf4a3b0a254674bd9082c3815da9c5bd200180c51a020ab838cdd2053cb`
- point_interval_results.json: `dbaaefee51ed61b6f1c0fe07558743bc3b4a63d875ea5eab3a8f5fe3247cce88`
- symbolic_identity_results.json: `88924a76e49d9c30aa687090274929b28fa01aea33ac5dcf658083cbdbde65b1`.

Results containing elapsed time can acquire a different raw hash on rerun while retaining identical mathematical witnesses. All imports remain within this new unit plus standard libraries/numpy; no other research module is imported. No Lean or external formal-kernel certification is claimed.
