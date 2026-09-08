# D10-B3 run log

AUTHOR LOG, 2026-09-08.

Scope observed:

- Work directory: `C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`.
- Written only under `research/R3/deepening_10h/path_affine_chords/general_family/jet_hessian/`.
- No server was used.
- `C:\canglan\` was not accessed, searched, traversed, or modified.
- No subprocess or other agent process was stopped.
- The implementation sets `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, and `NUMEXPR_NUM_THREADS=1`.

## Files produced

- `derivation.md`
- `jet_hessian.py`
- `results/direct_validation.json`
- `results/low_dim_hessian.json`
- `results/curvature_scout.json`
- `results/frozen_n93_rank2_stability.json`
- `results/summary.json`
- `verdict.md`

## Commands and outcomes

1. Read `math-theorem` instructions and relevant existing notes:
   `general_family/derivation.md`, `general_family/theorem.md`, and
   `next_structures/sparse_schur/path_schur.py`.

2. Python availability probe:
   initial PowerShell here-doc syntax attempt failed before running Python
   (`ParserError`, exit code 1, no file effect).  Retried with `-c`; Python
   version was `3.12.14`.

3. Direct exact-event validation:

   ```text
   python jet_hessian.py --validate-only
   exit code: 0
   status: PASS
   ```

   Summary:

   - n=5 rank2, 32 events, max abs jet-vs-Möbius diff:
     `5.773159728050814e-15`;
   - n=6 full-rank, 64 events, max abs diff:
     `1.7763568394002505e-15`;
   - n=7 full-rank, 128 events, max abs diff:
     `1.0694570229397016e-15`.

   The comparison uses exact-event Möbius derivatives from
   \(p_A=\sum_{T\subseteq A^c}(-1)^{|T|}\det K_{A\cup T}\).  Central finite
   differences are included only as an extra high-precision sanity check.

4. Low-dimensional full Hessian by polarization:

   ```text
   python jet_hessian.py --low-dim-only
   exit code: 0
   status: FINITE_HESSIAN_BUILT
   ```

   Summary:

   - n=5 finite Hessian max eigenvalue: `-4.343375596856688`;
   - n=6 finite Hessian max eigenvalue: `-4.374429104368119`.

   These are finite examples only, not a theorem.

5. Initial float curvature scout before the quotient fix:

   ```text
   python jet_hessian.py --scout-only --n-min 5 --n-max 100 --trials 24 --seed 20260908
   exit code: 0
   status: SCOUT_COMPLETE
   ```

   Summary:

   - n range: 5..100;
   - buckets: rank2 and full-rank;
   - total evaluations: 4608;
   - float positive normalized-H2 signals above `1e-10`: 13;
   - largest float signal: n=93, rank2, trial 15,
     \(H''_{\rm float}=184.7448188718266\), normalized by
     \(\|\dot K\|_F^2\) as `303866.09442688845`;
   - closest-to-zero float negative record before high-precision screening:
     n=34, rank2, normalized `-3.2491091342052347`.

   This run used the legacy final normalization \(T/Z=T\cdot Z^{-1}\) through
   a reciprocal jet.  It is preserved in this log as a failed attempt; its JSON
   was later overwritten by the corrected stable scout, while the first false
   positive is preserved in `results/frozen_n93_rank2_stability.json`.

6. Bug diagnosis and implementation fix:

   The legacy quotient path formed \(Z^{-3}\) in float.  For the frozen n=93
   case, \(Z\approx1.34\times10^{118}\), so \(Z^{-3}\) underflowed to zero.
   I replaced the final quotient by the recurrence obtained from \(A=CB\):

   ```text
   C0 = A0/B0
   C1 = (A1 - B1*C0)/B0
   C2 = (A2 - 2*B1*C1 - B2*C0)/B0
   ```

   This avoids inverse cubes and keeps the second derivative of \(T/Z\) stable.

7. Frozen n=93/rank2 replay and stability check after the fix:

   ```text
   python jet_hessian.py --check-frozen-candidate
   exit code: 0
   status: LEGACY_FLOAT_POSITIVE_REJECTED_BY_STABLE_ARITHMETIC
   ```

   Frozen signal:

   - n=93, bucket rank2, trial 15, seed `20260908`;
   - support indices: `[45, 85]`;
   - stable float \(H''\): `-0.007024918933640795`;
   - legacy inverse-jet \(H''\): `184.7448188718266`;
   - Decimal precision-110 \(H''\):
     `-0.00702491893361558273128976293139382722201050261979941592193012364299709517500299474586226424341835016175096945`;
   - normalized Decimal \(H''/\|\dot K\|_F^2\):
     `-11.55450362862002226211033003`;
   - smallest recorded step \(h=0.0005\) midpoint gap:
     `-8.781148687899363838623042762168288142433835571242206376200672697335265296646365E-10`.

   The symmetric chord second differences from Decimal value-only DP converge
   monotonically to the same negative \(H''\) ratio, so this is not a positive
   candidate.

   Exact rational feasibility certificate for the frozen decimal parameters:

   - interpreting the saved float strings as exact rationals,
     exact tridiagonal LDL pivots certify \(P-4I\succ0\);
   - exact tridiagonal LDL pivots certify \(50I-P\succ0\);
   - hence \(1/50\le\lambda(S)\le1/4\), so the strict DPP margin is at least
     `1/50`.

8. Corrected stable float curvature scout:

   ```text
   python jet_hessian.py --scout-only --n-min 5 --n-max 100 --trials 24 --seed 20260908
   exit code: 0
   status: SCOUT_COMPLETE
   ```

   Summary:

   - n range: 5..100;
   - buckets: rank2 and full-rank;
   - total evaluations: 4608;
   - positive stable-float normalized-H2 signals above `1e-10`: 0;
   - global max / closest-to-zero normalized curvature:
     n=34, rank2, trial 8, `-3.2491091342052325`.

   This is the current `results/curvature_scout.json`.

9. Summary file generated from existing result JSON:

   ```text
   results/summary.json
   status: PASS_STABLE_FLOAT_NO_POSITIVES
   ```

10. Syntax check:

   ```text
   python -m py_compile jet_hessian.py
   exit code: 0
   ```

## Interpretation of the n=93 jump

The n=93 jump is now classified as numerical pathology in the legacy float
second derivative accumulator, not as a structural transition.  The Decimal
decomposition shows

\[
(\log Z)''\approx0.2082391792394403,\qquad
(T/Z)''\approx0.2152640981730559,
\]

so the true \(H''\) is their small negative difference.  The stable float
quotient gives the same sign; the legacy inverse-jet path computed the second
derivative of \(T/Z\) with the wrong sign and magnitude.

The absence of positive records for n<93 is not evidence for a threshold.  The
corrected same-scope scout produced no positive records anywhere in n=5..100,
but this remains finite evidence rather than a theorem.
