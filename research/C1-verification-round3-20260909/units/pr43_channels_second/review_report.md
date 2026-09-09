# Fresh second mathematical review -- PR43 claims D and I--N

Reviewer role: fresh non-author review, analytical only.

Source scope is frozen in `frozen_scope.md`. I did not use initial reviewer reports, other child reports, or `continuation/CONSISTENCY_AUDIT.md` as evidence. I used only the assigned source material. Novelty and formal/mechanical proof status are unassessed.

## Executive verdict

Overall scoped verdict: `ACCEPTED_SCOPED`.

The PR43 claims D and I--N are correct within the stated scope, assuming the imported C3 diagonal-anchor theorem is accepted as an external input. I found no `CRITICAL_GAPS`. The main editorial tightening I recommend is to state explicitly that the Markov curvature formula involving division by `s=t^2` is an interior `s>0` identity; behavior at `t=0` and feasible boundaries is by continuity/finite-event extension, not by direct substitution into the divided formula.

| Claim | Verdict | Scope note |
|---|---:|---|
| D. Imported diagonal-anchor line concavity | `CORRECT` | Correct dependency usage only; I did not reprove the imported C3 theorem. |
| I. Diagonal active-sector arbitrary-rank theorem and `3+5` fixture | `CORRECT` | Uses the original coordinate sector `J`; no orthogonal basis substitution. |
| J. Per-conditional strict diagonal-anchor criterion | `CORRECT` | Strict diagonal contraction of each anchor `D_S` is essential and is stated. |
| K. Density-adjoint Markov intertwining/generator/Fisher/curvature identity | `CORRECT` | Correct for density adjoints and interior `s>0`; reversible cases are only special cases. |
| L. Diagonal exterior-degree closure | `CORRECT` | Independent coordinate refresh gives degree one `theta` and degree two `theta^2`. |
| M. Reversible obstruction, value `-125/78` | `CORRECT` | Rules out universal reversible exterior-noise mechanisms only. |
| N. Occupation-channel obstruction, `91/400` versus `99/400` | `CORRECT` | Rules out a unified classical occupation-channel representation only. |

## Sources and assumptions

Primary frozen statement: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md`, version `v3.1`, lines 1--8. The source binding identifies PR #43 commit `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.

Imported C3 source: `sources/dependency_c3/frozen_statement_v2.md` and `sources/dependency_c3/proof.md`, bound to commit `648f1906468e3e548410f98a6b1a53a978f2ea11`.

I use complete-configuration Shannon entropy throughout. For strict interior kernels all event probabilities are positive; feasible boundary statements are understood through continuity of finite event probabilities and of `-x log x` at zero.

For Markov kernels, I use the convention of `proof/07_markov_adjoint_and_reversible_obstruction.md`: `Q` is the forward transition on configurations / backward operator on observables, `Q^\dagger` is its `L^2(mu)` adjoint acting on densities, and the output density is `Q^\dagger f`.

## D. External diagonal-anchor input

Statement checked: PR43 freezes D as the external theorem that for every strict diagonal Hermitian contraction `D` and fixed Hermitian direction `V`, `u -> H(D+uV)` is concave on the whole legal parameter interval (`frozen_statement_v3.md:10--18`).

Dependency match: C3 freezes exactly the finite diagonal theorem for every diagonal `B=diag(b_i)` with `0<b_i<1`, every fixed Hermitian direction `A`, and the interval `J={t: 0<=B+tA<=I}` (`dependency_c3/frozen_statement_v2.md:6--15`). It explicitly says the direction need not commute with the diagonal base (`dependency_c3/frozen_statement_v2.md:14--15`) and prohibits substituting cardinality or quantum entropy for finite event laws (`dependency_c3/frozen_statement_v2.md:26--32`). Its proof identifies independent Bernoulli replacement with the affine DPP kernel `B+t(K-B)` (`dependency_c3/proof.md:81--112`) and extends from one-sided rays to the entire feasible interval including boundaries (`dependency_c3/proof.md:114--141`).

