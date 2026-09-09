# CODEX_VERIFICATION_TASKS.md

本文件把独立非作者审阅与重型计算拆成可执行单元。执行者应在新的上下文和隔离工作目录中工作，冻结所审 PR commit；网页作者同会话中的脚本和复算不计作独立审阅。

## A. 第二轮原定理的独立解析审阅

审阅对象：

- `../frozen_statement.md`
- `../proof/01_conditioning.md`
- `../proof/02_two_point_input.md`
- `../proof/03_lifting_and_exterior.md`

必须逐项裁决：

1. 事件行列式到条件 Schur 核
   \[
   p_{K(t)}(S,T)=p_A(S)p_{C-t^2B^T(A-E_{S^c})^{-1}B}(T)
   \]
   是否对全部完整事件成立；条件核是否在共同合法区间内严格合法。
2. `G(s)` 凹且在零取最大值如何严格推出真实仿射参数 `t` 上的凹性。
3. 实 `2 x 2` 熵全局凹性输入的矩阵铅笔证明是否完整。
4. `m x 2`、两坐标支撑提升和 rank-two 外幂公式的前提是否被准确保留。
5. 严格性和闭边界延拓是否有遗漏。

输出：`CORRECT`、`CORRECT_WITH_SCOPE` 或 `ERROR`；若非 `CORRECT`，给出最小错误位置和可修复条件。绑定具体 commit，不把本轮后续定理混入裁决。

## B. continuation 新定理的独立解析审阅

审阅对象：

- `frozen_statement_v2.md`
- `../proof/04_diagonal_active_sector.md`
- `../proof/05_exterior_markov.md`
- `../proof/06_quantum_measurement_obstruction.md`
- `attempts_continuation.md`

必须分别裁决：

1. 对角活动约化扇区定理 E 是否只依赖明确的外部对角锚点直线定理，以及熵直和、条件混合和 `t^2` 复合步骤是否正确。
2. 精确 `3+5` 例的严格可行性、`rank(B)=2`、非两坐标支撑和旧定理不覆盖性。
3. 逐条件线对角锚点判据 F。
4. 可逆 Markov 核下密度演化的方向是否正确；`T_theta G=theta G`、`T_theta d=theta^2d` 是否确实推出
   `(Id tensor T_theta)P_s=P_{theta s}`。
5. 生成元公式
   \[
   2\mathcal I''+\mathcal I'\ge0
   \]
   与真实 `t` 曲率的系数、符号和完整 Fisher 项。
6. 两模准自由测量障碍只排除统一经典占据通道，是否没有越界否定量子数据处理。

外部输入 D 需单独记录来源和采用范围；不把它当成网页作者新证明。

## C. 精确复算入口

运行：

```sh
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
```

只接受：

- Python 退出码 0；
- 末行 `ALL CONTINUATION CHECKS PASSED`；
- 所有等式以整数/有理算术或 SymPy exact expression 为零；
- 所有严格可行性以精确主子式、精确 Gershgorin/Weyl 有理界或向外舍入区间认证；
- 不把双精度特征值或 `numpy.allclose` 当作证书。

另用不导入作者核验器的实现，从包含概率 `det K_T` 经 Möbius 反演重建完整事件概率，至少复算：

- `3+5` 例在 `t=1/5,1/2,1` 的全部 256 个事件；
- 每个左配置的 32 个条件事件；
- 对角三点刷新核的 8 个状态、全部 64 个转移概率和外幂特征关系；
- 两模障碍的四个输入和四个输出事件。

## D. 相关三点块的 exact Markov 生成元 LP

固定输入来自 `inputs/rational_examples.json`：

\[
C=\begin{pmatrix}
1/2&1/12&1/15\\
1/12&2/5&1/20\\
1/15&1/20&3/5
\end{pmatrix},
\qquad
V=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}.
\]

状态顺序 `000,001,010,011,100,101,110,111`。先以精确有理算术计算

\[
\mu(T)=p_C(T),
\quad G(T)=V^T(C-E_{T^c})^{-1}V,
\quad d(T)=\det G(T).
\]

用无序对导通量 `w_xy=w_yx>=0` 表示可逆生成元：

