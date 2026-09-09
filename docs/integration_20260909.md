# 2026-09-09 main 整合记录

## 后继整合批次 3

| PR | 冻结头 | merge commit | 审阅依据 |
| --- | --- | --- | --- |
| [22](https://github.com/randomcat4/dpp-entropy-tools/pull/22) | `60645b4ea9e3f3a79d842b6fe039a33f9daaf7df` | `3833398ad1894bd2163551679618b33410ccb435` | [非作者归档审定](verification_20260909/base_prs.md)与对应原始固定证书复核 |
| [23](https://github.com/randomcat4/dpp-entropy-tools/pull/23) | `ffc8a7b855a9866306b3a6c22a5b4ecbc4be0d90` | `3a800bd6be13a1e5fe15b51245f38a4d6673cfe4` | 同上，固定面/rank-three 辅助结果 |
| [31](https://github.com/randomcat4/dpp-entropy-tools/pull/31) | `178eca3db82cdce495146eb8e1f16dece99f06f5` | `fe171d10de275eb9e4bb65de05a61bc709c59e33` | 同上，C2 原作者未自批；先合23，再改基main并检查差异仅 research/C2 |
| [35](https://github.com/randomcat4/dpp-entropy-tools/pull/35) | `83d69754dc46e9337a90dc784e128de72664ee72` | `04f29ff997d80fad70f35d4fb34c4605e0456c37` | [W3 新非作者审阅](../research/C2/verification2/w3/REVIEW.md)、实际源和服务器精确证书 |
| [30](https://github.com/randomcat4/dpp-entropy-tools/pull/30) | `94d67909bf8c1ea06da6350cf7907d6665cb166a` | `85bf8d2d55c285fb7f68455984b2e321892e7933` | [新非作者审阅公开副本](verification_20260909/pr30_fresh.md)，解析族与独立服务器 cert60 核族严格区分 |

每次合并使用冻结头约束及 merge 方法；研究分支保留。以上各 PR 没有配置 CI；通过的数学审閱/精确复算与 CI 不混记。PR35 内尚未完成的盒验证和当时 PR30 审查状态保持历史原样；后续 PR30 的接受以本批新报告为准。当前结果、被否定的充分条件、可用局部范围和开放义务同步更新到状态与路线页。

## 后继整合批次 2

[PR34](https://github.com/randomcat4/dpp-entropy-tools/pull/34) 的冻结头 `838c20b12907d94a9d6e023cc03f48c3f3b36c5c` 已以 `66e807ad5825e96932679669b42d16d4cb93832e` 合入。循环平均严格性和径向四次加强分别经过新的非作者审核，另有 15 个独立编写的固定算例全部通过；[审定、脚本与输出](verification_20260909/w2/README.md)已公开。没有配置 CI，不记为 CI 成功。共同刷新基础定理与 PR29 去重；一般猜想仍 INCOMPLETE。作者后续非恒定中心探索不包含在这一冻结头的认证中。

## 后继整合批次 1

用户已明确授权唯一集成人核验后合并 main，覆盖原 AGENTS 的旧 draft-only 分工。本批以 merge commit 保留祖先关系，未删除研究分支。

| PR | 审定头 | 合并提交 | 实际依据 |
| --- | --- | --- | --- |
| [24](https://github.com/randomcat4/dpp-entropy-tools/pull/24) | `e988aa3003484f6368133b8bc0c668331629e369` | `494949f473b2eaa9a1176a71525fab628ef9d641` | [非作者范围审定、两项服务器固定复算 PASS](verification_20260909/pr24.md)；无配置 CI，不记作 CI 通过 |

可用结果、关闭的充分条件、保留的候选和开放问题同步写入 [当前成果](research_status.md) 与 [路线台账](route_ledger.md)。后继 PR30/33 尚未因依赖已合而自动获认证。

用户授权整理当前 PR，并将进展、关闭路线、有用和有趣的发现合入 main。此次保留完整原始产物及提交来源，以跨路索引纠正过时状态；不重写被冻结的证明，不把候选合并成已认证定理。

## 原 PR 固定版本

| PR | 路线 | 纳入的 head |
| --- | --- | --- |
| [#4](https://github.com/randomcat4/dpp-entropy-tools/pull/4) | T1 | `475f82d7baeb8837a6141dc84df75795237eca32` |
| [#5](https://github.com/randomcat4/dpp-entropy-tools/pull/5) | T2 | `27dda692856da210e23ae74ce267b813d3221822` |
| [#6](https://github.com/randomcat4/dpp-entropy-tools/pull/6) | T3，CANDIDATE | `905f66d22768fdcee9ff746c14f8d4fef6120daa` |
| [#8](https://github.com/randomcat4/dpp-entropy-tools/pull/8) | R1 | `a1c59992f911b68321c23d42f8ffc4f41117da66` |
| [#10](https://github.com/randomcat4/dpp-entropy-tools/pull/10) | R3 | `b4804c061b186f51d7398e05ca06ba4d27808855` |
| [#11](https://github.com/randomcat4/dpp-entropy-tools/pull/11) | R2 | `686e2e8a10499d5f91a03832776ed9a0e0ee941e` |
| [#13](https://github.com/randomcat4/dpp-entropy-tools/pull/13) | A2 | `e42954fd46c7c68e301782786f9e57dd6f0933c0` |
| [#15](https://github.com/randomcat4/dpp-entropy-tools/pull/15) | A1 | `ace25e51897e3998520da8f15365253cbf8b120e` |

整合基线为 `96b2c3ac2fb5bb5a6b74b04e193787c1cd764c5e`。八个 head 在隔离副本无冲突整合；A1 原来以 R1 为基线，先合 R1 再将 A1 目标改为 main。各研究分支和开放研究 issue 保留，合并 PR 不表示停止整个路线。

## 本次实际检查

Windows、本地 Python 3.12.14；仅做轻量精确检查，没有重跑长时间搜索或启动服务器作业。

| 入口 | 实际结果 | 边界 |
| --- | --- | --- |
| `research/T1/tools/validate_bridge.py` | 无法导入 Unix `resource` 模块 | 平台入口限制，保留此前 Linux 复核记录；没有伪造成功。 |
| `research/T1/verifications/fresh_v1/fresh_v1_tests.py` | PASS，含维数不超过 5 的 1,099 个图和适用域案例 | 独立检查器回归，不是用枚举证明定理。 |
| `research/T2/artifacts/demo_checks.py` | 13 项通过，8/64 坐标示例通过 | 本次没有施加其历史输出模板提到的 Linux 资源上限；64 坐标计算 384 个块质量。 |
| `python -m unittest discover -s research/T3/core -p 'test_*.py'` | 10 项通过 | 保留 CANDIDATE。 |
| `python -m unittest research/T3/reference/test_reference.py` | 5 项通过 | 没有据此宣称完整接口验收。 |
| `research/R1/certificate/phase4/scripts/diagonal_perturbation_exact.py` | PASS，全 8 事件、多项式质量及 4/6/7 阶系数 | 有理代数辅助检查；一致解析余项依赖原复核。 |
| `research/R1/certificate/phase4/scripts/equicorrelation_trivial_symbolic.py` | PASS，精确行列式归约和正性重写 | 不替代一般三维证明。 |
| `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/exchangeable_triangle_global_closed/sanity.py` | 7 个固定有理点通过，100 位计算最大恒等式误差 `3e-96` | 脚本状态原样为 PASS_SCOUT_NOT_PROOF，定理依据为解析证明与复核。 |

本次不对全部研究脚本作可移植性承诺；R2、A1、A2 的数学认证沿用各自冻结对象的独立报告，未重新启动一轮证明或 Lean 构建。测试产生的 T2 机器相关结果不覆盖原始冻结产物。

## 如何读历史状态

请从 [当前成果](research_status.md) 和 [路线台账](route_ledger.md) 进入。A1 与 R3 的早期“对称块未闭合”、R3 的部分过宽 Lambda 零措辞，均在台账注明后续范围；历史文件本身保持可追溯。T3 和其他未审查单元继续保留候选状态。

后续还将只读检查线程与各自工作目录，另记尚未进入上述 PR 的产物。私有对话、服务器连接信息和私库材料不随此次公开整合复制。
