# I05-29: the original PR58 obstruction fixture over its maximal legal chord

Status: **PROVED (author analytic proof with an executed rational finite certificate); PENDING_REVIEW**. No independent arithmetic or mathematical acceptance is implied. Novelty is NOT_ASSESSED. This successor starts at main `c6618e37640c5d019d9bbdc6fbffdc7fe31241f1`; PR80 and earlier frozen review inputs are not modified.

## 1. Exact object and conclusion

This is precisely the difficult `s=9/10` fixture from PR58's `ADDENDUM_JOINT_ADDITIVE.md` at immutable commit `89aa874c24dd5a3ea98f8474826392560b1d0397`, not the different PR54 fixture with an accepted `3<=s<=15` corridor. Its rational input is

```
A = [[219/500, -47/1000, 73/1000],
     [-47/1000, 461/1000, 23/1000],
     [73/1000, 23/1000, 43/100]]
C = [[231/500, 1/50, -49/1000],
     [1/50, 43/100, 11/200],
     [-49/1000, 11/200, 3/5]]
U = [[7/40, -22/125],
     [339/1000, 13/250],
     [229/500, -231/500]]
V = [[141/200, 981/1000],
     [-343/1000, 113/250],
     [187/250, 577/1000]]
B = U V^T.
```

All thirty displayed entries are used literally. Both blocks are strictly between zero and the identity and internally correlated, and B is rank two with all nine entries nonzero. Every observed coordinate is active. The path is the true real affine kernel

    K(t) = [[A,tB],[tB^T,C]].

Let s_star be the smaller zero of the polynomial

    p_full(s) = 483302515981103/50000000000000000
      - (4181050254735181419359/250000000000000000000000) s
      + (441119923648976242762443261/62500000000000000000000000000) s^2.

The maximal closed legal interval is exactly `[-sqrt(s_star),sqrt(s_star)]`, and

    0.99991110703434507047 < s_star < 0.99991110703434507048.

### Theorem 1

For this kernel, at every strict legal t,

    H''(t) <= -t^2/5,                                      (1)

with H''(0)=0. Moreover `H(t)+t^4/60` is concave on the **entire maximal closed legal interval**. In particular, for distinct legal t0,t1 and 0<lambda<1, writing tm=(1-lambda)t0+lambda t1,

    H(tm)-(1-lambda)H(t0)-lambda H(t1)
      >= [(1-lambda)t0^4+lambda t1^4-tm^4]/60 > 0.           (2)

This is a favorable entropy theorem, not a positive-Jensen-defect counterexample. The sign convention in (2) is midpoint entropy minus the interpolated endpoint entropy. The old additive-projection and ratio-cone failures are not reversed: the full signed average compensates them.

A nonempty relative-open class of fully correlated, dense rank-two parameters around this same fixture satisfies (1)-(2) on **each member's own maximal legal interval**. Section 6 proves this moving-endpoint extension. Its parameter radius is not quantified.

## 2. Complete law and normalized curvature

We start from the full inclusion-exclusion definition, with the empty principal minor equal to one. For an event mask S define `A^S=A-diag(1_{S^c})`, and similarly C^T. Strictness makes every complete event probability positive and every event matrix invertible. Put

    mu(S,T)=p_A(S)p_C(T),
    G_A(S)=U^T (A^S)^(-1) U,
    G_C(T)=V^T (C^T)^(-1) V,
    a=tr(G_A G_C), b=det(G_A)det(G_C).

The Schur determinant and rank-two determinant lemma yield, for every complete event,

    p_ST(t)=mu(S,T) q_ST(s),
    q(s)=1-sa+s^2b, s=t^2.                                (3)

The committed checker obtains these exact rational coefficients and separately constructs all 64 principal minors of the true six-coordinate K(t), performs full Mobius inversion, and checks equality of every coefficient with (3). It does not infer a polynomial from evaluations. Both computations are author-owned; their structural difference does not constitute independent review.

Both fixed block marginals give exact conditional cancellation of a and b in each orientation. Consequently the derivatives multiplying log mu cancel in the complete sum. Set

    v=-a+2sb, w=-a+sb, h=-a+6sb,
    lambda(q)=log(q)/(q-1), lambda(1)=1.

Direct differentiation of the full law, including the complete Fisher and acceleration, gives

    Gamma(s) := -H''(t)/t^2
       = E_mu[4v^2/q+2 w h lambda(q)]                      (4)

for s>0. At s=0 the right side is regular and equals `6 E_mu a^2`. Indeed `I(t)=D(p_t||mu)=(t^4/2)E_mu a^2+O(t^6)`, giving H''(0)=0. Thus no division by a vanishing numerical curvature is used at the center.

The logarithmic secant is positive, continuous, and strictly decreasing on (0,infinity). One elementary representation proving this is

    lambda(q)=integral_0^1 [1+theta(q-1)]^(-1) dtheta.       (5)

## 3. One complete interior interval: signed terms compensate globally

