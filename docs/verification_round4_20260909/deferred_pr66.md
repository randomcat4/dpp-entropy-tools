# PR66：外部解析响应定理的适用性缺口

状态：**NEEDS_FIX / CRITICAL_GAPS，未接受最终定理**。作者头 `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` 未变；原 FIRST 初次缺少全文的历史保留。随后取得并核对 Dobrushin 原论文全文，发现问题在定理适用条件。没有启动 SECOND，也没有把最终 DPP 结论判为假。

稿件构造的平移不变区间相互作用具有多项式衰减和有限一阶矩；尚未证明它属于所引定理的相互作用空间。原论文的 A1 分支要求带支撑基数指数权重的 D2 条件，现有多项式上界不足以证明该条件。A2 分支则要求 C2 零状态条件：任一支撑坐标落在指定状态集时该相互作用项即为零。稿件未给出保范数的这类表示。一般子集展开可能付出指数代价，因此不能省略这一步。

需补齐可控的零状态分解、更强的适用范数估计，或一条确实涵盖其一般块函数类及复双参数族 `lambda U_s` 的原始响应定理。内部事件逆、影响、相互作用构造、平衡律、奇偶性和后续条件推导的审查与这一缺口分开记录；有限一阶矩的估计本身不证明响应解析性。

- [原始 FIRST 报告](../../research/C1-verification-round6-20260910/units/pr66/review_report.md)。
- [全文适用性后续报告](../../research/C1-verification-round6-20260910/units/pr66/import_closure_review.md)及[来源绑定](../../research/C1-verification-round6-20260910/units/pr66/PRIMARY_SOURCE_BINDING.json)。
- [Dobrushin 原始论文](https://www.mathnet.ru/eng/sm3631)：印刷页14–15的条件/类，17–18页的定理1–2，24–25页的 Banach 空间表述。完整PDF的 SHA256 为 `91d79d372cf4b574db400e06ad081d38eef793f576bb94d40c3dbe74a411c1ef`；PDF、全文转写和渲染均未重新公开。

这些是具体引用修复义务，不是新定理路线、数值任务或一般实 DPP 熵凹性反例。
