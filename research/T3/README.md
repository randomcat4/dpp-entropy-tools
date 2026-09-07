# T3 certificate tools

Status: CANDIDATE.

Branch: `research/T3-certificate-tools`.

Issue: #3.

This route builds a small, auditable certificate toolchain for finite DPP
entropy calculations. The first closed-loop target is a rational-input chord
gap certificate for all-subsets DPP entropy. It is deliberately not a random
search engine and does not claim a general concavity theorem from finite
checks.

The current candidate certifies the seed `2 x 2` rational chord case in
`artifacts/seed_chord_case.json` with a strict positive entropy chord gap lower
bound, and the independent reference implementation agrees on the sign. This is
not yet marked `VERIFIED`; a fresh-context verification must be bound to the
frozen commit before that state is claimed.

## Ownership

- Main T3 instance: top-level ledger files in `research/T3/`, final integration,
  issue/PR coordination.
- Child A: `research/T3/core/` and `research/T3/core_notes.md`.
- Child B: `research/T3/reference/` and `research/T3/reference_notes.md`.
- Child C: `research/T3/specs/` and `research/T3/interface_notes.md`.

Children were instructed not to spawn further agents, not to access
`C:\canglan\`, not to interfere with other work, and not to publish server
connection details or credentials.

## First Closed Loop

Input:

- rational symmetric marginal kernel `K`;
- rational symmetric direction `D`;
- rational chord points `t0 < tm < t1`;
- requested certificate type `entropy_chord_gap`.

Exact event probabilities are computed by Mobius inversion from inclusion
minors:

```text
q_t(S) = sum_{T: S subset T subset E} (-1)^(|T|-|S|) det(K(t)_T).
```

The entropy convention is `0 log 0 = 0`. A strict positive chord certificate
must prove feasibility at the covered chord points and an outward-rounded lower
bound

```text
H(K(tm)) - ((1-alpha) H(K(t0)) + alpha H(K(t1))) > 0.
```

If any probability, logarithm enclosure, rounding direction, feasibility check,
or coverage claim is not justified, the tool must refuse to certify.
