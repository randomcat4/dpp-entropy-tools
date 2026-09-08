# D10-U2 diagonal_flat_ridge fresh non-author review

STATUS: CORRECT

Layered verdict:

- Fixed diagonal global maximum: CORRECT.
- Zero-diagonal exact-event jet through fourth order: CORRECT.
- Compact-box fourth-order constant and small-\(t\) consequence: CORRECT.
- Local author-text repair needed: `proof.md:234-239` misses additive plus signs in the displayed Taylor expansion.  This is a local LaTeX/formula-joining error, not a constant or proof-chain error after the intended expansion is restored.

I did not modify author files.  I added only:

- `verifications/fresh_u2_audit.py`
- `verifications/fresh_u2_audit.json`
- `verifications/fresh_audit.md`

No server was used.  No `C:\canglan\` path was accessed.

## Author statement checked

The frozen claim states, for \(X=\operatorname{diag}(x_1,\ldots,x_n)\), \(0<x_i<1\):

- fixed-diagonal entropy maximum and strict equality iff \(K=X\): `frozen_claim.md:24-29`;
- zero-diagonal direction setup and \(p'_S(0)=0\): `frozen_claim.md:40-52`;
- exact-event second atom jet \(q_S/p_S(0)=-2\sum_{i<j}D_{ij}^2\zeta_i(S)\zeta_j(S)\): `frozen_claim.md:64-82`;
- fourth derivative formulas and strict negativity: `frozen_claim.md:88-96`;
- compact-box bound \(H^{(4)}(0)\le -6\|D\|_F^4/[n(n-1)M^2]\): `frozen_claim.md:101-111`;
- existential uniform small-\(t\) descent and the explicit coefficient after shrinking \(\rho\): `frozen_claim.md:117-130`;
- explicit scope limit: radial fourth-order theorem only, not full-neighborhood Hessian negativity: `frozen_claim.md:137-140`.

The proof sections carrying those claims are `proof.md:19-73`, `proof.md:84-103`, `proof.md:115-187`, `proof.md:199-281`, `proof.md:288-330`, and `proof.md:332-422`.

## Command run

From repo root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\diagonal_flat_ridge\verifications\fresh_u2_audit.py'
```

Exit code: `0`.

Denominators checked:

- global fixed-diagonal exact atom semantics: independent \(n=2,3,4\) strict rational kernels, with \(4,8,16\) atoms respectively;
- zero-diagonal jet: independent \(n=2,3,4\) rational cases, with \(4,8,16\) atom-polynomials respectively;
- all arithmetic in the jet layer is `Fraction`; entropy spot comparisons in the global layer use Decimal logs only after exact atoms are built.

The script does not import author `flat_ridge_sanity.py`.

## Layer 1: fixed diagonal global maximum

Status: CORRECT.

The proof uses ordinary finite Shannon subadditivity on the exact subset indicator vector \(Y\).  Since DPP inclusion probabilities give

\[
\mathbb P(i\in Y)=K_{ii}=x_i,
\]

subadditivity yields

\[
H(Y)\le \sum_i h(x_i).
\]

Equality in finite Shannon subadditivity is equality in the multi-information

\[
D(P_Y\|\prod_i P_{Y_i}),
\]

so it requires mutual independence of the coordinate indicators.  For a real symmetric DPP,

\[
\mathbb P(i,j\in Y)
=\det\begin{pmatrix}x_i&K_{ij}\\K_{ij}&x_j\end{pmatrix}
=x_ix_j-K_{ij}^2.
\]

Thus independence forces every \(K_{ij}=0\) for \(i\ne j\), hence \(K=X\).  Conversely \(K=X\) gives independent Bernoulli coordinates.  This proves the strict equality condition on the stated strict fixed-diagonal fiber.

Boundary audit:

- The theorem assumes \(0<x_i<1\) and strict kernels \(0\prec K\prec I\); boundary atoms and zero/one Bernoulli marginals are not claimed.
- The equality argument is fiberwise only: it fixes all \(K_{ii}=x_i\).
- Pair inclusion is used as inclusion probability, not as an exact atom; exact atom entropy is still the entropy of the full subset law obtained by Möbius inversion.

