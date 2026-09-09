# PR51 original half-filled theorem — second independent proof review

Verdict: **ACCEPTED_SCOPED** for PR51 head `4baebc317896278dcb8f0947d308fdce037c87cf`, original three-file package only.

This is an analytic second nonauthor review. I did not read the first review, did not fetch or use the private Drive verifier referenced by the author files, did not use PR41/PR43 theorem black boxes, did not execute math computation, and did not review the later `continuation.md` added at successor head `2e4b8754ad4af2fe055ebeeef1159877773372a3`.

## Frozen source and claim

Source directory:

`research/I05-22-missing-edge-20260909/`

Files read in full:

1. `proof_half_filled.md`
2. `sources_and_routes.md`
3. `verification.md`

The theorem under review is the strict Hessian negativity claim at the half-filled missing-edge center

\[
K(b,c)=
\begin{pmatrix}
1/2&0&b\\
0&1/2&c\\
b&c&1/2
\end{pmatrix},
\qquad
bc\ne0,\qquad 4(b^2+c^2)<1,
\]

for every nonzero real symmetric `3 x 3` direction `D` (`proof_half_filled.md:7-19`). The source explicitly excludes strictness on the coordinate axes `bc=0`, arbitrary chords leaving this family, and general real three-point concavity (`proof_half_filled.md:21-23`, `proof_half_filled.md:224-228`).

## Step-by-step review

### 1. Complete-event Hessian identity

The proof starts from the eight complete-event atoms obtained by Boolean inclusion-exclusion (`proof_half_filled.md:27-40`). For a true affine line `K+tD`, normalization gives

