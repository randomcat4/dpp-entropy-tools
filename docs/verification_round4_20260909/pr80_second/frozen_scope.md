# PR80 独立 SECOND 冻结范围

审查对象：PR80 严格冻结 head `1a322ace19fd8ccc679f849780850dde31deb3d2`。本轮是新的独立 SECOND，不继承任何 FIRST、其他 SECOND、C3 意见、公开评论或后续 live 版本结论。

## 允许材料

只读以下材料：

- `input/` 八个作者文件；
- `pr58_source/` 两个纯数学来源文件；
- `input_binding.json`。

未读取 FIRST、其他 SECOND、C3 意见、公开评论、后续 live 版本或任何禁止私有目录。作者脚本与作者摘要只作 `SOURCE_ONLY` 静态材料；未运行、未导入，也未做 determinant/log/entropy/interval 复算。

## 绑定核验

`input_binding.json` 声明 PR80 head `1a322ace19fd8ccc679f849780850dde31deb3d2`，并列出 10 个文件：`input/` 8 个、`pr58_source/` 2 个。实际文件数一致，全部 SHA-256 匹配。

绑定文件自身 SHA-256：

`025522e3dd378287fa289274f8734285638628932e8cb43c610d4ad932179a64`

`pr58_source/` 两个文件的 head 为 `89aa874c24dd5a3ea98f8474826392560b1d0397`。它们在本轮只作为 PR58 数学背景来源，不自动认证 PR80 的新 pair/fiber 数字诊断。

## 固定量词

本审查只处理 PR80 文本中声明的严格 rank-two cross-block 路径：

`K(t)=[[A,tB],[tB^T,C]]`，`s=t^2>0`，

以及 complete-law likelihood

`q=1+u=1-sa+s^2b`，`y=s^2b`。

所有全局 curvature 结论只在文本显式给出的 sufficient hypotheses 下成立。`s=9/10` fixture 的具体 pair counts、signs、lower bounds、global equality 与 PR58 fixture equality 在本包中没有 C2/raw 独立证书。

## Gate 总表

| Gate | Verdict | 范围说明 |
|---|---:|---|
| 输入 Git/SHA 绑定 | CORRECT | 10 个列名文件全部存在并匹配 SHA-256。 |
| exact conditional paired identity | CORRECT | 在已声明的 complete-law identity 与 fiber 条件 `E u=E y=0` 下，pair identity 代数推导闭合。 |
| Fisher/acceleration/mixed 项保留 | CORRECT | 文本保留 `Phi`、`4y^2/q`、`y psi` 与 `Delta u Delta y` mixed 项，无事件删除。 |
| free pairwise PSD 过松路线反驳 | CORRECT | `q'=q` 时 PSD 条件要求 `(5+4/q)^2<=8`，不可能。 |
| ratio-cone sufficient theorem | CORRECT | 是充分条件定理；只在每个实际 DPP pair 满足 `F>=0` 时推出 `H''<=0`。 |
| ratio-cone 覆盖 `s=9/10` fixture | INCOMPLETE | 作者后续诊断反而报告该机制在 75/66 个 pair 上失败；这些 counts/signs 无 C2 证书。 |
| diagonal strictness witness | CORRECT | 在 cone hypotheses 下，正质量非零 one-copy atom 的 diagonal pair 给出严格正贡献。 |
| offdiagonal reserve strictness | CORRECT | Cauchy slack identity 给出非负 reserve；列出的 offdiagonal 条件是充分条件。 |
| square completion 与 coefficient class | CORRECT | 恒等式和事件级充分符号条件闭合，但不覆盖 `s=9/10` fixture 的全部事件。 |
| reference fiber weights | CORRECT | 使用 product-reference `p_C` 或 `p_A`，不是 q-reweighted conditional law。 |
| fiber window/moment theorem | CORRECT | 从 `lambda` 单调性和 `z lambda >= c z-delta|z|` 得到 fiber lower bound。 |
| `s=9/10` pair counts/signs/lower bounds/fixture equality | INCOMPLETE | 本包无 C2/raw 独立证书；README 明确要求独立绑定。 |
| 作者脚本与 PASS 摘要 | SOURCE_ONLY | 未运行；README 说明输出是编辑摘要，不是 literal raw stdout。 |
| general dense correlated whole chord | INCOMPLETE | 作者文本也保持开放。 |
| novelty | NOT_ASSESSED | 未评估。 |
| formal proof | NOT_PERFORMED | 未做形式化。 |

## 核心边界

PR80 的符号恒等式和充分条件可以在其量词范围内静态接受为作者证明层面的 `CORRECT`。但所有具体新 finite arithmetic 事实，包括 `75/66` bad pair counts、四个 negative event signs、16 个 fiber positivity lower bounds、window/moment lower bounds、global equality 和代码矩阵等于目标 PR58 fixture，均仍为 `INCOMPLETE` 或 `SOURCE_ONLY`。不能因作者自报 `PASS` 升级。
