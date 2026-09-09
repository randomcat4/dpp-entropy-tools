# C2 第二轮：独立审核与服务器区间验证

本目录与作者 C2 的 PR31 证明分开。PR31 由 C3 安排的非作者审核；C2 不给自己的原证明独立认证。C3 是唯一 main 集成人。

## 范围与当前状态

| 单元 | 冻结范围 | 状态 |
|---|---|---|
| W3 v1.0 非作者审核 | 固定 U；每个标量中心 aI 附近半径 min(a,1-a)^2/1000；全部实对称方向 | ACCEPTED_SCOPED，仅 T1，见 w3/REVIEW.md |
| PR30 非作者审核 | 94d67909bf8c1ea06da6350cf7907d6665cb166a；精确 beta 零点接近族及独立有限参数证书 | ACCEPTED_SCOPED，见 beta/REVIEW.md；仅排除统一正安全余量 |
| 全方向 Hessian 区间 | 原 12 个冻结中心中的 R12_boundary_mid 单盒；六坐标半径 1/2048 | ACCEPTED_SCOPED，仅此单盒，见 hessian_review/REVIEW_single_box_R12_boundary_mid.md；其余 11 个中心未认证 |
| 事件导数重建 | 4 个校准中心及上述 12 个中心，全部 32 事件的六坐标二阶导数 | ACCEPTED_SCOPED，仅精确代数实现交叉检查 |

没有把有限中心、有限坐标盒或有限窗口提升为整个谱域或平稳熵率定理。

## 已完成的独立重建

`independent_events.py` 不导入作者验证代码。它直接展开五阶及以下全部主子式并作容斥，同时通过另一条固定秩三概率公式重建各事件。在每个冻结中心，32 事件的概率、6 个一阶导数及 21 个独立二阶导数全部以有理数严格相等；概率归一化与平均粒子数的仿射恒等式也核对到二阶。每点均有 26 个正概率事件和 6 个恒零事件。最小正概率逐点记录，没有删去稀有事件。

实际服务器运行使用 Python 3.12.3，单线程、无 GPU，退出码 0。第一批耗时和第二批耗时分别在 `main_output/independent_events.json` 与 `main_output/independent_centers.json` 中。这项结果只检查事件及导数的实现，不自行给出 Hessian 符号。

复算：

```sh
python3 independent_events.py --output independent_events.json
python3 independent_events.py --inputs main_output/hessian_inputs.json --output independent_centers.json
```

## 来源与隔离

- W3 的实际首轮冻结证明及作者证书按原文放在 `sources/W3/`。原作者文中的历史审核状态不代表本轮结论。
- PR30 源固定在 [94d67909bf8c1ea06da6350cf7907d6665cb166a](https://github.com/randomcat4/dpp-entropy-tools/tree/94d67909bf8c1ea06da6350cf7907d6665cb166a/research/C1)。不复制整份已公开 PR 源。
- PR24 的三项承重 N3 依赖，与 PR30 树中对应文件逐字节相同，见 `dependency_binding.json`。PR24 已由 C3 另外审核并合入；本轮不重复其相同服务器检查单元。
- 两位严格审核者是全新 GPT-5.5 xhigh 非作者上下文，先接收冻结命题与源证明，再作推导审核。既有作者和旧审核结论不能替代本轮审查。

本轮上限 8 CPU / 32 GiB，初始线程 1，无 GPU；各计算线有独立预算与停止条件。所有路径均为真实 K-affine，使用完整配置 Shannon 熵及全 Fisher。新颖性未审核；没有声明 Lean 形式化通过。

## 最终有限盒

`hessian/frozen_scope.md` 给出精确中心矩阵和六坐标范围。整个盒的谱包络为 [509/2048,1539/2048]，因此处于 0<A<I；盒与目标谱带的交集非空，但没有把整个盒或其余谱域都说成已覆盖。

正式作者服务器运行与非作者单盒复跑均退出 0。后者额外保存了完整分数形式的 Gershgorin 行证书；初始 INCOMPLETE 审核和失败记录保留。主实例还从已保存的外包矩阵独立重算有理合同变换，六行余量全部大于 1/10，见 `check_persisted_box.py` 与 `main_output/persisted_box_check.json`。这不是原坐标 Frobenius 曲率常数，接受的结论是全盒、全部非零实对称方向上的严格负曲率。

日志审计更正了早期预算汇总：73 个不同的计算尝试，保守地按全部 87 条状态记录计费，仍低于 128 上限。独立复核是另有预算的重放检查。详见 `hessian/attempt_accounting.json`。
