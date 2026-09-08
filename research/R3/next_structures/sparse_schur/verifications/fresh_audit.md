# Fresh audit of NS-1 sparse Schur path route

STATUS: CORRECT

This is a fresh cross-check of the scoped NS-1 claim only: an exact-event entropy evaluator for positive definite tridiagonal, path-sparse \(L\)-ensemble kernels, together with finite rational validations. It does not certify a real R3 counterexample, generic sparse-\(K\) paths, arbitrary trees, arrowheads, all low-treewidth kernels, or affine marginal-\(K\) chord closure.

## Files read

- `research/R3/problem.md`
- `research/R3/next_structures/sparse_schur/route_note.md`
- `research/R3/next_structures/sparse_schur/path_schur.py`
- `research/R3/next_structures/sparse_schur/evidence.md`
- `research/R3/next_structures/sparse_schur/validation.json`

No server was used. No sub-agent was spawned. No `C:\canglan\` path was accessed.

## Source-level checks

### 1. Exact-event semantics

CORRECT. The route states the strict-kernel \(L\)-ensemble atom formula
\[
p_K(S)=\det(I-K)\det L_S=\det(L_S)/\det(I+L)
\]
in `route_note.md:58-62`. This is an exact atom formula, not an inclusion-probability shortcut.

The direct validation path independently computes exact atoms from the marginal kernel by Möbius inversion:
\[
p_K(S)=\sum_{T\subseteq S^c}(-1)^{|T|}\det K_{S\cup T},
\]
as stated in `route_note.md:155-170` and implemented in `path_schur.py:234-251`. This matches the problem boundary in `research/R3/problem.md`, where \(\det K[S,S]\) is only an inclusion probability.

### 2. Selected-run unique decomposition

CORRECT. For a tridiagonal path \(L\), any selected set \(S\) decomposes uniquely into maximal contiguous selected runs. Gaps in \(S\) remove the corresponding path vertices, so \(L_S\) is block diagonal after permutation, with one tridiagonal interval block per selected run. This is exactly the factorization claimed in `route_note.md:64-76`.

The implementation `path_weight` scans a mask left to right, starts a run at the first selected vertex, advances to the maximal selected suffix, multiplies by `kappa[start][end]`, and resumes after the run (`path_schur.py:169-181`). This is the unique selected-run decomposition, not an orbit or group-count compression.

### 3. Continuant indexing

CORRECT. The route's one-based recurrence
\[
\kappa(a,b)=d_b\kappa(a,b-1)-e_{b-1}^2\kappa(a,b-2)
\]
with \(\kappa(a,a-1)=1\) appears in `route_note.md:78-88`.

The zero-based code initializes `previous2 = 1`, `previous1 = diagonal[start]`, stores `kappa[start][start]`, and for `end=start+1..n-1` uses
`diagonal[end] * previous1 - edge[end - 1] ** 2 * previous2`
(`path_schur.py:148-161`). This is the same continuant recurrence with the correct edge \(e_{end-1}\) between `end-1` and `end`.

### 4. \(Z/T\) dynamic program, prefix length, and empty prefix

CORRECT. The recurrence in `route_note.md:90-120` splits subsets of the first \(m\) vertices into either vertex \(m\) absent, or a last selected run \([a,m]\) preceded by an absent vertex \(a-1\) when \(a>1\).

The implementation uses zero-based prefix lengths:

- `z[0]=1`, `t_log[0]=0` in `path_schur.py:199-201`;
- absent last vertex contributes `z[length - 1]`, `t_log[length - 1]` in `path_schur.py:205-207`;
- for a last run `start..end`, `prefix_len = 0 if start == 0 else start - 1` in `path_schur.py:208-216`.

This correctly represents the route-note convention \(Z_{-1}=Z_0=1\), \(T_{-1}=T_0=0\) from `route_note.md:112-114`: in zero-based form, both "run starts at the first vertex" and "one absent separator before the run with no earlier prefix" map to the same empty prefix weight one.

### 5. Entropy formula

CORRECT. With event weights \(w_S=\det L_S\) and \(Z=\sum_S w_S=\det(I+L)\),
\[
H=-\sum_S \frac{w_S}{Z}\log\frac{w_S}{Z}
=\log Z-\frac1Z\sum_S w_S\log w_S.
\]

This is the route formula `H(K) = log Z_n - T_n/Z_n` in `route_note.md:116-120`, and the code computes `z_dec.ln() - t_log[n] / z_dec` in `path_schur.py:220-221`.

The implementation's logarithms are Decimal diagnostics, not outward-rounded sign certificates. That limitation is explicitly stated in `route_note.md:151-153` and `evidence.md:163-164`, so it is not a critical gap for the scoped evaluator/prototype claim.

### 6. SPD / Sylvester certificate

CORRECT for the scoped tridiagonal \(L\) family. The route uses exact leading continuants and Sylvester's criterion in `route_note.md:138-149`. The implementation computes the same leading continuants in `path_schur.py:128-145`; `path_entropy_dp` rejects inputs whose leading minors are not all positive and also checks all interval determinants are positive (`path_schur.py:191-197`).

For SPD \(L\), \(K=L(I+L)^{-1}\) has eigenvalues \(\mu/(1+\mu)\in(0,1)\), so it is a strict real positive contraction. This is the correct certificate for the path-sparse \(L\)-ensemble setting.

### 7. Complexity

CORRECT for reduced path entropy evaluation. There are \(n(n+1)/2\) interval determinants and the DP loops over `(length,start)` pairs once (`path_schur.py:203-216`), so arithmetic work is \(O(n^2)\) after interval preparation. The code records `state_count = n * (n + 1) // 2` and `full_events = 2**n` in `path_schur.py:222-228`.

