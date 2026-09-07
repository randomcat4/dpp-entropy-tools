# 分组计数约化 v1 的证明

状态：`PROVED`（作者稿）；尚未由新上下文对冻结 v1 作最终认证。

## 1. 精确事件概率

设 `Z=diag(z_1,...,z_n)`。由包含概率定义，

\[
\begin{aligned}
G_K(z)
&=\mathbb E\prod_{i\in Y}z_i
=\mathbb E\prod_i\{1+(z_i-1)1_{i\in Y}\}\\
&=\sum_{A\subseteq[n]}\det K_A\prod_{i\in A}(z_i-1)
=\det(I+K(Z-I)).
\end{aligned}
\]

因此 `z_S` 的系数就是精确事件概率 `p_K(S)`。当 `0<K<I` 时，令
`L=K(I-K)^{-1}`。`K` 与 `I-K` 可交换，故

\[
G_K(z)=\det(I-K)\det(I+LZ).
\]

行列式的主子式展开给出
`det(I+LZ)=sum_S det L_S z_S`，于是

\[
p_K(S)=\det(I-K)\det L_S. \tag{1}
\]

这由包含概率生成函数推出，与 Boolean 格上的 Möbius 反演

\[
p_K(S)=\sum_{T\subseteq S^c}(-1)^{|T|}\det K_{S\cup T}
\]

相同；没有把 `det K_S` 当成精确事件概率。

## 2. 分组核的谱和 L 矩阵

把空间正交分解为组常数子空间 `range(U)` 与每组内部的零和子空间。
在第 `g` 个零和子空间上，`U^T x=0` 且 `Kx=a_gx`。在
`range(U)` 上，因为 `U^TU=I_q`，有 `KU=UC`。故 `K` 的谱恰为
各 `a_g`（重数 `m_g-1`）与 `C` 的谱。这证明 `0<K<I`，并且

\[
\det(I-K)=\det(I-C)\prod_g(1-a_g)^{m_g-1}. \tag{2}
\]

对标量函数 `f(x)=x/(1-x)` 使用同一正交分解。写
`ell_g=f(a_g)`、`R=f(C)=C(I-C)^{-1}` 和
`B=R-diag(ell)`，得到

\[
L=f(K)=D+UBU^T, \tag{3}
\]

其中 `D` 在第 `g` 组等于 `ell_g I_{m_g}`。

## 3. 主子式只依赖计数

固定 `S`，记 `c_g=|S intersect G_g|`。限制 (3) 到 `S` 后，

\[
L_S=D_S+U_SBU_S^T.
\]

所有 `ell_g>0`，所以 `D_S` 可逆。矩阵行列式引理给出

\[
\det L_S=\det D_S\det(I_q+B U_S^TD_S^{-1}U_S).
\]

不同组的指标列正交，且第 `g` 列在 `S` 中有 `c_g` 个非零项，
每项为 `1/sqrt(m_g)`。因此

\[
U_S^TD_S^{-1}U_S
=\operatorname{diag}\!\left(\frac{c_g}{m_g\ell_g}\right)=D_c,
\]

从而

\[
\det L_S=\left(\prod_g\ell_g^{c_g}\right)\det(I_q+BD_c). \tag{4}
\]

若数值实现需要对称小矩阵，令 `W=D_c^{1/2}`。Sylvester 恒等式
`det(I+XY)=det(I+YX)` 给出

\[
\det(I+BD_c)=\det(I+WBW). \tag{5}
\]

(5) 对某些 `c_g=0` 仍成立；无需逆 `D_c`。又因 `L_S` 正定，(4)
右侧严格为正，所以浮点实现若得到非正符号必须拒绝，而不是取绝对值。

把 (2) 与 (4) 代入 (1)，即得到冻结 v1 的概率公式。右侧只依赖
计数向量 `c`，故组内置换轨道上的每个具体事件概率相同。

## 4. 熵和复杂度

计数轨道大小为 `N_c=prod_g binom(m_g,c_g)`，所有轨道大小之和为
`prod_g 2^{m_g}=2^n`。因此

\[
H(K)=-\sum_{0\le c_g\le m_g}N_c p_c\log p_c. \tag{6}
\]

式 (6) 使用单个事件的 `p_c`，不是轨道总质量 `N_cp_c`。计数向量
共有 `prod_g(m_g+1)` 个；朴素计算每个 `q x q` 行列式为 `O(q^3)`，
总算术代价为 `O(q^3 prod_g(m_g+1))`，储存可流式降到 `O(q^2)`。

## 5. 实现层对照

`artifacts/group_count_entropy.py --self-test` 对 `n=4,5,7` 的随机与
近边界严格正收缩核，先枚举全部包含主子式，再做 Möbius 反演，最后逐
事件与 (1)--(5) 对照。固定输出
`artifacts/out/self_test.json`；这项有限检查只验证实现，不替代上述证明。
