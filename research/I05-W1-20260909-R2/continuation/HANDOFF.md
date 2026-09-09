# HANDOFF.md

## 当前冻结状态

总体裁决仍为 `PARTIAL`，但已经证明的范围比旧版 handoff 更大：

- 第二轮条件 Schur、`m x 2`、两坐标支撑与 rank-two 外幂公式；
- 实三点核沿任意不定秩二方向全弦凹；
- rank-two resolvent 特征的 KL／互信息充分统计与压缩 Hessian；
- 三点条件方向的三分判据；
- 两侧相关、稠密非坐标的 `3+3` rank-two 结构族；
- 对角活动约化扇区的任意交叉秩定理和逐条件对角锚点判据；
- Markov 密度伴随交织及完整 Fisher 曲率接口；
- 可逆外幂半群和统一经典准自由测量通道的严格障碍。

一般两侧相关大块、一般非坐标 rank two 在上述判据之外仍开放。没有严格正弦差反例。PR #43 的新增作者主张尚待新上下文独立审阅。

## 下一步 1：先做完整独立解析审阅

以 `CODEX_VERIFICATION_TASKS_v2.md` 为唯一审阅清单。尤其不能遗漏：

- `proof/04_three_point_indefinite_rank2.md`；
- `proof/05_diagonal_and_feature_routes.md`；
- `proof/06_correlated_3plus3_family.md`。

应分别裁决三点定理、外幂充分统计／Hessian、三点条件判据和相关 `3+3` 族，而不是只审后写的活动扇区与 Markov 文件。

## 下一步 2：非可逆伴随生成元 LP

固定相关三点 `C,V`，使用定向平稳流，不再要求可逆或对称导通量。目标是对

\[
L^\dagger G_{11}=-G_{11},\quad
L^\dagger G_{12}=-G_{12},\quad
L^\dagger G_{22}=-G_{22},\quad
L^\dagger\det G=-2\det G
\]

返回有理非负流或有理 Farkas 不可行证书。浮点 LP 状态不够。

## 下一步 3：若 LP 可行，认证全参数区间

保留全部 64 个联合事件和完整 Fisher，认证

\[
\Psi(s)=2\mathcal I''+\mathcal I'\ge0
\]

覆盖完整闭合法区间，或返回严格负子区间。使用向外舍入对数区间或带显式余项的有理级数；单点或中点符号不能裁决。

## 下一步 4：若 Markov 路线失败

转向跨左配置的加权条件 Hessian

\[
\sum_Sp_A(S)D^2H(C-sM_S)[M_S,M_S],
\]

利用随机 resolvent 与二阶外幂矩消去，而不是逐 `S` 要求一般 rank-two 线凹。任何候选必须保留完整事件 Fisher，并说明如何覆盖非坐标奇异平面。

严格反例仍须满足：有理三核全部严格合法、全部事件逐一认证、弦差有向外舍入严格正下界。已证明的三点判据和 `3+3` 结构族必须从搜索域中排除。
