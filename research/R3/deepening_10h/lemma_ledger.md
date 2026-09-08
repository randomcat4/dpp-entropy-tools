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

## L-B4：fixed-beta 路径族的弱耦合统一负曲率

- 陈述：固定 `n`、`0<a<b<1` 与
  `0<eta<1/a-1/b`，存在 `epsilon(n,a,b,eta)>0`，使全部
  `tau in [a,b]^n` 且 `|1/tau_1-1/tau_n|>=eta`、全部非零小耦合
  sign chamber 以及全部方向同时满足 `nabla_tau^2 H<=-2I`；对应的
  `L` 为严格正定、图连通且异质的三对角路径核。
- 状态：`CORRECT`；首轮非作者审查否决了错误的严格 `-4` 表述，修订稿
  补全等号条件、eta 非空范围和图连通/参数分量区别后通过第二轮复审。
- 边界：这是定性弱耦合区域，不给 sharp epsilon，也不覆盖任意 beta。

## L-B5：路径曲率的 Fisher--残差分解

- 陈述：令 `ell=log det L_S`、`A=ell'`、`B=ell''`，则
  `H''=-Var(A)-Cov(ell,B)-E[(ell-Eell)(A-EA)^2]`；后两项组成全局
  翻号所需的唯一残差。
- 状态：`CORRECT`；解析微分与独立 exact-event 算术核验一致。
- 边界：残差尚无统一上界，故一般 fixed-beta 路径族仍 `OPEN`。

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

## L-M2b：固定谱基十二维强化点

- 陈述：存在一个浮点 fixed-Q 十二维中心和严格正谱速率，使机制比
  `rho=0.5464281988<1`；其冻结对称十进制有理 K,D 满足
  `H''=-32.4367046423...`，并在 `|t|<=1/200` 严格可行。
- 状态：`CORRECT`（冻结点）/ `SCOUT`（源 20000 中心）；80 位
  Möbius exact-event、实际弦、精确 LDL 和完整账目均经非作者复算。
- 边界：十进制有理化破坏精确交换性，交换子约 `1.87e-16`；exact
  证书是 near-commuting PSD 线，不是精确 fixed-Q 有理结构。

## L-M3：二维固定特征向量 PSD 谱速率排除

- 陈述：若 `n=2`、`K(t)=Q diag(lambda_i+t v_i) Q^T`、`Q in O(2)`、
  `0<lambda_i<1` 且非零 `v>=0`，则 `H''(0)<0`。
- 状态：`CORRECT`；exact-event 四原子、基数/单点层熵分解、承重
  AM--GM 严格界及秩一/重复谱边界均经非作者验缝。
- 三维阻断：存在严格可行有理例使单个 singleton atom 的二阶导为
  `2339/2450>0`；该例总 H'' 仍严格负，因此只阻断二维证明法。
- 边界：`n>=3` 的固定谱基 PSD/NSD 方向符号仍 `OPEN`。

## L-M4：谱子集到观察集的固定投影通道

- 陈述：固定 `Q` 时，`K=Q diag(theta) Q^T` 的 DPP 可表示为独立
  Bernoulli 谱子集 `Z` 经过
  `T_Q(S|R)=det(Q_{S,R})^2` 的 projection-DPP 通道；通道保基数，故
  `H(Y)=H(|Z|)+H(Y||Y|)`，并有显式 `p,p',p'',H''` 公式。
- 状态：`CORRECT`；Cauchy--Binet、包含概率到 exact atoms 的 Möbius
  识别、Fraction 导数及 90 位熵分解残差均经非作者核验。
- 推论：signed permutation、1x1/2x2 观察块直和与
  cardinality-uniform 通道给出已闭合凹子类。
- 边界：generic Q 的条件层熵曲率仍 `OPEN`；doubly stochastic 不提供
  二阶符号。

## L-M5：三维 singleton/pair 补集层联合符号

- 陈述目标：对 `P=q^2`、严格三维谱和 one-sign 速率，控制
  `G_P(r)''+G_P(s)''`，或至少证明它不超过 `-H(|Y|)''`。
- 状态：`OPEN`；exact layer reduction 与 202000 次搜索账为
  `CORRECT/SCOUT`，无全称证明。
- 已知阻断：`r_i''` 可正，且 singleton、pair 条件层分别可正，所以逐
  事件或逐层凹性均不是可行证明法；有限样本中两层正号尚未同时发生。

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
