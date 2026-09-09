# proof.md — 第二轮延续的完整证明入口

本文件是稳定入口，具体证明按 `proof_v3.md` 的十项顺序阅读。当前权威范围由以下三份文件共同给出：

- `RESULT_FINAL.md`：准确裁决、主张与审阅层级；
- `frozen_statement_v3.md`：完整量词和适用范围；
- `proof_v3.md`：全部证明正文的阅读顺序。

特别注意，完整证明不仅包括后写的对角活动扇区、Markov 伴随与量子通道障碍，还包括早期 continuation 分支中的两项实质主定理：

1. `../proof/04_three_point_indefinite_rank2.md`：所有实三点不定秩二方向的全弦凹性；
2. `../proof/06_correlated_3plus3_family.md`：三点条件方向判据和两侧相关、稠密非坐标的 `3+3` rank-two 全弦族。

`../proof/05_diagonal_and_feature_routes.md` 还给出 rank-two resolvent 特征作为精确充分统计量时的 KL／互信息保持，以及压缩 Hessian 的完整 Fisher 加唯一外幂标量分解。

外部对角锚点直线定理由另一独立团队提供；本 PR 只证明其条件 Schur 提升。PR #43 的第二轮和 continuation 作者级主张尚待新上下文非作者独立审阅。
