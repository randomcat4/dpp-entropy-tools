# I05-29 addendum — s=9/10 falsification, exact reserve, and a coefficient class

Status: **author proof / author rigorous finite certificate; PENDING_REVIEW**.  Nothing here is an independent review or a novelty determination.

This addendum supersedes the unresolved s=9/10 sentence in the initial PR80 packet and corrects the strictness sentence in its Theorem 4.1.  The original statement is preserved in git history rather than silently erased.

Throughout, the path is the true affine kernel

`K(t)=[[A,tB],[tB^T,C]]`, `s=t^2`,

with the complete configuration law, and the accepted rank-two notation

`q=1+u=1-sa+s^2 b`, `y=s^2 b`.

The accepted full-law curvature identity is

`t^2 I'' = E_mu[ Phi(u)+4 y^2/q+y psi(u) ]`,

`Phi(u)=4u^2/q+2u log q`, `psi(u)=8u/q+10log q`.

No event, rare atom, Fisher term, or acceleration term is removed below.

## 1. The PR80 ratio-cone does not cover the s=9/10 obstruction fixture

Use exactly the public rational 3+3 fixture in PR58 `ADDENDUM_JOINT_ADDITIVE.md`, at `s=9/10`.  The accompanying checker reconstructs all 64 complete events from A,C,U,V and outward-encloses every logarithm by the rational atanh series with a rigorous remainder.

For a conditional pair with `Delta u != 0`, the initial PR80 sufficient lower kernel was

`F(q,q',r)=L(q,q')+2(1+r^2)/(q+q')+r(5L(q,q')+4/(q q'))`,

`r=Delta y/Delta u`.

The cheap falsification is decisive:

- fixing S and pairing T,T': 75 of the 224 unordered pairs have a rigorously negative upper enclosure for F;
- fixing T and pairing S,S': 66 of the 224 unordered pairs have a rigorously negative upper enclosure for F.

The worst outward-enclosed values are approximately `-4245.633453787008` on the left-fiber test and `-3807.017321311469` on the right-fiber test.  The exact signs, not these decimal displays, are asserted by rational endpoints in the checker.

Therefore the ratio-cone theorem remains a valid sufficient theorem, but **this mechanism is DISPROVED as an explanation of the key s=9/10 fixture**.  It is not retained as the main route.

This is a method obstruction, not an entropy counterexample.  The true complete curvature at the same point is positive.

## 2. Exact Cauchy-slack identity and the correction to Theorem 4.1 strictness

For positive q,q' and arbitrary x,x', one has the exact identity

`x^2/q+x'^2/q'`

` = (x-x')^2/(q+q') + (q' x+q x')^2/[q q'(q+q')]`.          (2.1)

Thus equality in the Cauchy lower bound occurs exactly when

`q' x+q x'=0`.                                                (2.2)

Apply (2.1) to x=u and x=y in the exact signed pair kernel of PR80.  When `Delta u != 0` and `r=Delta y/Delta u`, the pair contribution J is **exactly**

`J=(Delta u)^2 F(q,q',r)`

`  + 2[(q'u+qu')^2+(q'y+qy')^2]/[q q'(q+q')]`.              (2.3)

This is the useful form after the ratio-cone failure: negative F on individual pairs is allowed, because the same pair carries an explicit nonnegative square reserve, and different pairs are averaged with their true signs.

It also exposes a flaw in the initial strictness sentence of Theorem 4.1.  The fact that the first line of the original J is nonzero does **not** by itself imply that the lower bound after Cauchy is strict; that mass may have been consumed by the difference-square lower bound.  A correct sufficient strictness statement for a pair with `Delta u !=0` is:

- `F>0`, or
- `q'u+qu' != 0`, or
- `q'y+qy' != 0`.

For `Delta u=0`, use the original exact J directly.  The theorem's non-strict conclusion remains valid; only its displayed automatic strictness rationale is corrected.

## 3. An even shorter exact square completion

Before any conditional pairing, the one-event integrand itself has the exact identity

`Phi(u)+4y^2/q+y psi(u)`

` = 4(u+y)^2/q + 2(u+5y) log q`.                              (3.1)

Since `u=-sa+s^2b` and `y=s^2b`, this is

`t^2 I''`

` = E_mu[ 4(-sa+2s^2b)^2/q`

`          +2(-sa+6s^2b) log(1-sa+s^2b) ]`.                 (3.2)

