# Proof III — radial lifting, coordinate support, and rank-two exterior powers

## 1. From conditional line concavity to radial concavity

Retain the notation of Proof I:

\[
G(s)=H(A)+\sum_Sp_A(S)H(C-sM_S),\qquad s\in[0,\tau^2]. \tag{1}
\]

Assume each true affine conditional line `s -> H(C-sM_S)` is concave on the common legal interval. Their fixed positive weighted sum is concave, so `G` is concave.

Both complete block marginals of `K(t)` are fixed, equal to `p_A` and `p_C`. At `s=0` the joint law is their product. Hence

\[
G(0)-G(s)=H(p_A)+H(p_C)-H(P_s)=I_{P_s}(X_A;X_C)\ge0. \tag{2}
\]

Thus `G` attains its maximum at the left endpoint. A concave function on an interval that attains its maximum at the left endpoint is nonincreasing: for `0<=x<y`, concavity gives

\[
G(x)\ge(1-x/y)G(0)+(x/y)G(y)\ge G(y). \tag{3}
\]

Now put `F(t)=G(t^2)`. For arbitrary legal `t_1,t_2` and `0<=lambda<=1`, convexity of the square gives

\[
(\lambda t_1+(1-\lambda)t_2)^2
\le \lambda t_1^2+(1-\lambda)t_2^2. \tag{4}
\]

Since `G` is nonincreasing and concave,

\[
\begin{aligned}
F(\lambda t_1+(1-\lambda)t_2)
&=G((\lambda t_1+(1-\lambda)t_2)^2)\\
&\ge G(\lambda t_1^2+(1-\lambda)t_2^2)\\
&\ge\lambda G(t_1^2)+(1-\lambda)G(t_2^2).
\end{aligned} \tag{5}
\]

Therefore `t -> H(K(t))` is concave on the entire legal interval.

If `B!=0`, choose `i,j` with `B_{ij}!=0`. For every `s>0`, the cross-block DPP covariance is

\[
\operatorname{Cov}(1_{i\in X},1_{j\in X})=-sB_{ij}^2\ne0. \tag{6}
\]

Thus the two blocks are not independent and (2) is strict: `G(s)<G(0)` for all `s>0`. Concavity then makes `G` strictly decreasing on `(0,\tau^2]`. The square inequality in (4) is strict for distinct `t_1,t_2` and `0<lambda<1`; hence (5) is strict. This proves strict radial concavity for nonzero `B`.

## 2. The arbitrary-by-two theorem

When the right block has size at most two, every conditional kernel `C-sM_S` in (1) is a one- or two-dimensional real DPP kernel and each conditional line is concave by Proof II. Consequently (5) applies for arbitrary left-block size and arbitrary real `B in R^{m x 2}`. If `rank(B)=2`, the whole symmetric direction

\[
\begin{pmatrix}0&B\\B^T&0\end{pmatrix}
\]

has rank four. Neither internal block is required to be diagonal or to commute with the direction.

## 3. Arbitrary dimension with at most two observed coordinates in the direction

Let `L(z)=L_0+zD` be a strict real DPP line on a finite coordinate set, and assume `D` is supported on a coordinate principal block `J` with `|J|<=2`. Put `R=J^c`. For an exact outside configuration `T subseteq R`, write

\[
Y_T=(L_0)_{RR}-E_{R\setminus T}.
\]

The outside marginal is independent of `z`. Applying the complete-event Schur formula while conditioning on `T` gives a DPP on `J` with kernel

\[
L_{J\mid T}(z)
=(L_0)_{JJ}+zD_{JJ}-(L_0)_{JR}Y_T^{-1}(L_0)_{RJ}. \tag{7}
\]

This is an affine real line of dimension at most two. Shannon's chain rule therefore yields

\[
H(L(z))=H((L_0)_{RR})+
\sum_{T\subseteq R}p_{(L_0)_{RR}}(T)H(L_{J\mid T}(z)), \tag{8}
\]

and every summand is concave by Proof II. Hence `H(L(z))` is concave.

If, in the cross-block radial family, the matrix `B` has nonzero columns only in a coordinate set `J` of size at most two, then every `M_S=B^TX_S^{-1}B` is supported on `J`. Equation (8) proves each conditional line in (1) concave, even when the right block has arbitrary size and is arbitrarily correlated with the remaining coordinates. The row-supported version follows by exchanging the blocks.

## 4. Rank-two exterior-power likelihood

Assume `rank(B)=2` and choose a full-column factorization

\[
B=UV^T,\qquad U\in\mathbb R^{m\times2},\quad V\in\mathbb R^{\ell\times2}. \tag{9}
\]

For complete configurations `S,T`, define

\[
G_A(S)=U^TX_S^{-1}U,\qquad
G_C(T)=V^TY_T^{-1}V. \tag{10}
\]

Divide the complete-event block determinant by its value at `s=0` and use Sylvester's determinant identity:

\[
\begin{aligned}
\frac{P_s(S,T)}{P_0(S,T)}
&=\frac{\det(Y_T-sV G_A(S)V^T)}{\det Y_T}\\
&=\det(I_\ell-sY_T^{-1}V G_A(S)V^T)\\
&=\det(I_2-sG_A(S)G_C(T)).
\end{aligned} \tag{11}
\]

For two-by-two matrices,

\[
\det(I_2-sXY)=1-s\operatorname{tr}(XY)+s^2\det X\det Y. \tag{12}
\]

Therefore, in `P_s=P_0+sR+s^2Q`,

\[
\frac{R(S,T)}{P_0(S,T)}=-\operatorname{tr}(G_A(S)G_C(T)),
\qquad
\frac{Q(S,T)}{P_0(S,T)}=\det G_A(S)\det G_C(T). \tag{13}
\]

The determinant perturbation identity

\[
p_{A+UZU^T}(S)=p_A(S)\det(I_2+ZG_A(S)) \tag{14}
\]

holds for every symmetric `Z` near zero. Summing over `S` and comparing the constant, linear, and quadratic coefficients gives

\[
\mathbb E_{p_A}G_A=0,\qquad
\mathbb E_{p_A}\det G_A=0. \tag{15}
\]

The same identities hold for `G_C`. These are the exact exterior-degree cancellations behind the zero marginals of `R,Q`.

Equation (11) is useful but does not permit a non-coordinate orthogonal rotation of `range(V)`: complete-configuration entropy is tied to the original observation basis. The still-open general rank-two problem is precisely to control the fixed-basis entropy of the rank-two affine family `C-sVG_A(S)V^T` after the resolvent-realizable averaging over `S`.