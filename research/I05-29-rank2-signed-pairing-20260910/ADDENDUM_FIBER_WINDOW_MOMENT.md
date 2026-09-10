# I05-29 addendum — a fiber window/moment lower bound that allows bad events

Status: **PROVED (author proof; PENDING_REVIEW)**.  The fixed `s=9/10` application below is an **author rigorous finite certificate; PENDING_REVIEW**.  Novelty is not assessed.

This is the structural continuation after the ratio-cone falsification in `ADDENDUM_S09_SIGNED_FIBERS.md`.  It does not require pairwise PSD and does not require every complete event to have nonnegative curvature contribution.

All notation is for the true affine path

`K(t)=[[A,tB],[tB^T,C]]`, `s=t^2`,

with the complete rank-two likelihood

`q=1+u=1-sa+s^2b`, `y=s^2b`.

The exact square completion already proved in the preceding addendum is

`Phi(u)+4y^2/q+y psi(u) = 4(u+y)^2/q + 2(u+5y)log q`.       (1.1)

Fix either a left or a right conditional fiber, with its true reference marginal weights.  Put

`v=u+y`,

`z=u(u+5y)`,

and define

`lambda(q)=log(q)/(q-1)` for `q!=1`, `lambda(1)=1`.           (1.2)

Since `log q=(q-1)lambda(q)=u lambda(q)`, the complete fiber curvature is exactly

`C_f = E[ 4v^2/q + 2 z lambda(q) ]`.                         (1.3)

## 1. Monotonicity of the logarithmic secant

### Lemma 1.1

`lambda(q)` is positive and strictly decreasing on `(0,infinity)`.

### Proof

Positivity follows because `log q` and `q-1` have the same sign.  For `q!=1`,

`lambda'(q)=[(q-1)/q-log q]/(q-1)^2`.

The numerator is nonpositive because

`log q-1+1/q >=0`: its derivative is `(q-1)/q^2` and its unique minimum is zero at `q=1`.  Continuity supplies the value at one. QED.

## 2. Fiber window/moment theorem

Assume a strict fiber has

`0<q_- <= q <= q_+`.                                         (2.1)

Set

`lambda_- = lambda(q_+)`, `lambda_+ = lambda(q_-)`,

`c=(lambda_+ + lambda_-)/2`,

`delta=(lambda_+ - lambda_-)/2`.                              (2.2)

Thus for every event in the fiber,

`lambda(q)=c+epsilon`, `|epsilon|<=delta`.                    (2.3)

### Theorem 2.1

For every strict rank-two conditional fiber,

`C_f >= 4 E[v^2]/q_+ + 2 c E[z] - 2 delta E[|z|]`.           (2.4)

In particular, the right side may be strictly positive even when some complete events have `z<0`, some one-event curvature integrands are negative, and many conditional event pairs violate the PR80 ratio-cone.

### Proof

From `q<=q_+`,

`4v^2/q >= 4v^2/q_+`.                                        (2.5)

From (2.3), pointwise

`z lambda(q)=c z+epsilon z >= c z-delta |z|`.                (2.6)

Average (2.5) and (2.6) in the exact identity (1.3). QED.

No Cauchy bound is applied to the mixed rank-two term.  The only loss is the explicitly exposed variation `delta` of the scalar secant `lambda` inside one conditional fiber.  The quantities

`E[v^2]`, `E[z]`, `E|z|`                                      (2.7)

are complete-fiber moments with the actual event weights.  For rational A,B,C and rational s they are rational; only the two endpoint values of `lambda` require logarithm enclosures.

### Structural interval form

The same proof is uniform on any family/parameter interval for which one has common bounds on `q_-,q_+` and lower/upper bounds on the three fiber moments in (2.7).  Thus the theorem is not tied to 3+3 or to one fixture.  It applies in arbitrary block dimensions whenever the cross rank is two and the accepted quadratic complete likelihood is valid.

It is materially weaker than eventwise sign condition `(a-sb)(a-6sb)>=0`: negative z-events are permitted and paid for only through the actual `E|z|` budget multiplied by the within-fiber secant spread `delta`.

## 3. Rigorous application to the public PR58 s=9/10 obstruction point

Use exactly the rational A,C,U,V fixture from accepted PR58 at `s=9/10`.  The checker `code/verify_s09_fiber_window_bound.py` imports the frozen event reconstruction/log enclosure from `verify_s09_signed_fibers.py`, recomputes the exact rational moments in (2.7), and encloses only `lambda(q_-)` and `lambda(q_+)` by the same rational atanh remainder scheme.

For all eight left fibers, the rigorous lower bounds in (2.4) are positive.  Approximate displays are

`S=0: 1.956458406808832`

`S=1: 1.149416870206478`

`S=2: 2.233813127078996`

`S=3: 1.175170052573918`

`S=4: 1.893884871338329`

`S=5: 2.043513885222431`

`S=6: 1.764779363969526`

`S=7: 1.685389414840739`.

For all eight right fibers, the rigorous lower bounds are likewise positive:

`T=0: 2.524214467071104`

`T=1: 0.702423465205957`

`T=2: 2.238222131167061`

`T=3: 1.364311069175426`

`T=4: 1.028310685176827`

`T=5: 2.271403595688184`

`T=6: 1.417013762759978`

`T=7: 3.027549266507641`.

The exact rational lower endpoints, not these decimals, decide every sign.

Therefore the difficult public point is covered by a structural bound that **allows its four negative one-event integrands and its 75/66 bad ratio pairs**.  This is stronger mechanistic information than simply recomputing the already-known positive global curvature.

## 4. Scope and equality

If the right side of (2.4) is positive on every fiber of either orientation, then averaging with the opposite fixed block marginal gives `t^2 I''>0`, hence `H''<0` at that physical parameter.

If the right side is merely zero, no automatic strictness is claimed.  The exact identities in the previous addendum, rather than the old erroneous first-line argument, govern equality.

This theorem does not close the whole legal chord.  Its next analytic target is to control `q_-/q_+` and the three moments in (2.7) from block/exterior-feature data uniformly in s.  That remaining step is distinct from the already-failed additive projection and ratio-cone routes.
