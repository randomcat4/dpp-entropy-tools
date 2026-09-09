# frozen_statement_v2.md

任务 ID：I05-W1-20260909-R2-continuation  
版本：v2，2026-09-09  
总体状态：**PARTIAL**

本文件冻结本轮新增命题。上一轮的条件 Schur 分解、`m x 2` 全弦定理、两坐标支撑推广和 rank-two 外幂公式保留在上级目录。这里的“已证明”表示本文给出了作者级完整推导；除特别注明的外部输入外，新增命题尚未经过新的非作者独立审阅。

## 0. 外部输入 D：对角锚点直线定理

本轮采用用户明确给出的、由另一独立团队完成的有限维定理：设 `D` 是任意大小的严格对角 Hermitian 收缩核，`V` 是固定 Hermitian 矩阵，则

\[
u\longmapsto H(D+uV)
\]

在其整个合法参数区间上凹。

本轮没有把该定理重新计作自己的独立结果，也没有重新审阅其原证明。仓库中对应材料位于 `research/C3/`；来源映射见 `sources_continuation.md`。

## 1. 定理 E：对角活动约化块上的任意秩跨块全弦凹性

固定严格实对称块 `A,C` 和任意实矩阵 `B`，令

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}.
\]

假设右块存在坐标子集 `J`，满足：

1. `B_{:,J^c}=0`；
2. `C_{J,J^c}=0`；
3. `C_J` 是严格对角收缩核。

则 `t -> H(K(t))` 在整个合法 `t` 区间上凹。

该定理不限制 `|J|` 或 `rank(B)`。特别地，`m,ell>2`、`rank(B)=2`、`B` 的右奇异平面稠密支撑在三个或更多坐标上时仍适用。右块在 `J^c` 上可以任意相关，只要它与活动子空间 `J` 在坐标意义下约化。交换左右两块后结论同样成立。

## 2. 推论 E1：一个不在旧覆盖范围内的精确族

取

\[
A=\begin{pmatrix}
2/5&1/20&1/30\\
1/20&1/2&1/25\\
1/30&1/25&3/5
\end{pmatrix},
\]

\[
C=\operatorname{diag}(1/3,1/2,2/3)\oplus
\begin{pmatrix}2/5&1/20\\1/20&3/5\end{pmatrix},
\]

以及

\[
B=\frac1{100}\begin{pmatrix}
1&1&2&0&0\\
2&0&3&0&0\\
1&-1&1&0&0
\end{pmatrix}.
\]

则 `A,C` 都是严格实对称收缩核，`rank(B)=2`，`B` 在右侧恰使用三个坐标且右奇异平面不包含于任意两坐标主平面，`C` 不是对角核，`K(t)` 至少在 `|t|<=1` 上严格合法，而 `t -> H(K(t))` 在整个实际合法区间上凹。这个例子不由上一轮“某一侧至多两个坐标支撑”或“某一侧块大小至多二”定理覆盖。

## 3. 定理 F：逐条件线的对角锚点判据

对左块完整配置 `S` 令

\[
X_S=A-E_{S^c},\qquad
M_S=B^{\mathsf T}X_S^{-1}B.
\]

若对每个 `S` 都存在实数 `sigma_S`，使

\[
D_S:=C-\sigma_SM_S
\]

是严格对角收缩核，则 `t -> H(K(t))` 在整个合法区间上凹。

这是一个有限、可直接检验的判据。所有非零 `(M_S)_{ij}` 必须给出同一比值 `C_{ij}/(M_S)_{ij}`；所有 `(M_S)_{ij}=0` 的位置同时要有 `C_{ij}=0`；所得 `D_S` 还须满足 `0<D_S<I`。该判据允许 `C` 本身相关且全连接，但不声称一般输入必满足比例关系。

## 4. 定理 G：rank-two 外幂特征的精确 Markov 交织

设 `rank(B)=2`，取满列秩分解 `B=UV^T`。在左右完整事件分布 `mu_A=p_A`、`mu_C=p_C` 下定义

\[
G_A(S)=U^{\mathsf T}(A-E_{S^c})^{-1}U,
\quad d_A(S)=\det G_A(S),
\]

\[
G_C(T)=V^{\mathsf T}(C-E_{T^c})^{-1}V,
\quad d_C(T)=\det G_C(T).
\]

