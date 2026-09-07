# Fresh v1 verification report

STATUS: CORRECT

Public candidate commit identified for the research/T2 mathematical snapshot: 31143e0925f95e1c05b2165a71c0d541a20be3ef.
Local content snapshot audited in a detached verifier checkout: 8150522d33f7c959e28af9febf11278e1476e6fc.

Scope: fresh-context audit of the frozen finite-block entropy-loss theorem, the anonymous proof, the two explicit boundary families, and the bounded implementation artifacts. I did not assess novelty, priority, entropy-rate claims, scalar stationary consequences, or any global DPP entropy-concavity statement.

## Theorem correctness

Verdict: CORRECT.

Claim A in `research/T2/frozen_theorem_v1.md` lines 14-20 is proved by `research/T2/proofs/construction_v1.md` lines 48-67 and 69-186, then extended to singular kernels at lines 188-205. The block product identity is adequate: finite inclusion probabilities determine the law by inclusion-exclusion, and the product block law has inclusion probabilities equal to the principal minors of the pinched kernel. This gives `L(K)=D(P_K || P_B)>=0` with the needed support condition.

The measurement relative-entropy comparison at `construction_v1.md` lines 69-118 is sound. The compression inverse inequality at lines 80-95 gives operator convexity of `-log` in the required finite-dimensional form. The isometry at lines 103-112 is well-defined for positive definite density matrices, and the calculation of `V* Delta V` gives the classical probability ratios. The quadratic-form step at lines 112-117 therefore proves the stated measured-relative-entropy bound.

The exterior-algebra realization at `construction_v1.md` lines 120-186 is faithful to the DPP marginal-kernel convention in the frozen theorem. The generating-polynomial argument at lines 137-145 recovers the exact finite DPP law, the quasifree entropy calculation at lines 147-155 gives `tr h(K)`, and the cross-entropy calculation at lines 166-182 correctly uses the fact that `K-B` has zero diagonal blocks against block-diagonal functions of `B`. Data processing under occupation measurement then gives `L(K)<=Q(K)` for strict contractions.

The singular limiting step at `construction_v1.md` lines 188-205 is valid for fixed finite dimension. The regularized kernels `K_epsilon=(1-2epsilon)K+epsilon I` and `B_epsilon=(1-2epsilon)B+epsilon I` stay paired by the same pinching, become strict contractions, and converge in both finite DPP entropy and spectral entropy. No inversion at the singular limit is used.

Claim B in `frozen_theorem_v1.md` lines 22-29 is proved by `construction_v1.md` lines 207-235. The spectral expansion at lines 211-218 is legitimate even when `K` has eigenvalues 0 or 1, because only `B` is used inside logarithms with a buffer. The scalar inequality at lines 219-225 extends to endpoint eigenvalues by continuity. The identity at lines 226-229, `sum_i w_ij(a_i-b_j)^2=<v_j,E^2v_j>`, is exactly the expansion of `(K-B)^2` in the `B` eigenbasis. The final noncommuting trace comparison at lines 230-235 is justified since `E^2>=0` and `tr(UV)>=0` for positive semidefinite `U,V`; no commutation of `E^2` with `[B(I-B)]^{-1}` is needed.

Claim C in `frozen_theorem_v1.md` lines 31-42 is proved by `construction_v1.md` lines 237-248. The coefficients are correct: the mixture loss appears only in the lower error, and the endpoint losses appear only in the upper error. The endpoint cases `t=0,1` are covered by the same algebra.

The explicit graph family at `construction_v1.md` lines 250-315 is correct. The seed spectra in lines 252-259 are `[1/5,2/5]` and `[3/5,4/5]`; the path or bounded-degree gluing at lines 260-273 preserves `0<=K_s<=I` under `|alpha| d<=1/5`; and the Frobenius accounting at lines 275-278 gives `||E||_F^2=4e alpha^2` and hence `L(K_s)<=25e alpha^2`. The rational seed-gap lower bound at lines 280-298 checks out: `grad H(q) dot(q-p)=-(2/25)log(13/12)` and the Hessian remainder is at least `9/100`, so the displayed lower bound `>=1/12` follows from `log(1+x)<=x`. The path specialization at lines 304-308 gives `(73m+27)/1200>0`.