Fix rational constants

    c=9993/10000, L=9999/10000, R=12499/12500.

For every one of the 64 events, compute the exact extrema on the **entire interval** [0,c]:

    q_minus=min q(s), q_plus=max q(s),
    V_minus=min (-a+2sb)^2,
    Z_minus=min [(-a+sb)(-a+6sb)].

These are quadratic extrema: evaluate both endpoints and the vertex if it lies in the interval. The checker proves q_minus>0 for every event; the minimum over events exceeds `0.00016525797154545668`.

Since V_minus>=0 and lambda is positive decreasing, (4) has the valid lower bound

    Gamma(s) >= F_lower + L_lower,                         (6)
    F_lower=sum mu 4 V_minus/q_plus,
    L_lower=sum 2 mu Z_minus Lambda_used,

where Lambda_used is a lower enclosure of lambda(q_plus) when Z_minus>=0, and an upper enclosure of lambda(q_minus) when Z_minus<0. This sign-dependent choice is essential. There is no assumption that each event or conditional fiber has a nonnegative contribution.

The exact rational calculations, with outward logarithm bounds from Section 7, give

    F_lower > 311/400,
    L_lower > -72/125.

More precise outward displays of these **computed bounds**, not enclosures of the actual curvature at every s, are

    F_lower in [0.77750666966931183645,0.77750666966931183646],
    L_lower in [-0.57595380099546928469,-0.57595380099546928468].

Hence, uniformly for 0<=s<=c,

    Gamma(s) > 311/400-72/125 = 403/2000 > 1/5.             (7)

The saved sum with downward dyadic rounding is larger than
`0.20155286867384255177`. All 64 signed contributions are in the evidence table. Negative contributions are not replaced by zero, and positive/negative conditional-fiber lower bounds are allowed to compensate across the outer average. This is not a repetition of the fixed `s=.9` curvature check and not a grid certificate.

## 4. The actual maximal legal endpoint

The full-occupancy probability is exactly p_full(s)=det K(sqrt(s)) from Section 1. Rational comparison proves

    p_full(L)>0>p_full(R),
    p_full'(s)<0 for 0<=s<=R.

The empty-event polynomial `p_empty(s)=det(I-K(sqrt(s)))` has a strictly positive exact minimum on [0,R]. At s=0 both K and I-K are positive definite. By continuity of their eigenvalues, neither can lose positive definiteness without its determinant vanishing. Thus K and I-K are positive definite until the unique root s_star in (L,R), and the first legal boundary is the full-event root. Just beyond it det K<0, so the legal interval cannot extend further. The linear matrix-inequality feasible set in t is an interval and is symmetric by block-sign conjugation.

The root is simple because p_full'<0. All other 63 complete-event polynomials have strictly positive exact minima on [c,R], with global minimum exceeding `0.00032985537365504102`. In particular, the exceptional event is identified rather than chosen after ignoring other small atoms.

## 5. Quantitative singular-endpoint control with all other events retained

