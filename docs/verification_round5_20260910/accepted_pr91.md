# PR91 — 完整事件 Riccati 响应与 Hessian 残差门槛的限定接受

Status: **ACCEPTED_SCOPED**。冻结作者头 `c7a072ec4eea0c5b0f445bca5796873a9e234948`，十四个文件。S3 在读取 FIRST 之前完成并公开 fresh SECOND；随后比对表明两审在数学范围上实质一致。

对象固定为

`f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8`，`t in [1/2,3/2]`，

使用自然对数、完整占用事件和每个原始格点的熵率归一化。

## 接受的解析范围

- 完整事件 Schur/Riccati 校正态表示：四个真实条件权重 `g_ab=ab det(D_ab-Q)`、分支 `T_ab(Q)=E(D_ab-Q)^(-1)E^T`、正性/归一化/不变球及包含变化权重的 Wasserstein 收缩。改进后的全律收缩常数是 `4259/6480<2/3`，因而不变律唯一。
- 该校正态表示自身的分支编码、满支撑与非原子性。它不排除另一种有限 HMM 表示。
- 真实熵率恒等式 `h(f_t)=(1/2) eta_t B_t`。因两点成组，`1/2` 是回到每个原始坐标不可省略的因子。
- 真正仿射 `K_t` 下的状态一、二阶 jet，以及完整不变测度二阶响应
  `h''=(1/2) eta[B''+L''u+2L'v]`。固定态 Fisher、状态运动、加速度和嵌套响应项全部保留。
- 完整事件 Fisher 率桥梁，以及单独的值层尾界。值层界不能直接微分成导数尾界。
- 利用 `LQ=0`、`L det(Q)=0` 的仿射消去与 Hessian-only 充分门槛
  `|h''-c2/2| <= e02/2+(9/100)e12+e20/2`。它要求整个状态域和参数单元上的严格外包，不接受抽样极值。

SECOND 独立重建了展示式中的有理算术，包括收缩常数、导数常数、Hessian 门槛系数、混合门槛系数、`Cscore=32135398/894645` 与值层系数 `9/16`；该复核未导入作者代码。FIRST 的静态审查把这些展示常数留作待机器审查，两者并不冲突。

## 未认证和未完成范围

作者的 252 个完整事件运行、三个程序输出 JSON、Poisson 多项式 scouts、私有系数档案和计算合同均保持 **SOURCE_ONLY**；scouts 明确是非证书。没有从旧 PR77 固定点或 PR79 上界预算继承整区间结论，也没有启动新的 7200 秒任务。

`h''(t)<0` 在整个 `[1/2,3/2]` 上仍为 **INCOMPLETE**：尚缺无缝参数覆盖和全状态域的严格余量外包。一般 DPP 凹性、新颖性、优先权、形式化验证与其他有限 HMM 不可能性均未接受。

## 来源、双审与合并

- 作者 [总览](../../research/I05-DPP-27-riccati-response-20260910/README.md)、[证明](../../research/I05-DPP-27-riccati-response-20260910/proof.md)、[Fisher 桥梁](../../research/I05-DPP-27-riccati-response-20260910/coding_and_fisher.md)、[残差证书](../../research/I05-DPP-27-riccati-response-20260910/curvature_certificate.md) 与 [仿射消去补充](../../research/I05-DPP-27-riccati-response-20260910/post_handoff_cancellation.md)。
- 冻结 FIRST：[范围](https://github.com/randomcat4/dpp-entropy-tools/blob/5b32943874e0633f87fa67e7150b01e134a1581e/research/C1-verification-round8-20260910/units/pr91/frozen_scope.md)、[报告](https://github.com/randomcat4/dpp-entropy-tools/blob/5b32943874e0633f87fa67e7150b01e134a1581e/research/C1-verification-round8-20260910/units/pr91/review_report.md)、[静态检查](https://github.com/randomcat4/dpp-entropy-tools/blob/5b32943874e0633f87fa67e7150b01e134a1581e/research/C1-verification-round8-20260910/units/pr91/code_review.md)。
- Fresh SECOND 的 [公开完整报告](https://github.com/randomcat4/dpp-entropy-tools/pull/91#issuecomment-5613576105) 与 [两审对齐记录](https://github.com/randomcat4/dpp-entropy-tools/pull/91#issuecomment-5613705012)。

PR91 以 `9043d8e2b763c974ff430b80505bbad5e79bf6c4` 合入，精确审阅头是第二父提交。接受范围仅以本文为准。
