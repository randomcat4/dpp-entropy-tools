# M2: simultaneous radial columns and the mixed-gain budget

Date: 2026-09-09. One bounded analytic unit; no numerical work.

**STATUS: PROVED (author candidate) for the restricted theorem in Section 1;
INCOMPLETE for the unrestricted two-column four-direction gain.** Independent
review is pending. The root N4 theorem is unchanged. Novelty is unconfirmed:
the proof extends the already checked A1 radial-column mechanism to multiple
independent leaves, using the already checked R1 two-site entropy theorem.

The new scope here is simultaneous columns, including their mixed Hessian
term, with arbitrary simultaneous motion of the central two-site block.
This is not a proof of arbitrary connection-column directions.

## 1. Frozen restricted statement, including zero column lengths

Fix an integer k>=1, numbers 0<dj<1, and nonzero vectors vj in R^2 for
j=1,...,k. For a real symmetric 2 by 2 matrix A and s in R^k define

    K(A,s) = [[A, s1 v1, ..., sk vk],
              [s1 v1^T, d1, ..., 0],
              [...                 ],
              [sk vk^T, 0, ..., dk]].

Let Omega be the set of all (A,s) for which 0<K(A,s)<I. It is open and
convex, because the kernel is affine in these parameters. Let F(A,s) be
the complete-event Shannon entropy, with natural logarithms.

**Restricted claim.** F is jointly concave on Omega. In fact, its entropy
midpoint inequality is strict between every two distinct points of Omega.
All real sj, including zero, are allowed. The fixed directions vj need not
be orthogonal or parallel and may give conflicting triangle signs.

The k=2 case is the diamond family requested in M2. The proof is written
with k because independent-leaf conditioning produces exactly the same
finite sums; it does not assert a statement for a non-diagonal leaf block.
Allowing A to vary is an explicit scope addition authorized by the route
owner during M2. The leaf marginals and vj remain fixed on each chord.

The only imported nontrivial theorem is real two-site full-event entropy
concavity, including strict finite chords, in
`research/R1/proofs/n2_concavity.md`, with commit-bound review in
`research/R1/verification/n2_concavity_commit_review.md`. We do not assume
the general three-site theorem. The single-column antecedent is
`research/A1/proofs/radial_slice_v1.md`.

## 2. Exact event conditioning and strict feasibility of every center

Write Vj=vj vj^T. For t in {0,1}^k set

    mj(tj) = dj if tj=1, and dj-1 if tj=0,
    qt = product_j dj^tj (1-dj)^(1-tj),
    Ct = A - sum_j sj^2 Vj / mj(tj).

The lower and upper extreme conditional kernels are

    C_all1 = A-sum_j sj^2 Vj/dj,
    C_all0 = A+sum_j sj^2 Vj/(1-dj).

The Schur complement of diag(dj) in K gives C_all1>0; that of diag(1-dj)
in I-K gives I-C_all0>0. For every t,

    C_all1 <= Ct <= C_all0.

Thus 0<Ct<I. The leaf marginal law is the fixed product law qt. Taking the
block determinant of each signed exact-event matrix gives

    p_K(U,t) = qt p_Ct(U),     U subset {1,2}.

This is a full-event identity. It implies the exact entropy formula

    F(A,s) = sum_j h(dj) + sum_t qt f(Ct),       f=H2.       (M2.1)

All terms are smooth on Omega. No nonlinear conditional path is being
mistaken for the affine physical K chord.

## 3. The complete second derivative along any parameter direction

Take an arbitrary feasible affine line A(z)=A+zW and sj(z)=sj+z hj,
where W is any real symmetric 2 by 2 matrix. At its current point,

    Ct'  = W-sum_j 2 sj hj Vj/mj,
    Ct'' = -sum_j 2 hj^2 Vj/mj.

Differentiating (M2.1) gives

    F'' = sum_t qt D^2 f(Ct)[Ct',Ct'] + sum_j Rj,          (M2.2)
    Rj  = -2 hj^2 sum_t qt Df(Ct)[Vj]/mj.

The first term in (M2.2) is nonpositive by the established two-site
concavity theorem. It retains every mixed term between distinct columns
and W; no separate-column concavity inference has been made.

For Rj, fix all leaf events other than tj and pair tj=0 with tj=1. Their
conditional centers, denoted C0 and C1, obey

    C0-C1 = aj Vj,       aj=sj^2/[dj(1-dj)] >=0.

Since dj/dj=1 and (1-dj)/(dj-1)=-1, this gives

    Rj = 2 hj^2 sum_(t_other) q_other
             (Df(C0)[Vj]-Df(C1)[Vj]).                    (M2.3)