\[
-H''=\sum_S(p'_S)^2/p_S+\sum_Sp''_S\log p_S
\]

as stated in `proof_half_filled.md:40-44`. The cofactor identity then groups the second derivatives of the two-point minors and the determinant into

\[
\mathcal B_K(D)=F_K(D)+2\sum_{i<j}l_{ij}\det D_{ij}
+2\Lambda\operatorname{tr}(K\operatorname{adj}D)
\]

(`proof_half_filled.md:46-52`). I checked the sign pattern from the displayed atom formula: each `q_ij''` contributes the log face ratio `log(p_0p_ij/(p_ip_j))`, and `q_123''` contributes the alternating full-cube ratio `Lambda`. This step includes the acceleration term and does not replace complete-event entropy by cardinality entropy.

### 2. Half-filled atoms, sign conjugation, and log signs

The diagonal sign conjugation reducing to `b,c>0` is legitimate: it preserves principal minors and complete-event probabilities and maps symmetric directions bijectively (`proof_half_filled.md:56-62`). Thus no direction is lost.

At the half-filled missing-edge center the atoms are

\[
\tfrac18(1-s,1+d,1-d,1+s,1+s,1-d,1+d,1-s)
\]

with `0<s<1`, `|r|<1`, and `k=s sqrt(1-r^2)` (`proof_half_filled.md:58-67`). From these atoms `Lambda=0`, and the three face log ratios produce the positive diagonal matrix

\[
N=\operatorname{diag}(g(s)-g(d),g(s)+g(d),W)
\]

(`proof_half_filled.md:69-82`). The positivity follows from `|d|<s`, monotonicity/oddness of `g`, and `W=log((1-d^2)/(1-s^2))>0`.

### 3. Exact 2+4 symmetry decomposition

The map `J(K)=S(I-K)S`, `S=diag(1,1,-1)`, fixes the center and preserves entropy by complementation plus sign conjugation. Its derivative is `L(D)=-SDS`, giving the two Hessian eigenspaces

- `D13,D23` only;
- `D11,D22,D33,D12` only

(`proof_half_filled.md:84-91`).

The cross terms vanish by Hessian invariance under this linear involution, not because a mixed block was ignored. This is a valid exact quadratic-form decomposition. In the two-dimensional sector, the displayed formula

\[
\mathcal B=F+2[g(s)+g(d)]D_{13}^2+2[g(s)-g(d)]D_{23}^2
\]

is strictly positive for any nonzero sector vector (`proof_half_filled.md:93-99`). This uses only nonnegativity of the retained complete Fisher term.

### 4. Four-dimensional block and full Fisher retention

For the remaining sector the coordinates

\[
P=D_{11}+D_{22},\quad E=D_{11}-D_{22},\quad Z=D_{33},\quad R=D_{12}
\]

are invertible linear coordinates on that sector. The first derivatives of the four nonredundant atom pairs are displayed in `proof_half_filled.md:103-114`; pairing complementary atoms with the weights in (4) gives the full Fisher form with denominators `(1-s^2)` and `(1-d^2)` (`proof_half_filled.md:116-123`). Those denominators keep the rare-event terms; no lower-bound shortcut is being used.

The acceleration term is

\[
A=-\frac W2(P^2-E^2)-2Z[g(s)P+g(d)E]+2WR^2
\]

(`proof_half_filled.md:122-128`). I checked the signs from the cofactor formula: `det D_12=(P^2-E^2)/4-R^2`, `det D_13=(P+E)Z/2`, and `det D_23=(P-E)Z/2`, with `l_12=-W`, `l_13=-(g(s)+g(d))`, and `l_23=-(g(s)-g(d))`. The mixed diagonal/Fisher terms are both retained.

The shape coordinate `T=sqrt(1-r^2)R` is invertible for the theorem's domain because `bc!=0` implies `|r|<1` (`proof_half_filled.md:130-137`). Thus the matrix `G_s(r)` in `(P,E,Z,T)` coordinates represents the same four-dimensional sector at every covered center.

### 5. Fixed-shape derivative and inertia continuation

The proof rewrites `G_s(r)` as a sum of two rank-one square terms and explicit log/cross terms (`proof_half_filled.md:140-149`). Differentiating at fixed `r` gives the rational matrix `dot G` in `proof_half_filled.md:151-160`. The derivative formula is consistent with

- `W'=2s(1-r^2)/((1-s^2)(1-r^2s^2))`;
- derivative of `2aa^T/(1-s^2)`;
- derivative of `2b_*b_*^T/(1-r^2s^2)`;
- derivative of `-g(s)J13` and `-g(rs)J23`.

The determinant certificate is

\[
\det\dot G_s(r)=
\frac{48s^4(1-r^2)^2(1+r^2-2r^2s^2)}
{(1-s^2)^4(1-r^2s^2)^4}>0
\]

(`proof_half_filled.md:162-168`). The last factor is `(1-r^2)+2r^2(1-s^2)>0`, so it is positive on exactly the open domain `0<s<1`, `|r|<1`.

The proof does not infer positive definiteness from determinant sign alone. It also supplies a seed: at `r=0`, all four leading principal minors of `dot G_s(0)` are positive (`proof_half_filled.md:170-179`). Since for fixed `s` the interval `r in (-1,1)` is connected and `det dot G_s(r)` never vanishes, the inertia-continuation lemma in `proof_half_filled.md:181-187` validly propagates positive definiteness to every `r` in the open interval.

### 6. Integration from singular `G_0`

At `s=0`, the fixed-shape formula gives `G_0(r)=diag(2,2,4,0)`, only semidefinite (`proof_half_filled.md:189-195`). This is not a gap: for fixed `r`, `dot G_u(r)` is positive definite for every `u in (0,s)`, so for any nonzero vector `x`,

\[
x^TG_s(r)x=x^TG_0(r)x+\int_0^s x^T\dot G_u(r)x\,du>0.
\]

The zero `T` direction in `G_0` is made strict by the positive integral. The argument also keeps the order of quantifiers straight: first fix `s` and move `r` for the inertia step; then fix `r` and integrate in `s`. This matches the review scope requested by the author source (`verification.md:41-45`).

## Attack checks

- **All six directions.** The `2+4` decomposition covers all real symmetric `3 x 3` coordinates. The coordinate maps are bijective in the covered domain (`proof_half_filled.md:84-99`, `proof_half_filled.md:103-137`, `proof_half_filled.md:195`).
- **No hidden PR41/PR43 dependency.** The proof states it rederives the needed events, cofactor identity, Fisher block, seed minors, and shape extension, and does not import PR41 or PR43 as theorem dependencies (`proof_half_filled.md:224-226`). I did not use those black boxes.
- **No determinant-only definiteness leap.** The determinant is used only to prevent eigenvalue crossing after a positive seed is established (`proof_half_filled.md:170-187`).
- **No endpoint overreach.** The proof works on `0<s<1`, `|r|<1`; these are exactly `4(b^2+c^2)<1` and `bc!=0`. The axes `bc=0`, `r=±1`, strictness there, and `s=1` are excluded or only mentioned as non-strict continuity limits (`proof_half_filled.md:21-23`, `proof_half_filled.md:181-195`).
- **Fixed observation coordinates.** The theorem and proof explicitly avoid rotated-basis entropy (`proof_half_filled.md:19-21`, `proof_half_filled.md:56-62`). Sign conjugation is a coordinate sign flip preserving principal minors, not an arbitrary orthogonal diagonalization.
- **Illustrative Jensen check.** The strict negative Jensen interval in `proof_half_filled.md:197-222` is clearly labeled as an illustration, not proof. The author-side verification file also says the exact checks are not independent review and the Jensen sign is not evidence for the universal theorem (`verification.md:1-3`, `verification.md:35-39`).

## Boundaries of acceptance

Accepted here:

- Strict negative Hessian at every strict half-filled missing-edge center with `bc!=0` and `4(b^2+c^2)<1`, for every nonzero real symmetric direction.
- The proof's use of complete-event entropy, fixed observation coordinates, full Fisher denominators, and exact acceleration.

Not accepted here:

- The later PR51 `continuation.md`.
- Any private Drive verifier or author-side script as independent evidence.
- General missing-edge centers with arbitrary diagonal entries.
- General real three-point entropy concavity.
- A universal quantitative margin.
- Arbitrary chords whose intermediate centers leave the stated half-filled family.
- Strictness on the axes `bc=0`; the source only states a non-strict continuity boundary there.
- Novelty, publication priority, or relation to unpublished/private material.

## Final verdict

**ACCEPTED_SCOPED.** I find no load-bearing gap in the original three-file PR51 proof for the stated half-filled missing-edge theorem at frozen head `4baebc317896278dcb8f0947d308fdce037c87cf`. The proof closes the complete-event Hessian inequality by an exact entropy symmetry split and a positive-definite four-dimensional block certificate, with the open endpoint and axis cases properly scoped.