Write p_i(s) for the raw complete probabilities, and use primes in this section for s derivatives only. The exact physical t-curvature is

    -H''(t)=4s sum_i (p_i')^2/p_i
              +2 sum_i (p_i'+2s p_i'') log p_i.             (8)

For c<=s<s_star let delta=s_star-s. If p_0 denotes the full event, define on [c,R]

    d0=min(-p_0')>0, d1=max(-p_0'),
    E0=max |p_0'+2s p_0''|.

Since p_0(s_star)=0, integration gives

    d0 delta <= p_0(s) <= d1 delta,
    |p_0'(s)|>=d0.

For every other event put `m_i=min p_i>0` and `E_i=max |p_i'+2s p_i''|`. The checker also verifies their maxima are below one on [c,R]. Therefore the full (8), bounding the nonrare Fisher contributions only by their known nonnegativity but retaining every acceleration term, satisfies

    -H''(t) >= A_e/delta-B_e log(1/delta)-C_e,               (9)

where

    A_e=4c d0^2/d1, B_e=2E0,
    C_e=B_e max(0,-log d0)+2 sum_{i!=0} E_i(-log m_i).

The error-controlled rational upper bound for C_e and exact A_e,B_e satisfy

    A_e > 1/100,
    B_e < 3/50,
    C_e < 14.                                               (10)

Their directed displays are approximately 0.010395798499440325,
0.051239847700694739, and 13.111573759686385, respectively; the last number is an upper-budget computation, not the actual adverse sum.

Here `0<delta<R-c<1/1600`. The function

    f(delta)=1/(100delta)-(3/50)log(1/delta)-14

is strictly decreasing for delta<1/6. Since log1600<8 (also rationally enclosed by the checker),

    f(delta)>16-(3/50)8-14=38/25>3/2.

Consequently `-H''(t)>3/2` on the terminal interval. Because s<s_star<R<1, this implies `Gamma(s)>3/2>1/5` there. Together with (7), it proves (1) throughout the strict maximal chord. The singular endpoint is not handled by deleting the full or empty event or by substituting a fixed positive likelihood window.

For t!=0, `(H+t^4/60)''=H''+t^2/5<=0`; at zero the analytic continuation gives the same inequality. Complete event probabilities are polynomial in t and `-x log x` is continuous at zero, so the concavity extends to the closed legal interval. The strict convexity of t^4 gives (2), including chords whose endpoints lie on the spectral boundary.

## 6. A nonempty open class with moving maximal endpoints

The preceding certificate extends beyond one fixed input without presuming that the legal endpoint is fixed.

Parameterize actual real rank-two blocks by `(A,C,U,V)` with U,V full column rank and A,C strict real symmetric. All complete-event coefficients are continuous functions of these parameters. Retain the same rational c,L,R. Define a parameter set by the following strict conditions:

- K(0) and I-K(0) are positive definite; the full-event polynomial has positive value at L, negative value at R, and negative derivative on [0,R]; the empty-event polynomial has positive minimum on [0,R].
- All q_minus on [0,c] are positive, and the exact, unrounded expressions in Section 3 obey `F_lower>311/400` and `L_lower>-72/125` (using the true lambda endpoints in the definition).
- All other 63 p_i have positive minima and maxima below one on [c,R], and the exact quantities in Section 5 obey `A_e>1/100`, `B_e<3/50`, `C_e<14`.

Every condition is continuous and strict. Extrema over the fixed compact intervals are continuous; the expression `Z_minus lambda(q_plus)` for Z_minus>=0 and `Z_minus lambda(q_minus)` for Z_minus<0 is continuous at Z_minus=0 as both branches vanish. The computed directed bounds prove that the displayed rational fixture lies strictly inside this parameter set.

It follows that this set contains a nonempty relative-open neighborhood of the original fixture. Intersect with the open conditions that all internal offdiagonals, all cross entries, and the row-pair minors of U,V remain nonzero. It still contains the fixture, and every member has two correlated blocks of three active observed coordinates, a dense rank-two B, and no forced proportional pair in either frame.

For every member, Section 4 locates its own unique simple maximal endpoint in (L,R), and Sections 3 and 5 prove the same uniform `H''<=-t^2/5` on its whole legal chord. Thus the neighborhood conclusion concerns **each member's moving maximal interval**, not an existential perturbation of one preassigned shorter compact interval. The radius is not quantified, and this does not cover arbitrary rank-two data or all dimensions.

This is a completed structural extension around the actual previously difficult point: membership of the center and every inequality needed for the continuum and boundary have been checked. It is not presented as an untested newly named sufficient criterion.

## 7. Reproduction, precision and evidence boundaries

Run from this directory, with Python and SymPy installed:

    python code/verify_whole_chord.py

`fixtures.py` embeds the complete rational matrices and reconstructs every event. `exact_core.py` contains only Fraction interval arithmetic and elementary logarithm enclosures. `verify_whole_chord.py` checks all exact polynomial identities and inequalities above, writes `output/whole_chord_certificate.json`, and prints directed displays. The original final execution used Python 3.13.5 / SymPy 1.14.0, one numerical thread, and returned exit 0. Runtime is reported in literal stdout and JSON; it is not an error bound.

For x>0, write x=2^k m with 1<=m<=2. Round m outward to a 56-bit dyadic interval. With z=(m-1)/(m+1), use N=28 terms of

    log m = 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1) + remainder,
    0<=remainder<=2 z^(2N+1)/[(2N+1)(1-z^2)].

Use the same construction for log2, multiplying its interval by the signed integer k, and round the final interval outward to 112 dyadic bits. For 1/2<=q<=2, lambda is evaluated directly with the positive even series

    lambda(q)=2/(q+1) sum_{j>=0} z^(2j)/(2j+1),

with the corresponding geometric tail and monotonic endpoint substitution; this avoids division by q-1 near one. Outside that window use signed interval division of log q by q-1. All positivity decisions are rational comparisons. No binary float decides legality, a sign, a polynomial coefficient, or a logarithm enclosure.

The interval sum additionally rounds each event's computed lower contribution downward to 112 dyadic bits, losing at most `64*2^-112`. Its displayed interval encloses this conservative rational lower number, not an upper/lower enclosure of actual Gamma(s). This avoids the invalid upper-bound convention disclosed in the older PR80 window file.

The final code also checks the original s=.9 complete value, obtaining

    t^2 I'' in [4.6535982453988417,4.6535982453988419].

That comparison confirms consistency with the accepted PR76 fixed value; it is not used to infer the continuum result. No additive residual is recomputed and no old stopped computation is relabeled PASS.

The local author prototype and development failures are recorded separately in `FAILURE_LEDGER.md`. The two full-law reconstruction routes remain author calculations, not two independent reviews. Source provenance, independent arithmetic, independent mathematical review, and novelty require separate dispositions. The general correlated rank-two conjecture remains INCOMPLETE.
