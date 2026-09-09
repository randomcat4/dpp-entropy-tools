一般地，若对每个 `1<=j<=d` 都已知 `j` 维实 DPP 完整熵沿任意真实 `K`-仿射线凹，那么右块大小 `ell<=d` 时，每个条件函数 (5.1) 都由该低维结论控制；§5 因而把低维仿射凹性传递成任意左块大小的跨块径向凹性。若只掌握恰好 `d` 维的版本，较小维数也可通过与固定独立 Bernoulli 坐标作块直和嵌入到 `d` 维；熵只增加常数。

### 6.1 一侧大小至多二

若右块大小 `ell<=2`，则每个条件核 `C-sM_S` 都是至多二维的任意真实仿射线。§3（或一维二元熵）保证 (5.1) 凹。因此 §5 立即给出：

\[
\boxed{
\ell\le2\Longrightarrow t\mapsto H\!\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}
\text{ 在整个合法区间上凹。}
}
\tag{6.1}
\]

这里 `m` 任意，`A` 可含任意内部相关，`B` 也任意。当 `ell=2` 且 `rank(B)=2` 时，整体方向

\[
D=\begin{pmatrix}0&B\\B^{\mathsf T}&0\end{pmatrix}
\]

的秩为四而不是一或二，并且交叉块本身秩为二；它可同时改变 `2m` 条交叉边。特别地 `m=ell=2`、`B` 可逆正是题目的秩二试金石。交换两块给出 `m<=2` 的版本。

### 6.2 任意维但交叉列支撑至多两个坐标

若 `B` 只有坐标集合 `J` 中至多两列非零，则对每个 `S`，

\[
M_S=B^{\mathsf T}X_S^{-1}B
\]

只支撑在 `J x J`。即使 `C` 维数任意、`J` 与其余坐标强相关，§4 仍保证每条 (5.1) 凹。故 §5 给出冻结定理 C。只有至多两行非零的情况由交换左右块得到。

## 7. rank-two 外幂/混合判别式的精确桥接

本节不用于替代 §5 的符号证明，而是精确解释 `R,Q` 和整块刷新为何在二阶外幂处失效。

设 `rank(B)=2`，取满列秩分解

\[
B=UV^{\mathsf T}.
\]

对完整配置 `S,T` 定义

\[
G_A(S)=U^{\mathsf T}X_S^{-1}U,
\qquad G_C(T)=V^{\mathsf T}Y_T^{-1}V.
\]

由 §2 的行列式比值和 Sylvester 行列式恒等式，

\[
\begin{aligned}
\frac{P_s(S,T)}{P_0(S,T)}
&=\frac{\det(Y_T-sV G_A(S)V^{\mathsf T})}{\det Y_T}\\
&=\det\!\left(I_\ell-sY_T^{-1}V G_A(S)V^{\mathsf T}\right)\\
&=\det\!\left(I_2-sG_A(S)V^{\mathsf T}Y_T^{-1}V\right)\\
&=\det(I_2-sG_A(S)G_C(T)).
\end{aligned}
\tag{7.1}
\]

对 `2 x 2` 矩阵，

\[
\det(I_2-sG_AG_C)
=1-s\operatorname{tr}(G_AG_C)+s^2\det G_A\det G_C.
\tag{7.2}
\]

所以

\[
R(S,T)=-P_0(S,T)\operatorname{tr}(G_A(S)G_C(T)),
\tag{7.3}
\]

\[
Q(S,T)=P_0(S,T)\det G_A(S)\det G_C(T).
\tag{7.4}
\]

这说明最高系数 `Q` 是两个二阶外幂特征的张量积。

(2.4) 立刻给

\[
\mathbb E_{p_A}G_A=0,
\qquad\mathbb E_{p_C}G_C=0.
\tag{7.5}
\]

再考察合法小邻域中的秩二更新 `A+zUU^T`。由 (1.1) 和矩阵行列式引理，

\[
p_{A+zUU^{\mathsf T}}(S)
=p_A(S)\det(I_2+zG_A(S)).
\]

