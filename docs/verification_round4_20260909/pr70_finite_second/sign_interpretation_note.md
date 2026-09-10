# P5/P6 符号解释澄清

本说明只澄清 `review_report.md` 第 9 节末句的措辞边界。不修改原报告，也不加入任何新计算。

## 澄清后的符号表述

对固定 PR70 对象 `K,D,tau=1/100000`，下面两项都具有完整 Shannon entropy 沿该物理方向的凹性方向符号：

- P5 记录 `-H_full'' > 0`，因此在该固定中心和方向上 `H_full'' < 0`。
- P6 记录完整事件 midpoint Jensen 量
  `[H(K-tau D)+H(K+tau D)]/2 - H(K) < 0`
  对该固定合法三点严格为负。

因此，P5 和 P6 是一致的固定对象凹性方向证据。原句“不是 negative full-entropy Hessian certificate”的意图只是防止把 P6 重新表述为凹性反例或全局 Hessian 定理；它不应被理解为否认固定 P5 证书 `-H_full'' > 0`。

## 边界

这些符号不提供 entropy concavity counterexample，也不提供全局 Hessian 符号定理、全局 full-entropy determinant 结论或三维 Shannon concavity 证明。它们只认证 P5/P6 gates 已记录的固定对象/固定方向证据。