上一轮已证明

\[
r_s(S,T):=\frac{P_s(S,T)}{\mu_A(S)\mu_C(T)}
=1-s\,\mathrm{tr}(G_A(S)G_C(T))+s^2d_A(S)d_C(T).
\tag{G1}
\]

设 `T_theta` 是右块配置空间上的一个 `mu_C`-可逆 Markov 核，满足

\[
T_\theta G_C=\theta G_C,
\qquad T_\theta d_C=\theta^2d_C.
\tag{G2}
\]

则精确地

\[
(\mathrm{Id}\otimes T_\theta)P_s=P_{\theta s}.
\tag{G3}
\]

数据处理由此给互信息沿降噪方向单调；它本身还不是熵凹性。若该 Markov 轨道进一步满足第 6 节的熵曲率条件，则得到目标 `t`-凹性。

## 5. 对角块时的外幂次数

若 `C=diag(c_1,...,c_ell)`，且 `v_i^T` 是 `V` 第 `i` 行，令

\[
z_i(T)=\begin{cases}1/c_i,&i\in T,\\-1/(1-c_i),&i\notin T.\end{cases}
\]

则

\[
G_C(T)=\sum_i z_i(T)v_iv_i^{\mathsf T},
\tag{G4}
\]

\[
d_C(T)=\sum_{i<j}z_i(T)z_j(T)\det(v_i,v_j)^2.
\tag{G5}
\]

在以 `Bernoulli(c_i)` 为平稳分布的逐坐标独立刷新核下，一次中心化坐标分数按 `theta` 缩放，二次无对角 Walsh 项按 `theta^2` 缩放。因此 (G2) 精确成立。

## 6. 生成元形式和可检验熵曲率证书

若 `T_{e^{-tau}}=e^{tau L}`，则 (G2) 等价于

\[
LG_C=-G_C,\qquad Ld_C=-2d_C.
\tag{G6}
\]

令 `f_tau=r_{e^{-tau}s_*}`，把 `L` 作用在右变量，定义

\[
\mathcal I(\tau)=\mathbb E[f_\tau\log f_\tau].
\]

则

\[
\mathcal I'(\tau)=\langle Lf_\tau,\log f_\tau\rangle,
\tag{G7}
\]

\[
\mathcal I''(\tau)=
\langle L^2f_\tau,\log f_\tau\rangle+
\left\langle\frac{(Lf_\tau)^2}{f_\tau}\right\rangle.
\tag{G8}
\]

在 `s=e^{-tau}s_*`、`t=sqrt(s)` 下，目标 `d^2H(K(t))/dt^2<=0` 等价于

\[
2\mathcal I''(\tau)+\mathcal I'(\tau)\ge0.
\tag{G9}
\]

所以 (G6) 是有限线性可行性问题，(G9) 是一个保留完整 Fisher 项的有限熵曲率证书。

## 7. 命题 H：相关准自由衰减不自动下降为经典配置通道

考虑

\[
K_\pm=\begin{pmatrix}1/2&\pm1/10\\ \pm1/10&1/2\end{pmatrix}.
\]

它们的完整配置 DPP 分布完全相同。取相关固定点

\[
A_0=\begin{pmatrix}1/2&1/5\\1/5&1/2\end{pmatrix}
\]

和 `theta=1/2`。标准规范不变准自由衰减的单粒子协方差映射为

\[
K\longmapsto \theta K+(1-\theta)A_0.
\]

两个输出非对角元分别为 `3/20` 与 `1/20`，故满事件概率分别为 `91/400` 与 `99/400`。输出配置分布不同。

所以不存在一个只依赖输入配置分布的统一经典随机核，可以在所有准自由输入上实现该相关固定点衰减。量子数据处理仍成立，但不能在没有额外桥接不等式时直接推出配置 Shannon 熵曲率。

## 8. 未解决范围

仍未解决：两侧活动块都大于二、均相关且 `rank(B)=2` 的一般非坐标径向族；满足 (G6) 的正 Markov 生成元是否总存在；即使生成元存在，(G9) 是否由 DPP 结构普遍保证；一般实有限核、一般复 Hermitian 版本和固定标量平稳熵率。新增作者结论尚未由新的非作者上下文独立审阅；新颖性未认证。
