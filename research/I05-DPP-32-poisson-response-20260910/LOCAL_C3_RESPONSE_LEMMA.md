# Local C3 response lemma needed by the Neumann bridge

Status: AUTHOR_PROOF / PENDING_REVIEW. Date: 2026-09-10.

This note adds only the higher-state-regularity estimate that PR91 did not state. It does not claim a C3 resolvent theorem. The estimate is for a single application of the exact complete-event four-branch operator and follows by direct differentiation.

Write

    L''A = sum_alpha [
        g_tt A(T)
        +2 g_t DA(T)[T_t]
        +g D2A(T)[T_t,T_t]
        +g DA(T)[T_tt]
    ].

All quantities are evaluated at the same physical t and state Q. Let U be a unit Frobenius state direction. From PR91/coding_and_fisher one may use

    ||T_Q|| <= k=34/81,
    ||T_t|| <= a=1/6,
    ||T_tt|| <= b=1/8,
    ||T_tQ|| <= u=352/729,
    ||T_ttQ|| < 1/2,

and from the complete-event weight identities

    sum |g_t| <= 7/64,
    sum |g_tt| <= 1/32,
    sum |Dg[U]| <= 2,
    sum |Dg_t[U]| <= 3/8.

For this family g_tt is state-independent, so D_Q g_tt=0.

Differentiate the four displayed terms once in Q and retain every product-rule contribution. The coefficients of |A|_1 are bounded by

    (1/32)k
    +2[(3/8)a+(7/64)u]
    +2b+1/2
    =11591/11664.

Here the terms respectively come from g_tt*DA*T_Q; the two derivatives of g_t DA*T_t; Dg*DA*T_tt; and g*DA*T_ttQ.

The coefficients of |A|_2 are bounded by

    2(7/64)ka
    +2a^2
    +2ua
    +kb
    =19895/69984.

These are respectively the g_t*D2A mixed term, Dg*D2A[T_t,T_t], the two T_tQ mixed terms, and D2A[T_Q,T_tt].

The sole |A|_3 contribution is

    k a^2 =17/1458.

Therefore every C3 observable A satisfies the explicit fixed-observable bound

    |L''A|_1
      <= (11591/11664)|A|_1
         +(19895/69984)|A|_2
         +(17/1458)|A|_3.                             (1)

No branch, probability derivative, state motion, or acceleration term is discarded in (1). This is a local operator estimate, not a statement that the centered resolvent is bounded on C3.

For the Neumann bridge, (1) shows precisely what remains to be supplied to obtain an analytic bound on

    G_m=sup |D_Q(B''+L''u_m+2L'v_m)|:

one needs finite bounds on |u_m|_1,|u_m|_2,|u_m|_3 and |v_m|_2, plus the corresponding finite state derivatives of B'', while |L'v_m|_1 is already controlled by the PR91 C2-to-C1 constant Cgrad. Because u_m and v_m are finite sums, these are finite regularity bounds and do not require asserting an unproved C3 Poisson solution.
