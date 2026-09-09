设 `J` 是右块至多两个坐标的集合，并假设 `B` 在 `J^c` 的列全为雰。右块 `C` 的大小可任意，且 `C` 可与其余坐标任意相关。则上述径向熵仍在整个合法区间上凹；`B != 0` 时严格凹。

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

本文件不声称：

- 任意块大小、任意 `rank(B)=2` 的径向族均凹；
- 一般实对称有限核沿任意仿射弦凹；
- 一般复 Hermitian 版本；
- 固定标量平稳 DPP 熵率结论；
- 新颖性或发表优先权。
