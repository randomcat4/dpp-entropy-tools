# CODEX_VERIFICATION_TASKS_v2.md

本文件是 PR #43 当前全部作者级主张的独立审阅规范。它取代旧版中“优先寻找可逆生成元”的要求，也修复旧版遗漏 `04_three_point_indefinite_rank2.md` 与 `06_correlated_3plus3_family.md` 的问题。

执行者必须使用新的非作者上下文和隔离工作目录，冻结具体 PR commit。网页作者同会话中的证明、脚本和复算不计作独立审阅。

## A. 先区分审阅层级

### A1. 既有仓库输入，不在本轮重复计数

- PR #32 的固定跨块秩一结果；
- R1 的实 `2 x 2` 完整配置熵全局凹性；
- C3 提供的“过严格对角核的整条合法仿射线凹性”。

应核对本 PR 对这些输入的引用范围，但不要把复用输入计作 PR #43 新主张的独立审阅。

### A2. PR #43 新上下文必须逐项裁决的作者级主张

依次审阅：

1. `../frozen_statement.md` 与 `../proof/01_conditioning.md`–`03_lifting_and_exterior.md`；
2. `frozen_statement_v3.md` 与 `../proof/04_three_point_indefinite_rank2.md`；
3. `../proof/05_diagonal_and_feature_routes.md`；
4. `../proof/06_correlated_3plus3_family.md`；
5. `../proof/04_diagonal_active_sector.md`；
6. `../proof/05_exterior_markov.md`，但以 `../proof/07_markov_adjoint_and_reversible_obstruction.md` 对伴随方向和可逆范围的修正为准；
7. `../proof/06_quantum_measurement_obstruction.md`。

每项输出 `CORRECT`、`CORRECT_WITH_SCOPE` 或 `ERROR`，并绑定冻结 commit。

## B. 三点不定秩二定理的最低检查点

必须从完整事件定义独立重建：

