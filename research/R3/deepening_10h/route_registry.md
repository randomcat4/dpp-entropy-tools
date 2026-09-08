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

### D10-H9：第五轮联合谱/谱基局部细化与边界诊断

- 状态：`CORRECT`（冻结点/已存账目）/ `SCOUT`（20000 个新提议）/
  `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：四片各含 1 个 source 行与 5000 个 proposal；所有 status/gap
  均非正，最大 gap `-4.78406e-5`，最好 `rho=0.5740468374<1`
- 核验：非作者不导入作者 gate，以 95 位 Möbius exact-event 重建
  strongest 得 `H''=-39.3902501599...`；三弦全负，Fraction LDL 认证
  D 正定及 `|t|<=1/200` 有 `1/2000` 严格可行裕量
- 边界：strongest 恰贴搜索配置的 `0.01` 谱裕量地板，但实际 K 仍
  strict；这提示单独降低地板检验机制，而不构成奇异点或全域结论

### D10-H10：降低谱裕量地板后的边界敏感性检验

- 状态：`CORRECT`（冻结账目/strongest/有限边界比较）/ `SCOUT`（20000
  个新提议）/ `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：配置地板从 `0.01` 降至 `0.002`；全部 status/gap 仍非正，最大
  gap `-3.82981e-6`，最好 `rho=0.5746069387<1`
- 核验：非作者以 120 位独立 4096-event/Mobius 得
  `H''=-40.2752548454...`，三弦全负，Fraction LDL 与
  `|t|<=1/200` 的 `1/2000` 裕量通过
- 边界诊断：strongest 实际谱裕量 `0.0153714`，高于上一 source 的
  `0.01` 且是新地板的 7.69 倍；四个 margin bin 的最好 rho 非单调，
  故本批不支持“提升纯由逼近谱边界驱动”，但只是一份有限证据

### D10-H11：谱裕量至少 0.02 的严格内区检验

- 状态：`CORRECT`（冻结账目/strongest/内区比较）/ `SCOUT`（20000 个新
  proposal）/ `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：把 H10 strongest 谱向 `1/2` 收缩到 source 裕量 `0.03`，并强制
  proposal 裕量至少 `0.02`；全部 20004 行 status/gap 非正，最好
  `rho=0.5745947309`，实际谱裕量 `0.0217108`
- 核验：非作者不导入作者 gate/search，以 120 位独立 4096-event/Mobius
  得 `H''=-47.2369085176...`；三弦全负，Fraction LDL 认证 D 正定及
  `|t|<=1/200` 的 `1/2000` 严格可行裕量
- 解释：该内区最好值只比 H10 当前最好低 `1.22078e-5`，约保留
  `99.9979%`；有限证据进一步削弱“高 rho 只是贴谱边界”的简单解释，
  但 `rho<1` 仍非反例，未完整重生全部 proposal 矩阵

### D10-H12：谱裕量至少 0.05 的更深内区检验

- 状态：`CORRECT`（冻结账目/strongest）/ `SCOUT`（20000 个新 proposal
  与跨裕量比较）/ `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：source 谱裕量 `0.06`、全部 proposal 记录裕量至少 `0.05`；20004
  行均无 positive gap 或 `rho>=1`，最好为 shard 1 index 2701，
  `rho=0.5729410207`
- 核验：非作者以 120 位独立 4096-event/Mobius 得
  `H''=-64.3600769391...`，三弦全负；Fraction LDL 认证 D 正定及
  `|t|<=1/200` 的 `1/2000` 严格可行裕量
- 解释：比 H10/H11 略低但仍约 0.573，说明当前机制在更深内区仍存在，
  同时提示随 margin 增大可能衰减；只有三个有限批次，不能声称单调或
  边界渐近定律，更不改变正曲率门槛 `rho>1`

### D10-H13：谱裕量至少 0.10 的深内区剖面

- 状态：`CORRECT`（冻结账目/strongest）/ `SCOUT`（20000 个新 proposal
  与跨裕量剖面）/ `INCOMPLETE`（完整 seed 重放与一般问题）
- 结果：source 谱裕量 `0.12`，全部 proposal 记录裕量至少 `0.10`；
  20004 行无 positive gap 或 `rho>=1`，最好 shard 0 index 70，
  `rho=0.5313886644`
