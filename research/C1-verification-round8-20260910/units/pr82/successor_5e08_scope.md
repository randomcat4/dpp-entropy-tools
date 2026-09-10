# PR82 5e08 successor delta FIRST scope

Status: source-only delta-FIRST review completed for the PR82 successor from `2e21cc4abd67f5b8ab486d1f61a43b4b4fb1ba9e` to `5e0861e4725d35c9e9b408c45c45291e121d5011`.

No arithmetic, author script, independent checker, finite enumeration, entropy computation, interval computation, formal verification, or new theory route was run. Previous PR82 reports were preserved.

## Immutable delta binding

Compare URL: `https://github.com/randomcat4/dpp-entropy-tools/compare/2e21cc4abd67f5b8ab486d1f61a43b4b4fb1ba9e...5e0861e4725d35c9e9b408c45c45291e121d5011`

Immutable GitHub URL base for the delta head: `https://github.com/randomcat4/dpp-entropy-tools/blob/5e0861e4725d35c9e9b408c45c45291e121d5011/`

Frozen delta source aliases:

| Alias | Lines | Git blob | SHA256 |
|---|---:|---|---|
| `source-snapshots/pr82_delta/SOURCE_BINDING.json` | n/a | n/a | `73F50522481455FD7C5DBE832D37A8BEC6693DB1C0EBB782643777C6DF40440F` |
| `source-snapshots/pr82_delta/COMPARE.json` | n/a | n/a | `8D197E58055AD36EB301DC577463E1FC26A42FC1741789244890713EB7E83F1F` |
| `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md` | 460 | `ab088c5d9b84f208f351d38f94510c5c7d2490ec` | `0A2745CAE90E001E49FA457734087C50F28903A02458E69D0BD267C00F0CE789` |
| `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8_correction.md` | 96 | `1e36e5ba49dc9644294bb83b62a0713adecc7dd6` | `6ED0ECF079E8EDE1AEAB9B4B035DFC57002FC7A21E951B42A6D23E1C81BC409E` |

The original PR82 README remains unchanged from the prior frozen source context.

## External primary sources checked

Only the actually load-bearing cited primary sources were checked:

- Bressaud, Fernandez, Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, arXiv:math/9806132, `https://arxiv.org/abs/math/9806132`.
- Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:2205.12561, `https://arxiv.org/abs/2205.12561`.

Dobrushin 1974 was not needed for this successor delta. Old PR66 FIRST/SECOND reports and C3 opinions were not opened.

## Review exclusions

- No later live head.
- No old PR66 review files.
- No author or independent computation.
- No finite check or C2 budget.
- No forbidden private tree.
- No assessment of novelty or formalization.

## Scoped outcome

`ACCEPTED_SCOPED`:

- `c4_response_p8_correction.md` has priority over the original compressed proof paragraph of Lemma 4.1 in `c4_response_p8.md`.
- With that correction, the BFG relaxation input is source-consistent: the proof uses a coarser polynomial majorant satisfying BFG's chain condition instead of treating every `B_b` observable as lying in BFG's original `V_phi` norm.
- Lemma 2.1 is acceptable as a conditional DPP derivative-memory lemma, assuming the inherited PR66 complex-disk `S_q` inverse and non-nullness inputs.
- Lemma 4.2's two-power Poisson loss is acceptable conditional on corrected Lemma 4.1.
- The threshold `p>8` is the right threshold for applying two Poisson losses with memory exponent `a=p/2`.
- The Tanaka discussion correctly refuses to use Tanaka as a black-box repair of `p>4`.

`INCOMPLETE_BRIDGE`:

- The response-regularity route is materially advanced, but the full "closed `p>8` theorem" is not certified solely by this delta because the strict quartic coefficient and `H'(0)=0` inputs are inherited from PR66/PR53 rather than re-bound and rechecked in these two files.
- The boundary/finite-memory error claim in `c4_response_p8.md` is underproved as written: the canonical truncation, stationary-law comparison, differentiated finite-memory response, and uniform remainder transfer need more detail before (6.7) can be accepted.

`PENDING_C2`: none. No finite or arithmetic check is required or authorized for this successor FIRST.

`NEEDS_FIX`: update the main file or add an inline pointer so that readers of `c4_response_p8.md` do not treat its original Lemma 4.1 proof paragraph as current. The correction file fixes the paired proof, but the main file remains misleading when read alone.
