# From the reviewed three-coordinate rank-two theorem to explicit rank-three/rank-four regions

Status: the matched-axis implication is a **specialization of the reviewed analytic PR88 theorem**, with a new quantitative Fisher bound. The rank-three slab, zero-intersection wedge and two rectangles are **PROVED by the present author, PENDING_REVIEW**. The unrestricted moving-rank-two problem remains **INCOMPLETE**.

All entropies are natural-log Shannon entropies of the complete event law. Every midpoint is the true arithmetic midpoint of physical kernels.

## 1. Common actual coordinate and matched Schur complements

Let

\[
A=\begin{pmatrix}a&r\\r&d\end{pmatrix},\qquad
B=\begin{pmatrix}b&z\\z&e\end{pmatrix},
\qquad 0<A,B<I_2.
\]

For `0<s<=1`, `c^2+s^2=1`, define rank-two kernels on three actual coordinates

\[
K_-=
\begin{pmatrix}a&r&0\\r&d&0\\0&0&0\end{pmatrix},
\qquad
K_+=
\begin{pmatrix}
bc^2&zc&bcs\\zc&e&zs\\bcs&zs&bs^2
\end{pmatrix}.
\]

Their ranges intersect in `span(e_2)`. Put

\[
\sigma_A=d-r^2/a,\qquad \sigma_B=e-z^2/b.
\]

A direct determinant calculation in the observation basis gives

\[
\det(K_+-K_-)=ab s^2(\sigma_A-\sigma_B). \tag{1}
\]

When `sigma_A=sigma_B`, the nonzero direction is singular. It cannot have rank one: a real symmetric rank-one matrix is semidefinite, whereas either order `K_-<=K_+` or `K_+<=K_-` would force the equal-dimensional endpoint kernels to have the same nullspace and hence the same range, contradicting `s>0`. Thus the direction is indefinite rank two.

PR88's reviewed analytic theorem for an indefinite rank-two difference supported on three actual coordinates applies to the true chord

\[
K(\tau)=(1-\tau)K_-+\tau K_+.
\]

It retains all complete events and gives

