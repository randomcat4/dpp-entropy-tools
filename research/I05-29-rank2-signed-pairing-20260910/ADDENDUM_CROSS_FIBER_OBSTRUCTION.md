# I05-29 continuation: a negative true fiber and a complete-interval compensation theorem

Status: AUTHOR PROOF / AUTHOR FINITE CERTIFICATE; PENDING_REVIEW. This is not an independent review or a novelty determination. The C1 FIRST archive in PR90 concerns its explicitly frozen earlier sources, not this delta.

The physical path throughout is the real affine kernel

`K(t) = [[A,tB],[tB^T,C]]`, `s=t^2`.

All complete configurations and their actual weights are retained. No spectral change of the observed coordinates is made. Write `mu(S,T)=p_A(S)p_C(T)` and `q=1-sa+s^2b=1+u`, `y=s^2b`. The full curvature is

`C_tot := t^2 I''(t) = E_mu[4(u+y)^2/q + 2(u+5y)log q]`,

where `I=H(A)+H(C)-H(K(t))`. For a fixed left configuration S, call its complete p_C-average `C_S`. Thus `C_tot=E_pA C_S`. The individual `C_S` is the curvature contribution from conditional relative entropy to p_C; it is NOT, in general, minus the second derivative of conditional Shannon entropy alone.

## 1. Correction of the previous correction: diagonal pairs settle strictness

The original Theorem 4.1's global strictness conclusion was not disproved by finding a gap in the proposed pair-level Cauchy rationale. In a finite strict DPP, a diagonal pair has positive product mass.

The exact Cauchy slack remains

`x^2/q+x'^2/q' - (x-x')^2/(q+q') = (q'x+qx')^2/[qq'(q+q')]`.

So a positive original first line does not automatically make the Cauchy inequality strict on that particular off-diagonal pair. But under the theorem's hypothesis all pair contributions are nonnegative, and

`J(T,T)=4(u(T)^2+y(T)^2)/q(T)`.

If any positive-mass atom has nonzero u or y, its diagonal pair supplies strict positivity. Therefore the global strictness sentence in the first RESULT was valid for this finite setting. The contrary descriptions in the earlier S09 addendum and previous author summary are overcorrections and are superseded here. This agrees with C1's source FIRST in PR90, without promoting this new proof to independently accepted status.

More precisely, at s>0 under the cone hypothesis, equality holds exactly when u=y=0 on every complete event. For the real cross-block path this is equivalent to B=0: if q=1, independence gives

`P(i in S,j in T)=A_ii C_jj`,

whereas the two-coordinate DPP determinant gives `A_ii C_jj-s B_ij^2`. Hence every B_ij vanishes. Conversely B=0 is constant. Nonzero cross-rank two therefore gives strict curvature wherever the cone hypothesis holds.

At t=0 no division by t^2 is permitted. Finite strict laws are analytic and `q=1+O(t^2)` with normalized coefficients, so `I(t)=(t^4/2)E_mu[a^2]+O(t^6)` and `H''(0)=0`.

## 2. A true DPP conditional fiber can be strictly negative

Let

`X=[[0,1],[1,0]]`, `R=[[1,1],[1,-1]]`,

`A=I_2/2`, `C=I_2/2+rX`, `B=sqrt(r/2) R`,

with `0<r<=1/8`, and take the complete interval `|t|<=1`.

### Strict legality

Here `B^T B=r I_2`. The Schur complements for K and I-K are

`C-2sr I_2` and `I_2-C-2sr I_2`.

Both have minimum eigenvalue `1/2-r-2sr >=1/8`. Therefore K(t) is strictly legal on the whole indicated interval. B has rank two and no zero entry.

### Exact negative fiber

Fix the left configuration S={first coordinate}, mask 1. Its event matrix is `A^S=diag(1/2,-1/2)`. Complete conditioning gives

`C_S(s)=C-s B^T(A^S)^(-1)B = I_2/2+r(1-2s)X`.

This formula also follows directly by taking a Schur complement in each full event determinant, so it does not assume a change of observed basis.

Put `d=1/4-r^2`, `e=1/4+r^2`, and `h(s)=4r^2 s(1-s)`. The two same-occupancy right events have reference probability d and conditional probability d+h; the two single-occupancy events have reference probability e and conditional probability e-h. All four events are present.

