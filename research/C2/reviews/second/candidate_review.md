CORRECT

# Independent review: I05-C2-20260909

## Binding

- Local review root: `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2`.
- Frozen local commit: `81b0123b7c1bcb4495e99d5707bf2388314f3bbf`.
- Reviewed files at that commit:
  - `research/C2/frozen_statement.md`, blob `9b3cc75260c43abf41201b36e80fe4cf8f7084d1`.
  - `research/C2/frozen_supplement.md`, blob `dc77c9507a03d67b387cb350a8ec42316d0d10f3`.
  - `research/C2/proof.md`, blob `0a8cf09210aeddbc03f355143f638069ccfbbe1e`.
  - `research/C2/mechanism/proof.md`, blob `70935232da868f66f70338123ad1907d391c2275`.
  - `research/C2/main_check.json`, blob `1b9ed5b4385113a8c9d357fb1f74e06017cdb4f0`.
- Note on the supplied "supplement blob": `70935232da868f66f70338123ad1907d391c2275` is the blob of `research/C2/mechanism/proof.md`; the short supplemental statement file has the separate blob above.

Line references below are to the frozen commit contents. I did not read other review reports and did not modify the parent repo.

## Verdict

I find no critical gap in the three frozen auxiliary claims, the supplemental anisotropic inequality, or the fixed-B asymptotic statement. The proof establishes only the restricted claims it states; it does not prove global concavity or resolve the moderate-spectrum residual regime.

## Main proof checks

1. Support and event formulas (`proof.md` lines 5-27). The L-ensemble reconstruction, the empty/singleton/pair/triple formulas, and the affine legal-step condition are valid for arbitrary real symmetric directions. The derivations use polynomial or congruence arguments, not a commutation assumption on `V`. Events of size greater than three vanish identically, and the remaining 26 events are strictly positive in the strict face, so no derivative of `log 0` is used.

2. Rare-event logarithm cancellation (`proof.md` lines 29-47). The identity `sum_S (3-|S|) p_S'' = 0` follows from `E(3-|X|)=3-tr A`, affine in the path parameter. Therefore after writing `p_S=e^(3-|S|)g_S` at a fixed center, the coefficient of `log e` cancels exactly. This keeps empty, singleton, pair, and top events; it is not a limit argument and does not discard rare-event accelerations.

3. Frame inequality and constants (`proof.md` lines 49-64). The certificate proves `G-D/22` positive definite by exact rational Sylvester minors, hence `Q(X) >= ||X||_F^2/22` for all real symmetric `X`. The constant `1/22` is a certified lower bound, not asserted to be the exact minimum frame constant. It applies to all six symmetric coordinates, so noncommuting perturbations are covered.

4. Upper-face compensation cone (`proof.md` lines 66-127). With `A=I-eB`, `I<=B<=2I`, and `delta=2e`, all eigenvalues of `A` lie in `[1-delta,1)`. In an eigenbasis of `A`, the derivative formulas for `DC[V]` are polynomial differential identities and remain valid at repeated eigenvalues. The bound `||DC[V]+V||_F<=4delta||V||_F` gives `||DC[V]||_F>=||V||_F/2` for `delta<=1/8`; together with `p_ij<=delta||w_ij||^2` and the frame bound this yields the pair Fisher lower bound `||V||_F^2/(176e)`. The logarithmic acceleration bound `5600||V||_F^2` includes every supported layer. Since `e<=1/1971200` makes `5600<=1/(352e)`, the claimed `H''<=-||V||_F^2/(352e)` follows uniformly for every symmetric `V`, including `V` depending on `B,e`.

5. Low-event derivative injectivity (`proof.md` lines 129-144). If all pair derivatives vanish, the frame inequality forces `DC[V]=0`. The identity `DC[V]=d[s(A^{-1}-I)-A^{-1}VA^{-1}]` then gives `V=sA(I-A)`, and tracing gives either `V=0` or `tr A=2`. In the latter case, `p_empty'=-2s det(I-A)`, so adding `p_empty'=0` excludes all nonzero pair-null directions. This covers arbitrary strict `A`, including repeated eigenvalues.

