# PR62：移动实秩一端点中点定理的限定接受

状态：**ACCEPTED_SCOPED**。冻结作者头 `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77` 的解析定理通过 C1 FIRST 和隔离 C3 SECOND，合并提交 `a33009272a88458b35f552fd0409fa9c69856a42`。全部九个文件保留，但数值示例和多环诊断的归档不等于独立有限认证。

## 接受的定理与严格性

任意 `n>=2`、实单位向量 x,y、`0<a,b<1`，令 `K-=a xx^T`、`K+=b yy^T`，并令 `K0=(K-+K+)/2` 为真实矩阵算术中点。完整 DPP 事件的自然对数 Shannon 熵满足

```text
H(K0) >= [H(K-)+H(K+)]/2,
```

等号当且仅当 `K-=K+`。此结论允许移动方向、不等端点特征值、任意实坐标符号与零坐标。证明使用实际中点的秩至多二事件律，没有把移动标架曲线当作仿射弦。

证明先混合两端的完整事件分布，再通过参数 `0<=r<=alpha*beta` 把空集和单点质量转移到二点事件。Lagrange 恒等式与 `A_r B_r-r p_empty=alpha*beta-r>0` 保证每个活动二点项的熵导数严格为正；零项被合法忽略。共线退化单独由 Shannon 严格凹性处理，并给出精确等号条件。

## 共同独立翻转进入严格内部

对同一条严格边界弦的三核统一应用

```text
K^(epsilon)=epsilon I+(1-2epsilon)K,  0<epsilon<1/2.
```

该仿射变换保持算术中点，正是每个占据位独立翻转的 DPP 核，谱位于 `[epsilon,1-epsilon]`。令原中点缺口为 G>0，定义

```text
delta_n(epsilon)=1-(1-epsilon)^n,
omega_n(epsilon)=delta_n*log(2^n-1)
                -delta_n*log(delta_n)-(1-delta_n)*log(1-delta_n).
```

在 `delta_n<=1-2^(-n)` 且 `2 omega_n<G` 时，提升后的缺口至少为 `G-2 omega_n>0`。因此每条已接受的严格边界弦都有非空的、充分小的共同 epsilon 区间。连续性界来自 [Audenaert 的原始论文](https://arxiv.org/html/quant-ph/0610146)；总变差定义、字母表大小 `2^n`、单调区间和统一对数底均已核对。

## 证据与排除范围

- [C1 FIRST 完整报告](https://github.com/randomcat4/dpp-entropy-tools/blob/57d28d42ef27801daafe9c990d72b7037670a296/research/C1-verification-round6-20260910/units/pr62/review_report.md)。
- C3 SECOND：[冻结范围](pr62_second/frozen_scope.md)、[完整报告](pr62_second/review_report.md)、[九文件来源绑定](pr62_second/source_binding.json)、[公开副本映射](pr62_second/publication_mapping.json)。SECOND 只接收作者源和原始连续性文献，没有 FIRST、C2 或其他审稿材料。
- [作者完整解析证明](../../research/N4/agent24_20260909/moving_rank1_theorem.md)。两名审稿均仅静态检查脚本与存储输出，没有执行算术。六坐标 Householder 示例的打印小数为作者说明材料，不是解析定理前提，也没有获得独立区间认证。
- [两相关块多环对象](../../research/N4/agent24_20260909/multiring_fixture.md)只是冻结设置与高精度诊断。其整族符号、全区间证书和 issue61 长计算仍未完成。

不接受任意秩二端点、一般移动高秩框架、任意大 epsilon 提升、一般实 DPP 熵凹性、全多环定理、反例、新颖性、优先权或形式化声明。
