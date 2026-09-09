# Sources and Inputs

## Local task sources read

- `tasks/C1/PROMPT.md`
- `runs/C1/repo/AGENTS.md`
- `runs/C1/repo/research/C1/frozen_statement.md`
- `runs/C1/repo/research/C1/CLAIM.md`
- `runs/C1/repo/research/N3/round2/verdict.md`
- `runs/C1/repo/research/N3/round2/checkpoint.json`
- `runs/C1/repo/research/N3/round2/provenance.md`
- `runs/C1/repo/research/N3/round2/falsification/beta_zero_existence.md`
- `runs/C1/repo/research/N3/round2/falsification/root_certificate.json`
- `runs/C1/repo/research/N3/round2/falsification/beta_root_certificate.py`
- `runs/C1/repo/research/N3/round2/falsification/beta_affine_probe.py`
- `runs/C1/repo/research/N3/falsification/rank2_projection_check.py`
- `runs/C1/repo/research/N3/falsification/unequal_sparse_probe.py`
- `runs/C1/repo/research/N3/round2/review/round2_final_review_v2.md`
- `runs/C1/repo/research/N3/round2/review/beta_root_audit_results.json`
- `runs/C1/repo/research/N3/round2/review/verify_beta_root_certificate.py`
- `runs/C1/repo/research/N3/round2/verifications/index.md`

## Source labels

The current C1 task source labels from `runs/C1/repo/research/C1/CLAIM.md` are:

    baseline e988aa3003484f6368133b8bc0c668331629e369
    tree     e7c177ca74da59744443dbfcaadafd98724767ec

The old round-two reference baseline used inside inherited certificates is:

    e476db1bb056af57e883a47f470ea0f4443c1837

Outputs in this child separate the current task source from the old reference
baseline.

## Literature status

No new external theorem was used in the certificate.  The needed Rayleigh and
DPP event identities were rebuilt directly for 3 by 3 kernels from determinant
expansion.  The optional papers listed in the parent prompt remain background
only; this child did not certify novelty and did not rely on a cited theorem
from them.

Private server connection details are intentionally not recorded here.
