# R3：实对称高维结构族

原反例目标状态：`INCOMPLETE`；分组计数约化工具状态：`VERIFIED` at
`f9a9e23d766ff303e3ac0a020e5b9f2299f2b683`。本路线只研究有限维实对称严格正收缩核，优先处理
`n>=11` 的分组交换、稀疏耦合和低秩更新结构。有限搜索未命中不解释为
全实域凹性；任何严格反例在新上下文认证前只标记 `CANDIDATE`。

第一工作单元冻结一个可闭合工具：对分组指标子空间上的低秩核，把精确
事件概率按组内入选计数聚合，将全子集熵从 `2^n` 项约化为
`prod_g (m_g+1)` 项。实现必须先和小维 Möbius 容斥逐事件对照。

## 复现入口

```text
python research/R3/artifacts/group_count_entropy.py --self-test
python research/R3/artifacts/search_group_chords.py --config research/R3/artifacts/search_smoke.json
```

浮点搜索只产生候选。认证接口、误差界和覆盖边界分别记录在
`hazards.md`、`lemma_ledger.md` 和 `verifications/`。

首次 verifier 在 `19a8271` 发现精确实现只覆盖标量 `a`；否决记录保留。
修订后 verifier 对固定提交 `f9a9e23` 输出 `CORRECT`，其范围仅是冻结的
分组计数约化，不包含反例、弦 gap、族内凹性或全实域结论。

## 下一结构轮

后续三路换结构结果整理在 `next_structures/`：

- 解耦四阶局部引理经非作者验证为 `CORRECT`，说明近解耦的浮点微小正
  gap 位于一类理论上局部严格向下的近零带内；
- 路径稀疏正定 `L` 的 `O(n^2)` 精确熵递推经非作者验证为 `CORRECT`，
  但尚未解决 `K` 空间仿射弦闭包；
- 不可约三块缺陷族完成非退化有限探针而无正候选，保留
  `SCOUT / PAUSED`。

这些结果没有完成原实反例目标，也没有给出全实域凹性结论。
