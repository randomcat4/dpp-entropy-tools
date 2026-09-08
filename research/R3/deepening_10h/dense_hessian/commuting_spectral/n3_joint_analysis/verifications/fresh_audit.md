# D10-M6 非作者验缝

日期：2026-09-08。采用 math-theorem 的验缝分层，不改作者材料。

**版本冻结：**本初审绑定 `initial_author_hashes.json`，其中 joint 脚本为 `e691fb...`。完整重放完成后作者开始实时修订；当前修订稿不在本裁决内，也没有获得本报告的认证。版本漂移导致的一次测试失败详记于 `version_drift.json`。

## 最终分层裁决

**原稿整体：INCORRECT，存在三项可局部修复的错误；不因此推翻全部 SCOUT 数据。**

| 项目 | 裁决 | 范围 |
|---|---|---|
| exact-event 及 H=count+G_P(r)+G_P(s) | CORRECT | 任意 Q∈O(3)、严格谱 θ，局部 K-affine 谱线 |
| 固定 (Q,θ) 的 Hessian / copositivity 等价 | CORRECT | 点态非正曲率；不是连续参数域上的证明 |
| 文稿 κ(C) 判据 | INCORRECT | 展示公式漏了四个加号；代码中的和式正确 |
| simplex 程序“返回一般矩阵准确最大值” | INCORRECT | 奇异零最大值可漏；固定绝对阈值还会漏大尺度严格正最大值 |
| sphere 全 support 特征向量覆盖 | CORRECT | 精确算术下连重特征值亦可用最小支撑论证覆盖；数值实现仍仅 SCOUT |
| 两批分母与零候选 | CORRECT as replay / SCOUT | 60384、83456、574547 均重放匹配 |
| Ψ'' 可正、单层可正 | CORRECT | 独立精确有理邻近实例和严格对数区间确认；总曲率仍负 |
| 将 Ψ''≤0 称为更弱/未关闭目标 | INCORRECT | 它是更强的充分条件，且已被显式例子否定 |
| 任意 n=3 PSD 谱速率的总熵凹性 | INCOMPLETE | 没有反例，也没有一般证明 |

## 1. 概率语义、分解和 Hessian

令 ℓ_i=θ_i/(1-θ_i)。严格谱下 L=Q diag(ℓ)Q^T，L-ensemble 公式与包含概率 Möbius 容斥等价。对 det L_S 作 Cauchy–Binet 展开，得到

\[
p_S=\sum_{J:\,|J|=|S|}\det(Q_{S,J})^2
\prod_{j\in J}\theta_j\prod_{j\notin J}(1-\theta_j).
\]

在 n=3，单点层的平方子式为 q_ai²；二点层由余子式恒等式得到同样的 q_ai²，以缺失行 a、缺失列 i 编号。该等式同时覆盖 det Q=±1，不要求旋转而排除反射。于是作者的四层事件公式正确。严格 θ 使 r、s 每个分量正，而每行 P=q² 和为 1，故所有事件原子及条件层对数均有定义。

设 π_1=Σr_i、π_2=Σs_i。按 N=|Y| 使用熵的链式法则，N=0、3 时条件熵为零，N=1、2 的加权条件熵分别是 G_P(r)、G_P(s)。因此精确得到

\[
H(Y)=H(N)+G_P(r)+G_P(s).
\]

对任意正向量路径 x，利用 Σ(Px)=Σx=π 直接微分：

