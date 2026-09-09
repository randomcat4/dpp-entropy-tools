# CODEX_VERIFICATION_TASKS_v2.md

本文件取代 `CODEX_VERIFICATION_TASKS.md` 中“优先寻找可逆生成元”的部分。原因是本轮已给出严格相关二点障碍：普遍可逆外幂半群为假。其余第二轮和 continuation 的独立审阅要求继续有效。

执行者必须使用新的非作者上下文和隔离工作目录，冻结 PR commit。网页作者同会话中的证明、脚本和复算不计作独立审阅。

## A. 解析审阅范围

依次审阅：

1. `../frozen_statement.md` 与 `../proof/01_conditioning.md`、`02_two_point_input.md`、`03_lifting_and_exterior.md`；
2. `frozen_statement_v3.md`；
3. `../proof/04_diagonal_active_sector.md`；
4. `../proof/05_exterior_markov.md`，但以 `07_markov_adjoint_and_reversible_obstruction.md` 对伴随方向和可逆范围的修正为准；
5. `../proof/06_quantum_measurement_obstruction.md`；
6. `../proof/07_markov_adjoint_and_reversible_obstruction.md`。

分别输出 `CORRECT`、`CORRECT_WITH_SCOPE` 或 `ERROR`。必须明确区分：外部输入 D、作者级新证明、exact 脚本交叉检查和未解决的一般目标。

最低检查点：

- 完整事件条件 Schur 恒等式及条件核合法性；
- `s`-凹且零点最大推出真实 `t`-凹性的复合论证；
- `m x 2` 和两坐标支撑定理的精确范围；
- 对角活动约化扇区定理及 `3+5` 例；
- Markov 前向分布的密度确由 `Q^dagger` 演化；
- `2 I''+I'` 的符号、系数和完整 Fisher；
- 可逆正交性障碍中的 `-125/78`；
- 准自由障碍只排除统一经典占据通道，没有越界否定量子数据处理。

## B. 作者 exact 核验器与独立实现

运行：

```sh
python -m pip install -r research/I05-W1-20260909-R2/continuation/requirements.txt
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
```

要求退出码 0，末行为 `ALL CONTINUATION CHECKS PASSED`。再写一个不导入作者核验器的实现，从包含概率 `det K_T` 经 Möbius 反演复算：

- `3+5` 例在 `t=1/5,1/2,1` 的全部 256 个事件；
- 8 个左配置各自的 32 个条件事件；
- 对角三点刷新核的 8 个状态和 64 个转移概率；
- 两模准自由障碍的四事件分布；
- 可逆障碍的四个 `Y_T^{-1}` 与 `E[dG12]=-125/78`。

所有等式用整数/有理算术。严格正定用精确主子式、精确有理界或代数数隔离；不得用 `allclose` 或双精度特征值作为证书。

## C. 先严格确认可逆机制确实被排除

输入：

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},
\qquad V=I_2.
\]

计算完整事件 `mu=p_C`、`G(T)=(C-E_{T^c})^{-1}`、`d(T)=det G(T)`，精确验证

\[
\langle d,G_{12}\rangle_\mu=-125/78.
\]

然后独立写出自伴 Markov 算子不同特征值特征函数正交的两行证明。该裁决只排除可逆核/生成元；不得写成原熵凹性反例。

## D. 相关三点块的非可逆平稳伴随生成元 LP

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

状态顺序 `000,001,010,011,100,101,110,111`。以精确有理算术计算

\[
\mu(T)=p_C(T),
\quad G(T)=V^T(C-E_{T^c})^{-1}V,
\quad d(T)=\det G(T).
\]

对每个有序状态对 `x!=y` 使用定向平稳流变量

\[
r_{xy}=\mu(x)q_{xy}\ge0.
\]

约束：

\[
\sum_{y\ne x}r_{xy}=\sum_{y\ne x}r_{yx}
\quad\text{for every }x,
\]

且对 `f=G11,G12,G22,d`，

