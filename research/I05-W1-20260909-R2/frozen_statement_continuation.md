# frozen_statement_continuation.md

版本：2026-09-09 continuation-v1  
审阅状态：作者级证明完成；尚未由新上下文非作者独立审阅。

## 导入输入

使用用户指定的另一团队结果：对任意有限实／Hermitian DPP，过任意严格对角核的整条合法真实仿射直线，完整配置 Shannon 熵凹。本包不重新认证该外部输入。

## 已证明命题 1：一侧对角、交叉秩任意

若 `A` 为任意严格实对称核，`C` 为任意维严格对角核，`B` 为任意实矩阵，则

\[
t\mapsto H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\]

在整个合法区间凹；`B!=0` 时严格凹。交换两块同样成立。这里不限制 `rank(B)`、矩阵稠密性或坐标支撑。

## 已证明命题 2：三点不定秩二方向

对任意严格实对称 `3 x 3` 核 `K` 和任意实对称不定秩二方向 `D`，`z -> H(K+zD)` 在全部合法区间凹。

## 已证明命题 3：两侧相关的非坐标 `3+3` 族

令 `n in R^3` 为单位向量，`theta=max_i n_i^2<1/2`，`P=I-nn^T`。取

\[
0<\alpha<1,
\quad \theta<\beta<1-\theta,
\quad A=\alpha P+\beta nn^T.
\]

令 `B in R^{3 x 3}` 满足 `rank(B)=2`、`n^TB=0`，记 `M_0=B^TB`。若存在严格对角 `D_0` 和实数 `eta` 使 `C=D_0+eta M_0` 为严格核，则

\[
t\mapsto H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\]

在整个合法区间凹，`B!=0` 时严格凹。

该命题允许 `A,C` 均非对角相关、`B` 稠密、左右秩二奇异平面均非坐标平面。显式有理例见 `proof/06_correlated_3plus3_family.md`。

## 精确降维引理

对 `rank(B)=2` 的外幂特征，似然比只依赖 `(G_A,G_C)`，并精确保持 KL／互信息：

\[
D(P_s\|p_A\otimes p_C)
=D(\bar P_s\|\bar p_A\otimes\bar p_C).
\]

固定 `C,V` 后，`Z -> H(C+VZV^T)` 的三参数 Hessian 为

\[
-\sum_T\mu_T(\ell_T')^2/\ell_T
+2\det(H)\Lambda_{C,V}(Z),
\]

其中第一项是完整 Fisher，第二项是唯一二阶外幂加速度标量。三维时该标量非负；一般维数符号仍开放。

## 未声称

不声称任意两侧相关、任意维一般 `rank(B)=2` 径向族已解决；不声称一般实有限核凹性、一般复核结论、固定标量平稳熵率、新颖性或独立认证。