- 核验：非作者独立 120 位 direct-Mobius 得
  `H''=-56.1447325358...`，全部 4096 atoms 与 signed determinant 一致，
  三弦全负；Fraction LDL 认证 D 正定及整段 `|t|<=1/200` 可行
- 解释：H10--H13 当前最好随实际 margin 约
  `.015,.0217,.05,.10` 为 `.574607,.574595,.572941,.531389`；这支持
  “到 0.10 后机制明显衰减”的有限观察，不证明单调性或边界渐近公式

### D10-H14：谱裕量至少 0.20 的中央区剖面

- 状态：`CORRECT`（冻结账目/最强点独立重算）/ `SCOUT`（20000 个新
  proposal 与跨裕量剖面）/ `INCOMPLETE`（一般问题）
- 结果：source 裕量 `0.22`，全部 proposal 裁剪至至少 `0.20`；20004 行
  无 positive gap 或 `rho>=1`，最好 shard 0 index 2996，
  `rho=0.3337720601`
- 核验：非作者独立 130 位 direct-Mobius 得
  `H''=-45.6559259259...`，四条实际弦均负；Fraction LDL 认证 D 正定及
  `|t|<=1/200` 有 `1/2000` 严格可行余量
- 解释：相对 margin `0.10` 的最好值明显下降；这是中央谱盒中的有限
  衰减剖面，不证明随 margin 单调，也不构成全局上界

### D10-H15：谱裕量至少 0.30 的更深中央区剖面

- 状态：`CORRECT`（冻结账目/最强点独立重算）/ `SCOUT`（20000 个新
  proposal 与跨裕量剖面）/ `INCOMPLETE`（一般问题）
- 结果：source 裕量 `0.32`，全部 proposal 裁剪至至少 `0.30`；20004 行
  无 positive gap 或 `rho>=1`，最好 shard 3 index 2902，
  `rho=0.1521946045`
- 核验：非作者独立 130 位 direct-Mobius 得
  `H''=-44.2031294195...`，三弦全负；Fraction LDL 认证 D 正定及整段
  `|t|<=1/200` 有 `1/2000` 严格可行余量
- 解释：H10--H15 的最好值随实际 margin 约
  `.015,.0217,.05,.10,.20,.30` 为
  `.574607,.574595,.572941,.531389,.333772,.152195`；仅为有限轮廓

### D10-H16：谱裕量至少 0.40 的中心谱盒剖面

- 状态：`SCOUT`（冻结账目与最强点的 fresh non-author audit 通过）/
  `INCOMPLETE`（全 seed 再生、单调性与一般问题）
- 结果：source 裕量 `0.42`，全部 proposal 裁剪至至少 `0.40`；20004 行
  无 positive gap、`rho>=1` 或异常 status，最好 shard 1 index 4686，
  `rho=0.03861710868`
- 核验：非作者用 160 位 direct-Mobius 重算得
  `H''=-41.5919048132...`；三弦全负，Fraction LDL 认证 D 正定及
  `|t|<=1/200` 有 `1/2000` 严格可行余量
- 解释：H10--H16 的最好值随实际 margin 约
  `.015,.0217,.05,.10,.20,.30,.40` 为
  `.574607,.574595,.572941,.531389,.333772,.152195,.038617`；这是有限
  描述剖面，不证明单调性，也不是中心谱盒的全域曲率上界

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

### D10-U3/S9：穿孔对角脊旁的 full-Hessian 负定开集

- 状态：`CORRECT`（局部与紧致统一版）/ `INCOMPLETE`（稀疏穿孔分类与全域）
- 结果：任意严格对角 `X` 与每条非对角边均非零的零对角 A，存在
  `epsilon_0(X,A)>0`，使所有 `0<|epsilon|<epsilon_0` 的
  `K=X+epsilon A` 都有完整 `Sym(n)` 负定熵 Hessian；每一点又有普通
  full-Hessian 负定开邻域，因此这些开区在整条对角平坦脊旁积聚
- 机制：U2 四阶式极化后，对角块为负常数量级，交叉块为
  `O(epsilon^3)`，边坐标块的主项为严格负的 `O(epsilon^2)`；Schur
  修正仅 `O(epsilon^6)`，不改变符号
- 核验：非作者 n=2,3,4 独立多变量 Fraction 检查 28 个 atoms、全部混合
  四次项消去与 46 个主导 z-Hessian 项，并补齐定量 Schur 小量条件
- 边界：全边非零是该主项证明的充分条件，不声称必要；稀疏 A 另行分类

