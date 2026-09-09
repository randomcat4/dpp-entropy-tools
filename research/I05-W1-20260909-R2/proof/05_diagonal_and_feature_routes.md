# proof/05_diagonal_and_feature_routes.md

本节比较两条有精确桥接式的跨域路线，并给出各自真正得到的结论。所用外部输入只有用户已说明由另一团队完成的“严格对角中心整条合法直线熵凹”定理；本会话不把它冒充为自己重新审阅的结果。

## 1. 条件测量／Gaussian 衰减路线

在规范不变准自由费米态中，边际核 `K` 是一粒子关联矩阵；固定坐标占据数测量给出相应 DPP 的完整配置分布。局部 Gaussian 衰减可在关联矩阵层面保持一个块并缩放跨块关联，但固定占据数测量一般不与该量子通道交换：若固定块关联矩阵非对角，通道甚至可从真空输入产生坐标基相干，因此测量后分布不由输入测量分布的经典后处理唯一决定。

这与第二轮已经严格算出的经典障碍一致：整块刷新把 `P_s` 送到

\[
P_0+(1-\lambda)sR+(1-\lambda)s^2Q,
\]

而目标径向 DPP 是

\[
P_0+(1-\lambda)sR+(1-\lambda)^2s^2Q.
\]

差为 `lambda(1-lambda)s^2Q`。因此量子数据处理不能在一般相关块上直接替代配置熵证明。

但条件 Schur 分解与对角中心定理组合后，得到一个确切全局推广。

### 定理 A：一侧对角时，跨块秩任意

设

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix},
\]

其中 `A` 为任意严格实对称核，`C` 为任意维严格对角核，`B` 为任意实矩阵，不限制秩或坐标支撑。则 `t -> H(K(t))` 在整个合法区间凹；`B!=0` 时严格凹。交换两块同样成立。

证明：由精确条件分解，

\[
G(s)=H(A)+\sum_Sp_A(S)H(C-sM_S),
\qquad M_S=B^T(A-E_{S^c})^{-1}B.
\]

每条条件线都经过同一个严格对角中心 `C`，故由导入的对角中心定理关于 `s` 凹。于是 `G` 凹。固定双边际及 `s=0` 的乘积分布给 `G(0)-G(s)=I(X_A;X_C)>=0`，故 `G` 非增；与 `t^2` 复合即得全弦凹性。`B!=0` 时任意 `s>0` 均有某个跨块两点协方差 `-sB_{ij}^2<0`，互信息严格为正，进而得到严格凹性。

这覆盖两侧维数都大于二、稠密非坐标 `B` 及任意交叉秩，但仍要求一侧内部块对角，不能作为一般相关块问题的终点。

## 2. 外幂／充分统计路线

对 `rank(B)=2` 写 `B=UV^T`。第二轮已经得到

\[
P_s(S,T)=p_A(S)p_C(T)L_s(G_A(S),G_C(T)), \tag{1}
\]

\[
L_s(G,H)=\det(I_2-sGH),
\quad G_A=U^T(A-E_{S^c})^{-1}U,
\quad G_C=V^T(C-E_{T^c})^{-1}V. \tag{2}
\]

似然比只依赖两个 `2 x 2` 特征。令 `\bar P_s` 为 `(G_A,G_C)` 的联合推前分布，`\bar p_A,\bar p_C` 为边际推前。由于 (1) 的似然比对特征可测，给定 `(G_A,G_C)` 后，原配置的条件分布仍为两个基准纤维条件分布之积。因此

\[
D(P_s\|p_A\otimes p_C)
=D(\bar P_s\|\bar p_A\otimes\bar p_C), \tag{3}
\]

并且

\[
I_{P_s}(S;T)=I_{\bar P_s}(G_A;G_C). \tag{4}
\]

熵的全部 `s` 依赖也只在该三维矩阵特征耦合中；配置纤维熵是常数。这是严格降维，不是丢弃 Fisher 的投影。

### 固定秩二压缩的完整 Hessian

固定严格 `C` 和满列秩 `V in R^{ell x 2}`。对右配置 `T` 记

\[
Y_T=C-E_{T^c},\qquad G_T=V^TY_T^{-1}V,
\quad \mu_T=p_C(T).
\]

对 `Z in Sym_2`，

\[
p_{C+VZV^T}(T)=\mu_T\ell_T(Z),
\quad
\ell_T(Z)=\det(I_2+ZG_T)
=1+\operatorname{tr}(ZG_T)+\det Z\det G_T. \tag{5}
\]

沿真实矩阵方向 `H in Sym_2`，

\[
\ell_T'=
\operatorname{tr}(HG_T)+
\operatorname{tr}(\operatorname{adj}(Z)H)\det G_T,
\qquad
\ell_T''=2\det H\det G_T. \tag{6}
\]

归一化保证 `sum mu ell'=sum mu ell''=0`。故完整配置熵 Hessian 精确为

\[
\boxed{
\nabla^2 H(C+VZV^T)[H,H]
=-\sum_T\mu_T\frac{(\ell_T')^2}{\ell_T}
+2\det(H)\Lambda_{C,V}(Z),
} \tag{7}
\]

其中

\[
\Lambda_{C,V}(Z)
=-\sum_T\mu_T\det(G_T)\log(\mu_T\ell_T(Z)). \tag{8}
\]

第一项是这三个真实参数的完整 Fisher 代价；第二项是唯一外幂加速度标量。三点不定秩二定理等价地证明：当 `ell=3` 时，任意合法 `Z` 都有 `Lambda_{C,V}(Z)>=0`，因而 `det(H)<0` 的方向加速度自动有利。一般维数中 (8) 的符号仍是一个清晰、可直接证伪的新关键引理。

这条路线比 Gaussian 通道更有推进力：它既解释全部 `R,Q`，又导出下一节的两侧相关 `3+3` 全弦定理；但它尚未控制一般维数的半定秩二条件方向。
