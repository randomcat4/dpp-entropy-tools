# PR79 独立第二审核冻结范围

## 审核对象

本轮审核对象是 PR79 whole-interval curvature upper-budget/Riccati/RPF 作者稿，冻结 head：

```text
ae1149f2ed7d657afa494740c3abae83de549d3f
```

本轮是与 PR77 相关但不同的有界单元。既有 PR77 独立二审报告保持原样；PR77 的数值保留和全区间缺口不得由 PR79 接口自动闭合。

Novelty: NOT_ASSESSED.

Formal verification: NOT_PERFORMED.

Computation: NOT_PERFORMED. 我没有运行 `tail_budget.py` 或任何数学脚本，也没有做行列式、对数、熵、几何级数或阈值重算。

## 读取文件

只读取并绑定以下文件：

- `input/RESULT.md`
- `input/tail_budget.py`
- `input/run_record.txt`
- `pr77_source/proof.md`
- `input_binding.json`

`pr77_source/proof.md` 是已知 PR77 纯作者源，head 为：

```text
2564e25a8b62a72992b9451988cd42e2d5a81834
```

本轮未读取 C1 FIRST、其他 SECOND、C3 裁定、PR89 状态或材料、PR79 以外材料、远程脚本或 `[excluded private directory]` 下任何文件。

## 绑定核对

`input_binding.json` 声明 4 个源文件加绑定清单。机器重新计算的 SHA256 已写入 `source_binding.json`，覆盖本轮读取的 5 个文件。

绑定中的源文件哈希与重新计算结果一致：

- `input/RESULT.md`
- `input/tail_budget.py`
- `input/run_record.txt`
- `pr77_source/proof.md`

## 本轮审核边界

本轮只审核作者源层面的公式接口、范围限定和证据打包：

1. `B_R` 是否是 PR77 CMI 二阶尾项公式给出的显式共同上界预算；
2. `sum_{r>=R}|d_r''(t)|<=B_R` 是否是 PR77 公式接口可支持的语义；
3. 有限深度条件曲率上界与 `B_R` 的组合逻辑是否正确；
4. 正区间证书到负区间的转移是否只依赖物理 gauge/evenness，而不是重新计算；
5. Riccati/hidden-filter 路线是否正确承认连续状态、分支概率、收缩、jets、测度响应和每原始格点 `1/2` 因子的缺口；
6. RPF/Poisson/CMI 接口是否保留 Fisher、加速度、测度响应和尾项；
7. 作者 PASS、预算数字和阈值比较是否被正确标为待检来源。

所有 PR79 具体预算数值、阈值比较和作者 PASS 均未被本轮独立接受为已算证书。本轮也没有新的 C2 数值契约。