### D10-U4：稀疏穿孔图的六阶传播

- 状态：`CORRECT`（连通且直径至多 2 的充分性、disconnected 阻断、
  n=3 完整分类）/ `INCOMPLETE`（一般连通图）
- 结果：任意 strict diagonal X 与任意非零实边权 A，只要支撑图连通且
  直径至多 2，所有足够小的非零 `X+epsilon A` 都有完整 Hessian 负定
  开邻域；一般维数 disconnected 支撑有精确跨分量零曲率方向
- 三维分类：triangle 与 path/star 成功，单边加孤立点及空图失败，故
  n=3 中 connected 当且仅当该小穿孔机制成功
- 机制：五次熵项恒为零；六次 triangle 项使缺失边 `(i,j)` 在有共同
  邻居时获得严格负的 `epsilon^4` Hessian 主项，并由三尺度合同封闭
- 核验：非作者独立核对 52 个 exact atoms、F5/F6 系数、混合阶数、缩放
  与断开图零方向；n=4 路径端点的 `epsilon^6` 探针仍只标 `SCOUT`

### D10-U5：四维路径的高阶传播与完整连通分类

- 状态：`CORRECT`（P4 小穿孔与 n=4 分类）/ `INCOMPLETE`（任意维连通图）
- 结果：任意严格对角 X 与任意非零 P4 路径边权 A，所有足够小的非零
  `X+epsilon A` 都有完整 `Sym(4)` 负定 Hessian；结合 U4，四维支撑图
  connected 当且仅当该小穿孔机制成功
- 机制：按图距离 `d(i,j)` 缩放缺边坐标；P4 六个 off-diagonal 坐标的
  极限块严格负对角，最远端点在 `epsilon^6` 阶获得负曲率，所有缩放后
  对角/交叉块余项消失
- 核验：非作者保留任意四个矩参数与三条路径边权，重建 94 项形式熵
  证书、全部 36 个条目和混合阶数；38 个四维连通标号图、228 个目标及
  LDL 枢轴完全重放，但这些有限覆盖仍只作 `SCOUT`
- 边界：一般最短路对角系数公式及任意维 connected 充分性尚未闭合；
  难点是同距离 limiting block 的交叉项，而非单个对角系数符号

### D10-U6/S10：对角脊是负定开集的角向泛型边界

- 状态：`CORRECT`
- 结果：每个严格对角核都是完整 Hessian 负定开集的相对边界点；零对角
  单位球上所有边都非零的方向集合开、稠密且满球面测度，并在足够小的
  非零半径进入该负定集
- 一致版：紧对角盒和 `min|A_ij|>=eta` 的紧角扇区共享一个小半径；每个
  足够小的环境球与负定集的交包含非空环境开集，因而有正 Lebesgue 测度
- 核验：非作者检查 Frobenius 归一化、n=2 两点球、角扇区正测度、U3
  一致量词及从低维径向扇区到环境正测度必须借助开放性的关键一步
- 边界：不声称负定集在整个严格核域稠密，也不分类所有稀疏角方向

### D10-U7：任意维连通支撑的完整小穿孔分类

- 状态：`CORRECT`
- 结果：对每个固定有限 n、任意严格对角 X、任意零对角实对称 A，沿
  `X+epsilon A` 的所有足够小非零点拥有完整 `Sym(n)` 负定 Hessian，
  当且仅当 A 的非零支撑图 connected；任意树、任意图直径和任意非零
  实边权均包含在内
- 精确主项：令 `d_e` 为坐标边 e 两端在支撑图中的距离，则
  `H_ee=-6 epsilon^(2d_e) sum_P[(prod_v w_v)(prod_{a in P}A_a^2)]`
  加高一阶余项；`e!=f` 的混合项比 `epsilon^(d_e+d_f)` 至少高一阶，
  图距离合同后的极限因此严格负对角
- 机制：exact-likelihood 系数中每个活跃顶点度至少 4；cross-block
  Hessian 恒零给 residual-support 局部性；等号情形只允许 doubled
  geodesic，通用 doubled-cycle 熵系数为 `-3`，二阶导后为 `-6`
- 核验：非作者逐条攻击局部性是否误用逐项相消、同距多最短路/共享端点/
  chord 等号情形、matching/chromatic 系数及余项量词，判定无缺口；独立
  Fraction 小图只作补充 sanity，不承担一般性
