# 路线注册表

## D10-A：固定块边缘的全局排除

- 冻结版本：v1 / FT-A
- 状态：`CORRECT`
- 方法族：熵次可加、互信息等号条件、二点包含概率
- 关键引理：L-A1、L-A2、L-A3
- 结果：覆盖整个固定 `A,B` 可行截面的全局不等式、严格等号条件和
  `8 max X_ij^4` 粗下界，均经非作者核验

## D10-B：路径 L 的 K-仿射三点闭包

- 冻结版本：v1 / FT-B
- 状态：`CORRECT`（闭包定理）/ `SCOUT`（gap）
- 方法族：有理矩阵恒等式、消元理想、低维构造/不存在证明
- 关键引理：L-B1
- 结果：任意维 `S(tau)` 精确族、开凸可行域、方向秩公式及
  connected heterogeneous rational 三元组经非作者核验；`n=5..30`
  共 12480 条弦无正 gap，仅作有限证据；fixed-beta 族另有经独立核验的
  `O(n^2)` 二阶 jet，修正后 `n=5..100` 共 4608 个方向无正号

### D10-B3：路径二阶 jet 与 n=93 异常归因

- 状态：`CORRECT`（递推/异常归因/统计复现）/ `SCOUT`（有限符号）
- 结果：旧 `Z^-3` 中间下溢制造 `H''≈184.745` 假阳性；稳定商递推和
  Decimal 给 `H''≈-0.007024918934`，精确 LDL 证明冻结弦严格可行；
  非作者复现 4608 次修正扫描，正号计数为 0
- 边界：没有证明 fixed-beta 路径族整体凹，也没有完成一般实反例目标

### D10-B4：路径弱耦合连续排除区与曲率残差

- 状态：`CORRECT`（修订后非作者复审）/ `INCOMPLETE`（任意耦合）
- 结果：固定维数、紧 tau 盒和非空异质性裕量后，存在统一
  `epsilon>0`，使每个 `0<|beta_i|<epsilon` 的 sign chamber 内所有
  路径核严格可行、图连通、异质，且完整 tau-Hessian `<=-2I`；因此
  全部非零 K-仿射方向局部严格向下
- 机制：`H''=-Var(A)-Cov(ell,B)-E[(ell-Eell)(A-EA)^2]`；后两项是
  任意耦合下仍可能压过 Fisher 项的唯一残差
- 审查轨迹：首稿过严的 `-4` 严格界被等号例否决；修正精确等号条件和
  参数分量边界后，独立复审为 `CORRECT`

## D10-C：信息几何桥接路线

- 冻结版本：v1 / FT-C
- 状态：`CORRECT`（恒等式）/ `INCOMPLETE`（正机制）
- 目标范畴：概率单纯形中的互信息、散度与中点隆起
- 关键引理：L-C1、L-C2
- 结果：恒等式、概率单纯形 KL/JS 分解和秩二 sign-flip 机制已核验；
  294 次非退化评价无正 gap；十一维固定族的 `|t|<=1/32` 连续区间
  排除证书也已独立核验

## D10-M：一般稠密 Hessian 与机制比值

- 状态：`CORRECT`（公式/实现）/ `SCOUT`（有限结果）
- 结果：完整实对称 Hessian 及 Fisher/事件加速度分解已独立核验；
  1822 个 `n=3..13` 中心无正曲率；保存的机制比值最高 0.526110<1

### D10-H2：十二维稳定 PSD 机制与对易子空间

- 状态：`CORRECT`（冻结点与结构诊断）/ `SCOUT`（源 160 中心）
- 结果：65/70 位 exact-event 复算给 `rho=0.5261099452`、总曲率
  `-20.4712207967`；精确 LDL 证明 D 正定且 `|t|<=1e-4` 严格可行；
  与 K 对易的正定方向子空间已有 `rho=0.5133580`
- 下一参数化：固定 Q、改变异质正谱速率；门槛保持 `rho>1`

### D10-H3：十二维 fixed-Q 谱速率定向扫描

- 状态：`CORRECT`（冻结点计算/可行性）/ `SCOUT`（20000 中心）/
  `INCOMPLETE`（一般 fixed-Q）
- 结果：四片各 5000 中心、浮点正候选 0，最好 `rho=0.5464281988`；
  独立 80 位全事件复算给 `H''=-32.4367046423`，三条实际弦均负
- 证书：十进制有理化线的 D 正定，`|t|<=1/200` 上谱裕量至少
  `1/2000`；20000 行、seed 重放、四个 best NPZ 和日志全部对账
- 精确结构边界：原 scout 是数值 fixed-Q；有理化 K,D 的交换子约
  `1.87e-16` 而非精确零，故 exact 证书只能称 near-commuting PSD 线