6. Exceptional pair-null direction (`proof.md` lines 146-157). Under `tr A=2` and `V=sA(I-A)`, `V` is a polynomial in `A`, so simultaneous diagonalization is legitimate. The affine eigenvalue path gives `c_i'=0` and `c_i''=-s^2 c_i(lambda_i^2+mu_j^2+mu_k^2)<0`. Since every pair cross product is nonzero, each pair has `p_ij''<0`, and because `0<p_ij<1`, the term `-p_ij'' log p_ij` is strictly negative. No sign is inferred for other cardinality layers.

## Supplemental mechanism checks

1. Anisotropic theorem (`mechanism/proof.md` sections 1-5). For any fixed full-spark real `n x 3` isometry, the definitions of `L` and the true `kappa` are finite and positive. The proof of `kappa>0` from four rows is sound: after an invertible coordinate change, the first three pair measurements force the diagonal entries of the symmetric form to vanish, and the fourth row, whose three coordinates are nonzero by full spark, forces all off-diagonal entries to vanish.

2. The anisotropic bound
   `H'' <= [-kappa/(4delta)+16L+18log(1/rho)+4] ||V||_F^2`
   follows from the exact cancellation formula, the layerwise logarithm bounds, and the pair Fisher lower bound. The constants check out: the logarithmic acceleration coefficients are bounded by `16L+18log(1/rho)+4` for `delta<=1/8`, and the Fisher term is at least `kappa||V||_F^2/(4delta)`. This covers arbitrary symmetric, noncommuting `V` and `R`; it does not cover all small eigenvalue-ratio regimes unless `delta log(1/rho)` is below the stated threshold.

3. Fixed-B asymptotic (`mechanism/proof.md` section 6). For fixed positive definite `B`, the expansion
   `H''=-J_B(V)/e+C_B(V)+O(e)||V||_F^2`
   has the correct signs in the pair Fisher constant term, singleton Fisher term, top-layer Fisher term, and scaled-log acceleration term. The stated remainder is uniform for `B` in compact subsets of the positive definite cone because the finitely many scaled probabilities are then uniformly separated from zero and all coefficients are analytic. The statement correctly excludes uniformity as `lambda_min(B)` tends to zero.

## Independent computation

Artifacts written in this review directory:

- `independent_check.py`
- `independent_check.json`
- `run_record.json`
- `independent_check.stdout`
- `independent_check.stderr`
- `representative_noncommuting_top_excess.json`

The actual recorded run was:

```text
cd /root/i05-seven-fronts-20260909/C2/review_second && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /root/i05-seven-fronts-20260909/C2/.venv/bin/python independent_check.py
```

Recorded exit code: `0`. Recorded Python PID: `165137`. Versions: Python `3.12.3`, SymPy `1.14.0`, NumPy `2.5.3`, mpmath `1.3.0`. Thread limits in the run record are all `1`.

The independent script rebuilds `U` from the displayed rational matrix, not from the original `main_check.py`. It verifies:

- `U^T U=I`, all ten triple determinants are nonzero, and all pair cross products are nonzero.
- The exact event formulas agree with inclusion-exclusion for all 32 events on a noncommuting rational fixture; the six events of size greater than three are zero and the 26 supported probabilities are positive.
- `sum p=1`, `sum p'=0`, `sum p''=0`, and `sum(3-|S|)p_S''=0`.
- `G-D/22` has all six leading principal minors positive; the trace-inverse lower bound is greater than `1/22`; `min gamma_S/4^|S|=441/1092025>2^-14`; the cone radius recomputes as `1/1971200`.
- A rational exceptional-direction sample with `tr A=2`, `V=A(I-A)` has all pair first derivatives zero, all pair second derivatives negative, and nonzero empty derivative.
- A noncommuting fixed-B asymptotic fixture reproduces `J=1.0625237678169856...` and `C_B=-3.3802985464495...`; the sampled remainders divided by `e` stay bounded for `e=10^-2,10^-3,10^-4`.
- The optional `representative_noncommuting_top_excess.json` was independently recomputed: all 26 probabilities, first derivatives, and second derivatives match exactly; the legal-step Sylvester checks are positive; the full central entropy chord is negative, and its half matches the file's `chord_interval` convention.

No formal proof assistant verification is claimed or needed for this review verdict.
