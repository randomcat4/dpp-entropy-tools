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

## L-M2c：谱与谱基联合细化强化点

- 陈述：存在一个数值 fixed-Q 十二维中心和严格正谱速率，使机制比
  `rho=0.5685905197<1`；其冻结有理化 K,D 满足
  `H''=-34.3715675595...`，并在 `|t|<=1/200` 内严格可行。
- 状态：`CORRECT`（冻结点/账目）/ `SCOUT`（20000 个新提议）；独立
  90 位 exact-event、三条实际弦、Fraction LDL、四片 CSV/manifest/
  NPZ/log 均复核通过。
- 边界：外层谱与谱基搜索是有限启发式；有理化后不精确交换，因此严格
  证书仍是 near-commuting PSD 线，不是连续空间定理。

## L-M2d：修复记账后的联合细化强化点

- 陈述：存在一个数值 fixed-Q 十二维中心和严格正谱速率，使
  `rho=0.5715404865<1`；冻结有理化线满足
  `H''=-29.1832216087...`，并在 `|t|<=1/200` 内严格可行。
- 状态：`CORRECT`（完整存储账目与冻结点）/ `SCOUT`（20000 新提议）；
  非作者 90 位 exact-event、三弦、Fraction LDL 及四片逐行对账通过。
- 边界：完整 seed proposal 再生成未复跑；有限无命中不推出一般
  fixed-Q、PSD/NSD 或全实域凹性。

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

## L-M6：三维非负谱速率锥的点态二次型门

- 陈述：固定 `(Q,theta)` 后，总熵 Hessian 的非负谱速率符号可化为
  3x3 对称矩阵在非负锥上的二次型符号，并可用 simplex 或全 support
  sphere 候选作数值正号门。
- 状态：`CORRECT`（约化与 v3 修订验收）/ `SCOUT`（60384 基点、
  416691 support 候选）/ `INCOMPLETE`（全参数域）。
- 审计边界：原一般 simplex 精确最大值声明被奇异 KKT 与缩放反例否定；
  v3 指定回归通过，但相对残差仍不是逐约束最优性证书，故只作浮点
  scout。`Psi''<=0` 是已被精确正例否定的更强充分条件。

## L-M7：三维近均匀补集层的显式严格屏障

- 陈述：若 fixed-Q 三维严格核的 singleton/pair 条件原子均落在
  `[1/4,4/9]`，则对每个非零 one-sign 谱速率有 `H''<0`；谱裕量
  `epsilon` 上，`-H''` 至少为
  `2 log(81/64) epsilon(1-epsilon)||v||^2/9`。
- 状态：`CORRECT`；成对 jet 的 `L1` 常数 6、count/Fisher 边界、实
  uniform-layer signed-exchangeable 分类、紧参数邻域与全区间有理实例
  均经非作者独立 exact-event 核验。
- 非退化证书：三异谱、异质对角、全连接 K 与 rank-3 non-thinning PSD
  D 在 `|t|<=1/20` 内满足全部 12 条条件界，谱裕量为 `19/100`。
- 边界：一般 `B(theta,Q;v)>=0` 仍 `INCOMPLETE`；本条不含 mixed-sign
  速率或非对易 PSD 方向，也不把有限 sanity 分母当作全称证明。

## L-M8：三维补集层的联合乘积屏障

- 陈述：设 `alpha=Pr/R`、`beta=Ps/T`。互补加速度可精确写成
  `A=2 sum_{j<k}v_jv_k C_i`，且
  `C_i>=log(27 min_a alpha_a beta_a)`。若该最小乘积大于 `1/27`，则
  对每个非零 one-sign fixed-Q 谱速率有 `H''<0`。
- 状态：`CORRECT`；补集索引、随机矩阵行列约定、AM--GM 符号、单速率
  count-Fisher 严格性、显式常数与有理区间实例经非作者独立核验。
- 定量：谱裕量 `epsilon`、乘积裕量 `m>=m0>1/27` 时，`-H''` 至少为
  `2 log(27m0) epsilon(1-epsilon)||v||^2/9`。
- 边界：`C_i` 条件外一般 n=3 fixed-Q 全域仍 `INCOMPLETE`；六中心和
  12 次区间尝试只作 `SCOUT/exact sanity`，不含非对易 PSD 方向。

## L-M2e：第三轮 fixed-Q 邻域联合细化账目与冻结点

- 陈述：从已核验的第二轮 strongest 出发，修复 source 记账后的联合
  谱/谱基脚本四片各评估 5000 个新中心，并在每个中心内优化非负谱速率。
- 状态：`CORRECT`（20004 个存储行的账目与 strongest）/ `SCOUT`
  （20000 个新 proposal）/ `INCOMPLETE`（未做全 seed 再生成、无全称）。
