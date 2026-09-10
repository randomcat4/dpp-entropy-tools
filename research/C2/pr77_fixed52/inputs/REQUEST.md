# C3 bounded independent reconstruction: PR77 fixed harmonic values, jets and constants

Execution authorization to C2 for this fixed finite theorem unit, after PR70's separately bounded fixed-object run has terminated and its owned PID is absent. This contract does not authorize issue74 continuum work, interval subdivision, deeper conditioning, varying amplitudes, exploratory parameters, or a new theorem route. C2 owns independent arithmetic; it does not supply a mathematical FIRST or SECOND verdict.

Frozen author source: PR77 head `6ebe38dc6503120d47e9d644cfac78cfb43666f5`, exactly 18 files under `research/I05-DPP-21-fixed-harmonic-20260909/`. Use original mathematical specifications `proof.md`, `frozen_statement.md`, `point_curvature.md` and `fisher_projection.md`. Public source: https://github.com/randomcat4/dpp-entropy-tools/tree/6ebe38dc6503120d47e9d644cfac78cfb43666f5/research/I05-DPP-21-fixed-harmonic-20260909

The later 8de8b0007f9374b7a5decb9b0a2f1c939fe897be adds five files but leaves all 18 original files byte-identical. Those additions are not premises or executed input under this contract. Author PASS summaries are comparison material only; do not import or execute author checker modules. No PR59/60 theorem or earlier local-tube radius is a new premise.

## Frozen object, phases and targets

The fixed true affine symbol is

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8.

Only t=1/2,1,3/2 and conditioning depth r=18 are production inputs; complete event lengths n=18 and n=19. Toeplitz K has diagonal 1/2, first off-diagonal t/16, second off-diagonal 1/8, all further entries zero. A scaled signed event matrix is 32*(K-I_absent), hence diagonal +/-16, first off-diagonal 2t=1,2,3, second off-diagonal 4, with sign (-1)^(number absent) applied to its determinant. Jets are derivatives with respect to t, including first-entry derivative 2, not derivatives in an unscaled nearest-neighbor entry. Retain complete configurations including rare events.

Execute in a single recorded ordered run: (A) exact small constants and covariance targets; (B) independent small-size determinant/jet crosschecks; (C) production n=18/19 values and jets for the three fixed t values; (D) outward entropy, curvature and true-rate conclusions. A failure in any phase is terminal. Preparation may design a single production pass that reuses the same independently generated jets for value and curvature sums; it must not run independent redundant value/jet jobs outside this budget.

### A. Exact analytic constants and local Fisher algebra

Independently reconstruct all rational constants that carry the stated inequalities, rather than copying their PASS values:

- Uniform comparison in proof.md sections 3–4: a=13/128, b=1/8, rho=49/64, diagonal dominance 3/64, distance 0/1/2/far residuals, C=16384/3243, A0=a*rho+b, B0=A0+b*rho, and the strict rational inequality C^3*A0^2*B0^2<C0=1033420800/1263214441. Record residuals and the exact positive difference.
- Value tail E_r=(256/15)*C0^2*rho^(4r-12), especially E_18.
- Uniform derivative ingredients proof.md section 8: inverse/operator bound substitutions yielding U1=9/8,U2=37/8; binary negative-entropy derivative bounds M2=256/15,M3=57344/225,M4=27656192/3375; the Bregman constants and event-score coefficients, retaining second derivatives. Record polynomial-geometric summation identities used by the tails.
- All three point-specific disks/rhos/residuals/factors in point_curvature.md section 2: (t,d,max|z|,rho)=(1/2,1/4,3/4,2/3),(1,1/8,9/8,2/3),(3/2,1/16,25/16,3/4); a=max|z|/16,b=1/8,C=1/r0,Cstar=C^3*(a*rho+b)^2*(a*rho+b+b*rho)^2. Check each displayed residual and factor. Compute kappa1=1/d,kappa2=2/d^2 and A0,A1,A2 from (3.4), then exact Tail_18 from (3.6) summed over r>=18. Do not replace the point tails by the looser whole-interval tail.
- Existing fisher_projection.md exact covariance claims: independently build inclusion determinants for {0,1},{0,1,2},{0,1,2,3},{0,1,3,4} using polynomial rational arithmetic in u=t/16, with a second determinant construction. Compare m,c0,c1,c2,c3,V, endpoint values and positivity/monotonicity numerators, yielding the displayed 16/286141 bound. This is only an algebra certificate for the full-Fisher projection, not a sign certificate for the remaining response terms.

### B. Independent complete-event implementation

Implement the fixed Toeplitz and signed-event convention from the literal mathematical input without importing author modules. Derive and document an independent width-two determinant/jet recurrence or equivalently efficient exact algorithm. Check division remainders, sign and jet scaling exactly.

