STATUS: CORRECT

# P2 rational benchmark certificate

The requested benchmark

```text
A = [[1/2, 1/10], [1/10, 1/3]]
u = (1/5, 1/6)
v = (1/7, -1/8)
J_A(w)=h(A-ww^T)-h(A)+grad h(A):(ww^T)
```

was certified by `rational_dpp_review.py p2-benchmark` using exact event
probabilities and rational logarithm intervals with 120 atanh-series terms.

The strict-domain checks for `A`, `A-uu^T`, and `A-vv^T` all pass.

For `L_u=Hess J_A(u)`, the interval matrix satisfies:

```text
L11 upper < -0.978671407445525664851237387607874793786970441276
L22 upper < -0.795149165465754985697332884893030190906482408706
det lower >  0.776571421409817124929370298602103193137061120350
```

For `L_v=Hess J_A(v)`, the interval matrix satisfies:

```text
L11 upper < -0.517744517566096722421672372244189548974846953784
L22 upper < -0.474814191554589662198486919765289420424058389829
det lower >  0.242647460554239533045887334929670799408622771839
```

Therefore both `L_u` and `L_v` are strictly negative definite.  This supplies
a concrete rational family satisfying the conditional premise used by the
two-scale P2 note.  It is not a claim about arbitrary `A,u,v`.

