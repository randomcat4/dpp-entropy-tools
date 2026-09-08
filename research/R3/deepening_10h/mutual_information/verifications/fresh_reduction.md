STATUS: CORRECT

# Fresh verification of D10-C mutual-information deliverables

Role: non-author verifier.  I did not modify the author files and did not
inspect the in-progress `analytic_bound/` branch.

## Files read

- `research/R3/deepening_10h/mutual_information/identity.md`
- `research/R3/deepening_10h/mutual_information/family.md`
- `research/R3/deepening_10h/mutual_information/probe.py`
- `research/R3/deepening_10h/mutual_information/mi_hessian_diagnostic.py`
- `research/R3/deepening_10h/mutual_information/paired_sign_diagnostic.py`
- `research/R3/deepening_10h/mutual_information/validate_diagnostic.py`
- `research/R3/deepening_10h/mutual_information/run_log.md`
- `research/R3/deepening_10h/mutual_information/verdict.md`
- `research/R3/deepening_10h/mutual_information/results/{manifest.json,summary.json,validation.json,diagnostic_validation.json,evidence_index.json,mi_hessian_diagnostic.json,paired_sign_diagnostic.json,candidate_ledger.csv}`

No external search was run.  No server was used.

## Overall verdict

The current main D10-C deliverables are internally correct as an
`INCOMPLETE` search/mechanism result:

- the FT-C mutual-information identity is correct;
- the simplex identity
  \[
  \Delta=-\langle q-p_0,\log p_0\rangle-\operatorname{KL}(q\|p_0)-\operatorname{JS}(p_-,p_+)
  \]
  is correct;
- the rank-two event-law quadratic formula and sign-flip mechanism are
  correct;
- the recorded feasibility, event semantics checks, and diagnostic counts are
  consistent with the scripts and results;
- no positive R3 gap candidate is claimed.

No critical gap found.

## 1. FT-C identity

For a finite block split \(E=A\sqcup B\), let \(U=Y\cap A\) and \(V=Y\cap B\).
Because inclusion probabilities on a finite Boolean lattice determine the
law by Möbius inversion, the marginal law of \(U\) is the DPP with kernel
\(K_A\), and similarly for \(V\).

For each \(j\in\{-,0,+\}\),

\[
I_j=I(U_j;V_j)
=H(K_{A,j})+H(K_{B,j})-H(K_j).
\]

Equivalently,

\[
H(K_j)=H(K_{A,j})+H(K_{B,j})-I_j.
\]

Taking endpoint average minus midpoint gives

\[
\Delta_E
=\Delta_A+\Delta_B+I_0-\frac{I_-+I_+}{2}.
\]

This matches `identity.md` lines 21--35 and `probe.py` line 176, where the
recorded residual is

\[
\Delta_E-\Delta_A-\Delta_B-\text{MI\_bump}.
\]

The sign convention is consistent throughout:

\[
\Delta=\frac{H_-+H_+}{2}-H_0.
\]

Positive \(\Delta_E\) would be a concavity violation.

## 2. Simplex geometry identity

Let

\[
q=\frac{p_-+p_+}{2},
\qquad
r=q-p_0.
\]

Then

\[
H(q)-H(p_0)
=-\sum_x(q_x-p_{0,x})\log p_{0,x}
-\sum_x q_x\log\frac{q_x}{p_{0,x}},
\]

because \(\sum_x(q_x-p_{0,x})=0\).  Also

\[
\operatorname{JS}(p_-,p_+)
=H(q)-\frac{H(p_-)+H(p_+)}{2}.
\]

Therefore

\[
\Delta_E
=\frac{H(p_-)+H(p_+)}2-H(p_0)
=-\langle r,\log p_0\rangle-\operatorname{KL}(q\|p_0)-\operatorname{JS}(p_-,p_+).
\]

This matches `identity.md` lines 37--53 and `probe.py` line 176:

```text
geometry_identity_residual = gap - (geom - kl - js)
```

with `geom=-r@log(p0)`.

KL and JS are nonnegative under the strict-positive probability setting.  Thus
the interpretation is correct: a positive gap requires the geometry term
\(G=-\langle r,\log p_0\rangle\) to exceed `KL+JS`.  In particular,
`G/(KL+JS)<1` rules out a positive gap for that evaluated chord when `G>0`.

## 3. Rank-two quadratic event law

For an exact event \(S\), the event determinant representation is

\[
p_K(S)=(-1)^{|S^c|}\det(K-I_{S^c}).
\]

At a strict center \(M\), set

\[
A_S=M-I_{S^c}.
\]

Strict atom positivity gives \(\det A_S\ne0\).  For

\[
D=uu^T-cvv^T,\qquad c>0,
\]

the matrix determinant lemma gives

\[
p_{M+tD}(S)
=p_M(S)
\det\!\left(I_2+t\,\operatorname{diag}(1,-c)
\begin{bmatrix}u&v\end{bmatrix}^T
A_S^{-1}
\begin{bmatrix}u&v\end{bmatrix}\right).
\]

Expanding the \(2\times2\) determinant gives

\[
p_{M+tD}(S)=p_0(S)+t\,a(S)+t^2\,b(S),
\]

where

\[
a=p_0\left(u^TA_S^{-1}u-c\,v^TA_S^{-1}v\right),
\]

