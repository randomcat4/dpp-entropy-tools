# 第三轮核验与整合队列

状态：RUNNING。用户已批准继续。日常认领、审阅、计算交接与恢复记录以[协调 issue #44](https://github.com/randomcat4/dpp-entropy-tools/issues/44)及各 PR/计算 issue 为准。本页记录版本边界，不构成数学认证。

| 对象 | 本轮初始冻结头 | 当前责任和状态 |
| --- | --- | --- |
| [PR41](https://github.com/randomcat4/dpp-entropy-tools/pull/41) | `6fd61dcd299417fc3a4eab3af682c03dd816b670` | 完整作者第二轮包已上传；C1 负责新强耦合三维族、完整六方向及独立块结论的首审。一般缺边三维的剩余矩阵不等式仍按作者文本保留开放。 |
| [PR43](https://github.com/randomcat4/dpp-entropy-tools/pull/43) | `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` | 完整 continuation 文件含新对角活动块、三维不定 rank-two、相关 3+3、外幂统计量和 Markov 障碍等主张；C1 按实际文件分项审查。旧 PR 摘要和五文件文字对应检查不代表本头。 |
| 重型计算交接 | 各计算 issue 单独冻结 | C2 主领。首次队列读取尚无独立计算 issue；作者任务须补齐精确对象/输入、算法、资源、严格误差、停止及检查点恢复后认领。预计网页超过 60 分钟的计算转至此流程。 |
| 依赖、范围及合并 | 每个将合版本单独核对 | C3 唯一集成人；直属有界任务做依赖映射及计算交接完整性检查，不重复 C1 首审。主数学结论首审通过后，再按风险安排独立补审。 |

版本与交接映射已经完成，见[三项有界检查及版本修正记录](verification_round3_20260909/README.md)。PR43 的统一 v3.1 头为 `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`；后继 `a7da3951a8ce02839dfa27f7205a1032d6f80f50` 仅解释旧 ZIP 不完整。二者均未改动实质证明、代码或计算输入/输出。C1 已在 [issue #46](https://github.com/randomcat4/dpp-entropy-tools/issues/46)认领首审；C2 已在 [issue #45](https://github.com/randomcat4/dpp-entropy-tools/issues/45)认领明确的三项有界计算。新任务字母不代表新的数值对象。

## 可审阅检查点与剩余审核

- PR41 首次独立审稿已通过冻结范围，报告在 [PR49 的首审记录](https://github.com/randomcat4/dpp-entropy-tools/blob/d362f216017ac0ac27876d1141fb307276379269/research/C1-verification-round3-20260909/units/pr41/review_report.md)。C1 已另启新鲜第二审；C3 已明确退出 PR41 补审，避免第三次重复审核。C2 的[独立符号报告](https://github.com/randomcat4/dpp-entropy-tools/blob/b9d1dd45a1a16f05963713178812bb3dfcae6f08/research/C2/verification3/pr41/REPORT.md)覆盖八事件、六方向导数、完整 Fisher/加速度、强耦合矩阵、独立块消去和一般缺边坐标恒等式。这些计算不替代解析主定理审核。
- PR43 的 E–H 与 I–N 仍待 C1 分项首审，之后由 C3 承担对应补审。外部输入 D 沿用既有接受，不重复计为新结果。两个 nested 作者核验器和独立 3+5/256 事件、刷新与两点机制障碍的[有界计算报告](https://github.com/randomcat4/dpp-entropy-tools/blob/1ddc775d8ceebf46ddd0335f04df282b58c1e8f7/research/C2/verification3/pr43_events/output/REPORT.md)已为 PASS；根目录 3+3 小样例由 C1 负责，C2 未重复。
- 固定非可逆 LP 的[有理流候选](https://github.com/randomcat4/dpp-entropy-tools/blob/d1c64ef49c7055df42a496d736742d4fb9aaa904/research/C2/verification3/pr43_flow/REPORT.md)含 56 条有向边变量，其中 33 条非零，自检 40 条方程残差均精确为零。当前仍是 `CANDIDATE_EXACT_SELF_CHECKED`；C2 的新鲜非作者验证者正在重建概率律与密度伴随。它不构成熵凹性结论。完整区间后续计算的端点/误差约定，以及额外扫描的有限输入仍在 issue #45 等待作者补齐。
- C3 已要求 PR43 的相关子族说明补写 `eta != 0`，以排除 `C=D0` 的对角特例；这是说明文字修正，未缩小主定理域。PR47 的公开执行元数据也在按既定边界改成可移植路径，完整私有运行记录与失败历史保留。

网页新研究分别在 [21 路熵率 issue #48](https://github.com/randomcat4/dpp-entropy-tools/issues/48)、[22 路一般缺边三维 issue #20](https://github.com/randomcat4/dpp-entropy-tools/issues/20#issuecomment-5600242506)、[23 路相关秩二块 issue #50](https://github.com/randomcat4/dpp-entropy-tools/issues/50)认领。它们是正在进行的作者研究，不是本页新增的已审定理；重计算另行冻结交接，现有固定 LP 不重复启动。

PR41 原来的“只有 CLAIM.md”描述，以及 PR43 原来的“五份可读重排”描述，均只是旧头的历史观察，已被本轮完整作者上传替代。作者新稿不自动继承 PR29/32/33/38/39/40 等旧头的接受，也不因继续使用旧目录而自动视为已经审核。

现有已接受结果仍按[成果页](research_status.md)的精确范围使用。两份新 PR 在独立审核完成前均为候选；既不宣布覆盖一般实三维或一般相关 rank-two 全弦，也不宣布其主张已被反驳。正确性、有限计算覆盖、新颖性和形式化分别记账。

每主实例最多 8 CPU 线程、32 GiB、无 GPU，计算初始一线程；最多三项直属有界子任务、无递归派生。长作业记录检查点与恢复方式，重启前检查自身作业避免重复。空缺参数在 issue 问作者，不猜；普通浮点只用于诊断。常规进度留库，私有历史库只在实质重大事件之后更新。
