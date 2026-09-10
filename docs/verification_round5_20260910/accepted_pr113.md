# PR113 — 无正矩 Wiener 尾下的真实熵率局部凹性

Status: **ACCEPTED_SCOPED**。冻结作者头 `a2bced01cc5de30943b20387b7e1d260c384661e`，全部 9 个作者文件。S3 fresh SECOND 在未读取 FIRST 时先完成全源审并公开；随后与 S1 PR118 的版本绑定 FIRST 交叉比对，两审对承重证明链、接受量词与排除项一致。本结果是解析证明，不以有限窗符号、选定事件或数值 PASS 替代定理。

## 接受的定理

令实符号 `c,g in A_0`，`c` 在半周期平移下不变，`g` 在半周期平移下反号且非零。记共同均值为 `0<mu<1`，并设

`r_c=sum_(m!=0)|c_hat(m)| < delta=min(mu,1-mu)`。

对每个奇频率 `k` 满足 `g_hat(k)!=0`，存在 `t=0` 的非空实邻域，使真实物理仿射 Toeplitz 核

`K_t=T(c)+tT(g)`

的完整配置 Shannon 熵率满足

`t -> h(c+tg)+|g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]`

为凹函数；适当缩小邻域后，其二阶导数在每个 `t!=0` 处严格为负，在中心可为零。符号可以实值但非偶，因此有限 Toeplitz 核允许为复 Hermitian；证明没有把它旋转为谱熵，也没有改成 `L`-仿射路径。

## 完整事件与热力学响应

以同均值 Bernoulli 完整原子为参考，作者证明

`p_(Lambda,t)(x)=q_(mu,Lambda)(x) det(I+B_x A_(Lambda,t))`。

小 Wiener 条件给出非正规矩阵的行、列和共同收缩 `rho<1`，从而普通实 trace-log 分支在所有完整原子上统一合法。事件概率的固定阶导数界保留 `p_x` 因子，所以求和时没有隐藏的 `2^|Lambda|` 损失，稀有原子、Fisher 和加速度项也没有被丢弃。

闭路按不同支撑顶点组织；对每个固定导数阶，长度 `m` 的导数由多项式因子乘 `rho^(m-r)` 控制。先固定闭路长度和位移、再取体积极限，最后用绝对可和的位移卷积与几何长度主项交换级数，得到真正完整配置熵率的局部 `C^4` 响应。同一论证对每个预先固定的有限导数阶成立，因此在开小 Wiener 区间上得到实参数 `C^infty`；没有统一阶乘半径，故不接受实或复解析性。

## 奇偶匹配与显式尾族

半周期对称使偶、奇子格边缘固定，并给出完整法律的互信息恒等式

`J(t)=h(c)-h(c+tg)>=0`，

且 `J` 为偶函数。若 `J''(0)>0`，二阶项直接给出严格局部结论；若 `J''(0)=0`，只导入已接受 PR53 的不相交匹配 binary-KL 下界，得到四阶系数至少

`|g_hat(k)|^4/[4 mu^2(1-mu^2)]`，

即修正项系数的两倍。两种情况因此闭合，无需预先假定二阶项消失。

均值 `1/3` 的显式尾 `w_n=1/[n(log(n+2))^2]` 经半周期配对后属于 `A_0`，但不属于任一正权 Wiener 类 `A_p`（`p>0`），也不满足所述 Fourier `H^1` 条件。故它确实展示本定理越过正矩和 `H^1` 假设，而不是只给一个有限 Fourier 特例。

## 不能外推的结论

本文不覆盖小 Wiener 球外的一般 `A_0` 中心、等号边界 `r_c=delta`、整个合法区间、任意可测或仅平方可积符号、一般标量符号弦、实/复解析性、熵反例、新颖性、最优性或形式化验证。Bressaud–Fernandez–Galves 与 Fernandez–Maillard 只作混合/记忆比较来源，不被当作本 `C^4/C^infty` 参数响应定理的依据。

作者冻结源中 `parity_matching_concavity.md` 式 (4.8) 附近有一个非承重排版字符；上下文和不等式方向无歧义，未改写作者头，也不影响接受。

## 来源、双审与合并

- 作者 [总览](../../research/I05-DPP-34-small-wiener-20260910/README.md)、[完整事件闭路证明](../../research/I05-DPP-34-small-wiener-20260910/complete_event_loop_C4.md)、[奇偶匹配与凹性](../../research/I05-DPP-34-small-wiener-20260910/parity_matching_concavity.md)、[显式无正矩族](../../research/I05-DPP-34-small-wiener-20260910/explicit_zero_positive_moment_family.md) 与 [`C^infty` 延伸](../../research/I05-DPP-34-small-wiener-20260910/smoothness_extension.md)。
- S1 FIRST [冻结范围](../../research/S1-pr113-first-20260910/frozen_scope.md)、[报告](../../research/S1-pr113-first-20260910/review_report.md)、[来源审计](../../research/S1-pr113-first-20260910/source_review.md) 与 [绑定](../../research/S1-pr113-first-20260910/source_binding.json)。
- S3 先于 FIRST 的 [fresh SECOND](https://github.com/randomcat4/dpp-entropy-tools/pull/113#issuecomment-5616506447) 与 [两审交叉门](https://github.com/randomcat4/dpp-entropy-tools/pull/113#issuecomment-5616695498)。

FIRST 档案 PR118 以 `e702f9ffbf3435229704b477c82d75dc63d9366c` 合入，第二父为 `1fa744d057cda3e18ed9798e7d81c476c9913b25`。作者 PR113 以 `433dc32d02f97c801d625549a5feb80ee947cfb1` 合入，第二父为精确冻结头 `a2bced01cc5de30943b20387b7e1d260c384661e`。接受范围仅以本文为准。
