# D10-U10f verdict

STATUS: INCOMPLETE.

No strict exchangeable triangle counterexample was found, but the full
two-parameter triangle domain was not proved.

## Certified only as author-side candidates

- `S3` representation reduction: the full six-dimensional Hessian splits as a
  two-dimensional invariant block plus a four-dimensional standard block.
- The standard block is strictly positive for every strict connected
  exchangeable triangle, using the already reviewed U8 identity
  `B=Fisher+det(N)G-det(N)eta eta^T` and the fact that the trace functional
  vanishes on the standard part.
- Therefore the whole exchangeable triangle problem reduces to one explicit
  scalar determinant inequality for the two-dimensional `(alpha,beta)` block.
- A punctured diagonal compact-neighborhood theorem candidate is proved by
  Taylor expansion:

```text
B_xx = 3/[x(1-x)] + O(a),
B_xa = O(a^2),
B_aa = 18 a^2/[x^2(1-x)^2] + O(a^3),
det B_T = 54 a^2/[x^3(1-x)^3] + O(a^3).
```

This gives `B>0` for all sufficiently small nonzero `a`, uniformly for
`x` in any compact subinterval of `(0,1)`.

## Remaining blocker

For

```text
0<alpha,beta<1, alpha != beta,
```

define the per-subset exact atoms

```text
p0=(1-alpha)(1-beta)^2,
p1=(1-beta)(alpha+2 beta-3 alpha beta)/3,
p2=beta(2 alpha+beta-3 alpha beta)/3,
p3=alpha beta^2.
```

Let `C` be the two-dimensional negative entropy Hessian of

```text
-p0 log p0 - 3p1 log p1 - 3p2 log p2 - p3 log p3
```

in variables `(alpha,beta)`.  Since `C_alpha_alpha>0`, the global triangle
claim is now exactly the open scalar inequality

```text
C_alpha_alpha C_beta_beta - C_alpha_beta^2 > 0.
```

I did not close this two-variable log inequality.

## Scout result

`exchangeable_triangle_sanity.py` ran successfully and wrote
`sanity_results.json`.

```text
exit code: 0
checked points: 177360
credible negative examples: 0
status: SCOUT_NO_COUNTEREXAMPLE
```

The smallest displayed eigenvalue in the raw float ledger is a near-diagonal
`-4.55e-13` cancellation artifact with `alpha-beta≈3.5e-10`; it is explicitly
recorded as a floating-point warning, not as a sign gate.

Finite scouting is not a theorem.