The direct Möbius validator is intentionally exponential and capped at \(n\le8\) (`path_schur.py:259-266`). It is validation machinery only, not the reduced evaluator.

### 8. Why affine marginal-\(K\) chords do not close

CORRECT as a limitation. The path recursion applies to kernels of the form
\[
K=L(I+L)^{-1}
\]
where \(L\) is path-sparse tridiagonal. R3 concavity chords are affine in marginal \(K\)-space:
\[
K_t=(1-t)K_0+tK_1.
\]

The inverse map \(K\mapsto L=K(I-K)^{-1}\) is nonlinear, and tridiagonal sparsity of \(L\) is not preserved by generic affine averaging in \(K\). The route explicitly states this blocker in `route_note.md:207-229`, so it does not falsely claim to be a complete chord-gap evaluator.

## Reproduced author self-test

Command:

```powershell
Set-Location -LiteralPath 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\R3\next_structures\sparse_schur\path_schur.py' --self-test --precision 90
```

Exit code: `0`.

Observed denominator and result:

- `heterogeneous_path_n6`: `events_checked = 64`, `mismatch_count = 0`, `mobius_sum = 1/1`, `l_ensemble_sum = 1/1`, `entropy_abs_diff = 4E-89`.
- `heterogeneous_path_n8`: `events_checked = 256`, `mismatch_count = 0`, `mobius_sum = 1/1`, `l_ensemble_sum = 1/1`, `entropy_abs_diff = 2E-89`.
- `n12_smoke`: `state_count = 78`, `full_events = 4096`, and `Z == det_I_plus_L` exactly.

This matches `validation.json:2-50` and the evidence summary in `evidence.md:61-111`.

## Fresh independent temporary check

I ran one additional heterogeneous rational path with \(n=7\), different from the author's \(n=6\) and \(n=8\) cases. The check was executed inline with `PYTHONDONTWRITEBYTECODE=1`, so no temporary validation file was written into the author directory.

Fresh case:

```text
diagonal = [4/3, 5/4, 7/5, 9/7, 11/8, 13/9, 17/11]
edge     = [1/10, -1/11, 1/12, 1/13, -1/14, 1/15]
```

Command:

```powershell
Set-Location -LiteralPath 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "<inline n=7 direct_validation_case>"
```

Exit code: `0`.

Observed denominator and result:

- `events_checked = 128`;
- `mismatch_count = 0`;
- `mobius_sum = 1/1`;
- `l_ensemble_sum = 1/1`;
- `entropy_abs_diff = 3E-89`;
- `spd_by_leading_continuants = true`;
- leading continuants:
  `4/3`,
  `497/300`,
  `139653/60500`,
  `540866069/182952000`,
  `200418307379/49470220800`,
  `48975922647709/8390910528000`,
  `4500864088170097/499958418960000`.

This directly checks all \(2^7=128\) exact atoms by Möbius inversion against the independent path-run \(L\)-ensemble formula.

## Critical-gap assessment

No critical gap was found in the scoped claim.

The route is correct as a path-sparse \(L\)-ensemble exact-event entropy reduction and prototype validation. The author also correctly marks the non-covered parts as HOLD or limitations:

- generic sparse marginal-\(K\) paths are not solved;
- arbitrary tree-sparse \(L\) is not solved;
- arbitrary arrowheads are not solved;
- affine marginal-\(K\) chords are not closed inside path-sparse \(L\);
- finite tests are not elevated to a theorem about all real DPPs.