- 边界：阈值依赖固定的 X 与全部非零边权；不覆盖 epsilon=0、边界对角、
  随 n 一致阈值或远离对角脊的全域 Hessian 符号

### D10-U8/M10：三维全域 Hessian 的一维 Schur 化

- 状态：`CORRECT`（结构化简、五维严格子空间、秩一边界族）/
  `SCOUT`（510+30 点）/ `INCOMPLETE`（全域标量界与 n=3 全域）
- 结构：以三个条件 odds 对数 `l_ij<=0` 和三体交互 Lambda 定义
  `N=-diag(l23,l13,l12)-Lambda K`；任意严格 K 有 `N>=0`，connected 时
  `N>0`，包括 Lambda=0 的非数值严格性论证
- 化简：`B=-Hess H=Fisher-2 tr(N adj D)`；经 N 合同后，完整六维正定
  问题等价于显式 positive-form-minus-rank-one 的单标量 `rho<1`。因而在
  `tr(N^-1 D)=0` 的五维超平面上曲率已严格为负，整个 Hessian 至多只剩
  一个可能坏方向
- 边界：对稠密秩一族
  `K_epsilon=epsilon I+(theta-epsilon)uu^T` 及补集，已证足够小 epsilon
  时 full Hessian 负定，且
  `rho=1-1/[theta log(1/epsilon)]+O(log^-2)` 从下方趋近 1；这否定统一
  `rho<=c<1` 的证明路线，却没有给出越过 1 的信号
- 核验：主审计独立核对 exact atoms、odds 恒等式、N 的两个符号分支、
  adjugate/Schur 与 off-diagonal Frobenius 因子；另一审计独立核对移动
  切/法空间、1+2+3 块缩放及补集。有限定向中心无正候选仍只作 SCOUT
- 边界：全域剩余问题已被集中为一个 DPP-specific Fisher 标量不等式；
  尚未证明 `rho<=1`，也未证明整个 n=3 核域全 Hessian 非正

### D10-U10a/U10b：标量门槛的信息投影化与错误捷径排除

- 状态：`CORRECT`（等价重写、充分条件、精确 blocker）/
  `INCOMPLETE`（全域 `rho<=1`）
- 结果：`rho` 等价于八个 event score 的 ridge 最小能量；Fisher-only
  Bessel 界并不普遍成立，补集自适应五分类代理也被严格有理 path 点否定
- 精确修正：遗漏的条件 Fisher 信息恰为三个正交 rank-one score 项，
  逐次 Sherman--Morrison 给
  `rho=R_T-c1-c2-c3`；剩余条件
  `c1+c2+c3>=R_T-1` 与原标量问题等价，而不是已经推进的弱引理
- 核验：两个非作者实现分别重建 ridge 归一化、Fisher-only blocker、
  path 的 log 区间/整弦以及全部三个 rank-one 修正；blocker 只否定证明
  代理，实际 `B(D)>28.680`

### D10-U10c：修复后的三维标量定向证伪

- 状态：`SCOUT`（fresh non-author corrected recheck）/
  `INCOMPLETE`（全域与完整 float seed 重放）
- 修复：首次 Decimal 空事件 jet 把对角 `-1` 错加到三个非对角坐标；
  已改为 `(-1,-1,-1,0,0,0)`，全部确定性高精度输出重生
- 结果：38436 次 float 尝试、22023 次 screen 接受；fresh 审计独立重建
  445 个高精度尝试，其中 444 个 strict valid、1 个精确非严格拒绝、
  0 个 `rho>1`；最好 `rho=0.9950999446`
- 风险：普通浮点在 `Lambda≈0` 且 N 近奇异时会把约 `0.5` 伪装成几乎
  `1`；因此候选必须重算 exact atoms/高精度 Fisher，有限未命中不作定理

### D10-U10d：中心交换对称路径的完整 Hessian 定理

- 状态：`CORRECT`（`x=1/2` 全部 strict path 与紧片厚化）/
  `INCOMPLETE`（一般二参数 path 与一般 n=3）
- 结果：对
  `K=[[1/2,a,0],[a,1/2,a],[0,a,1/2]]` 的每个 `0<8a^2<1`，完整
  `Sym(3)` 熵 Hessian 严格负定；不是只沿 path 族切向的结论
