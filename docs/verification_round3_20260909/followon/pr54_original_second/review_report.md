# PR54 original-unit second review — source-only proof audit

Verdict: **ACCEPTED_SCOPED**.

Frozen head reviewed: `d5c55447a0f7377dae085b8074f557e4f673b5a4`.

I reviewed the PR54 original unit only: `RESULT.md` and the pre-endpoint original helper/output. I did not read first-review artifacts, closure notes, private verifier code, PR54 addenda, endpoint-extension material, PR53 new finite-range material, or C2 issue #52 work. I did not run computation.

The accepted scope is exactly:

1. Theorem 1: arbitrary strict real diagonal blocks `A,C` and nonzero real rank-two cross block `B`, with strict local radial entropy curvature near `t=0` and an explicitly computable radius.
2. Theorem 2.3: finite cross-matching entropy deficit on the full legal chord, with arbitrary rank allowed for `B`.
3. Theorem 2.4: stationary two-layer entropy-rate deficit per cell, with the correct matching density and explicit `|d|/n` boundary loss.
4. Sections 3 and 4: exact finite interfaces and obstructions for the elementary-imset cone and nonreversible entropy-curvature flow route.
5. Section 5: the corrected finite-to-rate curvature criterion as a sufficient criterion, plus the extensive lower bound for `I_n''(0)` and the honest statement that the uniform `I_n'''=O(n)` condition remains open.

The accepted scope does not include whole-chord concavity, global rate concavity, endpoint extension, the four addenda, any theorem from PR43/PR53, the universal conditional-four-cycle cone, existence of the nonreversible flow/hidden-state construction, or any conclusion from finite output alone.

## Source inventory and boundary

The frozen `RESULT.md` has 1074 physical lines. The current helper has an endpoint-only block inserted at lines 148-172; to keep the review bounded I used the allowed pre-endpoint source snapshot for the helper/output, which contains the original 167-line helper and 13-line output. The original code lines 1-147 match the current source before the endpoint insertion, and the original matching/print tail is pre-endpoint lines 148-167. The current endpoint insertion and its three output lines were not reviewed.

The source status table says the three proved items are author proofs at lines 16-20 and marks the conditional cone, directed-flow construction, and whole-chord dense-block problem incomplete at lines 21-23. The line-level audit below checks that the proofs actually support the proved items within the stated boundaries.

## Public primary-source bridge checks

I checked only the primary-source bridges needed by the proof, not novelty.

- Borcea-Brändén-Liggett, *Negative Dependence and the Geometry of Polynomials*, arXiv:0707.2340 / JAMS 2009, supports that positive-contraction determinantal measures are strongly Rayleigh and that strong-Rayleigh measures have the conditional negative-dependence closure used here. The relevant bridge is consistent with PR54 lines 373-375 and 533-542.
- Pemantle-Peres, *Concentration of Lipschitz Functionals of Determinantal and Other Strong Rayleigh Measures*, arXiv:1108.0687 / CPC 2014, supports the strong-Rayleigh-to-stochastic-covering bridge. PR54 does not import their concentration constants blindly; Lemma 2.1 derives the specific `N lambda^2/2` moment bound from SCP and Hoeffding at lines 340-371.
- Lyons, *Determinantal Probability Measures*, arXiv:math/0204325 / PMIHES 2003, supports the discrete determinantal probability-measure setting, complete cylinder probabilities, and the projection/positive-contraction context. PR54 uses those only as background, and explicitly does not infer a four-way square coupling from pairwise domination at lines 605-653.
- Erbar-Maas, *Ricci Curvature of Finite Markov Chains via Convexity of the Entropy*, arXiv:1111.2687 / ARMA 2012, is correctly cited only as the reversible entropy-convexity/Bochner template. PR54 does not apply it as a black box to the nonreversible flow; see lines 787-792 and 997-1005.

## 1. Strict local radial curvature at decoupling

**Accepted within the local rank-two scope.**

