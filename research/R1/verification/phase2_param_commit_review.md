STATUS: CORRECT

Reviewed commit: `187e8a8a3f3ad3b03d686930253ebeaf0b5e228b`

Reviewed tree: `dc7acefc43aa51745bb4b96138a3fd9d86e5f40d`

Key blob ids:

- result: `29dd0ca1ae9d7cf2291bb2e6175cb48d0d482dd1`
- ledger: `0ae369486508c88832e39c52619f4b2a6a649c9f`
- summary: `0b01f86d37c8d6128611f9b54473d089b6189ee0`
- engine: `f9738402e5dc7df392d0d5cafce6fd5481e94841`
- numerics: `24d40e8de0e7a1a6fd57654f2fc762837dc0e099`
- best: `1136f64f895cc6df80c8dcd044904d245579977d`

Scope: commit-bound review only. I read fixed files from the reviewed commit
using `git show <commit>:<path>`. I did not read worktree copies, did not run
remote jobs, did not modify `public_repo`, and did not participate in the
P2-01 search implementation or run.

## Differences found

None.

## 1. Attempt accounting

The accounting is internally consistent.

Formal calls:

```text
42,578
```

Validation calls:

```text
40 + 40 + 17 + 43 + 64 + 64 + 43 + 512 = 823
```

Combined actual second-stage attempts:

```text
42,578 + 823 = 43,401 <= 50,000.
```

The formal engine cap is `48,000`, and the validation ledger reports
`maximum_combined_calls_after_registered_formal_run = 48,823`, still below
the parent cap of `50,000`. The actual combined count is lower because the
formal batch stopped at `42,578`.

## 2. Restart, stratum, ID, status, and exit checks

The formal batch requested:

```text
8 dimensions * 4 margin bands * 2 restarts = 64 restarts.
```

The ledger and summary both report `finished_restarts = 64` /
`completed_restarts = 64`.

Restart endings are consistent:

```text
15 optimizer-convergence terminations
49 per-restart call-limit terminations
15 + 49 = 64.
```

The per-dimension/per-band table sums correctly:

```text
n=3:  446 + 509 + 230 + 797  = 1,982
n=4:  1189 + 1221 + 1182 + 1104 = 4,696
n=5:  1414 + 1500 + 1486 + 1500 = 5,900
n=6:  1500 * 4 = 6,000
n=7:  1500 * 4 = 6,000
n=8:  1500 * 4 = 6,000
n=9:  1500 * 4 = 6,000
n=10: 1500 * 4 = 6,000
total = 42,578.
```

The column totals in `result.md` also sum correctly:

```text
10,549 + 10,730 + 10,398 + 10,901 = 42,578.
```

The final ledger audit reports:

- `formal_states = {"OK": 42578}`
- `formal_failures = 0`
- `distinct_call_ids = 42578`
- `min_call_id = 1`
- `max_call_id = 42578`
- `unique_contiguous_ids = true`
- `sqlite_quick_check = "ok"`
- `actual_exit_code = 0`

These support a terminal finite non-hit run, not a crashed or partially
unaccounted run.

The validation ledger has two numerical failures, both explicitly preserved as
pre-stabilization failures. The validation denominator includes them; they are
not silently removed.

## 3. Probability and Hessian pipeline

The main numerical pipeline is the correct one for the registered search.

In `numerics.py`, `inclusion_derivatives(k)` computes inclusion principal
minors `det K_A` and their first and second derivatives. The Hessian then
passes those inclusion-probability jets through the upper Boolean-lattice
Mobius transform:

```text
p, p1, p2 = (mobius(a, n) for a in (q, q1, q2)).
```

The entropy Hessian is then assembled from full event probabilities:

```text
h = -einsum(1+log(p), p2) - (p1.T/p) @ p1.
```

Thus the optimized objective is based on inclusion-minor derivatives followed
by Boolean Mobius inversion to full events. It is not using principal minors
as event probabilities.

The complement-stabilized branch has the correct orientation and derivative
signs. It computes events for `I-K` when `trace(K)>n/2`, then maps

```text
p_K(S) = p_{I-K}(S^c).
```

Since the kernel direction for `I-K` is `-V`, the first derivative changes
sign and the second derivative does not:

```text
p  = p[::-1]
p1 = -p1[::-1]
p2 = p2[::-1]
```

This sign convention is correct.

The signed-determinant event formula is not the source of the optimized
Hessian. It is used as a consistency diagnostic in `hessian(k)` and as an
alternate directional check in `signed_directional(k,v)`. A diagnostic
failure can reject an evaluation, but it does not replace the Mobius-based
probability pipeline.

## 4. Best value, alternate check, residual, and chord evidence

The best recorded object does not meet the promotion gate.

Best formal Hessian value:

```text
5.930937647366978e-15
```

Promotion threshold:

```text
1e-6
```

Alternate directional formula:

```text
8.881784197001252e-16
```

Eigenvector residual:

```text
6.0037609269151225e-15
```

The best Hessian value is many orders of magnitude below the promotion
threshold and is at the same scale as the eigenvector residual. Treating it as
floating-point zero is appropriate.

The two recorded feasible chord probes at the best object were negative:

```text
t = 0.00047033894450213036, delta = -1.138755756358023e-12
t = 0.0018813557780085215,  delta = -2.9154478831117103e-10
```

These support "no numerical candidate promoted" for this finite batch. They do
not support, and the result file does not claim, a universal exclusion theorem
for general real-symmetric strict-interior kernels.

## 5. Resource, wall-clock, and process terminal state

The configured formal resource limits are within the preregistered P2-01
limits:

- numerical threads: `1` (at most `3`)
- memory limit: `12 GiB`
- wall-clock ceiling: `5400` seconds (`90` minutes)
- GPU disabled in the numerical source

The terminal evidence is consistent:

- `process_exit.json` records exit code `0`.
- Program wall time: `705.8111944198608` seconds.
- Supervisor wall time: `705.912392616272` seconds.
- Both are well below the `5400` second ceiling.
- The final audit reports the worker and supervisor PIDs no longer existed.
- The result file reports no surviving matching process rows.

Therefore there is no live job to resume from this committed evidence.

## Conclusion

The fixed commit supports exactly the stated finite-batch conclusion:

```text
INCOMPLETE_FINITE_BATCH_COMPLETE
```

It gives a bounded, terminal, correctly accounted non-hit over the registered
P2-01 search space. It does not certify a counterexample, and it does not prove
a general theorem excluding the real-symmetric domain.
