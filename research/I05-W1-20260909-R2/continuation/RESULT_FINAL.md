# RESULT_FINAL.md

任务：I05-W1 第二轮延续  
最终裁决：**PARTIAL**  
本文件状态：**2026-09-09 一致性审计后的权威摘要**

## 0. 审阅层级

本 PR 中必须区分三类材料。

1. **仓库中已有审阅记录的外部输入。** 第一轮固定跨块秩一结果已经随 PR #32 合入；实 `2 x 2` 完整配置熵全局凹性由既有 R1 材料提供；过严格对角核的整条合法仿射线凹性由另一团队的 C3 材料提供。本 PR 使用这些结果，但不把它们重新计作本轮作者证明或本轮独立审阅。
2. **PR #43 的作者级完整证明。** 下文列出的第二轮与 continuation 主张均已有正文证明和作者 exact 交叉复算，但尚未由新的非作者 Codex／服务器上下文逐项审阅。
3. **开放问题与失败路线。** 一般两侧相关大块的一般非坐标 rank-two 径向族仍开放；没有严格正弦差反例。

## 1. 第二轮已有的作者级证明

对

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix},
\qquad s=t^2,
\]

逐左块完整配置 `S` 有精确条件 Schur 分解

\[
p_{K(t)}(S,T)
=p_A(S)\,p_{C-sB^{\mathsf T}(A-E_{S^c})^{-1}B}(T).
\]

因此完整熵分解为固定权重的条件熵和。由此已证明：任一侧块大小至多二时整条合法弦凹；交叉秩二时整体方向秩四；一侧至多使用两个观测坐标时可向任意维提升。对 rank two 还得到精确外幂似然比

\[
\frac{P_s(S,T)}{p_A(S)p_C(T)}
=\det(I_2-sG_A(S)G_C(T)).
\]

这些结果的详细入口是上级 `RESULT.md`、`frozen_statement.md` 与 `proof/01_conditioning.md`–`03_lifting_and_exterior.md`。

## 2. continuation 新增的作者级正结果

### 2.1 三点不定秩二方向全弦凹性

对任意严格实对称 `3 x 3` DPP 核 `K`，以及任意实对称、秩二且两个非零特征值异号的方向 `D`，

\[
z\longmapsto H(K+zD)
\]

在整个合法区间上凹，包括合法边界。

若 `n` 是 `D` 的单位零向量、`adj(D)=\gamma nn^T` 且 `\gamma<0`，令 `\kappa=n^TKn`。完整事件概率的二次系数 `c` 有精确条件四循环分解

\[
c=\sum_{i<j}\gamma n_k^2
\big[(1-\kappa)e^{ij\mid k=0}+\kappa e^{ij\mid k=1}\big].
\]

每个条件两点 DPP 的 log-odds 非正，故 `\langle c,\log p\rangle\ge0`。完整曲率

