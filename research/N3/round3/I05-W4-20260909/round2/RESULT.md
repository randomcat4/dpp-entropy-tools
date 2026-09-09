# RESULT — I05-W4 第二轮

日期：2026-09-09。

**总状态：PARTIAL。** 一般严格实三维核的完整 `K`-affine Shannon 熵凹性仍未证明，也没有得到严格熵反例。

## R2-T1：连通强耦合中心族的全六方向严格凹性

令

\[
K_{\kappa,\sigma}=\begin{pmatrix}
\tfrac12&0&\kappa\\
0&\tfrac12&\sigma\kappa\\
\kappa&\sigma\kappa&\tfrac12
\end{pmatrix},\qquad \sigma\in\{\pm1\},\qquad 0<8\kappa^2<1.
\]

则 `0<K<I`，非零边图连通。对任意非零实对称方向 `D`，

\[
\boxed{\ -H''(K_{\kappa,\sigma};D)>0.\ }
\]

这是完整六个真实矩阵坐标的结论；`D` 不必保持对角元 `1/2`、缺失边、两条边相等或任何置换对称。

在该族上 `v_i=1/4`，故

\[
|e_{13}|=|e_{23}|=4|\kappa|\longrightarrow\sqrt2
\quad\text{当 }8\kappa^2\uparrow1.
\]

旧 PR #33 的条件在这里仅覆盖 `|κ|<=1/16`，即 `8κ²<=1/32`。因此 R2-T1 不是把旧常数稍作放大，而是在一个连通结构族上覆盖其余全部强度，直至严格有效边界。与此同时两个事件概率 `(1-8κ²)/8` 趋于零，所以证明没有也不可能依赖统一事件概率下界。

## R2-T2：任意二点强块加孤立点

设（允许置换指标）

\[
K=A\oplus[z],\qquad 0<A<I_2,\quad 0<z<1.
\]

则对任意实对称三阶方向 `D`，

\[
\boxed{
-H_3''(K;D)=-H_2''(A;D_{\{1,2\}})
+\frac{D_{33}^2}{z(1-z)}\ge0.
}
\]

公式是等式；连接二点块与孤立点的两个方向被完整计入，但在该中心二阶恰为零。块内边可任意接近 `0<A<I_2` 的有效边界。例如

\[
A_\varepsilon=\begin{pmatrix}\tfrac12&\tfrac12-\varepsilon\\
\tfrac12-\varepsilon&\tfrac12\end{pmatrix},\qquad
0<\varepsilon<\tfrac12,
\]

的特征值为 `ε,1-ε`，归一化边为 `2-4ε`，可趋近 `2`。

R2-T2 的核心新引理是：任意严格二点 DPP 的条件熵 `H(X_1|X_2)` 对三个真实核坐标联合凹。证明保留四个事件的 Fisher 权重，并由

\[
\log t\le\frac{t-1}{\sqrt t}\qquad(t\ge1)
\]

给出一个显式正定二次型证书。

## 一般缺边连通族的进展与停止点

对

\[
K=\begin{pmatrix}x&0&b\\0&y&c\\b&c&z\end{pmatrix}
\]

已把全部六个真实方向无损改写为两个 Bernoulli 边际方向和四个事件自适应条件概率方向。完整 Fisher 在这些坐标中成为

\[
\frac{d_1^2}{x(1-x)}+\frac{d_2^2}{y(1-y)}
+\sum_{i,j}P(X_1=i)P(X_2=j)
\frac{T_{ij}^2}{t_{ij}(1-t_{ij})}.
\]

该变换在 `bc!=0` 时 Jacobian 严格非零。剩余加速度仍含条件 log-odds 的完整三点有限差分；本轮只在 R2-T1 的对称专门化中给出了解析正定证书。一般 `x,y,z,b,c` 的缺边连通族尚未证明，不以有限样本代替该缺口。

## 审阅边界

- R2-T1、R2-T2：作者侧完整证明与符号自检已提供。
- 一般缺边连通族及一般严格实三维：未解决。
- 新颖性：未认证。
- 独立非作者审阅：尚未进行；Codex 后续审阅必须另行记录。
