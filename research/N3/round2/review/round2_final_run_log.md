# N3 round2 review final run log

Working checkout:

```text
C:\game\gameproject\showa100\math\i05-successors-20260909\N3\children\review\repo
```

Branch:

```text
research/N3-review-20260909
```

Local Python used for successful round2 certificate reruns:

```text
C:\game\gameproject\showa100\comfyui\python_env\Scripts\python.exe
Python 3.12.14
numpy 2.5.1
scipy 1.18.0
mpmath 1.3.0
```

Thread environment for successful reruns:

```text
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
```

## Successful commands

Definition rebuild:

```text
<recorded in run_log.md from first round2 unit>
PID 9708
status PASS
coverage: 3 strict kernels; 3 pair-projection cross-checks; 9 Rayleigh polynomial pairs; 1 zero-edge connected sample
```

Dense weak-edge candidate:

```text
<recorded in run_log.md from first round2 unit>
PID 64148
status PASS
coverage: 2 sign branches; t=1/100,1/200,1/400; 6 asymptotic probe points; 2 exact density checks
```

Beta-zero root certificate:

```text
C:\game\gameproject\showa100\comfyui\python_env\Scripts\python.exe research\N3\round2\review\verify_beta_root_certificate.py
review PID 37660
author rerun PID 47096
exit status 0
output research\N3\round2\review\beta_root_audit_results.json
```

Coverage:

```text
fixed commits 1
author script reruns 1
bisection calls rerun 42
interval calls rerun 5
event formula samples 5
offdiag factor-two checks 120
H scaling samples 5
interval Gaussian brackets 3
whole root bracket checked true
```

Locked-odds dominance obstruction:

```text
C:\game\gameproject\showa100\comfyui\python_env\Scripts\python.exe research\N3\round2\review\verify_locked_obstruction.py
review PID 23608
author rerun PID 42080
exit status 0
output research\N3\round2\review\locked_obstruction_audit_results.json
```

Coverage:

```text
fixed commits 1
author script reruns 1
kernel calls certificate 1
direction calls certificate 1
Qlock forms 3
conditional slices 6
feasible endpoints 2
log terms 4
```

Signshortcut and degeneracy addendum:

```text
C:\game\gameproject\showa100\comfyui\python_env\Scripts\python.exe research\N3\round2\review\verify_signshortcut_and_degeneracy.py
review PID 65244
sign author rerun PID 29592
exit status 0
output research\N3\round2\review\signshortcut_degeneracy_audit_results.json
```

Coverage:

```text
sign fixed commits 1
sign author script reruns 1
sign event center count 1
sign Rayleigh pairs 3
degeneracy addenda read 1
degeneracy exact examples 1
```

## Script SHA256

```text
verify_round2_definitions.py              680ACB0024B90EEF80747025D6113D9E7BFC593A58FA514101BB05B295A5094F
verify_weak_edge_candidate.py             575D8496987C9A826B902C9C156C40E82A5D26F8EED98C87BC3A2D768D326FFB
verify_beta_root_certificate.py           E152E84CF9DF06A04F65BCDE57A37BDF9B0757FE89650F2480E73E6EEA94BDFF
verify_locked_obstruction.py              0C9466158E070C82BB57E1721DF5D87D69B7799760B12D52AABB3A3A9B053E65
verify_signshortcut_and_degeneracy.py     27FB8F3E3F392F9A8319B265E5910B011926BD809AF7B9F33C31F1EDC1261700
```

## Frozen source versions reviewed

```text
dense weak-edge candidate: 3087eb189237ec0a2d60127d0c35128f0cbcd91c
beta-zero root certificate: ab914ec2f73577907314ab3119c4d9f499b17e10
locked-odds obstruction: c6568dfe1c0c57aaf0b627e84601c35b79b22434
signshortcut obstruction: 2af6538
locked-odds historical lemma: 99205d9ac552355c148f011bb053731a8b1349f0
locked-odds degeneracy addendum: 0b6c89ef15db01385a37302e78509e0203838a74
```

## Failed or rejected attempts

```text
PowerShell status check: exit 1, used read-only $PID variable name; no file changes.
Manual beta-root rerun shell draft: rejected by automatic command safety before execution because it included recursive cleanup.
Windows python alias: exit 1, Microsoft Store stub.
Bundled Codex Python: exit 1, missing mpmath.
Empty-directory cleanup: rejected by automatic command safety; misplaced file had already been moved into the review checkout.
Weak-edge first run: exit 1, JSON serialization failed on numpy.bool_; patched script and reran successfully.
Signshortcut/degen first run: exit 1, missing old R3 rank_one_recheck.py dependency in temporary tree.
Signshortcut/degen second run: exit 1, full old R3 extraction hit Windows path-length limit; narrowed to the two needed R3 files and reran successfully.
```

No GPU use, no package installation, no system dependency changes, and no server process launch in this final unit.
