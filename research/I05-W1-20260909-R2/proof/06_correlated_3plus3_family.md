# proof/06_correlated_3plus3_family.md

## 1. 一个可直接检验的三点条件判据

考虑

\[
K(t)=\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix},
\qquad C\in\operatorname{Sym}_3(\mathbb R),
\qquad \operatorname{rank}B\le2.
\]

对左块完整配置 `S` 定义

\[
M_S=B^T(A-E_{S^c})^{-1}B.
\]

若每个 `S` 至少满足下列一项：

1. `rank(M_S)<=1`；
2. `M_S` 为不定秩二矩阵；
3. 仿射直线 `{C-rM_S:r in R}` 含有一个严格对角核；

则 `t -> H(K(t))` 在整个合法区间凹，`B!=0` 时严格凹。

证明：秩至多一时，每个完整事件概率沿真实参数 `r` 仿射，熵凹；不定秩二时使用 `proof/04`；第三种情形使用导入的对角中心全直线定理。于是所有条件熵 `H(C-sM_S)` 关于 `s` 凹，再用精确条件链及径向提升原理。

## 2. 两侧相关、非坐标秩二的结构定理

令 `n in R^3` 为单位向量，并设

\[
\theta=\max_i n_i^2<\frac12,
\qquad P=I-nn^T.
\]

取

\[
0<\alpha<1,
\qquad \theta<\beta<1-\theta,
\qquad A=\alpha P+\beta nn^T. \tag{1}
\]

令 `B in R^{3 x 3}` 满足

\[
\operatorname{rank}B=2,
\qquad n^TB=0, \tag{2}
\]

并记 `M_0=B^TB`。再取一个严格对角 `3 x 3` 核 `D_0` 和实数 `eta`，使

\[
C=D_0+\eta M_0 \tag{3}
\]

仍为严格核。则

\[
\boxed{
t\longmapsto
H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\text{ 在整个合法区间上凹；若 }B\ne0\text{ 则严格凹。}
} \tag{4}
\]

当 `alpha!=beta` 且 `M_0` 有非零非对角元时，`A,C` 都是相关的非对角内部块。条件 (2) 允许 `B` 稠密，其左右奇异二维子空间都可不具有任何两坐标支撑。

### 证明

取任意 `3 x 2` 满列秩矩阵 `U`，列空间为 `n^perp`。由 (2)，存在满行秩 `R in R^{2 x 3}` 使

\[
B=UR.
\]

对左完整配置 `S` 写

\[
X_S=A-E_{S^c},
\qquad G_S=U^TX_S^{-1}U,
\qquad M_S=R^TG_SR. \tag{5}
\]

若 `S={1,2,3}`，则 `A` 在 `n^perp` 上等于 `alpha I`，所以

\[
M_S=\alpha^{-1}M_0. \tag{6}
\]

若 `S=emptyset`，则 `A-I` 在 `n^perp` 上等于 `-(1-alpha)I`，所以

\[
M_S=-(1-\alpha)^{-1}M_0. \tag{7}
\]

由 (3)，这两条条件核直线都是

\[
D_0+rM_0,
\]

因而都穿过严格对角核 `D_0`，满足三点条件判据的第 3 项。

现在设 `|S|=1` 或 `2`。事件矩阵 `X_S=A-E_{S^c}` 的惯性为

\[
(|S|,3-|S|), \tag{8}
\]

因为把 `S,S^c` 排序后，`A_{SS}` 正定，而相应 Schur 补严格负定。因此

\[
\operatorname{sign}\det X_S=(-1)^{3-|S|}. \tag{9}
\]

取正交矩阵 `[\widehat U,n]`，其中 `\widehat U` 是 `n^perp` 的正交基。Jacobi 互补主子式恒等式给出

\[
\det(\widehat U^TX_S^{-1}\widehat U)
=\frac{n^TX_Sn}{\det X_S}. \tag{10}
\]

一般基 `U` 只把左侧乘以正的平方因子，不改变符号。

若 `S={i}`，则

\[
n^TX_Sn=\beta-\sum_{j\ne i}n_j^2
=\beta-(1-n_i^2)<0, \tag{11}
\]

因为 `beta<1-theta<=1-n_i^2`；同时由 (9) `det X_S>0`。若 `S` 的补集为 `{k}`，则

\[
n^TX_Sn=\beta-n_k^2>0, \tag{12}
\]

而 `det X_S<0`。两种情形都由 (10) 得

\[
\det G_S<0. \tag{13}
\]

所以 `G_S` 是不定 `2 x 2` 矩阵。由于 `R` 满行秩，`M_S=R^TG_SR` 为不定秩二 `3 x 3` 矩阵，满足条件判据第 2 项。

全部八个左配置都已覆盖，因此每条 `s -> H(C-sM_S)` 凹。条件 Schur 链和径向提升完成 (4) 的证明。

## 3. 完全显式的稠密有理例

取

\[
n=\frac1{\sqrt3}(1,1,1)^T,
\quad \alpha=\frac25,
\quad \beta=\frac12,
\]

故

\[
A=\frac25 I+\frac1{30}J
=\begin{pmatrix}
13/30&1/30&1/30\\
1/30&13/30&1/30\\
1/30&1/30&13/30
\end{pmatrix}. \tag{14}
\]

令

\[
B=\begin{pmatrix}
1&2&3\\
4&5&6\\
-5&-7&-9
\end{pmatrix}. \tag{15}
\]

它秩为二、全部条目非零，列和为零，故 `n^TB=0`；右零向量为 `(1,-2,1)^T`。所以左右秩二奇异子空间的法向量都具有三个非零坐标，均不是坐标二维平面。

有

\[
M_0=B^TB=
\begin{pmatrix}
42&57&72\\
57&78&99\\
72&99&126
\end{pmatrix}, \tag{16}
\]

其特征值为

\[
0,\quad123-3\sqrt{1663},\quad123+3\sqrt{1663}. \tag{17}
\]

取

\[
D_0=\frac25I,
\qquad C=D_0+\frac1{1000}M_0. \tag{18}
\]

于是 `C` 稠密非对角，三个特征值为

\[
\frac25,\quad \frac25+\frac{123-3\sqrt{1663}}{1000},
\quad \frac25+\frac{123+3\sqrt{1663}}{1000},
\]

均严格位于 `(0,1)`。

设 `lambda_max=123+3sqrt(1663)`。Schur 补给出精确合法区间 `|t|<tau`，其中

\[
\tau^2=
\min\left\{
\frac4{25\lambda_{\max}}+\frac1{2500},
\frac9{25\lambda_{\max}}-\frac3{5000}
\right\}. \tag{19}
\]

第二项较小，故

\[
\boxed{
\tau^2=\frac{4091}{15000}-\frac{\sqrt{1663}}{150}>0,
\qquad \tau\approx0.0294508621.
} \tag{20}
\]

正性可由 `4091^2-10000*1663=106281>0` 直接验证。这个 `3+3` 族具有两个相关内部块、稠密真正秩二跨块方向以及非坐标左右奇异平面，严格超出“一侧大小至多二”和“两坐标支撑”定理。
