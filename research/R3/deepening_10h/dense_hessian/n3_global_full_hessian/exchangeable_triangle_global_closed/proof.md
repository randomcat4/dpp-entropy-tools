# Global closure of the exchangeable-triangle determinant

## Status and dependencies

`PROVED`; two independent reconstructions returned `CORRECT` as recorded in
[verifications/fresh_audit.md](verifications/fresh_audit.md).
The finite standard-library identity replay is recorded in
[run_log.md](run_log.md); it is supplementary and is not used as the proof.

This unit imports only the already reviewed facts from U10f/U10h:

1. the exact event atoms and the `S3` Hessian splitting;
2. strict positivity of the four-dimensional standard block when
   \(\alpha\ne\beta\);
3. the two-dimensional Fisher/missing-information formula for the invariant
   block.

Everything after the odds substitution below is proved here.

## 1. Exact entropy and invariant Hessian

Put

\[
U=\alpha+2\beta-3\alpha\beta,\qquad
V=2\alpha+\beta-3\alpha\beta.
\]

The per-subset event atoms, with multiplicities \((1,3,3,1)\), are

\[
p_0=(1-\alpha)(1-\beta)^2,
\quad p_1=\frac{(1-\beta)U}{3},
\quad p_2=\frac{\beta V}{3},
\quad p_3=\alpha\beta^2.                                      \tag{1}
\]

Equivalently, the count law is that of

\[
N_0=X+Z,\qquad
X\sim\operatorname{Ber}(\alpha),\quad
Z\sim\operatorname{Bin}(2,\beta),
\]

and the observed subset is uniform conditional on its count.  Hence

\[
H_{\rm evt}=H(N_0)+\log 3\,
 (\alpha+2\beta-\beta^2-2\alpha\beta).                       \tag{2}
\]

Let \(C=-\nabla^2_{\alpha,\beta}H_{\rm evt}\).  The reviewed U10h
missing-information calculation gives

\[
F=\begin{pmatrix}u&0\\0&2v\end{pmatrix}
 -\kappa\binom{u}{-v}(u,-v),                                 \tag{3}
\]

where

\[
u=\frac1{\alpha(1-\alpha)},\qquad
v=\frac1{\beta(1-\beta)},
\]

\[
\kappa=2\alpha(1-\alpha)\beta(1-\beta)
 \left(\frac{1-\beta}{U}+\frac{\beta}{V}\right).           \tag{4}
\]

With

\[
\ell=\log\frac{3(1-\alpha)\beta V}{U^2},\qquad
\Lambda=\log\frac{\alpha(1-\beta)U^3}
 {(1-\alpha)\beta V^3},                                    \tag{5}
\]

the invariant block is

\[
C_{\alpha\alpha}=F_{\alpha\alpha},\quad
C_{\alpha\beta}=F_{\alpha\beta}+2(\ell+\beta\Lambda),
\quad
C_{\beta\beta}=F_{\beta\beta}+2(\ell+\alpha\Lambda).      \tag{6}
\]

The coordinate map \((x,a)\mapsto(\alpha,\beta)\) has determinant
\(-3\).  Consequently

\[
\det(-\nabla^2_{x,a}H_{\rm evt})=9\det C=9\Delta_T.          \tag{7}
\]

## 2. Odds ratio and the quartic numerator

Use the positive odds scale \(q\) and odds ratio \(t\):

\[
q=\frac{\beta}{1-\beta}>0,\qquad
t=\frac{\alpha/(1-\alpha)}{\beta/(1-\beta)}>0.              \tag{8}
\]

Thus

\[
\alpha=\frac{tq}{1+tq},\qquad
\beta=\frac q{1+q},\qquad
t=1\iff\alpha=\beta.                                       \tag{9}
\]

The two logarithms in (5) now depend only on \(t\):

\[
\ell=\log\frac{3(2t+1)}{(t+2)^2},\qquad
\Lambda=\log\frac{t(t+2)^3}{(2t+1)^3}.                     \tag{10}
\]

Define the nonnegative logarithmic deficits

\[
e=-\ell
=\log\left(1+\frac{(t-1)^2}{3(2t+1)}\right),             \tag{11}
\]

\[
d=-(\ell+\Lambda)
=\log\left(1+\frac{(t-1)^2}{3t(t+2)}\right),               \tag{12}
\]

and \(Q=(2t+1)(t+2)\).  Direct substitution of (8)--(12) into
(3)--(6), followed by clearing the positive denominator

\[
D=q\,t(1+q)^2(t+2)(2t+1)>0,                                 \tag{13}
\]

gives the exact quartic

\[
D\Delta_T=\sum_{k=0}^4 c_k(t)q^k.                           \tag{14}
\]

Four coefficients are

\[
c_0=2t\{2(t-1)^2+3e(2t+1)\},                               \tag{15}
\]

\[
c_4=2t\{2(t-1)^2+3dt(t+2)\},                               \tag{16}
\]

