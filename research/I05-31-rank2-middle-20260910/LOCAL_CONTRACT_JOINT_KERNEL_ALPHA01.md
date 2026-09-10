# Bounded local contract — alpha=1/10 joint Fisher–acceleration kernel

Status: **CONTRACT ONLY / NOT STARTED.** This is not a computation result, review, or proof. It is the required handoff if the exact three-variable expansion/certification exceeds 60 minutes. No previous PR116 execution budget is reused.

## Mathematical input

Use only the 13 exact complete-event types in `TWO_PARAMETER_ALPHA01_CHECKPOINT.md` for

`alpha=1/10`, `0<beta<1`, `0<=s<1`, `0<=u<=1`.

For every type retain its original total decoupled weight `W`,

`q=1-as+bs^2`, `v=a-2sb`, `z=(a-sb)(a-6sb)`,

`d=(1-u)+u q`.

The target is the exact joint kernel

`J(beta,s,u)=sum_types W[4v^2/d^2+2z/d]`.

Every `d` is positive on the strict physical domain. The computation must not replace the complete law by a spectral entropy, event subset, Fisher-only proxy, or a numerical probability floor.

## Exact variables and boundary factors

Use

`delta=1-s`, `w=1-u`.

Before any box subdivision:

1. combine identical denominator types exactly;
2. cancel only factors proved common to numerator and denominator over `QQ[beta,delta,w]`;
3. record the exact boundary limits at `beta=0,1`, `delta=0,1`, and `w=0,1` separately;
4. do not divide by `beta`, `1-beta`, `delta`, or `w` unless the corresponding vanishing order has first been proved symbolically.

## Primary algorithm

Use sparse exact rational polynomial arithmetic. Either of the following is admissible, with the chosen route recorded:

- clear the product of the distinct positive `d^2` denominators and certify the resulting numerator by recursive tensor Bernstein form; or
- retain the rational sum termwise and use exact Bernstein lower/upper bounds for each low-degree numerator and positive denominator on every box.

The initial box is

`beta,delta,w in [0,1]`.

A box is closed only when its exact rational lower bound for `J` is nonnegative, with strict positivity on the relative interior unless an analytically listed boundary zero applies. Otherwise bisect the coordinate with the largest normalized Bernstein range. Store the full rational box tree, the exact lower bound at every leaf, and the worst leaf.

No floating-point value may decide a sign. Floating displays may be emitted only after the exact comparison is complete.

## Counterexample branch

If an exact negative leaf is found, stop the positivity run and isolate an explicit rational point `(beta,s,u)` in that leaf with `J<0`. This is only a joint-kernel method obstruction. Then, in a separate exact stage:

1. evaluate the full `u` integral `Gamma=integral_0^1 J du` using directed rational logarithm enclosures;
2. report complete normalized Fisher and acceleration separately;
3. call it an entropy counterexample only if the final exact interval for `Gamma` is strictly negative.

## Resources

- one process, one CPU thread;
- no GPU;
- address-space ceiling: 16 GiB;
- absolute wall-clock ceiling: 6 hours;
- checkpoint interval: at most 10,000 processed boxes or 10 minutes, whichever comes first.

The implementation must report Python/CAS version, exact command, start/deadline/finish times, total CPU time, wall time, peak RSS, processed/closed/pending box counts, maximum depth, and final process absence.

## Stop and recovery contract

Stop immediately on the first arithmetic inconsistency, nonpositive denominator certificate, program exception, memory ceiling, or absolute deadline. Do not repair an input and silently rerun under the same budget.

A checkpoint must contain the exact pending-box queue, accumulated leaf certificates, polynomial/type metadata, and deterministic ordering key. A resumed run uses the remaining original six-hour deadline if the same process is recoverable; otherwise it is a new explicitly authorized run with a new ledger. No deadline reset or automatic budget expansion is allowed.

## Output

Commit, in a successor checkpoint rather than rewriting the mathematical source:

- implementation source;
- exact input/type manifest;
- exact common-factor or termwise denominator report;
- complete rational box certificate or exact negative witness;
- literal stdout/stderr and resource ledger;
- a short scope statement distinguishing author computation from independent review.