### D10-H5：谱与谱基联合局部细化

- 状态：`CORRECT`（冻结点计算/可行性/账目）/ `SCOUT`（20000 提议）/
  `INCOMPLETE`（连续中心空间）
- 结果：从 D10-H3 冻结点出发，在中心之间同时扰动谱与固定谱基；四片
  各 5000 个新提议，正曲率与正弦差均为 0，最好
  `rho=0.5685905197<1`
- 核验：独立 90 位 exact-event 复算给 `H''=-34.3715675595...`，三条
  实际弦均负；Fraction LDL 证明有理化 D 正定并在
  `|t|<=1/200` 保留 `1/2000` 可行裕量；全部 CSV、manifest、NPZ 与
  日志逐项对账
- 记账边界：产生版本漏写已知为负的 source 行，但 20000 个新 proposal
  均完整在账，故不改变本批零命中；当前脚本已改为冻结 source 与每个
  candidate。精确有理化仍只认证 near-commuting PSD 线

### D10-H6：修复记账后的第二轮联合细化

- 状态：`CORRECT`（账目/冻结点）/ `SCOUT`（20000 新提议）/
  `INCOMPLETE`（完整 seed 重放与连续空间）
- 结果：四片各显式记录 1 个 source 与 5000 个 proposal；20000 个新
  提议中正 status/正 gap 均为 0，最大 gap `-6.16597e-5`，最好
  `rho=0.5715404865<1`
- 核验：非作者不导入作者 gate，90 位 Möbius exact-event 给
  `H''=-29.1832216087...`，三条实际弦均负；Fraction LDL 证明 D 正定
  且 `|t|<=1/200` 上有 `1/2000` 裕量，CSV/manifest/JSON/NPZ/log 对账
- 边界：没有重跑完整 20000 次 proposal 生成；外层仍为有限 joint
  basis/spectrum heuristic，有理化冻结线仍只称 near-commuting PSD

### D10-M3：固定谱基的投影 DPP 通道约化

- 状态：`CORRECT`（表示/分解/所列子类）/ `INCOMPLETE`（generic Q）
- 结果：`K=Q diag(theta) Q^T` 的事件律精确等于独立谱子集经固定
  projection-DPP 通道的输出；`H(Y)=H(|Z|)+H(Y||Y|)`
- 瓶颈：Poisson-binomial 基数项已知凹，正曲率只能来自固定基数条件
  通道熵；doubly stochastic 只保证点态熵增，不能保证沿 t 的二阶符号
- 闭合子类：signed permutation、任意二维固定谱块、1x1/2x2 观察块
  直和、cardinality-uniform 投影通道；均按陈述经非作者 exact-event
  和高精度导数核验

### D10-M4：二维固定谱基 PSD 速率排除

- 状态：`CORRECT`（n=2 定理与 n=3 方法阻断）/ `INCOMPLETE`（n>=3）
- 结果：任意 `Q in O(2)`、严格二维谱和非零 `v>=0` 均有 `H''<0`；
  count entropy 严格凹，singleton split 的 perspective entropy 非正
- 三维边界：精确 Householder 例给单个事件
  `p_{1}''=2339/2450>0`，但有理对数区间仍证总 `H''<0`；它只否定
  “逐事件二阶非正”的外推法，不是正熵曲率候选
- 核验：独立 28 个事件多项式和解析承重不等式复核通过

### D10-M5：三维补集层约化与定向侦察

- 状态：`CORRECT`（约化/账目复现）/ `SCOUT`（202000 方向）/
  `INCOMPLETE`（三维全称）
- 结果：orthostochastic `P=q^2` 下，singleton/pair exact atoms 分别为
  `Pr`、`Ps`，未知条件项为 `G_P(r)+G_P(s)`；两层各自可有正曲率，
  但有限搜索未见其和为正
- 分母：180000 random + 22000 local；最好总 H''=-1.3335172，最好
  条件和 `Psi''=-4.75484e-9`，正候选 0
- 边界：它提示补集层抵消结构，不证明 n=3 凹性

### D10-M6：三维联合 Hessian 的锥上约化与修订侦察

- 状态：`CORRECT`（约化/纠错/修订账目）/ `SCOUT`（有限批次）/
  `INCOMPLETE`（一般 n=3）
- 结果：固定 `(Q,theta)` 后，非负谱速率方向的总曲率符号等价于一个
  3x3 Hessian 在非负锥上的二次型符号；修订批次检查 60384 个基点和
  416691 个 support 特征向量候选，simplex/sphere 正门均为 0
