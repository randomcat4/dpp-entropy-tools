# I05-22 R5: paired logit compression and global q/qbar imbalance curvature

Status: **PROVED (author proof; partially FIRST-reviewed, later deltas PENDING_REVIEW)** for the exact paired-logit compression and global imbalance lemmas originally recorded here. The later files on this branch add an author proof of a shared-corner cell theorem and close one full nonzero-Lambda half-leaf shape. **INCOMPLETE** remains the general half-leaf problem, general Lambda-nonzero missing-edge entropy concavity, and general real three-point concavity. No entropy counterexample is claimed. Novelty is unassessed.

This unit starts from reviewed `main` commit `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. It reads, but does not modify or rerun, the PR70 frozen source `f7be60759fd4d65184803b6585965dc7e5ccd624`. PR70's analytic FIRST is scoped-accepted in PR78. Issue73 remains a frozen computation contract and is not executed or duplicated here. The accepted PR60 Lambda=0 theorem is used only as a boundary of scope; its 1731-term certificate is not rerun.

The original detailed proof formerly in this file is preserved in Git history at blob `ad51fb200fb44e888025507f57189d55ec7dbd1a` and commit `449465e2b424c7f284bf4e8317d95966f6743371`. Its Sections 2--4 received scoped C1 FIRST acceptance in PR90. The mathematical statements are summarized below so the current branch has a concise entry point without duplicating the later self-contained proofs.

## Original accepted-scope result

For the strict connected missing-edge arrow

```text
K=[[x,0,b],[0,y,c],[b,c,z]],
v=x(1-x), w=y(1-y),
b^2=Av, c^2=Bw,
z=q+A(1-x)+B(1-y),
qbar=1-A-B-q,
0<x,y<1, A,B,q,qbar>0,
```

the accepted PR70 positive-pivot reduction is

```text
E_H=L0+L1+diag(1/v,1/w)
    -(C0+C1)(Y0+Y1)^(-1)(C0+C1)^T.
```

Pair the two conditional sides with

```text
psi(t)=t log t+(1-t)log(1-t),
g=psi'=log(t/(1-t)),
f=psi''=1/[t(1-t)].
```

All transcendental dependence of the paired matrices is compressed to

```text
ell, k, lambda, J,
```

where

```text
J(q)=int_0^A int_0^B f(q+a+b) db da,
lambda(q)=J'(q),
J(qbar)=J(q).
```

The paired acceleration scalar is

```text
n=A k+B ell-J+lambda(A mu+B nu),
mu=2x-1, nu=2y-1.
```

Since `f''>=32`, with `q0=(1-A-B)/2`,

```text
sign lambda=sign(q-q0),
abs(lambda)>=32AB abs(q-q0),
J(q)>=J(q0)+16AB(q-q0)^2.
```

These facts do not by themselves prove the general determinant sign.

## Later branch results

The complete detailed continuation is split into the following files.

- `coupled_gram_fixed_shape.md`: author-only reconstruction of the first four-scalar Gram and placement attempts, including an exact negative relaxed determinant and an exact proof that it is not DPP-realizable.
- `shared_corner_cell_theorem.md`: self-contained complete-event proof that the actual shared four-corner structure yields a sufficient condition `J<12AB`; it closes the entire legal family

```text
K(q)=[[1/2,0,1/4],
      [0,1/2,1/3],
      [1/4,1/3,q+25/72]],
0<q<11/36,
```

in every nonzero real symmetric direction, proving `E_H>0` and `det E_H>0` analytically for all q.
- `shared_corner_parallel_refinement.md`: replaces the uniform edge margin by the optimal actual edge conductances and proves the sharper sufficient condition

```text
KA+KB>J/(32AB).
```

- `verify_shared_corner_cell.py` and `shared_corner_cell_check.txt`: exact same-author algebra and direct complete-eight-event checks. They are not independent review.

## Scope ledger

- The fixed shape above is **PROVED (author; PENDING_REVIEW)** on its whole legal q interval; this is not a finite filament non-hit.
- The original four-scalar compression/global imbalance unit is **ACCEPTED_SCOPED by C1 FIRST**; isolated SECOND/integration remains separate.
- The later Gram, shared-cell, optimal-conductance, and fixed-shape proofs are **PENDING_REVIEW**.
- Universal `det E_H>=0`, universal half-leaf arrows, unequal leaf diagonals, general missing-edge arrows, and general real three-point concavity remain **INCOMPLETE**.
- No PR60 Lambda-zero arithmetic, issue73 filament execution, paired-resolvent universal claim, entropy counterexample, novelty claim, CI pass, or proof-assistant certification is asserted.