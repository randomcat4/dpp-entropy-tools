# PR81 C1 FIRST source-only review

Scoped verdict: ACCEPTED_SCOPED for the analytic content in PR81 Sections 2-4: the paired four-scalar compression and the global `q/qbar` imbalance theorem. The proof correctly reduces the paired logarithmic dependence to `ell,k,lambda,J`, proves `lambda=J'(q)`, and derives the global sign and quantitative lower bounds from complement symmetry plus `f''>=32`.

This is not an acceptance of general missing-edge entropy concavity, general real three-point concavity, or `det E_H>=0`. Those remain open exactly as the source says at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:248-267` and `:269-279`.

## Source binding

Reviewed PR81 source:

- `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md`, 279 lines, blob `ad51fb200fb44e888025507f57189d55ec7dbd1a`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/449465e2b424c7f284bf4e8317d95966f6743371/`

Scoped predecessor:

- `source-snapshots/pr70/proof.md`, 332 lines, blob `5732657cd5e5ce87d2d2409a4556379228ae3145`
- `source-snapshots/pr70/post_checkpoint.md`, 151 lines, blob `37206206cb83cfb948832ac731d34eaf966a26da`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/`

The status declarations in the author text were not used as evidence. This review used only the frozen formulas and the scoped predecessor premises supplied with the task.

## Accepted analytic points

ACCEPTED_SCOPED: domain and target are correctly frozen. PR81 uses the connected missing-edge arrow with `0<x,y<1` and `A,B,q,qbar>0` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:9-18`. Since `qbar=1-A-B-q`, every `t_ij=q+A(1-i)+B(1-j)` lies in `(0,1)`. The inherited full target is the PR70 two-dimensional core `E_H=L0+L1+diag(1/v,1/w)-(C0+C1)(Y0+Y1)^(-1)(C0+C1)^T` at PR81 `:27-35`, with `det E_H>=0` still unresolved. This matches PR70's reduction and warning at `source-snapshots/pr70/proof.md:231-259`.

ACCEPTED_SCOPED: the four-scalar paired-logit compression follows from the actual side definitions. PR70 defines `phi1(t)=t log t`, `phi0(t)=(1-t)log(1-t)`, side increments, `lambda_s`, and `J_s` at `source-snapshots/pr70/proof.md:117-130`. Summing side derivatives gives `phi1'(t)+phi0'(t)=log(t/(1-t))`, exactly PR81's `g(t)` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:39-58`. Therefore PR81's identities `ell=ell_0side+ell_1side`, `k=k_0side+k_1side`, `lambda=lambda_0+lambda_1`, and `J=J0+J1` at PR81 `:60-67` are correct.

ACCEPTED_SCOPED: the paired `L` and `C` matrices retain the PR70 side terms and collapse linearly. PR70 gives the side matrices at `source-snapshots/pr70/proof.md:136-157`; PR81's summed matrices at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:69-77` are the direct side sums after replacing side-specific quantities by `ell,k,lambda,J`. No one-sided sign assumption is used.

ACCEPTED_SCOPED: the `R` block collapse is justified. PR70's side identity `J_s=A k_s+B ell_s-n_s+lambda_s(A mu+B nu)` appears at `source-snapshots/pr70/proof.md:164-168`. Summing it gives PR81's `n=A*k+B*ell-J+lambda*(A*mu+B*nu)` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:87-95`. This verifies the requested `n` formula and keeps the side acceleration contribution through `R`.

ACCEPTED_SCOPED: full Fisher, acceleration, marginal, and mixed terms are retained. PR70's perspective differentiation includes `r''` and `P''` accelerations at `source-snapshots/pr70/proof.md:62-80`; the full side quadratic form includes `F_s+R_s` at `:149-157`; the full Shannon Schur keeps the leaf marginal `M=diag(1/v,1/w)` at `:218-227`; and the Fisher inverse identity uses all four score coordinates at `:261-292`. PR81 carries these into the paired Fisher `F=sum P_ij f(t_ij)a_ij a_ij^T` and the full core at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:95-104` and `:246-267`. The text correctly warns that a perspective or operator-mean argument cannot replace the DPP Hessian at PR81 `:223-240`.

