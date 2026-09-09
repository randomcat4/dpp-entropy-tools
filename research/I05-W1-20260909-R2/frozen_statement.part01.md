# frozen_statement.md

任务 ID：I05-W1-20260909-R2  
版本：v1，2026-09-09  
状态：PROVED（限于下述命题；一般实核及一般 rank-two 径向族仍开放）

## 1. 记号

有限坐标集上的实对称收缩核 `K` 定义 DPP：

\[
\Pr(T\subseteq X)=\det K_T,
\qquad
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T.
\]

完整配置 Shannon 熵为

\[
H(K)=-\sum_Sp_K(S)\log p_K(S),
\]

其中 `0 log 0=0`。严格核指 `0<K<I`。

把坐标分成大小为 `m` 和 `ell` 的两块。固定

\[
A\in\operatorname{Sym}_m(\mathbb R),\quad
C\in\operatorname{Sym}_{\ell}(\mathbb R),\quad
0<A<I,\quad0<C<I,
\]

以及 `B in R^{m x ell}`，并令

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}.
\]

记其严格合法区间为

\[
\mathcal I^\circ=\{t\in\mathbb R:0<K(t)<I\}.
\]

它关于零对称；`\mathcal I` 表示其闭包。

## 2. 定理 A：精确条件化与径向提升原理

对每个左块完整配置 `S subseteq [m]`，令

\[
X_S=A-E_{S^c},\qquad M_S=B^{\mathsf T}X_S^{-1}B,
\]

其中 `E_{S^c}` 在 `S^c` 上对角元为一、其余为零。则 `X_S` 可逆，而且对任意 `t in mathcal I^circ`、`s=t^2` 和任意右块配置 `T`，

\[
\boxed{
 p_{K(t)}(S,T)=p_A(S)\,p_{C-sM_S}(T).
}
\tag{A1}
\]

特别地，条件于左块恰为 `S` 后，右块仍是严格 DPP，其核沿真实仿射参数 `s` 变化：

\[
C_S(s)=C-sM_S.
\]

由链式法则，

\[
\boxed{
G(s):=H(K(\sqrt s))
=H(A)+\sum_Sp_A(S)H(C-sM_S).
}
\tag{A2}
\]

若所有函数 `s -> H(C-sM_S)` 在共同合法区间上凹，则 `G` 凹、在 `s=0` 取最大值且非增；于是

\[
t\longmapsto H(K(t))=G(t^2)
\]

在 `mathcal I` 上凹。若 `B != 0`，则它严格凹。

## 3. 定理 B：已知低维凹性向跨块径向族传递

假设对每个 `1 <= j <= d`，`j` 维实 DPP 完整配置熵在严格收缩核凸域上沿所有真实仿射直线凹。若上式中的右块大小 `ell <= d`，则 `t -> H(K(t))` 在整个合法区间上凹；`B != 0` 时严格凹。

本包自包含证明 `d=2` 的所需低维引理。因此得到：

> **满交叉秩二全弦定理。** 对任意 `m >= 1`、任意非对角或非交换的严格实对称块 `A in Sym_m`、`C in Sym_2`，以及任意 `B in R^{m x 2}`，
> \[
> K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}
> \]
> 的完整配置 Shannon 熵在整个合法 `t` 区间上凹；若 `B != 0` 则严格凹。
>
> 当 `rank(B)=2` 时，这是真正的交叉秩二方向。特别地，`m=ell=2` 时允许任意可逆 `B`，且 `A,C` 都不要求对角、交换或有坐标对称。

交换两块给出同样的 `m<=2` 结论。

## 4. 定理 C：任意维度中的两坐标支撑推广

