# D10-B4 run log

AUTHOR STATUS: REVISED_AFTER_FIRST_AUDIT, pending independent re-verification.

## Scope

- Work unit: D10-B4 analytic curvature for the fixed-beta path-affine family.
- Writable directory:
  `research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/`.
- No subagents used.
- No remote machine used.
- No dependency installation.
- No filesystem access to the forbidden legacy path.

## Inputs read

- `AGENTS.md`
- `research/R3/deepening_10h/problem.md`
- `research/R3/deepening_10h/hazards.md`
- `research/R3/deepening_10h/lemma_ledger.md`
- `research/R3/deepening_10h/path_affine_chords/general_family/theorem.md`
- `research/R3/deepening_10h/path_affine_chords/general_family/derivation.md`
- `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/derivation.md`
- `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/jet_hessian.py`
- `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/results/summary.json`
- `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/verifications/anomaly_results.json`
- `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/verifications/fresh_audit.md`
- `research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/verifications/fresh_audit.md`

## Commands

1. Failed because the Windows `python` app alias was not a usable interpreter:

```text
python research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/weak_coupling_sanity.py
```

Exit code: `1`.

2. Failed because the first sanity script draft wrote
   `weak_coupling_sanity.py/results/...` instead of
   `analytic_curvature/results/...`.

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/weak_coupling_sanity.py
```

Exit code: `1`.  This was a script-path bug, not a mathematical failure.

3. Passed after the output-path fix:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/weak_coupling_sanity.py
```

Exit code: `0`.

Output:

- `results/weak_coupling_sanity.json`
- status: `PASS`
- beta=0 diagonal formula vs O(n²) jet, \(n=3,5,8,12\):
  maximum absolute error `3.9968028886505635e-14`
- small nonzero beta cases, \(n=3,5,8,12\), eps in
  `{1e-4, 1e-3, 1e-2}`: all checked \(H''<0\)
- denominator: 4 beta=0 checks and 12 small-coupling deterministic checks
- threads: BLAS/OpenMP-related variables set to `1`

4. First non-author audit of `analytic_curvature/` returned `INCORRECT` for one
   local false statement in Theorem 1 and requested boundary clarifications.
   The verifier file was read but not modified.  Author files were revised to:

   - make the \(-4\|\delta\|^2\) bound non-strict and record the equality
     condition \(\delta_i\ne0\Rightarrow\tau_i=1/2\);
   - retain \(H''<0\) for every nonzero \(\delta\);
   - assume \(0<\eta<1/a-1/b\) for the nonempty/non-degenerate version;
   - state that connectedness means graph-connectedness of each \(L\), while
     the parameter set can split into sign chambers and two \(\tau\) branches.

Sanity rerun pending after this revision.

5. Passed after the theorem/verdict/decomposition boundary revision:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/weak_coupling_sanity.py
```

Exit code: `0`.

Output remains:

- `results/weak_coupling_sanity.json`
- status: `PASS`
- beta=0 formula vs O(n²) jet max absolute error:
  `3.9968028886505635e-14`
- all 12 deterministic small-coupling cases checked \(H''<0\)

6. Final rerun after replacing the remaining ambiguous phrase "connected
   subfamily" by "graph-connected path subfamily":

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/weak_coupling_sanity.py
```

Exit code: `0`; status remained `PASS` with the same denominator and max error.

## Mathematical result

The main new result is qualitative, not numerical: for every fixed dimension
and every compact \(\tau\)-box inside \((0,1)^n\), sufficiently small nonzero
path couplings preserve the strictly negative product-Bernoulli entropy
Hessian.  Adding a nonempty diagonal separation margin
\(0<\eta<1/a-1/b\) gives a heterogeneous strict positive-contraction family
whose individual \(L\)-path graphs are connected.

The decomposition note also isolates the only possible global sign-flip source
as the residual

\[
-\operatorname{Cov}(\ell,B)
-\mathbb E\left[(\ell-\mathbb E\ell)(A-\mathbb EA)^2\right].
\]

No positive candidate is claimed.
