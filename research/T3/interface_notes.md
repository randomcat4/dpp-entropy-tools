# T3 certificate interface handoff

Status: CANDIDATE. Mathematical conclusion: INCOMPLETE.
Owner: T3 child C. Integration target: issue #3, `research/T3-certificate-tools`.
Base commit: `96b2c3ac2fb5bb5a6b74b04e193787c1cd764c5e`.

This change supplies an executable schema check and an interface proposal, not a
strict entropy implementation or a verified mathematical certificate. Changes
are confined to this file and `research/T3/specs/`. The numerical core and
independent reference implementation remain integration dependencies.

## Read first

- [Contract](specs/contract.md): mathematical meaning, command proposals,
  refusal behavior, evidence and coverage requirements.
- [JSON Schema](specs/certificate.schema.json): request/response wire format.
- [Complexity](specs/complexity.md): implementable reductions and their proof
  obligations; no measured speedup is claimed.
- [Example request](specs/examples/scalar-curvature.request.json) and
  [illustrative response](specs/examples/scalar-curvature.response.json).
- [Contract check](specs/check_contract.py): validates the examples and rejects
  representative malformed objects. It cannot validate numerical certificates.

## Decisions for main

Version 0.1 accepts real symmetric rational affine paths `K(t) = K + t D`,
with a closed rational feasibility interval. It distinguishes point curvature,
uniform interval curvature, and one chord gap at a specified rational weight.
The entropy uses natural logarithms. Complex Hermitian inputs and entropy rates
need a later explicit extension; they must not be silently coerced.

The task shorthand `P(S)=det(K_S)` conflicts with exact-configuration entropy.
We expose `inclusion_minor[A]=det(K_A)` and obtain every `event_probability[S]`
by inclusion-exclusion. They are different named quantities in the contract.
This follows the repository's T3 instruction and the defining inclusion-event
identity in [Lyons, equation (1.1)](https://arxiv.org/html/1406.2707v1#S1).

`CANDIDATE` describes an artifact's review state; `PROVED` describes a strict
producer's conclusion about the precise requested predicate. Neither upgrades
the author to an independent verifier. An illustrative response has no executed
command, exit code, certificate hash, strict evidence, or certified coverage.

## Integration risks and next checks

1. Main must choose or adapt the proposed CLI names; no `dpp_entropy_tools`
   command is implemented here. Strict evidence file formats need to be frozen
   jointly with core/reference owners before accepting their first certificate.
2. A schema-valid response is not evidence of correctness. Consumers must check
   result binding, hashes, full domain coverage, witnesses, rounding, and the
   exact request using an independent checker. The supplied script is a contract
   smoke check only, including selected semantic guards.
3. The initial dimension cap of eight is an interface/resource choice, not a
   benchmark. Each job defaults to one thread; lane-wide resource allocation is
   still the responsibility of main. Retries must not inflate completed counts.
4. The scalar curvature example has a hand-computed expected value `-1`; it is
   deliberately unexecuted as a strict request. Main should produce a real
   certificate for it and then cross-check a coupled two-site case described in
   the contract before allowing T1/T2 to consume results.
5. No performance or novelty claim is established. Block compression must retain
   all exact configurations semantically and expose the true full-event count.

## Reproduce the contract check

From the repository root, in a local environment containing the pinned
`specs/requirements.txt` dependencies:

```text
python research/T3/specs/check_contract.py
```

This checks schema consistency, example semantics, selected refusal guards and
exact scalar arithmetic. Successful output reports contract checks only and
`certified=0`. Independent mathematical review and strict engine execution remain
outstanding. See `specs/validation.md` for the actual local check record.