At `s=1/2`, `u+y=0` on every event, and

`q_same=1/(1-4r^2)`, `q_single=1/(1+4r^2)`.

Consequently, exactly,

`C_{mask 1}(1/2) = -16r^2 log((1+4r^2)/(1-4r^2)) < 0`.       (2.1)

This is an actual legal rank-two DPP obstruction to universal positivity of every conditional fiber. It is not an abstract quadratic-likelihood relaxation and not an entropy counterexample. In fact Section 3 proves favorable full entropy curvature on the entire interval for the very same family.

At the rational member r=1/8, `B=R/4`, and the bad fiber is

`-(1/4)log(17/15)`,

outward-enclosed by `[-0.031290785739,-0.031290785738]`. The four full left-fiber values are enclosed by

`[0.840565528856,0.840565528857]`,

`[-0.031290785739,-0.031290785738]`,

`[0.459497907072,0.459497907073]`,

`[0.840565528856,0.840565528857]`.

Each has weight 1/4. Their complete average is in `[0.527334544761,0.527334544762]`.

### The obstruction is not restricted to a diagonal marginal

There is also a fully correlated exact family. Take

`A=[[1/2,3/8],[3/8,1/2]]`,

`B=k [[1,2],[2,-1]]`, `r=4k^2`, `C=I_2/2+rX`,

where `0<k<1/sqrt(88)`. The same mask has

`[[1,2],[2,-1]]^T (A^S)^(-1) [[1,2],[2,-1]] = 8X`.

Hence its conditional kernel and negative curvature are again exactly those in (2.1). Both A and C are correlated and every entry of B is nonzero.

For legality, `lambda_min(A)=lambda_min(I-A)=1/8` and `B^TB=5k^2 I`. Both full Schur complements are bounded below by `(1/2-44k^2)I>0` on s in [0,1]. Thus this is a whole family of strict real counterexamples to universal conditional-fiber positivity with both marginals correlated.

The rational member k=1/16 has `r=1/64`, a negative fiber in `[-0.0000076293969566,-0.0000076293969565]`, and positive full curvature at s=1/2 in `[0.0331791958709964,0.0331791958709965]`. Only this point's full positivity is asserted for this second family here; Section 3's continuum bound concerns the first family.

## 3. A complete-interval theorem with genuine cross-fiber compensation

### Theorem

For the first family in Section 2, for every `0<r<=1/8` and every `|t|<=1`, the complete configuration Shannon entropy satisfies

`H''(t) <= -(700/19) r^2 t^2`.                               (3.1)

It is strictly concave on [-1,1], although a complete conditional fiber is negative at s=1/2 for every member of the family.

### Proof: full-event coefficients, not a grid

The reference marginal p_A is uniform. In terms of d and e above, the sixteen conditional right-event probabilities fall into these exact groups:

* `d+4r^2s^2 +/- 2rs`: each sign occurs twice;
* `e-4r^2s^2`: occurs four times;
* `d-4r^2s^2 +/- 4r^2s`: each sign occurs twice;
* `e+4r^2s^2 +/- 4r^2s`: each sign occurs twice.

Divide each probability by its displayed constant term to obtain q; its full reference weight is one quarter of that constant term. Thus no multiplicity or event is lost.

These expressions imply the uniform likelihood window

`1/5 <= q <= 7/3`                                            (3.2)

for every r in (0,1/8] and s in [0,1]. For the first group, the minus expression decreases with s and the plus expression increases. At s=1 the two needed inequalities reduce to

`d+4r^2-2r-d/5 = (1-8r)(1-2r)/5 >=0`,

`7d/3-(d+4r^2+2r) = (1-8r)(1+2r)/3 >=0`.

For the other groups, `r^2/d<=1/15`, `r^2/e<=1/17`, and `s(1-s)<=1/4` give respectively the narrower windows `[13/17,1]`, `[7/15,16/15]`, and `[16/17,25/17]`.

Let `M_a=E_mu a^2`, `M_b=E_mu b^2`. Summing the displayed sixteen full-event coefficients gives the exact Gram relations

`E_mu ab=0`,

`M_a=16r^2(1+12r^2)/(1-16r^4)`,

