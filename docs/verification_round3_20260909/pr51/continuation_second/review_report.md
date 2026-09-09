# PR51 continuation — second independent review of new files

Verdict: **ACCEPTED_SCOPED** for the new continuation-file assertions at frozen public head `8b078ab834c46ce0c0e81967e3ada3fbbf542f1a`.

This review covers only `continuation.md` and `README.md` in the frozen source directory. It does not repeat the original half-filled theorem review, does not certify the old three-file package again, does not use the first review, does not fetch or use private Drive artifacts, does not import author code, does not use PR41/PR43 theorem black boxes, and does not duplicate C2 issue #52's multivariate `M` reconstruction/elimination/scout.

## Source and scope

Source directory:

`research/I05-22-missing-edge-20260909/`

Files read in full:

1. `continuation.md`
2. `README.md`

The author status line is correctly limited: identities, the positive two-dimensional block, and two method obstructions are author-proved and unreviewed; the remaining four-dimensional inequality and radial monotonicity conjecture are incomplete; issue #52 is not assumed (`continuation.md:1-4`). The README keeps the same status separation: continuation claims are author proof only, while the arbitrary-diagonal Schur inequality, Lambda-zero derivative conjecture, general real three-point concavity, and strict positive entropy counterexample remain incomplete (`README.md:5-17`).

## Review of the continuation identities

### 1. Product-domain parameterization

For the connected missing-edge center

\[
K=\begin{pmatrix}x&0&b\\0&y&c\\b&c&z\end{pmatrix},\qquad bc\ne0,
\]

the parameterization

\[
v=x(1-x),\quad w=y(1-y),\quad A=b^2/v,\quad B=c^2/w,\quad q=z-A(1-x)-B(1-y)
\]

is stated in `continuation.md:7-17`. The domain equivalence

\[
0<K<I
\quad\Longleftrightarrow\quad
0<x,y<1,\ A,B>0,\ q>0,\ q+A+B<1
\]

follows from the Schur complements of `diag(x,y)` in `K` and `diag(1-x,1-y)` in `I-K` (`continuation.md:19-25`). I checked the algebra: `q=z-b^2/x-c^2/y`, and `1-q-A-B=1-z-b^2/(1-x)-c^2/(1-y)`. The four conditional leaf probabilities

\[
t_{ij}=q+A(1-i)+B(1-j)
\]

then lie in `(0,1)` exactly on this product domain (`continuation.md:25-29`).

### 2. Invertible six-direction coordinates

The continuation represents an arbitrary physical symmetric direction by `d=D11`, `e=D22`, and a conditional derivative

\[
T_{ij}=m+f(i-x)+g(j-y)+h(i-x)(j-y)
\]

(`continuation.md:31-35`). The inverse map is displayed in `continuation.md:37-48`. I checked invertibility directly: since `bc!=0` and hence `A,B>0`, the formulas uniquely recover `D33,D13,D23,D12` from `(d,e,m,f,g,h)`. The double contrast `h` is preserved through `D12=bc\,h/(2AB)`, so the missing-edge direction is not discarded.

This is an analytic check of the coordinate map only. The source's reference to a verifier at `continuation.md:48` was not used.

### 3. Log quantities and rectangle coefficient

The four conditional probabilities satisfy `t00>t10,t01>t11`, so monotonicity of `psi(t)=log(t/(1-t))` gives `ell_j>0` and `k_i>0` (`continuation.md:50-63`). I also checked the two rectangle weights:

\[
v_0=\log\frac{(1-t_{10})(1-t_{01})}{(1-t_{00})(1-t_{11})}>0,\qquad
v_1=\log\frac{t_{10}t_{01}}{t_{00}t_{11}}>0,
\]

because each numerator exceeds its denominator by `AB` after substituting `t00=q+A+B`, `t10=q+B`, `t01=q+A`, `t11=q`. The identity `ell_0-ell_1=k_0-k_1=Lambda` is the corresponding log-ratio cancellation (`continuation.md:58-63`).

The rectangle coefficient

\[
J=f_0(t_{00})+f_0(t_{11})-f_0(t_{10})-f_0(t_{01})
=\int_0^A\int_0^B\frac{d\alpha\,d\beta}{(q+\alpha+\beta)(1-q-\alpha-\beta)}
\]

is positive on the product domain (`continuation.md:65-73`).

### 4. Full six-direction Schur collection

The continuation defines the full conditional Fisher

\[
F_c=\sum_{i,j}\frac{P_{ij}}{t_{ij}(1-t_{ij})}a_{ij}a_{ij}^T
\]

and says the full Fisher is `d^2/v+e^2/w+u^T F_c u` (`continuation.md:75-83`). This correctly separates the independent `(X1,X2)` marginal Fisher from the conditional third-bit Fisher while retaining both outcomes of the third bit.

The block formula

