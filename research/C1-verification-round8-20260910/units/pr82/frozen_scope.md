# PR82 C1 FIRST frozen scope

Status: source-only FIRST review completed against the frozen PR82 snapshot. No author code, mathematical script, finite enumeration, entropy computation, interval job, formal checker, live-head lookup, old reviewer report, or C3 opinion was used.

## Immutable source binding

Public PR: randomcat4/dpp-entropy-tools#82

PR82 head: `2e21cc4abd67f5b8ab486d1f61a43b4b4fb1ba9e`

PR82 base: `65e59a46b49cd2dbb5c779a4cfae8cef26441984`

Immutable GitHub URL base for PR82: `https://github.com/randomcat4/dpp-entropy-tools/blob/2e21cc4abd67f5b8ab486d1f61a43b4b4fb1ba9e/`

Frozen PR82 source aliases:

| Alias | Lines | Git blob | SHA256 |
|---|---:|---|---|
| `source-snapshots/pr82/SOURCE_BINDING.json` | n/a | n/a | `B6C20852EDA429C83174026A8EB454B9438ABAF64151528AB9FCBD0C78A9CF23` |
| `source-snapshots/pr82/research/I05-DPP-31-20260910/README.md` | 230 | `7c744e1ebde320bdd7519b4b78ce31d36d1ff5c4` | `C7F168E5E4F7A301AB28043255C12DFAC2AD411981068ED734F0032027ADAFBD` |

Out-of-scope exclusions:

- Later live commit `5e0861` and any later low-regularity files.
- PR79 reports, findings, and theory.
- Old PR66 FIRST/SECOND reports and C3 opinions. Mentions of an old review inside the README were treated only as provenance/background, not evidence.
- PR66 author code or computations.
- Any forbidden private tree.

## Primary source check

Dobrushin 1974 was consulted only as a primary-source hypothesis check for the load-bearing A1/A2 import discussion:

- Public page: `https://www.mathnet.ru/eng/sm3631`
- Public PDF: `https://www.mathnet.ru/links/65f76350e7e8dd7f8420ad19db2ee8af/sm3631_eng.pdf`
- Source PDF SHA256: `91D79D372CF4B574DB400E06AD081D38EEF793F576BB94D40C3DBE74A411C1EF`
- Pages checked: printed pp. 14--18 and 24--25.

No full PDF text is reproduced in these reports.

## Scoped outcome

`ACCEPTED_SCOPED`:

- The README's Dobrushin applicability blocker is source-consistent: the primary text separates the A1/A2 regimes so that the ordinary first-moment estimate available in PR66 does not by itself supply the A1 exponential support-cardinality condition, and A2 requires the null-state vanishing condition.
- Lemma 2.1 is accepted as a local mechanism obstruction: it gives a legal half-period-even `A_p` strict-margin center whose inverse Toeplitz kernel has a polynomial lower tail, ruling out a uniform exponential inverse-entry upgrade under the bare arbitrary-center `p>4` hypotheses.
- The finite L-ensemble Boolean Mobius/connected closed-walk formula is accepted at the finite determinant level, with its own convergence domain and sign convention caveat.
- The `C^4` response discussion is accepted only as a conditional observation about what kind of response theorem would be sufficient for local concavity.

`INCOMPLETE`:

- The original PR66 arbitrary-center `p>4` entropy theorem remains unrepaired.
- The A2 infinite-volume, boundary-term, complex-neighborhood, and Dobrushin absolute-norm bridge remains open.
- The A1 route remains open at the interaction level; Lemma 2.1 blocks only a uniform exponential inverse-localization upgrade.
- The finite-response route remains pending source/proof.

`NEEDS_FIX`: no blocking mathematical text defect was found in the frozen README under the scoped claims. For standalone public readability, the old-review path citations should be treated as provenance and the direct primary-source page facts should carry the argument.

`PENDING_C2`: no necessary finite computation is required for this FIRST acceptance. If later assigned, C2 should independently check finite determinant/Mobius identities from the stated formulas, not by importing any author computation.

Newness was not reviewed. Formalization was not performed.
