# I05-W4 第二轮：事件自适应强耦合结果

日期：2026-09-09。

本目录是 PR #33 的作者侧续篇。上一轮的弱耦合定理继续有效，但一般严格实三维命题仍未解决。本轮新增两个解析结果：

1. 一个**连通、强耦合、全六方向**的一参数中心族；其两条归一化边可从旧阈值 `1/4` 一直趋近有效边界 `sqrt(2)`，负熵 Hessian 对每个非零实对称方向严格为正。
2. 任意严格二点 DPP 块加一个孤立点时的**全六方向**凹性；块内唯一强边可任意逼近二点有效边界。

主证明不使用浮点扫描、统一概率下界或固定安全余量。审阅入口如下：

- `frozen_statement.md`：冻结的定义、全部量词、边界与未证明范围；
- `RESULT.md`：结论摘要及旧域关系；
- `proof.md`：八事件推导、完整 Fisher、全部真实坐标混合项及解析符号证书；
- `attempts.md`：不同路线、失败机制和一般缺边族的精确停止点；
- `sources.md`：使用的来源与假设边界；
- `verification.md`：作者自检、发布一致性检查及独立审阅边界；
- `HANDOFF.md`：至多两个可直接执行的独立审阅任务；
- `code/verify_symbolic.py`、`inputs/exact_inputs.json`、`outputs/verify_symbolic.txt`：复算代码、精确输入和规范输出。

运行作者自检：

```sh
python -m pip install -r requirements.txt
python code/verify_symbolic.py
```

预期末行：

```text
ALL SYMBOLIC CHECKS PASSED
```

同会话的符号复算属于作者自检，不是独立审阅。当前状态是：**作者证明材料完整，独立非作者审阅尚未进行，新颖性未认证。**