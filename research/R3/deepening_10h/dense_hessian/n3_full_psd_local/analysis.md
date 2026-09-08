# D10-S5 analysis and certificate

Status: **CORRECT_AFTER_FRESH_REVIEW_AND_REVISION_RECHECK** for the full
Hessian certificate; the finite PSD optimization remains `SCOUT`.

## 1. Exact-event Hessian construction

For any strict real DPP marginal kernel \(K\), exact atoms are obtained from
inclusion determinants by Möbius inversion:

\[
p_S(K)=\sum_{A\supseteq S}(-1)^{|A|-|S|}\det K[A,A].
\]

For a symmetric direction \(D\), set \(K(t)=K_*+tD\).  Each atom is a cubic
polynomial in \(t\):

\[
p_S(t)=p_S+p'_S t+\frac12p''_S t^2+O(t^3).
\]

The exact-event entropy Hessian is

\[
H''_{K_*}[D,D]
=
-\sum_S\frac{(p'_S)^2}{p_S}
-\sum_Sp''_S\log p_S.
\tag{1}
\]

The script constructs the polynomial \(p_S(t)\) directly from the Möbius
formula for each basis direction and pair of basis directions in

\[
(D_{11},D_{22},D_{33},D_{12},D_{13},D_{23}).
\]

Polarization yields the \(6\times6\) symmetric matrix \(A\) such that

\[
H''_{K_*}[D,D]=x(D)^\top A x(D).
\]

At \(K_*\), all base atoms are positive; the minimum exact atom is

\[
87/1250.
\]

## 2. Rational log intervals

The only irrational quantities in (1) are logarithms of rational base atoms.
For each rational \(u>0\), the script gives a rigorous interval for
\(\log u\).  It scales \(u\) into \([1,2)\), then uses

\[
\log y
=
2\sum_{k=0}^{N-1}\frac{z^{2k+1}}{2k+1}
+
R_N,
\qquad
z=\frac{y-1}{y+1},
\]

with the tail bound

\[
0\le R_N\le
\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

For this run \(N=35\).  Interval arithmetic then encloses every entry of the
Hessian matrix \(A\).

## 3. Gershgorin certificate

Let \(B=-A\).  From the interval matrix for \(A\), the script computes for each
row \(i\):

\[
\underline B_{ii}
-
\sum_{j\ne i}\overline{|B_{ij}|}.
\]

Every row margin is strictly positive.  The Decimal approximations are:

| row | margin for \(-A\) |
| ---: | ---: |
| 0 | 4.1067291327 |
| 1 | 4.0951564816 |
| 2 | 4.0760425600 |
| 3 | 1.9390872395 |
| 4 | 1.8005313724 |
| 5 | 1.7200075505 |

The exact rational margin certificates are stored in `hessian_scout.json`.
Gershgorin therefore proves \(B\succ0\), hence \(A\prec0\).  This is a
certificate over all real symmetric directions, so it strictly contains the
PSD/NSD cone.

In coordinate norm,

\[
-H''_{K_*}[D,D]\ge m\|x(D)\|_2^2,
\qquad m>0.
\]

Since

\[
\|D\|_F^2
=D_{11}^2+D_{22}^2+D_{33}^2
+2(D_{12}^2+D_{13}^2+D_{23}^2)
\le2\|x(D)\|_2^2,
\]

one also gets

\[
H''_{K_*}[D,D]\le-\frac m2\|D\|_F^2.
\]

This gives the requested local exclusion for arbitrary PSD/NSD directions.

## 4. PSD-cone attack log

Although the certificate already proves full negativity, I kept an explicit
positive-direction attack:

- random seed: `20260908`;
- rank-one random samples: `4000`;
- projected PSD starts: `400`;
- projected steps per start: `300`;
- normalization: Frobenius norm;
- rationalized best denominator cap: `2000`.

The best PSD value found was

\[
H''\approx -2.2850980382,
\]

at numerical rank one.  After rationalization with denominator at most 2000,
the certified exact-event value per Frobenius norm squared is approximately

\[
-2.2851089481.
\]

The rationalized direction has positive principal-minor PSD margins, including
positive determinant margin recorded in the JSON.  This is only an attack log;
the proof is the interval negative-definiteness certificate.

The M7 commuting direction \(D_*\) from equation (19) has

\[
H''_{K_*}[D_*,D_*]
\approx -2.2643612182.
\]

Thus the noncommuting search did not find a less negative certified direction
than the best rank-one scout, and it found no positive direction.

## 5. Local neighborhood consequence

The Hessian entries are smooth functions of \(K\) on the strict DPP kernel
domain because every exact atom is positive there.  Since \(A(K_*)\prec0\) with
a positive certified margin, continuity gives an open neighborhood \(U\) of
\(K_*\) such that

\[
H''_K[D,D]<0
\]

for every \(K\in U\) and every nonzero real symmetric \(D\).  This is an
existential local neighborhood statement; no computable radius is claimed.

It is stronger than the fixed-\(Q\) one-sign spectral statement at this single
base point, but it does not settle global concavity away from this local
neighborhood.