- 审查轨迹：初稿的 kappa 展示漏加号、simplex 优化器漏奇异内点且有
  绝对阈值缩放反例、`Psi''<=0` 强弱关系写反；v3 加入回归并重跑后复审
  通过，但明确撤回“一般矩阵精确最大值”声明
- 结构阻断：精确有理实例给 `Psi''` 严格正区间
  `[0.000651592,0.000651593]`，而总 H'' 仍负；所以只能继续攻击
  `Psi''<=-H(|Y|)''` 的联合屏障不等式

### D10-M7：三维近均匀补集层屏障

- 状态：`CORRECT`（显式充分区域、交换基点分类、区间证书）/
  `INCOMPLETE`（一般 n=3 fixed-Q 全域）
- 结果：总屏障分解出 `2 log(3) sum_{i<j}v_iv_j` 基线；成对 jet 的
  `L1` 范数至多 `6 sum_{i<j}v_iv_j`。若 singleton/pair 条件原子都在
  `[1/4,4/9]`，则所有非零同号 fixed-Q 谱速率严格负曲率，谱裕量
  `epsilon` 上屏障至少
  `2 log(81/64) epsilon(1-epsilon)||v||^2/9`
- 非退化实例：三异谱、异质对角、全连接有理 K 与 rank-3 non-thinning
  PSD D 在整个 `|t|<=1/20` 内由 12 条有理多项式界覆盖；最小余量
  `3133489/37800000`，谱裕量 `19/100`
- 核验：非作者独立 Möbius/channel 双重重建 8 事件，复算分类、常数、
  12 个区间条件和实际弦；判定 `PASS`
- 边界：只覆盖 fixed-Q/commuting 的 one-sign spectral directions；不
  覆盖任意非对易 PSD，也未解决充分区域之外的全局残差

### D10-M8：三维补集乘积屏障

- 状态：`CORRECT`（解析充分条件与精确区间证书）/ `SCOUT`（六个有理
  中心）/ `INCOMPLETE`（条件外一般 fixed-Q 全域）
- 结果：互补层加速度精确为 `A=2 sum v_jv_k C_i`；若
  `m=min_a alpha_a beta_a>1/27`，则
  `C_i>=log(27m)>0`，从而所有非零 one-sign fixed-Q 谱速率严格负曲率
- 定量：谱在 `[epsilon,1-epsilon]` 且 `m>=m0>1/27` 时，屏障至少
  `2 log(27m0) epsilon(1-epsilon)||v||^2/9`；两层原子均至少 `1/5`
  是简单充分子区，并严格扩张旧 `[1/4,4/9]`
- 非退化区间：三异谱、异质、全连接有理 K 与 rank-3 D 在
  `|t|<=1/100` 上由精确六次多项式覆盖，谱裕量 `29/150`
- 核验：非作者重建 48 个事件多项式/192 系数与 12 个区间尝试；10 个
  通过、2 个失败完整保留。只限 commuting one-sign，不覆盖非对易 PSD

### D10-H7：第三轮联合谱/谱基局部细化

- 状态：`CORRECT`（冻结点/已存账目）/ `SCOUT`（20000 个新提议）/
  `INCOMPLETE`（未完整重生成 seed proposal、一般问题）
- 结果：四片各含 1 个 source 行与 5000 个新 proposal；所有 status 与
  gap 均非正，最好机制比 `rho=0.5725909001`，最大存储 gap 约
  `-6.09e-5`
- 核验：非作者独立逐行重算账目，以 90 位 Möbius exact-event 重建
  strongest 得 `H''=-45.3758897236...`，三条实际弦均负；Fraction LDL
  认证有理化 D 正定及 `|t|<=1/200` 严格可行
- 边界：有理化证书只认证 near-commuting PSD K-仿射线；`rho<1` 仍是
  负曲率，有限未命中不证明一般凹性

### D10-H8：第四轮联合谱/谱基局部细化

