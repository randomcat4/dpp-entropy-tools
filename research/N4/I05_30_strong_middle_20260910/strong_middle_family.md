# A strong Schur-mismatched rank-two endpoint family: positive acceleration throughout the middle, but uniform full-chord concavity

Status: **PROVED by author, PENDING_INDEPENDENT_REVIEW**. This theorem covers a two-parameter set: every endpoint strength in a nontrivial interval and every point of its true affine chord. It is not an entropy counterexample or a general moving-rank-two theorem. Novelty is not assessed.

## 1. Family and quantifiers

Use the rational rotation

\[
R(q)=\frac1{1+q^2}
\begin{pmatrix}1-q^2&-2q\\2q&1-q^2\end{pmatrix}.
\]

Fix

\[
A=R(1/13)\operatorname{diag}(3/100,9/10)R(1/13)^T,
\]

and, for

\[
\lambda\in[4/5,9/10],
\]

put

\[
B_\lambda=R(3/7)\operatorname{diag}(3/20,\lambda)R(3/7)^T. \tag{1}
\]

Let `E=(e_1,e_2)` and retain the fixed physical frame

\[
V=\begin{pmatrix}
420/481&-612/5513\\
144/481&1785/5513\\
175/481&-1680/5513\\
60/481&4900/5513
\end{pmatrix}, \tag{2}
\]

which is obtained from principal-angle parameters `t_1=1/5`, `t_2=7/10` and rational top/bottom rotations `R(1/6)`. Define

\[
K_-=EAE^T,\qquad K_+(\lambda)=VB_\lambda V^T, \tag{3}
\]
\[
K_\lambda(t)=(1-t)K_-+tK_+(\lambda),\qquad0\le t\le1. \tag{4}
\]

The theorem is

\[
\boxed{
H''(K_\lambda(t))<-\frac12
\quad\text{for every }\lambda\in[4/5,9/10],\ 0<t<1.} \tag{5}
\]

Consequently every member has the true midpoint bound

\[
\boxed{
H(K_\lambda(1/2))-rac{H(K_-)+H(K_+(\lambda))}{2}>\frac1{16}.} \tag{6}
\]

All entropies in (5)--(6) are those of the full sixteen-event DPP law.

## 2. This remains a strong, full-rank-direction family

For every allowed `lambda`, the endpoint spectra are

\[
(3/100,9/10),\qquad(3/20,\lambda), \tag{7}
\]

so both kernels are rank two positive contractions with substantial anisotropy. The support planes `range(E)` and `range(V)` are fixed and disjoint. Thus `[E,V]` is invertible, and

\[
D_\lambda:=K_+(\lambda)-K_-
=[E,V]\operatorname{diag}(-A,B_\lambda)[E,V]^T. \tag{8}
\]

Every direction has rank four and inertia `(2,2)`. This is not a three-coordinate or rank-two direction.

The logical Schur complements are

\[
\sigma_A=\frac{4335}{8084},
\qquad
\sigma_B(\lambda)=\frac{841\lambda}{20(147\lambda+20)}. \tag{9}
\]

Their mismatch decreases across the interval but stays large:

\[
\sigma_A-\sigma_B(4/5)=\frac{47173}{161680},
\]
\[
\sigma_A-\sigma_B(9/10)=\frac{4428519}{15389915}. \tag{10}
\]

Both numbers exceed `0.287`. Hence the family is separated from the matched-Schur surface studied earlier.

## 3. Affine dependence of all complete atoms on the endpoint strength

Let `w` be the second column of `R(3/7)`. Then

\[
B_\lambda=B_0+\lambda ww^T. \tag{11}
\]

For every complete configuration `S`, the signed event matrix on the true chord has the form

\[
M_S(t,\lambda)=M_S(t,0)+t\lambda(Vw)(Vw)^T. \tag{12}
\]

The determinant is affine in `lambda`, because a determinant containing two columns from the same rank-one update vanishes. Therefore

\[
p_S(t,\lambda)=p_S(t,0)+\lambda[p_S(t,1)-p_S(t,0)] \tag{13}
\]

exactly. The checker reconstructs `p_S(t,0)` and `p_S(t,1)` independently from

\[
p_S=(-1)^{4-|S|}\det(K_\lambda(t)-E_{S^c}) \tag{14}
\]

and verifies (13) at `lambda=17/20`. No event polynomial is obtained by interpolation without this rank-one determinant identity.

## 4. Endpoint factors and the complete acceleration

Write

\[
\mathcal F(t,\lambda)=\sum_S\frac{(\partial_t p_S)^2}{p_S},
\qquad
\mathcal A(t,\lambda)=-\sum_S\partial_t^2p_S\log p_S. \tag{15}
\]

Then

\[
H''=\mathcal A-\mathcal F. \tag{16}
\]

On the left half, every complete event has the exact factor

\[
p_S(t,\lambda)=t^{b(S)}q^-_S(t,\lambda),
\qquad b(S)=|S\cap\{3,4\}|. \tag{17}
\]

As in the fixed member, the complete coefficient of `log t` vanishes:

\[
\sum_Sb(S)\partial_t^2p_S
=\frac{d^2}{dt^2}\mathbb E[X_3+X_4]=0. \tag{18}
\]

Thus

\[
\mathcal A=-\sum_S\partial_t^2p_S\log q^-_S
\qquad(0<t\le1/2). \tag{19}
\]

On the right, with `h=1-t` and `r(S)=max(|S|-2,0)`, exact rank-two endpoint factorization gives

\[
p_S(t,\lambda)=h^{r(S)}q^+_S(h,\lambda). \tag{20}
\]

The associated singular coefficient is

