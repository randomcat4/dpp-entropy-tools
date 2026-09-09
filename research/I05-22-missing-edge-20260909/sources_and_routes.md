# Sources, exact bridges, and route selection

Author research record, 2026-09-09. This file does not certify novelty.

## Frozen repository inputs and scope

Read main `docs/research_status.md` and `docs/route_ledger.md` in full. The accepted scopes relevant here are real two-dimensional concavity, exchangeable real three-point centers, and the normalized weak-coupling three-point domain. General real three-point concavity remains INCOMPLETE. The sparse beta-zero family excludes a universal positive safety margin. None of the new claims below are promoted to main's accepted scope.

Read the complete PR41 `research/N3/round3/I05-W4-20260909/round2/proof.md` (sections 1–10) and `attempts.md` at commit `6fd61dcd299417fc3a4eab3af682c03dd816b670`. Its equal-strength half-filled theorem, conditional two-point lemma, isolated-block identity, and missing-edge coordinates are author claims awaiting independent review.

Read the complete requested PR43 `research/I05-W1-20260909-R2/proof/04_three_point_indefinite_rank2.md` at its latest observed commit `a7da3951a8ce02839dfa27f7205a1032d6f80f50`. This differs from the older coordination freeze `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`. The three-point theorem is not treated as an accepted black box.

Read main R3 `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/derivation.md` and `proof_or_blocker.md`. In particular N positive definite at Lambda=0 is not the missing full Fisher-versus-cofactor inequality. The scalar rho reduction is an equivalence, not a solution.

### PR43 load-bearing identity, checked directly

Write the local quadratic event coefficient as c(S), pair coefficients as delta_ij=det(D_ij), and R=tr(K adj D). Inclusion-exclusion gives

`c = sum_(i<j) delta_ij e^(ij|k=0) + R e^(123)`,

where e^(123)(S)=(-1)^(3-|S|), and the face cycle is (+1,-1,-1,+1) in the two free bits. This holds for arbitrary D as a statement about the local t^2 coefficient; a cubic term can still be present.

For indefinite rank two, adj D=gamma nn^T, gamma<0, n unit null, and kappa=n^TKn lies in (0,1). Thus delta_ij=gamma n_k^2 and R=gamma kappa. Since e^(ij|k=1)-e^(ij|k=0)=e^(123), exactly

`c = sum delta_ij [(1-kappa)e^(ij|k=0)+kappa e^(ij|k=1)]`.

The conditional log odds of each real two-point DPP are nonpositive. Therefore <c,log p> is nonnegative, and the complete H''=-F-2<c,log p> is nonpositive. This verifies the carrier and its sign mechanism without assuming the theorem. It does not handle semidefinite rank two: gamma changes sign. Summing several such good directions would also leave unknown mixed Hessian terms.

`verify_exact.py` independently reconstructs the eight inclusion-exclusion polynomials and checks both the general coefficient law and `adj(uv^T+vu^T)=-(u cross v)(u cross v)^T`. This is an author-side independent implementation, not an independent nonauthor review.

### PR41 missing-edge coordinate bridge, checked directly

For K=[[x,0,b],[0,y,c],[b,c,z]], put v1=x(1-x), v2=y(1-y), phi_i=(i-x)/v1, psi_j=(j-y)/v2. The product marginal is P_ij=Bern_x(i) Bern_y(j), and

`t_ij = z-b^2 phi_i-c^2 psi_j`,

`T_ij=t'_ij=d3+b^2 d1 phi_i^2+c^2 d2 psi_j^2-2b h13 phi_i-2c h23 psi_j+2bc h12 phi_i psi_j`.

The map from (d1,d2,d3,h12,h13,h23) to (d1,d2,T00,T10,T01,T11) has determinant `8b^2c^2/(v1^2v2^2)` and is invertible for bc!=0. The complete Fisher is

`F=d1^2/v1+d2^2/v2+sum P_ij T_ij^2/[t_ij(1-t_ij)]`.

The script derives these identities from the event quotient p_(ij1)/(p_(ij0)+p_(ij1)), not from an imported author verifier. The general acceleration is still present. Merely displaying this coordinate change does not prove the general missing-edge inequality.

## Primary literature and the actual bridges used

1. Russell Lyons, *Determinantal probability measures*, Publ. Math. IHES 98 (2003), 167–212, DOI 10.1007/s10240-003-0016-0; primary manuscript https://arxiv.org/abs/math/0204325 . Yuzhou Gu, *Entropy of Determinantal Point Processes*, course-project report, https://sevenkplus.com/data/dpp.pdf , Theorem 7. The directly checked rank-one bridge is `rank D<=1 => each det(K_T+tD_T) affine => each complete p_S affine => H''=-F`. This does not control polarization with another rank-one direction. No other theorem of the course report is used.

