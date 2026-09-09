# Formal verification scope

L0 toolchain check completed on 2026-09-09, exit 0:

```
lean +leanprover/lean4:v4.32.0 --version
Lean (version 4.32.0, x86_64-w64-windows-gnu,
commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35, Release)
lake +leanprover/lean4:v4.32.0 --version
Lake version 5.0.0-src+8c9756b (Lean version 4.32.0)
```

This matches the existing baseline A2 toolchain. Installed versions were
listed before invoking the selected version; no toolchain was installed or
changed. No N4 analytic entropy statement was translated into Lean. The
existing baseline formal artifacts check elementary matrix identities and
provide no existing bridge for the entropy derivatives, uniform Taylor
remainders, or the conditional entropy proof here. The named Mathlib cache
location was absent. We do not claim partial or full Lean certification from
this version check. Independent exact arithmetic and proof review are
recorded separately.