I found no critical gap in the theorem proof.

## Boundary-example correctness

Verdict: CORRECT.

Boundary family B1 in `research/T2/boundaries/boundary_families.md` lines 15-35 correctly disproves a dimension-free entropy modulus depending only on `||K-B||_op`. For each two-site block, the exact probabilities are two masses `1/4-t_m^2` and two masses `1/4+t_m^2`, giving the entropy formula at lines 25-28. Since `log 2-h(1/2+2t^2)=8t^4+O(t^8)`, the choice `t_m=c m^(-1/4)` makes the operator error tend to zero while total entropy loss tends to `8c^4>0`, with both spectra in `[1/4,3/4]`.

Boundary family B2 in `boundary_families.md` lines 40-53 correctly disproves a universal buffer-independent Frobenius-quadratic bound. The rank-one projection law at lines 46-52 is exact, and the ratio `h(p)/(2p(1-p))` diverges. The strict-interior variant at lines 55-69 is also correct for fixed `theta in (0,1)`: the three small probabilities have leading coefficients `(1-theta)`, `theta`, and `(1-theta)`, so `H(K_(p,theta))=(2-theta)p log(1/p)+O(p)`, `H(B_p)-H(K_(p,theta))=theta p log(1/p)+O(p)`, and the ratio to `2theta p(1-p)` diverges like `(1/2)log(1/p)`.

The limitations at `boundary_families.md` lines 71-83 are accurately scoped. These examples refute only the quantified implications B1 and B2, and do not address normalized entropy, dimension-dependent bounds, entropy-rate limits, realification transfer, or global concavity.

## Computational certificate coverage

Verdict: CORRECT for its stated bounded scope, with limited coverage.

`research/T2/artifacts/block_transfer.py` faithfully implements a narrower real-rational helper rather than the full complex Hermitian theorem. The input parser rejects floats and non-real-symmetric matrices at lines 12-25; the partition and pinching code at lines 28-42 matches the frozen block interface; and the sufficient Gershgorin feasibility and block-buffer tests at lines 45-62 are sound but intentionally incomplete.

The exact probability enumeration at `block_transfer.py` lines 85-99 implements the finite DPP exact-mass formula for blocks up to eight coordinates. The logarithm enclosure at lines 102-123 is rigorous: after range reduction to `[1,2]`, it uses the positive arctanh series with a one-sided geometric tail bound. Entropy intervals and block entropy at lines 126-142 preserve interval direction. Decimal outward rounding at lines 145-155 floors lower endpoints and ceilings upper endpoints, including negative values. The Jensen interval calculation at lines 158-188 uses the correct interval arithmetic for `J_B` and then applies the theorem's asymmetric error terms.

I executed a bounded verifier harness covering `demo_checks.checks()` plus the chain examples at sizes 4 and 32 with exact rational arithmetic and log enclosures. The run completed with exit status 0, passed 13 checks, and certified positive exact-enclosure signs for both chain examples. A private execution log with PID, command, Python version, resource-cap statement, and exit status was written under `research/T2/verifications/` and is intentionally not part of this public report.

Coverage limits are properly described by the code and docs: the helper is not a proof assistant, does not certify arbitrary rejected feasible kernels, does not cover complex Hermitian input, and does not establish general numerical coverage. Optional reporting notes: `research/T2/artifacts/demo_checks.py` line 93 records the resource limit as launcher-imposed metadata, but the script itself does not impose that limit; callers should keep imposing thread and address-space caps externally when they need that audit property. Also, `block_transfer.py` line 181 reports `full_system_subsets_enumerated: 0` because the helper does not make a separate full-law enumeration call; for the degenerate one-block partition, the block entropy calculation at lines 136-142 is effectively full-system enumeration, so that field name can overstate avoidance in that special case. This is reporting-only and does not affect the interval certificate, whose `block_subsets_evaluated` count at line 182 remains the operative enumeration accounting.

## Final verdict

CORRECT. The frozen finite-dimensional theorem, the proof, the two explicit boundary counterexamples, and the bounded exact-rational demo helper are correct within their stated scopes. No novelty certification is made.