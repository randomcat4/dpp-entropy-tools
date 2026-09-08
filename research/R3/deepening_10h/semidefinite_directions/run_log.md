# D10-S 运行记录

- 2026-09-08：有界解析工作；未启动随机搜索或远端作业。
- 工作根固定为本仓库，只新增 semidefinite_directions/。
- 完整输入：仓库 AGENTS.md、本阶段 problem/assumptions/frozen theorem、
  local_toolbox、cross_category_probe、hazards、lemma_ledger。
- 文献：Gu、Hillion–Johnson、Yu–Johnson、Lyons 两版本及 BBL 原始来源；
  精确引用与适用域见 prior_scope.md。发现旧 Lyons Theorem8.1 需要可交换，
  改用后续综述 Theorem2.9 支持一般序；不混淆版本。
- `python research/R3/deepening_10h/semidefinite_directions/sanity.py`：
  Python3.12.14，退出0，2.5515456199645996秒。种子无；无失败候选。
- 整理时发现混合项示例的一阶导数 s/t 标签互换，修正文字与变量顺序；
  对称乘积及混合项结论未变。相同确定参数复跑退出0，2.523205518722534秒。
  共2次运行，每次6个核点/2条弦；独特分母仍为6/2，而非12/4个不同对象。
- 仅标准库、单进程；线程环境限制1，不安装依赖、不使用GPU。
- repo 内 Lean 文件模式检索无匹配（检索退出1）；没有运行 Lean，未作
  形式化认证声明。
- 脚本 exact/Möbius 检查的算术通过，不是独立证明审稿；作者未给自己
  标记 CORRECT，交回主实例决定冻结及新上下文验证。