\[
R''_\lambda(t),\qquad
R_\lambda(t)=\sum_Sr(S)p_S(t,\lambda). \tag{21}
\]

The two-dimensional rational certificate proves

\[
R''_\lambda(t)<0
\quad(1/2\le t\le1,\ 4/5\le\lambda\le9/10). \tag{22}
\]

Since `log(1-t)<=0`, the term

\[
-R''_\lambda(t)\log(1-t) \tag{23}
\]

is nonpositive and can be discarded only when forming an upper bound on `mathcal A`. No rare event itself is discarded.

## 5. Exact tensor-product Bernstein cover

Each regular factor `q^\pm_S` and each `partial_t^2p_S` is a rational polynomial in the half-chord variable and is affine in `lambda`. The parameter domain is divided into

- 32 rational chord boxes on each half: `[i/64,(i+1)/64]`;
- 16 rational strength boxes across `[4/5,9/10]`.

There are 512 exact rectangles per half.

On a rectangle `[a,b]x[u,v]`, substitute

\[
x=a+(b-a)X,\qquad\lambda=u+(v-u)L,\qquad X,L\in[0,1]. \tag{24}
\]

For a polynomial

\[
P(X,L)=\sum_{i,j}c_{ij}X^iL^j,
\]

its tensor-product Bernstein coefficients are

\[
b_{k\ell}=\sum_{i\le k,j\le\ell}
 c_{ij}\frac{\binom{k}{i}}{\binom{n}{i}}
       \frac{\binom{\ell}{j}}{\binom{m}{j}}. \tag{25}
\]

Because Bernstein basis functions are nonnegative and sum to one, `P` lies between the smallest and largest `b_{k\ell}`. Every coefficient in (25) is rational. This is used for the factors, second derivatives and `R''`, rather than a floating-point enclosure.

Across all 1024 rectangles the certificate proves

\[
q^-_S,q^+_S\ge\frac{3969}{37519690}>0. \tag{26}
\]

It then encloses every logarithm outward. The resulting complete acceleration bounds are

\[
\mathcal A(t,\lambda)\le
0.324493392860807532273834389384667508
\quad(0<t\le1/2), \tag{27}
\]

and

\[
\mathcal A(t,\lambda)\le
2.389230399161136150122324317884720714
<\frac{239}{100}
\quad(1/2\le t<1). \tag{28}
\]

The right-end singular-sign cover has the strictly negative upper bound

\[
R''_\lambda(t)\le
-\frac{16473743916151986}{156050994644436125}<0. \tag{29}
\]

Thus (28) includes a rigorous sign treatment of every endpoint-zero event.

## 6. Uniform complete-Fisher lower bound

The derivative of the actual second-coordinate occupancy is

\[
(D_\lambda)_{22}=
\frac{3(11012018430000\lambda-221198959538374231)}
{780254973222180625}. \tag{30}
\]

It is negative and increasing throughout the interval, so its smallest absolute value occurs at `lambda=9/10`:

\[
(D_{9/10})_{22}
=-\frac{663567146165361693}{780254973222180625}. \tag{31}
\]

The score inequality for this physical Bernoulli bit gives

\[
\mathcal F(t,\lambda)
\ge4(D_\lambda)_{22}^2
\ge
\frac{1761285429880169957563283382047304996}
{608797823237945804170360480125390625}
>\frac{289}{100}. \tag{32}
\]

Combining (28) and (32) proves

\[
H''(t,\lambda)<\frac{239}{100}-\frac{289}{100}
=-\frac12, \tag{33}
\]

which is (5). Integration of the midpoint Green kernel, whose mass is `1/8`, proves (6).

## 7. Positive acceleration persists throughout the endpoint family

The same exact rational cover, now restricted to `t=1/2`, gives

\[
\boxed{
0.019387765277301260016920697418348759
<\mathcal A(1/2,\lambda)
<0.166254091468359865786981264262285661} \tag{34}
\]

for every `lambda in [4/5,9/10]`.

Thus the harmful sign is not confined to the original `lambda=17/20` example. A full interval of strongly correlated, Schur-mismatched, disjoint-support rank-two endpoint pairs has strictly positive affine acceleration at its full-rank midpoint, yet the complete Fisher term controls the whole chord uniformly.

This is the main structural conclusion of this unit. The natural family is safe, but not because each entropy-acceleration contribution is favorable.

## 8. Rational logarithm bounds and reproduction

For rational `x>0`, write `x=2^ky`, `1<=y<2`, and `z=(y-1)/(y+1)`, so `0<=z<=1/3`. The checker uses 192-bit directed fixed-point arithmetic to enclose

\[
\log x=k\log2+2\sum_{j=0}^{63}\frac{z^{2j+1}}{2j+1}+R, \tag{35}
\]

with

\[
0\le R\le\frac{9}{4(129)3^{129}}. \tag{36}
\]

Every multiplication, division and tail addition is rounded in the appropriate direction. Polynomial and Bernstein arithmetic is exact over rational numbers.

Run

```sh
python certify_strong_family.py
```

The generated `strong_family_certificate.json` contains the exact family, Schur mismatch endpoints, factor lower bound, acceleration and Fisher margins, rowwise cover summaries, midpoint acceleration interval and runtime. The bounded author run is recorded in `strong_family_stdout.txt`.

## 9. Remaining freedom

The proof uses a large visible one-coordinate derivative, approximately `-0.85`, to control the full Fisher information. It does not cover strong directions arranged so that every diagonal entry of `K_+-K_-` is small or zero. Such low-visible-Fisher directions can still have rank four, large off-diagonal motion and positive acceleration. They are the remaining mechanism-driven candidate class after this family exclusion.
