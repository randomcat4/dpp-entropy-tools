STATUS: CORRECT

# Domain verification report for frozen theorem v1

Reviewed commit: a71d52bc8c5b45df9ea4795343c290899a2d1f84

Reviewed mathematical file SHA256:

- `research/T1/frozen_theorem_v1.md`: 94ebb6017e5e185552806739d29ec40333bfcfae9706fd1965c8a1a3d0da89de
- `research/T1/proofs/criterion_v1.md`: 141f626b3ffea65607da9a2ed48fe6235bf1db4f9158751998c90ee23013f416
- `research/T1/hazards.md`: 3832ce03d9f0cda17a6b73f6694879e588beb897608283d5673b1928628416e2

Scope: I checked only the frozen theorem, the proof, and the risk ledger listed above. I did not use provenance, exploration notes, other verification reports, numerical scans, or external literature. The conclusion below is only a correctness judgment for the stated strict-interior bridge-supported imaginary-direction theorem, not a novelty judgment.

## Findings

No critical gap was found.

The signed Schur-complement reduction in `criterion_v1.md` lines 13-32 is correct for mixed inclusion/exclusion events. For fixed `T subset R`, the full event determinant has the block form with `Q_T = K_R - I_{R\T}` and endpoint block `K_U - I_{U\E}`. Dividing by `w_T = (-1)^{|R\T|} det Q_T` leaves exactly the sign `(-1)^{|U\E|}` in lines 23-27. This matches the frozen event-probability convention in `frozen_theorem_v1.md` lines 10-14. Since `w_T` is the marginal event probability on `R`, lines 19 and 41 also justify invertibility of `Q_T` and positivity of all four conditional endpoint events.

The proof correctly handles the possible hidden dependence on the bridge weight. In `criterion_v1.md` lines 10-19, removing the bridge separates its connected component into two sides, and all other components may be assigned arbitrarily because they have no off-diagonal connection to the bridge component. Thus `K_R` and `w_T` do not contain the bridge entry `z`. In lines 28-32, `Q_T` is block diagonal across the two sides, the `u` row of `K_{U,R}` only meets the `u` side, and the `v` row only meets the `v` side. The Schur correction is therefore diagonal, real, and independent of `z`; the endpoint off-diagonal remains exactly `z`.

The four conditional endpoint probabilities in lines 34-41 have the correct signed-event form for a two-point marginal kernel `[[a_T,z],[conj(z),b_T]]`. They sum to one, their one-point conditional marginals are `a_T` and `b_T`, and strict positivity follows from the strict interior established in lines 5-8 and the conditioning argument in line 41. Since the bridge is an existing support edge by `frozen_theorem_v1.md` lines 5-8, its center has `q=|z|^2>0`. The derivative computation in `criterion_v1.md` lines 43-59 is valid: the displayed expansion gives `r_11 r_00 - r_10 r_01 = -q`, so the logarithmic ratio is strictly below one and the partial derivative with respect to `q` is strictly negative.

The multi-bridge argument in lines 62-77 is also sufficient. In any nonzero determinant permutation term, a bridge entry cannot lie in a cycle of length at least three, because the remaining off-diagonal factors in that cycle would form an undirected cycle containing the bridge. Hence a used bridge appears only through the transposition product `K_uv K_vu = |K_uv|^2`; phases disappear event-by-event, including for mixed events with diagonal exclusion shifts. The local real parameterization by positive `q_e` in lines 67-68 is legitimate because every frozen bridge has nonzero real weight. Along the pure imaginary affine path, lines 69-75 give `q_e(t)=K_uv^2+t^2 A_uv^2`, so all first derivatives `q'_e(0)` vanish. Therefore Hessian cross terms in `F(q(t))` vanish at second order, and only the strictly negative first partials from the single-bridge calculation remain.

The stated edge cases are covered under the frozen premises. Disconnected graphs and isolated vertices are compatible with the partitioning step in line 11 and the graph procedure in line 80. Dense cyclic blocks are allowed because the application in lines 84-87 only perturbs interblock tree links, while hazards lines 13-14 correctly exclude using phase cancellation on cyclic perturbed edges inside dense blocks. Arbitrary real bridge signs are removed by the `q=|z|^2` formulation and the sign-preserving square-root parameterization in line 67. The zero direction is handled in line 77. Local two-sided feasibility follows from strict Loewner interior in lines 5-8. Boundary kernels and zero event probabilities are explicitly outside scope in `frozen_theorem_v1.md` lines 28-29 and `criterion_v1.md` lines 89-97.

The non-enumerative decision procedure in lines 79-82 decides the structural sufficient condition using exact zero information, positive-definiteness checks, bridge detection, and support containment. Its arithmetic-operation statement distinguishes exact arithmetic from bit complexity, as required by `frozen_theorem_v1.md` lines 25-26 and hazards line 19.

## Residual scope limitations

The report certifies correctness only for strict contractions, existing bridge-supported pure imaginary skew directions, and ordinary second derivative at the center. It does not certify cyclic-edge imaginary perturbations, real perturbations, boundary kernels, global line concavity, entropy rates, or novelty, all of which the frozen theorem excludes.
