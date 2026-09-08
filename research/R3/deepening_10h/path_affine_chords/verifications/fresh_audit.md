# Fresh audit of D10-B / FT-B path-affine chords

STATUS: CORRECT

I am not the FT-B author. I did not revise the frozen claim or the author's files. This report verifies the explicit existence-side certificate for FT-B: exact rational tridiagonal \(L_-,L_0,L_+\) with
\[
\Phi(L_0)=\frac{\Phi(L_-)+\Phi(L_+)}2,\qquad
\Phi(L)=L(I+L)^{-1}.
\]
It does not certify an R3 positive entropy gap.

## Files read

- Frozen FT-B section from `research/R3/deepening_10h/frozen_theorem_v1.md`
- `research/R3/deepening_10h/hazards.md`
- `research/R3/deepening_10h/path_affine_chords/approach.md`
- `research/R3/deepening_10h/path_affine_chords/search_or_algebra.py`
- `research/R3/deepening_10h/path_affine_chords/evidence.json`
- `research/R3/deepening_10h/path_affine_chords/verdict.md`
- `research/R3/deepening_10h/path_affine_chords/run_log.md`

The author script imports the existing NS-1 path validator when rerun; I did not modify that dependency or any author output file.

## Algebraic check

### \(S=(I+L)^{-1}\) transform

Correct. If \(P=I+L\) and \(S=P^{-1}\), then
\[
\Phi(L)=L(I+L)^{-1}=(P-I)P^{-1}=I-S.
\]
Thus the \(K\)-space midpoint identity is equivalent to
\[
S_0=\frac{S_-+S_+}{2}.
\]

### Fixed-beta innovation parameterization

Correct. The script defines a unit lower-bidiagonal \(R\) with subdiagonal \(-\beta_i\) (`search_or_algebra.py:188-205`) and
\[
S(\tau)=R^{-1}\operatorname{diag}(\tau)R^{-T}
\]
(`search_or_algebra.py:208-216`). This is affine in \(\tau\), so \(\tau_0=(\tau_-+\tau_+)/2\) gives \(S_0=(S_-+S_+)/2\).

The inverse precision is
\[
P(\tau)=S(\tau)^{-1}=R^T\operatorname{diag}(1/\tau)R
\]
(`search_or_algebra.py:219-227`). Since \(R\) is bidiagonal, \(P(\tau)\) is tridiagonal; \(L(\tau)=P(\tau)-I\) remains tridiagonal. Adjacent edges are \(-\beta_i/\tau_{i+1}\), so nonzero \(\beta_i\) and positive \(\tau_i\) give a connected path.

The code also checks \(P S=I\), \(\Phi(L)=I-S\), tridiagonality, nonzero adjacent edges, heterogeneous diagonal, leading-continuant SPD, exact K/S midpoint identities, non-L-line status, and exact ranks (`search_or_algebra.py:287-357`).

### SPD and strict DPP feasibility

Correct for the deposited examples. The script certifies \(L>0\) by exact leading continuants (`search_or_algebra.py:175-186`, `search_or_algebra.py:313-316`). For real symmetric tridiagonal \(L\), positive leading principal minors certify SPD by Sylvester's criterion.

Once \(L>0\), \(I+L> I\), hence \(S=(I+L)^{-1}\) has spectrum in \((0,1)\) and \(K=I-S=\Phi(L)\) is a strict real positive contraction. This supplies the FT-B feasibility certificate.

### Heterogeneity condition

The script predicate `len(set(diag)) > 1` checks nonconstant diagonal, not pairwise-distinct diagonal. This is a weak predicate if "heterogeneous" were later interpreted as all diagonal entries pairwise distinct. However the actual n=3, n=4, and fresh n=5 examples have visibly pairwise-distinct listed diagonal entries at every point, so this is not a critical gap for the submitted examples.

### Not an \(L\)-space line

Correct. The evidence records `L_zero_is_endpoint_average = false` and `not_an_L_line = true` for n=3 and n=4, and the fresh n=5 test also returns `not_an_L_line = true`. Thus the construction solves the frozen \(K\)-space midpoint condition rather than confusing it with an \(L\)-space straight line.

## Reproduced author checks

I reran the author construction by importing `search_or_algebra.py` and calling `build_evidence(100)` directly, rather than executing its default CLI writer. This avoided overwriting `evidence.json`.

Command shape:

```powershell
Set-Location -LiteralPath 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "<import search_or_algebra.py; call build_evidence(100); print summary>"
```

Exit code: `0`.

Observed denominator and results:

| case | points | atoms per point | total exact atoms | K midpoint | S midpoint | rank \(K_+-K_-\) | shape/SPD | direct Möbius |
| --- | ---: | ---: | ---: | --- | --- | ---: | --- | --- |
| n=3 | 3 | 8 | 24 | true | true | 3 | pass | 0 mismatches |
| n=4 | 3 | 16 | 48 | true | true | 4 | pass | 0 mismatches |

