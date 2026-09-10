# Frozen scope - PR80 FIRST source review

Reviewer role: fresh non-author FIRST reviewer for PR80. This is a bounded source-only review with no inherited verdict from old FIRST/SECOND reports, old opinions, author self-assessment, or executable checker output.

## Immutable source binding

Primary PR80 source:

- Alias: `source-snapshots/pr80/research/I05-29-rank2-signed-pairing-20260910/RESULT.md`
- Public URL: https://github.com/randomcat4/dpp-entropy-tools/blob/1b8c322faa6571a4da060677b757615e65594e35/research/I05-29-rank2-signed-pairing-20260910/RESULT.md
- Base: `65e59a46b49cd2dbb5c779a4cfae8cef26441984`
- Head: `1b8c322faa6571a4da060677b757615e65594e35`
- Blob: `b9c4c72068049108595ccc70a4f7e431807146bc`
- Lines read: all 245 lines

Accepted-main premises used only as scoped source premises:

- Alias: `source-snapshots/accepted_main/AGENTS.md`
- Public URL: https://github.com/randomcat4/dpp-entropy-tools/blob/65e59a46b49cd2dbb5c779a4cfae8cef26441984/AGENTS.md
- Blob: `f0c32cefd2aafaf8b7083fe8e99c3515760af9c7`
- Lines read: all 14 lines

- Alias: `source-snapshots/accepted_main/research/I05-23-middle-20260909/RESULT.md`
- Public URL: https://github.com/randomcat4/dpp-entropy-tools/blob/65e59a46b49cd2dbb5c779a4cfae8cef26441984/research/I05-23-middle-20260909/RESULT.md
- Blob: `7e981841708a117a2f07852f10eb7b4a53f93515`
- Lines read: all 309 lines

- Alias: `source-snapshots/accepted_main/research/I05-23-middle-20260909/ADDENDUM_CONDITIONAL_CENTERING.md`
- Public URL: https://github.com/randomcat4/dpp-entropy-tools/blob/65e59a46b49cd2dbb5c779a4cfae8cef26441984/research/I05-23-middle-20260909/ADDENDUM_CONDITIONAL_CENTERING.md
- Blob: `974dcaad80b763d6a058272bacb316d92d00e162`
- Lines read: all 137 lines

## Review target

This review covers only the following PR80 mathematical claims:

1. The exact signed conditional two-event decomposition in Theorem 2.1, especially the zero conditional means, diagonal `q=q'` convention, and the sign/coefficient of the mixed term.
2. The free-vector PSD obstruction in Proposition 3.1, as a method obstruction rather than an entropy counterexample.
3. The DPP-constrained ratio-cone sufficient criterion in Theorem 4.1 and its interval-family wording in Corollary 4.2.
4. Degenerate, zero-direction, equality, strictness, and local-curvature-to-chord-scope wording.

## Frozen accepted premises

The accepted source premise is the complete-law identity

`t^2 I''(t)=E_mu[Phi(u)+4y^2/q+y psi(u)]`,

with `q=1+u=1-sa+s^2b`, `y=s^2b`, `Phi(u)=4u^2/q+2u log q`, and `psi(u)=8u/q+10 log q`; see `source-snapshots/accepted_main/research/I05-23-middle-20260909/RESULT.md` lines 22-38.

The accepted conditional-centering premise is that fixed DPP marginals give, on every fixed left or right conditional fiber, `E a=E b=0`, hence `E u=E y=0`; see `source-snapshots/accepted_main/research/I05-23-middle-20260909/ADDENDUM_CONDITIONAL_CENTERING.md` lines 17-41.

## Explicit exclusions

This review does not review or prove global dense correlated rank-two whole-chord concavity. It does not certify PR58 `s=9/10` coverage by the new cone. It does not run arithmetic, Python, SymPy, author scripts, checker scripts, numerical reconstruction, interval jobs, entropy jobs, finite fixture jobs, or formal checking. Any fixture-level ratio-cone certification remains a separate C2-style finite check with frozen inputs and gates.
