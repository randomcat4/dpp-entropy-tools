# D10-U10f exchangeable triangle subfamily

AUTHOR UNIT.  This directory is not self-certified and must be reviewed by a
fresh non-author context before any result is used as certified.

## Object

Let

```text
K(x,a)=x I_3 + a(J_3-I_3)
     = [[x,a,a],[a,x,a],[a,a,x]]
```

be a real symmetric strict DPP kernel.  Equivalently, with

```text
alpha = x+2a,      beta = x-a,
x = (alpha+2 beta)/3,  a=(alpha-beta)/3,
```

strict feasibility is

```text
0 < alpha < 1,     0 < beta < 1.
```

The requested triangle case excludes the disconnected diagonal line:

```text
a != 0, equivalently alpha != beta.
```

`H(K)` is the Shannon entropy, with natural logarithms, of the full eight-event
DPP law.  Exact atoms are always computed by Mobius inversion of inclusion
determinants, not by treating principal minors as exact events.

Let

```text
B(K) = - Hess H(K)
```

as a quadratic form on the full six-dimensional observation space

```text
(11,22,33,12,13,23),
```

where an off-diagonal coordinate means the symmetric perturbation
`E_ij+E_ji`.

## Target question

Decide whether, for every strict feasible exchangeable triangle with `a != 0`,

```text
B(K(x,a)) > 0 on all of Sym(3).
```

The goal is full six-dimensional Hessian positivity, not merely positivity
along the two-parameter exchangeable family.

If the full-domain triangle statement is not closed in this unit, the fallback
is to freeze exact reductions, genuine proved subdomains, boundary/asymptotic
information, and the smallest remaining scalar blocker.  Finite grid or random
checks are only `SCOUT`.