The theorem statement at lines 107-122 fixes strict `0<A<I`, `0<C<I`, nonzero rank-two `B`, and the affine block path. Lines 124-181 define the rank-two complete-event score `u`, acceleration `v`, the lower score certificate `underline sigma^2_ij`, the legal-radius bound, the third-derivative bound, and the final estimate `H''(t) <= -3 underline sigma^2_ij t^2`.

The complete-event likelihood calculation is sound. Lines 194-204 use the signed complete-event determinant, Schur complement, and the rank-two determinant lemma to get
`q_s(S,T)=1+s u(S,T)+s^2 v(S,T)`, with `s=t^2`. The normalization identities `E_mu u=E_mu v=0` at lines 206-209 follow because the finite polynomial likelihood integrates to one for small legal `s`. The proof does not delete rare events or replace the complete law by a projected statistic; the relative entropy identity is stated at lines 211-220.

The nonzero-score argument is also sound. Lines 224-242 use one nonzero entry `B_ij` and the exact two-point inclusion identity to get `E_mu[Z_ij u]=-B_ij^2`; lines 243-252 then give the positive lower bound on `sigma^2` by Cauchy-Schwarz. The denominator is positive because strict `A,C` imply `A_ii,C_jj in (0,1)`, hence `A_ii C_jj in (0,1)`.

The derivative and constant chain closes. Lines 260-276 give the exact full relative-entropy derivatives and keep the Fisher term. Lines 278-289 prove `q_s>=1/2`, `|q_s'|<=M_1`, `|q_s''|<=2V_0`, and hence `|I'''(s)|<=L_3`; the constants match the displayed definitions: `3*M_1*(2V_0)/(1/2)=12M_1V_0` and `M_1^3/(1/2)^2=4M_1^3`. Lines 293-321 correctly convert from `s` back to the true affine parameter `t`: `H''(t)=-(2I'(s)+4sI''(s))`, `J'(s)=6I''(s)+4sI'''(s)`, and the choice `delta <= 3 underline sigma^2/(10L_3)` gives `J'(s)>=3 underline sigma^2` and then `J(s)>=3 underline sigma^2 s`.

The legal-radius check is adequate: lines 147-176 define `epsilon`, `beta`, `delta_leg`, and `delta`; lines 319-320 use the off-diagonal perturbation norm `|t| ||B||op` to keep both `K(t)` and `I-K(t)` bounded below by `epsilon/2`. This proves strictness only in the certified neighborhood, exactly as scoped at lines 323-328.

## 2. Full-law matching entropy deficit and stationary rate bridge

**Accepted.**

Lemma 2.1 is valid with its stated constant. Lines 340-349 state the moment bound for a strict strong-Rayleigh law and a 1-Lipschitz Hamming function. The proof at lines 353-371 uses conditional SCP under coordinate revelation: the two possible conditional laws differ by at most one remaining bit, hence the full configurations differ by at most two bits. Hoeffding for a martingale increment in an interval of length two gives `exp(lambda^2/2)` per coordinate, so the total bound is `exp(N lambda^2/2)`. Lines 373-375 correctly distinguish strong Rayleigh/SCP from mere pairwise negative correlation.

The entropy variational inequality at lines 377-392 is the standard Donsker-Varadhan one-line tilt argument and has the right sign for negative `lambda`.

The finite matching theorem is sound. Lines 396-405 allow arbitrary rank `B` and require only that the displayed finite `K(t)` is legal. Since the diagonal blocks are strict, the decoupled law has full support, so `D(P_t || mu)` is finite even if the displayed legal endpoint is not strict. Lines 416-424 identify `H(K(0))-H(K(t))` with the full relative entropy because the two block marginals remain exactly `A` and `C`. Lines 428-443 define the matching statistic and use vertex-disjointness to make it 1-Lipschitz; the exact two-point DPP inclusion gives the shift `-t^2 W_M`. Lines 444-450 choose `lambda=-t^2 W_M/N` and get precisely `t^4 W_M^2/(2N)`. This proves a full-law lower bound, not a projected-law replacement, as lines 452-454 say.

