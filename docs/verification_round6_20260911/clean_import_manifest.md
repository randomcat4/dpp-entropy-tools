# 干净逐文件导入说明

Status: **FINAL_WHOLE_FILE_WHITELIST**。

机器清单为同目录 `verified_import_whitelist_round6.json`。迁移器只接受三类 whole-file 条目：

- `ACCEPTED_SCOPED`：限定范围内已完成解析复核，并在承重时完成独立有限门；
- `VERIFIED_REVIEW`：FIRST/SECOND、source binding、closeout report；
- `VERIFIED_FAILURE_EVIDENCE`：复现失败、历史 provenance 缺口或非认证档案的证据，用于防止未来误提升。

清单按冻结 commit 逐文件抓取，`destination` 保留原相对路径。公共 main 上“存在”不构成 clean import 许可；未列文件一律不导入。

## 允许进入的数学对象

- PR86/97：complete rank-two atoms、fixed-pair dilute theorem、canonical square、axis/wedge、strong whole chord 与 strength family；有限证书采用 PR143 的 fresh independent 输出。
- PR94：`CHANNEL_LIFT.md` 与 `MODE_FAMILY.md`；采用 PR143 的独立 16-identity / 64-event 重建。排除被 PR95 覆盖的 `WHOLE_CHORD.md`。
- PR104：实际 parallel-criterion failure、common-diagonal sufficient criterion、double-boundary wedge；采用 PR143 的 168-event exact reconstruction。
- PR106：`p>=1/2` 中心 Fisher 四次展开、complete-event localization 与 score-moment method obstruction；不重复导入被 PR117 覆盖的 `p>=1` 定理。
- PR116：特殊 `alpha=1/10,beta=1/3` whole chord、moments、endpoint phase/Fisher dominance、uniform endpoint band、lossless cardinality/label reduction、joint identities、独立验证的 negative-`R` 与 negative-acceleration 方法点。
- PR120：只导入 `compact_unequal_middle/` 的 theorem/checker；equal-coupling 和 top-level obstruction 由 PR124 覆盖。
- PR124：pointwise resolvent method obstruction、equal-strength half-leaf、punctured small-edge theorem。
- PR130：严格 `L^infinity` parity-center `Theta(t^4)` 单元。
- PR136：全 `[1/2,3/2]` 的严格真熵率曲率证明、证书接口与 PR139 fresh 128-node 复现。

## 只保留为审阅或失败证据

- PR90、100、132、137--143 的精确 review/binding/report 文件。
- PR98 的 fresh JSON round-trip 只证明数据可解析，不导入其试验数据或 scout。
- PR112 §6 的 independent reconstruction 与 retired-checker diagnostic 只证明新重建结果并记录旧链失败；PR112 作者整包不导入。
- PR66、110、115 的处置由最终 S1 closeout 和本轮矩阵记录；三者作者源不导入。

## 明确排除

- PR66 的原 Dobrushin 证明路线；PR98 全部 archival trial inputs；PR112 的 withdrawn wide certificate 与含标签错误的整包；PR115 的旧有限 signs。
- PR94 `WHOLE_CHORD.md`、PR120 的 equal-coupling/top-level duplicate、PR106 被 PR117 覆盖部分。
- PR116 `RATIONAL_KERNEL_BERNSTEIN_ALPHA01.md`、`check_endpoint_phase.py`、未启动/未闭合 contracts、checkpoint/handoff 文件，以及任何对 compact-middle 总符号的暗示。
- 仅有作者 `PASS`、无法绑定的历史日志、已知错误 checker 输出、未完成研究方向和 novelty 声称。

PR116 Bernstein 重建可在未来形成新的追加清单；在它产出完整 generator、cleared numerator、multidegree/monomial count、5700 个 Bernstein coefficients 与最小整数核对之前，当前清单保持不变。
