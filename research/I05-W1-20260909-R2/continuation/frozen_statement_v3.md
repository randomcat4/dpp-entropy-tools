# frozen_statement_v3.md

任务 ID：I05-W1-20260909-R2-continuation  
版本：v3，2026-09-09  
总体状态：**PARTIAL**

本文件是 continuation 的最新冻结命题，取代 `frozen_statement_v2.md` 中对 Markov 核必须可逆的限制；v2 作为推导历史保留。第二轮原有条件 Schur、`m x 2` 定理和 rank-two 外幂公式见上级目录。除外部输入 D 外，以下均为作者级证明，尚待新的非作者独立审阅。

## D. 外部输入：对角锚点直线凹性

采用用户指定、由另一独立团队证明的有限维定理：任意严格对角 Hermitian 收缩核 `D` 与固定 Hermitian 方向 `V` 给出的函数

\[
u\mapsto H(D+uV)
\]

在其整个合法参数区间上凹。本轮只使用该输入，不重新计作自己的证明或审阅。

## E. 对角活动约化扇区上的任意秩跨块全弦凹性

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

则 `t -> H(K(t))` 在整个合法区间上凹。`|J|` 和 `rank(B)` 均不限；交换两块同样成立。

精确例：

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

\[
B=\frac1{100}\begin{pmatrix}
1&1&2&0&0\\
2&0&3&0&0\\
1&-1&1&0&0
\end{pmatrix}.
\]

两侧块都大于二，`A,C` 都非对角，`rank(B)=2`，右奇异平面稠密使用三个坐标而不包含于任意两坐标主平面。`K(t)` 至少在 `|t|<=1` 严格合法，且本定理覆盖它的整个实际合法区间。上一轮的“小块至多二”与“两坐标支撑”定理均不覆盖此例。

## F. 逐条件线的对角锚点判据

对左完整配置 `S` 令

\[
M_S=B^T(A-E_{S^c})^{-1}B.
\]

若每个 `S` 都存在实数 `sigma_S`，使

\[
D_S=C-\sigma_SM_S
\]

是严格对角收缩核，则 `t -> H(K(t))` 在整个合法区间上凹。

## G. rank-two 外幂特征的一般 Markov 伴随交织

设 `rank(B)=2`，取 `B=UV^T`，并定义

\[
G_A(S)=U^T(A-E_{S^c})^{-1}U,
\quad d_A(S)=\det G_A(S),
\]

\[
G_C(T)=V^T(C-E_{T^c})^{-1}V,
\quad d_C(T)=\det G_C(T).
\]

则

\[
r_s(S,T):=\frac{P_s(S,T)}{p_A(S)p_C(T)}
=1-s\operatorname{tr}(G_A(S)G_C(T))+s^2d_A(S)d_C(T).
\tag{G1}
\]

设 `Q_theta` 是保持 `mu=p_C` 的 Markov 核，`Q_theta^dagger` 是它在 `L^2(mu)` 中、作用于密度的伴随。若

\[
Q_\theta^\dagger G_C=\theta G_C,
\qquad Q_\theta^\dagger d_C=\theta^2d_C,
\tag{G2}
\]

则精确地

\[
(\operatorname{Id}\otimes Q_\theta)_\#P_s=P_{\theta s}.
\tag{G3}
\]

可逆核是 `Q_theta^dagger=Q_theta` 的特例，但一般不能要求可逆。

连续时间写成 `Q_{e^{-tau}}=e^{tau L}` 时，所需前向密度生成元满足

\[
L^\dagger G_C=-G_C,
\qquad L^\dagger d_C=-2d_C.
\tag{G4}
\]

令 `f_tau=r_{e^{-tau}s_*}`，经典互信息为

\[
\mathcal I(\tau)=\langle f_\tau,\log f_\tau\rangle.
\]

则

\[
\mathcal I'=\langle L^\dagger f,\log f\rangle,
\]

\[
\mathcal I''=\langle (L^\dagger)^2f,\log f\rangle
+\left\langle\frac{(L^\dagger f)^2}{f}\right\rangle,
\]

且真实 `K`-仿射参数 `t` 上的凹性等价于

\[
2\mathcal I''+\mathcal I'\ge0.
\tag{G5}
\]

第二项保留全部完整配置 Fisher。用定向平稳流 `r_xy=mu(x)q_xy>=0` 表示时，(G4) 和流量平衡是有理线性可行性问题。

## H. 对角核时的外幂次数闭合

若 `C=diag(c_i)`，令

\[
z_i(T)=\frac{\mathbf1_{i\in T}-c_i}{c_i(1-c_i)}
\]

且 `v_i^T` 为 `V` 第 `i` 行，则

\[
G_C(T)=\sum_i z_i(T)v_iv_i^T,
\]

\[
d_C(T)=\sum_{i<j}z_i(T)z_j(T)\det(v_i,v_j)^2.
\]

逐坐标独立刷新使一次分数乘 `theta`、二次互异坐标分数乘 `theta^2`，故 (G2) 精确成立。这解释对角锚点机制为何越过交叉秩一。

## I. 可逆外幂半群的严格相关二点障碍

取

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},
\qquad V=I_2.
\]

在 `mu=p_C` 下，精确地

\[
\langle d_C,(G_C)_{12}\rangle_\mu=-125/78\ne0.
\]

若某个 `0<theta<1` 的 `mu`-可逆 Markov 核同时满足

\[
Q_\theta G_C=\theta G_C,
\qquad Q_\theta d_C=\theta^2d_C,
\]

自伴性与不同特征值要求这两个特征函数正交，矛盾。因此不存在这样的可逆核，也不存在相应可逆连续生成元。

该障碍发生在已经由其他方法证明凹性的二维块上，所以只否定“普遍可逆外幂噪声”机制，不否定 DPP 凹性。非可逆伴随交织、隐藏状态 dilation 和条件 Schur 补偿仍开放。

## J. 相关准自由衰减不自动下降为经典占据配置通道

令

\[
K_\pm=\begin{pmatrix}1/2&\pm1/10\\\pm1/10&1/2\end{pmatrix},
\quad
A_0=\begin{pmatrix}1/2&1/5\\1/5&1/2\end{pmatrix},
\quad\theta=1/2.
\]

`K_+` 与 `K_-` 的完整配置分布相同。经准自由协方差衰减

\[
K\mapsto\theta K+(1-\theta)A_0
\]

后，两个输出的满事件概率分别为 `91/400`、`99/400`。所以没有一个只依赖输入占据配置分布的统一经典随机核能在所有准自由输入上表示该相关固定点衰减。

## 未解决范围

仍未解决：两侧活动块都大于二且均相关、一般非坐标 `rank(B)=2` 的整条径向配置熵凹性或严格反例；非可逆平稳伴随生成元是否存在；若存在，(G5) 是否自动成立；一般实有限核、一般复 Hermitian 版本与固定标量平稳熵率。没有正弦差反例。新颖性未认证。
