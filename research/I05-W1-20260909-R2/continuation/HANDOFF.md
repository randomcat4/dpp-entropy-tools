# HANDOFF.md

## 当前冻结状态

本轮新增结论为 `PARTIAL`：

- 已把第二轮条件 Schur、`m x 2` 与外幂结果完整纳入 continuation PR；
- 新证对角活动约化扇区上的任意秩跨块全弦凹性；
- 新证逐条件线对角锚点判据；
- 新证 rank-two 外幂特征的精确 Markov 交织及真实 `t` 曲率的完整 Fisher 生成元公式；
- 严格排除相关准自由衰减自动下降为经典占据配置通道。

一般两侧相关大块、一般非坐标 `rank(B)=2` 仍开放。尚无严格正弦差反例。新增作者结论尚待新的非作者独立审阅。

## 下一任务 1：先裁决 exact Markov 生成元

输入固定在 `inputs/rational_examples.json` 的相关三点 `C,V`。目标是对

\[
LG_{11}=-G_{11},\quad LG_{12}=-G_{12},
\quad LG_{22}=-G_{22},\quad L\det G=-2\det G
\]

返回非负有理可逆导通量，或有理 Farkas 不可行证书。不要只返回浮点 LP 状态。

这个任务能直接区分两种局面：若可行，继续完整熵耗散曲率；若不可行，则“对所有相关 DPP 构造同次数 Markov 半群”的普遍机制已被一个明确输入严格排除。

## 下一任务 2：若生成元可行，认证整个合法区间

使用 `CODEX_VERIFICATION_TASKS.md` 中固定的 `A,U,C,V`，构造全部 64 个联合事件和

\[
\Psi(s)=2\mathcal I''+\mathcal I'.
\]

必须覆盖由精确 Schur 补确定的完整闭合法区间，保留

\[
\left\langle (Lf)^2/f\right\rangle
\]

这一完整 Fisher 项。输出全区间非负证书或严格负子区间。单点浮点值不能裁决。

## 下一任务 3：若 exact Markov 路线失败，转向加权条件 Hessian

直接研究

\[
\sum_Sp_A(S)D^2H(C-sM_S)[M_S,M_S]
\]

而不是逐 `S` 要求每条 rank-two 线凹。优先利用随机 resolvent 的精确矩恒等式

\[
\mathbb E(A-E_{S^c})^{-1}=0
\]

及其二阶外幂消去，寻找跨 `S` 的加权补偿。任何候选不等式必须保持完整事件 Fisher，且说明如何作用于非坐标二维奇异平面。

## 下一任务 4：严格反例门槛

只有在有理 `3+3` 三核全部严格合法、64 个事件逐一认证并得到

\[
\frac{H(K_-)+H(K_+)}2-H(K_0)>0
\]

的向外舍入正下界后，才标记 `COUNTEREXAMPLE`。正加速度项、浮点正 Hessian或某个充分条件失败均不够。

独立审阅与计算的完整输入、误差要求和输出格式见 `CODEX_VERIFICATION_TASKS.md`。