ACCEPTED_SCOPED: the rectangle FTC identities are correct. From `t_00=q+A+B`, `t_10=q+B`, `t_01=q+A`, and `t_11=q`, PR81's identities for `ell_0`, `ell_1`, `k_0`, `k_1`, and `J(q)=int_0^A int_0^B f(q+a+b) db da` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:106-122` follow directly from `g'=f` and `psi''=f`. Differentiating under the finite rectangle gives `lambda(q)=J'(q)` at PR81 `:119-124`.

ACCEPTED_SCOPED: complement symmetry is correct. With `r=1-A-B` and `qbar=r-q`, PR81's change of variables `(a,b)->(A-a,B-b)` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:126-150` sends the argument to the complement and uses `f(1-t)=f(t)`. This proves `J(r-q)=J(q)` and, by differentiation, `lambda(r-q)=-lambda(q)`.

ACCEPTED_SCOPED: the global curvature floor is correct. PR81 computes `f''(t)=2[(1-2t)^2+u]/u^3=2(1-3u)/u^3` with `u=t(1-t)` at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:151-173`. The expression decreases on `0<u<=1/4` and is minimized at `u=1/4`, giving `f''>=32`. Integrating over the `A x B` rectangle gives `J''(q)>=32AB`.

ACCEPTED_SCOPED: the sign and lower bounds for `lambda` and `J` follow. Since complement symmetry gives `lambda(q0)=0` at `q0=r/2`, integrating `J''>=32AB` proves `sign lambda(q)=sign(q-q0)`, `|lambda(q)|>=32AB|q-q0|`, and `J(q)>=J(q0)+16AB(q-q0)^2`, as stated at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:175-200`. Equality for `lambda=0` occurs only on the balanced surface `q=qbar`; on the fundamental domain `0<q<=qbar`, PR81 correctly gets `lambda<=0`, strictly negative off balance at `:191-197`.

ACCEPTED_SCOPED: the coarse endpoint envelope is valid on the fundamental domain. PR81's bounds at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:203-219` use `t>=q` and `1-t>=qbar`, hence `4<=f(t)<=1/(q qbar)` and `f''(t)<=2/(q qbar)^3`. These are coarse but legal and do not claim determinant control.

ACCEPTED_SCOPED: PR81 states the actual implication for `E_H` correctly. The new theorem supplies `ell>0`, `k>0`, `J>0`, a sign-fixed `lambda`, and the displayed quantitative bounds at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:248-265`. The source also correctly says these scalar facts do not prove `det E_H>=0` because `lambda`, `ell`, `k`, `J`, `F`, `R`, and the marginal matrix co-vary in the exact core at PR81 `:242-267`.

## Required fix

NEEDS_FIX: the categorical wording at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:271-274` says PR70 "already refutes" the complement-paired resolvent route. The PR70 post-checkpoint finite obstruction is still independently pending C2 under this review scope. PR81 already acknowledges that status at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:5`, so line `:273` should be softened to something like: "Did not revive complement-paired resolvent convexity; PR70 records an author finite obstruction to that auxiliary route, pending independent C2 certification." This is a wording/evidence-status fix, not a gap in the PR81 Section 2-4 analytic proof.

## Pending and out of scope

PENDING_C2: the PR70 finite paired-resolvent witness remains pending independent certification. The object and exact fractions appear at `source-snapshots/pr70/post_checkpoint.md:5-35`, with reproduction notes at `:100-109`, but this C1 review did not execute or certify them.

OPEN determinant sign: `det E_H>=0` remains open, exactly as PR81 states at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:248-267`. No general missing-edge entropy concavity or real three-point entropy concavity is certified.

NOT_ASSESSED novelty: novelty is not assessed. The Kubo-Ando and Effros sources listed at PR81 `:223-240` are used only as motivation and are explicitly not treated as a DPP theorem or a bridge over the acceleration terms.

NOT_PERFORMED formal: no Lean, proof-assistant, symbolic checker, interval arithmetic, entropy finite job, or author checker was run.

Final classification: ACCEPTED_SCOPED for PR81's four-scalar paired-logit compression and global `q/qbar` imbalance theorem; NEEDS_FIX for the line `:273` evidence-status wording; PENDING_C2 for the finite paired-resolvent obstruction; OPEN for `det E_H>=0`; novelty NOT_ASSESSED; formal verification NOT_PERFORMED.
