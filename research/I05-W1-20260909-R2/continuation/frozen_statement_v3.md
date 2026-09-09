# frozen_statement_v3.md

任务 ID：I05-W1-20260909-R2-continuation  
版本：v3.1，2026-09-09  
总体状态：**PARTIAL**  
本文件状态：**一致性审计后的最新冻结命题**

第二轮原有条件 Schur、`m x 2` 定理、两坐标支撑提升和 rank-two 外幂公式见上级 `frozen_statement.md`。除下述外部输入 D 外，本文件列出的命题均为 PR #43 的作者级证明；尚待新的非作者独立审阅。

## D. 外部输入：对角锚点直线凹性

采用用户指定、由另一独立团队证明的有限维定理：任意严格对角 Hermitian 收缩核 `D` 与固定 Hermitian 方向 `V` 给出的函数

\[
u\mapsto H(D+uV)
\]

在其整个合法参数区间上凹。本轮只使用该输入，不重新计作自己的证明或审阅。

## E. 实三点不定秩二方向定理

令 `K` 为严格实对称 `3 x 3` DPP 核，`D` 为实对称秩二矩阵，且两个非零特征值异号。则在所有满足

\[
0<K+zD<I
\]

的参数上，

\[
z\longmapsto H(K+zD)
\]

凹；结论连续延拓到合法边界。

该命题在原观测坐标中成立，不使用正交变基。若 `n` 是 `D` 的单位零向量、`adj(D)=\gamma nn^T`、`\gamma<0`，令 `\kappa=n^TKn`，则完整事件概率的二次系数 `c` 满足

\[
c=\sum_{i<j}\gamma n_k^2
\big[(1-\kappa)e^{ij\mid k=0}+\kappa e^{ij\mid k=1}\big],
\]

从而 `\langle c,\log p\rangle\ge0`，并与完整 Fisher 项共同给出曲率非正。半定秩二方向不在本命题中。

## F. rank-two 外幂充分统计与压缩 Hessian

设 `rank(B)=2`，取 `B=UV^T`，并定义

\[
G_A(S)=U^T(A-E_{S^c})^{-1}U,
\qquad
G_C(T)=V^T(C-E_{T^c})^{-1}V.
\]

则

\[
\frac{P_s(S,T)}{p_A(S)p_C(T)}
=\det(I_2-sG_A(S)G_C(T)).
\]

把两侧配置分别推前到 `G_A,G_C` 后，KL 与互信息精确保持。此为充分统计恒等式，不是 Fisher 投影。

固定严格 `C`、满列秩 `V` 和 `Z,H\in\operatorname{Sym}_2`，写

\[
G_T=V^T(C-E_{T^c})^{-1}V,
\quad \mu_T=p_C(T),
\]

\[
\ell_T(Z)=\det(I_2+ZG_T).
\]

在合法域内，

\[
D^2H(C+VZV^T)[H,H]
=-\sum_T\mu_T\frac{(\ell_T')^2}{\ell_T}
+2\det(H)\Lambda_{C,V}(Z),
\]

\[
\Lambda_{C,V}(Z)
=-\sum_T\mu_T\det(G_T)\log(\mu_T\ell_T(Z)).
\]

第一项是全部事件 Fisher。由定理 E，当 `C` 为三点核时，不定秩二方向所需的外幂加速度符号有利；一般高维的对应符号未冻结为定理。

## G. 三点条件方向判据

考虑

\[
K(t)=\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix},
\qquad C\in\operatorname{Sym}_3(\mathbb R),
\qquad \operatorname{rank}B\le2.
\]

对每个左块完整配置 `S` 令

\[
M_S=B^T(A-E_{S^c})^{-1}B.
\]

若每个 `S` 至少满足一项：

1. `rank(M_S)\le1`；
2. `M_S` 为不定秩二矩阵；
3. 仿射直线 `{C-rM_S:r\in\mathbb R}` 含有一个严格对角核；

则 `t\mapsto H(K(t))` 在整个合法区间上凹；若 `B\ne0`，则严格凹。

## H. 两侧相关、非坐标的 `3+3` rank-two 结构族

令 `n\in\mathbb R^3` 为单位向量，

\[
\theta=\max_i n_i^2<\frac12,
\qquad P=I-nn^T.
\]

取

\[
0<\alpha<1,
\qquad \theta<\beta<1-\theta,
\qquad A=\alpha P+\beta nn^T.
\]

令 `B\in\mathbb R^{3\times3}` 满足

\[
\operatorname{rank}B=2,
\qquad n^TB=0,
\]

并记 `M_0=B^TB`。若存在严格对角 `3 x 3` 核 `D_0` 和实数 `\eta`，使

\[
C=D_0+\eta M_0
\]

仍为严格核，则

\[
t\longmapsto
H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\]

在整个合法区间上凹；若 `B\ne0`，则严格凹。

当 `\alpha\ne\beta` 且 `M_0` 有非零非对角元时，`A,C` 均相关、非对角。`B` 可稠密，左右奇异二维子空间均可不在任何两坐标主平面中。

显式例：

\[
A=\frac25I+\frac1{30}J,
\quad
B=\begin{pmatrix}1&2&3\\4&5&6\\-5&-7&-9\end{pmatrix},
\quad
C=\frac25I+\frac1{1000}B^TB.
\]

其严格合法区间为 `|t|<\tau`，其中

\[
\tau^2=\frac{4091}{15000}-\frac{\sqrt{1663}}{150}>0.
\]

## I. 对角活动约化扇区上的任意秩跨块定理

固定严格实对称块 `A,C` 和任意实矩阵 `B`，令

\[
K(t)=\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}.
\]

