# PR82 — `p>4` 完整事件响应与多尺度有限记忆速率的限定接受

Status: **ACCEPTED_SCOPED**。最终冻结作者头 `290a84064eaae2e857d637f58531e95f4ca3cb3b`。既有定性证明在 `365347e` 前完成限定 FIRST/SECOND；新增多尺度文件 `a81fa2349ef122d7c9ccbda43ddd70e8dfab402f` 及最终 README `18de8b1338ca23688207d87c6e9c95cd1105ab79` 又分别通过新鲜 FIRST 与独立 SECOND。

## 接受的范围

令 `a=p/2>2`。在源码所列 `c,g in A_p`、半周期偶/奇对称、非零奇 Fourier 模式及某个 `0<delta<1/2` 的严格谱裕量下，真实物理仿射核 `K_t=T(c)+tT(g)` 的完整配置 Shannon 熵率在零点附近满足修正局部凹性。证明使用全部完整事件的单侧条件律、真实不变未来律、Fisher 与响应项；不使用谱熵、有限窗外推或 `L`-仿射替代。

定性响应骨架接受以下结论：完整事件逆矩阵/两腿影响给出 `B_a` 变差；Bressaud–Fernández–Galves 的匹配后缀耦合连同内部重证的缺陷更新估计给出一阶损失

`R_s:B_b -> B_(b-1)`，`b>1`。

因此以 `s=t^2` 做两阶响应恰需 `a>2`，即该路线覆盖每个 `p>4`。旧 Dobrushin A1/A2 导入仍无效且未被使用。正确边界结论是有限时间相关/Poisson 截断误差 `O(M^-eta)`，其中 `0<eta<a-2`；已撤回的原始冻结记忆平稳导数速率不是前提。

新增定量单元针对规范化的 canonical memory-frozen conditional chain。若冻结深度为 `N`、时间截断为 `M`，则通过 `s` 的二阶响应满足

`C_(eta,F) { M^-eta + N^-a M^3 }`。

其中 `N^-a M^3` 是嵌套二阶响应的最坏项；证明没有暗中使用第三次强空间 Poisson 逆。取 `M=floor(N^(a/(3+eta)))` 得到 `N^(-a eta/(3+eta))`，所以任意严格小于 `a(a-2)/(a+1)` 的指数都可获得，端点指数不在结论中。

抽象移动可观测量应把误差记为

`epsilon_N = operator_error + observable_error = O(N^-a)`。

在熵专门化 `F=log G` 中，一致非空性把可观测量误差直接控制在同一核/算子误差内；这一非阻断澄清不改变速率。

## 不能外推的结论

冻结记忆条件链不被认作有限节 DPP。本文不接受有限窗熵 Hessian 外推、整个合法区间、`p<=4`、端点速率、任意可测符号、完整解析平稳响应、原 PR66 的 Dobrushin 路线、熵反例、最优性、新颖性或形式化验证。没有执行数值计算或开启新预算。

## 来源、双审与合并

- 作者 [项目索引](../../research/I05-DPP-31-20260910/README.md)、[定性修复](../../research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_repair.md)、[边界修正](../../research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_boundary_correction.md)、[一阶损失证明](../../research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_one_loss.md) 与 [多尺度定量证明](../../research/I05-DPP-31-pr66-lowreg-20260910/c4_response_spatial_truncation_p4_multiscale.md)。
- 既有 [3653 双审检查点](../verification_round4_20260909/pr82_3653_checkpoint.md)。
- 新鲜 FIRST [范围](../../research/S1-pr82-290a-delta-first-20260910/frozen_scope.md)、[报告](../../research/S1-pr82-290a-delta-first-20260910/review_report.md)、[静态检查](../../research/S1-pr82-290a-delta-first-20260910/code_review.md) 与 [来源绑定](../../research/S1-pr82-290a-delta-first-20260910/source_binding.json)。
- 独立 SECOND 的 [完整公开报告](https://github.com/randomcat4/dpp-entropy-tools/pull/82#issuecomment-5613623910) 与 [最终 README delta 记录](https://github.com/randomcat4/dpp-entropy-tools/pull/82#issuecomment-5613799451)。

FIRST 档案 PR105 以 `e0965104cf84eca96c737c737160b60043757470` 合入。作者 PR82 以 `09e09086c0dc8b30d5859a7e1e2cba86623d2631` 合入，精确最终审阅头是第二父提交。接受范围仅以本文为准。
