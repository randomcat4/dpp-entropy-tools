# PR57：r=0 精确证书链的限定接受

状态：**ACCEPTED_SCOPED**。作者候选为 `ba890f6294272849fa0a20d5c7e0e9f97d171d51`，最终交付为 `169cda3daf8054b53ea5622a0cb14b35a097f2e3`。这是新合同下补齐的结果；[PR55 部分档案](../verification_round3_20260909/archived_pr55.md)及其旧 FIRST INCOMPLETE 保留为历史记录。

## accepted_scope

仅在 `r=0`、`|mu|<1`、`|nu|<1`、`0<u<1` 上，显示的四维 Schur 矩阵 `Rstar` 严格正定。使用已经接受的六固定物理方向归约和正定消元块，得到原矩阵 `M` 对所有六个固定方向坐标正定。

所接受的链条是：从显示公式重新构造 Rstar，计算精确行列式并提取整数 P，再经正交域代换得到整数 Q；Q 的全盒系数给出 P 严格为正及行列式处处非零；结合一个精确正定种子和连通开域上的恒定惯性，最后作 Schur 与同余提升。正行列式本身没有被当作正定性的充分条件，Bareiss 中间主元也没有被假设在整个参数域不为零。

行列式恒等式为

```text
det Rstar = (1-mu^2)^2 (1-nu^2)^2 P / [2(1-u^4)^5].
```

代换为 `mu=(X-1)/(X+1)`、`nu=(Y-1)/(Y+1)`、`u=U/(1+U)`，其中 `X,Y,U>0`。P 有 26 项、次数盒 `(4,4,16)`；Q 的完整 425 个位置中 389 个为正、36 个为零，最小正系数 192、最大 99220032。归档 P/Q 仅在重建后用于逐项比较。

## 独立核验与执行边界

- [新的非作者 FIRST 全文](../../research/C2/r0_independent52/review_first/REVIEW.md)：独立编写检查器，从显示矩阵重建置换/Berkowitz 行列式、P、两种 Q 变换与全部系数，再核验种子和域内推论。其实际运行证据保留在[结果](../../research/C2/r0_independent52/review_first/run01/RESULT.json)中。
- [新上下文 SECOND 全文](pr57_second/review_report.md)：未接触 FIRST 报告、代码、输出或结论；独立审查显示公式到实现的逐行对应、显式证书和分母—非零—种子—惯性—Schur 论证。核对了记录的完整系数盒，但没有再启动符号算术。这一范围与 FIRST 的独立重算明确区分。
- [SECOND 冻结范围](pr57_second/frozen_scope.md)、[源文件绑定](pr57_second/source_binding.json)和[候选到最终包的对应](pr57_source_delta.json)：作者数学证明、代码、冻结输入和数学产物均未变；修改仅为 README、STATUS 和执行台账，并新增 FIRST 证据与交接材料。C3 验证 93 个最终包 blob、解析 59 份 JSON；这些是来源与包装检查，不替代数学审核。

作者与 FIRST 算术分别耗时 9.707 秒和 9.499 秒，均在同一个 `13:32:37–14:17:37 UTC` 有界窗口内完成，单进程、单 CPU/线程、16 GiB、无 GPU。旧失败记录、FIRST 的文字匹配诊断和更短内部截止均未删除；[执行台账](../../research/C2/r0_independent52/execution/LEDGER.md)解释其实际含义。C3 未延长该窗口。

## excluded_scope

不接受全 r、Lambda 非零、一般实核熵凹性、熵反例、新颖性或 Lean 认证。本单元不重新审定已接受的八事件到 Schur 的归约，也不把后继 PR60 的新作者头自动纳入。有限配置 Shannon 熵、真实熵率和辅助矩阵正性仍分别记账。
