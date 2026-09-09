# 第四轮独立核验与整合：2026-09-09

状态：**RUNNING，按具体单元接受**。前轮九个 PR 已完成；本轮 PR57、PR59、PR60、PR62 及 PR64/71 证据已合入，后续单元仍走独立门槛。常规协作入口为 [issue44](https://github.com/randomcat4/dpp-entropy-tools/issues/44)。

| 单元 | 冻结源 | 当前结论与下一门槛 |
| --- | --- | --- |
| PR57 | 作者 `ba890f6294272849fa0a20d5c7e0e9f97d171d51`；最终包 `169cda3daf8054b53ea5622a0cb14b35a097f2e3` | **ACCEPTED_SCOPED**；r=0 精确矩阵链，新 FIRST 独立重算与隔离 SECOND 通过；合并 `818ee1a210bdcf3a57d2fac6c73e806375a8eee7`；[完整范围](verification_round4_20260909/accepted_pr57.md) |
| PR58 | 当前 `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`；原始/新增稿与各文字修订分别留档 | 原始和新增解析单元已双审；原 [3,15]/s10 的 PR72 有限 FIRST 接受证据，近似小数说明已修待 delta 闭合，有限 SECOND 进行。新增 s9/10 的 PR76 首个阈值小数界精确失败，独立有限门槛未完成 |
| PR59 | `892a121a6e26fcf638c75de917e50a4503b5675e` | **ACCEPTED_SCOPED**；五单元双审通过，合并 `0a396f65e4daa9407bb4ed6295f703d4d2e0dfe1`；[精确范围](verification_round4_20260909/accepted_pr59.md) |
| PR60 | `f869fd251c0d6fdad737b6d5efa287307795a87d` | **ACCEPTED_SCOPED**；五单元双审，合并 `ccdc63d3c16bbf7e09b20261b4b60242ba3ae010`；[精确范围](verification_round4_20260909/accepted_pr60.md) |
| PR62 | `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77` | **ACCEPTED_SCOPED**；秩一中点与小幅共同翻转解析双审，合并 `a33009272a88458b35f552fd0409fa9c69856a42`；作者有限示例未独立认证；[范围](verification_round4_20260909/accepted_pr62.md) |
| PR64 | `5b40617fe7172aa266614aa28688d310218cb387` | **MACHINE_PASS + 对应数学双审**；原始全 r 包合并 `d90a009136947139aa9233d76621d2d2d22f58f8`。首次机械索引失败和同窗修复保留 |
| PR66 | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | **INCOMPLETE**；内部解析链有条件认可，Dobrushin 原始定理的相互作用/扰动类适用性尚未闭合；全文已找到交原 FIRST，未启动 SECOND |
| PR69 | 已读 `972646e03be0062a233ae2c434ad1bff3e520913` | C1 第五轮 FIRST 档案，包含 PR60 全 r/辅助、PR58 corridor 和各独立修订闭合；后继头不自动继承 |
| PR71 | `8878516c0ad12e60884419fc03525b2a7caa7be3` | **MACHINE_PASS + 对应数学双审**；辅助原始包已合入，仅为方法障碍及真实曲率/Jensen检查 |
| PR72 | `e557d93e864582c9f9e7bd4384ed21d6ae2f66e2` | **MACHINE_PASS**；原 PR58 四区间与 s10；有限 SECOND 与源文字闭合进行中 |
| PR75 | 已读 `57d28d42ef27801daafe9c990d72b7037670a296` | C1 新到 PR62/66 FIRST 档案；解析接受和外部引用缺口分别记录 |
| PR76 | `a7979c33b6e82431b6ddf1d39ac69e254d7b655a` | **STOPPED_FIRST_EXACT_MISMATCH**；T<166.44125195305153 被严格有理包络否定。W/V 请求更正独立记账，不算作者错误；无重跑/续时 |

保留现有三个主实例：C1 首审、C2 有界计算、C3 唯一 main 集成。作者不得自证，后继头不得自动继承审定；最多三个直属子任务，禁止子任务继续派生。严谨审查用 GPT-5.5 xhigh。除非出现具体义务，不重复旧理论或计算。

C2 全 r 任务使用 issue52 单独的新合同：首单元总墙钟 2700 秒、单进程/CPU/线程、16 GiB、无 GPU，成功、严格不一致或截止即停，修复不得重置时钟。实际成功运行 15:31:39–15:32:32 UTC，52.957 秒；原截止 16:13:03 UTC 未改变，进程已退出。PR58 的固定区间和 PR60 的辅助符号障碍按各自新合同处理，不是全 r 窗口的延长。PR57 的旧窗口不再使用。网页预计超过 60 分钟的计算须先形成明确 compute issue。

本地和服务器进行了只读来源盘点：当前 C2 准备目录的子树 `e7b64c2ec98c31d38904b4e8d371751d26de49c1` 与 PR64 首个公开包一致；旧服务器运行输出保留原状，未当新证明。原始连接信息和服务器路径未公开。

五路网页21–25均获授权；21–23的后续工作继续各自研究对象，24/25不被审查队列打断。以后网页提示词必须明确“不要转 Work”。日常消息留在公开 PR/issue，只对真正重大接受或推翻升级。一般实核熵凹性、一般全合法率弦、发表新颖性及全量形式化仍未获认证。
