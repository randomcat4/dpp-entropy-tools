# An exact strongly correlated, Schur-mismatched moving-rank-two chord with positive middle acceleration but globally dominant Fisher information

Status: **PROVED by author, PENDING_INDEPENDENT_REVIEW**. This is a theorem for one exact full affine chord and every parameter on that chord. It is not a finite-point diagnostic, an entropy counterexample, or a universal moving-rank-two theorem. Novelty is not assessed.

Throughout,

\[
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T,
\qquad H(K)=-\sum_{S\subseteq[4]}p_K(S)\log p_K(S),
\]

with natural logarithms, empty determinant one and `0 log 0=0`. The target is the true physical-kernel line

\[
K(t)=(1-t)K_-+tK_+,\qquad 0\le t\le1. \tag{1}
\]

## 1. Exact input and geometry

For a rational parameter `q`, put

\[
R(q)=\frac1{1+q^2}
\begin{pmatrix}1-q^2&-2q\\2q&1-q^2\end{pmatrix}. \tag{2}
\]

This is a rational orthogonal matrix. Define the two strongly anisotropic logical kernels

\[
A=R(1/13)
\begin{pmatrix}3/100&0\\0&9/10\end{pmatrix}R(1/13)^T,
\]
\[
B=R(3/7)
\begin{pmatrix}3/20&0\\0&17/20\end{pmatrix}R(3/7)^T. \tag{3}
\]

In entries,

\[
A=\begin{pmatrix}
18189/361250&-23751/180625\\
-23751/180625&635547/722500
\end{pmatrix},
\]
\[
B=\begin{pmatrix}
8697/16820&-294/841\\
-294/841&8123/16820
\end{pmatrix}. \tag{4}
\]

Let `E=(e_1,e_2)`. Take principal-angle parameters

\[
t_1=1/5,\qquad t_2=7/10,
\]

so

\[
C=\operatorname{diag}(12/13,51/149),\qquad
S=\operatorname{diag}(5/13,140/149).
\]

Rotate both physical halves by `R(1/6)` and put

\[
V=\begin{pmatrix}R(1/6)C\\R(1/6)S\end{pmatrix}
=\begin{pmatrix}
420/481&-612/5513\\
144/481&1785/5513\\
175/481&-1680/5513\\
60/481&4900/5513
\end{pmatrix}. \tag{5}
\]

The endpoints are

\[
K_-=EAE^T,\qquad K_+=VBV^T. \tag{6}
\]

Both are legal real rank-two contractions. Their nonzero spectra are exactly

\[
(3/100,9/10),\qquad(3/20,17/20). \tag{7}
\]

The matrix `[E,V]` is invertible, so the endpoint ranges are disjoint and every `K(t)` with `0<t<1` is positive definite. Since both `I-K_-` and `I-K_+` are positive definite, `I-K(t)` is also positive definite. Hence all sixteen complete atoms are strictly positive in the open chord.

The full-rank direction `D=K_+-K_-` obeys

\[
D=[E,V]\begin{pmatrix}-A&0\\0&B\end{pmatrix}[E,V]^T. \tag{8}
\]

Thus its inertia is `(2,2)`, not the reviewed three-coordinate rank-two case. Exact arithmetic gives

\[
\det D=\frac{67473}{150078760}>0. \tag{9}
\]

The logical Schur complements relative to their first coordinates are

\[
\sigma_A=\frac{\det A}{A_{11}}=\frac{4335}{8084},
\qquad
\sigma_B=\frac{\det B}{B_{11}}=\frac{14297}{57980}, \tag{10}
\]

with substantial mismatch

\[
\sigma_A-\sigma_B=\frac{8485397}{29294395}\approx0.28965. \tag{11}
\]

This object is outside the matched-Schur surface, the small-angle square, the common-coordinate rank-two direction and the dilute regime.

## 2. Exact complete-event Hessian

For each `S subseteq [4]`, define the complete atom directly by the signed determinant

\[
p_S(t)=(-1)^{4-|S|}\det\bigl(K(t)-E_{S^c}\bigr). \tag{12}
\]

Each `p_S` is an exact rational polynomial of degree at most four. All sixteen polynomials are stored in `strong_middle_certificate.json` and regenerated from (2)--(6) by `certify_strong_chord.py`; none is fitted or supplied as an inclusion probability.

For `0<t<1`, differentiation of the complete entropy gives

