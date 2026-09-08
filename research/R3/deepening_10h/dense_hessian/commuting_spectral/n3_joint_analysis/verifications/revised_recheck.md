# D10-M6 v3 修订复审

日期：2026-09-08。沿用 math-theorem 验缝分层，仅修改验证目录。初审报告与版本漂移记录全部保留，本报告不覆盖或抹去初版问题。

## 最终裁决

**CORRECT，限于本次冻结修订、回归测试及 SCOUT 结果报告。**

- κ 的加号、原 simplex 奇异遗漏的处理、指定尺度回归、Ψ''≤0 的强弱和已证伪表述均已修正。
- 完整 v3 重放得到 60384 个基点评估、416691 个 support 候选，两个正总曲率列表均为零，全部匹配。
- 数值求解器明确撤回“任意一般矩阵的精确最大值”声明；仍有残差缩放的限制，详见第 3 节。因此本裁决不是一般优化器完备性认证。
- n=3 总熵凹性仍为 **INCOMPLETE**；这批有限数据仍为 **SCOUT**，不是定理。

## 1. 冻结版本与范围

作者源码 SHA-256 实际读取得到：

```text
6d275dc10ffa5466f7ead81277fd622c64378f5e020eeb3dd8345aec3a085b9a
```

与下发版本、`review_response.md`、`joint_probe_results_v3.json` 内嵌哈希一致。核验开始和完整重放结束均验证哈希；本次没有版本漂移。

其他关键冻结哈希：

```text
joint_probe_results_v3.json
ed00949868a6fa7958ba917bbbd87eaa0b19fd78b043df37f924eddf003a1fd9
copositive_and_sphere_reduction.md
c907f1a92fd3c288143afc35ede35ee16cd476c2462b13fe106f56bea509569c
joint_reduction.md
5e4c5ba2a984ae5b34ebc260468d8206a97328b0065e5fc9418d9f7a9da14574
review_response.md
4cc40a9bf3a09ecf373de384c4eec76a22a3d963b109b53ae74133da209188ae
verdict.md
0cd8a8af8f0c7f49527ca60ed80d0e9de68de05b1259f18e7e228d7bf976655a
```

`revised_check.json` 同时记录 search_report、hazards 等全部核验文件的哈希。初版 `e691fb...` 的裁决继续绑定初版，不自动转移到 v3；本次是针对上述新哈希的复审。

## 2. 两个原始回归均通过

独立夹具直接构造矩阵、使用已知解析最大值作为参照，没有调用作者的 `optimizer_regression_checks` 作为判断依据。

| 回归矩阵 | simplex 真最大值 | v3 返回 | sphere 返回及真值 |
|---|---:|---:|---:|
| J−3I | 0 | -1.8503717077085963e-17 | -6.409875621278563e-17，真值 0 |
| 10^14(6J−16I) | 2×10^14/3 | 66666666666666.68 | 200000000000000，等于真值 |

两项 simplex 返回向量均为数值上的 (1/3,1/3,1/3)，球面返回 (1/√3,1/√3,1/√3)。夹具独立检查非负、归一化、目标值误差。第一例误差属零附近的舍入；第二例与浮点真值参照差 0.015625，相对误差约 2.34e-16。

解析参照不依赖数值求解：在 simplex 上，第一例的二次型是 1−3||v||²，第二例是 10^14(6−16||v||²)；都由 ||v||²≥1/3 得到对应最大值。球面参照则来自两矩阵在均匀方向上的最大特征值。

因此初审的奇异零最大值回归和 1e14 缩放正最大值回归均没有再次失败。

## 3. KKT 修复成立的层次与剩余限制

v3 不再用 A^{-1}1 及其分母门槛，而对每个非空支撑建立增广系统

\[
\begin{pmatrix}2A&-1\\1^T&0\end{pmatrix}
\binom v\lambda=\binom01.
\]

该方程与 simplex 相对内点驻点条件一致。即使 A 奇异，增广系统也可能非奇异，正如原 J−3I 反例；因此原先直接跳过奇异 A 的代数漏洞已消除。顶点、显式二维边驻点仍保留，候选经过有限性、非负近似及归一化检查。

函数 docstring、`simplex_optimizer_note` 和修订文稿均明确称其为浮点 scout，且声明不是适用于任意退化一般 3×3 矩阵的形式精确优化器。没有继续保留被初审否定的无条件精确最大值声明。

**非阻断但必须保留的限制：相对残差不是逐约束证书。** `_kkt_residual_ok` 使用

\[
\|A_{KKT}z-b\|_\infty\le 10^{-9}
+10^{-10}\max(1,\|A_{KKT}\|_\infty\max(1,\|z\|_\infty),\|b\|_\infty).
\]

在缩放回归例，独立检查原始 least-squares 解给出