若右侧存在坐标集 `J`，使

\[
B_{:,J^c}=0,
\qquad C_{J,J^c}=0,
\qquad C_J\text{ 为严格对角核},
\]

则 `t\mapsto H(K(t))` 在整个合法区间上凹。`|J|` 与 `rank(B)` 均不限；交换两块同样成立。

PR 内的精确 `3+5` 例具有两个大于二的非对角块、`rank(B)=2`，且右奇异平面稠密使用三个观测坐标；上一轮的“小块至多二”和“两坐标支撑”定理均不覆盖该例。

## J. 逐条件线的对角锚点判据

对左完整配置 `S` 令

\[
M_S=B^T(A-E_{S^c})^{-1}B.
\]

若每个 `S` 都存在实数 `\sigma_S`，使

\[
D_S=C-\sigma_SM_S
\]

是严格对角收缩核，则 `t\mapsto H(K(t))` 在整个合法区间上凹。

## K. rank-two 外幂特征的一般 Markov 伴随交织

令

\[
d_A(S)=\det G_A(S),
\qquad d_C(T)=\det G_C(T),
\]

并写

\[
r_s(S,T)
=1-s\operatorname{tr}(G_A(S)G_C(T))+s^2d_A(S)d_C(T).
\]

设 `Q_\vartheta` 是保持 `\mu=p_C` 的 Markov 核，`Q_\vartheta^\dagger` 是它在 `L^2(\mu)` 中作用于密度的伴随。若

\[
Q_\vartheta^\dagger G_C=\vartheta G_C,
\qquad
Q_\vartheta^\dagger d_C=\vartheta^2d_C,
\]

则

\[
(\operatorname{Id}\otimes Q_\vartheta)_\#P_s=P_{\vartheta s}.
\]

连续时间所需条件为

\[
L^\dagger G_C=-G_C,
\qquad L^\dagger d_C=-2d_C.
\]

若 `f_\tau=r_{e^{-\tau}s_*}`、`\mathcal I(\tau)=\langle f_\tau,\log f_\tau\rangle`，则

\[
\mathcal I'=\langle L^\dagger f,\log f\rangle,
\]

\[
\mathcal I''=
\langle(L^\dagger)^2f,\log f\rangle
+\left\langle\frac{(L^\dagger f)^2}{f}\right\rangle,
\]

且真实 `K`-仿射参数 `t` 上的凹性等价于

\[
2\mathcal I''+\mathcal I'\ge0.
\]

第二项保留全部完整配置 Fisher。一般相关块上的存在性与曲率符号仍开放。

## L. 对角核的外幂次数闭合

若 `C=\operatorname{diag}(c_i)`，令

\[
z_i(T)=\frac{\mathbf1_{i\in T}-c_i}{c_i(1-c_i)},
\]

且 `v_i^T` 为 `V` 第 `i` 行，则

\[
G_C(T)=\sum_i z_i(T)v_iv_i^T,
\]

\[
d_C(T)=\sum_{i<j}z_i(T)z_j(T)\det(v_i,v_j)^2.
\]

逐坐标独立刷新把一次分数乘 `\vartheta`、二次互异坐标分数乘 `\vartheta^2`，从而精确实现 K 的交织条件。

## M. 可逆外幂半群的严格相关二点障碍

取

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},
\qquad V=I_2.
\]

在 `\mu=p_C` 下，

\[
\langle d_C,(G_C)_{12}\rangle_\mu=-125/78\ne0.
\]

故不存在任何 `0<\vartheta<1` 的 `\mu`-可逆 Markov 核同时把 `G_C` 与 `d_C` 分别乘以 `\vartheta`、`\vartheta^2`，也不存在相应可逆连续生成元。该命题只排除普遍可逆机制，不否定 DPP 熵凹性。

## N. 相关准自由衰减不自动下降为经典占据配置通道

令

\[
K_\pm=\begin{pmatrix}1/2&\pm1/10\\\pm1/10&1/2\end{pmatrix},
\quad
A_0=\begin{pmatrix}1/2&1/5\\1/5&1/2\end{pmatrix},
\quad \vartheta=1/2.
\]

`K_+` 与 `K_-` 的完整配置分布相同。经

\[
K\mapsto\vartheta K+(1-\vartheta)A_0
\]

后，输出满事件概率分别为 `91/400`、`99/400`。所以没有一个只依赖输入占据配置分布的统一经典随机核能在所有准自由输入上表示该相关固定点衰减。

## 未解决范围

仍未解决：两侧活动块都大于二且均相关、一般非坐标 `rank(B)=2`，并且条件方向不满足 G 中三项判据时的整条径向配置熵凹性或严格反例；非可逆平稳伴随生成元是否存在；若存在，K 中的完整熵耗散曲率是否自动非负；一般实有限核、固定标量平稳熵率与一般复 Hermitian 版本。没有正弦差反例。新颖性未认证。
