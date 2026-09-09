# Correlated 3+3 signed-multiring fixture

**Status: INCOMPLETE.**  The exact setup and finite evaluations are valid, but
no interval-family sign theorem and no counterexample is claimed.

## Frozen affine line

Let

\[
A={1\over25}\begin{pmatrix}9&7&7\\7&9&7\\7&7&9\end{pmatrix},
\qquad
C={1\over25}\begin{pmatrix}16&7&7\\7&16&-7\\7&-7&16\end{pmatrix},
\]

and

\[
B=\begin{pmatrix}
1/24&-7/600&1/30\\
-7/300&-11/300&4/75\\
1/600&17/600&-7/150
\end{pmatrix}.
\]

Define the genuine `K`-affine line

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix},
\qquad
D=K'(t)=\begin{pmatrix}0&B\\B^{\mathsf T}&0\end{pmatrix}.      \tag{1}
\]

The spectra of `A` and `C` are respectively

\[
(2/25,2/25,23/25),\qquad(2/25,23/25,23/25),
\]

so each internal triangle is strongly correlated and close to two different
spectral faces.  The products of the three internal off-diagonal signs are
opposite.  The coupling is dense and has rank two.

The unique left and right null directions are proportional to

\[
(1,2,3)^{\mathsf T},\qquad(-1,5,3)^{\mathsf T}.
\]

Exact `2x2` minors of `[n,An]` and `[n,Cn]` show that neither is an eigenvector
of its internal block.  Hence the accepted PR43 special correlated `3+3`
null-eigenvector structure does not apply.

## Exact legality and endpoint geometry

Writing `B=UV^T`, positive definiteness is checked through the two `3x3`
Schur complements

\[
C-t^2B^{\mathsf T}A^{-1}B,
\qquad
I-C-t^2B^{\mathsf T}(I-A)^{-1}B.                 \tag{2}
\]

The executable check proves by exact rational Sylvester minors that both
`K(t)` and `I-K(t)` are positive definite for `|t|<=21/10`.
The first positive legal endpoint is a simple `I-K` Schur root `tau` with

\[
{2149\over1000}<\tau<{43\over20}.                 \tag{3}
\]

The `K`-side Schur complement remains positive definite at `t=43/20`, so this
is indeed the first loss of strict legality.  The exact discriminant is

\[
{9646065\over286557184}>0,
\]

and the endpoint-bracketing Schur determinants are

\[
{13081664272059\over105800000000000000000}>0,
\qquad
-{76510341\over16928000000000}<0.                 \tag{4}
\]

Thus this line has a real compact middle separated from both the decoupling
point and the simple endpoint neighborhoods already treated abstractly in
PR54.

## All complete events and the full Hessian

Use

\[
\begin{aligned}
u_1&=(1,1,-1)^T,&u_2&=(1,-2,1)^T,\\
v_1&=(1,-1,2)^T,&w&=(13/6,5/6,-2/3)^T,\\
U&=[u_1,u_2]/50,&V&=[v_1,w/2],
\end{aligned}
\]

so that `B=UV^T`.  For every complete left/right event `(S,T)`, set

\[
X_S=A-E_{S^c},\quad Y_T=C-E_{T^c},
\]

and define `G_A,G_C` as in `prior_art.md`.  The exact Schur determinant gives

\[
p_t(S,T)=p_A(S)p_C(T)
\{1+t^2u_{S,T}+t^4v_{S,T}\},                     \tag{5}
\]

with

\[
u_{S,T}=-\operatorname{tr}(G_A(S)G_C(T)),
\qquad
v_{S,T}=\det G_A(S)\det G_C(T).                  \tag{6}
\]

The script independently cross-checks all 64 values at `t=1` against the full
signed `6x6` event determinant, constructs all rational triples
`(p,p',p'')`, and checks

\[
\sum p=1,\qquad\sum p'=\sum p''=0,
\]

and evaluates the complete formula

\[
H''(t)=-\sum_{S,T}{p_t'(S,T)^2\over p_t(S,T)}
       -\sum_{S,T}p_t''(S,T)\log p_t(S,T).        \tag{7}
\]

No event or Fisher term is omitted.

## Motivated finite probes

The logarithms below were evaluated with `mpmath` at 110 decimal digits.
They are diagnostics, not outward-rounded interval certificates.
The symmetric local gap uses the true affine endpoints
`K(t-1/100)` and `K(t+1/100)`.

| `t` | `H''(t)` | local Jensen gap |
|---:|---:|---:|
| 1/10 | -3.766636057606856e-4 | -1.886378741891064e-8 |
| 1/2 | -8.491533416641444e-3 | -4.245938752073047e-7 |
| 1 | -2.804876332360292e-2 | -1.402450881035699e-6 |
| 3/2 | -5.645638510362832e-2 | -2.822855338824257e-6 |
| 19/10 | -9.676827842005823e-2 | -4.838603621651560e-6 |
| 21/10 | -1.453203466092864e-1 | -7.269231005346147e-6 |

At all frozen points the cardinality-three contribution is positive while the
complete curvature is negative.  For example, at `t=1/10`, the cardinality
three layer contributes approximately `+0.097818`, while the total is only
approximately `-0.000376664`.  This reproduces the relevant compensation
mechanism in a structure outside the fixed five-point frame: no individual
cardinality-layer sign can settle the line.

## What this does and does not establish

The exact rational parts establish the input, rank, full-event polynomial,
normalization identities, legality through `21/10`, and the simple endpoint
bracket.  The decimal signs establish only high-precision finite diagnostics.
They do not prove `H''<0` between sample points and do not exclude another
choice of `A,C,B`.

GitHub issue #61 freezes the heavy task: interval-certify (7) on the compact
middle and connect it to the simple-endpoint theorem, or return a positive
interval box.  That computation is deliberately not hidden behind a claim of
completion.
