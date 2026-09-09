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

其中 `E_{S^c}` 在 `S^c` 上对角元为一、其余为零。则 `X_S` 可逆，而且对任意 `t in \mathcal I^\circ`、`s=t^2` 和任意右块配置 `T`，

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

在 `\mathcal I` 上凹。若 `B != 0`，则它严格凹。

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

设 `J` 是右块至多两个坐标的集合，并假设 `B` 在 `J^c` 的列全为零。右块 `C` 的大小可任意，且 `C` 可与其余坐标任意相关。则上述径向熵仍在整个合法区间上凹；`B != 0` 时严格凹。

对称地，若 `B` 只有至多两行非零，也成立。

其基础是另一个自包含结论：在任意维实核中，若一个真实仿射方向只支撑在某个至多两坐标的主块上，则完整配置熵沿该直线凹。

## 5. 定理 D：rank-two 外幂/混合判别式桥接

若 `rank(B)=2`，任选满列秩分解

\[
B=UV^{\mathsf T},\qquad U\in\mathbb R^{m\times2},\quad
V\in\mathbb R^{\ell\times2}.
\]

对完整配置 `S,T` 令

\[
G_A(S)=U^{\mathsf T}X_S^{-1}U,
\qquad
G_C(T)=V^{\mathsf T}Y_T^{-1}V,
\qquad
Y_T=C-E_{T^c}.
\]

则对所有合法 `s=t^2`，

\[
\boxed{
\frac{P_s(S,T)}{P_0(S,T)}
=\det\!\bigl(I_2-sG_A(S)G_C(T)\bigr)
}
\tag{D1}
\]

并因此

\[
\frac{R(S,T)}{P_0(S,T)}=-\operatorname{tr}(G_A(S)G_C(T)),
\]

\[
\frac{Q(S,T)}{P_0(S,T)}=
\det G_A(S)\det G_C(T).
\tag{D2}
\]

在各自块的完整事件分布下，

\[
\mathbb E G_A=0,\quad\mathbb E\det G_A=0,
\qquad
\mathbb E G_C=0,\quad\mathbb E\det G_C=0.
\tag{D3}
\]

这给出 `R,Q` 的精确、非拟合表示，但本身不解决一般任意维 rank-two 情形。

## 6. 严格障碍命题

以下较强断言为假：

1. `\langle Q,\log(P_s/P_0)\rangle >= 0` 对所有合法 rank-two 径向族成立；
2. 以概率 `lambda` 将一整个相关块独立刷新，所得分布等于把交叉块缩放为 `sqrt(1-lambda) B` 的 DPP。

本包给出一个 `2+2` 有理严格内点例。第一项有严格区间

\[
\langle Q,\log(P_s/P_0)\rangle
\in[-0.453573880156865070680274635197,
     -0.453573880156865070680274635196],
\]

故原曲率公式中的 `-10s` 项严格为正；但完整曲率仍严格为负。第二项的精确差为

\[
\lambda(1-\lambda)s^2Q,
\]

当 `Q` 非零时不可能相等。

## 7. 未声称的范围

本文件不声称：任意块大小、任意 `rank(B)=2` 的径向族均凹；一般实对称有限核沿任意仿射弦凹；一般复 Hermitian 版本；固定标量平稳 DPP 熵率结论；新颖性或发表优先权。