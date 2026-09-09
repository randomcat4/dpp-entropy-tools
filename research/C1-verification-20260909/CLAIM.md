# C1 finite-kernel independent verification

Status: RUNNING. This is verification and evidence integration, not a new
open-ended exploration line. The earlier C1/PR30 author result is excluded
from self-acceptance. Only C3 may integrate into main.

Frozen first inputs:

- W1 round one only: PR32, commit 7c6e40bb3ba6dd0537f3c49bba83c718f86462fb.
- W4 T1--T3: PR33, commit 0f06eef1dc723058b46596ff9b704d7e97d3522f.
- C3 radial theorem and separate rate certificate: PR29, commit
  648f1906468e3e548410f98a6b1a53a978f2ea11.

W1 round two is a distinct supplied claim. Its author artifact arrived at
PR32 commit a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8 in the separate
`research/I05-W1-20260909-R2/` directory and is under a new review:
for fixed strict real symmetric contractions A (m by m), C (2 by 2), and
fixed real B (m by 2), the whole-configuration entropy of
K(t)=[[A,tB],[tB^T,C]] is concave on its entire feasible interval and strictly
concave if B is nonzero. Support is in actual coordinates; orthogonal
rotations are not entropy-preserving coordinate relabelings. We must check
conditional Schur probabilities, all events, degeneracies, endpoints, and
the distinction between strict Jensen concavity and a strictly negative
second derivative at every point. The first-round acceptance is not
evidence that this stronger round-two theorem has been accepted.

Three fresh nonauthor child units own W1, W4 and C3 separately. Each freezes
its exact scope and computational certificate target before running. Initial
limits: one numerical thread and at most 8 GiB per child, no GPU; total C1
cap eight CPU and 32 GiB. Heavy arithmetic uses isolated server directories.
Keep exact inputs, scripts, outputs, PID/runtime/exit records and failures.
Do not enlarge old random scans. No checksum inventory is required.

Verdicts must be ACCEPTED_SCOPED / NEEDS_FIX / REFUTED / INCOMPLETE, with exact
scope and remaining obligations. Author claims may be archived with their
unverified status. Any finding that changes a main claim is reported promptly
to the unique integrator. No descendants, fourth main instance, main merge,
external outreach, or automatic repeated scan is allowed.

The review branch is based on the already available N3 source commit
e988aa3003484f6368133b8bc0c668331629e369; only this C1 verification directory
will be changed. Public main's newer commit was not present in the local
object database, so no existing source tree or other line was overwritten.
