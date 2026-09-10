# Operator contraction versus absolute localized sums: reverse audit

Status: **AUTHOR REVERSE AUDIT / PENDING INDEPENDENT REVIEW.**

This note has priority over any ambiguous wording in the first PR117 checkpoint. It does not change the theorem statement. It records exactly where operator norm, localization, Wiener absolute summation, and the fixed center tail enter.

## 1. The trace-log itself uses only operator norm

Fix a finite-range half-period-even reference `c^0` and a complete word `x`. Write

\[
M_x^0=T(c^0)-I_{Z_x},\qquad R_x^0=(M_x^0)^{-1},\qquad E_t=T(c-c^0+t g).
\]

Complete-event coercivity gives, uniformly in volume and word,

\[
\|R_x^0\|_{2\to2}\le \delta_0^{-1}.
\tag{A.1}
\]

Hence if

\[
\kappa:=\delta_0^{-1}\sup_{|t|\le\tau}\|c-c^0+t g\|_W<1,
\tag{A.2}
\]

then

\[
\|R_x^0E_t\|_{2\to2}\le\kappa<1.
\]

Therefore

\[
\log\det(I+R_x^0E_t)
=\sum_{m\ge1}\frac{(-1)^{m+1}}m\operatorname{Tr}(R_x^0E_t)^m
\tag{A.3}
\]

converges in operator norm. This step does **not** justify taking absolute values after expanding the spatial indices. No such inference is made below.

## 2. Absolute summability after localization is a second estimate

For a localization radius `R`, let `R_x^{[R]}` be the configuration-local approximation from `arbitrary_A0_C4_proof.md`. The proof uses

\[
\|R_x^0-R_x^{[R]}\|_{2\to2}\le C e^{-aR},
\qquad
\|R_x^{[R]}\|_{2\to2}\le B,
\tag{A.4}
\]

where one may take

\[
B=\delta_0^{-1}+1.
\tag{A.5}
\]

Crucially, `B` is an **operator-norm** bound. It is not a row-sum, Schur, Wiener, or common diagonal-envelope norm of the inverse family.

Expand only the Toeplitz perturbations,

\[
E_t=\sum_d e_t(d)S_d,
\qquad \sum_d|e_t(d)|\le\eta.
\tag{A.6}
\]

For a fixed displacement tuple `d=(d_1,...,d_m)`, define

\[
F^{[R]}_{m,d,\Lambda}(x)
=|\Lambda|^{-1}\operatorname{Tr}
(R_x^{[R]}S_{d_1})\cdots(R_x^{[R]}S_{d_m}).
\]

Then simply from `|Tr A|/|Lambda|<=||A||` and `||S_d||<=1`,

\[
\|F^{[R]}_{m,d,\Lambda}\|_\infty\le B^m.
\tag{A.7}
\]

Telescoping one inverse factor at a time gives

\[
\|F^{[R]}_{m,d,\Lambda}-F^{[R-1]}_{m,d,\Lambda}\|_\infty
\le C m B^{m-1}e^{-aR}.
\tag{A.8}
\]

No spatial entrywise absolute sum of an inverse appears in (A.7)-(A.8).

## 3. Complete-law derivatives add only polynomial support cost

For every bounded complete-event observable supported on a finite coordinate set `J`, differentiation of the full atom law gives

\[
|\partial_t^q E_tF|\le A_q|J|^q\|F\|_\infty,
\qquad 0\le q\le4.
\tag{A.9}
\]

The authoritative safe support count is the correction

\[
|J|\le C m^2(R+1).
\tag{A.10}
\]

Combining (A.8)-(A.10),

\[
|\partial_t^qE_t\Delta_RF_{m,d,\Lambda}|
\le C_q m^{2q+1}(R+1)^q B^{m-1}e^{-aR}.
\tag{A.11}
\]

Thus configuration localization pays an exponentially summable shell factor and a polynomial in `m,R`; it does not introduce a Fourier displacement weight.

## 4. Absolute displacement sums and the geometric constant

If `ell` of the `q` derivatives hit the affine Toeplitz coefficients, then after absolute summation over all displacement tuples,

\[
\sum_{d_1,\ldots,d_m}
\prod_{j\in M}|\widehat g(d_j)|
\prod_{j\notin M}|e_t(d_j)|
\le \|g\|_W^{\ell}\eta^{m-\ell}.
\tag{A.12}
\]

After summing localization shells, the corrected coarse bound is

\[
\sup_{\Lambda,|t|\le\tau}
\left|\partial_t^q |\Lambda|^{-1}E_t\operatorname{Tr}(R_x^0E_t)^m\right|
\le C_q m^{3q+1}B^{m-1}\eta^{m-q}(1+\|g\|_W)^q.
\tag{A.13}
\]

Hence the absolute length sum is geometric provided

\[
B\eta<\rho<1.
\tag{A.14}
\]

Equation (A.14) is stronger than the bare operator trace-log condition (A.2), but `B` is still only the common operator bound (A.5). There is no hidden common `ell^1` inverse envelope.

## 5. Quantifier order: the center tail is made small before `t` is shrunk

The center tail is fixed once `c^0` is fixed. Shrinking `t` cannot reduce it. The correct order is:

1. Start with the given strict `c in A_0` and margin `delta`.
2. Choose a sufficiently large finite Fourier truncation `c^0` so that
   \[
   \varepsilon_0:=\|c-c^0\|_W<\delta/2
   \]
   and, with `delta_0=delta-epsilon_0` and `B=delta_0^{-1}+1`,
   \[
   B\varepsilon_0<1/4.
   \tag{A.15}
   \]
   This is possible because `epsilon_0 ->0` while `B<=2/delta+1` is uniformly bounded as the truncation range increases.
3. Freeze this truncation. Only then choose `tau>0` so that
   \[
   B\tau\|g\|_W<1/4.
   \tag{A.16}
   \]
4. Therefore for `|t|<=tau`,
   \[
   B\eta\le B(\varepsilon_0+\tau\|g\|_W)<1/2.
   \tag{A.17}
   \]

Thus no argument uses an uncontrolled fixed center quantity `B*tail` and then tries to repair it by shrinking `t`.

## 6. Before and after differentiation: constant ledger

For fixed derivative order `q<=4`:

- trace-log existence: geometric constant `kappa<=delta_0^{-1} eta`;
- localized product sup norm: `B^m`, with `B<=delta_0^{-1}+1`;
- shell error: `C(c^0,delta_0) e^{-a(c^0,delta_0)R}`; these constants may deteriorate with truncation range but are summed in `R` only after the truncation is frozen;
- complete-law Bell differentiation: polynomial `|J|^q`, with constants depending on the true path margin and `||g||_W`;
- displacement absolute sum: only `eta` and `||g||_W`;
- walk-length absolute sum: polynomial in `m` times `(B eta)^m`.

The localization decay constants `C,a` are not required to be uniform over a sequence of truncation ranges. The proof selects one finite truncation and freezes it. This is why arbitrarily slow `A_0` tails are allowed.

## 7. Scope

This audit supports the PR117 `A_0` theorem only. It gives no passage from density of `A_0` to a larger symbol class, no whole-legal-interval result, and no HMM representation. It retains the complete Shannon law and therefore the whole Fisher-plus-acceleration curvature identity.