# 运行日志

所有命令应设置 `OMP_NUM_THREADS`、`OPENBLAS_NUM_THREADS`、
`MKL_NUM_THREADS`，并记录退出码。浮点搜索结果一律为诊断。

## 待运行

- 小维逐事件 Möbius 自检：完成，固定输出 `out/self_test.json`，三例
  `n=4,5,7` 均通过；最大逐事件绝对误差 `1.11e-15`，最大熵误差
  `5.17e-15`。自检进程完成并写出结果。
- 120 个 `n=11,12` 分组弦 smoke trial：完成，0 浮点候选、0 缺失记录；
  最佳 `Delta=-0.006842470469982764`。原始 120 行账本及摘要均保留。
- 首次 `unittest discover`：退出码 1。原因是测试动态导入未先登记
  `sys.modules`，Python 3.12 的 `dataclass` 装饰器在收集阶段报错；数学
  测试尚未执行。修复只改测试装载器。
- 第二次 `unittest discover`：退出码 0；3 项测试全部通过，用时 0.011 秒。

## 文件完整性

- `self_test.json` SHA-256：
  `b53b8592eca03e40e5f0fce0d3beb27cdd1cd8cac856c0d4bbb46b78235ffcb5`
- `search_smoke.jsonl` SHA-256：
  `49b61f48cb08562cb8bee04dc2e8d10e158cb7964addd0a7d16e52d03ec4a5fe`
- `search_smoke.summary.json` SHA-256：
  `8991ade03926d0fbffbbfe8142172ad002b043d976e34fed5e297fde55499233`