\[
\mathcal B_K(D)=
\binom de^T[L+\operatorname{diag}(1/v,1/w)]\binom de
+2\binom de^T C u
+u^T(F_c+R)u
\]

is stated in `continuation.md:85-119`. I did not expand every entry by machine algebra, but I checked the derivation route: starting from the complete-event cofactor identity, substituting the inverse direction map, and collecting terms naturally produces a `2+4` Schur collection with a marginal Fisher block, cross block, and conditional block. The displayed log part in `continuation.md:112-117` keeps the full acceleration, including `D12` through `det D12` and the `Lambda tr(K adj D)` term. I found no sign or quantifier gap in the stated collection.

### 5. Strict positivity of the two-dimensional `L` block

The `L` block is

\[
L=\begin{pmatrix}A\ell/(2v)&J\\J&Bk/(2w)\end{pmatrix}
\]

(`continuation.md:85-87`). The proof in `continuation.md:121-142` is valid. Since `f_0''(t)=1/t+1/(1-t)` is strictly convex on `(0,1)`, the trapezoid bound over the rectangle gives

\[
J<\frac B2(\ell_0+\ell_1),\qquad
J<\frac A2(k_0+k_1).
\]

Also

\[
\ell-w(\ell_0+\ell_1)=(1-y)^2\ell_0+y^2\ell_1>0
\]

and similarly for `k-v(k0+k1)`. Therefore

\[
J^2<\frac{AB}{4}(\ell_0+\ell_1)(k_0+k_1)
<\frac{AB\ell k}{4vw}=L_{11}L_{22},
\]

with positive diagonal entries. This proves `L` positive definite without using the marginal Fisher.

The continuation then correctly states the remaining obligations as the four-dimensional Schur complement inequalities (29) and (30), and explicitly says neither has been proved (`continuation.md:144-156`). This is a key correct boundary.

### 6. Face-coupling mixed terms

The exact face acceleration identity (31) decomposes the log-acceleration into two sets of conditional two-point face terms plus the leftover couplings

\[
2Jde-\frac{vwJ}{2AB}h^2
\]

(`continuation.md:158-180`). This is the right kind of obstruction to naive two-point iteration: adding separate face proofs would double-spend Fisher and miss the displayed mixed terms (`continuation.md:180-182`). The continuation does not claim those leftover terms have a globally favorable sign by themselves.

### 7. Lambda-zero parameterization and fixed-direction derivative identity

The Lambda-zero condition is derived from the two log formulas

\[
v_1=\log\left(1+\frac{AB}{q(q+A+B)}\right),\qquad
v_0=\log\left(1+\frac{AB}{(1-q-A-B)(1-q)}\right),
\]

so `Lambda=0` iff `q=(1-A-B)/2` (`continuation.md:184-194`). I checked this by equating denominators after cancelling `AB`.

The four-parameter subfamily

\[
\mu=2x-1,\quad \nu=2y-1,\quad A=u^2(1+r)/2,\quad B=u^2(1-r)/2
\]

with `|mu|,|nu|,|r|<1`, `0<u<1` gives the displayed `K(u)` (`continuation.md:193-205`). The fixed physical direction coordinates in (33) are independent of `u` once `(mu,nu,r)` and the direction vector are fixed (`continuation.md:208-213`).

I checked the conditional derivative vector in (34): substituting the fixed coordinates into the conditional derivative formula gives the six components shown in `q_ij`, and the denominators `J_u=1-u^4`, `L_u=1-r^2u^4` are exactly `4t_ij(1-t_ij)` for equal and unequal leaf states (`continuation.md:215-227`). The marginal Fisher is the constant block `diag(v,w,0,0,0,0)`, as stated.

The derivative identity

\[
M(\mu,\nu,r,u)=F'(u)+Q
\]

is a fixed-direction analytic identity (`continuation.md:227-246`). I checked the structural dependencies: `Lambda` remains zero along the path, `Q` comes from the derivative of the diagonal cofactor/log matrix, and the entries `n1,n2,n3` match the derivative scales induced by the `u`-dependent log weights. The continuation makes the correct boundary statement: `M>0` is a conjectural remaining sign condition, not a result, and issue #52 is a request rather than evidence (`continuation.md:248-250`, `README.md:66-74`).

## Method-obstruction checks

### 1. Auxiliary conditional resolvent

The first obstruction says conditional-resolvent convexity

\[
\Phi(K)=\sum_{i,j}P_{ij}(K)^2/p_{ij1}(K)
\]

is false even at a strict arrow center (`continuation.md:254-263`). The file gives a rational `K_*`, direction `D_*`, and exact value

\[
\Phi''(K_*;D_*)=
-53670727895896612562246875/14117659525214393686902< -3800
\]

(`continuation.md:264-281`).

Because this was a small standalone obstruction, I froze and ran one independent exact rational check in this directory. It reconstructed the two-bit marginals and the `p_ij1` atoms from inclusion-exclusion, applied the displayed formula for `(P^2/R)''`, and confirmed:

