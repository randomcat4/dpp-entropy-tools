# proof.md — 第二轮延续证明索引

本轮证明分成六个自包含模块；前 1–3 个是第二轮已有成果，后 4–6 个是本次继续探索新增成果。按下列顺序阅读即可得到全部推导：

1. [`../proof/01_conditioning.md`](../proof/01_conditioning.md)：完整事件行列式、条件 Schur 核、熵链分解。
2. [`../proof/02_two_point_input.md`](../proof/02_two_point_input.md)：实 `2 x 2` 完整配置熵全局凹性输入。
3. [`../proof/03_lifting_and_exterior.md`](../proof/03_lifting_and_exterior.md)：`m x 2` 全弦提升、两坐标支撑推广、rank-two 外幂似然公式及旧障碍。
4. [`../proof/04_diagonal_active_sector.md`](../proof/04_diagonal_active_sector.md)：对角活动约化扇区任意秩定理、精确 `3+5` 例、逐条件线对角锚点判据。
5. [`../proof/05_exterior_markov.md`](../proof/05_exterior_markov.md)：混合判别式的外幂次数、精确 Markov 交织、生成元 LP 与完整 Fisher 熵曲率证书。
6. [`../proof/06_quantum_measurement_obstruction.md`](../proof/06_quantum_measurement_obstruction.md)：相关准自由衰减不能普遍下降为经典占据配置通道的严格有理障碍。

冻结命题见 [`frozen_statement_v2.md`](frozen_statement_v2.md)，结论和范围见 [`RESULT_CONTINUATION.md`](RESULT_CONTINUATION.md)，失败路线见 [`attempts_continuation.md`](attempts_continuation.md)。

## 逻辑依赖

新增定理 E/F 的唯一外部数学输入是用户指定、由另一独立团队证明的“过严格对角核的整条合法 Hermitian 直线配置熵凹性”。本轮不重新证明该输入；来源和采用范围见 [`sources_continuation.md`](sources_continuation.md)。条件 Schur、熵链、外幂公式、Markov 交织、生成元曲率关系和两模障碍均在上述模块中直接推导。

## 审阅状态

第二轮已有命题及本轮新增命题均已给作者级完整证明和 exact 脚本交叉检查，但本轮新增内容尚未由新的非作者 Codex/服务器上下文独立审阅。独立任务和可接受证书格式见 [`CODEX_VERIFICATION_TASKS.md`](CODEX_VERIFICATION_TASKS.md)。
