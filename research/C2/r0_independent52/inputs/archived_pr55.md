# PR55: scoped algebra and partial computation archive

Final source head: `12798ccc1afdff007a2deec3f49baf26755d1a93`. Merge: `43d8fd24af560afaa34b1ec8e7c7dd053e691603`. All 59 files are under `research/C2/lambda_zero52/`. This is a **PARTIAL evidence archive**, not acceptance of an r=0 or full-r positivity theorem. [Bounded result](../../research/C2/lambda_zero52/RESULT.md), [final status](../../research/C2/lambda_zero52/STATUS.md), and [original issue52 input](../../research/C2/lambda_zero52/inputs/frozen_issue52.md).

## Accepted algebra, with separate review scopes

For the frozen Lambda-zero family, `|mu|,|nu|,|r|<1`, `0<u<1`, the six physical direction coordinates are held fixed in u. The [independent analytic formula review](../../research/C2/lambda_zero52/formula_review/FORMULA_REVIEW.md) verifies all eight atom formulas, full Fisher/acceleration, `M=Fmat'+Q`, and the initial negative Hessian `diag(v,w,4,0,0,0)`. In particular, the log-product derivatives are supplied analytically by that review; the machine run did not independently derive this link.

The [structural note](../../research/C2/lambda_zero52/structure/STRUCTURE.md) has a [first nonauthor review](../../research/C2/lambda_zero52/structure_review/REVIEW.md), [separate C3 second](followon/pr55_structure_second/review_report.md), and [exact source-supplement closure](followon/pr55_structure_second/source_delta_review.md). It gives an invertible pointwise congruence after the fixed-direction derivative, a positive two-dimensional eliminated block and an explicit four-dimensional Schur complement Rstar. The negative-vector back-map is retained. With x=T zeta, `M_red=T^{-T} M T^{-1}`, `det T=8u^4a^2b^2`, and

`det M=16 n1 n2 u^12 a^5 b^5 v w det Rstar`.

The prefactor is positive in the open domain. This identity supplies no remaining determinant sign by itself. The [single seed](../../research/C2/lambda_zero52/structure/POSITIVE_SEED.md) at `mu=nu=r=0,u=1/2` has a [separate nonauthor review](../../research/C2/lambda_zero52/structure_review/POSITIVE_SEED_REVIEW.md): its scaled Rstar has strict row margins `(10068,88320,88320,40053)`. A single seed cannot establish global nonvanishing.

## Actual bounded run and preserved failure

The original arithmetic window was 11:22:28–12:07:28 UTC on 2026-09-09. Three sequential author processes finished at 11:54:46, 12:00:41 and 12:03:33; at most one arithmetic process/thread ran, with 16 GiB and no GPU. [Run ledger](../../research/C2/lambda_zero52/resume/RUN_LEDGER.md) and [original computation report](../../research/C2/lambda_zero52/compute/REPORT.md).

Implemented event/jet/Fisher and denominator checks passed within their stated dependency scope. Both original determinant stages then failed while serializing a SymPy Integer, after saving their first minor. Wrapper exit0 is not stage success. The recorded repair used the saved Rstar matrices and the remaining original time to obtain second, third and fourth principal determinants in both cases. A subsequent exact integer coefficient transformation used only the saved factors. Original failures and checkpoints remain intact; no new 45-minute allocation or duplicated reconstruction occurred.

## r=0 candidate remains INCOMPLETE

The recorded r=0 residual P has degrees `(4,4,16)` and proposed identity

`det Rstar=(1-mu^2)^2(1-nu^2)^2 P/[2(1-u^4)^5]`.

The positive-orthant substitution `mu=(X-1)/(X+1)`, `nu=(Y-1)/(Y+1)`, `u=U/(1+U)` records 389 positive nonzero coefficients, minimum192. The [fresh r=0 first review](../../research/C2/lambda_zero52/r0_review/REVIEW.md) accepts the domain, sign and inertia implications **conditionally**, but did not independently reconstruct `Rstar -> determinant -> P -> Q`. Its clock check was eight seconds after the hard deadline; it launched no arithmetic.

Accordingly, r=0 is **INCOMPLETE**, not ERROR and not an accepted theorem. C3's reserved certificate second stays behind the unmet first gate. Source identity and JSON syntax checks cannot supply that missing independent arithmetic. The archive passed byte/public-field checks for59files and JSON parsing for21files; those are packaging checks only.

The full-r transform records6415positive and146negative coefficients. Mixed coefficients establish neither a negative value nor a global positive sign. No exact negative M direction or entropy counterexample was produced.

[Issue52](https://github.com/randomcat4/dpp-entropy-tools/issues/52) remains open: a future authorized bounded run would need an independent reconstruction of the frozen r=0 certificate chain; full r separately needs a domain certificate or an exact negative point/direction. No further arithmetic is authorized by this archive. Negative radial M would refute a stronger sufficient method, not automatically entropy concavity.
