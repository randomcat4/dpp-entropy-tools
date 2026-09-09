# 第三轮核验与整合队列

状态：RUNNING。初始作者 PR41/43 与 C1/C2 核验包均已完成限定接受并合入；新收到 PR51/53/54 与计算 issue52 后继续独立核验。[协调 issue #44](https://github.com/randomcat4/dpp-entropy-tools/issues/44)及各 PR/计算 issue 保存实际认领和恢复记录。C3 为唯一 main 集成人。

| 对象 | 最终头 / 当前冻结头 | 状态与范围 |
| --- | --- | --- |
| [PR41](https://github.com/randomcat4/dpp-entropy-tools/pull/41) | `6fd61dcd299417fc3a4eab3af682c03dd816b670` | ACCEPTED_SCOPED，merge `13d6c09d5d3fcf8c19cd0b01e5d735fd8778cdb6`。两名独立解析审稿；等幅强耦合中心全六方向、独立块与二点条件熵引理。一般缺边只接受坐标/Fisher 恒等式 |
| [PR43](https://github.com/randomcat4/dpp-entropy-tools/pull/43) | `6adb231c3c1d3bf3aafc0d21132e9ad34621df89` | ACCEPTED_SCOPED，merge `de0c592c01e5b9e59e64db9df9f0d05ea1a6c01f`。E–H、D/I–N 分组双审；两处 eta 描述修正已检查。完整范围见下文 |
| [PR47](https://github.com/randomcat4/dpp-entropy-tools/pull/47) | `997c95eaf607a64d0e166dc8a08001794f59c657` | READY_SCOPED 已合，merge `6cbd76078caf1dc3444b0783409ef9af4968c265`。PR41 八事件符号、PR43 指定 256 事件/条件事件重建及独立有理有向流审核通过 |
| [PR49](https://github.com/randomcat4/dpp-entropy-tools/pull/49) | `b3816871965782378da5d4b559992176a66b6c26` | 审阅记录已合，merge `580efb43568030013e0a2eac318bbe0e8db4051e`。三项首审和三项新鲜第二审均结束；旧 H 文字缺口由 PR43 的明确两行增量关闭 |
| [PR51](https://github.com/randomcat4/dpp-entropy-tools/pull/51) | 最终 `184535756f5ed92f2f5c47804bdc8466a7d15041` | ACCEPTED_SCOPED，merge `ed10e23134d5dd8350f1cd9636204143c62ebc40`。原定理与续稿分别双审；[完整范围和证据](verification_round3_20260909/accepted_pr51.md)。一般 Schur 与径向 M 正性仍开放 |
| [PR53](https://github.com/randomcat4/dpp-entropy-tools/pull/53) | 原EW源`73cdbd09`；说明修订`ebecc412467939591e018a295a18c49a0a341ce9` | 原桥接与FR双审通过；EW首审与独立第二审均通过。三文件说明修订的FR/EW第二审增量均已闭合，原首审人增量报告待归档。全合法区间仍开放；[精确版本边界](verification_round3_20260909/pr53_version_boundaries.md) |
| [PR54](https://github.com/randomcat4/dpp-entropy-tools/pull/54) | 最终 `d5c55447a0f7377dae085b8074f557e4f673b5a4` | ACCEPTED_SCOPED，merge `24ae88bf14b540b66490e3266a75849e6e258bad`。原稿与两组附录分别双审；五处明确条件/措辞修复全部独立闭合。[完整范围与证据](verification_round3_20260909/accepted_pr54.md) |
| [计算 #52 / PR55](https://github.com/randomcat4/dpp-entropy-tools/pull/55) | 最终`12798ccc1afdff007a2deec3f49baf26755d1a93` | PARTIAL_ARCHIVE已合，merge`43d8fd24af560afaa34b1ec8e7c7dd053e691603`。代数与种子限定接受；r=0证书首审INCOMPLETE、全域符号OPEN，全部算术已停止。[档案与缺口](verification_round3_20260909/archived_pr55.md) |

## 已接受结论与证据

[成果页](research_status.md)与[路线台账](route_ledger.md)列当前可使用的范围；[PR43 的完整量词、双审、非可逆固定生成元与版本修正](verification_round3_20260909/accepted_pr43.md)区分正面定理、条件框架和机制障碍。外部对角输入 D 不重复计数。所有结果均使用完整配置概率，数值检查不替代全参数证明；新颖性和形式化另行记账。

C1 已结束初始三项首审和三项新鲜第二审；C2 已结束初始三项计算及后续新鲜流证书审核。C3 根据实际在行任务撤回了先前 PR41/43 的补审预留，没有启动第三次重复审稿。当前新工作按上表分项认领。PR51 原定理的两名审稿与续稿审稿分别记账；C1 已明确不启动 PR53/54 第二审，C3 在对应首审通过后接续，新增附录不继承原稿审定。

PR43 初始数值头 `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` 到统一 v3.1 `7bd5962bbb2020ce47fbe286adda7dfe02f9645d` 只改十二份声明/索引/任务文本；后继 a7da3951 只说明旧 ZIP 不完整；最终 6adb231c 在两处相关性描述补 eta!=0。旧输入中的 reversible 字段不适用于当前非可逆 LP，实际计算使用 PR47 的有向输入与右端位对应坐标1的明确约定。详见[初期依赖与交接检查](verification_round3_20260909/README.md)，它们是映射记录，不是额外审稿人数。

## 尚待明确的计算交接

[issue #45](https://github.com/randomcat4/dpp-entropy-tools/issues/45)的单个固定 LP 已有独立接受的有理可行流。其后续完整合法区间熵耗散曲率任务仍缺明确的端点处理与 `1e-20` 误差语义；额外扫描还需有限候选/搜索盒与预算。C2 已问作者，未通过猜测启动后续作业。生成元存在不等于曲率条件成立。

网页研究分别在 [21 路熵率 issue #48](https://github.com/randomcat4/dpp-entropy-tools/issues/48)、[22 路缺边三维 issue #20](https://github.com/randomcat4/dpp-entropy-tools/issues/20)、[23 路相关秩二块 issue #50](https://github.com/randomcat4/dpp-entropy-tools/issues/50)。作者的继续研究与本页的已审接受分开；重计算另行冻结交接，现有固定 LP 不重复启动。PR51 的私有作者代码未被获取或搬入公开库；独立自编精确检查已经公开。PR56 保存 C1 的 PR53/54 首审和后续修复审定，不覆盖 C3 另审的新增附录。

每主实例最多 8 CPU 线程、32 GiB、无 GPU，计算初始一线程；最多三项直属有界子任务、无递归派生。长作业保存检查点与恢复方式；只操作自身目录和进程。常规进度留公开库，私有历史库只在实质重大事件后更新。空 CI 列表不记作通过。

[后继完整审稿档案](verification_round3_20260909/followon/README.md)保存PR53原稿第二审、PR54两组附录的独立首审/第二审和精确修复闭合。C1首审与原稿修复记录在[PR56](https://github.com/randomcat4/dpp-entropy-tools/pull/56)，新增PR53定理另行冻结，不覆盖滚动新稿。