- 状态：`CORRECT`（冻结点/已存账目）/ `SCOUT`（20000 个新提议）/
  `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：四片各含 1 个 source 行与 5000 个 proposal；所有 status/gap
  均非正，最大 gap `-4.51714e-5`，最好 `rho=0.5735840442<1`
- 核验：非作者不导入作者 gate，以 90 位 Möbius exact-event 重建
  strongest 得 `H''=-42.1913416922...`；三弦全负，Fraction LDL 认证
  D 正定及 `|t|<=1/200` 有 `1/2000` 严格可行裕量
- 边界：未全量再生 20000 个 proposal；有理化线 near-commuting 而非
  精确 fixed-Q，有限负号不升级为全域定理

## D10-U：均匀核的四阶平坦脊

- 状态：`CORRECT`
- 结果：Hessian 零空间为零对角方向；所有非零零对角射线四阶严格向下，
  且足够近的去心径向邻域曲率严格为负

### D10-U2：异质对角核的全局 fiber 最大与四阶平坦脊

- 状态：`CORRECT`
- 全局结果：固定全部 singleton 边缘 `K_ii=x_i` 后，
  `H(K)<=sum h(x_i)`，等号 iff K 对角；任一非零 off-diagonal 由 pair
  inclusion `x_ix_j-K_ij^2` 破坏独立性
- 局部接触：在 `X=diag(x)` 与 `diag D=0` 处，前三阶熵导数为零，且
  `H''''=-12 sum_{i<j}D_ij^4/[x_i(1-x_i)x_j(1-x_j)]<0`
- 一致性：紧对角盒及单位零对角方向上有显式统一四阶负界，并由紧致
  连续性给统一小步径向下降；不把它写成附近所有 Hessian 都负
- 核验：n=2,3,4 独立 Fraction exact-event/Möbius 与旧均匀 U1 常数均
  通过；审计发现并修复一处 Taylor 展示漏加号，修订复审 `PASS`

## D10-S：半正定方向

- 状态：`CORRECT`（twin-pair 子类）/ `OPEN`（一般 PSD/NSD）
- 结果：任意维、真实外耦合的 twin-pair 定号方向在整个可行区间有
  `H''<=-4(d^2-e^2)log2`；PSD 秩一混合 Hessian 非正这一更强捷径被
  精确反例否定，但不反驳一般 PSD 方向主问题

### D10-S3：PSD 机制定向搜索与对角观察子类

- 状态：`CORRECT`（原观察坐标对角子类）/ `SCOUT`（有限 PSD 搜索）/
  `OPEN`（一般 PSD/NSD）
- 结果：对角 K 与对角 D 的整条可行线满足
  `H''=-sum d_i^2/[x_i(1-x_i)]`，非零方向严格为负；固定十二维中心
  22511 次提议/控制及 n=2..5 的 940 中心、14440 方向无正候选
- 范围：一般对易 K,D 不在对角观察子类内；配置熵不是谱不变量

### D10-S4：紧对角盒附近的 PSD/NSD 连续排除区

- 状态：`CORRECT`
- 结果：对任意严格观察坐标对角核 `K0=diag(x_i)` 和任意实对称 D，
  `H''=-sum D_ii^2/[x_i(1-x_i)]`；若 D 非零且 PSD/NSD，则严格为负
- 连续推广：固定 `n` 与 `[a,b]^n subset (0,1)^n` 后，紧致性与 Hessian
  连续性给出整个对角盒周围的统一开邻域，其中
  `H''_K[D,D]<=-c||D||_F^2` 对全部 PSD/NSD D 成立
- 核验：非作者从 exact-event Möbius 语义独立重推，并以 n=2,3 异质
  Fraction 例核验；半径只作存在性，不外推为全严格核域定理

### D10-S5：非退化三维核的完整 Hessian 负定邻域

- 状态：`CORRECT`（full Hessian/开邻域）/ `SCOUT`（有限 PSD 优化）
- 结果：在一个三异谱、异质对角、全连接有理 K* 上，`-Hessian` 的
  六坐标有理区间矩阵严格对角占优，最小 Gershgorin 行裕量
  `>43/25`；故对全部实对称 D，
  `H''<=-(43/50)||D||_F^2<0`
- 邻域：完整 Hessian 的矩阵连续性给 K* 周围统一负定开邻域，覆盖非
  对易 PSD/NSD，而非只覆盖 fixed-Q 方向；未给显式半径
- 审查轨迹：首轮发现可选 projected PSD scout 的 off-diagonal
  Frobenius 梯度漏除 2；修复后全量重跑与修订复审通过，核心证书从未
  依赖该优化器
- 边界：局部三维结论，不推出全域凹性；精确 PSD-cone optimizer 未解

### D10-S6：对角盒 PSD/NSD 的显式半径

- 状态：`CORRECT`
- 结果：令 `s=min(a,1-b)`、`q=s^n`、`m=q/2`，以 determinant 一至三阶
  混合导数的逐事件界定义显式 `L`，取
  `delta=min(q/(2n),2/(nL))`；若严格 K 距 `[a,b]^n` 中某对角核不超过
  delta，则全部 PSD/NSD D 满足
  `H''_K[D,D]<=-2||D||_F^2/n`
- 核验：非作者独立检查 atom floor、导数计数、链式法则、`2^n` 求和、
  PSD trace 界及 n=2,3,4 exact sanity
- 边界：半径极保守，仅为局部定量排除，不含 indefinite 方向或全域结论

共同瓶颈：正事件加速度必须压过 Fisher/JS 损失；同时必须尊重 `K`
空间仿射性，并把精确事件律与严格可行性纳入证书。
