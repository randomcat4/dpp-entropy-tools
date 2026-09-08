# 引理依赖账

## L-A1：块边缘核

- 陈述：DPP 在坐标子集上的边缘仍为 DPP，核为相应主子矩阵。
- 状态：`KNOWN`；相对 FT-A 严格更弱。
- 核验义务：只用包含概率定义即可推出。

## L-A2：熵次可加与等号条件

- 陈述：有限随机变量 `U,V` 满足 `H(U,V)<=H(U)+H(V)`，等号当且仅当
  独立。
- 状态：`KNOWN`；相对 FT-A 严格更弱。

## L-A3：非零跨块项破坏独立

- 陈述：若某个 `X_ij!=0`，则单点包含事件的联合概率为
  `A_ii B_jj-X_ij^2`，不等于边缘乘积。
- 状态：`CORRECT`；非作者已从 singleton inclusion 独立验缝。

## L-B1：三点路径闭包对象

- 陈述：FT-B 所述三元组在任意维存在，且可取 full-rank、connected、
  heterogeneous rational 数据。
- 状态：`CORRECT`；`S(tau)` 构造与 n=6 独立 exact-event/DP 复算通过。

## L-B2：一般 fixed-beta 路径族

- 陈述：`Omega_beta` 是非空开凸域；`K(tau)` 对 tau 线性，`L(tau)`
  为 SPD connected 三对角路径核，方向秩等于 tau 支撑大小。
- 状态：`CORRECT`。

## L-B3：路径熵二阶 selected-run 递推

- 陈述：在 fixed-beta 族的 $\tau(t)=\tau_0+t\delta$ 线上，可由区间
  continuant jets 与 selected-run DP 在 $O(n^2)$ 时间计算 $H,H',H''$；
  最后的 $T/Z$ 必须用稳定商递推，不能显式形成 `Z^-3`。
- 状态：`CORRECT`；非作者以 n=5 精确有理 Möbius Hessian、n=93
  Decimal/value-only 弦、精确 LDL 和完整 4608 次种子重放核验。
- 边界：修正扫描无正号是 `SCOUT`，不推出全族凹性。

## L-C1：弦 gap 的互信息分解

- 陈述：`Delta_E=Delta_A+Delta_B+I_0-(I_-+I_+)/2`。
- 状态：`CORRECT`；FT-C 与 KL/JS 等价分解均经非作者验缝。

## L-C2：非退化互信息中点隆起机制

- 陈述：存在一个明确结构族，使互信息中点隆起严格压过边缘熵 deficit，
  或证明某冻结族中不可能。
- 状态：`OPEN`（一般族）；294 次非退化评价未命中。固定十一维 PSD 族
  的 `|t|<=1/32` 排除为 `CORRECT`，全部 2048 事件及余项链条已验缝。

## L-M1：一般实方向 Hessian 分解

- 陈述：`H''=-sum (p')^2/p-sum p'' log p`，并可在全部实对称坐标上
  分成 Fisher 与事件加速度矩阵。
- 状态：`CORRECT`；n=3、n=5 独立实现与有限差分通过。

## L-M2：稳定 PSD 机制与固定特征向量缩减

- 陈述：存在一个严格十二维冻结核和正定方向，其事件加速度/Fisher 比为
  `0.5261099452`；限制到与核对易的方向子空间仍可达到 `0.5133580`。
- 状态：`CORRECT`（仅冻结点）；两轮非作者以 exact-event、Decimal、
  精确 LDL、实际弦和独立广义特征问题复算。
- 边界：两值都小于翻号门槛 1，不是正反例，也不推出一般 PSD 结论。

## L-U1：均匀核 Hessian 与四阶项

- 陈述：`H''(I/2)[D,D]=-4 sum D_ii^2`；若 `diag(D)=0`，四阶项为
  `-8 sum_{i<j}D_ij^4`。
- 状态：`CORRECT`；独立 n=3 exact symbolic 复算通过。

## L-S1：半正定方向符号

- 陈述：严格核上的非零 `D>=0` 或 `D<=0` 是否总有 `H''<=0`。
- 状态：`OPEN`；不得从 0.501403 的有限机制比值外推。

## L-S2：twin-pair 条件化排除

- 陈述：固定余部、两个坐标外耦合相同且二点方向
  `[[d,e],[e,d]]` 为 PSD/NSD 时，`H''<=-4(d^2-e^2)log2`，非零方向
  严格为负。
- 状态：`CORRECT`；非作者重推条件化 Schur 补、Shepp--Olkin 接口与
  rank-one 分支，并新增 n=4 有理 exact-event 核验。

## L-S3：原观察坐标对角 PSD/NSD 排除

- 陈述：若 `K(t)=diag(k_i+t d_i)` 整段严格可行，则
  `H''=-sum d_i^2/[x_i(t)(1-x_i(t))]`，且非零 D 时严格为负。
- 状态：`CORRECT`；非作者从包含概率 Möbius 反演、乘积 Bernoulli 熵和
  有理小维事件独立验缝。
- 边界：只覆盖固定观察坐标下的对角核/方向，不覆盖正交旋转后的任意
  对易对；一般 PSD/NSD 问题仍 `OPEN`。
