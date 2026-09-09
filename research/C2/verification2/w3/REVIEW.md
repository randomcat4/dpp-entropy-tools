ACCEPTED_SCOPED W3/T1 near-scalar all-direction Hessian bound only; novelty, Lean formalization, and global `0<A<I` concavity are not certified.

## Scope and source binding

I audited only T1 from `math/i05-web-round2-20260909/harvest/W3/frozen_statement.md:42`, namely: for every `a in (0,1)`, with `epsilon=min(a,1-a)` and `||A-aI||_op <= epsilon^2/1000`, the proof must show `H''_A[V,V] <= -||V||_F^2/25` for all real symmetric `V` along the actual affine path `A+tV`, hence `K(t)=U(A+tV)U^T`. I did not read old W3 reviews or author result judgments before forming this verdict.

Bound source blobs supplied by the main instance:

- `frozen_statement.md`: `6678e3db6e47ef548362fdd6e7ef9626dad6e2da`
- `proof.md`: `e985c56d258c7f08ff159960f59fac57e3c8692d`
- `code/verify.py`: `485ea7fe663256d40173bef7b272cf0f28a5bdaa`

The frozen statement itself marks the original global target as `PARTIAL`, not solved, at `frozen_statement.md:5` and `frozen_statement.md:7`. T1's near-scalar radius and all-direction conclusion are at `frozen_statement.md:44` through `frozen_statement.md:56`; chord limitations are at `frozen_statement.md:82` through `frozen_statement.md:91`; newness is explicitly unaudited at `frozen_statement.md:93` through `frozen_statement.md:95`.

## Independent reconstruction

The probability reconstruction is sound for the fixed rank-three DPP. The proof derives the L-ensemble formula from the full event generating polynomial and keeps the path affine in `A`, not in `B` or `L`, at `proof.md:34` through `proof.md:40`. The layer formulas for empty, singleton, pair, and triple events are given at `proof.md:42` through `proof.md:60`. The support claim is also correct: under `0<A<I` and full spark, exactly the `|S|<=3` events are positive and the six `|S|>3` events are identically zero, as stated at `proof.md:62`.

The entropy decomposition does not drop the top layer. The proof first separates `H=Phi+G` over all positive support configurations at `proof.md:66` through `proof.md:93`, then proves the exact geometric polynomial identity for `G` at `proof.md:114` through `proof.md:150`. The determinant/adjugate Hessian identities used there are standard three-dimensional polarization identities and are stated at `proof.md:123` through `proof.md:129`.

The center Fisher identity uses all four layers. At `proof.md:157` through `proof.md:176`, the empty and triple layers, plus singleton and pair cross terms, cancel exactly, leaving the full Fisher form `F_a`. The log-acceleration term at the scalar center vanishes because total mass and expected cardinality have zero second derivative along every `A`-affine direction; see `proof.md:184` through `proof.md:200`. This proves the center identity `H''_{aI}=-F_a-tr(adj(V)M_a)`.

The center compensation estimate is also valid for noncommuting directions. The proof decomposes `V=sI+W`, with `tr W=0`, at `proof.md:319` through `proof.md:332`, expands `adj(sI+W)` without simultaneous diagonalization at `proof.md:335` through `proof.md:347`, and uses the certified bounds on `m(a)` and `E` to prove
`(7/8)F_a(V)+tr(adj(V)M_a) >= 119/1600 ||V||_F^2`
at `proof.md:349` through `proof.md:374`.

The non-scalar transfer is the load-bearing part and I found it closed. With `delta=||A-aI||_op`, `rho=delta/epsilon`, the proof bounds every normalized probability ratio between `(1-rho)^3` and `(1+rho)^3` at `proof.md:378` through `proof.md:398`. It then bounds every `Q''_S(B)[V,V]` uniformly by layer constants `(2,3,3,2)` at `proof.md:400` through `proof.md:428`, converts this to a mixed Hessian bound at `proof.md:430` through `proof.md:443`, and uses it to prove the Fisher stability estimate at `proof.md:445` through `proof.md:481`. The log-acceleration remainder keeps all layers and has weight constant `2+9+9+2=22`, giving `66 rho/(1-rho)` at `proof.md:483` through `proof.md:502`. The geometric error `2 beta tr((A-aI)adj(V))` is bounded at `proof.md:504` through `proof.md:508`.

