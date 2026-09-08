# Provenance and separation of roles

- T1 main: statement selection and freeze, resource allocation, graph/rational
  applicability checker, bounded regression harness, integration and records.
- Criterion author (GPT-6 Astra high): independent representation scouting and
  complete candidate proof after the main approved the exact bridge hypotheses.
- Boundary attacker (GPT-6 Astra high): independent small-matrix and boundary
  analysis; owns exploration/boundary.md and its artifacts.
- Definitions auditor (GPT-5.5 xhigh): independent public definitions and primary
  literature condition checks, without access to the candidate proof.
- Fresh proof/checker verifier (GPT-5.5 xhigh): audited pinned anonymous objects
  and the exact checker; report fresh_v1.md, STATUS: CORRECT.
- Fresh domain verifier (GPT-5.5 xhigh): independently audited only frozen
  statement, proof, and hazards without the first verdict; domain_v1.md, STATUS: CORRECT.

All research computation occurs in isolated server checkouts. Initial aggregate
resource ceiling: 8 CPU threads / 32 GiB; actual jobs are single-threaded and
small. No GPU or system dependency changes. Public files contain mathematical
and reproducibility content only. The initial three subagents cannot spawn.

The initial three direct agents completed before their slots were reused for
fresh verification contexts. There were never more than three active direct
subagents. No descendants were spawned. Frozen mathematical objects were
not rewritten during integration; artifacts/frozen_objects.json checks bytes.
The main instance corrected a bibliographic title and updated usefulness
priorities in the unreviewed administrative records only.