Independent check: Renaming C3's `B` to PR43's diagonal anchor `D`, and C3's `A` to PR43's direction `V`, gives the PR43 input exactly. PR43 uses this input in I and J only for affine lines passing through strict diagonal kernels (`proof/04_diagonal_active_sector.md:97--99`, `proof/04_diagonal_active_sector.md:168--181`). I found no hidden commutativity, zero-mean, rank, or coordinate-support assumption.

Verdict: `CORRECT`.

## I. Diagonal active-sector arbitrary-rank theorem

Statement checked: With strict real symmetric blocks `A,C` and arbitrary real `B`, if a right coordinate set `J` satisfies `B_{:,J^c}=0`, `C_{J,J^c}=0`, and `C_J` is strict diagonal, then `t -> H([[A,tB],[tB^T,C]])` is concave on the full legal interval; `|J|` and `rank(B)` are unrestricted, and the block-swapped version also holds (`frozen_statement_v3.md:171--188`).

Proof dependencies: The complete-event Schur identity gives
`p_{K(t)}(S,T)=p_A(S)p_{C-sM_S}(T)` and
`G(s)=H(A)+sum_S p_A(S)H(C-sM_S)` with `s=t^2` (`proof/01_conditioning.md:24--40`, `proof/01_conditioning.md:63--68`). The radial lifting lemma correctly converts `s`-concavity plus `G(s)<=G(0)` to concavity in the true affine parameter `t`, using the fixed block marginals and mutual information (`proof/03_lifting_and_exterior.md:3--43`; repeated in `proof/04_diagonal_active_sector.md:28--63`).

Independent proof check: Under the coordinate-sector hypotheses, `M_S` has zero rows and columns outside `J`, and `C-sM_S=(C_J-sM_{S,J}) \oplus C_{J^c}` (`proof/04_diagonal_active_sector.md:67--87`). Complete-event entropy of a block diagonal kernel is additive, so each conditional entropy is `H(C_J-sM_{S,J})+H(C_{J^c})` (`proof/04_diagonal_active_sector.md:90--94`). The first term is an affine line through the strict diagonal kernel `C_J`, so D applies with no rank restriction on `M_{S,J}` and no commutation requirement (`proof/04_diagonal_active_sector.md:97--101`). Averaging with fixed positive weights gives `s`-concavity; the radial lemma gives the real `t`-path concavity. The argument remains in the original coordinate basis because the condition is a coordinate support/block condition on `J`; no entropy-changing orthogonal change of observation basis is used.

Boundary and `t=0` check: The proof does not confuse `s=t^2` with an affine kernel parameter. The actual affine family is in `t`; `s` is used only after the Schur conditioning step. The conversion at `proof/04_diagonal_active_sector.md:35--63` covers crossings through `t=0`, while line 99 invokes finite-event continuity for the legal boundary.

`3+5` fixture check: The displayed matrices have `A` non-diagonal of size 3, `C` non-diagonal of size 5 through its final `2 x 2` block, and `B` supported in the first three right coordinates (`proof/04_diagonal_active_sector.md:103--126`). The Gershgorin/Weyl bounds prove strict legality at least for `|t|<=1` (`proof/04_diagonal_active_sector.md:128--162`). The row relation gives `rank(B)=2`, and the first and third rows are not proportional; since all first three right coordinates are active, the right row/singular plane is not contained in any two-coordinate principal plane (`proof/04_diagonal_active_sector.md:164`). Taking `J={1,2,3}` verifies the theorem's hypotheses.

Counterexample attempts: High rank of `B` does not break the proof, because the imported D theorem allows arbitrary Hermitian directions in arbitrary finite dimension. A non-coordinate orthogonal diagonalization attempt would be invalid for configuration entropy, but the proof never uses one. The old two-coordinate or `m x 2` theorems are not being smuggled in.