This is not a bound.  It is the complete Fisher/acceleration curvature rewritten so that one positive square and one signed logarithmic term remain.  In particular, it identifies exactly where any genuinely bad contribution can live.

### Structural coefficient class

Because `log q` has the same sign as `q-1=u`, the logarithmic term in (3.1) is nonnegative whenever

`u(u+5y)>=0`.

Equivalently,

`(a-sb)(a-6sb)>=0`.                                          (3.3)

Hence, on any strict legal s-interval, if every complete event satisfies (3.3), then

`t^2 I''(t)>=0` and therefore `H''(t)<=0` throughout that interval.       (3.4)

This is a genuine rank-two coefficient family: it depends only on the two exact exterior coefficients a,b of each complete event and the physical parameter s.  It does not use an additive projection, a pairwise PSD relaxation, a spectral-basis rotation, or a Markov dilation.

The exact equality condition under (3.3) is also transparent.  At a fixed positive-mass event its contribution vanishes exactly when both

`u+y=0`

and

`(u+5y) log q=0`.                                            (3.5)

Thus strict curvature follows whenever (3.3) holds everywhere and at least one positive-mass event violates one of the equalities in (3.5).

A useful ratio reading of (3.3), when `a !=0`, is that `z=sb/a` must avoid the open interval between `1/6` and `1`; the product form (3.3) is the authoritative sign-safe statement and also covers zero/sign-changing a,b.

## 4. The s=9/10 fixture lies beyond eventwise positivity but is fiberwise positive

The coefficient class (3.3) is not being retrofitted onto the PR58 witness.  The checker finds four of the 64 complete events whose full square-completed integrand (3.1) is rigorously negative:

`(S,T)=(0,6),(1,5),(2,5),(3,0)`.

Approximate values, for orientation only, are respectively

`-0.0329178878621, -0.146087892643, -0.00522998215918, -0.242061854492`.

So even eventwise nonnegativity is too strong for this fixture.

However the complete signed conditional averages are all strictly positive.  Fixing S and averaging all eight T-events with the true reference weights p_C gives, for S=0,...,7,

`3.79240050874127, 1.96273941667876, 4.75518267654239, 3.24698718938302,`

`4.05256739971849, 4.99435498141659, 6.96644598681454, 10.0331252210680`.

Fixing T and averaging all eight S-events with p_A gives, for T=0,...,7,

`4.63688172921528, 1.32074408433296, 4.07780724877714, 3.46804802345122,`

`1.86032005138374, 4.40402670068084, 5.72936606784156, 12.5187735902853`.

Every displayed positivity is certified by a rational lower endpoint, not by the decimal display.  Averaging either set of eight fiber values with the opposite block marginal gives the same complete value

`t^2 I'' = 4.653598245398841... >0`,                          (4.1)

consistent with the already accepted PR76 complete-curvature enclosure.

This produces a strict hierarchy on one legal correlated dense rank-two point:

1. free pairwise PSD fails analytically;
2. the actual DPP ratio-cone fails on many pairs on both sides;
3. even one-event nonnegativity fails on four complete events;
4. nevertheless every complete conditional fiber has positive signed curvature average;
5. hence the full curvature is positive.

The surviving mechanism is therefore genuinely a **fiber compensation** mechanism, not a relabeling of pairwise or eventwise positivity.

## 5. What is proved, disproved, and still open

**PROVED (author algebra; PENDING_REVIEW):** the exact reserve identity (2.3), the square completion (3.1)-(3.2), the coefficient family theorem (3.3)-(3.5), and the corrected strictness conditions.

**DISPROVED as a mechanism for the fixed witness (author rigorous finite certificate; PENDING_REVIEW):** the PR80 ratio-cone, on both possible conditional orientations at `s=9/10`.

**PROVED for the fixed point (author rigorous finite certificate; PENDING_REVIEW):** all 16 one-sided complete conditional fiber curvature averages are strictly positive, despite four negative individual event contributions; the global sum is positive and agrees with the accepted PR76 value.

**INCOMPLETE:** a block-level theorem forcing fiber-average positivity for all s in a broad correlated rank-two family, and the general dense correlated whole chord.  The fixed point is a mechanism test, not promoted into a universal theorem.

**NOVELTY:** not assessed here.

The existing issue #63 remains the separate >60-minute contract for the older whole-chord additive computation.  No new long computation was needed for this addendum.