- 结果：最好 `rho=0.5725909001<1`；90 位独立全事件复算给
  `H''=-45.3758897236...`，实际弦均负，严格有理 LDL/谱裕量证书通过。
- 边界：有理化对象因取整一般只 near-commuting；本条不是 fixed-Q 全域
  定理，也不是 PSD/NSD 一般定理。

## L-M2f：第四轮 fixed-Q 邻域联合细化账目与冻结点

- 陈述：从第三轮 strongest 再作四片各 5000 个联合谱/谱基 proposal，
  每片显式保留 source 行，并冻结最大机制比点。
- 状态：`CORRECT`（20004 个存储行与 strongest）/ `SCOUT`（20000 个
  新 proposal）/ `INCOMPLETE`（未全 seed 再生、无全称）。
- 结果：最好 `rho=0.5735840442<1`；非作者 90 位全事件复算给
  `H''=-42.1913416922...`，实际弦、Fraction LDL 与谱裕量均通过。
- 边界：精确有理化对象只作 near-commuting PSD 线解释；不改变翻号
  门槛 `rho>1`。

## L-M2g：第五轮 fixed-Q 邻域联合细化账目与冻结点

- 陈述：从第四轮 strongest 再作四片各 5000 个联合谱/谱基 proposal，
  每片显式保留 source 行，并冻结最大机制比点。
- 状态：`CORRECT`（20004 个存储行与 strongest）/ `SCOUT`（20000 个
  新 proposal）/ `INCOMPLETE`（未全 seed 再生、无全称）。
- 结果：最好 `rho=0.5740468374<1`；非作者 95 位全事件复算给
  `H''=-39.3902501599...`，实际弦、Fraction LDL 与谱裕量均通过。
- 边界：strongest 贴着本轮配置的 `0.01` 谱裕量地板，故后续另作降低
  地板的机制诊断；有理化对象仍只作 near-commuting PSD 线解释。

## L-M2h：谱裕量地板敏感性账目

- 陈述：从第五轮 strongest 出发，把配置谱裕量地板降为 `0.002` 后，
  四片各 5000 个 proposal 的新 strongest 有
  `rho=0.5746069387`、实际谱裕量 `0.0153714`；它比 source 更靠内部。
- 状态：`CORRECT`（冻结文件、120 位 strongest gate、全账本 margin
  profile）/ `SCOUT`（有限 20000 proposal）/ `INCOMPLETE`（无全称）。
- 结果：四个 margin bins 的最好 rho 依次约为 `0.5736420`、`0.5743571`、
  `0.5746069`、`0.5735366`，不呈朝边界单调增强。
- 边界：这排除的是该冻结批次的简单边界解释，不排除其他边界机制；
  有理化线仍只称 near-commuting。

## L-U1：均匀核 Hessian 与四阶项

- 陈述：`H''(I/2)[D,D]=-4 sum D_ii^2`；若 `diag(D)=0`，四阶项为
  `-8 sum_{i<j}D_ij^4`。
- 状态：`CORRECT`；独立 n=3 exact symbolic 复算通过。

## L-U2：异质对角 fiber 与零对角四阶项

- 陈述：固定 `diag K=x` 时，对角核唯一全局最大化 DPP 熵；若
  `X=diag(x)`、`diag D=0`，则 `H'=H''=H'''=0`，且
  `H''''=-12 sum D_ij^4/[x_i(1-x_i)x_j(1-x_j)]<0` 对 D 非零成立。
- 状态：`CORRECT`；全局等号条件、exact-event 二阶 atom jet、交叉边
  正交消失、显式四阶常数和紧盒统一界均经非作者独立 Fraction 核验。
- 边界：全局最大只在固定对角 fiber 内；四阶结论是从对角基点出发的
  零对角径向下降，不推出任意附近非对角核上的 Hessian 定号。

## L-U3/S9：全边穿孔后的 full-Hessian 负定性

- 陈述：若 `X=diag(x)` 严格，零对角 A 满足每个 `A_ij!=0`，则存在
  `epsilon_0(X,A)>0`，使 `0<|epsilon|<epsilon_0` 时
  `Hess H(X+epsilon A)` 在全部 `Sym(n)` 上严格负定；每个点周围还有
  full-Hessian 负定开邻域。紧对角盒、单位 A 及统一边下界给统一阈值。
- 状态：`CORRECT`；非作者独立极化四次式、核对混合导数阶数、余项、
  Schur 补与 n=2,3,4 exact-event 多变量展开。
- 边界：全边非零仅为充分非退化前提；稀疏图、高阶传播和全域结构仍
  `INCOMPLETE`。

## L-U4：直径二支撑图的 full-Hessian 负定穿孔