Independent checks:

- \(n=2,3,4\) strict rational non-diagonal kernels had exact atoms summing to \(1\), exact singleton marginals equal to the diagonal \(x_i\), and pair inclusion
  \[
  \sum_{S\supseteq\{i,j\}}p_S=x_ix_j-K_{ij}^2.
  \]
- In all three examples, a nonzero off-diagonal produced a nonzero pair-product gap and Decimal entropy satisfied \(H(X)>H(K)\).

## Layer 2: zero-diagonal exact-event jet

Status: CORRECT.

For \(K(t)=X+tD\) with \(\operatorname{diag}D=0\), the determinant derivative of every principal inclusion minor at \(t=0\) has trace term

\[
\det X[A,A]\operatorname{tr}(X[A,A]^{-1}D[A,A])=0.
\]

Möbius inversion therefore gives \(p'_S(0)=0\) for every exact atom.  The independent script rebuilt all exact atom polynomials from inclusion determinants and verified this exactly.

For \(q_S=p_S''(0)\), the checked formula is

\[
\frac{q_S}{p_S(0)}
=-2\sum_{i<j}D_{ij}^2\zeta_i(S)\zeta_j(S),
\qquad
\zeta_i(S)=
\begin{cases}
1/x_i,&i\in S,\\
-1/(1-x_i),&i\notin S.
\end{cases}
\]

The constant `-2` is correct.  The direct pair inclusion check also gives

\[
\sum_{S\supseteq\{i,j\}}q_S=-2D_{ij}^2,
\]

matching `proof.md:180-187` and `hazards.md:37-40`.

Entropy derivative audit:

- \(\log p_S(0)\) is a constant plus singleton indicators.
- For orders \(1,2,3,4\), exact atom derivatives satisfy both total-mass cancellation
  \[
  \sum_S p_S^{(m)}(0)=0
  \]
  and singleton-marginal cancellation
  \[
  \sum_{S\ni i}p_S^{(m)}(0)=0.
  \]
- Since \(p'_S(0)=0\), the nonlinear entropy terms do not contribute to \(H''(0)\) or \(H'''(0)\).

Therefore

\[
H'(0)=H''(0)=H'''(0)=0.
\]

The fourth derivative is

\[
H^{(4)}(0)=-3\sum_S \frac{q_S^2}{p_S(0)}.
\]

Under the product base law, the \(\zeta_i\) are independent and centered.  The independent script explicitly checked that distinct edge characters are orthogonal, including shared-endpoint and disjoint-edge cases.  Hence all cross-edge terms vanish, and only identical edges survive:

\[
H^{(4)}(0)
=-12\sum_{i<j}
\frac{D_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
\]

The constant `-12` is correct.  Any nonzero zero-diagonal symmetric \(D\) has at least one nonzero off-diagonal entry, so \(H^{(4)}(0)<0\).

Independent Fraction cases:

| case | n | atoms | result |
|---|---:|---:|---|
| `n2_fraction_edge` | 2 | 4 | PASS |
| `n3_fraction_mixed_signs` | 3 | 8 | PASS |
| `n4_fraction_all_edges` | 4 | 16 | PASS |

## Local text repair: Taylor display

`proof.md:234-239` currently displays

\[
h(a_S+\Delta)
=
h(a_S)
(-\log a_S-1)\Delta
-\frac{\Delta^2}{2a_S}
O(\Delta^3).
\]

As rendered, this is missing additive plus signs and can be read as multiplication by \(h(a_S)\).  It should be

\[
h(a_S+\Delta)
=h(a_S)+(-\log a_S-1)\Delta-\frac{\Delta^2}{2a_S}+O(\Delta^3).
\]

The subsequent lines `proof.md:243-281` use the intended additive expansion: the linear logarithmic terms cancel, and the surviving \(t^4\) contribution is \(-q_S^2/(8a_S)\) before multiplying by \(4!\).  My independent Fraction check reproduces the downstream constants \(-3\) and \(-12\).  I classify this as LOCAL_REPAIR_REQUIRED, not as an incorrect theorem or incorrect constant.

## Layer 3: compact-box fourth-order bound

Status: CORRECT.

For \(x_i\in[a,b]\subset(0,1)\) and

\[
M=\max_{u\in[a,b]}u(1-u),
\]

we have \(x_i(1-x_i)\le M\).  Therefore

\[
H^{(4)}(0)
\le -\frac{12}{M^2}\sum_{i<j}D_{ij}^4.
\]

Since \(\operatorname{diag}D=0\),

\[
\sum_{i<j}D_{ij}^2=\frac{\|D\|_F^2}{2},
\qquad
N=\frac{n(n-1)}2.
\]

Cauchy's inequality gives

\[
\sum_{i<j}D_{ij}^4
\ge
\frac{\|D\|_F^4}{2n(n-1)}.
\]

Thus the author constant is correct:

\[
H^{(4)}(0)
\le
-\frac{6\|D\|_F^4}{n(n-1)M^2}.
\]

For \(\|D\|_F=1\), this is a uniform negative fourth derivative at \(t=0\) over the compact diagonal box and zero-diagonal unit directions.

What it can imply:

- By compactness and continuity of the fourth derivative on a strict feasible tube, it gives an existential \(\rho>0\) such that, after shrinking \(\rho\),
  \[
  H(X+tD)\le H(X)-\frac{t^4}{8n(n-1)M^2}
  \]
  for all \(x\in[a,b]^n\), zero-diagonal \(\|D\|_F=1\), and \(0<|t|\le\rho\).
- The coefficient \(1/[8n(n-1)M^2]\) follows from \(C_4/48\) with \(C_4=6/[n(n-1)M^2]\).
- Strict feasibility for small \(t\) is uniform because \(\|D\|_{\mathrm{op}}\le\|D\|_F=1\), so \(|t|\le \frac12\min(a,1-b)\) keeps both \(K(t)\) and \(I-K(t)\) positive definite.

What it cannot imply:

- It does not give an explicit numerical \(\rho\) unless one also supplies a uniform modulus/bound for the fourth derivative away from zero.
- It does not prove Hessian negativity in any full neighborhood; the base Hessian is flat in zero-diagonal directions.
- It does not cover directions with nonzero diagonal after leaving the diagonal ridge.
- It does not turn fixed-diagonal radial descent into a theorem about arbitrary K-affine chords with changing diagonals.

The global fixed-diagonal theorem separately gives non-quantitative strict descent \(H(X+tD)<H(X)\) for every strict feasible \(t\ne0\) and nonzero zero-diagonal \(D\), because the whole line keeps the diagonal fixed and is non-diagonal.

## Independent audit JSON highlights

`fresh_u2_audit.json` reports:

- `status: PASS`;
- `fixed_diagonal_global_maximum_semantics: PASS`;
- `zero_diagonal_exact_event_jet: PASS`;
- `compact_box_fourth_order_constant: PASS`.

Exact Fraction highlights:

- `n2_fraction_edge`: \(H^{(4)}=-3969/31250\), uniform-bound margin \(H^{(4)}-\mathrm{rhs}=-1863/62500\).
- `n3_fraction_mixed_signs`: \(H^{(4)}=-1676041/7087500\), uniform-bound margin \(-76609321/574087500\).
- `n4_fraction_all_edges`: \(H^{(4)}=-12422497945225499/271001338675200000\), uniform-bound margin \(-429451253625779311/36585180721152000000\).

These cases are not a proof by themselves; they are independent exact sanity checks supporting the line-by-line mathematical audit above.

## Final conclusion

The D10-U2 frozen claim is mathematically correct in the stated scope.  The only issue found is the local Taylor-display typo in `proof.md:234-239`; once the missing plus signs are inserted, the proof chain, constants, equality condition, and compact-box small-\(t\) consequence are coherent.