`M_b=256r^4/(1-16r^4)`,

`M_b/M_a=16r^2/(1+12r^2) <=4/19`, `M_a>=16r^2`.             (3.3)

The cancellation `E_mu ab=0` is global. It does not assert, and in this example cannot be replaced by, positivity of every fiber.

Write `v=u+y` and `z=u(u+5y)`. From (3.3),

`E v^2=s^2 M_a+4s^4 M_b`,

`E z=s^2 M_a+6s^4 M_b`,

`E|z| <= (E u^2+E(u+5y)^2)/2 = s^2 M_a+(37/2)s^4 M_b`.      (3.4)

The last step is the elementary inequality `|xy|<=(x^2+y^2)/2`, used after retaining the complete signed expectation; no pair or fiber is discarded.

The scalar secant `lambda(q)=log(q)/(q-1)`, with lambda(1)=1, is decreasing. On (3.2),

`5/8 <= lambda(q) <=81/40`.                                 (3.5)

Indeed `lambda(7/3)=(3/4)log(7/3)>5/8` and `lambda(1/5)=(5/4)log 5<81/40`. These only require `log(7/3)>5/6` and `log5<81/50`, also certified by rational atanh remainders in the checker.

Using the midpoint `53/40` and half-width `7/10` of (3.5) in the exact full curvature gives

`C_tot >= (12/7)E v^2+(53/20)E z-(7/5)E|z|`

`       >= (83/28)s^2 M_a-(22/7)s^4 M_b`

`       >= (175/76)s^2 M_a`

`       >= (700/19)r^2 s^2`.                                (3.6)

The penultimate step uses s<=1 and M_b/M_a<=4/19. For t!=0 divide (3.6) by t^2=s and use I''=-H''. At t=0 use the analytic endpoint argument in Section 1. This proves (3.1) on the entire interval, not just its rational samples. Since the upper bound is strictly negative away from the single point t=0, H is strictly concave on [-1,1]. QED.

## 4. Recheck of the original 64-event s=9/10 target

The new checker reimplements the exact event reconstruction from the published A,C,U,V input; it does not replace that input with the simpler obstruction family. Using rational atanh enclosures followed by outward dyadic rounding, it verifies all 64 events and all 224 unordered pairs in each orientation, with no undecided ratio sign:

* negative ratio counts remain 75 and 66;
* the four negative complete one-event contributions remain (0,6),(1,5),(2,5),(3,0);
* the minimum left/right window lower bounds are in `[1.149416870206,1.149416870207]` and `[0.702423465205,0.702423465206]`;
* the full value is in `[4.653598245398,4.653598245399]`.

All sixteen original fixture fibers remain positive. This fact is fully compatible with the new theorem: the fixed point is covered by the earlier sufficient bound, but positivity of every fiber cannot be demanded as the universal mechanism.

## 5. Evidence, scope, and remaining obligation

`code/verify_fiber_obstruction_family.py` is author-side executable evidence; `output/verify_fiber_obstruction_family.txt` retains its exact-sign and outward-decimal summary. The final recorded run used Python 3.13.5 / SymPy 1.14.0 and took 0.477 seconds. There was no >60-minute job and no new compute contract.

Development transparency: a first author run stopped on a SymPy structural-expression equality assertion for an algebraically equal rational identity. It was repaired to test `simplify(lhs-rhs)==0`, and the complete final script was rerun. This was not an independent checker run, not a mathematical mismatch, and not an extension of any C2 stop-on-mismatch contract.

Author conclusions: universal individual-fiber positivity is DISPROVED by (2.1), including a fully correlated family; the explicit first family has a PROVED complete-interval cross-fiber compensation theorem (3.1), pending independent review. General dense correlated rank-two whole-chord curvature is not established: arbitrary blocks do not supply the special global Gram cancellation and quantitative window (3.2)-(3.3).

The retained window bound is an elementary inequality, not by itself a general DPP theorem. This continuation uses it to finish a nontrivial explicit continuum family and to identify an exact obstruction to the stronger fiberwise route. Newness relative to the literature is NOT_ASSESSED. The limited primary-source lookup of Kulesza--Taskar, arXiv:1207.6083, establishes background DPP inference context only, not novelty or the entropy theorem here.
