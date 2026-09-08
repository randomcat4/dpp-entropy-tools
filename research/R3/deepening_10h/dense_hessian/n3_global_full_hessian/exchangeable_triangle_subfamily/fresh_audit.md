# D10-U10f fresh non-author audit

STATUS: CORRECT for the exact formulas, S3 reduction, scalar equivalence,
and punctured-diagonal compact-neighborhood theorem.

The full strict exchangeable-triangle domain remains INCOMPLETE. The author's
finite search remains SCOUT, not a certified full-domain sign check.

This audit did not import or execute the author's code. Its complete
independent implementation is embedded in [fresh_audit_log.md](fresh_audit_log.md),
and the exact polynomials/check results, full point coordinates, source
SHA256 hashes and rational warning certificates are frozen in
[fresh_audit_results.json](fresh_audit_results.json).

Frozen principal proof: proof_or_blocker.md SHA256
8034ada41d90e34c79891e47b62e0bc20d5a14fd85f8a405a1ee4d5223039538.
Author-version hashes were checked before and after the audit computation.

## 1. Exact-event semantics and derivative table: CORRECT

Starting with a general symmetric six-coordinate kernel, the independent
implementation forms each principal determinant as a multivariate rational
polynomial and applies Möbius inversion. Substituting the exchangeable kernel
gives exactly the author's four per-subset atoms (proof lines 27--30), with
multiplicities (1,3,3,1). All eight symbolic identities vanish exactly.

The 20 first/second derivative entries at lines 123--143 agree with formal
polynomial differentiation. In particular p2_alpha=beta(2-3 beta)/3 is
correct. The earlier alternative mentioned by the author is not used.

The formula B=sum (dp dp^T/p + Hess(p) log p) is the negative entropy
Hessian: the extra Hess(p) term from differentiating p log p cancels because
the total atom mass is identically one. Offdiagonal coordinates change both
Kij and Kji; the independent symbolic matrix enforces this convention.

## 2. S3 split and full four-dimensional strictness: CORRECT

Permutation averaging sends any D to its mean diagonal and mean edge
components. Thus T=span(I,J-I) is the fixed space, and the kernel of this
averaging map is exactly W as defined at lines 51--53. Invariance gives
B(t,w)=B(t,average(w))=0, without any assumption that the two standard
copies are separately uncoupled. Coupling within the four-dimensional W
is allowed and does not affect the argument.

The reviewed U8 identity applies to every symmetric D. Here a!=0 makes the
observation graph connected. All pair log odds ell are equal, and
N=-ell I-Lambda K is exchangeable, so its inverse has equal diagonal and
equal offdiagonal entries. Consequently eta(D)=tr(N^(-1)D)=0 for every
D in W, including arbitrary mixed diagonal/edge contrasts.

Strict N>0 is not lost at Lambda=0. For Lambda>0 the conditional-odds
inequalities imply N>=Lambda(I-K)>0; for Lambda<0 they imply
N>=(-Lambda)K>0. If Lambda=0 and ell=0, the two conditional-square identities
would simultaneously give (1-x)a+a^2=0 and xa-a^2=0. Adding them forces
a=0, excluded here. Thus N=-ell I>0 also in this case.

For nonzero D in W, tr(N^(-1)D N^(-1)D) is
||N^(-1/2)D N^(-1/2)||_F^2>0. Therefore the U8 expression proves B(D,D)>0
on the whole four-dimensional W for every strict nonzero triangle, not only
on commuting or PSD directions. The numerical W LDL checks are supplementary.

## 3. Invariant block and determinant gate: CORRECT

The affine map (alpha,beta) -> (x,a) has Jacobian determinant -1/3 and is
invertible. Its direction columns in observation coordinates are
(1,1,1,1,1,1)/3 and (2,2,2,-1,-1,-1)/3. Pulling back the independent full
Hessian gives precisely the author's matrix C. This is a congruence, not
an orthonormal-basis identification; definiteness is preserved.

C_alpha_alpha is strictly positive, not merely nonnegative: all
p_alpha_alpha vanish while p0_alpha=-(1-beta)^2 is nonzero. Hence the two by
two matrix is positive definite exactly when Delta_T=det C>0. Together
with the strict W block and zero T/W cross terms, this is an exact
equivalence with the full Sym(3) question. It is not a proof that Delta_T
is positive on the entire square.

## 4. Local Taylor coefficients and uniform quantifier: CORRECT

The claimed Taylor coefficients at lines 193--202 can be derived without
numerically differencing a nearly singular Hessian. Put y=1-x. At fixed x,
the four layer atoms are exactly

```text
p_k = q_k + c_k a^2 + d_k a^3,
q_k = x^k y^(3-k),
c = (-3y, 2-3x, 3x-1, -3x),
d = (-2, 2, -2, 2).
```