If sj=0, C0=C1 and Rj=0 exactly. This covers the zero-length locus without
using the singular representation ej=alpha_j bj. If sj!=0, the segment
C1+u Vj, 0<=u<=aj, is strictly feasible by convexity.

## 4. Rank-one event identity pays every radial acceleration cost

For any strictly feasible 2 by 2 kernel C and V=vv^T, every exact event
probability along C+uV is affine in u. This follows directly because every
principal determinant under a rank-one update is affine, and finite Mobius
inversion preserves affinity. Equivalently, in the four-event formulas,
the second derivative is a signed multiple of det(V)=0.

Let l_C(V) be the vector of first derivatives of the four event masses,
and define the positive Fisher form

    I_C(V) = sum_U l_C(V)_U^2/p_C(U).

Then

    D^2 f(C)[V,V] = -I_C(V) <0   when v!=0.              (M2.4)

For strictness, some vi^2>0. The derivative of the inclusion probability
of site i is vi^2, which is a sum of derivatives of exact event masses;
not all those derivatives can be zero. All probabilities are positive.

Integrating (M2.4) on the conditional rank-one segment yields

    Df(C0)[Vj]-Df(C1)[Vj]
      = - integral_0^aj I_(C1+u Vj)(Vj) du <=0.          (M2.5)

Combining (M2.3) and (M2.5), each Rj is nonpositive; it is strictly
negative whenever hj sj!=0. Thus (M2.2) proves joint concavity.

This uses monotonicity only along the same rank-one line and tested in
the same rank-one direction. It does not assert matrix-order monotonicity
of the entropy gradient. That stronger shortcut is known to fail.

A checkable lower bound on the amount paid is also available. Cauchy-Schwarz
on the two groups of events with site i present/absent gives

    I_C(Vj) >= (vj)_i^4/[Cii(1-Cii)] >= 4(vj)_i^4.

The first inequality follows by summing the event derivatives in each
group, whose sums are +(vj)_i^2 and -(vj)_i^2. Therefore

    -Rj >= 8 hj^2 sj^2 max_i (vj)_i^4/[dj(1-dj)].        (M2.6)

No uniform positive lower bound is claimed at sj=0 or at shrinking
physical columns. Formula (M2.6) is zero there, as it should be.

## 5. Strict finite chords and all degeneracies

Consider two distinct parameter points in Omega and their connecting line.
If some hj!=0, then sj(z) is nonzero except at at most one point. Since
vj!=0, the corresponding Rj is strictly negative at all other points.
Thus F'' is strictly negative on a set of positive measure in every
nondegenerate subinterval. Integration against the positive triangular
kernel gives a strictly negative midpoint gap.

If every hj=0, then W!=0. Every Ct varies affinely by the same W. The
strict finite-chord part of the two-site theorem applies to every f(Ct),
and the strictly positive qt preserve strictness in (M2.1).

These cases exhaust distinct parameter pairs, because the nonzero vj
make the parameter-to-kernel map injective. At a point with all sj=0 and
W=0, radial-column second derivatives can be zero; this does not contradict
strict finite-chord concavity. No boundary contraction is included.

## 6. What this proves about the genuinely two-column mixed Hessian

Return to k=2, fixed A for this subsection, and call the leaves 3 and 4.
At a center with b3,b4 nonzero, restrict ej=alpha_j bj. Put Bj=bj bj^T,
Q_C=-D^2f(C), and define

    Xjt = 2 Bj/mj,
    cj = sum_t qt Q_Ct[Xjt,Xjt],
    mjoint = sum_t qt D^2f(Ct)[X3t,X4t]
           = 4(D^2f(C11)-D^2f(C10)
                -D^2f(C01)+D^2f(C00))[B3,B4].

Let pj be minus the conditional acceleration at alpha_j=1, with the other
column direction zero. Sections 3-4 prove pj>0. The full radial 2 by 2
curvature is exactly

    F'' = -(c3+p3)alpha3^2-(c4+p4)alpha4^2
           +2 mjoint alpha3 alpha4.                    (M2.7)

Because the sum of positive-semidefinite bilinear forms qt Q_Ct is itself
positive semidefinite, its Cauchy-Schwarz inequality gives

    |mjoint| <= sqrt(c3 c4).

Both cj are strictly positive: each Xjt is a nonzero rank-one direction
and (M2.4) applies. Consequently the projected gain using the FULL
single-column costs, including acceleration, obeys the strict bound

    gain_radial = |mjoint|/sqrt((c3+p3)(c4+p4))
       <= sqrt(c3 c4/((c3+p3)(c4+p4))) <1.              (M2.8)