\[
(L^\dagger f)(y)
=\frac1{\mu(y)}\sum_{x\ne y}r_{xy}[f(x)-f(y)]
\]

分别等于 `-G11,-G12,-G22,-2d`。

最终只接受：

1. 全部为有理数的非负定向流，逐状态精确代回流量平衡和四组特征方程；或
2. 有理 Farkas 对偶证书，严格证明该系统不可行。

浮点 LP 只用于找基或对偶候选。不要重新施加 `r_xy=r_yx`；那一附加条件已经被 C 排除。

## E. 若 D 可行：全区间完整熵耗散曲率

固定左侧：

\[
A=\begin{pmatrix}
2/5&1/20&1/30\\
1/20&1/2&1/25\\
1/30&1/25&3/5
\end{pmatrix},
\qquad
U=\frac1{20}\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},
\]

令 `B=UV^T`，右侧使用 D 的 `C,V`。以精确 Schur 补隔离完整合法 `s=t^2` 区间。对全部 64 个联合事件构造

\[
f_s=1-s\operatorname{tr}(G_AG_C)+s^2d_Ad_C.
\]

用 D 的前向密度生成元认证

\[
\Psi(s)=2\left[
\langle (L^\dagger)^2f_s,\log f_s\rangle+
\left\langle\frac{(L^\dagger f_s)^2}{f_s}\right\rangle
\right]
+\langle L^\dagger f_s,\log f_s\rangle\ge0
\]

在整个闭合法区间成立，或返回严格负子区间。

误差要求：

- 端点用精确代数数隔离或有理内外包围；
- 64 个事件各有严格正下界；
- 对数用 Arb/MPFI、真正向外舍入区间，或带显式余项的有理 `atanh` 级数；
- 保存自适应细分覆盖清单，区间并集覆盖全域；
- 每个最终符号区间宽度不超过 `1e-20`；无法分离则返回 `UNRESOLVED`。

若 `Psi<0`，只说明该生成元充分条件失败。必须另算真实 DPP `H''` 或三点弦差，才能讨论原命题。

## F. 若 D 不可行或 E 失败：非坐标 `3+3` 严格反例门槛

固定 `m=ell=3`，要求 `A,C` 严格、非对角、活动部分相关，`B=UV^T` 恰秩二，且两侧奇异平面都不在任意两坐标主平面；排除定理 E/F 已覆盖范围。

浮点搜索只用于候选。最终 `COUNTEREXAMPLE` 必须给有理 `A,C,B,t_0,h`，精确证明三核

\[
K(t_0-h),\quad K(t_0),\quad K(t_0+h)
\]

均满足 `0<K<I`，全部 64 个事件逐一正、总和为一，并以向外舍入区间证明

\[
\Delta=
\frac{H(K(t_0-h))+H(K(t_0+h))}{2}-H(K(t_0))>0.
\]

`Delta` 的严格下界至少 `1e-20`。正加速度、浮点正 Hessian或某个充分条件失败都不够。若没有证书，报告预先声明的参数盒、样本数和最大未认证候选，只能标记 `NO_CERTIFIED_COUNTEREXAMPLE_IN_DECLARED_SEARCH`。

## G. 若非可逆 LP 连续失败：下一理论接口

不要无限更换随机 `C,V`。对至少两个机制不同、事先冻结的相关输入得到 exact 不可行证书后，转向跨左配置的加权条件 Hessian：

\[
\sum_Sp_A(S)D^2H(C-sM_S)[M_S,M_S].
\]

尝试利用

\[
\mathbb E(A-E_{S^c})^{-1}=0
\]

及二阶外幂矩消去，而不是逐 `S` 要求一般 rank-two 直线凹。任何新充分条件必须保留全部完整事件 Fisher，并在非坐标二维奇异平面上可直接检验。

## H. 交付

返回冻结 commit、环境/线程、命令、退出码、精确输入、机器可读证书、解析审阅、失败对象及最小剩余义务。发现错误时另写 review 和最小补丁建议，不改作者冻结文本。新颖性审计与正确性裁决分开。