- 机制：反射与补集-sign 两个对称把六维 form 分块，核心 3x3 再 Schur
  成 2x2；其 determinant 由 `(1-r^2)n^2<4` 与 `0<rn-m<2r^2`
  给严格正下界
- 邻域：任意远离 `a=0` 与谱边界的紧中心线片段都有统一 x 向开厚化；
  一般 x 的 odd 块已正，even 块仍精确等价于单个 `sigma(x,a)>0`
- 核验：非作者从 exact atoms 重建 multiplicity、两次对称、Schur 公式
  和一元严格界，判定 centered theorem 与量词均无缺口

### D10-U10e：一般交换对称路径与双边界尺度

- 状态：`INCOMPLETE`（全域 `sigma>0`）/ `PASS`（解析约化恒等式的 fresh
  audit）/ `SCOUT`（高精度网格与双尺度 profile）
- 约化：一般
  `K(x,a)=[[x,a,0],[a,x,a],[0,a,x]]` 的 reflection-odd 块全域严格；
  even 四维块精确缩为单个 Schur 标量 `sigma(x,a)>0`，并以
  `c=2a^2/x^2` 把半域写成矩形 `0<x<=1/2, 0<c<1`
- 边界：`c->0` 时 `sigma->1/[x(1-x)]>=4`；唯一 full atom 在
  `c=1-s` 时为 `x^3s`，Fisher 出现显式正 rank-one pole，危险方向必须
  渐近切于该 atom 的零导超平面
- 双尺度：幂律 `s=x^p` 给 `x sigma->1`，真正有限尺度是
  `s=exp(-beta/x)`；冻结 profile 在 `beta≈0.58` 附近仍为正，但尚未把
  极限函数及一致余项闭成定理
- 核验：异人从 inclusion determinant 与 Möbius 重建 exact atoms，核对
  even/odd 交块、odd 严格性、Schur determinant 和 full-atom jet；稳定
  Sherman--Morrison 与直接 sigma 残差低于 `1e-153`。这些通过项不把
  `phi(beta)>0` 或全域 `sigma>0` 自动升级为定理

### D10-U10i：指数双尺度的闭式极限

- 状态：`SCOPED_CORRECT`（闭式极限与紧 beta 指数楔形）/
  `INCOMPLETE`（非紧 `beta(x)` 与全路径域）
- 闭式：在 `s=exp(-beta/x)`、固定 `beta>0` 下，作者通过受限能量极小
  而非 profile 拟合得到
  `phi(beta)=(beta+log2+2)(beta+log2)^4/[2 beta^2(log2)^2]`
- 正性与尺度：`phi>8(log2+2)>0`，两端发散；唯一极小点
  `beta≈0.5802776353`、极限最小值约 `26.60376012`。旧 `26.581` 是
  `x=1e-4` 的有限尺度值，两者已明确区分
- 连续结论：对每个固定紧 `beta` 区间，已审证明给
  `sigma=phi+O_J(sqrt(x))`，因而足够小 x 的整片连续指数楔形 full
  Hessian 严格负定；当 `beta(x)->0` 或无穷时尚无统一余项
- 核验：异人检查受限能量归一化、trial 的两个精确约束、U8 coercivity、
  singleton/full-atom forcing 与紧区间量词，并独立复算有限/极限数值；
  未发现 scoped 证明缺口，且明确拒绝向非紧 beta 或全路径外推

### D10-U10j：非紧指数尺度的定量扩张

- 状态：`PROOF_CANDIDATE_NO_BLOCKER_FOUND`（五分钟最小异审）/
  `INCOMPLETE`（完整常数审计、代数率和全路径）
- 候选界：令 `R=2+beta+1/beta`；在 `xR^6<=c`、
  `exp(-beta/x)<=x^2` 下，作者候选给
  `|sigma-phi(beta)|<=C sqrt(x)R^6`
- 推论候选：每个固定 `0<theta<1/12` 的连续区
  `x^theta<=beta<=x^(-theta)` 最终严格负定；`theta=1/24` 给
  `O(x^1/4)` 误差。最小异审确认量词推出和 R^6 估计骨架无循环
- 边界：异审未重建全部 universal constants、cofactor/eigenvalue 界和
  线性求解，因此未升为 `CORRECT`；`s=x^p` 对应的更小 beta 仍在域外

### D10-U10f：交换三角形族的 S3 约化

- 状态：`CORRECT`（exact atoms、S3 分块、去心对角紧致邻域）/
  `INCOMPLETE`（整个二参数三角形域）/ `SCOUT`（177360 点）
