# CONSISTENCY_AUDIT.md

审计对象：PR #43 在 commit `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` 的完整变更树。  
审计性质：作者同会话的文档一致性核对，不是非作者数学审阅。

## 1. 发现的不一致

证明树中已经存在以下完整文件：

- `../proof/04_three_point_indefinite_rank2.md`；
- `../proof/05_diagonal_and_feature_routes.md`；
- `../proof/06_correlated_3plus3_family.md`。

上级根目录的 `RESULT_CONTINUATION.md`、`frozen_statement_continuation.md`、`README_CONTINUATION.md`、`CODEX_TASKS.md` 与 `verification_continuation.md` 也已经记录这些主张。

但是后写的 `continuation/RESULT_FINAL.md`、`frozen_statement_v3.md`、`proof_v3.md`、`README_v3.md` 和 PR 正文只摘要了活动扇区、对角锚点、Markov／可逆障碍与量子障碍，遗漏了：

1. 所有实三点不定秩二方向的全弦凹性；
2. rank-two resolvent 特征的 KL／互信息充分统计及压缩 Hessian；
3. 三点条件方向的三分判据；
4. 两侧相关、稠密非坐标的 `3+3` rank-two 结构族及精确合法半径。

此外，旧 `HANDOFF.md` 与 `attempts_continuation.md` 仍把“可逆导通量”作为存活任务，和后续 `-125/78` 可逆障碍矛盾。旧 `CODEX_VERIFICATION_TASKS_v2.md` 也遗漏了三点与 `3+3` 两份证明的独立审阅。

## 2. 本次修正

本提交只做范围整合和审阅接口修正：

- 更新 `RESULT_FINAL.md` 与 `frozen_statement_v3.md`，纳入上述四项主张；
- 更新 `proof.md`、`proof_v3.md`、`README_v3.md`，给出无遗漏阅读顺序；
- 更新 `verification.md`，汇总两条作者 exact 复算链及曾修正的诊断常数；
- 更新 `CODEX_VERIFICATION_TASKS_v2.md`，要求新上下文逐项审阅三点、充分统计和 `3+3` 结果；
- 更新 `HANDOFF.md` 与 `attempts_continuation.md`，删除已经失效的可逆 LP 目标，仅保留非可逆密度伴随；
- 更新 `sources_continuation.md`，明确哪些步骤自包含、哪些是外部输入；
- 将 `RESULT_CONTINUATION.md` 标记为历史快照。

## 3. 先前本地归档的状态

另行检查了先前交付的 `I05-W1-20260909-R2-continuation_result.zip`。该归档有 21 个条目，但属于较早快照：

- 根 `RESULT.md`／`frozen_statement.md` 只覆盖第二轮原 `m x 2` 等结果；
- 归档中没有 `04_three_point_indefinite_rank2.md`、`05_diagonal_and_feature_routes.md`、`06_correlated_3plus3_family.md`、`RESULT_FINAL.md` 或 `frozen_statement_v3.md`；
- 包内 `continuation/proof.md` 指向 `proof_continuation.md`，但该文件不在归档中。

因此该 ZIP 不是当前完整、自包含的最终审阅对象。按用户本次明确要求，没有重新打包；PR #43 的冻结 commit 及本目录权威入口是当前完整来源。

## 4. 没有做的事情

- 没有修改 `../proof/04_three_point_indefinite_rank2.md`、`05_diagonal_and_feature_routes.md`、`06_correlated_3plus3_family.md` 的数学正文；
- 没有新增一个超出这些证明文件的定理；
- 没有把作者复算升级成非作者独立审阅；
- 没有修改 `main`，没有合并 PR；
- 没有重新打包 ZIP。

## 5. 审计后的权威入口

- `README_v3.md`
- `RESULT_FINAL.md`
- `frozen_statement_v3.md`
- `proof_v3.md`
- `verification.md`
- `CODEX_VERIFICATION_TASKS_v2.md`

总体裁决保持 `PARTIAL`。一般两侧相关、一般非坐标 rank-two 情形仍开放，但未解决范围现在准确排除了已经证明的三点判据和相关 `3+3` 结构族。