\[
H''(\tau)\le-\sum_S\frac{p'_\tau(S)^2}{p_\tau(S)}. \tag{2}
\]

Use the actual-coordinate statistic `X_3`. Since

\[
\frac{d}{d\tau}\mathbb E_\tau X_3=bs^2,
\]

Cauchy--Schwarz for the full score yields

\[
\sum_S\frac{p'_\tau(S)^2}{p_\tau(S)}
\ge\frac{b^2s^4}{\operatorname{Var}_\tau(X_3)}
\ge4b^2s^4. \tag{3}
\]

The midpoint Green weight is `min(tau,1-tau)/2` and integrates to `1/8`, so

\[
\boxed{
G(0):=H(K(1/2))-\frac{H(K_-)+H(K_+)}2
\ge\frac{b^2s^4}{2}>0.} \tag{4}
\]

Equation (4) is quantitative but remains inside the reviewed PR88 structural class; it is not counted as a new general matched-Schur theorem.

## 2. Exact diagonal transfer and a rank-three slab

Replace `e` in `B` by `e+q`, keeping the support geometry fixed. For any legal diagonal perturbation

\[
K(\delta)=K+\delta e_i e_i^T,
\]

and each configuration `T` of the remaining coordinates, differentiating the signed event determinant gives the exact complete-law pairing

\[
p_{K(\delta)}(T\cup\{i\})=p_K(T\cup\{i\})+\delta p_{K_{\hat i}}(T),
\]
\[
p_{K(\delta)}(T)=p_K(T)-\delta p_{K_{\hat i}}(T). \tag{5}
\]

Hence total variation is exactly `|delta|`; no event is omitted. At the endpoint the perturbation has TV `|q|`, while at the midpoint it has TV `|q|/2`. With

\[
\omega_d(x)=h(x)+x\log(d-1),
\]

we therefore have

\[
G(q)\ge G(0)-\omega_8(|q|/2)-\frac12\omega_8(|q|). \tag{6}
\]

The direction determinant becomes

\[
\det(K_+(q)-K_-)=-ab s^2q. \tag{7}
\]

Thus every nonzero admissible `q` gives a genuine rank-three direction while both endpoints remain rank two with a one-dimensional support intersection.

For the exact family

\[
A=\begin{pmatrix}2/5&1/5\\1/5&2/5\end{pmatrix},\qquad
B=\begin{pmatrix}3/5&1/5\\1/5&11/30\end{pmatrix}, \tag{8}
\]

and the rational angle `c=3/5`, `s=4/5`, the Schur complements are both `3/10`. Direct complete-law rational logarithm bounds give

\[
G(0)\in[
0.237412353391516407213231567603,
0.237412353391516407213231567604]. \tag{9}
\]

Substitution in (6) proves legality and

\[
\boxed{G(q)>3/100\qquad (|q|\le3/100).} \tag{10}
\]

The certified lower endpoint before simplification is

\[
0.033781455418877285235432212648\ldots .
\]

## 3. Rotating the common coordinate: full-event wedge bound

Keep (8) and the first moving vector

\[
v_1=ce_1+se_3.
\]

Rotate the second vector to

\[
v_2=c_2e_2+s_2e_4,\qquad w=s_2^2,
\]

and put `K_+(w)=V(w)BV(w)^T`, `M(w)=(K_-+K_+(w))/2`. At `w=0` the endpoint supports intersect in one dimension; for `w>0` they are disjoint and `rank M=4`.

Let `D_B=be-z^2` and

\[
C_*={1\over2}\left(2e+D_B+ae+2|rz|c+aD_Bs^2\right). \tag{11}
\]

We claim

\[
\|p_{M(w)}-p_{M(0)}\|_{\rm TV}\le C_*w. \tag{12}
\]

Delete coordinate four from a sample of `M(w)`. The deletion changes the configuration with probability at most `M(w)_{44}=ew/2`. Between the resulting three-coordinate marginal and `M(0)`, the only changed inclusion minors are

\[
\Delta d_2=-ew/2,
\]
\[
\Delta d_{12}=
\frac{-(D_Bc^2+ae)w+2rzc(1-c_2)}4,
\]
\[
\Delta d_{23}=-D_Bs^2w/4,\qquad
\Delta d_{123}=-aD_Bs^2w/8. \tag{13}
\]

Since `1-c_2<=w`, the absolute value of the second expression is at most `(D_Bc^2+ae+2|rz|c)w/4`. For any two complete laws on three points, Möbius inversion gives

\[
\|p-p'\|_{\rm TV}
\le{1\over2}\sum_{\varnothing\ne T\subseteq[3]}
2^{|T|}|d_T-d'_T|. \tag{14}
\]

Using (13), `c^2+s^2=1`, and adding the deletion cost proves (12). Thus all eight marginal events and every event containing coordinate four are included in a deterministic finite bound.

The plus endpoint is the logical `B` process followed by marking its second occupied logical point into coordinates two and four, so exactly

\[
H(K_+(w))-H(K_+(0))=e h(w). \tag{15}
\]

Combining (12), the sixteen-symbol entropy modulus and (15) yields

\[
\boxed{
G(w)\ge G(0)-[h(C_*w)+C_*w\log15]-{e\over2}h(w).} \tag{16}
\]

For (8), `c=3/5`, `s=4/5`,

\[
D_B=9/50,\qquad C_*=7213/12500. \tag{17}
\]

Parametrize `c_2=(1-t_2^2)/(1+t_2^2)`, `s_2=2t_2/(1+t_2^2)`. On `0<=t_2<=1/10`,

\[
w\le400/10201,\qquad C_*w\le28852/1275125.
\]

A 64-term rational `atanh` logarithm enclosure in (16), starting from (9), gives

\[
\boxed{G(t_2)>3/100\qquad(0\le t_2\le1/10).} \tag{18}
\]

The unsimplified certified lower endpoint is

\[
0.037715568105819433236405885383\ldots .
\]

This wedge fixes the first angle at `t_1=1/2`, well outside the old PR86 small-angle square.

## 4. Two rank-three/rank-four rectangles

Now replace `B_{22}=11/30` by `11/30+q`. The endpoint law changes by TV at most `|q|`. For the midpoint,

\[
M(q,t_2)=M(0,t_2)+{q\over2}v_2v_2^T.
\]

For each nonempty coordinate set `T`, rank-one determinant multilinearity gives

\[
|\det M(q,t_2)_T-\det M(0,t_2)_T|
={|q|\over2}v_{2,T}^T\operatorname{adj}(M(0,t_2)_T)v_{2,T}.
\]

Every principal block is a positive contraction; its adjugate is positive semidefinite with operator norm at most one. Hence the last expression is at most `|q| ||v_{2,T}||^2/2`. Applying the four-coordinate version of (14) gives

\[
\|p_{M(q,t_2)}-p_{M(0,t_2)}\|_{\rm TV}
\le{27\over2}|q|, \tag{19}
\]

because `sum_{T containing i}2^{|T|}=54` and `||v_2||=1`.

Consequently

\[
G(q,t_2)\ge L(t_2)-
\omega_{16}(27|q|/2)-{1\over2}\omega_{16}(|q|), \tag{20}
\]

where `L(t_2)` is the certified wedge lower bound from (16). Exact rational-log evaluation proves

\[
\boxed{
|q|\le1/5000,\quad0\le t_2\le1/10
\quad\Longrightarrow\quad G>1/100,} \tag{21}
\]

with lower endpoint `0.010515807043070212155665620928...`, and

\[
\boxed{
|q|\le1/1000,\quad0\le t_2\le1/20
\quad\Longrightarrow\quad G>3/50,} \tag{22}
\]

with lower endpoint `0.062893393815551820896302241655...`.

At `t_2=0,q!=0`, (7) gives rank three. At `t_2>0`, the concatenated endpoint frame is invertible and the direction is congruent to `diag(-A,B(q))`; its inertia is `(2,2)` and its rank is four. These are true affine directions, not derivatives of the angle-parameter curve.

## 5. Fixed checks and limitations

Direct complete-law evaluations, used only as consistency checks, give

```text
t2=0:    G in [0.237412353391516407213231567,
                0.237412353391516407213231568]
t2=1/20: G in [0.239534406051189238077581067,
                0.239534406051189238077581068]
t2=1/10: G in [0.245807839942224732803206456,
                0.245807839942224732803206457]
```

The continuous conclusions are (10), (18), (21) and (22), not interpolation between these samples.

The result does not cover general one-dimensional-intersection rank-three directions, arbitrary zero-intersection rank-four directions, large second angles, simultaneous boundary-scale changes, or the strong-correlated middle sought in the continuation. It supplies no entropy counterexample and no novelty claim.

Run `python audit_axis_wedge.py`. The script reconstructs every law by both signed determinants and Möbius inversion and uses a 64-term rational `atanh` series with the explicit tail

\[
0\le R_N\le{2z^{2N+1}\over(2N+1)(1-z^2)},\qquad0\le z\le1/3.
\]