\[
H''(t)=\mathcal A(t)-\mathcal F(t), \tag{13}
\]
\[
\mathcal F(t)=\sum_S\frac{p'_S(t)^2}{p_S(t)},
\qquad
\mathcal A(t)=-\sum_Sp''_S(t)\log p_S(t). \tag{14}
\]

The first term in (14) is the full classical Fisher information of the complete law. No event, layer or mixed direction is omitted.

## 3. A global complete-Fisher lower bound from one actual coordinate

For any statistic `f` of a complete configuration, the score identity and Cauchy--Schwarz give

\[
\mathcal F(t)\ge
\frac{\bigl(\frac d{dt}\mathbb E_t f\bigr)^2}
{\operatorname{Var}_t(f)}. \tag{15}
\]

Choose the actual occupancy bit `f=1_{\{2\in X\}}`. Its expectation is the physical diagonal entry `K_{22}(t)`, so its derivative is the constant

\[
D_{22}=-\frac{51043753689855861}{60019613324783125}. \tag{16}
\]

Because a Bernoulli variance is at most `1/4`, throughout the open chord

\[
\mathcal F(t)\ge4D_{22}^2
=\frac{10421859163002695299495099824205284}
{3602353983656484048345328284765625}
>\frac{57}{20}. \tag{17}
\]

This bound is on the complete Fisher sum in (14), not on a spectral or particle-count surrogate.

## 4. Left endpoint regularization: every bottom event retained

For `S subseteq[4]`, let

\[
b(S)=1_{\{3\in S\}}+1_{\{4\in S\}}.
\]

Exact symbolic factorization of the sixteen atom polynomials gives

\[
p_S(t)=t^{b(S)}q^-_S(t), \tag{18}
\]

where every `q^-_S` is strictly positive on `[0,1/2]`. The factors represent all events involving either or both moving bottom coordinates; no rare event is deleted.

Substituting (18) into the acceleration term yields

\[
\mathcal A(t)=
-\sum_Sp''_S(t)\log q^-_S(t)
-\log t\sum_S b(S)p''_S(t). \tag{19}
\]

The coefficient of `log t` vanishes exactly. Indeed,

\[
\sum_Sb(S)p_S(t)=\mathbb E_t[X_3+X_4]
=K_{33}(t)+K_{44}(t), \tag{20}
\]

and one-point inclusion probabilities are affine in `K(t)`, hence affine in `t`. Its second derivative is zero. Therefore

\[
\mathcal A(t)=-\sum_Sp''_S(t)\log q^-_S(t)
\qquad(0<t\le1/2). \tag{21}
\]

The checker partitions `[0,1/2]` into the 32 closed rational intervals

\[
[i/64,(i+1)/64],\qquad0\le i<32. \tag{22}
\]

On each interval it encloses every exact polynomial `q^-_S` and `p''_S` by sign-aware rational monomial bounds, proves the lower endpoint of every `q^-_S` positive, encloses its logarithm outward and multiplies intervals without assuming the signs of `p''_S`. The resulting exact upper bound is

\[
\mathcal A(t)\le
0.447590129231891892302103787346710469
<\frac{41}{20} \tag{23}
\]

on the whole left half.

## 5. Rank-two right endpoint: exact higher-cardinality factors

Put `h=1-t` and

\[
r(S)=\max(|S|-2,0).
\]

Because the endpoint `K_+` has rank two, events of size three and four vanish there. For this exact dense endpoint, symbolic factorization sharpens this to

\[
p_S(t)=h^{r(S)}q^+_S(h), \tag{24}
\]

where every `q^+_S` is strictly positive for `0\le h\le1/2`. Thus

\[
\mathcal A(t)=
-\sum_Sp''_S(t)\log q^+_S(h)-R''(t)\log h, \tag{25}
\]

with

\[
R(t)=\sum_Sr(S)p_S(t)
=-\frac{9t(t-1)}{293743048742468000}
\left(29347145944200t^2+2770180654685548t+443122727619975\right). \tag{26}
\]

A direct derivative is

\[
R''(t)=
-\frac{9}{146871524371234000}
\left(176082875665200t^2+8222500526224044t-2327057927065573\right). \tag{27}
\]

The quadratic in parentheses is positive at `t=1/2`, its derivative is positive there, and its second derivative is positive. Hence

\[
R''(t)<0\qquad(1/2\le t\le1). \tag{28}
\]

Since `log h<=0`, the omitted term in (25) satisfies

\[
-R''(t)\log h\le0. \tag{29}
\]

It is therefore safe for an upper bound to retain only the regular part. The same 32-box exact rational procedure, now in `h`, gives

\[
\mathcal A(t)\le
2.033807212767484134212899422441121840
<\frac{41}{20} \tag{30}
\]

throughout the right half. Equations (23) and (30) prove the global acceleration bound

\[
\mathcal A(t)<\frac{41}{20}\qquad(0<t<1). \tag{31}
\]

## 6. Whole-chord conclusion

Combining (17) and (31) in the full identity (13),

\[
\boxed{H''(t)<\frac{41}{20}-\frac{57}{20}=-\frac45
\qquad(0<t<1).} \tag{32}
\]

Thus this strongly correlated, disjoint-support, full-rank-direction rank-two endpoint chord is strictly entropy-concave on its entire legal interval. By integrating the midpoint Green kernel and using entropy continuity at the boundary endpoints,

\[
H(K(1/2))-\frac{H(K_-)+H(K_+)}2>\frac1{10}. \tag{33}
\]

A direct independent expression from all three complete event laws gives the stronger author-certified value

\[
G\in[
0.855287043211861975243460436575901058,
0.855287043211861975243460436575919773]. \tag{34}
\]

The theorem itself follows from (32); the decimal interval in (34) is an additional fixed-input check.

## 7. The dangerous mechanism really occurs

At the full-rank midpoint `t=1/2`, the acceleration is strictly positive:

\[
\mathcal A(1/2)\in[
0.091509816433464862273171837567186173,
0.091509816433464862273171837567255234]. \tag{35}
\]

The positivity is driven by the singleton layer, not by dropping high-cardinality configurations. The complete cardinality decomposition is:

| Cardinality | Fisher contribution | Acceleration contribution |
|---:|---:|---:|
| 0 | `0.000291110692398...` | `-1.717907186441357...` |
| 1 | `5.224280966639617...` | `+4.829269128292475...` |
| 2 | `0.395350042663457...` | `-2.458962918243294...` |
| 3 | `0.035501168361516...` | `-0.556177667888545...` |
| 4 | `0` | `-0.004711539285812...` |

The total complete Fisher is about `5.655423288356989`, and consequently

\[
H''(1/2)\in[
-5.563913471923524035878192808311324263,
-5.563913471923524035878192808311255202]. \tag{36}
\]

This establishes a concrete point where the affine acceleration term has the feared positive sign, but it does not overcome the full Fisher term. It is therefore a mechanism witness and a full-chord exclusion, not a method-only artifact.

## 8. Endpoint emerging masses and relation to reviewed boundary theory

The complete event factors also give the total linear emerging masses

\[
\beta_0=\frac{488210425}{970894132}>0,
\qquad
\beta_1=\frac{34701373072827}{349278298148000}>0. \tag{37}
\]

These agree with the reviewed fixed-affine-line boundary mechanism in PR88, but the proof above does not merely invoke an unspecified endpoint neighborhood: it explicitly covers both endpoint halves and the compact middle with no gap.

## 9. Exact logarithm and interval semantics

For every rational `x>0`, the checker writes `x=2^k y`, `1<=y<2`, and `z=(y-1)/(y+1)`, so `0<=z<=1/3`. It encloses

\[
\log x=k\log2+2\sum_{j=0}^{31}\frac{z^{2j+1}}{2j+1}+R,
\]
\[
0\le R\le\frac{2z^{65}}{65(1-z^2)}. \tag{38}
\]

`log 2` uses the same formula at `z=1/3`. All polynomial, interval, Fisher and comparison operations are exact rational arithmetic; displayed decimals are rounded outward. There is no numerical probability floor. Exact zeros occur only at the rank-two endpoints and are handled by (18) and (24).

Run

```sh
python certify_strong_chord.py
```

The generated `strong_middle_certificate.json` stores the exact input matrices, all sixteen event polynomials, complete midpoint layers, both endpoint factor orders, every interval box and all reported enclosures. `strong_middle_stdout.txt` records the bounded author run. Independent arithmetic review remains outstanding.

## Scope still open

This closes the entire true affine chord for one deliberately strong and substantially Schur-mismatched pair. It does not prove that every member of a neighborhood in endpoint-parameter space is safe, does not cover all moving rank-two endpoints, and does not rule out a more balanced direction where every one-coordinate derivative is small enough that the statistic lower bound (17) loses force. Such low-visible-Fisher strong directions are the remaining natural target.
