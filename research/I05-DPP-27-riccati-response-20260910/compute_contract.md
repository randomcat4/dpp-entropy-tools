# Issue74 continuum job amendment: three-Poisson residual certification

Status: REQUESTED / NOT CLAIMED HERE / NOT RUNNING HERE. Intended executor: Codex or a local verification agent. This is a concrete alternative implementation of issue74's ORIGINAL continuum task, not a second concurrent 120-minute budget. The completed PR77 fixed-point C2 job is separate and must not be rerun under this request. Before starting, read the newest issue74 claims; an active continuum owner must agree on the handoff instead of launching a duplicate.

## Frozen source, object and scope

Mathematical source: PR91, `proof.md`, `curvature_certificate.md`, `coding_and_fisher.md`, as present at author branch commit a5a60970b914dcef353fb52494766e063eba6808. These are AUTHOR_PROOF/PENDING_REVIEW, not accepted independent premises. Read and reconstruct the critical identities and constants. The source does not inherit PR77 finite signs, PR79 tail lower bounds, or finite-HMM assumptions.

Exactly t in [1/2,3/2], f_t=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8. Every computation concerns the genuine affine correlation-kernel direction. Correction state Q is symmetric 2x2, ||Q||_2<=1/8. Use all four signs alpha=(a,b), D_alpha=[[a/2,t/16],[t/16,b/2]], E=[[1/8,0],[t/16,1/8]], g_alpha=ab det(D_alpha-Q), T_alpha=E(D_alpha-Q)^(-1)E^T.

Exact global inputs: epsilon=81/1024, branch contraction 34/81, full weighted-kernel contraction 4363/5184. The true rate is half the invariant average of B=-sum g log g. Do not replace it by quantum entropy, a principal inclusion determinant, or the entropy rate of an assumed finite HMM.

The degree-10 t=5/4 scout is OPTIONAL trial-generation guidance only. Its sampled residuals are not trusted bounds and its original coefficient archive is private Drive fallback. All mathematical inputs and public trial-generation source are in PR91; an executor can generate fresh trials independently and must freeze the exact coefficients it actually certifies.

## Required algorithm

1. Independently implement the four rational maps, weights and fixed-Q parameter derivatives. Check signed complete-event products and genuine first/second t jets against an independent inclusion-minor/Mobius implementation at lengths 2,4,6. Check normalization and all rare events. Check the exact matrix inequalities, coupling constants and error-coefficient rational comparisons used below. Do not call author checker modules as the independent reconstruction.

2. Choose finite polynomial trial functions u,v,w and scalars c0,c1,c2, either constant in each rational parameter cell J or polynomial/rational in t. Begin with degree 10 in the three state coordinates. Degree 12 is allowed only within the same recorded clock, preserving the degree-10 attempt. Use rational dyadic parameter subdivisions of [1/2,3/2]. Ordinary floating least squares may GENERATE candidate coefficients but cannot certify them; freeze candidates as exact rationals before interval verification. Record the polynomial ordering and all coefficients.

3. At fixed t define L using the exact four branches and form

   r0=B-c0-(I-L)u,
   r1=B_t+L_t u-c1-(I-L)v,
   A=B_tt+L_tt u+2 L_t v,
   r2=A-c2-(I-L)w.

Here subscripts t on L denote OPERATOR derivatives, holding the trial function fixed. If coefficients depend on t, separate t_map from t_coeff, differentiate in t_map, then identify them. Include map-motion terms D u(T)T_t and D2 u(T)[T_t,T_t] in the first/second operator derivatives. B_tt includes both -(g_t)^2/g and -g_tt log g; the full law response remains in the three-Poisson formula.

4. With directed outward interval arithmetic at a fixed initial precision of 256 bits, enclose on the ENTIRE intersection B x J:

   e01>=sup ||D_Q r0||_F,
   e02>=sup ||D_Q^2 r0||_op,
   e11>=sup ||D_Q r1||_F,
   e20>=sup |r2|.

Use analytic automatic differentiation and rigorous interval Taylor/Bernstein or branch-and-bound bounds, not finite differences or a sampled maximum. The semialgebraic domain is (1/8)I+Q>=0 and (1/8)I-Q>=0. A box can be excluded only by a proved domain-exclusion test. Record the tests and any use of global inverse/weight bounds. For raw state coordinates x=Q11,y=Q22,z=Q12, use grad norm squared rx^2+ry^2+rz^2/2 and the safe Hessian Frobenius square rxx^2+ryy^2+rzz^2/4+2rxy^2+rxz^2+ryz^2. Arithmetic and logarithm errors belong in the residual enclosures.

5. Certify each cell only when

   sup_J(c2/2)+13*e01+e02/8+6*e11/5+e20/2 < 0.

Publish the explicit upper margin. The accepted cells must cover every point of [1/2,3/2] including both endpoints. A finite c2, a sampled residual, or a selected subset of parameter cells is not a whole-interval result. Failure of this sufficient budget is not an entropy counterexample. Any rigorously positive true-curvature cell is a finding to report, but an entropy counterexample still needs the specified three fixed legal symbols and a positive Jensen difference with rigorous errors.

## Claim, resources, stopping and resumption

The executor must post an issue74 claim naming this amendment, frozen source/input/executable, assigned owner, UTC start, absolute deadline and owned PID BEFORE the first timed arithmetic/package-loading step. Preparing a design is not a running job. No work is assumed merely because Codex is available.

Maximum total elapsed budget: 7200 seconds, including candidate generation, package loading, small checks, certification, allowed degree-12 continuation and repairs. At most four CPU threads, 16 GiB RAM, no GPU. Start with one arithmetic thread; any parallel partition must be logged. This consumes the original continuum job budget rather than adding another. Do not reuse unused PR77/70 finite-job clocks.

Stop at: complete negative coverage; a rigorously positive true-curvature cell; first mathematical mismatch; demonstrated inability of the chosen residual scheme to separate within its rigorously bounded error; deadline; or memory cap. A purely mechanical implementation failure can be repaired only under the still-live original deadline and with original failure plus exact patch retained. Do not silently change precision, amplitudes, target interval, resource limits or restart the clock.

Checkpoint completed parameter cells, open cells, state boxes, exact trial coefficients, current polynomial degrees, outward residual bounds, environment, arithmetic precision, command, stdout/stderr, exit status and owned-process absence. Resume only after a NEW explicit issue authorization naming the retained checkpoint and a fresh bounded budget; completed cells need not be recomputed if their exact source/input remain unchanged. Retain all failures. Do not claim external mathematical review from a machine PASS.

## Required public deliverable

A fresh branch from main in an owned research/C2-or-agent subdirectory, linked to issue74 and PR91, with independent source, literal input JSON, trial coefficients, domain covering/exclusion certificates, all residual bounds, gap-free parameter coverage report, global strict upper margin if successful, raw execution ledger, and exact stop/resume state if incomplete. Avoid a giant opaque PASS summary. No credentials, server connection data or checksums are requested. Commit refs are sufficient source/version identifiers.

Analytic review and novelty remain distinct. No FIRST/SECOND reviewer is assumed to have accepted PR91 or begun reviewing it.
