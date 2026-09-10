# PR81 d995 SECOND frozen scope

## 审阅身份与边界

独立 SECOND 审阅；非作者；未生成子代理。本轮只审阅 PR81 d995 单元的五份纯作者来源及绑定，不改写任何 PR77/PR79/PR89 报告。

## 允许输入

唯一允许目录：

`docs/verification_round4_20260909/pr81_d995_second`

实际读取：

1. `input_binding.json`
2. `input/coupled_gram_fixed_shape.md`
3. `input/proof.md`
4. `input/shared_corner_cell_theorem.md`
5. `pr70_source/proof.md`
6. `pr70_source/thinning_bridge.md`

未读取 sibling `pr81_second`、FIRST、其他 SECOND、C3 裁决、公开评论、later live、私有排除目录或 `[excluded private directory]`。

## 绑定与哈希

`input_binding.json` 绑定 PR81 head `d99550bfd9eee623ec80edbca1da17ff0ddbe4bf`，previous head `92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac`。五个源文件均已用本机 SHA-256 和行数核对：0 缺失，0 delivered SHA 不匹配，0 行数不匹配。

三份文件的 `original_sha256` 与 `delivered_sha256` 不同，原因是绑定中声明的等行数删除非数学 review-history/status 文字：

- `input/proof.md`
- `input/shared_corner_cell_theorem.md`
- `pr70_source/proof.md`

本报告严格区分 `original_git_blob`/`original_sha256` 与本地审阅包的 `delivered_sha256`，不混称二者。完整机器哈希写入 `source_binding.json`。

## 审阅类型

只做静态数学证明、来源与哈希审阅。未运行或导入作者/独立数学脚本；未做 determinant/log/entropy/interval/Gram/finite arithmetic；未编译；未提出新 C2 合约。

## 审阅目标

重点检查：

- 完整八事件与六个真实物理方向是否保留；
- one-edge lemma 的二阶导数、弦不等式与 Gram 论证；
- shared-corner 四角单元分解是否保留共同角点而非独立标量范围；
- `J < 12AB` 是否足以推出全六方向严格正的 `Q=-H''`；
- `A=1/4, B=4/9` 在完整合法 `0<q<11/36` 区间内是否合法并满足条件；
- strictness/coercivity 是否由简单解析证明闭合；
- 大有理数 minors、作者 checker PASS、诊断值是否被错误当作独立证据。

## 范围排除

Novelty `NOT_ASSESSED`。Formal verification `NOT_PERFORMED`。作者 checker、诊断搜索、大有理数 relaxed witnesses 与 Sylvester minors 不作为独立验算证据接受；只作为作者附带材料记录。一般 half-leaf arrows、一般 missing-edge arrows、一般实三点 concavity 仍在本轮范围外。