Verdict: `CORRECT`.

## J. Per-conditional strict diagonal-anchor criterion

Statement checked: For each left complete configuration `S`, if there exists a real `sigma_S` such that `D_S=C-sigma_S M_S` is a strict diagonal contraction, then the full radial block entropy is concave in `t` (`frozen_statement_v3.md:191--205`).

Independent proof check: For fixed `S`,
`C-sM_S=D_S+(\sigma_S-s)M_S` (`proof/04_diagonal_active_sector.md:168--178`). This is the same affine line through the strict diagonal anchor `D_S`, with a translated scalar parameter. D therefore gives concavity of `s -> H(C-sM_S)` on the legal interval for that conditional line, and the same weighted-sum/radial-lifting argument closes the global `t` result (`proof/04_diagonal_active_sector.md:181`).

Strictness check: The strict diagonal contraction hypothesis is not cosmetic. C3/D requires the anchor diagonal entries to lie strictly between 0 and 1. PR43 states that strictness (`frozen_statement_v3.md:199--205`) and the proof tells implementers to check both the off-diagonal ratio equations and `0<D_S<I` (`proof/04_diagonal_active_sector.md:183--189`). Cases where `M_S=0` and `C` is non-diagonal may still be concave, but they are outside this sufficient criterion rather than counterexamples to it.

Verdict: `CORRECT`.

## K. Density-adjoint Markov intertwining, generator, full Fisher term, and curvature identity

Statement checked: For rank-two factorization features, if a `p_C`-stationary Markov kernel has density adjoint satisfying `Q_theta^\dagger G_C=theta G_C` and `Q_theta^\dagger d_C=theta^2 d_C`, then applying the right-side channel sends `P_s` to `P_{theta s}`; in continuous time the needed density-generator conditions are `L^\dagger G_C=-G_C` and `L^\dagger d_C=-2d_C`; the entropy curvature certificate keeps the full Fisher term and true `t`-concavity is expressed by `2 mathcal I''+mathcal I' >=0` (`frozen_statement_v3.md:207--262`).

Exterior likelihood dependency: The rank-two likelihood ratio is
`r_s=1-s tr(G_A G_C)+s^2 d_A d_C`, derived by Sylvester's determinant identity and the `2 x 2` determinant formula (`proof/03_lifting_and_exterior.md:89--126`, `proof/05_exterior_markov.md:5--30`).

Density-adjoint check: `proof/07` correctly separates observables from densities. It defines `Q_theta^\dagger` by the `L^2(mu)` adjoint relation (`proof/07_markov_adjoint_and_reversible_obstruction.md:7--12`) and gives the output density formula after applying the forward Markov kernel (`proof/07_markov_adjoint_and_reversible_obstruction.md:14--19`). Substituting `Q_theta^\dagger G_C=theta G_C` and `Q_theta^\dagger d_C=theta^2 d_C` into the two nonconstant terms of `r_s` gives `r_{theta s}` (`proof/07_markov_adjoint_and_reversible_obstruction.md:22--43`). This is the right nonreversible statement; the earlier reversible-observable version in `proof/05` is only a special case.

Generator check: With directed stationary flows, stationarity is flow balance (`proof/07_markov_adjoint_and_reversible_obstruction.md:55--65`), and differentiating the density adjoint gives the finite linear system for `L^\dagger` (`proof/07_markov_adjoint_and_reversible_obstruction.md:68--76`). The reversible constraint `r_xy=r_yx` is correctly identified as an additional restriction, not part of the general route (`proof/07_markov_adjoint_and_reversible_obstruction.md:76`).