The stationary rate normalization is correct. Lines 456-475 define a two-layer stationary Toeplitz DPP and entropy rate per cell, `h(t)=lim H_n(t)/n`, where each finite window contains `2n` observed variables. For fixed offset `d`, lines 481-490 construct `q_n=n-|d|` disjoint matched pairs and `N_n=2n`. Dividing Theorem 2.3 by `n` gives exactly line 494:
`t^4 (n-|d|)^2 |b_d|^4/(4n^2)`. Lines 496-498 then pass to the stationary block-entropy limit and obtain the rate deficit `t^4 |b_d|^4/4`. The boundary loss is visible and harmless: lines 500-506 identify the `|d|/n` loss and reject direct-sum replication as a rate proof.

This proves a global entropy-rate deficit from the decoupled point, hence strict maximality of `t=0` when some `b_d` is nonzero, as lines 476-477 state. It does not prove whole-chord concavity or a global second-derivative sign; lines 508-510 correctly say so.

## 3. Elementary-imset cone and square-coupling obstruction

**Accepted as an exact interface and limitation, not as the missing universal cone theorem.**

Lines 516-542 correctly define elementary conditional four-cycles and derive the DPP sign. After conditioning outside `{i,j}`, a strict DPP complete law gives a two-coordinate strong-Rayleigh law, so negative correlation gives `p(R)p(Rij)<=p(Ri)p(Rj)`, and therefore `<e^{ij|R}, log p> <= 0`.

The rank-two indefinite interface at lines 545-599 is algebraically correct. For `D=aa^T-bb^T`, determinant multilinearity gives `p_{K+zD}=p+zr+z^2c`. Introducing the positive rectangle `K+x aa^T+y bb^T` and using rank-one multilinearity, the mixed coefficient `m=partial_x partial_y p` satisfies `c=-m` after substituting `x=z,y=-z`. If the conic system (3.7) has nonnegative weights, then `<m,log p><=0`, hence `<c,log p>>=0`; the entropy curvature formula at lines 580-584 keeps both the Fisher sum and acceleration term. This is a pointwise certificate at the current base law; a line-wide result would require the certificate after recentering along the line.

Lines 588-599 correctly describe rational feasible tables and rational Farkas witnesses. Lines 601-603 explicitly leave the universal assertion incomplete and do not import open PR43.

The pairwise-covering limitation at lines 605-653 is a valid logical obstruction. The four pairwise covering relations in lines 625-639 hold, but the forced middle marginals in lines 645-648 prevent a single face-supported square coupling. This does not disprove the DPP-specific cone, and the source says that at lines 650-653. The corrected numerical interpretation at lines 655-667 is also properly scoped: floating infeasibility is not treated as a rational certificate.

## 4. Nonreversible flow and entropy-curvature interface

**Accepted as an interface and obstruction statement.**

Lines 682-727 state the finite directed-flow feasibility system. The flow convention is consistent: `r_xy=mu_x q_xy` is flow from `x` to `y`; stationarity equates total inflow and outflow at each `y`; the density-adjoint formula at lines 695-699 follows from that balance. The exterior-scaling equations at lines 701-718 are the exact linear conditions needed for the three entries of `G_C` to have eigenvalue `-1` and `det G_C` to have eigenvalue `-2`. Lines 720-727 correctly separate rational certificates from floating LP statuses.

The entropy-trajectory calculation is sound. Lines 734-742 show that if the exterior scaling holds and `s=s_*e^{-tau}`, then `partial_tau f_s=L^dagger f_s`. Lines 743-757 derive the full relative-entropy first and second derivatives and keep the complete Fisher term. Lines 759-764 correctly convert the trajectory derivatives into the true affine-kernel curvature:
`-H''(t)=2I'(s)+4sI''(s)=(2/s)(2 Ical''+Ical')`.

