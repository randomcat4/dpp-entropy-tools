# P2-01 registered implementation

Status: INCOMPLETE. Numerical exploration, with no presumption that a counterexample exists.

The formal job has a hard 48,000 objective-call ceiling. A separate reserve of at most 2,000 calls covers local/remote validation, including failed tests and repeated validation. Their denominators are reported separately. This remains within the parent-registered 50,000-call limit. The job uses one numerical CPU thread, a 12 GiB address-space ceiling, no GPU, and an absolute 5,400-second wall deadline set on its first launch. Resumption does not change the deadline or replenish calls.

## Numerical object and strata

For n=3 through 10, compute the entire Hessian in a Frobenius-orthonormal basis of real symmetric directions and record its largest eigenpair. Four actual minimum spectral-margin strata are (0.2,0.4), (0.05,0.2), (0.01,0.05), and (0.001,0.01). A spectral parameterization sets the smaller distance to {0,1} within the chosen band and independently sets the spectral width. An arbitrary dense symmetric matrix supplies the eigenvectors and normalized intermediate eigenvalues. Taking the optional full complement covers kernels whose closest spectral endpoint is 1. Apart from repeated-spectrum parameter singularities, the parameterization covers general kernels in these strata, not a patterned symmetry family.

Each dimension/stratum cell has two restarts, one of each endpoint orientation, at most 750 objective calls per restart. Sixteen deterministic full-spectrum scouts precede full-coordinate L-BFGS-B maximization. There are 32 cells and 64 formal restarts. Optimizer convergence may end a restart below its cap; the unused calls are not automatically reallocated.

## Exact-event semantics and stability

The primary computation differentiates inclusion probabilities det K_A and applies the upper Boolean-lattice Mobius transform separately to probabilities, first derivatives, and second derivatives. It never uses an untransformed principal minor as a full event probability.

When trace(K)>n/2, the same inclusion/Mobius calculation is performed on L=I-K. The complement identity p_K(S)=p_L(S^c) maps the resulting full events back; kernel direction V maps to -V, so first derivatives change sign and second derivatives do not. This is an exact change of random indicator variables, not a change of the entropy objective or feasible kernel class. Signed-determinant event probabilities are used only as an independent algebraic diagnostic, never as the primary replacement for the Mobius probabilities.

A preserved pre-stabilization self-test failed at n=10, band (0.01,0.05), upper-endpoint orientation because direct floating-point Mobius inversion had relative error 0.0010140886 for a rare event. Its original and reproduced failures are retained and charged separately. The complement-stabilized tests include full event mapping, entropy identity, first-derivative sign reversal, second-derivative mapping, mass conservation, analytic Hessian versus signed-direction formula, and centered finite differences. Remaining diagnostic failures count as failed objective attempts.

## Durable accounting and recovery

Before each objective evaluation, an immediate SQLite transaction checks global and restart budgets, inserts a RESERVED row, and increments the spent-call counter; the transaction is committed with synchronous=FULL. Only then is the numerical objective called. The result updates that row afterward. An exception or process loss therefore cannot give its reserved budget back. Reservations left by an interrupted invocation are labeled INTERRUPTED_UNKNOWN on recovery and remain spent.

An exclusive OS file lock prevents two workers from sharing a run. Immutable configuration includes source hashes. A run must be explicitly resumed, and source/configuration changes are refused. Completed scouts are skipped by their recorded stage; an interrupted optimizer restarts from its best recorded parameters using only the remaining restart quota. The internal L-BFGS history is not preserved, so this is budget-safe warm resumption rather than bit-identical optimizer continuation.

The local smoke pauses after 17 calls and resumes for the remaining 47, yielding exactly the unique call IDs 1 through 64. A separate audit checks those IDs and counters. The supervised formal launch records the actual subprocess return code in addition to application status.

## Candidate handling

A largest Hessian eigenvalue above 1e-6 freezes K,V, spectral diagnostics, two feasible numerical chords, and an author-side alternate directional calculation. The formal run then pauses for independent recomputation. Its status remains NUMERICAL_HIT_AWAITING_INDEPENDENT_RECOMPUTATION; author checks are not certification. No tiny floating-point positive value is promoted. Failure to find a hit has no implication for the global real-symmetric conjecture.

