# 05 — rank-two 外幂次数、Markov 交织与生成元证书

本文件证明 continuation `frozen_statement_v2.md` 的定理 G 和生成元等价式。一般相关活动块是否满足这些条件仍开放。

## 1. 外幂似然比

设 `rank(B)=2`，取满列秩分解 `B=UV^T`。上一轮已证明

\[
r_s(S,T):=\frac{P_s(S,T)}{p_A(S)p_C(T)}
=1-s\,a(S,T)+s^2b(S,T),
\tag{1.1}
\]

其中

\[
a(S,T)=\operatorname{tr}(G_A(S)G_C(T)),
\qquad b(S,T)=d_A(S)d_C(T),
\]

\[
G_A(S)=U^T(A-E_{S^c})^{-1}U,
\quad d_A(S)=\det G_A(S),
\]

\[
G_C(T)=V^T(C-E_{T^c})^{-1}V,
\quad d_C(T)=\det G_C(T).
\]

## 2. 精确 Markov 交织

设 `T_theta` 是右配置空间上的 `p_C`-可逆 Markov 核，其条件期望算子满足

\[
T_\theta G_C=\theta G_C,
\qquad T_\theta d_C=\theta^2d_C.
\tag{2.1}
\]

由于可逆性，给联合分布应用该核后，相对于固定参考边际 `p_A tensor p_C` 的输出密度是 `(Id tensor T_theta)r_s`。逐项使用 (2.1)：

\[
\begin{aligned}
(\mathrm{Id}\otimes T_\theta)r_s
&=1-\theta s\,\operatorname{tr}(G_AG_C)
+\theta^2s^2d_Ad_C\\
&=r_{\theta s}.
\end{aligned}
\tag{2.2}
\]

乘回固定参考边际，得到

\[
(\mathrm{Id}\otimes T_\theta)P_s=P_{\theta s}.
\tag{2.3}
\]

这比整块刷新精细：一阶外幂必须乘 `theta`，二阶外幂必须乘 `theta^2`。完整块刷新把全部中心化特征统一乘 `theta`，所以在 `d_C` 非零时不能满足 (2.3)。

## 3. 对角核的混合判别式次数

设 `C=diag(c_1,...,c_ell)`，`v_i^T` 是 `V` 第 `i` 行。对完整配置 `T`，

\[
Y_T=C-E_{T^c}
\]

为对角矩阵，其第 `i` 个逆对角元是

\[
z_i(T)=\frac{\mathbf1_{\{i\in T\}}-c_i}{c_i(1-c_i)}.
\tag{3.1}
\]

所以

\[
G_C(T)=V^TY_T^{-1}V
=\sum_i z_i(T)v_iv_i^T.
\tag{3.2}
\]

二维 Cauchy--Binet 给

\[
\det\left(\sum_i z_iv_iv_i^T\right)
=\sum_{i<j}z_iz_j\det(v_i,v_j)^2.
\tag{3.3}
\]

可直接展开验证：`z_i^2` 系数因 `det(v_iv_i^T)=0` 消失，`z_iz_j` 系数为 `det(v_iv_i^T+v_jv_j^T)=det(v_i,v_j)^2`。

令每个坐标独立地以概率 `theta` 保留，以概率 `1-theta` 从 `Bernoulli(c_i)` 重抽。`z_i` 在平稳 Bernoulli 下均值为零，因此

\[
T_\theta z_i=\theta z_i.
\tag{3.4}
\]

不同坐标刷新独立，故

\[
T_\theta(z_iz_j)=\theta^2z_iz_j,\qquad i\ne j.
\tag{3.5}
\]

代入 (3.2)-(3.3)，精确得到 (2.1)。这给出条件 Schur、外幂和逐坐标刷新之间的桥梁。

## 4. 连续时间生成元

令 `theta=e^{-tau}` 且 `T_{e^{-tau}}=e^{tau L}`。对 (2.1) 在 `tau=0` 微分：

\[
LG_C=-G_C,
\qquad Ld_C=-2d_C.
\tag{4.1}
\]

固定 `s_*>0`，令

\[
f_\tau=r_{e^{-\tau}s_*}
=1-e^{-\tau}s_*a+e^{-2\tau}s_*^2b.
\]

由 (4.1)，

\[
\partial_\tau f_\tau
=e^{-\tau}s_*a-2e^{-2\tau}s_*^2b
=Lf_\tau.
\tag{4.2}
\]

定义两块经典互信息

\[
\mathcal I(\tau)=
\langle f_\tau,\log f_\tau\rangle_{p_A\otimes p_C}.
\]

因 `L1=0`，

\[
\mathcal I'(\tau)=\langle Lf_\tau,\log f_\tau\rangle.
\tag{4.3}
\]

再微分：

\[
\mathcal I''(\tau)=
\langle L^2f_\tau,\log f_\tau\rangle+
\left\langle\frac{(Lf_\tau)^2}{f_\tau}\right\rangle.
\tag{4.4}
\]

第二项是完整配置 Fisher 项，没有投影或删事件。

## 5. 与真实 `t` 曲率的等价关系

写同一互信息为 `I(s)`，其中 `s=e^{-tau}s_*`。链式法则给

\[
\mathcal I'=-sI'(s),
\tag{5.1}
\]

\[
\mathcal I''=sI'(s)+s^2I''(s).
\tag{5.2}
\]

又

\[
H(K(t))=H(A)+H(C)-I(t^2).
\]

所以

\[
-\frac{d^2}{dt^2}H(K(t))
=2I'(s)+4sI''(s)
=\frac2s\left(2\mathcal I''+\mathcal I'\right).
\tag{5.3}
\]

目标曲率非正因此等价于

\[
2\mathcal I''+\mathcal I'\ge0.
\tag{5.4}
\]

代入 (4.3)-(4.4)，得到有限配置空间上的精确证书：

\[
2\left[
\langle L^2f,\log f\rangle+
\left\langle\frac{(Lf)^2}{f}\right\rangle
\right]
+\langle Lf,\log f\rangle\ge0.
\tag{5.5}
\]

这不是把 `Q log` 项单独定号，而是利用一个正 Markov 结构把全部加速度和 Fisher 重新组织成熵耗散曲率。

## 6. 正生成元搜索是有理线性可行性问题

右块有 `N=2^ell` 个完整配置，平稳质量 `mu_x>0`。若要求可逆生成元，用无序对导通量

\[
w_{xy}=\mu_xq_{xy}=\mu_yq_{yx}\ge0
\]

作变量，则

\[
(Lf)(x)=\frac1{\mu_x}\sum_{y\ne x}w_{xy}[f(y)-f(x)].
\tag{6.1}
\]

把 `f` 依次取 `G11,G12,G22,d`，要求特征值 `-1,-1,-1,-2`，得到系数全为有理数的线性等式与 `w_xy>=0`。因此可行解可以给成有理导通量表，不可行性可以给成有理 Farkas 对偶证书；浮点 LP 状态不是最终证据。

本文件不声称一般相关 DPP 的该系统总可行。固定三点输入和严格认证要求见 `continuation/CODEX_VERIFICATION_TASKS.md`。