The missing sign condition is exactly identified. Lines 765-785 explain that feasibility, stationarity, and data processing are insufficient; the needed statement is the second-order entropy-production inequality `2 Ical''+Ical' >= 0`, equivalently `D' <= -D/2` when `D=-Ical'`. Lines 787-792 cite reversible entropic Ricci/Bakry-Emery methods only as a template, not as a proof for the present nonreversible setting. The hidden-state extension at lines 794-812 also has the right quantifier: even an exact lifted intertwining would still need the entropy inequality to descend with the required direction and constants. Lines 814-818 leave existence and the Bochner estimate incomplete.

## 5. Corrected finite-to-rate curvature bridge

**Accepted as a sufficient local criterion and as a precise remaining gap statement.**

Proposition 5.1 at lines 829-848 is the standard Jensen-limit argument: if each finite normalized entropy is concave and the stationary entropy-rate limit exists, the pointwise limit is concave. Lines 850-852 correctly emphasize that finite restrictions of an affine infinite DPP kernel are true affine principal submatrices.

Proposition 5.2 includes the necessary repaired hypotheses. Lines 856-867 explicitly assume the split fixed-marginal form, `I_n(0)=I_n'(0)=0`, an extensive lower bound `I_n''(0)>=c n`, and a finite extensive upper bound `|I_n'''(s)|<=L n` with `0<L<infinity`, all independent of `n`. Lines 884-898 repeat the finite `J_n` argument with constants: from `I_n''(s)>=cn-Lns` and `|I_n'''(s)|<=Ln`,
`J_n'(s)=6I_n''(s)+4sI_n'''(s)>=6cn-10Lns`, so `s<=3c/(10L)` gives `J_n'(s)>=3cn`; integrating from `J_n(0)=0` gives the local curvature bound, and integrating twice gives the normalized quartic deficit. The finitely many small `n<n0` do not affect the limit.

The source does not turn the matching deficit into concave approximants. Lines 900-929 prove only the first condition, `I_n''(0)` extensive, using the matching statistic and the variance bound from Lemma 2.1. Lines 924-929 explicitly leave the uniform `I_n'''=O(n)` condition open and reject rare-event deletion. Lines 931-942 state the boundary-remainder variant carefully: if concave approximants have an `o(n)` uniform error, their normalized limit is concave, but Theorem 2.4 supplies only a quartic deficit with boundary normalization, not such approximants. Lines 1070-1074 repeat that rare-event truncation would remove part of the Fisher term and is therefore not an allowed proof of the missing bound.

## 6. Original exact helper/output

**Accepted as a consistency fixture only. No computation was run in this review.**

The pre-endpoint helper checks a rational dense `3+3` fixture, not a theorem by enumeration. Lines 15-29 define strict rational `A,C` and dense rank-two `B=UV^T`. Lines 62-77 verify rank, dense entries, non-coordinate null-vector behavior relative to PR43's special family, and positive principal minors for `A,I-A,C,I-C`. Lines 79-112 enumerate all `8 x 8` complete configurations, build complete-event probabilities, verify normalization, and check the score identities `E u=E v=0` and `E[Z_00 u]=-B_00^2`. Lines 113-127 independently compare the full six-by-six complete law at `t=1/10` with the rank-two likelihood formula for all 64 configurations. Lines 129-146 compute the finite constants and certified local radius. Lines 149-153 compute the size-three matching gap coefficient, and lines 155-167 print the intended exact outputs.

The pre-endpoint output lines 1-13 match the fixture's scope: complete configurations, full likelihood check, outside-PR43-special-family check, exact score/radius data, and matching gap coefficient. I did not review the endpoint-specific insertion in the current helper/output.

## Verdict limits and corrections

No load-bearing gap was found in the repaired PR54 original unit. The proof now keeps the full complete law, the full Fisher terms, and rare configurations. The Section 5 repairs are present and material: `I_n(0)=I_n'(0)=0` is explicit, `0<L<infinity` is explicit, and the matching deficit is not mislabeled as a concave-approximant family.

This review accepts the local rank-two curvature theorem, the full-law matching deficit, the two-layer stationary rate deficit/maximizer statement, and the stated finite interfaces/obstructions. It does not accept any whole-chord concavity theorem, any global rate concavity theorem, any endpoint extension, any addendum theorem, or any result depending on finite output as proof.
