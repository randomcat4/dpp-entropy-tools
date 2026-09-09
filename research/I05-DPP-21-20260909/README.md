# I05 DPP 21 — fixed scalar entropy rate beyond the PR39 Wiener neighbourhood

Issue: #48. Draft PR: #53. Branch: `research/I05-DPP-21-20260909`.

## Status

**New scoped theorem: PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED.**

**Original arbitrary-symbol / whole-legal-interval target: INCOMPLETE.**

No true entropy-rate counterexample is claimed. The accepted main results are used only within their frozen scope: PR29/34 cover lines through a constant symbol; PR39 covers the half-period-even/odd orbit only in its explicit small Wiener interval. Open-PR author claims are not treated as theorems.

## New result beyond PR39

Let `c,g` be real trigonometric polynomials with

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g != 0,
delta <= c <= 1-delta
```

for some `delta>0`. The center may be nonconstant, may have mean different from `1/2`, and need not satisfy `2||c-1/2||_W<1`.

Put `mu=integral c`. For any odd `k` with `g_hat(k)!=0`, set

```text
gamma=|g_hat(k)|^2,
alpha_k=gamma^2/[8 mu^2(1-mu^2)].
```

Then there is `epsilon(c,g,k)>0` such that

```text
t -> h(c+t g)+alpha_k t^4
```

is concave on `[-epsilon,epsilon]`. Hence `h(c+t g)` is strictly concave there.

The proof first obtains configuration-uniform exponential decay for every complete-event conditional inverse, including arbitrarily rare configurations. This yields a Hölder, Banach-holomorphic one-sided `g`-function and an analytic true entropy rate through the Ruelle transfer operator. Separately, a vertex-disjoint matching plus DPP negative association gives the true rate inequality

```text
h(c)-h(c+t g)
 >= (1/2) d(mu^2-|g_hat(k)|^2 t^2 || mu^2).
```

The normalized `g`-function shows that the term linear in `s=t^2` vanishes. The displayed rate inequality then forces a strictly positive fourth-order coefficient and gives the stated local curvature. No derivative of `H_n/n` is passed through the limit.

A fully explicit Rudin-Shapiro center in the proof has mean `1/2` but

```text
2||c-1/2||_W=15/8>1,
```

so PR39 does not apply. With `g(theta)=cos(2 pi theta)/64`, the new theorem gives an unspecified positive interval on which

```text
h(c+t g)+t^4/(3*2^27)
```

is concave. The exact Fourier constants are checked with integer/rational arithmetic; no entropy computation is used.

## Route comparison

The selected route is prediction/variational plus transfer operators. It retains the exact Schur-complement conditional kernel and all Fisher/acceleration content, but uses quasilocality to obtain a rate formula rather than trying to sign each finite conditional acceleration.

The cluster route is reorganized in a weighted inverse algebra. It supplies convergence outside a small Wiener row-sum disk, but individual cluster coefficients are not assigned an unsupported sign.

The independent operator route is the balanced fermionic beam-splitter reduction in `proof.md`. Existing quantum entropy-power theorems control von-Neumann entropy, not occupation-configuration Shannon entropy, so that route remains open and is not used in the new theorem.

## Files

- `finite_range_local_theorem.md`: exact statement, complete proof, explicit non-Wiener-small center, route comparison, and remaining scope.
- `proof.md`: earlier bridge ledger, complete-event determinant likelihood, inverse-decay lemma, cluster baseline, and beam-splitter obstruction.
- `sources.md`: primary sources and the precise role of each.
- `code/check_rudin_shapiro_example.py`: dependency-free exact check of the explicit example constants.
- `output/rudin_shapiro_exact.json`: recorded exact output; it is not an entropy-rate certificate.
- `code/probe_balanced_beamsplitter.py` and its output: bounded floating diagnostic only, explicitly non-proof.

## Remaining gap

Finite Fourier range plus strict legality now gives a genuine structure domain beyond PR39, but only near `t=0`. Analyticity on a compact legal subinterval does not determine the sign away from zero. The whole legal interval for the PR39 example `[-384,384]`, the full half-period class, and arbitrary fixed measurable symbol chords remain unresolved.