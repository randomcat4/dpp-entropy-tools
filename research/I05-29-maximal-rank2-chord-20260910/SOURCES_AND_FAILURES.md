# Sources, methods, retained failures, and review scope

## Source binding and previously accepted scope

The 30 displayed rational matrix entries are taken from PR58's joint-additive source, Section 3, at `89aa874c24dd5a3ea98f8474826392560b1d0397`, path `research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md`. The copied finite input is explicit in `input/fixture.json` and RESULT. It is the dense correlated s=9/10 witness, not the distinct fixture in RESULT Section 4 with the accepted s in [3,15] corridor.

Before this task the latest main `docs/research_status.md`, `docs/route_ledger.md`, `docs/verification_round3_20260909/accepted_pr54.md` and `docs/verification_round4_20260909/accepted_pr58.md` were read. They accept local/simple-endpoint results and the fixed s=9/10 method obstruction, not this whole maximal chord. PR80's author continuation and issue93 were also checked. No review comments were present on issue93 when read. A PR's empty GitHub review list is not used to erase source FIRST reports archived elsewhere.

The main ledger already covers all real m-by-2 cross-block paths. Therefore PR80's preceding 2+2 continuum example is not a new region of entropy concavity; its actual negative complete fiber remains a method obstruction. The present source is genuinely 3+3 with all nine cross entries nonzero. On both conditional orientations its all-included fiber has a positive-semidefinite rank-two update and no diagonal anchor: at least one cross minor of the off-diagonal vectors of C and B^T A^(-1)B, or of A and BC^(-1)B^T, is nonzero. The checker verifies this limited exclusion of the listed coordinate/anchor tests. This does not constitute a literature-wide novelty proof.

## Two structurally different approaches, and their bridges

**Complete-law signed moments and a retained rare Fisher term.** This is the successful method in RESULT. The proof begins from the stated complete-event Mobius law, derives its event determinant and rank-two Schur coefficients, and differentiates the genuine affine K path. Its compact-interval part uses exact signed moment identities and quadratic extrema. At the boundary it keeps the rare event's own reciprocal probability beside its logarithm; it does not replace that Fisher term by a common-window constant.

Primary DPP background: A. Kulesza and B. Taskar, *Determinantal point processes for machine learning*, arXiv:1207.6083v4, Section 2.2, equations (13), (15), (25), and Section 2.4.3. The complete atomic L-ensemble identity and its relation L=K(I-K)^(-1) are relevant algebraic identities, not an assertion that L is affine here. All finite coefficients used in RESULT are additionally derived from the user's Mobius definition and cross-checked; no conditional-law bridge is imported without verification.

**Fixed-generator entropy dissipation.** P. Caputo, P. Dai Pra and G. Posta, *Convex entropy decay via the Bochner--Bakry--Emery approach*, Ann. IHP Probab. Stat. 45 (2009), 734--753, DOI 10.1214/08-AIHP183, Lemma 2.1 and equations (2.3)--(2.4), give a second-derivative/dissipation comparison under a self-adjoint irreducible generator. Remark 2.2 separates this comparison from a mere modified logarithmic Sobolev inequality. In particular this primary theorem is not itself a nonreversible-generator theorem.

The physical bridge can be checked without an imported claim. With tau=-log(s), t=exp(-tau/2), and J(tau)=I(t), the chain rule gives

`t^2 I''(t)=4J''(tau)+2J'(tau)`.

Thus even J'<=0 and J''>=0 would not suffice: one needs `2J''+J'>=0`. A quantitative bound `J''>=-kappa J'` would be sufficient when kappa>=1/2, but requires an exact stationary semigroup representation of this density and the actual second-order bound. The accepted two-point visible-feature collision already blocks a universal visible linear mechanism; this task constructs neither a hidden exact marginal nor a nonreversible substitute. It does not apply reversible transport-geodesic convexity to the radial parameter.

The full parsed primary texts at the cited equations were inspected. Attempts to render the relevant PDF pages using the web screenshot tool failed; a local PDF-download fallback also failed. No conclusion here relies on an unread figure or table. The sources provide background and a checked distinction of hypotheses, not the new entropy theorem or a novelty determination.

## Fast falsification and retained losses

1. The old best additive Cauchy projection and PR80's actual ratio cone both fail on this source at s=9/10. Their accepted/author status remains separately recorded in the earlier packets. The new proof does not enlarge either projection or assert every conditional pair/fiber is nonnegative.

2. An attempted single broad global-window estimate on [0,.99], replacing both positive moments by their minima from zero and summing per-event negative maxima, gives a lower bound about -0.1438. It fails as a sufficient estimate. This is not evidence of negative true curvature. Separating the two compact intervals preserves the increase of the positive signed moments and produces rigorous positive margins.

3. More fundamentally, a common-window treatment cannot cover this source's entire maximal chord. As s approaches s_*, q_e goes to zero while z_e tends to a strictly negative value. Hence the window penalty has N bounded away from zero and lambda(q_min) tends to infinity; the old global-window lower bound tends to negative infinity. By contrast RESULT (4.3) shows the actual rare complete-event integrand grows at least as a positive constant divided by q_e, and the full curvature is positive. This is a precise obstruction to the common-window endpoint relaxation, resolved by retaining the rare Fisher pole, not an entropy counterexample.

4. The reference law is not evaluated at an illegal endpoint and called a DPP. The interval [99/100,1] is used only to bound the 63 retained event polynomials; the actual legal endpoint is strictly below one and the full event is kept separately until that endpoint.

## Execution and remaining gaps

The script is deterministic, standard-library only and contains exact comparison checks rather than assertions disabled by Python -O. The final first full run passed 417 checks and wrote literal stdout plus rational evidence. Exploratory floating displays were used only to choose rational bounds; they are not the certificate. No failure was hidden and no external independent-compute stop contract was reused or enlarged. The user's previous 60-minute transfer rule was expressly removed for this task; no claim that a new Codex job has started follows from that change.

All new author results are PENDING_REVIEW. Independent source binding, arithmetic reimplementation, two mathematical review gates where required, formal certification and novelty remain distinct. General dense correlated rank-two maximal-chord concavity remains INCOMPLETE. This packet asserts a complete exact fixture plus the explicit coefficient/matrix family, not a universal theorem.
