# Post-checkpoint continuation: optimal parallel-edge criterion

Status: **PROVED (author; PENDING_REVIEW)** for the refinement below. It strictly sharpens the coarse `J<12AB` sufficient theorem in `shared_corner_cell_theorem.md`; it does not assert that the refined condition holds for every half-leaf arrow. Novelty is not assessed.

The previous checkpoint was already uploaded before this refinement was derived. No issue73 job, filament scan, PR60 arithmetic, or external worker result is used.

## 1. Optimal coefficient of one actual edge

For an actual interval `0<u<u+s<1`, define

```text
f0=f(u), f1=f(u+s),
h=g(u+s)-g(u), m=h/s,
f(t)=1/[t(1-t)], g'(t)=f(t).
```

After completing the leaf-diagonal square in the exact corner decomposition, the remaining endpoint quadratic is

```text
M_edge(X,Y)=[f1 X^2+f0 Y^2-2mXY]/8.                 (1)
```

The earlier inverse-root argument gives `m^2<f0 f1`; AM-GM then gives `f0+f1-2m>0`. Define

```text
kappa(u,s)
 =(f0 f1-m^2)/[8(f0+f1-2m)].                        (2)
```

### Lemma 1

For all real `X,Y`,

```text
M_edge(X,Y) >= kappa(u,s)(X-Y)^2.                   (3)
```

Moreover, `kappa(u,s)` is the largest coefficient for which (3) holds for every `X,Y`.

### Proof

Minimize (1) subject to `X-Y=1`, or equivalently require the determinant of the two-by-two matrix of `M_edge-kappa(X-Y)^2` to vanish at the optimal coefficient. Both calculations give exactly (2); positivity of the original endpoint matrix gives (3). The earlier `3/8` lemma says in particular

```text
kappa(u,s) >= 3/8.                                   (4)
```

The quantity in (2) is determined by the same two rational corner Fisher weights and the same edge log integral. It is not a free optimization variable.

## 2. Parallel combination of the two opposite edges

Use the actual half-leaf rectangle and notation of `shared_corner_cell_theorem.md`. Define

```text
kA_minus=kappa(q,A),
kA_plus =kappa(q+B,A),
kB_minus=kappa(q,B),
kB_plus =kappa(q+A,B),

KA=kA_minus*kA_plus/(kA_minus+kA_plus),
KB=kB_minus*kB_plus/(kB_minus+kB_plus).              (5)
```

For horizontal differences

```text
r_plus =T00-T10, r_minus=T01-T11,
Delta=r_plus-r_minus,
```

weighted Cauchy gives

```text
kA_plus r_plus^2+kA_minus r_minus^2 >= KA Delta^2.  (6)
```

The two vertical edges similarly give `KB Delta^2`. Substitution into the exact complete-event corner identity therefore improves the previous lower bound to

```text
Q_K(D)
 >= sum_edges s h [delta-(X+Y)/(4s)]^2
    +4d^2+4e^2+2Jde
    +[KA+KB-J/(32AB)] Delta^2.                       (7)
```

Every object in (7) comes from the same four corner values `q,q+A,q+B,q+A+B`.

## 3. Refined sufficient theorem

### Theorem 2

A strict connected half-leaf arrow has strictly negative complete Shannon Hessian in all six real symmetric physical directions whenever

```text
KA+KB > J/(32AB).                                    (8)
```

Equivalently its accepted two-dimensional core satisfies `E_H>0` and `det E_H>0`.

### Proof

The binary potential lies in `[-log 2,0]`, hence every rectangle satisfies

```text
0<J<2 log 2<2<4.
```

Thus the `(d,e)` quadratic `4d^2+4e^2+2Jde` in (7) is positive definite. Condition (8) makes the alternating-cell coefficient positive. Vanishing of the four completed edge squares, the `(d,e)` block, and the cell mode again forces `d=e=T=0`, hence the physical direction is zero. This is the same strictness argument as in Theorem 5.1 of the checkpoint.

By (4), each parallel pair in (5) is at least `3/16`, so `KA+KB>=3/8`. Therefore the old condition

```text
J<12AB
```

is an immediate coarse corollary of (8). The refined test retains actual endpoint placement and can certify rectangles for which the uniform `3/8` estimate is too weak.

## 4. What is and is not closed

The requested fixed shape `A=1/4,B=4/9` was already completely closed by the coarse corollary, with the analytic bound `J<13/10<4/3=12AB`. The refinement is not needed for that proof.

For general half-leaf arrows, the remaining question within this method is now the single actual scalar inequality

```text
KA+KB >= J/(32AB).                                   (9)
```

No universal proof of (9) is asserted here. Treating the four `kappa` values or `J` independently would again enlarge the realizable domain and is not a valid substitute. A long numerical test of (9) along the frozen filaments remains part of issue73 rather than this continuation.

Final classification: **PROVED (author; PENDING_REVIEW)** for Lemma 1, the exact lower bound (7), and Theorem 2. Universal (9), unequal leaf diagonals, and general missing-edge entropy concavity remain **INCOMPLETE**.