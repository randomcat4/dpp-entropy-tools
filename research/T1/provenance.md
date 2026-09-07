# Provenance and separation of roles

- T1 main: statement selection and freeze, resource allocation, graph/rational
  applicability checker, bounded regression harness, integration and records.
- Criterion author (GPT-6 Astra high): independent representation scouting and
  complete candidate proof after the main approved the exact bridge hypotheses.
- Boundary attacker (GPT-6 Astra high): independent small-matrix and boundary
  analysis; owns exploration/boundary.md and its artifacts.
- Definitions auditor (GPT-5.5 xhigh): independent public definitions and primary
  literature condition checks, without access to the candidate proof.
- Fresh final verifier: pending; will receive only frozen objects and anonymous
  proof at a pinned commit, and will not repair or coauthor that proof.

All research computation occurs in isolated server checkouts. Initial aggregate
resource ceiling: 8 CPU threads / 32 GiB; actual jobs are single-threaded and
small. No GPU or system dependency changes. Public files contain mathematical
and reproducibility content only. The initial three subagents cannot spawn.
