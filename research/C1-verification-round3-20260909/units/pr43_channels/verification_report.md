# PR43 v3.1 channel/extension verification report

Reviewer: C1 round-three reviewer 3, non-author.
Current report-binding commit: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.
Historical unchanged proof/code/input commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.

Scope files written first:

- `frozen_scope.md`
- `COMPUTE_PLAN.md`

I did not read `CONSISTENCY_AUDIT.md` as mathematical evidence. I did not duplicate C2's public compute lane for full 256-event 3+5 enumeration, author verifier replay, or the directed nonreversible LP.

## Evidence run

Short exact check:

- Local script: `short_exact_checks.py`
- Runner: `run_short_checks.sh`
- Server directory: `[isolated owned execution directory]`
- Environment: Python 3.12.3, SymPy 1.13.3, NumPy 2.1.2, mpmath 1.3.0 (`short_exact_checks.version.txt:1-5`)
- Exit: `EXIT_CODE=0` (`short_exact_checks.out:20`)
- Algorithm: exact `Fraction` arithmetic from complete-event determinant `p(S)=(-1)^(n-|S|) det(K-E_{S^c})`, with no author-code import (`short_exact_checks.out:4`)

This run independently rechecked the four-state reversible obstruction, the two-input occupation-channel obstruction, and low-cost structural facts for the 3+5 fixture. It was not a full 256-event certificate.

## Verdicts

### D. External diagonal-anchor input

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

PR43 v3.1 uses the diagonal-anchor theorem as external input only (`continuation/frozen_statement_v3.md:10`). The dependency's finite statement covers every diagonal `B=diag(b_i)` with `0<b_i<1` and every Hermitian direction, with concavity on the whole feasible interval including boundary (`sources/dependency_c3/frozen_statement_v2.md:8-15`). Its proof identifies the DPP product-replacement affine family (`sources/dependency_c3/proof.md:83-112`) and extends to entire feasible rays, both signs, and the join at zero (`sources/dependency_c3/proof.md:116-124`).

PR43's calls in I/J require exactly a strict diagonal anchor plus a Hermitian affine direction; I found no added hidden hypothesis.

### I. Diagonal active sector, arbitrary rank, and 3+5 fixture

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

The proof starts from the complete-event Schur identity and entropy chain rule (`proof/01_conditioning.md:30-67`). Under `B_{:,J^c}=0` and `C_{J,J^c}=0`, each conditional matrix splits as `(C_J-sM_{S,J}) \oplus C_{J^c}` (`proof/04_diagonal_active_sector.md:67-94`). The active term is a true Hermitian affine line through the strict diagonal kernel `C_J`, so the C3 input applies; fixed positive averaging gives `s`-concavity, and the monotone `G(t^2)` lemma transfers it to the real `t` path (`proof/04_diagonal_active_sector.md:35-63`, `97-101`).

The exact 3+5 example's analytic certificate gives strict `A,C` bounds, `|t|<=1` strict legality, `rank(B)=2`, non-two-coordinate right singular plane, and non-diagonal `A,C` (`proof/04_diagonal_active_sector.md:128-164`). My short exact check independently confirms `rank(B)=2`, row relation, three active nonzero columns, and Frobenius square `22/10000` (`short_exact_checks.out:13-17`). Full 256-event enumeration is intentionally left to C2 issue 45.

### J. Per-condition diagonal anchor criterion

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

For each left configuration `S`, the hypothesis gives a strict diagonal contraction `D_S=C-\sigma_S M_S`. Then `C-sM_S=D_S+(\sigma_S-s)M_S` is the same true affine line through that diagonal anchor (`proof/04_diagonal_active_sector.md:168-181`). The proof then averages the conditional concavity with the fixed weights from the Schur chain rule and uses the same `t^2` radial lift. The finite check criterion for a concrete use is correctly stated as common off-diagonal ratios, matching zero positions, and final strict `0<D_S<I` (`proof/04_diagonal_active_sector.md:183-189`).

### K. Markov density-adjoint intertwining and curvature identity

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

The rank-two likelihood ratio is the quadratic exterior formula from `proof/03_lifting_and_exterior.md:89-126`, with zero exterior marginals in `proof/03_lifting_and_exterior.md:138-142`. The v3.1 statement correctly changes the Markov condition from a reversible observable action to the density adjoint (`continuation/frozen_statement_v3.md:207-262`). The proof verifies that if `mu Q=mu`, then a forward Markov step sends density `f` to `Q^\dagger f` (`proof/07_markov_adjoint_and_reversible_obstruction.md:7-19`), so `Q^\dagger G_C=\vartheta G_C` and `Q^\dagger d_C=\vartheta^2 d_C` imply `(Id \otimes Q)_#P_s=P_{\vartheta s}` (`proof/07_markov_adjoint_and_reversible_obstruction.md:22-43`).