This controls the mixed Hessian rather than simply ignoring it. It succeeds
because the exact DPP rank-one geometry proves that acceleration adds to
the available cost. It is the gain on the two-dimensional radial direction
subspace, not the full four-dimensional operator gain of M1. At a zero
column, use the hj vj formulation from Sections 3-4 instead; that column's
Hessian and mixed terms vanish at the point, while the full concavity
statement remains valid.

## 7. A concrete conflicting-sign diamond covered by this theorem

For every fixed rational 0<r<=1/2 take the M1 center

    A=[[1/2,1/10],[1/10,1/3]],
    u=(1/5,1/6)^T,   v=(1/7,-1/8)^T,
    d3=r^2, d4=r^4, b3=r u, b4=r^2 v.

Fix these d3,d4,u,v on each tested chord. The simultaneous direction
e3=b3, e4=-b4 is covered: it changes the two independent column lengths
in opposite directions and preserves the conflicting triangle signs on
|z|<=1/4. It is not the generic nonradial e,f direction proposed in M1.

For an explicit endpoint feasibility check, on this interval the scaled
vectors satisfy

    |(1+z)u| <= (1/4,1/4),
    |(1-z)v| <= (1/5,1/6).

Their outer-product absolute row sums total at most 119/600 and 67/360,
respectively, strictly less than the A diagonal-dominance margins 2/5 and
7/30. The same bounds are less than those of I-A. The lower Schur
complement therefore stays positive, as does the upper one, whose
outer-product coefficients r^2/(1-r^2), r^4/(1-r^4) are both <=1.
The whole chord is strictly feasible and has strictly negative entropy
gap. This holds for every such r without assuming a compact lower bound
on the leaf marginals. The theorem also permits central A movement whenever
the resulting endpoints remain strictly feasible.

## 8. Exact breakpoint for arbitrary two-column directions

For arbitrary ej in R^2, set Sj=bj ej^T+ej bj^T and Xjt=Sj/mj. Use the
notation

    cj = sum_t qt Q_Ct[Xjt,Xjt] >=0,
    aj = 2 ej^T sum_(t_other) q_other (G_C0-G_C1) ej,
    m  = sum_t qt D^2f(Ct)[X3t,X4t].

For the two scalar coefficients multiplying these chosen directions,
the full negative-curvature costs are lj=cj-aj. The exact mixed term is
the M1 discrete mixed Hessian. Conditional-Hessian Cauchy-Schwarz only gives

    m^2 <= c3 c4.

The desired two-direction sign gate instead needs lj>=0 and

    m^2 <= (c3-a3)(c4-a4).                              (M2.9)

If an aj is positive, the needed budget may be smaller than c3 c4. The
rank-one proof above no longer applies because the conditional-center
separation is parallel to bj bj^T but the gradient difference is tested
against ej ej^T. For nonparallel bj,ej these are different directions.
Existing A1 evidence shows that such acceleration can indeed be positive;
concavity alone gives no sign in this mismatched test.

Equivalently, the conditional-Hessian Cauchy-Schwarz slack would have to pay

    c3 c4-m^2 >= c3 a4+c4 a3-a3 a4,                     (M2.10)

together with nonnegative lj. Equation (M2.10) is explicitly an equivalent
remaining obligation for the chosen two directions, NOT a newly proved
lemma or a relabelled research advance. This unit supplies no proof of it
for arbitrary directions. Pure Fisher Cauchy-Schwarz is still weaker: the
conditional H2 Hessian itself contains the event log-odds acceleration
correction, so Fisher costs cannot silently replace cj.

## 9. Certification, failures, and stop record

- PROVED author candidate: the precisely frozen jointly radial-column
  theorem, including arbitrary central W, every sj=0 case, and strict
  finite chords. The proof uses the known two-site theorem and exact
  rank-one event affinity, not a general n=3 concavity hypothesis.
- PROVED author candidate: projected mixed-gain bound (M2.8) with the full
  single-column costs, and the explicit conflicting-sign family exclusion.
- INCOMPLETE: arbitrary nonradial two-column directions and (M2.9)/(M2.10).
- Rejected shortcut: conditional-Hessian Cauchy-Schwarz alone pays the full
  budget. The precise failure is a positive mismatched acceleration aj.
- Numerical function calls, seeds, numerical PIDs and background jobs: none;
  actual numerical denominator 0. No Lean or interval certificate run.
- Independent review: pending. Research novelty: unconfirmed; this is a
  multiple-column extension of the A1 mechanism, not a main-problem claim.
- Scope changes during the unit: the route owner explicitly authorized
  arbitrary central W and formulation with k independent leaves. No
  unrestricted frozen N4 premise was changed.

This completes one bounded M2 unit. No new scan, higher-dimensional search,
or further generalization is launched by this child. Only this file was
added in M2; M1 artifacts and other agents' files were not changed.
