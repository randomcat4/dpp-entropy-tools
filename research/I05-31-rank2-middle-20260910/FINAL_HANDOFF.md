# I05-31 / PR116 final handoff

Status: **AUTHOR RESEARCH ARCHIVE / PENDING_INDEPENDENT_REPRODUCTION AND REVIEW.** This file is a closeout inventory, not a new proof, computation, review, merge authorization, or acceptance decision.

The repository main observed at closeout was `917be9e6daced79410e26298d8c490d7a0ea3a89`. PR116 was not rebased during closeout. The exact final PR head is recorded in the final PR conversation comment after this file is committed.

All mathematical statements concern complete-configuration Shannon entropy for a true affine physical-kernel path and retain all complete events, Fisher terms, and acceleration terms. No spectral entropy, affine-`L` replacement, endpoint-to-middle inference, or entropy-rate claim is included.

## Canonical conclusions carried forward

1. `RESULT_EXCHANGEABLE.md`: for the exact `alpha=1/10, beta=1/3` dense correlated `3+3` rank-two chord, the maximal legal interval is `[-1,1]` and
   `H''(t)<=-(16/625)t^2`; equivalently `H(t)+(4/1875)t^4` is concave on the closed chord.
2. `TWO_PARAMETER_ALPHA01_CHECKPOINT.md` and `TWO_PARAMETER_GLOBAL_MOMENTS.md`: the natural family
   `A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha))P`
   has maximal chord `[-1,1]`, thirteen generic complete-event likelihood types, and the displayed exact global moment formulas.
3. `RATIONAL_KERNEL_CHECKPOINT.md`, `RATIONAL_KERNEL_BERNSTEIN_ALPHA01.md`, and `RATIONAL_KERNEL_NEGATIVE_POINT.md`: all interpolation denominators are positive on the strict physical domain; pointwise positivity of the acceleration-only rational kernel is false; on the `alpha=1/10` slice the note records a continuum positive region for `u<=15/16` and an exact negative point near `u=1`. These are auxiliary-kernel statements, not entropy counterexamples.
4. `FULL_PARAMETER_ENDPOINT_PHASE.md` is the canonical endpoint phase formula. With `x=2alpha-1`, `y=2beta-1`,
   `A_norm=C_A log(1/(1-s))+O(1)` with
   `C_A=alpha(1-alpha)[7+x^2-7y^2-4xy+3x^2y^2]/3`.
   The integrated acceleration is negative in an explicit open endpoint phase. The complete Fisher has the stronger pole
   `F_norm=C_F/(1-s)+O(1)`,
   `C_F=(16alpha(1-alpha)/3)[3beta(1-beta)+alpha(1-alpha)+(beta-alpha)^2]>0`,
   so this phase is not a Shannon-entropy counterexample.
5. `ALPHA01_UNIFORM_ENDPOINT_SHARPENING.md`: at `alpha=1/10`, the full complete curvature is favorable uniformly in `0<beta<1` whenever `0<1-s<=10^-4`. This endpoint band is not used to infer the compact middle.
6. `JOINT_KERNEL_F_DIVERGENCE_IDENTITY.md` and `REVERSE_KL_JOINT_IDENTITY.md`: the full normalized curvature is the integral of the joint Fisher-acceleration kernel and equals the physical-parameter curvature of the stated normalized reverse-mixture divergence. This is an identity, not a positivity theorem.
7. `CARDINALITY_LABEL_DECOMPOSITION.md`: the full 64-event law is bijectively reorganized into the explicit `4x4` cardinality coupling plus three symmetric three-state label channels. No event is discarded.

## Retained source and actual execution evidence

The following source/output pairs are present and are the only retained literal execution outputs in this PR:

- `code/verify_exchangeable.py`
  with `output/verify_exchangeable.stdout.txt`;
- `code/certify_integrated_acceleration_negative.py`
  with `output/certify_integrated_acceleration_negative.stdout.txt`.

Both are author-side executions only. Their `PASS` text must not be promoted to independent arithmetic, mathematical review, formal verification, or acceptance.

`code/check_endpoint_phase.py` is present as a source-only algebraic checker. No literal execution output or run ledger was retained for it; therefore this PR makes no machine-PASS claim for that file.

Two finite-result notes, `RATIONAL_KERNEL_BERNSTEIN_ALPHA01.md` and `RATIONAL_KERNEL_NEGATIVE_POINT.md`, retain their exact author values but do not have standalone generator source plus literal stdout in PR116. They must be treated as **author source-text claims with finite source/output binding still missing**, and independently reconstructed before any acceptance. No output has been invented during closeout.

## Computation contract status

`JOINT_ALPHA01_EXACT_CONTRACT.md` is explicitly superseded and was never started.

The only operative future local contract is `LOCAL_CONTRACT_JOINT_KERNEL_ALPHA01.md`: one process, one CPU thread, no GPU, 16 GiB address-space ceiling, six-hour absolute wall limit, and exact checkpoint/recovery requirements. Its status remains **NOT STARTED**. No budget was consumed or reused, no server/SSH execution was requested, and no result follows from the contract.

## Unfinished items

- No proof or counterexample is established for the full compact-middle sign of `Gamma` over the natural two-parameter family.
- No full `alpha=1/10`, all-`beta`, all-`s`, all-`u` certificate for the joint kernel `J` has been run.
- No true Shannon-entropy counterexample has been found in this family.
- General dense correlated rank-two whole-chord concavity, general real-kernel concavity, and the corresponding true Toeplitz entropy-rate extension remain open.
- The PR has not received independent mathematical review or independent finite/source reconstruction for this I05-31 packet and is not approved for integration.

The empty closeout placeholder was removed. This archive now stops here for migration and independent local reproduction.
