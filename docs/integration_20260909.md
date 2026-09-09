# 2026-09-09 main 整合记录

## 第四轮后继整合：PR60、PR62

PR60 的五个单元和 PR62 的解析中点/小幅翻转定理均分别完成 C1 FIRST 与隔离 C3 SECOND。[PR60 精确范围](verification_round4_20260909/accepted_pr60.md)及[PR62 精确范围](verification_round4_20260909/accepted_pr62.md)记录接受的量词、证据和排除项。独立原始机器包 PR64、PR71 与 PR60/62 作者头已依次合入：`d90a009136947139aa9233d76621d2d2d22f58f8`、`c19fe33c47f26f4ca51b51daba5f1e1d3febee22`、`ccdc63d3c16bbf7e09b20261b4b60242ba3ae010`、`a33009272a88458b35f552fd0409fa9c69856a42`。所有合并父提交和冻结头均核对。PR58 的新增有限小数阈值已有首个精确不一致，未合入；PR66 外部定理适用性仍由原 FIRST 核实。

## 第四轮后继整合：PR59

冻结作者头 `892a121a6e26fcf638c75de917e50a4503b5675e` 的五个独立单元均经 C1 FIRST 和隔离 C3 SECOND 接受，以 `0a396f65e4daa9407bb4ed6295f703d4d2e0dfe1` 合入。[精确接受范围与证据](verification_round4_20260909/accepted_pr59.md)区分紧致管邻域定理、RPF 恒等式、仅定性的误差接口和未闭合的占据态符号问题。没有新算术运行。

## 第四轮后继整合：PR57

PR57 作者候选 `ba890f6294272849fa0a20d5c7e0e9f97d171d51` 经独立 FIRST 和隔离 SECOND 接受，仅覆盖 r=0 开域的 Rstar/M 正性。最终包 `169cda3daf8054b53ea5622a0cb14b35a097f2e3` 的数学源逐字未改，已以 `818ee1a210bdcf3a57d2fac6c73e806375a8eee7` 合入。

[完整 accepted_scope、排除范围、两类核验覆盖及资源记录](verification_round4_20260909/accepted_pr57.md)保留 FIRST 独立执行、SECOND 解析/源代码/证书审核的差别；C3 未重复算术。旧 PR55 的未完成记录保持历史原样。后继 PR58/59/60 与新增队列不自动获审定，见[当前逐单元状态](verification_round4_20260909.md)。

## 后继整合批次 14：PR53 局部真实熵率定理与 PR56 审稿包

PR53最终头`ebecc412467939591e018a295a18c49a0a341ce9`合为`717cdb1c6acc3f51de9e04c77ec4dc6d8baa3419`；PR56最终头`02417b25a5202485386ff069b93af7a7f9cc1e6e`合为`40d17f5c650a6259c54c9447e580b70f788c5714`。分别11作者文件、41审稿/绑定文件，全部按精确头和目录范围合并。

[PR53完整接受范围](verification_round3_20260909/accepted_pr53.md)：任意均值、严格指数加权Fourier半周期中心与非零奇方向，局部真实熵率四次加强凹性，无Wiener小范数条件。FR和EW分别首审/独立第二审；最后三文件说明修订由原首审人和原第二审人分别闭合，根作者不自证。原桥接单元独立记账，有限Fourier特例不与EW重复计为两项一般性突破。

完整配置条件概率、固定较弱Hölder空间、RPF谱隙/归一化与链式法则给出真实率解析性；没有交换窗口导数极限。静态算例检查不冒充独立运行。全合法区间、任意可测符号和一般实核凹性仍开放。历史报告与明确修复闭合一并保留；主状态页给最终审定。

本轮九个PR已完成处理：41、43、47、49、51、53、54、55、56。PR55是部分证据档案，r=0候选核验未完成，不在已证定理中；issue52与旧issue45缺交接条件项保留开放。没有新增计算预算、研究路线或形式化/新颖性认证。

