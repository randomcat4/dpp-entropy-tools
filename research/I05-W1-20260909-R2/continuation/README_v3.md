# I05-W1 第二轮延续 — 最新可审核入口

总体状态：**PARTIAL / PR #43 NEW CLAIMS NOT YET INDEPENDENTLY REVIEWED**。

先前交付的 `I05-W1-20260909-R2-continuation_result.zip` 是不完整的历史快照：缺少三点、外幂充分统计、相关 `3+3` 和 v3 入口，且其中一个证明索引引用了未收录文件。按当前指令不重新打包；审阅应固定本 PR commit。

## 权威入口

1. `RESULT_FINAL.md`：一致性审计后的准确摘要，区分既有外部输入、PR #43 作者级主张和开放范围。
2. `frozen_statement_v3.md`：最新冻结命题；现已纳入三点不定秩二定理、外幂充分统计、三点条件判据和相关 `3+3` 族。
3. `proof_v3.md`：全部证明文件的完整顺序。
4. `CONSISTENCY_AUDIT.md`：说明审计前遗漏、修正范围和未改动的证明文件。
5. `verification.md`：作者 exact 复算覆盖与独立性边界。
6. `CODEX_VERIFICATION_TASKS_v2.md`：新上下文非作者审阅与服务器计算接口。
7. `attempts_continuation.md`、`sources_continuation.md`、`HANDOFF.md`：失败路线、来源边界和剩余义务。

## 当前作者级正结果

除第二轮原有的条件 Schur、`m x 2`、两坐标支撑与 rank-two 外幂公式外，continuation 还证明：

- 实三点核沿任意不定秩二方向整条合法线凹；
- rank-two resolvent 特征精确保持 KL／互信息，并给出完整压缩 Hessian；
- 三点条件方向满足“rank≤1／不定 rank2／穿过对角锚点”逐配置判据时，全局径向族凹；
- 一个两侧相关、稠密非坐标的 `3+3` rank-two 结构族整条合法区间凹；
- 对角活动约化扇区上的任意交叉秩定理及逐条件对角锚点判据；
- 一般 Markov 密度伴随交织，以及可逆半群和统一经典量子测量通道的严格障碍。

一般两侧相关、一般非坐标 rank-two 目标仍开放，但未解决范围必须排除上述已经证明的 `3+3` 族和三点条件判据。

## 作者复算

```sh
python ../code/verify_continuation.py
python code/verify_continuation.py
python code/verify_continuation_v2.py
```

三项均有仓库内保存的实际输出。复算不等于独立审阅。
