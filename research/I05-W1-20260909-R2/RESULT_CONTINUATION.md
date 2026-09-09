# RESULT_CONTINUATION.md

任务：I05 W1 第二轮继续探索  
状态：**PROVED（实质受限定理；一般两侧相关 rank-two 仍开放）**  
独立审阅：**尚未完成**。同会话推导、符号检查和脚本重跑仅算作者交叉复算；Codex／服务器非作者审阅接口见 `CODEX_TASKS.md`。

## 新增证明结果

### 1. 一侧内部块对角时，交叉秩任意

导入用户指定的另一团队定理：“过任意严格对角核的整条合法真实仿射线，配置 Shannon 熵凹”。结合本轮条件 Schur 恒等式

\[
p_{K(t)}(S,T)=p_A(S)p_{C-t^2B^T(A-E_{S^c})^{-1}B}(T)
\]

得到：若 `C` 为任意维严格对角核，`A` 为任意严格实对称核，`B` 为任意实矩阵，则

\[
t\mapsto H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\]

在整个合法区间凹；`B!=0` 时严格凹。交换两块同样成立。这里不限制 `rank(B)`、稠密性或坐标支撑，故覆盖两侧维数都大于二的任意交叉秩族。

### 2. 三点实核沿任意不定秩二方向凹

对任意严格实对称 `3 x 3` DPP 核 `K` 和任意实对称不定秩二方向 `D`，

\[
\boxed{z\mapsto H(K+zD)}
\]

在全部合法区间凹。若 `p_z=p+zr+z^2c`，取 `D` 的单位零向量 `n`，写 `adj(D)=gamma nn^T`、`gamma<0`，并令 `kappa=n^TKn`，则二阶完整事件系数有精确条件四循环分解

\[
c=\sum_{i<j}\gamma n_k^2
\big[(1-\kappa)e^{ij|k=0}+\kappa e^{ij|k=1}\big].
\]

每个条件两点 DPP 的 log-odds 非正，所以 `<c,log p>>=0`。完整曲率

\[
H''=-\sum_x(p_x')^2/p_x-2\langle c,\log p\rangle
\]

两项均非正。完整证明见 `proof/04_three_point_indefinite_rank2.md`。

### 3. 两个相关内部块的稠密非坐标 `3+3` 秩二族

令 `n in R^3` 为单位向量，`theta=max_i n_i^2<1/2`，`P=I-nn^T`。取

\[
0<\alpha<1,
\quad \theta<\beta<1-\theta,
\quad A=\alpha P+\beta nn^T.
\]

令 `B in R^{3 x 3}` 满足 `rank(B)=2`、`n^TB=0`，记 `M_0=B^TB`。若存在严格对角 `D_0` 和实数 `eta` 使 `C=D_0+eta M_0` 为严格核，则

\[
\boxed{
t\mapsto H\!\begin{pmatrix}A&tB\\tB^T&C\end{pmatrix}
\text{ 在整个合法区间凹}.}
\]

空／满左配置的两条条件线穿过 `D_0`；其余六个条件方向由 Jacobi 互补主子式恒等式证明为不定秩二，故由上一条定理闭合。

显式稠密有理例：

\[
A=\frac25I+\frac1{30}J,
\quad
B=\begin{pmatrix}1&2&3\\4&5&6\\-5&-7&-9\end{pmatrix},
\quad
C=\frac25I+\frac1{1000}B^TB.
\]

`A,C` 均非对角相关；`B` 全条目非零、秩二，左右零向量分别为 `(1,1,1)^T` 和 `(1,-2,1)^T`，所以左右奇异二维平面均非坐标。精确合法半径为

\[
|t|<\tau,
\qquad
\tau^2=\frac{4091}{15000}-\frac{\sqrt{1663}}{150}>0.
\]

这严格超出“任一块大小至多二”“一侧内部块对角”和“两坐标支撑”三类旧覆盖。完整证明见 `proof/06_correlated_3plus3_family.md`。

## 精确外幂降维

对 `rank(B)=2` 写 `B=UV^T`，则

\[
\frac{P_s(S,T)}{P_0(S,T)}
=\det(I_2-sG_A(S)G_C(T)).
\]

该似然比只依赖两个 `2 x 2` resolvent 特征，所以 KL 和互信息精确降到其推前分布，不是 Fisher 投影。固定 `C,V` 后，`Z -> H(C+VZV^T)` 的完整三参数 Hessian 精确为

\[
-\sum_T\mu_T(\ell_T')^2/\ell_T
+2\det(H)\Lambda_{C,V}(Z),
\]

其中第一项是完整 Fisher，第二项是唯一外幂加速度标量。三维定理给 `Lambda>=0`；一般维数的同一符号是本轮留下的直接可检验关键引理。

## 两条路线的裁决

- **fermionic Gaussian／诱导测量路线：** 一粒子关联矩阵层面可精确衰减跨块关联，但一般相关固定块下，占据数测量不是该通道的经典后处理。该路线只在对角中心输入下闭合，得到“任意交叉秩、一侧对角”定理。
- **外幂／混合判别式／充分统计路线：** 保留全部事件和真实核仿射方向，导出了三点不定秩二定理和相关 `3+3` 族，是本轮的主推进。

## 失败路线与边界

1. `<Q,log(P_s/P_0)> >= 0` 已有严格反例，未重新假定。
2. 整块刷新与目标径向 DPP 的精确差为 `lambda(1-lambda)s^2Q`，未重新假定保持 DPP。
3. 非坐标奇异平面不能正交旋成两个观测坐标后套二维定理。
4. 高维 `Lambda>=0` 的随机无命中不构成证明。

仍未解决：两侧块均大于二、均一般相关、`B` 为任意非坐标秩二矩阵的全径向定理或严格反例；半定秩二条件方向的完整 Fisher 联合控制；一般实有限核、一般复核及固定标量平稳熵率。

## 复算

```sh
python code/verify.py
python code/verify_continuation.py
```

新增脚本精确检查三点四循环分解、显式 `3+3` 例的严格可行性与八个条件方向分类、64 事件外幂似然恒等式和精确合法半径。100 位曲率值只作一致性诊断，不承担证明。实际输出见 `data/continuation_verification_output.txt`。