\[
G_P(x)''=-\sum_a\frac{y_a'^2}{y_a}
+\frac{\pi'^2}{\pi}-\sum_a y_a''\log(y_a/\pi).
\]

这里 Cauchy–Schwarz 只控制前两项的和非正；不能删除最后一项。作者分解的符号和 complement 方向翻号均正确。count 的 Shepp–Olkin 输入被限制在 Poisson-binomial 计数熵，没有不当传递给全事件熵。

固定 (θ,Q)，θ∈(0,1)^3 上 H 光滑，沿 θ+tv 的二阶导数为 v^T Mv，其中 M 是对称 3×3 Hessian。作者用 e_i 和 e_i+e_j 的六次评估重构 M，极化系数 1/2 正确。因为所有非零 v 都有一个非空局部可行区间，且二阶型在 v→-v 下不变，PSD/NSD 方向的点态非正曲率确与 -M 在闭非负象限的 copositivity 等价。

“给定 (θ,Q) 的点态等价”不证明“所有 (θ,Q)”成立；若要求完整仿射区间凹性，还必须让点态断言覆盖该区间每个基点。

## 2. 必须修订：κ(C) 的展示公式

`copositive_and_sphere_reduction.md:42`–`47` 把五项直接并列，没有加号，按 LaTeX 意义是乘积。应是

\[
\kappa(C)=\sqrt{c_{11}c_{22}c_{33}}
+c_{12}\sqrt{c_{33}}+c_{13}\sqrt{c_{22}}
+c_{23}\sqrt{c_{11}}+\sqrt{2\bar c_{12}\bar c_{13}\bar c_{23}}.
\]

不是仅有视觉区别。例如

\[
C=\begin{pmatrix}1&-1/4&1/4\\-1/4&1&1/4\\1/4&1/4&1\end{pmatrix}
\]

严格对角占优且正定，当然 copositive；错误的五项乘积却为负，会错误排除它。代码 `copositive_margins_for_negative_hessian` 保留了正确加号，故这不是本批计算零命中的来源。

核对来源：Hadeler 的 3×3 判据也可写成各对角及 bar 非负，再加 `det C≥0 或 T≥0`，T 为上述前四项之和；研究论文 [Copositive geometry of Feynman integrals](https://doi.org/10.1007/s11005-025-01961-w) 明确列出此等价式。恒等式 T²−2∏bar=−det C 说明它与正确 κ 和式一致。

代码把最终 κ 判据容差设成 -5e-9，把 simplex 非正判断容差设成 5e-8，而正候选门槛是 1e-10。这些不相同的容差只适用于数值一致性检查，不构成 exact copositivity 证书。

## 3. 单纯形枚举：准确最大值与正号检测必须区分

一般全支撑驻点满足 Mv=λ1、1^T v=1。作者 `joint_copositive_probe.py:253` 通过 M^{-1}1 构造；`263` 行遇到奇异矩阵直接略过，因此不是完整驻点求解器。

独立单元测试实际调用原函数，取

\[
M=\begin{pmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{pmatrix}.
\]

在 simplex 上 v^TMv=1−3||v||²≤0，真最大值为 0，唯一在 v=(1/3,1/3,1/3) 取得。程序返回 -1/2 和某条边的中点。它漏掉了奇异内点，并非舍入误差。独立有理 bordered KKT 方程

\[
\begin{pmatrix}M&-1\\1^T&0\end{pmatrix}
\binom v\lambda=\binom 01
\]

准确恢复 v=(1/3,1/3,1/3)、λ=0。因此函数文档中的“返回最大值”“所有情况准确到浮点”是过强陈述。这个一般矩阵反例并未声称自己来自某个 DPP Hessian。

不过，**精确算术下，该漏项不会漏掉严格正最大值**。证明如下：若全局最大点 v 在某支撑 I 的相对内点且最大值 m>0，则 M_Iv=m1。若 M_I 奇异，对任意 z∈ker M_I 有 0=z^T M_Iv=m1^Tz，故 1^Tz=0。取非零 z，沿 v+sz 走到 simplex 边界，二次型不变；因此同一个正最大值在更小支撑取得。重复此过程，最终在顶点或可逆支撑上被枚举。二维奇异情形也被作者的独立边二次式检查覆盖。

这说明可以保留“精确的严格正存在性测试”的数学路线，但不能据当前实现认证一般矩阵的准确最大值或零/严格负边界。有限阈值、`solve` 病态性与容差裁剪又增加数值限制，故本批仍为 SCOUT。

此外，原函数的固定绝对分母阈值本身会破坏上述理想化正号检测。取

\[
M=10^{14}\begin{pmatrix}-10&6&6\\6&-10&6\\6&6&-10\end{pmatrix}.
\]

在 simplex 上 v^TMv=10^14(6−16||v||²)，真最大值是 2×10^14/3>0，仍在均匀内点。满支撑矩阵可逆，但 1^T M^{-1}1=1.5e-14 被 `abs(denom)>1e-13` 的门槛拒绝；边上的最大值只有 -2e14，程序于是返回负值。该例已在冻结原函数快照上实际运行，结果保存为 `scale_simplex`。

这是**一般优化器的尺度反例**，不是声称这些矩阵能由本批严格剪裁的 DPP 参数产生。奇异反例和缩放反例均不能单独推翻本批 0 positive 记录，但足以要求删除无条件的“完整准确优化器”声明；理想化覆盖论证必须明确排除这些数值阈值。

## 4. 球面 support 枚举：重特征值可闭合覆盖

最大化 v^TMv，v≥0、||v||=1。紧致性保证最大点存在。选所有最大点中支撑基数最小的 v，记 I=supp(v)。相对内点的一阶条件给 M_Iv=λv。

若 λ 在 M_I 上的特征空间维数至少 2，取该空间中与 v 正交的非零 w。由于 v 在 I 上严格正，w 必有正负分量。沿 v+sw 走到非负象限边界，并归一化；它仍在同一特征空间，Rayleigh 商仍为 λ，却有更小支撑，矛盾。

所以存在一个最小支撑全局最大点，其支撑特征值简单。任意正交特征基均会列出这个向量及其反号；它同号，作者程序会保留。因为所有 7 个非空支撑均被枚举，精确算术下任意重复特征值也不会导致最大值遗漏。这比作者 hazards 中“重特征值需另处理”的保留说法更完整；只枚举满支撑的特征基当然不够，但当前代码并非如此。

若 j∉I，对曲线 (v+εe_j)/||v+εe_j|| 的右导数为 2(Mv)_j。因此全象限局部最大点必须满足 (Mv)_j≤0。作者记录的 KKT 符号正确。不把这些条件作为筛选也不会引入无效正曲率方向：所有被保留的 v 都非负可行，正二次型本身就是有效方向；而至少一个全局最大点已经包含在候选中。

数值实现使用 ±1e-10 同号容差，随后取绝对值，并按距离 1e-9 去重；它得到的是可行近似向量。接近退化时不能把这些阈值当形式证明。`574547` 是此实现的去重后计数，不是代数不变量，也不是 574547 次独立全事件重算。

## 5. 完整重放和统计口径

`replay_scans.py` 只读加载作者模块并调用 scan，不调用会覆盖作者 JSON 的 main；禁止生成作者目录的字节码缓存。两个输出写到本目录，完整重放 exit_code=0，总时间约 233.27 秒。

| 检查 | 原输出 | 本次重放 |
|---|---:|---:|
| joint 基点次数 | 60384 | 60384 |
| joint 正总曲率候选 | 0 | 0 |
| joint copositive/simplex mismatches | 0 | 0 |
| joint 最好总曲率 | -1.333333333333333 | 相同 |
| sphere 基点次数 | 83456 | 83456 |
| sphere support 候选次数 | 574547 | 574547 |
| sphere 正总曲率候选 | 0 | 0 |
| sphere 最好总曲率 | -1.3375999999999997 | 相同 |

三个正条件层记录的值及 sphere 的所报 ratio 也逐项匹配。

分母要进一步区分：

- structured_orthogonals 产生 6³×2=432 个列表项。joint 只取前 48 项×8 个谱=384；sphere 使用全部 432×8=3456，再分别加 60000 / 80000 个随机基点。这里是评估次数，不声称全是不同参数，也不声称覆盖全部 O(3)。
- joint 的总 Hessian 遍历 60384 个基点；Ψ、singleton、pair 的 Hessian 只在 60000 个随机基点重构，structured 循环未做这三层最大化。
- 每个 Hessian 用 6 个方向重构；joint 随机基点共重构四个 Hessian，即每点 24 次组件函数调用，不是总共六次。基础重构调用合计 384×6+60000×24=1442304，另有 best-record 更新等调用。
- copositive/simplex mismatch 比较只出现在随机循环，所以零 mismatch 的比较分母为 60000；384 个 structured 点虽算了 copositive margins，却没做同一 mismatch 记录判断。
- sphere 的 574547 次候选计算是 v^TMv。count/Ψ 组件和 ratio 每基点只在“总曲率最大”的那个 v 上计算；所报 -8.54e-8 不是 Ψ/(-count) 在全锥的最大值。这也解释为何它不与另一批正 Ψ 记录矛盾。
- 两个扫描都在找到首个正总曲率后提前停止；这次实际走完全部请求点，零列表不是被截断后的零。它们只有 summary JSON，没有逐基点 ledger，所以完整重放用于核对累计统计，不能将原文件本身当逐点审计轨迹。

这是原实现复现，与下一节的独立精确概率算法是两个不同层级；没有把原实现重放冒称独立数学推导。

## 6. 条件层正曲率：独立精确有理确认

`independent_check.py` 不导入作者事件、Hessian 或分层算法。对五个储存基点，先从作者 Q 的精确十进制有理条目构造 A=(Q-I)(Q+I)^{-1}，再取 B=(A-A^T)/2 和

\[
Q_*=(I+B)(I-B)^{-1}.
\]

本次五个 Q+I 均可逆。B 精确反对称，所以 Q_* 精确有理正交；程序以 Fraction 验证 Q_*^TQ_*=I。与作者 Q 的最大条目差均小于 4e-16。**这些是明确冻结的邻近有理实例，不是把浮点 Q 默称精确正交。** 每个 Q_*、θ、v 的完整有理参数、可行半径及全部八个事件三次多项式均在 `independent_check.json`。

随后对 K(t)=Q_*diag(θ+tv)Q_*^T 的全部主子式作精确排列行列式展开，再逐系数 Möbius 容斥；同时独立计算 spectral-channel 原子多项式，两者 40 个事件多项式、每个 4 个系数完全相同。概率及导数总和也用有理数精确核对。

五点 80 位 entropy 和 curvature 分解残差最多约 1e-77。对三个正层例进一步使用纯有理对数区间，而不是仅依赖 Decimal 正号：将 x=2^k m，1≤m<2；对 z=(m-1)/(m+1)∈[0,1/3) 使用

\[
2\sum_{j=0}^{7}\frac{z^{2j+1}}{2j+1}
\le\log m\le
2\sum_{j=0}^{7}\frac{z^{2j+1}}{2j+1}
+\frac{2z^{17}}{17(1-z^2)}.
\]

log 2 用 z=1/3 的同一界；负 k 时交换上下端。按每个有理 p'' 系数的符号传播区间，最后向外舍入至分母 10^9，得到严格包围：

| 邻近有理实例 | 待确认曲率的有理区间 | 总 H''（80 位节选） |
|---|---|---:|
| best_psi_simplex | Ψ''∈[81449/125000000, 651593/1000000000] | -4.554353674789741... |
| best_singleton_layer_simplex | singleton''∈[270250879/200000000, 675627199/500000000] | -223.579462659072115... |
| best_pair_layer_simplex | pair''∈[1529487739/1000000000, 1529487743/1000000000] | -167.017213379956431... |

三个总 H'' 也有独立有理对数区间，区间上端严格为负，完整端点存于 JSON。三个方向均有两项严格正、一项零，因此秩为 2，而不是 rank-one。

每个实例取

\[
r=\frac12\min_{i:v_i>0}\frac{\min(\theta_i,1-\theta_i)}{v_i}>0.
\]

则 |t|≤r 时全部谱仍严格在 (0,1)，精确 Q_* 保证该谱证书及 K-affine 性；v 非负，D 精确 PSD。参数和每个 r 的分母全部留存。

因此“单层总是凹”和“Ψ''总是非正”都被这些局部精确实例否定，且不是浮点正号幻象；但总熵曲率没有为正。这只是失败证明路线的负控制，不能宣传为 DPP 熵凹性的反例。

## 7. 必须修订：目标强弱与已证伪状态

`joint_reduction.md:131` 把 Ψ''≤0 称为比 Ψ''≤−H(N)'' 更弱的目标。因 H(N)''≤0，有 -H(N)''≥0，故逻辑相反：Ψ''≤0 是更强的充分条件。它现已被正 Ψ 实例否定，不应在 `134` 行附近继续仅作为“未关闭的不等式”叙述。

真正仍开放的是允许正 Ψ 由 count barrier 抵消的联合不等式。这一修订不改变作者最终总熵问题 INCOMPLETE 的状态。

## 8. 命令、范围与哈希

工作目录固定为仓库根；所有新文件只在本 verifications 目录，无作者文件修改。

```powershell
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/verifications/replay_scans.py
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/verifications/independent_check.py
```

完整双扫描重放 exit_code=0，冻结后的最终独立检查 exit_code=0，约 0.34 秒。中间新增尺度测试时，实时作者函数已经从原版本改成引用 `SIMPLEX_DEGENERACY_TOL` 等模块级辅助量的修订版本，导致原 AST 测试夹具触发 NameError，未写入结果；该次 Python 执行失败已保留，不能因随后同条 shell 中的哈希命令成功而算作测试成功。

现已将两种优化器反例绑定到 `original_simplex_snapshot.py`，概率输入绑定到完成的 `joint_replay.json` / `sphere_replay.json`。`replay_scans.py` 增加初审源哈希门；实时作者脚本变更后，它会拒绝把新版本当原版本重放。若重放整个初始扫描，需要恢复初审源版本；本目录只额外冻结了被测 simplex 函数，没有伪称保存完整原作者源码。当前实时修订将留给另行指定的 revised recheck。

线程变量固定为 1，无额外安装、无 GPU。复现环境 Python 3.12、NumPy；数值库特征基的选择可能影响退化情形下去重后的浮点候选数，当前同环境确实重现 574547。

关键 SHA-256：

```text
joint_copositive_probe.py
e691fb766e5a3a41357205e3656e07bed308f2a27f9b6c884df9f6f91446da9d
sphere_support_probe.py
3c376f113aaa1495d6cf4246f589c5aa98399407cf1dd3bcb011b364564106d9
copositive_and_sphere_reduction.md
d27262802f52450b57d49d2618521560cffebc940edd25541cede1818e87304d
joint_probe_results.json
bbc433f2fe358e6c35138da3845c25e76c1dcbfe1d655016e6f5fa7ea4fce246
sphere_probe_results.json
fe3569d4f000e218176584ba063d8883a2f62185faab5540f9e3fc584bf5a9f9
independent_check.py
e8c56ed5c89d593423e4b1082921c60610e7a3f84fc141b6a86615bf9d484d57
replay_scans.py
0e4e6dd81aae3bbff9c81f2c9cc699ef3cd9858d2dee4da270db045ed4fa2f27
```

其余作者文件哈希、完整有理参数和事件多项式见 `independent_check.json`；完整重放结果为 `joint_replay.json` 与 `sphere_replay.json`。本审查不涉及新颖性或一般 n=3 定理认证。
