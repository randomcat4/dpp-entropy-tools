# DPP32 finite-window frontier for the parity mutual-information route

Status: AUTHOR_PROOF / PENDING_REVIEW. This is a structural supplement to CHECKPOINT.md. It is not a finite-sample substitute for the entropy-rate problem.

Let s=q^2=t^2/256 and let p_X(s) be any complete-event probability on a finite consecutive window for the fixed band-two Toeplitz kernel with diagonal 1/2, nearest-neighbor entry q, and distance-two entry b=1/8.

## Proposition: n<=3 is automatically convex in s

Every complete-event probability p_X(s) is affine in s for window size n<=3.

Proof. By the signed complete-event determinant formula, p_X is a determinant of a matrix whose q-dependence occurs only in the nearest-neighbor odd-even entries. Gauge symmetry q->-q makes p_X an even polynomial in q. For n<=3 a determinant term can use at most two q-entries, so the polynomial degree in q is at most2. Hence p_X(s)=a_X+b_X s.

Let p_X(0) be the parity-decoupled product law. The finite-window relative entropy

    D_n(s)=sum_X p_X(s) log[p_X(s)/p_X(0)]

therefore satisfies

    D_n''(s)=sum_X (p_X'(s))^2/p_X(s) >=0

whenever the complete-event probabilities are positive. Thus the first three window sizes cannot expose the unresolved acceleration term.

## First genuine obstruction at n=4

At n=4 quadratic dependence on s is already present. For the all-occupied event, direct determinant expansion gives

    p_1111(s)=(64s-25)(64s-9)/4096
             =s^2-(17/32)s+225/4096.

For the all-empty event,

    p_0000(s)=s^2-(33/32)s+225/4096.

Hence p_X'' is no longer identically zero, and

    D_n''(s)=sum_X (p_X')^2/p_X
              +sum_X p_X'' log[p_X/p_X(0)]

contains the exact acceleration contribution from n=4 onward. The second sum has no termwise sign in general. Therefore any proof of rate convexity that argues only that the complete probabilities are affine in s is valid for n<=3 and fails structurally at n=4.

This is a method obstruction, not an entropy counterexample: no negative D_4'' or negative rate convexity is claimed. Its purpose is to locate exactly where the Poisson/invariant-law term in CHECKPOINT.md becomes mathematically unavoidable.
