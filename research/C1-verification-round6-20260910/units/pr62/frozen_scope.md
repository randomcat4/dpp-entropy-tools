# PR62 frozen-scope record

Reviewer: `C1 fresh PR62 first reviewer`.

Role: independent non-author mathematical FIRST reviewer for PR62, `randomcat4/dpp-entropy-tools`.

Verdict scope: source/evidence-only C1 review. I performed ordinary proof reasoning and static code inspection. I did not execute arithmetic, SymPy, author scripts, finite diagnostics, entropy jobs, tests, or formal checks.

Frozen PR head: `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`.

Frozen author base: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

Frozen prefix: `research/N4/agent24_20260909/`.

Source packet binding: `sources/pr62/SOURCE_BINDING.json` records nine added files, all with `download_hash_verified: true`, and states that the packet is from a public immutable GitHub commit. I cite the PR files below through the public-safe alias `source-snapshots/pr62/`.

## PR62 source aliases

- `source-snapshots/pr62/README.md`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `7aed571e22e5b4637949daf53ff3a5f29fa8707f`, 58 lines.
- `source-snapshots/pr62/moving_rank1_theorem.md`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `57cf8735a215bba8059e364a0ae905426c2f2873`, 310 lines.
- `source-snapshots/pr62/multiring_fixture.md`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `5ddc8b57959e655ba921ca3b6849d85457d325e6`, 176 lines.
- `source-snapshots/pr62/prior_art.md`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `2395efc17869c325217a04ed0fdc8000d6791c9b`, 94 lines.
- `source-snapshots/pr62/failure_ledger.md`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `19811a3728f33829fffbe2f5cc6b7282a073545c`, 49 lines.
- `source-snapshots/pr62/code/verify_rank1_midpoint.py`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `dbb9fa96cff42f98403817fe2984f96d22262a10`, 213 lines.
- `source-snapshots/pr62/code/probe_multiring_fixture.py`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `fd476d5d12240943ad5e24eb0e4e8c1693b4704c`, 202 lines.
- `source-snapshots/pr62/output/verify_rank1_midpoint.txt`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `3429b53381dec9ca952cc977584bb2defe9da633`, 21 lines.
- `source-snapshots/pr62/output/probe_multiring_fixture.txt`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `595f3680b4caa95765f25b6c50f61dff4a2f40ae`, 91 lines.

## Review boundaries applied

- I read `sources/AGENTS.md` before reviewing, as assigned.
- I did not read sibling PR62 review artifacts, PR69 reports, future PRs, or C1/C3 review opinions.
- I did not access, search, or traverse `excluded unrelated private directories`.
- Accepted-main material was consulted only for scoped background on PR54/PR43 separation. It was not treated as a prior review of PR62.
- External primary-source check: K. M. R. Audenaert, arXiv `quant-ph/0610146`, <https://arxiv.org/abs/quant-ph/0610146>, Theorem 1 and its classical reduction, was used only to confirm the finite-alphabet Fannes-Audenaert continuity inequality invoked in `moving_rank1_theorem.md`.

## Status categories used

- `CORRECT/ACCEPTED_SCOPED`: the reviewed claim is correct in the precise frozen scope and with the stated evidence type.
- `NEEDS_FIX`: the claim has a repairable blocking defect.
- `REFUTED`: the claim is false under its stated assumptions.
- `INCOMPLETE`: the current evidence does not establish the claim in the requested sense.
- `NOT_ASSESSED`: the topic was outside this review's audit scope and is not being used as a theorem gate.