Curvature and Fisher check: For positive interior densities, the derivative identities
`mathcal I'=<L^\dagger f,log f>` and
`mathcal I''=<(L^\dagger)^2 f,log f> + <(L^\dagger f)^2/f>` are correct because the density has total mass one (`proof/07_markov_adjoint_and_reversible_obstruction.md:78--87`). The second term is the full complete-configuration Fisher term; no event deletion or projection is introduced. The relation to true `t` curvature follows from `s=t^2`: `proof/05` computes
`-d^2 H/dt^2=(2/s)(2 mathcal I''+mathcal I')` (`proof/05_exterior_markov.md:163--195`), so for `s>0` the nonpositivity of `H''(t)` is equivalent to `2 mathcal I''+mathcal I' >=0`.

Boundary and notation note: The divided formula is not a literal formula at `s=0`; `t=0` and feasible endpoints require the finite-event continuity/differentiability argument used elsewhere. Also, `proof/07` line 89 writes `2 I''+I'` while the precise notation in the frozen statement and `proof/05` is `2 mathcal I''+mathcal I'`. I treat this as notation/scope tightening, not a critical mathematical gap, because `proof/05` supplies the exact chain-rule calculation.

Counterexample attempts: The reversible obstruction in M does not refute K, because K uses density adjoints and explicitly leaves nonreversible stationary kernels open (`frozen_statement_v3.md:262`, `proof/07_markov_adjoint_and_reversible_obstruction.md:166--175`). The existence of a kernel/generator and the nonnegativity of the final entropy-dissipation curvature are also explicitly left open, so K is a correct framework statement rather than a completed general concavity theorem.

Verdict: `CORRECT`.

## L. Diagonal exterior-degree closure

Statement checked: For diagonal `C`, `G_C(T)=sum_i z_i(T)v_i v_i^T` and `d_C(T)=sum_{i<j}z_i(T)z_j(T)det(v_i,v_j)^2`; independent coordinate refresh multiplies the degree-one score by `theta` and the distinct-coordinate degree-two terms by `theta^2` (`frozen_statement_v3.md:264--282`).

Independent proof check: For `C=diag(c_i)`, the inverse diagonal entry of `Y_T=C-E_{T^c}` is exactly
`z_i(T)=(1_{i in T}-c_i)/(c_i(1-c_i))` (`proof/05_exterior_markov.md:63--83`). The `2 x 2` Cauchy--Binet expansion gives only cross terms `z_i z_j det(v_i,v_j)^2`, because each rank-one self term has zero determinant (`proof/05_exterior_markov.md:86--95`). Under independent Bernoulli coordinate refresh at stationarity, each centered score satisfies `T_theta z_i=theta z_i`, and independence gives `T_theta(z_i z_j)=theta^2 z_i z_j` for `i!=j` (`proof/05_exterior_markov.md:96--110`). In this product diagonal case the refresh kernel is reversible, so the same scaling is valid for the density-adjoint formulation in K.

Verdict: `CORRECT`.

## M. Reversible exterior semigroup obstruction

Statement checked: For
`C=[[1/2,1/10],[1/10,1/2]]` and `V=I_2`, the inner product
`<d_C,(G_C)_{12}>_mu=-125/78 != 0`, ruling out a `mu`-reversible Markov kernel with eigenvalues `theta` on `G_C` and `theta^2` on `d_C` for `0<theta<1`, and ruling out the corresponding reversible generator (`frozen_statement_v3.md:284--299`).

Independent arithmetic check: The event probabilities are `mu=(6/25,13/50,13/50,6/25)` (`proof/07_markov_adjoint_and_reversible_obstruction.md:100--110`). Since `mu(T)d(T)=(-1)^{2-|T|}`, the desired inner product is the signed sum of the `(1,2)` entries of the four inverse event matrices (`proof/07_markov_adjoint_and_reversible_obstruction.md:112--124`). The signed off-diagonal contributions are
`-5/12`, `-5/13`, `-5/13`, and `-5/12`, summing to
`-10/12-10/13=-5/6-10/13=(-65-60)/78=-125/78` (`proof/07_markov_adjoint_and_reversible_obstruction.md:127--139`).

