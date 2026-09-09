# proof.md — 条件化提升、满交叉秩二全弦凹性与严格障碍

任务 ID：I05-W1-20260909-R2。所有对数为自然对数。全文研究真实的 `K`-仿射族；`s=t^2` 只在跨块径向族中作为由 Schur 补精确产生的参数使用。

## 1. 完整事件的单行列式表示与严格正性

令 `K` 是 `n x n` 实对称核，`S subseteq [n]`，并令 `E_{S^c}` 是在 `S^c` 上对角元为一、其余为零的对角矩阵。按这些被减去的对角元展开行列式，

\[
\det(K-E_{S^c})
=\sum_{U\subseteq S^c}(-1)^{|U|}\det K_{[n]\setminus U}.
\]

令 `T=[n]\setminus U`，则 `T superset S`。乘以 `(-1)^{|S^c|}` 后，符号满足

\[
|S^c|+|U|\equiv |T|-|S|\pmod2,
\]

故

\[
\boxed{
p_K(S)=(-1)^{|S^c|}\det(K-E_{S^c}).
}
\tag{1.1}
\]

这与题目给出的 Möbius 反演定义完全相同。

若 `0<K<I`，则每个完整事件概率严格为正。把 `S` 排在前面并写

\[
K-E_{S^c}
=\begin{pmatrix}
K_{SS}&K_{S,S^c}\\
K_{S^c,S}&K_{S^c,S^c}-I
\end{pmatrix}.
\]

当两块都非空时，Schur 补给出

\[
\det(K-E_{S^c})
=\det K_{SS}\,
\det\!\left(
K_{S^c,S^c}-I-K_{S^c,S}K_{SS}^{-1}K_{S,S^c}
\right).
\]

第一因子正。`K_{S^c,S^c}-I` 负定，减去半正定矩阵后仍负定，故第二因子的符号是 `(-1)^{|S^c|}`。空块情形直接由 `K>0` 或 `I-K>0` 得到。因此 (1.1) 严格为正，特别地下面出现的所有事件矩阵都可逆。

## 2. 精确条件化公式

### 2.1 跨块径向族

把坐标分成左右两块。固定完整配置 `S subseteq [m]`、`T subseteq [ell]`，记

\[
X_S=A-E_{S^c},\qquad Y_T=C-E_{T^c}.
\]

对

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}
\]

使用 (1.1) 和 `X_S` 的 Schur 补：

\[
\begin{aligned}
p_{K(t)}(S,T)
&=(-1)^{m-|S|+\ell-|T|}
 \det\begin{pmatrix}X_S&tB\\tB^{\mathsf T}&Y_T\end{pmatrix}\\
&=(-1)^{m-|S|}\det X_S\;
  (-1)^{\ell-|T|}
  \det\!\left(Y_T-t^2B^{\mathsf T}X_S^{-1}B\right).
\end{aligned}
\]

令

\[
M_S=B^{\mathsf T}X_S^{-1}B,
\qquad C_S(s)=C-sM_S,
\qquad s=t^2.
\]

第二个带符号行列式正是 `p_{C_S(s)}(T)`，所以

\[
\boxed{
p_{K(t)}(S,T)=p_A(S)p_{C_S(s)}(T).
}
\tag{2.1}
\]

这不是拟合，也没有遗漏 `s^2` 或更高项；它是逐完整事件的恒等式。

### 2.2 条件核确实是严格收缩核

固定严格合法的 `t` 和 `S`。由 §1，联合概率 `p_{K(t)}(S,T)` 对所有 `T` 严格为正，而 `p_A(S)>0`。故 (2.1) 右侧定义了一个全支撑概率分布

\[
q_S(T)=p_{C_S(s)}(T)=\Pr(X_C=T\mid X_A=S).
\]

由 Möbius 反演的逆变换，任意 `U subseteq [ell]` 满足

\[
\det(C_S(s))_U=\sum_{T\supseteq U}q_S(T)>0.
\]

同理，`U` 中所有点都不出现的概率是

\[
\det(I-C_S(s))_U
=\sum_{T:T\cap U=\varnothing}q_S(T)>0.
\]

