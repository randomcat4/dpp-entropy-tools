# S1 round-2 independent review report

Status: **CORRECT for the frozen finite B1 baseline checks at n=6 and n=8, and CORRECT for the finite one-complex-affine-edge concavity lemma.**

This report is scoped to the first independent round-2 unit. It does not certify any entropy-rate sign, does not audit a later rate certificate, and does not turn the finite negative B1 diagnostics into a positive or negative resolution of the scalar entropy-rate conjecture. I did not use phase or rate drafts before the B1 baseline replication.

## Audited public/frozen objects

- Frozen round-2 theorem file: `research/S1/round2/frozen_theorem_v1.md`.
- Baseline candidate: `research/S1/round2/baseline_candidate.json`, candidate id `S1-R2-B1`.
- Author B1 result used only after my independent run: `research/S1/round2/main/baseline_jet_result.json`.
- One-edge proof: `research/S1/round2/main/single_complex_edge.md`, frozen in local main commit `85150fd`.

## Independent B1 reconstruction

I reconstructed the scalar Toeplitz DPP directly from the trigonometric symbol

`f_t=p+t dp+sum_k((a_k+t da_k)cos(2πkx)+(b_k+t db_k)sin(2πkx))`

with Fourier coefficients

- `c_0=p+t dp`,
- `c_k=(a_k+t da_k-i(b_k+t db_k))/2`,
- `c_-k=conj(c_k)`.

For exact events I used the determinant with selected rows from `K` and unselected rows from `I-K`. This keeps the non-even center and mixed cosine/sine direction visible; no event derivative cancellation was assumed.

The candidate passes the rational uniform-margin check exactly. The triangle bound gives lower `11/400`, upper `349/400`, hence the claimed margin `11/400` is certified for all `|t|<=1/8`.

The center is not reducible to the old even case. It has nonzero sine coefficients, and the exact phase-cycle invariants are non-real:

- `Im(c1*c1*conj(c2)) = 519/2000000`,
- `Im(c1*c1*c1*conj(c3)) = -1577/100000000`.

The endpoints are also not being silently identified by conjugacy or translation. Their means are `179/400` and `181/400`, so translation/reflection equivalence is already blocked at the diagonal mean level.

## Finite event and jet results

The independent run covered all exact events for n=6 and n=8. For each n it evaluated all `2^n` center events for the full seven-parameter Hessian, and all `2^n` events at `t=-tau,0,+tau` for the finite midpoint gap.

Key independent values:

| window | finite midpoint gap | Hessian max eigenvalue | fixed-direction H'' | Fisher positive term | acceleration term |
|---:|---:|---:|---:|---:|---:|
| n=6 | `-0.000102776762078705` | `-0.0166810202054028` | `-0.0131516066072110` | `0.0121269597920560` | `-0.00102464681515499` |
| n=8 | `-0.000139893195540530` | `-0.0278059605842385` | `-0.0179005660743535` | `0.0164166964267147` | `-0.00148386964763885` |

Here the Fisher number is the positive quadratic form `sum (p'_omega)^2/p_omega`; its contribution to the entropy Hessian is negative. Thus `H'' = acceleration - Fisher_positive`, matching the displayed totals.

The non-even warning is active in the data: the maximum absolute fixed-direction event derivative at n=8 is `0.00285249087448019`, so the old `p'_A(0)=0` shortcut would be false for this unit.

Numerical residuals were small:

- n=8 center probability sum residual: `4.44e-16`;
- n=8 center gradient-sum infinity norm: `9.92e-16`;
- n=8 center event-Hessian-sum infinity norm: `1.11e-15`;
- n=8 maximum determinant imaginary part across the checked event determinants: `3.39e-20`;
- n=8 minimum center exact-event probability: `0.00104690964591555`;
- n=8 maximum event-matrix condition number: `3.13`.

After the independent run, I compared against `main/baseline_jet_result.json`. The n=8 midpoint gap, Hessian maximum eigenvalue, fixed-direction total, Fisher, and acceleration all matched within `1.4e-15`; n=6 finite gap matched within `8.9e-16`. The comparison file records the exact main JSON leaf paths that matched.

## Run record

- Script: `research/S1/round2/review/round2_baseline_review.py`.
- Result JSON: `research/S1/round2/review/round2_baseline_review_result.json`.
- Comparison JSON: `research/S1/round2/review/round2_baseline_comparison.json`.
- Run record JSON: `research/S1/round2/review/round2_baseline_run_record.json`.
- Python: bundled workspace Python, NumPy `2.3.5`.
- Thread environment: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
- Seed: deterministic, no random seed used.
- PID: `37196`.
- Exit code: `0`.
- Script SHA-256: `aeb39573cfa053717c1cceea541cc7cf16e9f57ec8b40da45a36a4a45858c58b`.
- Candidate SHA-256: `5059e4c166db4f39d6b9e8d22c4c75d29707e7e2b9e096f74a29b3ecac3d87e3`.
- Main result SHA-256: `20479ee0e5203cc37039145f02d102def10ba0313446c40004dd6ea10c6bb4b1`.

## One complex affine edge audit

Status: **CORRECT, within the stated finite-kernel scope.**

The proof conditions on an exact outside configuration `gamma` on `R=V\{a,b}`. Since only the unordered pair `{a,b}` varies, the outside exact-event weight depends only on fixed entries and is independent of `t`. The conditional two-point DPP kernel has fixed diagonals and a single affine complex off-diagonal `z_gamma+t v`; this follows from the exact-event Schur complement because the outside block and cross rows are fixed.

For the conditional two-point kernel, the four masses are

- `p11=rs-q`,
- `p10=r(1-s)+q`,
- `p01=(1-r)s+q`,
- `p00=(1-r)(1-s)-q`,
- `q=|z_gamma+t v|^2`.

Differentiating the four-event entropy as a function of `q` gives

- `F'(q)=log((p11 p00)/(p10 p01))<=0`, because `p11 p00-p10 p01=-q`;
- `F''(q)=-(1/p11+1/p10+1/p01+1/p00)<0`.

For a real parameter `t`, `q'=2 Re(conj(z_gamma+t v)v)` and `q''=2|v|^2`, so

`d²/dt² F(q(t)) = F''(q)(q')² + 2|v|²F'(q) <= 0`.

This retains the Fisher term and does not rely on a real gauge, conjugate endpoint shortcut, finite dependence, or mixing. If `v!=0`, each conditional `q_gamma(t)` can vanish at at most one real parameter value; away from that finite exceptional set, the relevant second derivative is strictly negative. Integrating over any nontrivial interval gives strict concavity even if the pointwise second derivative vanishes at isolated degenerate points.

The limitation in the proof is correctly stated: this is a one-edge finite-kernel lemma. It cannot be used to rule out or certify a Toeplitz harmonic direction that moves several kernel entries and possibly diagonal/marginal data at once.

## Boundaries and risks

The B1 finite checks are independent numerical verification of the frozen n=6/n=8 diagnostics and the exact rational margin. They are not interval-log certificates and do not make a rate claim. The full Hessian negativity here is for the seven coefficient coordinates of this finite Toeplitz baseline at the center; it should not be read as a class theorem for all complex centers or all multi-edge perturbations.

No critical gap was found in the audited finite objects.

