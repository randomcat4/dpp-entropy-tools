# 07 — 一般 Markov 伴随交织与可逆机制的严格障碍

本文件修正并加强 `05_exterior_markov.md` 的 Markov 表述。可逆核只是充分特例；一般存活路线必须使用保持边际的 Markov 核在密度上的 `L^2(p_C)` 伴随。新增内容尚待新的非作者独立审阅。

## 1. 非可逆版本的精确交织

令 `mu=p_C`，`Q_theta(x,y)` 是右配置空间上的 Markov 核，并假设 `mu Q_theta=mu`。其作用在观测函数上的后向算子仍记 `Q_theta`；相对于 `L^2(mu)` 的伴随记作 `Q_theta^dagger`：

\[
\langle Q_\theta^\dagger f,g\rangle_\mu
=\langle f,Q_\theta g\rangle_\mu.
\]

若输入分布相对于 `mu` 的密度是 `f`，经过前向核 `Q_theta` 后的输出密度恰为 `Q_theta^dagger f`。逐坐标写即

\[
(Q_\theta^\dagger f)(y)
=\frac1{\mu(y)}\sum_x\mu(x)f(x)Q_\theta(x,y).
\tag{1.1}
\]

对 rank-two 径向族，

\[
r_s(S,T)=1-s\operatorname{tr}(G_A(S)G_C(T))+s^2d_A(S)d_C(T).
\]

所以只要

\[
Q_\theta^\dagger G_C=\theta G_C,
\qquad Q_\theta^\dagger d_C=\theta^2d_C,
\tag{1.2}
\]

就有

\[
(\operatorname{Id}\otimes Q_\theta)_\#P_s=P_{\theta s}.
\tag{1.3}
\]

证明是把 (1.2) 逐项代入 `r_s`；不要求 `Q_theta` 可逆。若核可逆，则 `Q_theta^dagger=Q_theta`，恢复 `05_exterior_markov.md` 的特例。

## 2. 非可逆连续生成元

令 `Q_{e^{-tau}}=e^{tau L}`，其中 `L` 是后向生成元，`L^dagger` 是密度的前向生成元。所需特征关系是

\[
L^\dagger G_C=-G_C,
\qquad L^\dagger d_C=-2d_C.
\tag{2.1}
\]

若 `q_xy>=0` 是 `x to y` 的跳率，令定向平稳流

\[
r_{xy}=\mu(x)q_{xy}\ge0\qquad(x\ne y).
\]

平稳性等价于每个状态的流量平衡

\[
\sum_{y\ne x}r_{xy}=\sum_{y\ne x}r_{yx}.
\tag{2.2}
\]

由 (1.1) 微分，

\[
(L^\dagger f)(y)
=\frac1{\mu(y)}\sum_{x\ne y}r_{xy}[f(x)-f(y)].
\tag{2.3}
\]

因此 (2.1)、(2.2) 与 `r_xy>=0` 构成一个系数全为有理数的线性可行性问题。可逆情形额外要求 `r_xy=r_yx`；本节说明该额外要求一般不成立。

熵耗散公式保持不变，只需把此前的 `L` 全部解释为前向密度生成元 `L^dagger`：

\[
\mathcal I'=\langle L^\dagger f,\log f\rangle_\mu,
\]

\[
\mathcal I''=\langle (L^\dagger)^2f,\log f\rangle_\mu
+\left\langle\frac{(L^\dagger f)^2}{f}\right\rangle_\mu.
\]

真实 `t`-凹性仍等价于 `2 I''+I'>=0`，完整 Fisher 项仍保留。

## 3. 可逆外幂半群的严格二点障碍

取相关严格核和满秩特征矩阵

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},
\qquad V=I_2.
\]

对每个完整配置 `T`，令

\[
Y_T=C-E_{T^c},\qquad G(T)=Y_T^{-1},\qquad d(T)=\det G(T).
\]

四个事件概率按 `T=00,10,01,11` 为

\[
\mu=(6/25,13/50,13/50,6/25).
\]

事件行列式给

\[
\mu(T)d(T)=(-1)^{2-|T|}.
\tag{3.1}
\]

因此

\[
\mathbb E_\mu[dG]
=C^{-1}-(C-E_{\{2\}})^{-1}-(C-E_{\{1\}})^{-1}+(C-I)^{-1}.
\tag{3.2}
\]

只看 `(1,2)` 元。四个逆矩阵对应的贡献分别为

\[
-5/12,\quad -5/13,\quad -5/13,\quad -5/12,
\]

所以

\[
\boxed{
\langle d,G_{12}\rangle_\mu=-\frac{125}{78}\ne0.
}
\tag{3.3}
\]

现在假设存在某个 `0<theta<1` 的 `mu`-可逆 Markov 核，满足

\[
Q_\theta G_{12}=\theta G_{12},
\qquad Q_\theta d=\theta^2d.
\]

可逆性使 `Q_theta` 在 `L^2(mu)` 自伴。于是

\[
\theta\langle d,G_{12}\rangle
=\langle d,Q_\theta G_{12}\rangle
=\langle Q_\theta d,G_{12}\rangle
=\theta^2\langle d,G_{12}\rangle.
\]

因 `theta != theta^2`，必有 `⟨d,G12⟩=0`，与 (3.3) 矛盾。

故：

> 对这个严格相关二点 DPP，不存在任何 `0<theta<1` 的可逆 Markov 核同时按 `theta` 缩放一次 resolvent 特征、按 `theta^2` 缩放二次外幂特征。

同理不存在满足相应 `-1,-2` 特征关系的可逆连续生成元。

## 4. 含义与边界

该障碍甚至发生在右块维数二，而该维数的跨块径向熵凹性已由完全不同的条件 Schur加二维熵定理证明。因此它只否定“普遍可逆外幂噪声半群”，不否定原凹性，也不否定：

- 非可逆平稳 Markov 核的伴随交织；
- 在更大隐藏状态空间上的 Markov dilation；
- 只对特定 `A,U,s` 成立的熵耗散不等式；
- 条件 Schur 路线中的跨 `S` 加权补偿。

后续 exact LP 应先移除 `r_xy=r_yx`，保留流量平衡 (2.2)，并要求前向伴随特征关系 (2.1)。