\[
b=-c\,p_0\left[
(u^TA_S^{-1}u)(v^TA_S^{-1}v)
-(u^TA_S^{-1}v)^2
\right].
\]

This agrees with `identity.md` lines 55--69.  It also agrees with the
implementation for a general already-assembled direction \(D\):

```text
a = p0 * tr(A^-1 D)
b = 0.5 * p0 * (tr(A^-1 D)^2 - tr((A^-1 D)^2))
```

in `probe.py` lines 155--156.  The recorded
`quadratic_event_max_error <= 5.551115123125783e-17` confirms the numerical
implementation is consistent with this quadratic law on the finite evaluated
set.

## 4. Sign-flip mechanism

For fixed \(M,u,v,c,t\), compare

\[
D_-=uu^T-cvv^T,
\qquad
D_+=uu^T+cvv^T.
\]

The quadratic coefficients are opposite:

\[
b_+=-b_-.
\]

Therefore for the symmetric endpoint mixture,

\[
q-p_0=t^2b,
\]

and the geometry term

\[
G=-\langle q-p_0,\log p_0\rangle
\]

also flips sign.  The linear coefficient, KL cost, and JS cost need not flip
or remain fixed.  This is exactly how `identity.md` lines 71--75 and
`paired_sign_diagnostic.py` lines 18--30 describe the mechanism.

The results support this implementation: `paired_sign_diagnostic.json` reports

```text
max_geometry_flip_residual = 2.8437064443671833e-15
positive_geometry_terms_in_PSD_companion = 27
max_PSD_geometry_over_KL_plus_JS = 0.05987417021531596
```

Since the maximum PSD `G/(KL+JS)` ratio is far below `1`, the positive
geometry terms are too small to produce a positive total gap.

## 5. Feasibility and event semantics checks

`probe.py` uses exact rational LDL certificates in `certificate`:

- it certifies \(K-mI\succ0\);
- it certifies \(I-K-mI\succ0\);
- the margin `m` is rational and then checked by exact Fraction arithmetic.

The result summaries record:

```text
min_exact_margin = 0.004107
min_direction_rank = 2
max_mobius_error = 4.2457357074532354e-16
max_information_identity_residual = 2.6840508982051148e-15
max_geometry_identity_residual = 2.8035299776130174e-15
```

For n≤8, direct Möbius checks are used on base points and selected endpoints.
`diagnostic_validation.json` separately reports

```text
endpoint_mobius_checks = 12
max_endpoint_mobius_error = 3.2612801348363973e-16
```

The exact DPP event formula implementation in `Events.evaluate` matches

\[
p_K(S)=(-1)^{|S^c|}\det(K-I_{S^c}),
\]

with an explicit determinant-sign check before using the positive atom value.

## 6. Rank-two and non-thinning checks

The main direction generator requires exact integer Gram nondegeneracy on both
blocks.  That implies global \(u,v\) independence and rules out collapse to
rank one for

\[
uu^T/(u^Tu)-c\,vv^T/(v^Tv).
\]

The direction is indefinite in the main probe by float inertia gate, and the
algebraic rank-two conclusion follows from the independence of the two rank
one generators with positive \(c\).  `validate_diagnostic.py` additionally
checks the rounded Hessian diagnostic directions by exact rational row
reduction and exact non-proportionality to the center.

The non-thinning explanation is correct for the tested n=6,8,11 cases:
a rank-two direction cannot be a nonzero scalar multiple of the full-rank
strict center \(M\).

## 7. MI and entropy conventions

The implementation uses natural-log Shannon entropy:

```text
entropy(p) = -p @ log(p)
I = p @ log(p/prod)
```

`MI_bump` is defined as

\[
I_0-\frac{I_-+I_+}{2}.
\]

`marginal_deficit_sum` is `-Delta_A-Delta_B`, so

\[
\Delta_E=\Delta_A+\Delta_B+\text{MI\_bump}
=\text{MI\_bump}-\text{marginal\_deficit\_sum}.
\]

This matches the textual interpretation in `identity.md`, `family.md`, and
`verdict.md`.  The author correctly avoids calling negative or zero scout
values counterexamples.

## 8. Count and denominator audit

I independently parsed the result files and obtained:

```text
original proposals = 78
accepted rank-two indefinite directions = 77
filtered proposals = 1
original finite chord evaluations = 231
original ledger rows = 309
full MI Hessian centers = 9
full MI Hessian finite chord evaluations = 9
paired sign finite chord evaluations = 54
paired sign PSD chords = 27
total finite chord evaluations = 294
additional random proposals = 0
float candidates across all stages = 0
positive MI midpoint bumps across all stages = 0
```

The arithmetic is consistent:

\[
231+9+54=294.
\]

The warning in `evidence_index.json` is appropriate: `294` is an evaluation
count, not a claim of 294 pairwise-distinct mathematical chords, because the
controlled paired experiment can revisit an existing indefinite direction at
a common step.

## 9. Boundary of this verification

I verified the current main D10-C deliverables only.  I did not verify any
in-progress `analytic_bound/` material.  The status remains `INCOMPLETE` for
the research route because no positive gap or general exclusion theorem was
proved.  The identities and recorded finite diagnostics are correct within
their stated scope.
