## NEW AUTHORIZED REPAIR UNIT — fixed `t=5/4`, 1800-second cumulative budget

Authorization checkpoint: the old 7200-second continuum budget is closed and remains attached to terminal invalidation commit `279d4aff09ac56878d3f544f04d32ad4beeb4eaa`. Its invalid output is retained as evidence and will never be relabeled PASS. This is a new, narrower repair unit, not a reset or continuation of the old clock.

Owner: Codex primary local executor on the UIO host. Requested execution mode: one Sol/xhigh primary context, no subagents and no additional model calls. `C:\canglan\` is explicitly out of scope and will not be read or written.

New cumulative clock: start `2026-09-10T11:58:39Z`; absolute deadline `2026-09-10T12:28:39Z` (1800 seconds). Tests, symbolic package load, probes, implementation, formal execution and repairs all count. The deadline does not move. Resources: at most 2 CPU threads, 8 GiB RAM, no GPU.

### Frozen source, input and target

- Failure parent and immutable evidence: `279d4aff09ac56878d3f544f04d32ad4beeb4eaa`.
- Analytic source: accepted-scoped PR91 author head `c7a072ec4eea0c5b0f445bca5796873a9e234948`.
- Trial input: PR98 head `55649309437a78d9e5174386d8d260a4ee9c02a1`, exact published degree-10 blobs already copied under the old branch.
- New successor branch: `compute/issue74-t125-r1-repair-20260910`, rooted at `279d4aff09ac56878d3f544f04d32ad4beeb4eaa`.
- Only physical parameter: exact `t=5/4`.
- State domain for any global certificate: symmetric `Q=[[x,z],[z,y]]` with `(1/8)I+Q>=0` and `(1/8)I-Q>=0`.

The only accepted formal outcomes are: (a) a rigorous full-state-domain PR91 Hessian-only certificate at `t=5/4`; (b) a rigorous point obstruction showing that the frozen trial cannot satisfy that gate at `t=5/4`; or (c) an explicit stopped/incomplete record. None is a general entropy counterexample.

### Exact repair

The required residual is

```text
r1(Q,t)=partial_t(B+Lu)(Q,t)-c1-v(Q)+(Lv)(Q,t).
```

For every state multi-index `alpha`, the repaired extractor must use

```text
[partial_t(B+Lu)]_(alpha) - v_(alpha,t-order 0) + (Lv)_(alpha,t-order 0).
```

Only the first term is taken at parameter order one. The fixed-parameter `-v+Lv` terms must never be differentiated in `t`.

### Mandatory preflight gates before formal execution

1. **Analytic hand-check fixture.** Use explicit nonzero low-degree polynomials `u`, `v`, `w`, including a nonzero state Hessian for `v`, and the genuine parameter-dependent four-branch `L_t`. At exact `Q=0,t=5/4`, record separately `partial_t(B+Lu)`, `-v`, `+Lv`, and `partial_t Lv`; prove by an exact nonzero witness that the correct fixed-parameter assembly differs from the withdrawn old extraction.
2. **Independent derivative path.** Build the same low-degree fixture directly with a separate symbolic differentiator, not the normalized-Jet recurrence. Compare its complete `D_Q^2 r0`, complete `D_Q^2 r1`, and value `r2` against the interval-Jet enclosures. This must cover every Hessian component and the full operator-versus-trial-coefficient derivative convention.
3. **Frozen-input sanity.** Check that actual PR98 `u,v,w` are nonzero with the published 285-term ordering, all four input hashes match, probabilities are positive and sum exactly to one at the formal point, and the corrected/withdrawn `r1` extractions are demonstrably distinct.

Any failed or ambiguous test stops the unit. Tests and raw outputs are retained and may not be converted into a formal PASS.

### Formal-run and stop rules

Only after every preflight gate passes: freeze code, tests, source binding and preflight outputs in a public immutable commit; post the exact commit/blob hashes, command, waiting launcher PID, UTC release time and remaining budget; then perform exactly one formal `t=5/4` run. Use exact rational algebra and at least 256-bit outward logarithm enclosures. Sampling and finite differences may not certify anything.

Stop at the first mathematical mismatch, failed preflight, memory/deadline limit, rigorous point obstruction, or completed full-domain certificate. A mathematical error is terminal; no silent fix/retry. Mechanical failures may be repaired only inside the same deadline with all failures retained. All final claims must distinguish true curvature, certificate feasibility and raw machine output.
