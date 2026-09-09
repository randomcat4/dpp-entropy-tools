# PR54 first-pass frozen scope

Reviewer: first independent proof review, non-author.

Source object: `sources/pr54` only, bound by `SOURCE_BINDING.json` to PR `54`, immutable commit `203f7044815faac9a2de7bc8dbc5bfe249026b1f`, three files under `research/I05-23-20260909/`:

- `RESULT.md`
- `code/verify_local_and_matching.py`
- `output/verify_local_and_matching.txt`

Excluded source objects:

- The later `sources/pr54_daf9c31` bundle and its two addenda are not reviewed here.
- Open PR43 author claims are not accepted as premises. They may be mentioned only as scoped background exactly as PR54 does at `RESULT.md` lines 7-12, 601-603, and 1024-1030.
- PR51, issue 52, and any current remote head changes are out of scope.
- Novelty and priority are not assessed.

Global interpretation frozen from `RESULT.md` lines 14-27 and 41-80:

- The branch claims three proved results and several delimited interfaces.
- The branch does not claim whole-chord entropy concavity from the quartic deficit.
- The branch does not claim a general radial theorem for all dense internally correlated blocks.
- The branch does not delete complete events or omit the complete Fisher term.

## Frozen claims

### C1. Strict local radial curvature for arbitrary rank-two cross block

Frozen from `RESULT.md` lines 107-188, with proof at lines 190-321 and scope at lines 323-328.

Objects and quantifiers:

- `A` is an `m x m` real strict DPP kernel and `C` is an `ell x ell` real strict DPP kernel, with `0 < A < I` and `0 < C < I`.
- `B` is a nonzero real `m x ell` matrix of rank two.
- `K(t) = [[A, tB], [t B^T, C]]`.
- For any full-rank factorization `B = U V^T`, complete configurations `S,T` define
  `X_S = A - E_{S^c}`, `Y_T = C - E_{T^c}`,
  `G_A(S)=U^T X_S^{-1} U`, `G_C(T)=V^T Y_T^{-1} V`,
  `u(S,T)=-tr(G_A(S)G_C(T))`, and
  `v(S,T)=det G_A(S) det G_C(T)`.
- With the product complete law `mu(S,T)=p_A(S)p_C(T)`,
  `sigma^2 = E_mu u^2`.

Claim:

- `sigma^2 > 0`.
- For an explicitly computable `delta > 0` defined by lines 147-177, `K(t)` is strict and
  `H''(t) < 0` for every `0 < |t| <= sqrt(delta)`.
- The quantitative bound claimed is
  `H''(t) <= -3 sigma_*^2 t^2`, where
  `sigma_*^2 = B_ij^4 / (A_ii C_jj(1-A_ii C_jj))` for any selected nonzero entry `B_ij`.

Excluded interpretations:

- No whole-chord concavity.
- No claim for rank other than two in this immutable source object.
- No use of a projected event in place of the full complete law.

### C2. Exact rational fixture

Frozen from `RESULT.md` lines 82-101 and the two fixture files.

Claim:

- The script `verify_local_and_matching.py` is a symbolic consistency check for one rational internally correlated dense `3+3` rank-two example.
- It verifies all 64 complete configurations for the displayed likelihood, exact score identities, a certified local radius, and a matching entropy-deficit coefficient.
- It is not claimed to prove any global or generic theorem by finite enumeration.

### C3. Strong-Rayleigh/SCP martingale moment bound

Frozen from `RESULT.md` lines 340-375.

Objects and quantifiers:

- `mu` is a strict strong-Rayleigh law on `{0,1}^N`.
- `F` is 1-Lipschitz in Hamming distance.
- `lambda` is any real number.

Claim:

- `log E_mu exp(lambda(F-E_mu F)) <= (N/2) lambda^2`.
- The proof uses conditional stochastic covering, a martingale reveal process, and Hoeffding's lemma with martingale difference interval length at most two.

### C4. Entropy variational inequality

Frozen from `RESULT.md` lines 377-392.

Claim:

- For `P << mu` and any real random variable `F`,
  `D(P||mu) >= lambda(E_P F - E_mu F) - log E_mu exp(lambda(F-E_mu F))`
  for every real `lambda`.

### C5. Finite cross-matching entropy deficit

Frozen from `RESULT.md` lines 394-454.

Objects and quantifiers:

- `A` and `C` are strict finite real DPP kernels.
- `K(t) = [[A,tB],[tB^T,C]]` is legal at the displayed value of `t`.
- `M` is a matching in the bipartite support of `B`.
- `W_M = sum_{(i,j) in M} B_ij^2` and `N=m+ell`.

Claim:

- `H(K(0))-H(K(t)) >= t^4 W_M^2/(2N)`.
- If `B != 0`, choosing a one-edge matching gives strict entropy deficit for every legal `t != 0`.
- The statistic is used only as a variational test of the full relative entropy.

### C6. Two-layer stationary entropy-rate deficit

Frozen from `RESULT.md` lines 456-510.

Objects and quantifiers:

- A real DPP on `Z x {L,R}` is stationary under simultaneous cell shifts.
- The block Toeplitz kernel has cross block `B_{i,j}=b_{j-i}`.
- Every finite restriction of the two diagonal blocks is strict.
- `t` lies in a legal interval.
- `H_n(t)` is the entropy of cells `1,...,n` in both layers and
  `h(t)=lim_n H_n(t)/n`.

Claim:

- For every fixed offset `d`,
  `h(0)-h(t) >= t^4 |b_d|^4/4`.
- If the cross block is not zero, `t=0` is a strict global maximizer of entropy rate along the legal radial chord.
- This remains only a quartic deficit, not a second-derivative concavity theorem.

### C7. Elementary-imset four-cycle certificate interface

Frozen from `RESULT.md` lines 514-604.

Claim:

- The elementary conditional vector `e^{ij|R}` evaluates a four-point second difference.
- For strict determinantal complete laws, conditional two-coordinate negative correlation gives
  `<e^{ij|R}, log p> <= 0`.
- For an indefinite rank-two line `K+z(aa^T-bb^T)`, if the mixed rectangle coefficient `m` has a conic representation by elementary imsets, then the entropy curvature at the base point is nonpositive with the full Fisher term retained.
- A rational feasible weight table proves the certificate; a rational Farkas vector proves infeasibility.

Excluded interpretation:

- The universal assertion that the conic representation always exists is explicitly incomplete.

### C8. Pairwise stochastic covering does not imply square coupling

Frozen from `RESULT.md` lines 605-653.

Claim:

- Proposition 3.1 gives a two-bit example where all four adjacent pairwise covering relations hold but no face-supported square coupling of the form `(R,Ri,Rj,Rij)` exists.
- This disproves only the logical implication from pairwise covering to a square coupling, not the DPP-specific four-cycle cone.

### C9. Directed-flow/Farkas and entropy-curvature interface

Frozen from `RESULT.md` lines 670-818.

Claim:

- For a finite visible state space, the stationary directed-flow unknowns `r_xy=mu_x q_xy` give a rational linear feasibility system for stationarity and exterior degree equations.
- Farkas' lemma gives the stated rational infeasibility interface.
- Even if the flow realizes the degree-one and degree-two features, radial entropy concavity still requires the trajectory-specific inequality
  `2 Ical'' + Ical' >= 0`, equivalently `D' <= -D/2`.
- Data processing or modified log-Sobolev estimates alone do not supply this second-order inequality.

Excluded interpretation:

- No existence theorem for such flows for every correlated DPP block.
- No nonreversible Bochner estimate is proved.

### C10. Curvature-to-rate sufficient criteria and limitations

Frozen from `RESULT.md` lines 822-939.

Claims:

- If every finite block entropy `H_n` is concave on an interval and `h(t)=lim_n H_n(t)/n`, then the entropy rate is concave on that interval.
- Under uniform extensive information-curvature hypotheses
  `I_n''(0) >= c n` and `|I_n'''(s)| <= L n`, a local finite-block curvature bound and normalized quartic rate deficit follow.
- In the stationary two-layer Toeplitz setting, the matching statistic proves the extensive lower bound for `I_n''(0)` asymptotically.
- The uniform extensive `I_n'''` bound, or an equivalent entropy-production estimate, remains unproved.
- Boundary-controlled approximants with `b_n/n -> 0` would pass concavity to the normalized limit.

Open wording to audit in the review:

- Proposition 5.2 uses `J_n(0)=0`; as written this requires either an explicit `I_n'(0)=0` hypothesis or a definition of `I_n` as the relative entropy from the decoupled complete law.
- The formula `3c/(10L)` needs `L>0` or a convention when `L=0`.
- The final boundary-remainder sentence must not be read as deriving concave approximants from the matching deficit alone.