- 陈述：若零对角 A 的非零支撑图连通且直径至多 2，则对任意严格对角
  X，足够小非零 `epsilon` 下 `Hess H(X+epsilon A)` 在全部 `Sym(n)`
  上严格负定；若支撑图断开，则存在精确跨分量零曲率方向。n=3 中由此
  得到 connected iff 的完整分类。
- 状态：`CORRECT`；F5 消失、F6 triangle 系数、共同邻居缺边主项、三尺度
  合同和 disconnected factorization 均经非作者 exact-event 核验。
- 边界：一般直径大于 2 的连通图仍 `INCOMPLETE`；P4 单项探针非全
  Hessian 证明。

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

## L-S4：任意对角核上的全对称方向 Hessian 与 PSD/NSD 邻域

- 陈述：若 `K0=diag(x_i)` 严格，则对任意实对称 D，
  `H''_{K0}[D,D]=-sum D_ii^2/[x_i(1-x_i)]`。固定紧对角盒后，存在
  盒周统一邻域与 `c>0`，使其中所有 PSD/NSD 方向满足
  `H''_K[D,D]<=-c||D||_F^2`。
- 状态：`CORRECT`；非作者独立 exact-event/Möbius 推导与 n=2,3 异质
  有理例均通过。
- 边界：这是严格核域内的局部邻域存在定理；任意 indefinite 方向不在
  严格界内，零对角方向在对角核处二阶平坦。

## L-S5：非退化三维核上的 full-Hessian 负定证书

- 陈述：在 M7 equation (19) 的三异谱、异质对角、全连接有理 K* 上，
  对每个非零实对称 D 有
  `H''[D,D]<=-(43/50)||D||_F^2<0`；并存在 K* 周围的 full-Hessian
  统一负定开邻域。
- 状态：`CORRECT`；非作者以六变量 exact-event 多项式、独立有理 log
  区间和 Gershgorin 证书重建，最小行裕量严格大于 `43/25`。
- 审计修订：可选 PSD scout 的 off-diagonal Frobenius 梯度因子曾错误，
  修复并全量重跑后复审通过；定理证书不依赖该 scout。
- 边界：结论局部而非全域；精确 PSD-cone 最大方向仍未分类。

## L-S6：紧对角盒 PSD/NSD 邻域的显式半径

- 陈述：对固定 `n>=2`、`0<a<=b<1`，令 `s=min(a,1-b)`、`q=s^n`、
  `m=q/2`，并以证明中的逐事件三阶导数界定义 L。半径
  `delta=min(q/(2n),2/(nL))` 内，对全部 PSD/NSD D 有
  `H''_K[D,D]<=-2||D||_F^2/n`。
- 状态：`CORRECT`；determinant 混合导数计数、entropy 三阶链式法则、
  atom floor、PSD trace 不等式和小维 exact sanity 均经独立核验。
- 边界：显式常数极保守，只覆盖对角盒附近的定号方向，不含全域或
  indefinite 方向。

## L-S7：S5 full-Hessian 邻域的显式闭球

- 陈述：对 S5 的有理 `K_*`，半径
  `delta=36163/16056110400` 的闭 Frobenius 球内，所有核都严格且对任意
  实对称 D 有 `H''_K[D,D]<=-(43/100)||D||_F^2`。
- 状态：`CORRECT`；非作者核对 `L=160561104/841`、`L delta=43/100`、
  谱/atom 下界、三阶链式法则、混合 determinant 计数和全方向范数传递。
- 边界：半径是保守的解析下界，不是最大区域估计；不推出全域凹性。

## L-S8：M8 有理线上的 full-Hessian 负定整段

- 陈述：对 M8 Section 5 的有理 `K(t)=K_0+tR`，全部
  `t∈[-6/25,6/25]` 上 `-Hess H(K(t))` 的六坐标矩阵正定；同时 K 严格、
  connected、异质对角且三异谱。
- 状态：`CORRECT`；非作者从 exact events 重建 173 个有理区间叶、log
  包围和 Gershgorin 证书，最小行裕量约 `2.66258e-4`，无失败叶。
- 边界：这是一个特定三维连续线段，不代表所有 M8 核或全严格核域；
  更大半径的当前证书失败不等于数学反例。

## L-S8b：预条件 full-Hessian 线段扩张

- 陈述：S8 同一有理线上，对全部 `t∈[-29/100,29/100]` 有
  `-Hess H(K(t))>0`；整段谱裕量 `1/150`，并保持 connected、异质对角、
  三异谱。
- 状态：`CORRECT`；65 个有理预条件叶和 2 个 plain 叶经非作者逐项
  区间重建，闭区间无缝覆盖，合同矩阵全部可逆。
- 边界：`299/1000` 运算超时为 `INCOMPLETE`；预条件坐标的行裕量不能
  原样宣称为 raw Hessian 的 Frobenius 常数。