```text
raw v_i       ≈ 6.25e-30
sum(raw v)    ≈ 1.875e-29
raw residual  = 1
residual scale≈ 4.4e15
accepted      = True
```

也就是说，原始解并没有满足 sum v=1；由于量纲相异的 KKT 各行被整体大范数掩盖，它仍通过残差门。随后 `_add_simplex_candidate` 重新归一化，因为本回归矩阵对称而得到正确均匀方向。

所以本次通过不能解读为“任意大尺度问题的 KKT 约束已经准确求解”，更不能把该残差当最优性证书。若未来要升级为可靠优化工具，应对方程分块/缩放、单独验证归一化约束，并处理数值退化；本任务没有替作者实现这些扩展。

当前结果仍可作为 scout：被接受的最终 v 是实际非负归一化向量，其 v^TMv 是可检查的候选值；新增 sphere 全 support 门独立于此 KKT 残差，在数学上提供另一条点态符号检测路线。两门仍使用浮点 Hessian 和阈值，不能形成连续域上的排除定理。

## 4. v3 完整计数重放

哈希绑定加载作者模块后仅调用 scan，不调用会覆盖作者结果的 main。完整输出存为 `revised_replay_v3.json`。

| 字段 | 作者 v3 | 独立夹具重放 |
|---|---:|---:|
| base_points_checked | 60384 | 60384 |
| structured / random | 384 / 60000 | 384 / 60000 |
| sphere_candidate_vectors_evaluated | 416691 | 416691 |
| positive_total_candidates | 0 | 0 |
| sphere_positive_gate_hits | 0 | 0 |
| copositive_mismatches | 0 | 0 |

四项储存 best value（total、Ψ、singleton、pair）与作者 v3 JSON 的浮点差均为零。重放耗时约 212.59 秒，exit_code=0；期间核验范围内文件哈希全部保持不变。

计数语义沿用初审限定：

- 60384 是评估次数，不是连续基点域覆盖或去重后的参数个数。
- 416691 是 total Hessian 上的去重 support 向量目标值评估，不是每个向量都重新做八原子熵计算。
- Ψ、singleton、pair 三个额外 Hessian 只在 60000 个随机基点上计算；总 Hessian 也计算 384 个 structured 点。
- mismatch 比较的分母仍是 60000 个随机点，而非所有 60384 点。
- 新代码分别记录 simplex 正门和 sphere 正门，并以二者逻辑 OR 决定 POSITIVE_FOUND 和提前停止；当前两者都为空，实际走完全部请求点。
- 原 83456 / 574547 的另一个 sphere 批次不是本次 v3 的分母，不与 416691 混合。本次未重复运行旧批次，初审已核验的记录继续保留。

这是代码重放，不冒充全批独立多精度重算。事件 Hessian 核心公式与初审相比没有实质改变。另对 v3 最好 total 点做闭式核对：θ_i=1/2 时

\[
M=-4P^TP,\qquad P=Q\circ Q.
\]

储存 Hessian 与该公式的最大条目差为 2.22e-16。均匀谱速率给 H''=-4/3，与最好值一致。

## 5. 文本修订核对

κ(C) 的五项现在用明确的四个 `+` 连接，与代码和经典和式判据一致；初审中由“误成乘积”导致的反例不再适用。

`joint_reduction.md` 现在正确表述：

- Ψ''≤−H(N)'' 与总曲率非正等价；
- 由于 H(N)''≤0，Ψ''≤0 是更强的充分条件；
- Ψ''≤0 已被正条件层例否定，不再作为未关闭的候选定理；
- 仍开放的目标是允许正 Ψ 由 count barrier 抵消的总不等式。

这与初审给出的邻近精确有理实例及 Ψ''∈[0.000651592,0.000651593] 的严格区间一致。没有将条件层正曲率误报为总熵反例。

search_report / verdict 中个别层最好值仍沿用初版最后一两个浮点位，与 v3 JSON 的差仅在约 1e-15，非数学结论差异；使用精确机器值时以对应版本 JSON 为准。所有文稿均保留 SCOUT / INCOMPLETE 边界，没有把两个回归测试或有限未命中升级为一般定理。

## 6. 复算命令和产物

工作目录为仓库根，命令：

```powershell
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/verifications/revised_check.py
```

线程变量均限制为 1，禁止作者目录字节码写入。命令实际完成，未安装依赖，未使用 GPU，未修改作者文件。本次无测试失败。

产物：`revised_check.py`、`revised_check.json`、`revised_replay_v3.json`。结果 JSON 记录完整矩阵、两个解析参照、返回向量、原始 KKT 解和残差、所有输入哈希及重放输出哈希。

**结论不可越界：修订验收 CORRECT；有限批次 SCOUT；一般 n=3 PSD 谱速率总熵凹性仍 INCOMPLETE。**
