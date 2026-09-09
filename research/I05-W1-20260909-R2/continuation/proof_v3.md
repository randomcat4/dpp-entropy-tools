# proof_v3.md — 一致性审计后的完整证明索引

以下顺序覆盖 PR #43 中全部作者级主张；没有任何主定理只存在于摘要而没有对应证明正文。

1. `../proof/01_conditioning.md`：完整事件行列式、条件 Schur 核与熵链。
2. `../proof/02_two_point_input.md`：实 `2 x 2` 完整配置熵全局凹性输入。
3. `../proof/03_lifting_and_exterior.md`：`m x 2` 全弦提升、两坐标支撑推广、rank-two 外幂似然公式与上一轮障碍。
4. `../proof/04_three_point_indefinite_rank2.md`：实三点核沿任意不定秩二方向的整条合法线凹性；条件四循环分解与完整 Fisher。
5. `../proof/05_diagonal_and_feature_routes.md`：一侧对角任意交叉秩定理、外幂充分统计的 KL／互信息精确保持、压缩三参数 Hessian 与外幂标量。
6. `../proof/06_correlated_3plus3_family.md`：三点条件方向三分判据，以及两侧相关、稠密非坐标 `3+3` rank-two 结构族和精确合法半径。
7. `../proof/04_diagonal_active_sector.md`：对角活动约化扇区上的任意秩定理、精确 `3+5` 例和逐条件线对角锚点判据。
8. `../proof/05_exterior_markov.md`：外幂次数、Markov 交织、生成元熵导数和完整 Fisher 曲率接口；其中可逆性的范围由第 9 项修正。
9. `../proof/07_markov_adjoint_and_reversible_obstruction.md`：一般平稳非可逆核的密度伴随表述，以及普遍可逆外幂半群的严格相关二点障碍。
10. `../proof/06_quantum_measurement_obstruction.md`：相关准自由衰减不能普遍下降为经典占据配置通道。

最新冻结命题为 `frozen_statement_v3.md`，最新裁决为 `RESULT_FINAL.md`。`RESULT_CONTINUATION.md` 与 `frozen_statement_v2.md` 仅是中间历史快照，不再作为当前范围依据。

外部输入只有用户指定的对角锚点直线定理；本 PR 不重做其证明或独立审阅。其他结论都在上述文件中给出作者级推导。

作者 exact 复算入口：

```sh
python ../code/verify_continuation.py
python code/verify_continuation.py
python code/verify_continuation_v2.py
```

第一项覆盖三点四循环、相关 `3+3` 族、八个条件方向和精确合法半径；后两项覆盖活动扇区、外幂刷新、Markov／量子障碍。它们均为同会话交叉复算，不是非作者审阅。

独立审阅以 `CODEX_VERIFICATION_TASKS_v2.md` 为准，并必须单独裁决第 4–6 项，而不能只审阅第 7–10 项。