The directed-flow generator equations are also correctly oriented: stationarity is flow balance, and the density generator is `(L^\dagger f)(y)=mu(y)^{-1} sum_x r_xy(f(x)-f(y))` (`proof/07_markov_adjoint_and_reversible_obstruction.md:47-76`). The entropy derivative formulas keep the full Fisher term (`proof/05_exterior_markov.md:145-161`, corrected by `proof/07_markov_adjoint_and_reversible_obstruction.md:78-89`). The chain rule gives `-H_tt=2I_s'+4sI_s''=(2/s)(2 mathcal I''+mathcal I')`, hence the coefficient and sign in the `2 mathcal I''+mathcal I' >= 0` test are right for `s>0` (`proof/05_exterior_markov.md:165-207`).

Boundary note: the displayed `2/s` formula is an interior `s>0` identity. At `t=0`, strict interior entropy is analytic and the exterior zero-mean identities give `I_s'(0)=0`; closed legal endpoints are handled by function-value continuity when such an inequality proves interior concavity. This is a scope/care-in-writing note, not a critical proof gap. General related-block existence and automatic curvature sign remain explicitly open (`continuation/frozen_statement_v3.md:260-262`, `320-326`).

### L. Diagonal exterior Walsh degree closure

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

For diagonal `C`, `Y_T^{-1}` is diagonal with entries `z_i(T)`, so `G_C` is a degree-one sum in the centered coordinate scores and `d_C` is a degree-two sum over distinct pairs by Cauchy-Binet (`proof/05_exterior_markov.md:65-94`). Independent coordinate refresh multiplies `z_i` by `\vartheta` and `z_i z_j` by `\vartheta^2` for `i != j` (`proof/05_exterior_markov.md:96-110`). This exactly supplies K's adjoint/eigenfunction condition in the diagonal case.

### M. Reversible exterior semigroup obstruction

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

For `C=[[1/2,1/10],[1/10,1/2]]`, the proof computes `mu=(6/25,13/50,13/50,6/25)` and reduces `<d,G_12>` to the signed sum of four inverse off-diagonal entries (`proof/07_markov_adjoint_and_reversible_obstruction.md:91-139`). My independent exact check gives the same event law, signed entries `[-5/12,-5/13,-5/13,-5/12]`, and inner product `-125/78` (`short_exact_checks.out:5-8`).

If a `mu`-reversible Markov kernel had eigenvalues `\vartheta` on `G_12` and `\vartheta^2` on `d`, self-adjointness would force orthogonality for distinct eigenvalues, contradicting the nonzero inner product (`proof/07_markov_adjoint_and_reversible_obstruction.md:142-164`). The theorem's boundary is also correctly stated: this only excludes universal reversible exterior noise, not DPP concavity, nonreversible adjoint mechanisms, hidden-state dilations, or conditional Schur compensation (`proof/07_markov_adjoint_and_reversible_obstruction.md:166-177`).

Stale generated payload fields that still say reversible should be treated as a payload/documentation defect only. They do not refute theorem K or M, provided the theorem/proof text and C2 LP use the directed v2 equations.

### N. Quasi-free decay versus classical occupation-channel obstruction

Status: `CORRECT`.
Repository mapping: `ACCEPTED_SCOPED`.

The two input kernels `K_+` and `K_-` have the same two-point complete-configuration law because it depends on `c^2`; the proof lists `p_11=6/25`, `p_10=p_01=13/50`, `p_00=6/25` (`proof/06_quantum_measurement_obstruction.md:5-35`). Under `K -> \vartheta K+(1-\vartheta)A_0` with `\vartheta=1/2`, the two output off-diagonal entries are `3/20` and `1/20`, giving full-event probabilities `91/400` and `99/400` (`proof/06_quantum_measurement_obstruction.md:36-72`). My independent exact check reproduces the identical inputs and different outputs (`short_exact_checks.out:9-12`).

Thus no single stochastic map on occupation probability vectors can represent this quasi-free fixed-point decay for all inputs, since identical input probability vectors would have to produce identical outputs (`proof/06_quantum_measurement_obstruction.md:74-80`). The proof explicitly avoids claiming a quantum data-processing violation (`proof/06_quantum_measurement_obstruction.md:82`). The primary-source dependency for existence of the quasi-free CPTP symbol map is Dierckx, Fannes, and Pogorzelska, "Fermionic Quasi-free States and Maps in Information Theory", arXiv:0709.1061, Section 5.1 and Proposition 8; with `A=sqrt(vartheta) I` and `B=(1-vartheta)A_0`, the condition `0 <= B <= I-A* A` is met in this example.

## Remaining obligations

- Attach or cross-reference C2 issue 45 public certificates for the full author verifier replay, full 3+5 256-event enumeration, and directed nonreversible LP. I did not duplicate them.
- Keep K's theorem text tied to density adjoints and directed flows. Any stale reversible labels in generated payloads should be cleaned before publication packaging, but they are not mathematical proof gaps in the v3.1 theorem/proof pair.
- Novelty remains unreviewed.