## 后继整合批次 13：PR55 部分证据档案

[PR55](https://github.com/randomcat4/dpp-entropy-tools/pull/55)最终头`12798ccc1afdff007a2deec3f49baf26755d1a93`，merge`43d8fd24af560afaa34b1ec8e7c7dd053e691603`，59文件。[逐项审定与失败/恢复范围](verification_round3_20260909/archived_pr55.md)明确区分已审代数、单个种子、带解析依赖的机器检查和未认证正性候选。

r=0首审为INCOMPLETE：截止后没有独立复算，C3未越过首审门槛启动接受性第二审，也未延长算术预算。一般r混合系数不判负。此合并归档可复用数据和历史，不新增r=0/全域M正性或熵反例结论。全部算术进程已结束，issue52保留未完成义务。

## 后继整合批次 12：PR54 原稿与两组附录分别双审

[PR54](https://github.com/randomcat4/dpp-entropy-tools/pull/54) 最终头 `d5c55447a0f7377dae085b8074f557e4f673b5a4`，merge `24ae88bf14b540b66490e3266a75849e6e258bad`。九文件范围完整检查；三组独立首审/新鲜第二审分别覆盖原RESULT/原算例、三个局部/端点附录及端点算例增量、后加外幂/流/率附录。

[精确接受范围与全部修复版本](verification_round3_20260909/accepted_pr54.md)记录任意秩近解耦曲率、简单谱端点、全弦匹配/双层率熵差、可见二点线性缩放障碍和条件接口。原稿三处Section5条件/措辞修复经原首审人闭合后再独立第二审；端点解析延拓与有理谱界两处修复经提出问题的第二审人闭合。历史发现保留。没有把任何熵亏损或接口升级为一般全弦凹性。

独立端点有理算例通过；没有重复运行原作者整套脚本或C2的新矩阵作业。PR53原五文件双审通过，但新473行局部熵率定理另行首审；C2唯一计算的已报外部截止为12:07:28 UTC，本批不使用尚未得到的整体符号证书。

## 后继整合批次 11：PR51 原定理与续稿分别双审

[PR51](https://github.com/randomcat4/dpp-entropy-tools/pull/51) 最终头 `184535756f5ed92f2f5c47804bdc8466a7d15041`，merge `ed10e23134d5dd8350f1cd9636204143c62ebc40`。原半填充不等强全六方向定理和新增归约各自完成独立首审及新鲜第二审；[报告、精确检查与完整限定范围](verification_round3_20260909/accepted_pr51.md)已归档。

接受严格半填充连通缺边中心的任意非零边强比和全部六方向严格负曲率；接受一般缺边的正定二维消元块、完整 Schur/Fisher/加速度、面耦合与两项方法障碍。一般四维 Schur 不等式、固定方向径向 M 正性及一般实三维凹性仍未证明，C2 issue52 的后续计算不是本次接受的前提。

最后两份入口文档仅去除私有存储定位和账户元数据，保留私有复现边界与全部数学/输出。三份数学源及所有展示代码块均未变。未获取或搬运私有作者代码。原作者稿的历史未审状态不代表当前 main 结论；本批范围优先。没有将草稿状态或空 CI 列表当作审稿证据。

PR53 第二审、PR54 原稿三处条件修复与新增附录双审、C2 #52 有界计算继续在同一轮执行。

## 后继整合批次 10：PR43 分项双审与精确流证书

| PR | 合入头 | merge commit |
| --- | --- | --- |
| [43](https://github.com/randomcat4/dpp-entropy-tools/pull/43) | `6adb231c3c1d3bf3aafc0d21132e9ad34621df89` | `de0c592c01e5b9e59e64db9df9f0d05ea1a6c01f` |
| [47](https://github.com/randomcat4/dpp-entropy-tools/pull/47) | `997c95eaf607a64d0e166dc8a08001794f59c657` | `6cbd76078caf1dc3444b0783409ef9af4968c265` |
| [49](https://github.com/randomcat4/dpp-entropy-tools/pull/49) | `b3816871965782378da5d4b559992176a66b6c26` | `580efb43568030013e0a2eac318bbe0e8db4051e` |

完整前提、两个独立审阅单元的首审/新鲜第二审、固定输入、有限计算覆盖及已修正版本，见[PR43 与固定非可逆流的限定接受](verification_round3_20260909/accepted_pr43.md)。外部对角中心输入 D 不计为新证明。E 的任意严格实三点不定秩二方向、G/H 的条件判据及相关非坐标 3+3 特殊族、I/J 的活动坐标/逐条件锚点均按所列前提接受；F/K/L 只接受相应恒等式与条件框架。M/N 是机制障碍，不是熵反例。

C1 的三个首审与三个后续新鲜上下文第二审已完成；C3 未再重复启动这些审稿。H 的两个描述句补 `eta!=0`，正好实现两次独立审稿提出的最小修正，定理允许 eta=0 的参数域保持不变。C3 完整检查两行增量后关闭文字缺口；旧 NEEDS_FIX 记录保留。

C2 的固定有向流新增独立非作者验算，通过全部八事件、56 边、40 方程和密度伴随方向，给出非可逆的有限平稳生成元。它没有证明完整熵耗散曲率。全部作者重放与指定独立有限事件检查通过，失败/中断历史均在。PR47 最后只整理公共路径与入口默认值，数学程序、精确输入/输出及流子树未改；两份入口语法检查通过，无数学重跑。各 PR 没有配置 CI。

初始 PR41/43 和对应 C1/C2 交付均已合齐。新到 PR51 的半填充不等强缺边族已单独冻结并由 C3 认领首审，旧接受不迁移；继续当前授权核验。一般实核、一般相关秩二块和一般非恒定中心标量熵率仍开放。

## 后继整合批次 9：第三轮 PR41 双审通过

[PR41](https://github.com/randomcat4/dpp-entropy-tools/pull/41) 冻结完整作者头 `6fd61dcd299417fc3a4eab3af682c03dd816b670`，merge commit `13d6c09d5d3fcf8c19cd0b01e5d735fd8778cdb6`。合并时以该头约束，13 个新增文件仅在 `research/N3/round3/I05-W4-20260909/round2/`；未删除分支。

依据为 C1 的[首审](https://github.com/randomcat4/dpp-entropy-tools/blob/5612f0a61c9f3cfe3f5ffbea960a3a672c2f9f9a/research/C1-verification-round3-20260909/units/pr41/review_report.md)、[新鲜独立第二审](https://github.com/randomcat4/dpp-entropy-tools/blob/5612f0a61c9f3cfe3f5ffbea960a3a672c2f9f9a/research/C1-verification-round3-20260909/units/pr41_second/review_report.md)，两位非作者先后分别检查完整八事件及全部六方向。C2 的[独立恒等式重建及作者重放](https://github.com/randomcat4/dpp-entropy-tools/blob/b9d1dd45a1a16f05963713178812bb3dfcae6f08/research/C2/verification3/pr41/REPORT.md)另行 PASS，正式运行退出 0；早期过大化简中断的检查点仍保留。仓库未配置 CI，空列表未记作通过。

接受 R2-T1 的 `sigma=±1`、`0<8*kappa^2<1` 强耦合等幅缺边中心全六方向严格负曲率；完整 Fisher、加速度与稀有事件均保留，`G_s'` 的全区间正定性加积分处理 `G_0` 的零方向。接受 R2-T2 的任意严格二点块加孤立点恒等式、半负定性及承重的二点条件熵引理，包括零边情形。连接方向在独立块中心 Hessian 为零，不宣称严格负定。

一般缺边三维仅接受条件坐标、可逆 Jacobian 和完整 Fisher 恒等式，剩余矩阵不等式仍开放。没有把该中心族上的 Hessian 结论推广成任意长弦；没有一般实三维、熵率、复域、新颖性或 Lean 认证。下文批次 8 的 PR41 占位观察是旧头历史，已由本批完整提交替代。

## 后继整合批次 8：最后的单盒证书

[PR42](https://github.com/randomcat4/dpp-entropy-tools/pull/42) 最终合入头 `51ca1aaaf5c9e7dfdc4f10ca16c05d05f8789223`，merge commit `211a434e242ea35945bc8b27f512e925141c847b`。原数学冻结头为 `1007c44460ea937d391d4389a79efba01f95a1e9`；后继仅将公开预算中的三条私人工作区路径改为通用表述，数学代码、输入、输出及审稿均不变。全部新增/修改文件局限于 `research/C2/verification2/`，既有 W3/PR30 证明和审核保持原样。

接受的范围仅为固定五点有理框架 `K=UAU^T` 下 R12_boundary_mid 的六坐标半径 `1/2048` 盒：A0 的对角为 `(41/100,17/50,3/4)`，非对角为 `(-3/25,0,0)`；每个盒内 A 和每个非零实对称 V 均有严格负熵曲率。全盒谱包络 `[509/2048,1539/2048]` 在 `0<A<I`；其余 11 中心、全中间谱带、熵率和新颖性均未认证。

最终数学程序 blob `e0603c77dc5a2844d0c94a36238f27856882c873`。正式服务器运行退出 0；新的非作者单盒重放同样退出 0，并保存完整精确分数 Gershgorin 行。[最终非作者报告](../research/C2/verification2/hessian_review/REVIEW_single_box_R12_boundary_mid.md)与[旧 INCOMPLETE](../research/C2/verification2/hessian_review/REVIEW.md)并存，拒绝把中途十进制摘要替代最终证书。26 个正支撑事件和 6 个恒零事件均保留；12 中心的 10752 项精确导数一致仅为实现交叉检查，没有认证 12 个盒。

C2 主实例另从保存的 Hessian 外包矩阵独立作有理合同变换，六行严格余量均大于 1/10；这是预条件坐标的矩阵证据，不是原坐标的 Frobenius 曲率常数。[完整方法及预算更正](../research/C2/verification2/hessian/certificate_method.md)记录了 73 次不同尝试和保守 87 条状态计费，小于 128 上限，未新增中心或扩盒。没有配置 CI。

已交付的原始队列与后继审定单元至此全部整合。新 PR41/W4 第二轮当前观察头 `fbcce06d19f45c6f0c84708dfed9f8cd10736dce` 仅新增一份 CLAIM.md，正文明确 under development；保留草稿和 INCOMPLETE，不合入、不继承旧证明的接受。

## 后继整合批次 7：非恒定中心弱区间

[PR39](https://github.com/randomcat4/dpp-entropy-tools/pull/39) 的冻结头 `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f` 以 `7f72e1f5cea918ef80c9b28f1155b79e270fe62b` 合入。合并前差异仅为 `research/W2/nonconstant_orbit/` 下新增文件，主证明未变；旧 PR34 的通过没有自动迁移到本项。

[两项独立解析审核及第三个上下文的独立算术实现](verification_20260909/w2_pr39/README.md)均已接受各自限定范围。NC 的复解析闭路展开给出线性体积界，四次主项与 Cauchy 余项控制产生显式窗口一致区间，先用有限 Jensen 后取真实熵率极限。NC-channel 仅排除独立于交叉块的通用局部实现。偶例与非偶例认证 [-1,1]，没有认证偶例的整个合法区间 [-384,384]。

在保存服务器冻结计划后，独立程序以一线程完成两组 n=4 全事件、多项式/KL 系数、Boolean/闭路恒等式及精确通道矛盾检查，退出 0，五组 PASS，耗时 2.452382 秒。计算输入和代码保持冻结，未扩大搜索；同一程序的重跑不是第四名审稿者。无配置 CI，不记作 CI 通过。

## 后继整合批次 6：原队列收齐

| PR | 冻结头 | merge commit | 依据 |
| --- | --- | --- | --- |
| [33](https://github.com/randomcat4/dpp-entropy-tools/pull/33) | `a0869b44bdce75acb8c2438806b21d3cf013e508` | `1cf1b1e24ed998cfb2623def4f06dc5a6f62817b` | [W4 T1–T3 最终非作者接受](../research/C1-verification-20260909/READY_BATCH_04.md)；原数学头0f06eef1至本头仅增checkpoint |
| [40](https://github.com/randomcat4/dpp-entropy-tools/pull/40) | `9249ddcba31ef9f0352867654507ee6d3b689231` | `bf88ad9940c393dd14c124c965f5459eeec0ffb3` | 解析逐步审查、严格七点补充证书、超时及错误倒数舍入的拒绝/修复全过程 |

原始八个 PR 已按依赖关系合齐。当前成果与路线页已按数学适用范围重新整理，批次历史保留于本页。与此同时新收到 W2 续接 PR39，已冻结新头 `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`，三个独立有界单元正在核 NC 解析主证明、NC-channel/固定例，以及独立算术；暂不继承 PR34 认证。没有因为旧队列合完而停止新到的授权核验。

## 后继整合批次 5

| PR | 合入头 | merge commit | 独立依据 |
| --- | --- | --- | --- |
| [32](https://github.com/randomcat4/dpp-entropy-tools/pull/32) | `1469e123293e68e1ab3836e8ec5e06a0beb2db61` | `25fd44ec4d791348cf704c49ecb846b65acc2232` | 首轮 [PR36 报告](../research/C1-verification-20260909/children/w1/W1_INDEPENDENT_REVIEW.md)与第二轮 [PR38 报告](../research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md)分别审定 |
| [38](https://github.com/randomcat4/dpp-entropy-tools/pull/38) | `d0ee74fd1355f4c364aa914ccebf6527256898f1` | `fa347cbf16d438d2486c10b3b554de5adf34d2b3` | 32+64 完整事件精确检查、一般二维矩阵铅笔符号恒等式为零、边界严格性说明 |

PR32 原审定头是 `a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8`。按非作者审阅明确要求，新增一个父接该头的文字修正提交，唯一差异是 `research/I05-W1-20260909-R2/frozen_statement.part02.md:1` 中“列全为雰”改为“列全为零”。GitHub compare 已核实无其他变化，数学内容继承相同审定。公开原冻结提交仍可访问。当前剩余旧队列 PR33/W4 尚在单独审查。

## 后继整合批次 4

| PR | 冻结头 | merge commit | 独立依据 |
| --- | --- | --- | --- |
| [29](https://github.com/randomcat4/dpp-entropy-tools/pull/29) | `648f1906468e3e548410f98a6b1a53a978f2ea11` | `eec0a94d3e1b15c1f1b126004cddf720745626c5` | 原作者 C3 未自批；[C1 的两个分项非作者接受](../research/C1-verification-20260909/READY_BATCH_02.md) |
| [36](https://github.com/randomcat4/dpp-entropy-tools/pull/36) | `03831b8031a3620e705f9538ae7810129e886a2a` | `4cab4c5534286eda21f20c476514f3f285fea908` | W1 首轮、C3 定理和固定率证书的审阅/实际计算；W1 第二轮和 W4 未在本批获接受 |
| [37](https://github.com/randomcat4/dpp-entropy-tools/pull/37) | `b0a208c7ab0cf0b4afdeb56d56211e90a5303468` | `2248f8e6d484a27636eebbe5508637b1bedfba0d` | [PR30 新非作者审核与机器证据](../research/C2/verification2/beta/REVIEW.md)，没有重复发布 W3 已合文件 |

PR36 此后新增审核须独立后继 PR；冻结本批不会给未审后续内容自动认证。原作者文件保持固定版本，已知非阻塞文案事项写入审阅与当前状态。无 CI 的记录与实际计算 PASS 继续分别说明。

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
