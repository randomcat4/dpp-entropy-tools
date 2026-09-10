# Frozen scope

## Version binding

- Repository: `randomcat4/dpp-entropy-tools`
- Pull request: `#113`
- Author head: `a2bced01cc5de30943b20387b7e1d260c384661e`
- Base observed at claim time: `bcbf7016e2abc6401b66f39ac9202d235ee32fad`
- Review kind: independent mathematical/source FIRST

All nine author files in `research/I05-DPP-34-small-wiener-20260910/` are included:

| Path | Blob |
|---|---|
| `README.md` | `097e2d621dcc52dc5a224ff1de27cdc52c525b07` |
| `author_self_audit.md` | `bde06aac882be680bf5a567aa5074dfc76710fd3` |
| `complete_event_loop_C4.md` | `f2bfac4a8d0c418f141dc53be1c2d88c2c0ccefc` |
| `explicit_zero_positive_moment_family.md` | `fa10cb9d9af8693c9afa5a7a50038a214231e02c` |
| `parity_matching_concavity.md` | `3aa0d324f0eac2ab338b7f4eeb18dd08fc55cee3` |
| `review_addendum.md` | `d0df208401b2d3ee2fdecb395290770d68ff48e3` |
| `review_contract.md` | `df78865e423f4ef9aeef15c27c88b1db8b64a273` |
| `route_comparison_sources.md` | `82df1d44dba252cefbcfa4f80878be2d422601a2` |
| `smoothness_extension.md` | `882c4cc4bc587b8ff8ebb0417f0e72a1e2a98e6d` |

## Accepted imported dependency

Only the matching lower bound is imported from the accepted PR53 packet:

\[
h(c)-h(c+t g)\ge
\frac12 d_{\rm Ber}
(\mu^2-|\widehat g(k)|^2t^2\,\|\,\mu^2).
\]

The current acceptance checkpoint is `docs/verification_round3_20260909/accepted_pr53.md`, blob `92746613904ec719685f4839dd580f2f1fcfca77`.  The underlying matching proof is in `research/I05-DPP-21-20260909/finite_range_local_theorem.md`, blob `e1c014d654d71a89c700dbd12e44fdab95cd2a9d`, at PR53 author head `ebecc412467939591e018a295a18c49a0a341ce9`.

No PR53 response regularity is imported.

## Explicit exclusions

- arbitrary `A_0` centers outside the small-Wiener ball;
- the equality boundary `r_c=min(mu,1-mu)`;
- a whole legal interval;
- arbitrary measurable or merely square-integrable symbols;
- a finite-section or selected-event substitute for the complete law;
- separate signs for the Fisher and atom-acceleration terms;
- real or complex analyticity;
- a DPP entropy counterexample;
- optimality, novelty, priority, formal verification, numerical evidence, SECOND, or merge.

A later PR113 head requires a fresh delta review.
