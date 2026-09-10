# PR117 — 任意严格 `A_0` 中心的真实熵率局部凹性

Status: **ACCEPTED_SCOPED**。冻结作者头 `70d69bf5c47282c953010518ff264cb2a7a09bf9`，全部 7 个作者文件。S3 fresh SECOND 在未读取 FIRST 时先完成全源审并公开；作者随后只修正两份非承重来源/总览文件，S3 对精确 delta 复核通过；最后完整读取 S1 PR126 的版本绑定 FIRST。两审对承重证明链、量词和排除项一致。本结果是解析证明，不使用机器输出、有限窗符号或选定事件代替定理。

## 接受的定理

令实符号 `c,g in A_0` 满足

- `c(theta+1/2)=c(theta)`；
- `g(theta+1/2)=-g(theta)` 且 `g!=0`；
- 存在 `delta>0` 使 `delta<=c<=1-delta` 几乎处处。

记 `mu=c_hat(0)`。对每个奇频率 `k` 满足 `g_hat(k)!=0`，存在 `epsilon>0`，使真实物理仿射 Toeplitz 核

`K_t=T(c)+tT(g)`

在 `[-epsilon,epsilon]` 上严格合法，且完整配置 Shannon 熵率满足

`t -> h(c+tg)+|g_hat(k)|^4 t^4/[8mu^2(1-mu^2)]`

为凹函数；适当缩小区间后，其二阶导数在每个 `t!=0` 处严格为负，在中心可以为零。这里没有小 Wiener 中心条件，也没有任何正 Fourier 矩条件。

## 有限程预条件与绝对和边界

从固定严格中心选取同均值、半周期偶的有限 Fourier 截断 `c^0`，令 `r=c-c^0`。对每个有限体积完整 word，参考事件矩阵

`M_x^0=T(c^0)-I_Z`

经占据/空缺符号矩阵得到统一奇异值下界。它虽不定号但为有限带 Hermitian；几何逆展开给出对事件和体积统一的指数离对角衰减，并构造配置局域近似 `R_x^[R]`，满足算子误差 `Ce^(-aR)`。

完整原子精确因子化为

`p_t(x)=p_0(x) det(I+R_x^0 T(r+tg))`。

trace-log 的存在只使用算子收缩。空间展开后的绝对和另行估计：局域逆只付共同算子界 `B^m`，绝对位移和只付 Toeplitz 系数的 Wiener 范数；证明没有从非正规乘积的算子收缩推出逐路径逆包络。量词顺序是先把有限截断取得足够远，使冻结中心尾满足 `B||r||_W<1/4`，再冻结全部局域化常数并缩小 `t`，使 `B|t|||g||_W<1/4`。

作者后出的权威支撑计数为

`|J_(m,R,d)|<=C m^2(R+1)`，

与位移大小无关。结合完整法律 Jacobi/Bell 界，四阶以内的长度主项可取为

`C_q m^(3q+1)B^(m-1)eta^(m-q)(1+||g||_W)^q`。

它在 `B eta<rho<1` 下可和。每个完整原子的概率因子始终保留，所以对局域 observable 求和没有 `2^|J|` 损失，稀有原子、Fisher、原子加速度和混合响应项均未删除。

## 热力学极限与曲率

相对有限程参考的 KL 密度先按固定长度、位移和局域半径取体积极限，再由统一主项依次恢复 shell、位移与长度，得到局部 `C^4`。同一有限程参考的单侧完整 conditional 具有指数 cylinder shell；其交叉熵期望及边界误差也可四次微分。有限恒等式

`D(p_t||p_0)=-H(p_t)-E_t log p_0`

因此识别真正完整配置 Shannon 熵率 `h(c+tg)` 的 `C^4` 响应，而不是谱熵或有限窗曲率外推。

半周期结构固定奇偶子格边缘，并使零点两侧独立；故 `J(t)=h(c)-h(c+tg)` 是偶的、非负的 `C^4` 函数。若 `J''(0)>0`，二阶项直接给出严格局部结论；若 `J''(0)=0`，只导入已接受 PR53 的 regularity-free matching floor，四阶系数至少为

`|g_hat(k)|^4/[4mu^2(1-mu^2)]`，

即所加修正项系数的两倍。两种情况共同给出上述凹性和离零严格性。

## 来源修正与排除项

初稿曾错误声称无权 `p=1` BGS 代数在 `B(ell^2)` 中没有范数控制反演。Fang--Shin 2020 的引言明确回顾 Baskakov 的相应经典结果；作者在最终头撤回该说法。准确边界是：PR117 不需要、也不建立完整事件逆族的 BGS 范数控制；初始共同 `ell^1` 逆包络路线没有在本稿证明，但这不是文献上的不可能性，更不是熵反例。

本文不覆盖整个合法区间、`A_0` 外任意可测或仅平方可积符号、一般标量符号弦、一般有限实核凹性、实/复解析性、熵反例、新颖性、最优性或形式化验证。S1 指出的逐锚点估计 `|A_ii|<=||A||` 是现有算子 shell 界的直接说明，不是附加假设或未补门槛。

## 来源、双审与合并

- 作者 [总览](../../research/I05-DPP-35-arbitrary-A0-20260910/README.md)、[`C^4` 主证明](../../research/I05-DPP-35-arbitrary-A0-20260910/arbitrary_A0_C4_proof.md)、[曲率证明](../../research/I05-DPP-35-arbitrary-A0-20260910/arbitrary_A0_concavity.md)、[算子/绝对和审计](../../research/I05-DPP-35-arbitrary-A0-20260910/operator_vs_absolute_sum_audit.md)、[支撑计数修正](../../research/I05-DPP-35-arbitrary-A0-20260910/support_count_correction.md) 与 [来源审计](../../research/I05-DPP-35-arbitrary-A0-20260910/source_and_failure_audit.md)。
- S1 FIRST [冻结范围](../../research/S1-pr117-first-20260910/frozen_scope.md)、[报告](../../research/S1-pr117-first-20260910/review_report.md)、[来源审计](../../research/S1-pr117-first-20260910/source_review.md) 与 [绑定](../../research/S1-pr117-first-20260910/source_binding.json)。
- S3 先于 FIRST 的 [fresh SECOND](https://github.com/randomcat4/dpp-entropy-tools/pull/117#issuecomment-5618371191)、[来源 delta](https://github.com/randomcat4/dpp-entropy-tools/pull/117#issuecomment-5618447349) 与 [双审交叉门](https://github.com/randomcat4/dpp-entropy-tools/pull/117#issuecomment-5618554246)。

FIRST 档案 PR126 以 `b42f0fc2bccf793312298d22721ae1b7b8bd501a` 合入，第二父为 `e2f2927cf1990e9e170b86db182b71c5564e1988`。作者 PR117 以 `2f66f1a67af9e23bf77ec04f1d6f716947072394` 合入，第二父为精确冻结头 `70d69bf5c47282c953010518ff264cb2a7a09bf9`。接受范围仅以本文为准。
