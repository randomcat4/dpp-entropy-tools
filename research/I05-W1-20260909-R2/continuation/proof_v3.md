# proof_v3.md — 最新完整证明索引

按下列顺序阅读：

1. `../proof/01_conditioning.md`：完整事件条件 Schur 分解与熵链。
2. `../proof/02_two_point_input.md`：实二点完整配置熵全局凹性。
3. `../proof/03_lifting_and_exterior.md`：`m x 2` 全弦提升、两坐标支撑推广、rank-two 外幂公式和上一轮障碍。
4. `../proof/04_diagonal_active_sector.md`：对角活动约化扇区任意秩定理、精确 `3+5` 例、逐条件线对角锚点判据。
5. `../proof/05_exterior_markov.md`：外幂次数、可逆特例的 Markov 交织、生成元熵导数和完整 Fisher 曲率。
6. `../proof/07_markov_adjoint_and_reversible_obstruction.md`：把第 5 项推广到一般平稳非可逆核的密度伴随，并严格排除普遍可逆外幂半群。
7. `../proof/06_quantum_measurement_obstruction.md`：相关准自由衰减不能普遍下降为经典占据配置通道。

最新冻结命题为 `frozen_statement_v3.md`，最新裁决为 `RESULT_FINAL.md`。外部对角锚点直线定理由用户指定的另一独立团队提供，本轮仅使用；来源见 `sources_continuation.md`。

作者 exact 复算入口：

```sh
python code/verify_continuation.py
python code/verify_continuation_v2.py
```

新增 continuation 仍未由新的非作者上下文独立审阅；Codex 任务以 `CODEX_VERIFICATION_TASKS_v2.md` 为准。
