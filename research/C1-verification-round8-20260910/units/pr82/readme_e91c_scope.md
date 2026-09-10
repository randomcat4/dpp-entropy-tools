# PR82 README e91c delta-FIRST frozen scope

## Frozen object

This is a source-only FIRST review of the PR82 README-only delta
`5e0861e4725d35c9e9b408c45c45291e121d5011...e91c17333c2e2c3e86d8f6b24b29e121d3c31e75`.

Public compare:
https://github.com/randomcat4/dpp-entropy-tools/compare/5e0861e4725d35c9e9b408c45c45291e121d5011...e91c17333c2e2c3e86d8f6b24b29e121d3c31e75

Frozen source aliases read:

* `source-snapshots/pr82_readme_e91c/SOURCE_BINDING.json`
* `source-snapshots/pr82_readme_e91c/COMPARE.json`
* `source-snapshots/pr82_readme_e91c/research/I05-DPP-31-20260910/README.md`

Binding facts from the frozen metadata:

* PR: 82.
* Base: `5e0861e4725d35c9e9b408c45c45291e121d5011`.
* Head: `e91c17333c2e2c3e86d8f6b24b29e121d3c31e75`.
* Modified file: `research/I05-DPP-31-20260910/README.md`.
* README blob: `6c7190255ba37098da53131a9ac18262609b47fb`.
* README sha256: `e825f894feb7da599f9d2959f390a37a13b1ef6391bd47dfff48702f64796ddf`.
* Delta size: 7 additions and 7 deletions in the README. The successor p>8 files are unchanged by this delta and are not re-reviewed here.

## Method and exclusions

I performed source reading and ordinary analytic checking only. I did not run author code, independent checkers, finite computations, entropy jobs, interval jobs, formal tools, or arithmetic reconstruction. I did not read other FIRST/SECOND reviews, C3 opinions, later live heads, or unrelated historical review files.

This report reviews only the exact README text delta: Dobrushin source wording, Hamiltonian sign and Boolean Möbius convention, grouped closed-walk convergence wording, the corrected quartic target, and whether the original arbitrary-center `p>4` theorem remains open. It does not upgrade acceptance of the unchanged successor p>8 files.

## Scoped outcome

### ACCEPTED_SCOPED

* README lines 17--25 now locate the Dobrushin blocker directly in the primary source and no longer cite an internal source-bound FIRST addendum as evidence. This closes the wording defect in the method checkpoint.
* README line 47 correctly separates PR66's internal inverse/two-leg/equilibrium/parity claims from the external Dobrushin import; it does not use an old review result as a new proof premise.
* README lines 76--87 correctly fix the Hamiltonian convention. With `H(S)=-log det L_S` and `J_A=sum_{B subseteq A}(-1)^(|A|-|B|)H(B)`, the closed-walk expression for the Hamiltonian coefficient has the displayed positive sign, while the coefficient for `log det L_S` has the opposite sign.
* README line 87 correctly weakens the convergence statement: the closed walks are grouped at fixed length before summing, giving a finite Boolean Möbius combination of absolutely convergent trace series, without claiming absolute summability after taking absolute values of individual walks or all supports.
* README lines 188--200 correctly state the local fourth-order target for the corrected functional `F(t)=h(c+tg)+alpha t^4`. The condition `H^{(4)}(0)/24+alpha<0` is the right strict quartic condition for `F''(t)<0` at sufficiently small nonzero `t`, assuming the stated even `C^4` response hypotheses.
* README lines 3, 91--96, 210, and 214--228 preserve the essential limitation: the original arbitrary-center `p>4` theorem remains incomplete, the A2 infinite-volume/absolute-norm bridge remains missing, and finite-order response is still pending source/proof.

### INCOMPLETE / unchanged

* This README patch does not prove the original PR66 arbitrary-center `p>4` theorem.
* This README patch does not prove the infinite-volume DPP-to-A2 interaction bridge, the absolute weighted Dobrushin norm, or a fourth-order response theorem for the polynomial-memory chain.
* This README patch does not certify the unchanged successor p>8 files as a closed theorem. Their scoped status remains the one recorded in the separate `successor_5e08_*` reports.

### NEEDS_FIX

None for this README-only delta.

### PENDING_C2

None. The delta contains no finite numerical claim requiring an independent arithmetic contract.