All eight formulas are independently checked as polynomial identities.
The distribution has marginal x at each coordinate, so its cross entropy
against the independent q law is exactly 3h(x). Thus

```text
H(K(x,a)) = 3h(x) - KL(p || q).
KL(p || q) = (a^4/2) sum_k m_k c_k^2/q_k + O(a^5)
           = 3a^4/[2x^2(1-x)^2] + O(a^5).
```

The last identity is verified symbolically after multiplying by x^3 y^3:
sum m_k c_k^2 x^(3-k)y^k=3xy. This proves the claimed coefficient 18 in
B_aa and 54 in det B_T. It also yields the stronger harmless estimates
B_xx=3/[x(1-x)]+O(a^4) and B_xa=O(a^3), which imply the author's looser
O(a) and O(a^2) statements.

The uniform conclusion does not follow from bare continuity of an arbitrary
matrix with a zero eigenvalue. Here the needed uniform Taylor control is
available: for x in [r,1-r], first choose |a|<r/4. Then both eigenvalues
x+2a,x-a are bounded away from zero and one on a slightly smaller closed
strip. The eight atoms and p log p are jointly analytic on a neighborhood
of that strip, with all required mixed derivatives uniformly bounded.
Taylor's theorem therefore supplies uniform remainder bounds, including
the derivatives used to form the Hessian.

Consequently det B_T/a^2 extends continuously to a=0 with value
54/[x^3(1-x)^3]>0, uniformly over the compact x interval; B_xx also stays
positive uniformly. Shrinking epsilon_r proves both signs for ALL nonzero
a with |a|<epsilon_r, of either sign. Section 2 then supplies strictness on
W. This fills the routine uniform-Taylor justification behind the author's
wording at lines 205--208; no extra hypothesis or new numerical inference
is needed. There is no uniform full-Hessian lower bound down to a=0, and
the author does not claim one.

## 5. Cancellation warnings: independently confirmed at frozen examples

The author reports the lowest floating invariant eigenvalue as
-4.547473508864641e-13, at
alpha=0.9997357815484197, beta=0.9997357811995604.
Independent exact rational jets with 150-digit logs give:

| Input encoding | Delta_T | Small invariant eigenvalue |
| --- | --- | --- |
| Displayed decimal rationals | 4.4021320562759988e-9 | 6.9769093192691935e-13 |
| Exact stored binary64 rationals | 4.4021314203300276e-9 | 6.9769083113625836e-13 |

The other invariant eigenvalue is about 6309.57. A subtraction of quantities
on that scale to extract a value near 7e-13 is plainly ill-conditioned in
binary64; the sign change is quantitatively consistent with rounding.

This is not only a high-precision heuristic: an independent outward rational
logarithm enclosure proves C_alpha_alpha>0 and Delta_T>0 at this point and
at all five supplied warning examples, under both input encodings (12/12).
It uses base-two range reduction, the atanh series with t<=1/3, 100 terms,
outward integer rounding at scale 10^80, and an explicit positive tail
bound. The exact rational determinant endpoints are stored in the JSON.
Hence these frozen warnings are not entropy-curvature counterexamples.

This audit does NOT certify all 2494 warnings: the author stores only five
examples plus the worst point. The source's floating warning label and
absolute -1e-8 bad threshold remain heuristic. In particular the script's
SCOUT status is hard-coded and must never be reused as a rigorous sign gate.

## 6. Denominators, limitations, and layered disposition

- Exact symbolic checks: 8 atom identities, 20 derivative-table entries,
  8 fixed-x atom expansions, and the cleared quartic coefficient identity.
- Independent high precision: 37/37 cases, consisting of 5 ordinary bases,
  12 warning input encodings, and 20 signed near-diagonal Taylor points.
  Full Hessian, cofactor representation, T/W cross block, invariant pullback,
  and W positivity checks pass. These finite evaluations are not a theorem.
- Rational interval gates: 12/12 warning encodings have strictly positive
  invariant determinant, with exact feasible eigenvalues alpha,beta.
- Author acceptance denominator regenerated from seed 20260908:
  240^2-240=57360 grid points plus 120000 accepted proposals, total 177360.
- The source reports bad_count=0 and warning_count=2494. This audit checks
  the script and frozen report and independently regenerates its count,
  but does NOT replay all 177360 floating sign evaluations or all warning
  cases. That part remains finite SCOUT evidence, not a full certified run.

Final layered verdict: CORRECT for the scoped analytic reductions and local
theorem; CORRECT for the 12 frozen warning sign certificates; SCOUT for
the finite source search; INCOMPLETE for global Delta_T>0 and for a full
independent high-precision replay of the author's entire batch.

No critical mathematical gap was found in the claimed local theorem.
No assertion about novelty or general n=3 concavity is made.
