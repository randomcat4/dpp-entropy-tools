# PR88 — 坐标支撑 rank-two 与固定线边界渐近的限定接受

Status: **ACCEPTED_SCOPED**。冻结作者头 `6c8ad2eaedcc93c7dfc5417b2d71b4e826d9be5c`，六个文件。完整 FIRST 与隔离 SECOND 对解析范围一致；既有 C3 来源闭合已把报告绑定到原始 Git 对象。源码作为混合状态研究档案进入 main，不提升其中未获独立认证的有限证据。

## 接受的解析范围

- 完整事件的 rank-two Cauchy–Binet/Möbius 展开，包括全部混合面积、三重项和四重项。
- 三个实际观察坐标上的不定 rank-two 机制，保留完整 Fisher、加速度及全部物理方向。
- 共同稠密模态在移动方向支撑于三个实际观察坐标时的精确条件分解；由此得到的坐标支撑全弦严格凹定理允许外部任意相关。这里不能用谱基旋转替代观察坐标假设。
- 每条固定仿射合法线的多重边界渐近 `H''(h)=-beta/h+O(1+|log h|)`，以及由其得到的固定线端点邻域。该邻域不对变化角度或退化族作统一承诺。
- 共同 bit-flip 连续性与 rank-one 严格性机制；始终使用真实仿射中点和完整配置熵，计数生成行列式只用于质量出现，不替代配置熵。

## 未认证和未完成范围

下列内容保持 **SOURCE_ONLY / PENDING INDEPENDENT COMPUTATION**：方法夹具及提升后的符号、六点有限值、64 个多环原子四次式、`beta=6784/16875`、条件障碍矩阵/比值、三个区间探针、`verify.py` 与 `certificate_compact.json`。脚本未由本批执行；JSON 不是独立证书。

任意移动 rank-two 中点、一般实核熵猜想以及多环紧致中段仍为 **INCOMPLETE**。辅助方法桥梁的失败不是熵反例。没有接受新颖性、优先权或形式化验证结论，也没有新增计算预算。

## 来源、双审与合并

- 作者 [总览](../../research/N4/I05_20260910/README.md)、[主证明](../../research/N4/I05_20260910/proof.md) 与 [续稿](../../research/N4/I05_20260910/continuation.md)。
- FIRST [范围](../verification_round4_20260909/pr88_final_first/frozen_scope.md)、[报告](../verification_round4_20260909/pr88_final_first/review_report.md)、[静态检查](../verification_round4_20260909/pr88_final_first/code_review.md)。
- 隔离 SECOND [范围](../verification_round4_20260909/pr88_second/frozen_scope.md)、[报告](../verification_round4_20260909/pr88_second/review_report.md)、[静态检查](../verification_round4_20260909/pr88_second/code_review.md) 及 [来源闭合](../verification_round4_20260909/pr88_second/c3_provenance_closure.md)。
- [合入前最终检查点](../verification_round4_20260909/pr88_final_checkpoint.md)。

PR88 以 `097c4db1e17c176d8b75e9ad5054f5beff9e0e06` 合入，精确审阅头是第二父提交。接受范围仅以本文为准。
