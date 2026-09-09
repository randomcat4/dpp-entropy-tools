# Problem

The frozen S1 problem asks whether scalar stationary determinantal process entropy rate is concave:

```text
h((f+g)/2) >= (h(f)+h(g))/2
```

for fixed measurable scalar symbols `f,g:T->[0,1]`.

This rate subtask takes the first finite-degree diagnostic subfamily from the frozen theorem:

```text
f_t(x) = p + sum_{k=1}^m (a_k cos(2 pi k x) + t b_k sin(2 pi k x))
```

with fixed finite `m`, rational coefficients, and a uniform margin

```text
epsilon <= f_t <= 1-epsilon
```

at the two endpoints `t=+-tau` and at the center `t=0`.

For the supplied benchmark:

```text
m = 3
p = 1/2
a = (9/50, -3/25, 2/25)
b = (1/10, 2/25, -3/50)
tau = 1/4
epsilon = 3/50
```

The task is to produce actual entropy-rate bounds, not finite-window curvature evidence.  Since `f_{-tau}(x)=f_tau(-x)`, reflection gives `h(f_-tau)=h(f_tau)`.  A positive counterexample therefore needs certified bounds satisfying

```text
L_+ - U_0 > 0,
```

where `L_+ <= h(f_tau)` and `U_0 >= h(f_0)`.
