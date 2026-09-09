# Scoped merge eligibility for PR22, PR23, PR31

Date: 2026-09-09.

Repository: randomcat4/dpp-entropy-tools.

Public heads reviewed:

| PR | Frozen head | Public tree | Local tree checked | Base |
|---:|---|---|---|---|
| 22 | 60645b4ea9e3f3a79d842b6fe039a33f9daaf7df | 5ed568031bb26ef6bbb99382fa5907582f8f1c40 | 5ed568031bb26ef6bbb99382fa5907582f8f1c40 | main |
| 23 | ffc8a7b855a9866306b3a6c22a5b4ecbc4be0d90 | 7a763443798483daa1b936a7db59c2e36aba623b | 7a763443798483daa1b936a7db59c2e36aba623b | main |
| 31 | 178eca3db82cdce495146eb8e1f16dece99f06f5 | f26902c2ba01116a7643f01cb4424340581c20c7 | f26902c2ba01116a7643f01cb4424340581c20c7 | PR23 head |

GitHub PR review objects: none for all three PRs. Existing non-author reviews are committed review artifacts inside the PR trees, not GitHub review events.

CI/status checks: no statuses and no check suites on the three frozen heads.

Draft state: all three PRs are draft PRs.

Public main context: the public API observed main at 66e807ad5825e96932679669b42d16d4cb93832e, whose first parent is b9a1d527c66bf63ba7a8b5a42dd2ba0258a1947b. PR24 is closed and merged. PR34/W2 had also advanced public main at the time of this audit.

Path conflict check: PR22 has 128 added files and PR23 has 146 added files, with zero path overlap against the current public main tree. PR31 has 62 added files, base equal to PR23 head, and zero path overlap with the PR23 tree.

## PR22

Verdict: ACCEPTED_SCOPED.

Scope accepted: archival S1 fixed-object results only.

The strict mathematical certificate accepted in the latest round is the fixed S1-R2-B1 negative entropy-rate pair-gap certificate. It treats the three symbols separately, uses six variational extreme-past kernels, enumerates 288 exact event determinants at past length four, and has a strictly negative rational gap interval. The committed non-author rate audit reports CORRECT for this fixed negative pair gap.

The first-round B0 and P0 certificates are also presented as fixed negative-pair exclusions: B0 has two committed non-author checks, and P0 has one committed non-author check of the variational refinement. The one-complex-edge proof is a finite one-edge obstruction only and is reviewed within that scope.

No accepted claim resolves Lyons-Steif Conjecture 9.2, proves a family theorem, proves all non-even directions, or establishes novelty. The PR body and S1 verdict keep the full conjecture as INCOMPLETE.

Merge eligibility: mathematically eligible as a draft scoped research archive. Process caveats are draft state, no CI, no GitHub review objects, and GitHub's live mergeability field remained unknown after the main-branch change. The all-addition path check against current public main found no path conflict.

## PR23

Verdict: ACCEPTED_SCOPED.

Scope accepted: archival N4 fixed-face and rank-three auxiliary results only.

The first-round N4 packet has one committed non-author reviewer accepting the conditional separated rare-leaf two-scale theorem, its rational Hessian premise, and the simultaneous radial-column theorem. These are restricted local/exclusion results and do not prove arbitrary nonradial N4 concavity.

The round-two packet has one committed non-author reviewer accepting the support/analyticity/Hessian shell and BSC-lift gate, the top-layer budget bound, the coarse identity, the n5 projection entropy gate, and a strict negative finite noncommuting diagnostic. The search record reports no positive candidate. The F2 result correctly treats top-layer budget failure as real but compensated by lower layers in the tested cases.

No accepted claim proves fixed-face concavity, unrestricted real-kernel concavity, or a positive counterexample. Round-two explicitly remains STOPPED_SUBSTANTIVE / INCOMPLETE.

Merge eligibility: mathematically eligible as a draft scoped research archive. Process caveats are draft state, no CI, no GitHub review objects, and GitHub's live mergeability field remained unknown after the main-branch change. The all-addition path check against current public main found no path conflict.

## PR31

Verdict: ACCEPTED_SCOPED.

Scope accepted: C2 auxiliary compensation results stacked on PR23.

The frozen C2 claims are restricted and well separated from the original five-point/global question. The accepted claims are: the explicit upper-face cone for the fixed five-point frame, low-event derivative injectivity with the exceptional pair-null family, strict negative pair log-acceleration on that exceptional family, the anisotropic upper-face inequality, and the fixed-B asymptotic expansion in its stated compact-positive range.

Two committed fresh non-author reviews report CORRECT for the frozen auxiliary claims and run independent supporting computations. The finite search remains PARTIAL: no positive full curvature, positive finite chord, or interior positive lift is claimed.

No accepted claim proves the original global five-point sign problem, the moderate-spectrum residual regime, novelty, or formal proof-assistant verification.

Merge eligibility: mathematically eligible after PR23, because PR31 is stacked on PR23 head ffc8a7b855a9866306b3a6c22a5b4ecbc4be0d90. GitHub reports PR31 as clean/mergeable against its PR23 base. Process caveats are draft state, no CI, and no GitHub review objects.

## Public-output hygiene

No credentials, tokens, server addresses, or private handoff text were found in the reviewed public markdown scan. Some committed logs/scripts/review notes retain ordinary run metadata such as PIDs and absolute execution paths. I did not classify this as a merge blocker because it does not expose connection details or authentication material. If the publication policy forbids absolute local run paths altogether, PR23 and PR31 need a small wording/log-sanitization pass before merge.

## Queue

PR31 must wait for PR23. PR22 is independent of the N4/C2 stack.

Preferred linear queue if preserving the requested order:

1. PR22
2. PR23
3. PR31

Preferred linear queue if unblocking the stack first:

1. PR23
2. PR31
3. PR22

In either queue, merge language should say "scoped archived proofs/certificates accepted" and should not say the full conjecture or full face/global problem is accepted.
