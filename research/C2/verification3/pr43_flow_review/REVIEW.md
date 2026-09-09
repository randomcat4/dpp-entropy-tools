# Independent PR43 Flow Certificate Review

Verdict: `CORRECT_WITH_SCOPE`.

I independently checked the PR43 task D directed stationary flow certificate. The certificate gives an exact nonnegative directed stationary flow whose density adjoint has eigenvectors `G11`, `G12`, `G22`, and `d=det(G)` with eigenvalues `-1`, `-1`, `-1`, and `-2`, respectively.

This review certifies only the finite Markov generator and feature-contraction claim for the fixed task D input. It does not certify entropy curvature, entropy concavity, or novelty.

## Source Binding

- Public PR47 source commit from handoff: `d1c64ef49c7055df42a496d736742d4fb9aaa904`.
- Local frozen candidate commit actually checked: `f249f897c212e49e66ec62a34fba715c47b9bce5`.
- Frozen upstream PR43 task commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.
- Task file: upstream `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:D` at the frozen PR43 commit.
- The public commit was not present in this local checkout, so the replay is bound to the local frozen commit. The handoff states the public PR47 `pr43_flow` subtree is unchanged from that frozen local commit.

The frozen JSON inputs were materialized from `f249f897c212e49e66ec62a34fba715c47b9bce5` into this review directory:

- `frozen_f249_flow_certificate.json`
- `frozen_f249_instance.json`

## Independent Method

The checker `verify_pr43_flow_independent.py` is self-contained. It does not import the candidate verifier and does not use the candidate's stored `A,b` system as an axiom.

It recomputes:

- strict positivity of `C` and `I-C` by exact principal minors;
- the full event law `mu(T)` from inclusion determinants by Mobius inversion;
- all eight matrices `G(T)=V^T(C-E_{T^c})^{-1}V` and `d(T)=det(G(T))`;
- all 56 ordered flow entries `r_xy`;
- all 8 balance equations and all 32 feature equations;
- the explicit generator rates `q_xy=r_xy/mu(x)` and `q_xx=-sum_{y!=x}q_xy`;
- the density adjoint `diag(mu)^-1 Q^T diag(mu)` to verify the four feature eigenvector equations with the correct orientation.

## Exact Findings

Both kernels are strict:

- `C` principal minors: `{1}=1/2`, `{2}=2/5`, `{3}=3/5`, `{1,2}=139/720`, `{1,3}=133/450`, `{2,3}=19/80`, `{1,2,3}=4081/36000`.
- `I-C` principal minors: `{1}=1/2`, `{2}=3/5`, `{3}=2/5`, `{1,2}=211/720`, `{1,3}=44/225`, `{2,3}=19/80`, `{1,2,3}=451/4000`.

The recomputed full-event law is positive and sums to `1`:

```text
mu(000)=451/4000
mu(001)=499/4000
mu(010)=2981/36000
mu(011)=2869/36000
mu(100)=6491/36000
mu(101)=6559/36000
mu(110)=4469/36000
mu(111)=4081/36000
```

The candidate supplies exactly 56 ordered directed flow entries, all nonnegative. The optional `nonzero_flow` field matches exactly the positive entries of `flow`.

All 40 exact constraints have zero residual:

- 8 stationary balance equations;
- 8 equations for `G11` with eigenvalue `-1`;
- 8 equations for `G12` with eigenvalue `-1`;
- 8 equations for `G22` with eigenvalue `-1`;
- 8 equations for `d` with eigenvalue `-2`.

The explicit generator `Q` has nonnegative off-diagonal rates, zero row sums, and exact stationarity `mu Q=0`. Therefore it is a finite continuous-time Markov generator and `mu` is stationary for the semigroup `exp(tQ)`.

The directed flow is not reversible. One exact asymmetry certificate is:

```text
r_000_001 = 420677961406813/8696843031960000
r_001_000 = 8656153/126480000
r_000_001 - r_001_000 = -10820517324948991/539204267981520000
```

The optional comparison against `frozen_f249_instance.json` also passed: its `mu`, all eight `G` matrices, `detG`, features, state order, and variable order match the independent recomputation.

## Artifacts

- Portable checker: `verify_pr43_flow_independent.py`
- Exact evidence JSON: `evidence.json`
- Final run metadata: `run_metadata.json`
- Private run log: dedicated review directory, `run_frozen_f249.log`.
- Private invocation metadata: dedicated review directory, `run_invocation_frozen_f249.json`.

Run status: exit code `0`, single-thread exact rational arithmetic, no GPU, no LP resolve/search. There was one earlier launcher-only failure from the Windows `python` alias before the bundled workspace Python was used; it did not execute the checker or affect the frozen replay.

## Scope Limits

No critical gaps were found in the exact directed stationary flow certificate for task D. This is not a review of task E, entropy curvature, full interval entropy dissipation, or any general concavity theorem. Novelty remains unreviewed.
