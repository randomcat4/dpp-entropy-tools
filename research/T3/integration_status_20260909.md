# T3 归档补记：有限种子复核与整链缺口

状态仍为 **CANDIDATE**。本文件补上原 PR 文件未反映、但已经公开在 [issue #3 评论](https://github.com/randomcat4/dpp-entropy-tools/issues/3#issuecomment-5571508890) 的复核记录。它不改写冻结命题或核心代码。

该评论绑定候选 `905f66d22768fdcee9ff746c14f8d4fef6120daa`，报告新上下文对有限种子行为返回 `STATUS: CORRECT`：精确事件使用 Möbius 反演；弦符号与冻结 v1 一致；核心与独立参考得到相同概率和正 `J=H(mid)-average H(endpoints)`；下界约 `0.1107560618109726105714089086`；零概率使用熵极限，不支持的曲率零点予以拒绝。

这里保留的是公开复核报告摘要。本次没有找到独立报告全文已经进入该 PR 的文件证据，因此不把摘要升级为完整端到端认证。旧 README/provenance 中“独立验证待完成”的表述，应区分为“有限种子已有上述审查记录，整链验收仍未完成”。

仍缺：

- 严格 witness-file checker 及其独立验证。
- 更充分的 acceptance cases，覆盖拒绝与接受边界。
- 最好补充不共享 Möbius 代码路径的 mixed-row determinant 参考实现。

2026-09-09 的主线整合只复跑了核心 10 项和参考 5 项测试；没有据此晋升整条路线。种子的正 J 支持凹性，不是实反例。