Reversible obstruction check: If `Q_theta` is self-adjoint in `L^2(mu)` and scales `G_12` by `theta` and `d` by `theta^2`, then
`theta<d,G_12>=<d,QG_12>=<Qd,G_12>=theta^2<d,G_12>`, impossible for `0<theta<1` because the inner product is nonzero (`proof/07_markov_adjoint_and_reversible_obstruction.md:142--164`). The generator version is the infinitesimal analogue with eigenvalues `-1` and `-2`. The proof correctly limits the obstruction to reversible mechanisms and does not claim a nonreversible obstruction (`proof/07_markov_adjoint_and_reversible_obstruction.md:166--175`).

Verdict: `CORRECT`.

## N. Occupation-channel obstruction

Statement checked: The two correlated kernels `K_+` and `K_-` have the same complete occupation law, but after the quasi-free affine decay `K -> theta K+(1-theta)A_0` with `theta=1/2`, their full-event probabilities are `91/400` and `99/400`; hence no single classical stochastic kernel depending only on the input occupation distribution can represent this correlated fixed-point quasi-free decay for all inputs (`frozen_statement_v3.md:301--319`).

Independent arithmetic check: For a two-mode kernel with diagonal entries `a=b=1/2` and off-diagonal `c`, the complete event probabilities depend on `c^2`; hence `K_+` and `K_-` have identical occupation laws (`proof/06_quantum_measurement_obstruction.md:5--34`). The affine decay sends the off-diagonal entries to `3/20` and `1/20` (`proof/06_quantum_measurement_obstruction.md:36--60`). Thus the `11` event probabilities are `1/4-(3/20)^2=91/400` and `1/4-(1/20)^2=99/400` (`proof/06_quantum_measurement_obstruction.md:62--70`). A classical stochastic matrix on occupation probability vectors would give identical outputs from identical inputs, so the contradiction is immediate (`proof/06_quantum_measurement_obstruction.md:74--80`).

Quasi-free CPTP mapping check: Dierckx--Fannes--Pogorzelska, arXiv:0709.1061, state in Proposition 8 that quasi-free maps include the symbol update `Q -> A^*QA+B` and give the CP condition `0<=B<=1-A^*A` (arXiv PDF lines 1121--1125). Their Section 5.1 also records that these maps send gauge-invariant quasi-free states to gauge-invariant quasi-free states by that symbol update (arXiv PDF lines 961--964). For PR43's map choose the paper's `A=sqrt(theta) I` and the paper's `B=(1-theta)A_0`. Since `A_0` has eigenvalues `3/10` and `7/10` (`proof/06_quantum_measurement_obstruction.md:38--49`), `0<=(1-theta)A_0<=(1-theta)I=I-A^*A`, so the map used in N satisfies the cited quasi-free CP hypothesis.

Scope check: The proof states the correct limitation: it does not deny the quasi-free quantum channel or quantum relative-entropy data processing; it only says fixed occupation-basis measurement is not a sufficient statistic for this correlated fixed-point decay (`proof/06_quantum_measurement_obstruction.md:82--88`). It also distinguishes this obstruction from the older whole-block refresh mismatch (`proof/06_quantum_measurement_obstruction.md:84--88`) and from the remaining rank-two entropy obligations (`proof/06_quantum_measurement_obstruction.md:90--118`).

Verdict: `CORRECT`.

## Residual limits

The review accepts only the frozen PR43 D and I--N claims in their stated scope. It does not prove the imported C3 theorem anew, certify novelty, certify any formal proof, or resolve the open general rank-two / general real / complex Hermitian entropy-concavity problems listed in the frozen statement (`frozen_statement_v3.md:320--322`).

Recommended noncritical clarification: in K, add one sentence saying that `2 mathcal I''+mathcal I' >=0` is the interior `s=t^2>0` curvature certificate for the true `t`-path, while `t=0` and legal boundary points are obtained by the finite-event continuity arguments already used in the radial proof.