- 结果：对 `K=xI+a(J-I)`，完整六维空间分成二维 invariant 块与四维
  standard 块；standard 块对每个 strict `a!=0` 自动严格正，故全问题
  等价于一个显式二维负熵 Hessian 行列式 `Delta_T(alpha,beta)>0`
- 局部定理：任意 `x∈[r,1-r]` 上都存在统一 `epsilon_r>0`，使全部
  `0<|a|<epsilon_r` 的完整 Hessian 严格负定；这是一整条去心族及其
  环境开邻域，不是单个点
- 噪声归因：最差 binary64 小本征值 `-4.55e-13` 经 150 位重算为
  `+6.98e-13`；12/12 个冻结 warning 编码又由有理 log 区间严格证正，
  定位为大尺度消去误差而非仅凭阈值丢弃

### D10-U10h：交换三角形四条谱边界带

- 状态：`PASS`（秩一 Fisher 恒等式与四条紧横截边界带）/
  `INCOMPLETE`（角点、分离的紧中区与全域）/ `SCOUT`（86 点）
- 结构：二维 invariant Fisher 恰为
  `diag(u,2v)-kappa(u,-v)(u,-v)^T`，熵加速度只含两个 odds 对数；异人
  精确核对了 beta 重数导致的 factor 2 与 `n_beta/n_alpha` 的放置
- 边界定理：横向变量限制在任意 `[r,1-r]` 后，四条谱边界都有统一
  内邻域 full `Sym(3)` 严格负定；两个基本极限为
  `alpha Delta_T -> beta^2[2/(beta(1-beta))-2log(4/3)]` 与
  `beta Delta_T -> 2/(1-alpha)`，另两条由 complement 而非交换参数得到
- 阻断：`alpha<->beta` 不是熵对称，`C_ab>=0` 也在 `beta->0` 整条路径上
  失败；正的 `C_bb` 极点仍使 determinant 为正。四角双尺度和中区全局
  log 不等式仍未闭合

### D10-U10g：连通 Lambda-zero 子流形

- 状态：`CORRECT_SCOPED_MINIMAL_REPLAY`（结构恒等式、显式球与外场盒）/
  `INCOMPLETE`（全域）/ `SCOUT`（作者 15 个有理点）
- 参数化：经 sign gauge，连通 `Lambda=0` 等价于正加权 Cauchy
  `L_ij=w_iw_j/(z_i+z_j)`，`z_i` 两两不同；对角 external-field tilting
  保持该子流形，因而它具有真正三参数连续结构
- 精确门：外场 score 给 `F^{-1}eta=D_f`，保留三条条件 score 后完整
  Hessian 等价于一个显式 `3x3` Schur 矩阵 `T>0`；丢弃该修正的
  Fisher-only 充分条件在中心路径边界发散，因此不是可行全域捷径
- 显式邻域：围绕 `K(1/2,3/10)` 的 Frobenius 半径
  `49/214688160≈2.28238e-7` 球内，对所有 `D∈Sym(3)` 有
  `B(D,D)>=||D||_F^2/6`；异人以 exact Fraction/90 位重建 Kstar、18 个
  Fisher-field 条目、基点谱下界和全部半径常数，并验证三参数外场盒确实
  落入该球。完整 15 点账本未复跑，不影响解析球证书的限定结论

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

### D10-S7：非退化三维 full-Hessian 负定闭球的显式半径

- 状态：`CORRECT`
- 结果：以 S5 有理核 `K_*` 为中心，取
  `delta=36163/16056110400≈2.25229e-6`；整个闭 Frobenius 球自动严格
  可行、八个 exact atoms 至少 `87/2500`，且对全部实对称 D 有
  `H''_K[D,D]<=-(43/100)||D||_F^2`
- 机制：逐事件三阶导数给 Hessian Lipschitz 常数
  `L=160561104/841`，恰有 `L delta=43/100`，从 S5 的 `43/50` 基点
  裕量传递到整球
- 核验：非作者重建 signed determinant/Mobius、`3/6/6` 混合导数计数、
  atom floor 与 Frobenius 算子界，并独立检查 672 个 event jets
- 边界：半径故意保守，不近似最大负定连通区域；全域问题仍开放

### D10-S8：非退化三维 full-Hessian 负定连续线段