The reproduced Decimal scout gaps use the frozen sign convention
\[
\Delta=\frac{H(K_-)+H(K_+)}2-H(K_0).
\]
They are:

- n=3: `-0.00045556980402948637966202904966273876636359662215010218795433969502053929872088544141161521326441`
- n=4: `-0.00084150938797292809775272697635216508407540691808349059968484019798488667772598963986582249100154`

Both are negative. No positive R3 gap is certified or suggested by these two examples.

## Fresh n=5 exact triple

The fixed-beta construction naturally generalizes. I tested a new n=5 rational triple:

```text
beta      = (1/5, -2/7, 3/11, -1/6)
tau_minus = (1/34, 1/39, 1/44, 1/49, 1/54)
tau_plus  = (1/47, 1/36, 1/59, 1/41, 1/63)
tau_zero  = (tau_minus + tau_plus)/2
```

Command shape:

```powershell
Set-Location -LiteralPath 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "<import search_or_algebra.py; call analyze_case on fresh n=5 parameters>"
```

Exit code: `0`.

Results:

- `K_midpoint_identity_exact = true`
- `S_midpoint_identity_exact = true`
- `not_an_L_line = true`
- `rank_K_plus_minus = 5`
- `rank_S_plus_minus = 5`
- `all_points_pass_FT_B_shape = true`
- `all_direct_mobius_validations_pass = true`
- three points, `32` atoms per point, `96` exact atoms checked by the validator, `0` mismatches
- Decimal scout gap:
  `-0.00064959413095735400052394645519833847303461738396454721134062942265233439417079719991467459009276`

The n=5 point data also satisfy:

| point | L diagonal | L edges | SPD | connected | heterogeneous | direct Möbius |
| --- | --- | --- | --- | --- | --- | --- |
| minus | `864/25, 2038/49, 5644/121, 99/2, 53` | `-39/5, 88/7, -147/11, 9` | true | true | true | 32/32, 0 mismatches |
| zero | `2022691/50625, 5117017/126175, 3285772/62315, 26477/585, 743/13` | `-936/125, 10384/721, -2009/165, 126/13` | true | true | true | 32/32, 0 mismatches |
| plus | `1186/25, 1951/49, 7387/121, 167/4, 62` | `-36/5, 118/7, -123/11, 21/2` | true | true | true | 32/32, 0 mismatches |

No n=5 blocker occurred.

## Independent n=5 exact-atom check

To avoid relying only on the reused NS-1 validator for the fresh case, I also ran an inline independent exact rational comparison for the same n=5 triple:

- exact atoms from marginal \(K=I-S\) by direct Möbius inversion of inclusion probabilities \(\det K_T\);
- exact atoms from the full \(L\)-ensemble formula \(\det(L_S)/\det(I+L)\).

This second check did not use the path-run factorization. It checked another `96` exact atoms:

| point | events | mismatch count | Möbius sum | L sum | min atom |
| --- | ---: | ---: | --- | --- | --- |
| minus | 32 | 0 | 1 | 1 | `1/154378224` |
| zero | 32 | 0 | 1 | 1 | `38625/7467399898112` |
| plus | 32 | 0 | 1 | 1 | `1/257855724` |

Exit code: `0`.

This confirms the exact-event semantics for the fresh n=5 triple independently of the path entropy DP.

## Gap sign and R3 status

The gap sign convention is correct:
\[
\Delta=\frac{H(K_-)+H(K_+)}2-H(K_0).
\]
All reproduced and fresh scout gaps are negative. Therefore the examples solve FT-B's closure/existence side but do not produce an R3 entropy nonconcavity candidate. Decimal entropy values are scout diagnostics only; no outward-rounded interval certificate is needed because no positive gap is being claimed.

## Critical-gap assessment

No critical gap found for the explicit FT-B existence certificate.

Verified:

- \(S=(I+L)^{-1}\) transformation and \(\Phi(L)=I-S\);
- linearity of \(S(\tau)\);
- inverse precision \(S(\tau)^{-1}=R^T\operatorname{diag}(1/\tau)R\) and tridiagonal \(L\);
- exact n=3 and n=4 rational midpoint identities;
- SPD, connected, and heterogeneous shape conditions;
- non-rank-one perturbations in the deposited examples;
- direct Möbius exact-atom semantics;
- negative gap sign under the correct R3 convention;
- natural n=5 extension with exact checks.

Remaining nonclaims:

- no positive R3 gap;
- no theorem that all path-sparse \(L\) chords are concave;
- no exhaustive classification of FT-B triples;
- no full real-DPP entropy conclusion.

No server was used. No sub-agent was spawned. No `C:\canglan\` path was accessed. No author file was modified.