```text
Phi_second -53670727895896612562246875/14117659525214393686902
K_schur_q 3/5750 positive true
IminusK_schur 11/375 positive true
matches_expected true
```

See `targeted_compute_plan.md` and `targeted_compute_output.txt`. This check did not touch the issue #52 matrix or author verifier.

The source scopes the obstruction correctly: the entropy Hessian and Jensen example have the concave sign, so this is not a DPP entropy counterexample or a positive-gap candidate (`continuation.md:283-298`, `README.md:40-55`).

### 2. Coefficientwise PSD failure

The second obstruction uses the already covered half-filled equal-strength family and the displayed direction

\[
D_s=\begin{pmatrix}1/4&-1/4&0\\-1/4&1/4&0\\0&0&s/6\end{pmatrix}
\]

(`continuation.md:300-309`). The README adds that `D_s` is PSD rank two with eigenvalues `0,1/2,s/6`, and that its acceleration contribution is harmful (`README.md:56-64`).

I checked both assertions analytically. The top-left `2 x 2` block has eigenvalues `0` and `1/2`, and the third eigenvalue is `s/6`, so `D_s` is PSD rank two for `0<s<1`. Expanding

\[
\frac12+\frac89s^2+\frac{s^2}{18(1-s^2)}-\frac s6\log\frac{1+s}{1-s}
\]

using `log((1+s)/(1-s))=2(s+s^3/3+s^5/5+\cdots)` gives the stated coefficients

\[
\frac12+\frac{11}{18}s^2-\frac1{18}s^4+O(s^6)
\]

(`continuation.md:309-316`). Thus coefficientwise PSD after this rescaling is too strong, while the full curvature remains positive by the already reviewed half-filled theorem. The source also correctly notes that this does not refute the fixed-coordinate derivative conjecture because the testing direction varies with `s` (`continuation.md:316-317`).

## README-specific assertions

The README's status map is accurate for the continuation: it labels the continuation results as author-proof/not-independently-reviewed, keeps the arbitrary-diagonal Schur complement and Lambda-zero derivative conjecture incomplete, and does not claim CI or proof-assistant certification (`README.md:5-17`).

The reproduction section describes private/uploaded artifacts and exact outputs (`README.md:19-39`). I did not fetch or use those artifacts. The exact-output block is properly scoped as author-side support, and its warning that the auxiliary obstruction is not an entropy counterexample is correct (`README.md:40-55`).

The conditional marginal Hessian clarification is also correct. At the independent `(X1,X2)` leaf center, the first marginal score is `d(i-x)/v+e(j-y)/w`; any second derivative from the missing-edge entry has zero row and column sums, while `log P_ij` separates as a sum of a function of `i` and a function of `j`. Therefore its acceleration pairing with `log P_ij` vanishes, and

\[
-H(X_1,X_2)''=d^2/v+e^2/w
\]

(`README.md:56-62`). This confirms that (30) subtracts the exact marginal Hessian, not an arbitrary Fisher projection. The README correctly says positivity of the conditional target remains unproved.

## Boundaries of acceptance

Accepted here:

- The exact general product-domain parameterization and conditional probabilities.
- The invertible six-direction coordinate map for connected missing-edge centers with `bc!=0`.
- The full six-direction block collection as a Schur-form identity at the analytic level.
- Strict positive definiteness of the eliminable `2 x 2` `L` block on the full product domain.
- The exact face-coupling terms showing why naive two-point iteration is insufficient.
- The Lambda-zero parameterization and fixed-direction derivative identity as a correctly specified handoff target.
- The auxiliary-resolvent and coefficientwise-PSD obstructions, with their stated non-counterexample scope.
- README assertions about conditional marginal Hessian subtraction, `D_s` PSD rank two, harmful acceleration, reproduction boundary, and issue #52 not being a completed result.

Not accepted here:

- The original half-filled theorem, already reviewed separately.
- Any private Drive packet or author verifier as independent evidence.
- The full arbitrary-diagonal missing-edge inequality (29).
- The stronger conditional Schur target (30).
- Positivity of the Lambda-zero matrix `M`.
- Any C2 issue #52 result or heavy exact-elimination claim.
- General Schur/global `M` sign beyond the stated identities.
- General real three-point concavity or a strict positive DPP entropy Jensen counterexample.
- Novelty or publication priority.

## Final verdict

**ACCEPTED_SCOPED.** The PR51 continuation files correctly add a proved positive eliminable block, a complete six-direction Schur/Fisher/acceleration bookkeeping identity, exact face-coupling obstruction terms, a well-scoped Lambda-zero derivative handoff, and two rigorous method-obstruction examples. They do not overclaim the open four-dimensional Schur complement, the global `M` sign, or the C2 issue #52 computation.