\[
(Lf)(x)=\mu(x)^{-1}\sum_{y\ne x}w_{xy}[f(y)-f(x)].
\]

要求

\[
LG_{11}=-G_{11},\quad LG_{12}=-G_{12},
\quad LG_{22}=-G_{22},\quad Ld=-2d.
\]

最终必须返回以下二者之一：

1. 一份全部为有理数的非负导通量表，并逐状态精确代回四组特征方程；
2. 一份有理 Farkas 对偶向量，严格证明该线性系统与 `w>=0` 不可行。

浮点 LP 的 `optimal/infeasible` 状态只可用于找候选，不是最终裁决。若可行解存在，优先稀疏化，但稀疏不是认证要求。

## E. 若 D 可行：完整熵耗散曲率证书

选择左块与 `U` 为以下固定有理对象，避免事后挑选：

\[
A=\begin{pmatrix}
2/5&1/20&1/30\\
1/20&1/2&1/25\\
1/30&1/25&3/5
\end{pmatrix},
\qquad
U=\frac1{20}\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},
\]

令 `B=UV^T`，并取由精确 Schur 补确定的完整合法 `s` 区间。对全部 64 个联合事件构造

\[
f_s=1-s\operatorname{tr}(G_AG_C)+s^2d_Ad_C.
\]

用 D 中的 exact 生成元认证

\[
\Psi(s):=2\left[
\langle L^2f_s,\log f_s\rangle+
\langle (Lf_s)^2/f_s\rangle
\right]+\langle Lf_s,\log f_s\rangle\ge0
\]

在整个闭合法区间成立，或返回一个严格负区间。

误差要求：

- 端点用精确代数数隔离或有理内外包围；
- 每个正事件质量有严格正下界；
- 对数用 MPFI/Arb、向外舍入 `mpmath` 包装证明，或带显式余项的有理 `atanh` 级数；
- 自适应区间细分必须保存覆盖清单，区间并集覆盖全域；
- 每个最终符号区间宽度不超过 `1e-20`，若无法分离则返回 `UNRESOLVED`，不可按中点符号裁决。

若 `Psi<0` 在某点严格成立，这只否定该生成元的曲率充分条件；还需直接计算真实 DPP `H''` 或弦差，不能自动称为 DPP 反例。

## F. 若 D 不可行或 E 失败：定向寻找真正 3+3 rank-two 反例

固定维数 `m=ell=3`，要求：

- `A,C` 均严格、非对角且活动部分相关；
- `B=UV^T` 恰秩二；`U,V` 的列空间均不包含于任意两坐标主平面；
- 不属于定理 E/F 的对角活动/对角锚点范围；
- 保留全部 64 个完整事件与完整 Fisher。

浮点搜索只用于候选。最终 `COUNTEREXAMPLE` 必须给出有理 `A,C,B,t_0,h`，使

\[
K(t_0-h),\ K(t_0),\ K(t_0+h)
\]

均严格满足 `0<K<I`，并以向外舍入误差界证明

\[
\Delta=\frac{H(K(t_0-h))+H(K(t_0+h))}{2}-H(K(t_0)>0.
\]

注意上一式排版应解释为 `-H(K(t_0))`；证书中必须使用正确表达式。要求：

- 所有三核严格可行有精确主子式或特征值隔离证书；
- 64 个事件逐一正且和为 1；
- `rank(B)=2` 以精确非零二阶子式和零三阶行列式确认；
- `Delta` 的严格下界至少为 `1e-20`；
- 若只能得到正 Hessian，则继续缩成三点弦差，不得以局部浮点量结束。

没有严格正弦差时，报告 `NO_CERTIFIED_COUNTEREXAMPLE_IN_DECLARED_SEARCH`，同时给出预先声明的参数盒、样本数、优化目标和最大未认证候选；不得升级为普遍凹性证据。

## G. 交付格式

服务器结果应包含：冻结 commit、环境和线程数、命令、退出码、精确输入、机器可读证书、简短解析审阅、失败状态及最小剩余义务。不要修改网页作者的冻结命题；发现错误时另写 review 文件和最小补丁建议。新颖性审计与数学正确性分开。