2. Erwan Hillion and Oliver Johnson, *A proof of the Shepp–Olkin entropy concavity conjecture*, Bernoulli 23(4B) (2017), 3638–3649, DOI 10.3150/16-BEJ860; primary manuscript https://arxiv.org/abs/1503.01570 . Its entropy is that of a Bernoulli sum, not the complete DPP configuration. The usable methodological bridge is to keep probability derivatives and local log ratios paired with the Fisher denominators. On our Boolean cube the exact replacement is `H''=-sum(p')^2/p-2 sum delta_ij L_ij|0-2R Lambda`, obtained from the face identity above. The remaining inequality couples those logs to the same eight scores; cardinality concavity alone says nothing sufficient about it.

3. Omar Boussaid, Carolin Kreisbeck and Anja Schloemerkemper, *Characterizations of symmetric polyconvexity*, Arch. Ration. Mech. Anal. 234 (2019), 417–451; https://arxiv.org/abs/1806.06434 . The relevant cross-field distinction is restricted rank-one/symmetric-rank-one positivity versus actual convexity of a quadratic form. Our exact DPP bridge is `B(D)=F(D)-2tr(N adj D)`, N positive semidefinite from conditional odds. For a symmetrized rank-one direction D=uv^T+vu^T, `adj D=-(u cross v)(u cross v)^T`, so B(D)>=0 follows immediately. This is not full B>=0. For example, the artificial form `2||D||_F^2-(tr D)^2` is nonnegative on indefinite rank-two symmetrized directions but equals -3 at D=I. It is not a DPP counterexample. This route explains why PR43 alone does not close the remaining directions, and was not used to make an invalid decomposition argument.

4. Davit Harutyunyan and Gagik Amirkhanyan, *Rank-one convexity, polyconvexity, and extremality for three-dimensional elasticity tensors in various symmetry classes*, arXiv:2607.21828v1, 23 July 2026; primary text https://arxiv.org/html/2607.21828v1 . Its inertia/definiteness criteria suggested inspecting a continuous matrix field with a tractable determinant rather than estimating every mixed entry separately. The exact bridge used here is strictly elementary and proved in full: fixed s, continuous symmetric G'_s(r), det G'_s(r)>0 for all |r|<1, and G'_s(0)>0 imply G'_s(r)>0 by absence of zero eigenvalues. Then G_s=G_0+integral G'_s is positive definite. No result about elasticity tensors is imported as a DPP theorem, and no priority claim for this elementary method is made.

## Route choice and new result

The general missing-edge event-weighted matrix is still difficult because all unequal-diagonal mixed terms survive. The half-filled case retains a true complement/sign involution, giving an exact 2+4 decomposition without setting any direction coordinate to zero in the final theorem. The four-dimensional block admits a rational derivative determinant and inertia continuation across *all* unequal edge-strength ratios. This is the route completed in `proof_half_filled.md`.

PR41 only treats the equal-strength rays b=+/-c in its new strong-coupling theorem. The present author result removes that equality while allowing every nonzero real direction and every strict coupling strength `4(b^2+c^2)<1`. It is not simply a change in the weak-coupling constant. Its proof re-derives the seed and uses neither PR41 nor PR43 as a theorem dependency.

## Routes explicitly not reused

The repository has already disproved a uniform safety margin, uniformly shifted full-atom log-integrand positivity, Loewner antitonicity of the conditional two-point entropy gradient, and replacement of complete Fisher by selected one-/two-point projections. None is assumed here. Positive definiteness at an isolated block cannot give a naive open tube because connecting directions are flat there. Good-direction decompositions without mixed Hessian control, L-affine paths, and observational basis rotation are excluded.

The current author continuation tests whether the stronger missing-edge conditional entropy `C=H(X3|X1,X2)` is concave at arbitrary arrow centers. Complete Fisher for C is the displayed conditional sum, with all acceleration retained. No finite scout is a proof of this candidate. A failure of a sufficient intermediate kernel inequality is not an entropy counterexample. Post-checkpoint progress and any exact new obstruction will be recorded separately.

## Remaining obligations and status

PROVED (author, unreviewed): the full six-direction theorem at every strict half-filled missing-edge center with bc!=0; its non-strict axis extension; the explicit identities used in that proof.

INCOMPLETE: arbitrary missing-edge diagonal parameters, general strict real three-point centers, general remaining semidefinite/full-rank directions outside the stated center family, and a strict positive Jensen counterexample. No numerical finite sample is used to close any of these domains.

The GitHub write of the Python verifier was blocked by a tool safety-state check. It was not retried through another GitHub endpoint. The user-authorized Google Drive fallback was actually uploaded and metadata-read back; see `verification.md`. The proof itself is committed on this research branch. This publication checkpoint does not end the ongoing analytic continuation.
