# PR70 固定有限对象 SECOND 审查范围

审查角色：PR70 固定有限单元的独立 SECOND 验证者。本报告不继承 FIRST、历史 SECOND 或 C3 裁定结论。

## 冻结来源

- 作者冻结 head：`f7be60759fd4d65184803b6585965dc7e5ccd624`。
- 作者输入绑定：`input_binding.json`，列出 8 个文件，实际 8 个文件，全部 SHA-256 匹配。
- C2 原始计算 head：`611d5f70e8bb70237755ca4fdbe8ab14c8b715c1`。
- C2 executable/preparation head：`29d4d77d7dba65de933d196a89b4db2616234991`。
- C2 机器输入绑定：`machine_input_binding.json`，列出 74 个文件，实际 74 个文件，全部 SHA-256 匹配。
- 绑定文件 SHA-256：
  - `input_binding.json`: `1c3903cdb653213d178150cf124dc905e580c7ac5b5c9aeac312ebeb01a8fe47`
  - `machine_input_binding.json`: `656ccb1ec498507b033de39f882f0714f832d4d00cc67b66350ad9a66c9e2632`

## 审查边界

本轮只读：

- `input/` 冻结作者文件。
- `machine_input/implementation/`、`machine_input/inputs/`、`machine_input/outputs/`、`machine_input/execution/`。
- 包根目录下两份绑定文件。

未读取 C1 FIRST、历史 SECOND、C3 裁定、machine topREADME、machine_notes、FINAL_HANDOFF 或 `[excluded private directory]` 下任何路径。未运行作者 checker、C2 checker、行列式/log/熵复算或任何新算术验证。只使用 JSON 解析、SHA-256 核验、源码行检查和结构化字段摘取。

## 固定数学对象

本 SECOND 审查仅接受 `post_checkpoint.md` 第 1 节的固定 PR70 对象：

- `K=[[1/25,0,2/15],[0,3/4,1/4],[2/15,1/4,18/25]]`。
- `D=[[1,-7/5,11/9],[-7/5,1/5,0],[11/9,0,-1/7]]`。
- `tau=1/100000`。
- 真实导数参数：物理线 `K+tD` 中的 `t`。
- 完整事件顺序：作者写法 `0,1,2,12,3,13,23,123`；C2 二进制 mask 顺序 `[0,1,2,3,4,5,6,7]`，选中/互补条件位 mask 为 `4`。
- 对数：自然对数。
- C2 对数包围：固定 `N=80` 的 atanh 归一化。

## gate 裁定总表

| Gate | Verdict | 绑定证据 |
|---|---:|---|
| 来源/文件绑定 | CORRECT | 两份绑定清单均与实际交付文件和声明 head 匹配。 |
| 固定对象与输入回显 | CORRECT | `object.json` 与作者 P1/P6 对象一致，并在 `input_echo.json` 中原样回显。 |
| 可执行/输入文件与 prep 一致性 | CORRECT | 参与计算的已交付 prep 文件全部匹配 `PREPARATION_SHA256.json`。两个 prep 顶层说明文件未纳入本公开包，且未读取。 |
| 单次执行封套 | CORRECT | 600 秒窗口 `2026-09-10T02:10:08Z` 到 `02:20:08Z`；`02:10:10Z` 退出；`02:10:38Z` 检查 PID 缺席；无 repair、无 retry。 |
| 完整八事件 jets | CORRECT | Mobius 与 signed determinant 双构造一致；8 行 `(p,p',p'')` 字面匹配作者 P2 表。 |
| 叶边缘与归一化 | CORRECT | 四个 marginal 多项式与独立二点律一致；总多项式与 jet 归一化通过。 |
| 六组 Sylvester 正定性与三点事件 | CORRECT | `K/I-K` 的三点端点/中心六组三阶 leading minors 全部为正并字面匹配；三点事件律归一且原子为正。 |
| P2/P3 quotient 与精确分数 | CORRECT | 8 个 P3 quotient 行检查通过；`Phi0`、`Phi1`、`Phi_pair` 精确分数匹配；`Phi_pair` 字面区间包含且严格为负。 |
| P5 side/conditional/full 曲率 | CORRECT | side 导数双形式、保留的 `P''` 项、full/leaf Fisher 与 acceleration、`-Hconditional''=G0''+G1''` 结构恒等式均通过；四个 P5 区间为正且字面包含。 |
| N80 log 包围 gates | CORRECT | 28 个正 log argument、`log2` 的 `w=1/3`、负乘数端点反转、宽度 gate、宽符号 gate 与字面包含 gate 均存在。 |
| P6 完整 Shannon Jensen 符号 | CORRECT | 完整熵 Jensen 区间严格为负且字面包含；这是局部凹性 witness，不是熵反例。 |
| 全局 one-sided / full entropy / general concavity 命题 | INCOMPLETE | 超出固定有限对象范围；不作全局 `G1''>=0`、full entropy determinant 或三维凹性裁定。 |
| Novelty | NOT_ASSESSED | 未做新颖性或先行工作裁定。 |
| Formal proof | NOT_PERFORMED | 未做 Lean/证明助手形式化。 |

## 解释边界

固定 C2 证据支持这个单一有理对象上的作者范围 P2/P5/P6。它不证明全局 one-sided 不等式、全局 conditional entropy 符号、full entropy determinant 目标或三维 Shannon 凹性定理。P2 的 paired-resolvent 负曲率是辅助方法 obstruction；不是 entropy counterexample。P6 的 Jensen 值对完整 Shannon entropy 呈凹性符号。
