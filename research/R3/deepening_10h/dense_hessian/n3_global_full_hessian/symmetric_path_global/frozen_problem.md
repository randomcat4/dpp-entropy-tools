# D10-U10e frozen problem

Work in the reflection-symmetric path family

```text
K(x,a) = [[x,a,0],
          [a,x,a],
          [0,a,x]]
```

and use sign conjugacy plus complementation to restrict to

```text
0 < x <= 1/2,     0 < a < x/sqrt(2).
```

Equivalently set

```text
c = 2a^2/x^2,     0 < c < 1,
```

so `a=x sqrt(c/2)`.  The task is to attack the remaining scalar from the
reviewed U10d reduction:

```text
sigma(x,a) > 0.
```

If proved, together with the reviewed weighted-trace-zero input used by U10d,
this would close full `Sym(3)` negative-entropy-Hessian positivity for the
entire connected symmetric path family.  If not proved, freeze the smallest
remaining inequality and a reproducible high-precision two-dimensional
profile.  Finite grids are not allowed to become a theorem.
