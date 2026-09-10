# I05 收束轮：开放 PR 全量核验与干净导入边界

Status: **CLOSED_SCOPED / STOPPED_HANDOFF_READY**。

本轮处理了收束开始时全部 18 个开放 PR：`66,86,90,94,97,98,100,104,106,110,112,115,116,120,124,130,132,136`，并整合了本轮产生的 FIRST、SECOND 与独立有限复现记录 PR137--143。作者/审阅包整合后的公共主分支锚点为 `0360b0bd744ec9a3d05ef7699da6d56e22e185b0`；本文件所在收尾 PR 的 merge commit 是其后的记录性提交。

处置原则只有三条：

1. 原始证据来源失败，不因后来以新路线重证而被追认。例如 PR112 的旧 wide-interval 生产记录仍然无效；PR136 是新的、更强的证明链。
2. 公共主分支可以保留范围精确的历史、失败记录和非认证档案；新私有主分支只能按逐文件白名单导入，不等同于复制公共 main。
3. 方法反例与 Shannon 熵反例严格分开。本轮没有得到真实 Shannon 熵反例，也没有完成一般 moving-rank-two / compact-middle 总问题；新颖性与优先权未评估。

## 结果摘要

- `MERGED / ACCEPTED_SCOPED`：PR86、94、97、104、106、116、120、124、130、136。
- `MERGED / VERIFIED_REVIEW_OR_EVIDENCE`：PR90、100、132、137--143。
- `MERGED / ARCHIVE_ONLY_NON_CERTIFYING`：PR98；它只恢复可解析试验数据，不进入干净数学导入。
- `CLOSED_UNMERGED`：PR66、110、112、115。PR66 的原 Dobrushin 路线有适用性缺口；PR110/115 被已接受后继严格覆盖；PR112 是混合包，含不可恢复的旧证据来源和需修正文案。

独立有限复现实际覆盖了 PR136 的完整 128 节点生产、PR86/97 的 4096-box 与强 chord/family 证书、PR94 的 16 个 channel 恒等式和两个 64-event law、PR104 的 168 个完整事件 jets、PR120 的 1024-box Gershgorin 门、PR98 的三份 JSON 精确往返、PR112 §6 的新 exact reconstruction，以及 PR116 的 64-event 表、11/13 类型、moment/boundary identities、负 `R` 点和负 integrated-acceleration 点。

PR116 的冻结 `check_endpoint_phase.py` 在结构性 SymPy `==` 断言处失败；独立化简验证了底层公式。其 `R>0` Bernstein box 在作者包中没有 generator/certificate；第一轮新重建运行 600.298 秒、峰值约 1.547 GiB，尚未生成 cleared numerator。按最新运行策略，该重建已改为 **REPRODUCTION_RESUMED / UNVERIFIED**，不预设运行时长上限；它及完整 joint-kernel compact-middle 问题均不进入当前已证白名单。

详见：

- [逐 PR 处置矩阵](verification_round6_20260911/closeout_matrix.md)
- [干净逐文件导入说明](verification_round6_20260911/clean_import_manifest.md)
- `verified_import_whitelist_round6.json`：机器可读 whole-file 白名单；只有 `ACCEPTED_SCOPED`、`VERIFIED_REVIEW`、`VERIFIED_FAILURE_EVIDENCE` 三类。

公共仓库在收尾记录 PR 建立前没有遗留开放 PR。远程计算服务器不可用，本轮所有新计算均在本地、无 GPU、受控 CPU/内存条件下完成或继续；没有把“未运行”写成“失败”，也没有把超时写成数学否证。