1. `rank(D)=2` 导致每个事件概率至多二次；
2. `adj(D)=gamma nn^T`、`gamma<0`，以及 `delta_ij=gamma n_k^2`；
3. 三点二次系数为 `gamma n^TKn`；
4. 条件四循环分解逐八个原子成立；
5. 条件两点 DPP 的 log-odds 非正；
6. 完整曲率
   \[
   H''=-\sum(p')^2/p-2\langle c,\log p\rangle
   \]
   的系数和符号；
7. 论证适用于每个合法内点，边界只通过函数值连续性延拓；
8. 没有把半定秩二方向纳入结论。

## C. 外幂充分统计与压缩 Hessian

独立核对：

1. `P_s/(p_Ap_C)=det(I_2-sG_AG_C)`；
2. 给定 `(G_A,G_C)` 后，基准纤维条件分布分解，从而 KL／互信息推前等号成立；
3. `ell_T(Z)=det(I_2+ZG_T)` 的一、二阶导数；
4. 压缩 Hessian 中的第一项确为全部事件 Fisher，第二项系数确为 `2 det(H) Lambda`；
5. 三维 `Lambda` 符号只在不定秩二方向的适当意义下由三点定理给出，没有被外推到一般高维或半定方向。

## D. 三点条件判据与相关 `3+3` 族

### D1. 条件判据

对每个 `M_S` 的三种情形分别核对所调用的定理和共同合法参数区间；确认逐配置条件熵凹可经固定权重求和及 `t^2` 径向提升得到全弦凹性。

### D2. 结构族解析审阅

核对：

1. `theta=max_i n_i^2<1/2` 与 `theta<beta<1-theta` 的用途；
2. 空／满左配置的 `M_S` 与 `M_0` 成比例，条件线穿过 `D_0`；
3. 对 `|S|=1,2`，事件矩阵惯性和 Jacobi 互补主子式恒等式确实推出压缩 `2 x 2` 矩阵不定；
4. 满行秩合同保持非零惯性，从而 `M_S` 为不定秩二；
5. 严格性和合法边界没有遗漏。

### D3. 显式有理／代数例

固定：

\[
A=\frac25I+\frac1{30}J,
\quad
B=\begin{pmatrix}1&2&3\\4&5&6\\-5&-7&-9\end{pmatrix},
\quad
C=\frac25I+\frac1{1000}B^TB.
\]

以精确算术核对：

- `rank(B)=2`、左右零向量及两侧奇异平面非坐标；
- `M_0` 的特征多项式 `x(x^2-246x+162)`；
- `0<A,C<I`；
- 八个 `M_S` 的分类；
- `tau^2=4091/15000-sqrt(1663)/150>0`；
- 至少两个非零有理 `t` 上全部 64 个事件为正并和为一。

高精度熵曲率只能作为一致性诊断，不替代解析证明。

## E. 活动扇区、Markov 与量子障碍

独立核对：

- 对角活动约化扇区定理及 `3+5` 例；
- 逐条件对角锚点判据；
- Markov 前向分布的密度由 `Q^dagger` 演化；
- `2 I''+I'` 的符号、系数和完整 Fisher；
- 可逆正交性障碍 `-125/78` 只排除可逆机制；
- 准自由障碍只排除统一经典占据通道，不否定量子数据处理。

## F. 作者脚本与独立实现

运行全部作者入口：

```sh
python research/I05-W1-20260909-R2/code/verify_continuation.py
python -m pip install -r research/I05-W1-20260909-R2/continuation/requirements.txt
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
python research/I05-W1-20260909-R2/continuation/code/verify_continuation_v2.py
```

要求退出码均为零，末行分别匹配仓库保存输出。然后另写不导入作者核验器的实现，从包含概率 `det K_T` 经 Möbius 反演复算三点八事件、相关 `3+3` 六十四事件、`3+5` 二百五十六事件、量子障碍四事件及可逆障碍四个逆矩阵。

所有结构等式使用整数／有理／代数数精确算术。不得用 `allclose` 或双精度特征值作证书。

## G. 相关三点块的非可逆平稳伴随生成元 LP

固定输入：

\[
C=\begin{pmatrix}
1/2&1/12&1/15\\
1/12&2/5&1/20\\
1/15&1/20&3/5
\end{pmatrix},
\qquad
V=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}.
\]

以有序定向平稳流 `r_{xy}=mu(x)q_{xy}\ge0` 建立流量平衡，并要求密度伴随满足

\[
L^\dagger G_{11}=-G_{11},\quad
L^\dagger G_{12}=-G_{12},\quad
L^\dagger G_{22}=-G_{22},\quad
L^\dagger d=-2d.
\]

最终只接受：

1. 全部为有理数的非负定向流及逐状态精确代回；或
2. 有理 Farkas 对偶证书。

不得重新施加 `r_{xy}=r_{yx}`；可逆附加条件已经被严格排除。

若 LP 可行，再对固定 `A,U,C,V` 认证整个合法区间上的

\[
2\mathcal I''+\mathcal I'\ge0
\]

或给出严格负子区间。端点、事件正下界、对数区间与自适应覆盖要求沿用旧版：最终符号区间宽度不超过 `1e-20`，无法分离则返回 `UNRESOLVED`。

## H. 反例搜索边界

若转向 `3+3` 或更高维搜索，必须显式排除本 PR 已证明的范围：

- 任一侧块大小至多二；
- 一侧至多两个观测坐标支撑；
- 对角活动约化扇区／逐条件对角锚点；
- G 中三点条件方向判据；
- H 中相关 `3+3` 结构族。

最终 `COUNTEREXAMPLE` 必须给出有理三核、严格可行性、全部事件正性和弦差的向外舍入严格正下界。正 Hessian、浮点信号或某个充分条件失败都不够。

## I. 交付

返回冻结 commit、环境与线程、命令、退出码、精确输入、机器可读证书、逐主张解析裁决、失败对象和最小剩余义务。发现错误时另写 review 和最小补丁建议，不改作者冻结文本。新颖性审计与数学正确性分开。