- 状态：`CORRECT`（整段证书）/ `INCOMPLETE`（更大区间与全域）
- 结果：沿 M8 Section 5 的有理线 `K(t)=K_0+tR`，对整个
  `t∈[-6/25,6/25]`，K 严格可行、全连接、异质对角、三异谱，且完整
  `Sym(3)` 熵 Hessian 严格负定，覆盖非对易 PSD/NSD 与不定号方向
- 机制：把 `B(t)=-Hess H(K(t))` 写成六坐标矩阵，以有理 subdivision、
  natural-log 区间和逐叶 Gershgorin 严格对角占优封闭连续区间
- 核验：非作者不导入作者模块，重建 173 个叶区间且 0 失败；最小行
  裕量约 `2.6625753e-4`，atom 下界 `63029/5000000`，谱裕量 `1/25`
- 边界：`49/200`、`1/4` 只在当前 Gershgorin 方法上失败，浮点仍负，
  不是反例；不声称 Frobenius 定量常数或最大区间

### D10-S8b：预条件证书扩张到近谱退化端点

- 状态：`CORRECT`（`[-29/100,29/100]`）/ `INCOMPLETE`（`299/1000` 与端点）
- 结果：同一有理线上完整 `Sym(3)` Hessian 负定段扩大到
  `[-29/100,29/100]`，覆盖 `49/200`、`1/4`、`7/25`，距正端首个谱
  退化点 `3/10` 只差 `1/100`；整段谱裕量 `1/150`
- 机制：困难叶使用固定有理上三角 P，对 `P^T B(t)P` 作区间
  Gershgorin；P 可逆，故以合同传回 `B(t)>0`
- 核验：67 叶无缝覆盖且全过，65 个预条件、2 个 plain；非作者逐叶
  重建，最小变换后行裕量约 `4.0965144e-4`，atom 下界
  `15168331/7680000000`
- 边界：变换后裕量不直接等于 raw B 的同数值下界；`299/1000` 严格
  区间运算超时只说明计算阻断，不是反例

### D10-S8c：正谱退化端点前的完整半开尾段

- 状态：`CORRECT`
- 结果：同一有理线的完整 `Sym(3)` 熵 Hessian 在
  `t∈[29/100,3/10)` 每一点严格负定；与 S8b 拼接后，正向已连续认证到
  首个谱退化端点之前，而非只认证若干靠近端点的采样点
- 机制：只有 empty atom 在 `t=3/10` 一阶消失；六个有理预条件叶覆盖
  `[29/100,299/1000]`，解析 scalar Schur majorant 覆盖
  `[299/1000,3/10)`，处理 `1/s` 与 `log(1/s)` 不同尺度
- 核验：非作者不导入作者 gate，独立重建八个 atoms 和六坐标 Hessian；
  bridge 最小变换裕量约 `0.2066315`，tail 模型最小裕量约 `0.6499154`
- 边界：`t=3/10` 不在严格核域而明确排除；粗 `h=1/100` 界失败只是
  方法失败，不是正曲率，也不推出整条可行线或全域凹性

### D10-S8d/S8e：负端尾段与整条最大可行线

- 状态：`CORRECT`
- S8d：完整 `Sym(3)` Hessian 在 `-1<t<=-29/100` 每点严格负定；只有
  full-set atom 在 `t=-1` 一阶消失，解析 Schur 尾段覆盖到
  `-999/1000`，162 个有理预条件叶无缝桥接到 `-29/100`
- 核验：非作者独立重建 atoms、奇异 jet、六坐标 Hessian、Schur 模型与
  全部叶；bridge 最小变换行裕量约 `0.00938478`，tail 裕量约
  `0.20009962`，0 个失败最终叶；`t=-0.9` 的重谱/等对角点也被覆盖
- S8e 拼接：S8d 的 `(-1,-29/100]`、S8b 的
  `[-29/100,29/100]`、S8c 的 `[29/100,3/10)` 恰好覆盖 M8 线的最大
  严格可行区间 `(-1,3/10)`；所以整条可行线每点的完整 Hessian 负定
- 边界：这是一条非平凡最大可行 affine line 的全线定理，不是整个 n=3
  核域的凹性；每点有环境开邻域，但不声称跨开放端点区间的统一半径

共同瓶颈：正事件加速度必须压过 Fisher/JS 损失；同时必须尊重 `K`
空间仿射性，并把精确事件律与严格可行性纳入证书。