At each of the three t values, compare complete-event values with independently implemented inclusion-minor Mobius inversion through n=6 and direct signed-event determinants through n=8. Compare first and second jets with independently computed determinant polynomial interpolation or another independently implemented exact derivative method through n=6. Shared low-level integer operations are acceptable; the two event constructions must not share an author event generator or sign helper as their only source of truth. Record every finite range and exact agreement count; all crosschecks belong to this same clock.

### C. Production events and jets

For all six (t,n) pairs, enumerate all 2^n complete events exactly. Obtain N,N',N'' with p=N/32^n and its true t derivatives. Prove N>0 for each event and record exactly

    event_count=2^n,
    sum N=32^n,
    sum N'=sum N''=0.

Retain a checkable exact histogram/aggregation and a deterministic enumeration audit. It may aggregate by N with count,sum N',sum N'',sum (N')^2, sufficient to independently reconstruct the entropy, Fisher and acceleration sums. Do not replace these data by PASS summaries. Large raw records may be losslessly compressed/chunked with hashes and an explicit schema; avoid giant decimal strings in human-readable summaries. The production algorithm, complete counts, exact totals, positive minima, distinct counts and output hashes must be retained.

### D. Outward finite and true-rate inequalities

Use natural logs. At fixed precision 100, use correctly rounded Decimal.ln on exact integer N and log32, with fixed absolute widening 1e-90 before directed floor/ceiling multiplication, division, summation and subtraction. Record Python implementation/version, decimal backend/libmpdec version, all contexts, rounding modes, flags/traps and conversion rules. Derive an explicit bound ensuring the widening exceeds the log rounding error over every observed N; treat N=1 exactly. Python's official contract is https://docs.python.org/3/library/decimal.html#decimal.Decimal.ln . Merely setting a directed rounding context for ln is insufficient, since ln itself is rounded to nearest. No binary float enters any bound. Record a rigorous per-log inventory or reproducible exact integer argument histogram with all interval endpoints and arithmetic metadata.

Compute directed intervals for H_18,H_19,h_18=H_19-H_18 for each t. Compute H_n''=-(sum (N')^2/N + sum N''*log N)/32^n, retaining Fisher and acceleration separately. The log32 derivative term cancels only after the exact derivative normalization check. Obtain h_18''=H_19''-H_18''. Target arithmetic interval width <=1e-40 for these finite values and curvatures; the analytic tail is separately reported and is not an arithmetic error.

For the midpoint theorem require a strictly positive lower margin for

    lower(h_18(1))-E_18
       -(upper(h_18(1/2))+upper(h_18(3/2)))/2 - 1/10000.

Only the midpoint lower bound subtracts E_18; the endpoint upper bound uses h<=h_18. This proves one fixed true-rate concave chord. It does not prove a continuum curvature sign.

For each t, retain the true-curvature enclosure [lower(h_18'')-Tail_18,upper(h_18'')+Tail_18]. Require a strictly positive lower margin for threshold-trueUpper, with thresholds respectively -1/2500,-1/1000,-1/500. The negative-t transfer is analytic gauge symmetry, not an additional production run. Do not use H_n''/n or fit/extrapolate a sequence. Do not infer signs between the three points.

## Budget, stop rules and evidence

Single process, single CPU thread, <=16 GiB RAM, no GPU, maximum 2700 seconds elapsed for the entire object including phases A–D, mathematics package loading, tests, crosschecks, production and any eligible mechanical repair. Do not overlap with the PR70 owned process. Start the one immutable deadline at the first arithmetic/package-loading operation for this object and publish start UTC, absolute deadline, PID and exact command. Reading specifications, writing an unexecuted independent implementation, hashing, and source publication may precede the start. Freeze executable/input/request in a public preparation head before execution.

No pilot, resource microbenchmark, extra parameter, depth increase, adaptive precision, second precision, timer reset, deadline extension, continuation after mathematical mismatch or unrecorded rerun. Record and terminate at the first exact mismatch, failed positivity/normalization, insufficient interval separation, timeout or memory limit. Distinguish mathematical falsity from an unresolved certificate or implementation defect. A purely mechanical exception may be repaired only under the original still-live deadline, preserving the original failure and exact patch; a mathematical mismatch is terminal. Kill only the owned process tree and record absence afterward.

Publish raw independent implementation, mathematical inputs, exact constants/covariance evidence, small crosschecks, production histogram/jet aggregates, full directed intervals and margins, all output hashes, source bindings, environment, precise execution and failure/repair ledger. Preserve a complete run record for every generated artifact, including point curvature. Separate raw inputs/implementation/outputs/execution from machine interpretation for isolated mathematical review. C2 can declare an all-target MACHINE_PASS only if every required stage and inequality passes. Mathematical acceptance still requires independent FIRST and isolated SECOND on those actual artifacts. The continuum target and general entropy-concavity questions remain open.