\[
\frac{c_3}{2}
=2(t^2-1)^2+dtQ(3-2d)+et(4t^2+7t-2),                       \tag{17}
\]

\[
\frac{c_2}{2}
=4(t-1)^2(t^2+t+1)-dP_d+e\{-P_e-4dtQ\},                    \tag{18}
\]

where

\[
P_d=2t^4-7t^3-10t^2-12t,
\qquad
P_e=-12t^3-10t^2-7t+2.                                    \tag{19}
\]

Complementation sends \((\alpha,\beta)\) to
\((1-\alpha,1-\beta)\), hence \((t,q)\) to \((t^{-1},q^{-1})\).
It preserves \(\Delta_T\), interchanges \(d\) and \(e\), and yields

\[
c_k(t;d,e)=t^4c_{4-k}(t^{-1};e,d).                          \tag{20}
\]

Equation (20) defines \(c_1\) from (17) and also makes \(c_2\)
self-reciprocal.

## 3. Positivity of all five coefficients

Equations (11)--(12) show \(d,e\ge0\), with simultaneous equality only
at \(t=1\).  Thus (15)--(16) give

\[
c_0>0,\qquad c_4>0\qquad(t\ne1).                            \tag{21}
\]

### The coefficient \(c_3\)

If \(t\ge1/4\), then

\[
d\le\log(4/3)<1/3,
\qquad 4t^2+7t-2=(4t-1)(t+2)\ge0.                           \tag{22}
\]

Every term on the right of (17) is therefore nonnegative, and the first
term is strict when \(t\ne1\).

It remains to handle \(0<t<1/4\), where \(d\) is unbounded and (22)
must not be used.  Put

\[
z=\frac{(1-t)^2}{3t(t+2)},\qquad d=\log(1+z).
\]

The elementary bound \(\log(1+z)\le\sqrt z\) and
\(z\le1/(6t)\) give

\[
d^2\le\frac1{6t},\qquad
dtQ(3-2d)\ge-2tQd^2\ge-\frac Q3\ge-\frac98.                \tag{23}
\]

On the same interval, \(e<\log(4/3)<1/3\),
\(t(4t^2+7t-2)>-2t\), and
\(2(t^2-1)^2>225/128\).  Hence

\[
\frac{c_3}{2}
>\frac{225}{128}-\frac98-\frac16
=\frac{179}{384}>0.                                        \tag{24}
\]

Thus \(c_3>0\) for every \(t\ne1\), and (20) gives \(c_1>0\).

### The coefficient \(c_2\)

By (20), it is enough to take \(t>1\).  Then
\(d<\log(4/3)<1/3\), and the coefficient of \(e\) in (18) satisfies

\[
-P_e-4dtQ
>\frac{28t^3+10t^2+13t-6}{3}>0.                            \tag{25}
\]

If \(P_d\le0\), every term in (18) is nonnegative and the base term is
strict.  If \(P_d>0\), then

\[
4(t-1)^2(t^2+t+1)-dP_d
>4(t-1)^2(t^2+t+1)-\frac{P_d}{3}
\]

\[
=\frac{10t^4-5t^3+10t^2+12}{3}>0.                          \tag{26}
\]

Therefore \(c_2>0\) for \(t>1\), and (20) covers \(0<t<1\).

Combining (13)--(26), for \(t\ne1\) and \(q>0\),

\[
\Delta_T=\frac{\sum_{k=0}^4c_k(t)q^k}{D}>0.                \tag{27}
\]

Moreover, the exact expression

\[
C_{\alpha\alpha}=
\frac{(1+tq)^2\{q^2(t+2)+6qt+t(2t+1)\}}
{qt(1+q)^2(t+2)(2t+1)}>0                                   \tag{28}
\]

shows that \(C\) is positive definite.  The reviewed U10f standard block
is also strictly positive.  Hence the full six-dimensional form
\(-\operatorname{Hess}H\) is positive definite at every connected strict
exchangeable triangle.

## 4. The diagonal is a genuine quartic ridge

At \(\alpha=\beta=x\), equivalently \(a=0\), one obtains exactly

\[
C=\frac1{3x(1-x)}
\begin{pmatrix}1&2\\2&4\end{pmatrix},
\qquad \ker C=\operatorname{span}(2,-1).                    \tag{29}
\]

This is a real second-order null direction, not floating-point noise.
Along the fixed-\(x\) exchangeable puncture,

\[
H(x,a)=3h(x)-\frac{3a^4}{2x^2(1-x)^2}+O(a^5),              \tag{30}
\]

so

\[
\partial_a^4H(x,0)=-\frac{36}{x^2(1-x)^2}<0.               \tag{31}
\]

The determinant opens quadratically away from the ridge:

\[
\frac{\Delta_T}{(\alpha-\beta)^2}
\longrightarrow\frac{2}{3x^3(1-x)^3}>0.                   \tag{32}
\]

Thus the zero set is a positive-dimensional disconnected ridge, while
every connected puncture in the exchangeable family is strictly negative
in all `Sym(3)` entropy-curvature directions.