Combining these gives the exact final coefficient at `proof.md:510` through `proof.md:545`:

`119/1600 - 243/250000 - 66/1999 - 1/16000 = 161215319/3998000000 = 1/25 + 1295319/3998000000`.

Thus the proof reaches the frozen T1 conclusion with a small but strictly positive rational margin. The chord statement is scoped correctly: it only applies when the whole symmetric segment remains inside one T1 closed ball; see `proof.md:560` through `proof.md:567`.

## Certificate audit

The bundled verifier uses exact `Fraction` arithmetic and rational log intervals, not floating-point proof decisions; see `code/verify.py:2` through `code/verify.py:7` and `code/verify.py:72` through `code/verify.py:83`. It verifies the fixed `U`, full spark support weights, and both tight-frame identities at `code/verify.py:168` through `code/verify.py:181`. It verifies `m(0),m(1)`, `beta`, and the `E` operator/Frobenius bounds at `code/verify.py:183` through `code/verify.py:206`, the Fisher LDL certificate at `code/verify.py:211` through `code/verify.py:215`, and the final rational margin at `code/verify.py:223` through `code/verify.py:227`.

Relevant certificate fields are present in `output/certificate.json`: arithmetic mode at line `3`, `U` at line `6`, log-derived constants at lines `158` through `178`, `E_geo/E0` and `E` bounds at lines `189` through `251`, `E` pivots at lines `286` and `325`, Fisher certificate data at lines `430` and `530`, and the final `uniform_margin` at line `538`.

I also wrote and ran an independent verifier in this review directory:

- `math/i05-seven-fronts-20260909/runs/C2/verification2/w3/budget.md`
- `math/i05-seven-fronts-20260909/runs/C2/verification2/w3/independent_verify_w3.py`
- `math/i05-seven-fronts-20260909/runs/C2/verification2/w3/independent_output/independent_certificate.json`
- `math/i05-seven-fronts-20260909/runs/C2/verification2/w3/remote_output/stdout.txt`
- `math/i05-seven-fronts-20260909/runs/C2/verification2/w3/remote_output/environment.json`

The independent script reconstructs the frozen matrix directly from the displayed rational `U` at `independent_verify_w3.py:260`, uses 40-term rational log intervals at `independent_verify_w3.py:204` and `independent_verify_w3.py:284`, checks `E` with leading-principal-minor positive-definiteness at `independent_verify_w3.py:320`, checks the Fisher matrix by exact leading principal minors at `independent_verify_w3.py:325` through `independent_verify_w3.py:334`, checks the final margin at `independent_verify_w3.py:339` through `independent_verify_w3.py:342`, and independently recomputes the 32-event inclusion-exclusion coefficients at `independent_verify_w3.py:373` through `independent_verify_w3.py:389`.

Local run result:

```text
PASS_SCOPED_EXACT_CHECKS
positive_support=26 zero_events=6
uniform_margin=161215319/3998000000
margin_minus_1_over_25=1295319/3998000000
```

Server recomputation result, in the assigned remote W3 directory, was also successful:

```text
owned_pid=166879
exit_status=0
PASS_SCOPED_EXACT_CHECKS
positive_support=26 zero_events=6
uniform_margin=161215319/3998000000
margin_minus_1_over_25=1295319/3998000000
```

Server environment recorded in `remote_output/environment.json`: CPython `3.12.3`, Linux `6.8.0-79-generic`, `numpy 2.5.3`, `scipy 1.18.1`, `sympy 1.14.0`, `mpmath 1.3.0`, with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`.

## Verdict

Correctness for the scoped T1 statement: accepted. I found no weakening from the stated near-scalar hypothesis to a global `1/4 I <= A <= 3/4 I` claim, no commutativity assumption on `A` and `V`, no omission of the full Fisher contribution, and no missing event layer in the T1 derivation. The constants in the transfer step close with exact rational slack.

Novelty and importance: not audited. The frozen package itself says independent review and novelty certification were still pending; this review only certifies the scoped mathematical correctness of W3/T1 under the frozen assumptions.

Formal status: not Lean-checked and not mechanically formalized. This is a natural-language proof audit supported by exact rational finite certificates and an independent exact recomputation.