\[
H''=-\sum_x\frac{(p_x')^2}{p_x}-2\langle c,\log p\rangle
\]

两项均非正；没有丢弃 Fisher 项，也没有改变观测基。证明见 `../proof/04_three_point_indefinite_rank2.md`。半定秩二方向不在该定理范围内。

### 2.2 rank-two 外幂充分统计与压缩 Hessian

对 `B=UV^T`，联合似然比只依赖 `(G_A,G_C)`，因此把两侧完整配置分别推前到这些 `2 x 2` resolvent 特征后，KL 与互信息精确保持；这不是 Fisher 投影。

固定严格 `C` 和满列秩 `V`，令

\[
p_{C+VZV^T}(T)=\mu_T\ell_T(Z),
\qquad
\ell_T(Z)=\det(I_2+ZG_T).
\]

沿 `H\in\operatorname{Sym}_2` 的完整 Hessian 为

\[
D^2H(C+VZV^T)[H,H]
=-\sum_T\mu_T\frac{(\ell_T')^2}{\ell_T}
+2\det(H)\Lambda_{C,V}(Z),
\]

\[
\Lambda_{C,V}(Z)
=-\sum_T\mu_T\det(G_T)\log(\mu_T\ell_T(Z)).
\]

第一项是全部事件的 Fisher 代价，第二项是唯一二阶外幂加速度标量。三点不定秩二定理给出右块维数为三时的相应有利符号；一般高维符号仍开放。证明见 `../proof/05_diagonal_and_feature_routes.md`。

### 2.3 三点条件方向的有限判据

若右块 `C` 为严格实 `3 x 3` 核、`rank(B)\le2`，并且对每个左配置 `S`，

\[
M_S=B^T(A-E_{S^c})^{-1}B
\]

至少满足以下一项：

1. `rank(M_S)\le1`；
2. `M_S` 是不定秩二矩阵；
3. 直线 `{C-rM_S:r\in\mathbb R}` 含一个严格对角核；

则 `t\mapsto H(K(t))` 在整个合法区间上凹；`B\ne0` 时严格凹。三类条件分别由 rank-one 事件仿射性、2.1 的三点定理和外部对角锚点定理闭合，再经条件 Schur 径向提升汇总。

### 2.4 两侧相关、稠密非坐标的 `3+3` rank-two 结构族

令 `n\in\mathbb R^3` 为单位向量，

\[
\theta=\max_i n_i^2<\frac12,
\qquad P=I-nn^T,
\]

并取

\[
0<\alpha<1,
\qquad \theta<\beta<1-\theta,
\qquad A=\alpha P+\beta nn^T.
\]

设 `rank(B)=2`、`n^TB=0`，记 `M_0=B^TB`。若存在严格对角核 `D_0` 和实数 `\eta`，使

\[
C=D_0+\eta M_0
\]

仍为严格核，则

\[
t\longmapsto H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\]

在整个合法区间上凹；`B\ne0` 时严格凹。

空／满左配置的条件线穿过 `D_0`；其余六个配置的条件方向由 Jacobi 互补主子式恒等式证明为不定秩二，从而由 2.3 闭合。该族允许 `A,C` 均相关、非对角，`B` 稠密，左右奇异二维平面均非坐标。

完全显式例为

\[
A=\frac25I+\frac1{30}J,
\qquad
B=\begin{pmatrix}1&2&3\\4&5&6\\-5&-7&-9\end{pmatrix},
\qquad
C=\frac25I+\frac1{1000}B^TB.
\]

其精确合法半径为

\[
|t|<\tau,
\qquad
\tau^2=\frac{4091}{15000}-\frac{\sqrt{1663}}{150}>0.
\]

它严格超出“小块至多二”“两坐标支撑”和“一侧活动块对角”三类旧覆盖。证明见 `../proof/06_correlated_3plus3_family.md`。

### 2.5 对角活动约化扇区与逐条件对角锚点

若跨块耦合只进入右侧某个坐标约化扇区 `J`，且活动主块 `C_J` 为严格对角核，则整条径向熵凹；`|J|` 与 `rank(B)` 均不限，左右可交换。PR 内给出一个非对角 `3+5` 精确例，其右奇异平面稠密使用三个坐标。

更一般地，若每个条件方向 `M_S` 的直线 `C-sM_S` 都穿过某个严格对角核，则全局径向族凹。证明见 `../proof/04_diagonal_active_sector.md`。

## 3. 精确接口与严格障碍

对 rank two，若保持 `p_C` 的 Markov 核在密度伴随上把 `G_C` 乘 `\vartheta`、把 `\det G_C` 乘 `\vartheta^2`，则前向作用精确把 `P_s` 送到 `P_{\vartheta s}`。连续生成元版本保留完整 Fisher，并把真实 `t`-凹性化为

\[
2\mathcal I''+\mathcal I'\ge0.
\]

一般相关块上不能普遍要求该核可逆：对

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},
\qquad V=I_2,
\]

精确有

\[
\langle\det G_C,(G_C)_{12}\rangle_{p_C}=-125/78.
\]

可逆 Markov 算子的不同特征值特征函数必须正交，故所需可逆外幂半群不存在。仍存活的是非可逆密度伴随或隐藏状态 dilation。

另有量子通道障碍：两个输入 DPP 的配置分布相同，但经同一个相关固定点准自由衰减后，输出满事件概率为 `91/400` 与 `99/400`。因此该量子通道一般不下降为只依赖输入占据配置分布的统一经典随机核。这不否定量子数据处理，也不是 DPP 凹性反例。

## 4. 失败路线与未解决范围

本轮没有重新假定单独 `\langle Q,\log(P_s/P_0)\rangle` 非负、整块刷新保持 DPP、正交变换保持配置熵、量子互信息单调自动推出测量熵凹，或坐标轴上的 rank-one 凹性自动控制混合 Hessian。

仍未解决：两侧活动块都大于二且均相关、`B` 为一般非坐标 rank two、且条件方向不落入 2.3 判据时的整条径向配置 Shannon 熵凹性或严格反例；一般实有限核；固定标量平稳熵率；一般复 Hermitian 版本；新颖性与发表优先权。

## 5. 交付载体说明

先前名为 `I05-W1-20260909-R2-continuation_result.zip` 的本地归档是较早、不完整的快照：它没有本节 2.1–2.4 的证明文件或 v3 最终入口，包内还有一个指向未收录 `proof_continuation.md` 的索引。按本次指令不重新打包；本 PR 的冻结 commit 与 `README_v3.md` 所列文件是当前完整审阅对象。

## 6. 计算与独立审阅状态

作者 exact 复算包括两组入口：

```sh
python research/I05-W1-20260909-R2/code/verify_continuation.py
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
python research/I05-W1-20260909-R2/continuation/code/verify_continuation_v2.py
```

第一项检查三点四循环分解、稠密 `3+3` 例、八个条件方向、外幂似然和精确合法半径；后两项检查对角活动扇区、外幂刷新、准自由障碍、可逆障碍与非可逆 LP 输入。所有这些仍只是同一作者会话的 exact 交叉复算。

**PR #43 中的第二轮与 continuation 新主张尚未由新上下文非作者独立审阅。** 最新独立任务以 `CODEX_VERIFICATION_TASKS_v2.md` 为准；该文件必须覆盖 2.1–2.4，而不能只审阅后写的 Markov 分支。
