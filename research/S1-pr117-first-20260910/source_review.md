# Source review

## Author sources read

All seven files added by the frozen PR117 head were read as author sources:

- `README.md`;
- `arbitrary_A0_C4_proof.md`;
- `arbitrary_A0_concavity.md`;
- `operator_vs_absolute_sum_audit.md`;
- `review_contract.md`;
- `source_and_failure_audit.md`;
- `support_count_correction.md`.

Priority rules were respected.  In particular,
`support_count_correction.md` supersedes the optimistic `O(mR)` count, and
`operator_vs_absolute_sum_audit.md` supplies the final constant ledger.  The
old `README.md` condition involving an `ell^1` inverse envelope is treated as
withdrawn history, not as a premise.  The final source correction in
`source_and_failure_audit.md` was delta-reviewed at the new frozen head.

## External-source boundary

No external norm-controlled inversion, Gibbs response, Ruelle response, or
Dobrushin theorem is load-bearing in the submitted proof.  The finite matrix
steps needed for the new bridge are rederived in the packet and were audited
directly.  The Samei--Shepelska and Fang--Shin references are used only to
map the norm-control literature and explain why the initial inverse-envelope
route was not established inside this packet; this FIRST does not upgrade
either source into a theorem about the configuration-dependent complete-event
family.

The corrected wording is source-accurate.  Fang--Shin's introduction states
that Baskakov proved norm-controlled inversion for the `p=1` BGS and Jaffard
algebras in `B(ell^2)`.  Their own nonsymmetric result instead treats
`C_(p,r)` under `r>d(1-1/p)`.  Thus the old manuscript claim denying the
classical unweighted `p=1`, `ell^2` result was too strong, while the corrected
neutral statement is justified: an abstract norm-control theorem still must
be mapped to this exact word- and volume-uniform complete-event family before
it supplies the differentiated envelope.  The final PR117 proof does not need
that mapping at all.

The only imported mathematical result in the final curvature step is the
repository's previously accepted PR53 regularity-free matching floor, with
exactly the limited role stated in PR117.  This review neither reopens that
prior verdict nor imports PR53's separate analytic-response machinery.

## Reproducibility links

- Frozen PR117 tree:
  `https://github.com/randomcat4/dpp-entropy-tools/tree/70d69bf5c47282c953010518ff264cb2a7a09bf9/research/I05-DPP-35-arbitrary-A0-20260910`
- Main proof at the frozen head:
  `https://github.com/randomcat4/dpp-entropy-tools/blob/70d69bf5c47282c953010518ff264cb2a7a09bf9/research/I05-DPP-35-arbitrary-A0-20260910/arbitrary_A0_C4_proof.md`
- Operator/absolute-sum audit:
  `https://github.com/randomcat4/dpp-entropy-tools/blob/70d69bf5c47282c953010518ff264cb2a7a09bf9/research/I05-DPP-35-arbitrary-A0-20260910/operator_vs_absolute_sum_audit.md`
- Authoritative support correction:
  `https://github.com/randomcat4/dpp-entropy-tools/blob/70d69bf5c47282c953010518ff264cb2a7a09bf9/research/I05-DPP-35-arbitrary-A0-20260910/support_count_correction.md`
- Corrected source/failure audit:
  `https://github.com/randomcat4/dpp-entropy-tools/blob/70d69bf5c47282c953010518ff264cb2a7a09bf9/research/I05-DPP-35-arbitrary-A0-20260910/source_and_failure_audit.md`
- Fang--Shin primary publication:
  `https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.5802/crmath.54/`
- Samei--Shepelska primary preprint:
  `https://arxiv.org/abs/1809.04097`
