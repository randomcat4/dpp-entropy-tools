# proof.md — 事件自适应强耦合证明

## 1. 统一约定与完整二阶变分

写

\[
K=\begin{pmatrix}x&a&b\\a&y&c\\b&c&z\end{pmatrix},\qquad
D=\begin{pmatrix}d_1&h_{12}&h_{13}\\h_{12}&d_2&h_{23}\\h_{13}&h_{23}&d_3\end{pmatrix}.
\]

令

\[
q_{12}=xy-a^2,\quad q_{13}=xz-b^2,\quad q_{23}=yz-c^2,
\]

\[
r=xyz+2abc-xc^2-yb^2-za^2.
\]

按事件顺序

\[
0,1,2,12,3,13,23,123
\]

八个概率是

\[
\begin{aligned}
p_0&=1-x-y-z+q_{12}+q_{13}+q_{23}-r,\\
p_1&=x-q_{12}-q_{13}+r,\\
p_2&=y-q_{12}-q_{23}+r,\\
p_{12}&=q_{12}-r,\\
p_3&=z-q_{13}-q_{23}+r,\\
p_{13}&=q_{13}-r,\quad p_{23}=q_{23}-r,\quad p_{123}=r.
\end{aligned}
\]

所有导数均沿真实矩阵直线 `K+tD`。在严格内点八个概率均正，并且

\[
\boxed{
\mathcal B_K(D):=-H''(K;D)
=\sum_S\frac{(p'_S)^2}{p_S}+\sum_Sp''_S\log p_S.
}\tag{1}
\]

第一项记为 `F`，第二项记为 `A`。后文始终使用八项 `F`；没有删掉稀有事件或三点事件。

## 2. R2-T1 的中心、有效性和事件概率

先取 `σ=1`；其他符号由对角符号共轭处理。令

\[
K_\kappa=\begin{pmatrix}
\tfrac12&0&\kappa\\
0&\tfrac12&\kappa\\
\kappa&\kappa&\tfrac12
\end{pmatrix},\qquad s=8\kappa^2.
\]

向量 `(1,-1,0)` 的特征值为 `1/2`，其正交补上的矩阵为

\[
\begin{pmatrix}\tfrac12&\sqrt2\kappa\\\sqrt2\kappa&\tfrac12\end{pmatrix}.
\]

故特征值为

\[
\tfrac12,\quad \tfrac12+\sqrt2\kappa,\quad \tfrac12-\sqrt2\kappa.
\]

因此 `0<Kκ<I` 当且仅当 `0<=s<1`；主定理取 `0<s<1`。

代入八事件公式，置

\[
A_-:=\frac{1-s}{8},\qquad A_+:=\frac{1+s}{8},\qquad A_0:=\frac18,
\]

得到

\[
(p_0,p_1,p_2,p_{12},p_3,p_{13},p_{23},p_{123})
=(A_-,A_0,A_0,A_+,A_+,A_0,A_0,A_-).\tag{2}
\]

当 `s↑1` 时 `p_0=p_{123}=A_-↓0`。以下证明保留这两个事件的真实 `1/A_-` Fisher 权重，不用统一正下界替代它们。

## 3. 六个真实方向与八个一阶事件导数

定义可逆线性坐标

\[
P=d_1+d_2,\quad \Delta=d_1-d_2,\quad Z=d_3,
\]

\[
R=h_{12},\quad H=h_{13}+h_{23},\quad N=h_{13}-h_{23}.
\tag{3}
\]

也即 `d1=(P+Δ)/2`、`d2=(P-Δ)/2`、`h13=(H+N)/2`、`h23=(H-N)/2`。从第一节的八个概率逐项求导，得到

\[
\begin{array}{c|l}
S&4p'_S\\ \hline
0&-4\kappa H+4\kappa^2P-P-8\kappa^2R-Z\\
1&\Delta+4\kappa N-4\kappa^2P+8\kappa^2R-Z\\
2&-\Delta-4\kappa N-4\kappa^2P+8\kappa^2R-Z\\
12&4\kappa H+4\kappa^2P+P-8\kappa^2R-Z\\
3&4\kappa H-4\kappa^2P-P+8\kappa^2R+Z\\
13&\Delta-4\kappa N+4\kappa^2P-8\kappa^2R+Z\\
23&-\Delta+4\kappa N+4\kappa^2P-8\kappa^2R+Z\\
123&-4\kappa H-4\kappa^2P+P+8\kappa^2R+Z.
\end{array}\tag{4}
\]

这些是完整八事件的一阶导数；直接相加为零。

二阶导数各自仍含 `d_i d_j`、`h_{ij}^2`、`d_i h_{jk}` 和 `h_{ij}h_{ik}`。由于 (2) 只有三种 log 权重，`A` 只需要三组的精确和。逐项相加得到

\[
\begin{aligned}
\sum_{S\in\{0,123\}}p''_S
&=-\frac{\Delta^2+2H^2+2N^2-P^2-4PZ+4R^2}{2},\\
\sum_{S\in\{12,3\}}p''_S
&=-\frac{\Delta^2-2H^2-2N^2-P^2+4PZ+4R^2}{2},\\
\sum_{S\in\{1,2,13,23\}}p''_S
&=\Delta^2-P^2+4R^2.
\end{aligned}\tag{5}
\]

三式之和为零。这里仅因同组事件的 `log p` 完全相同而合并；没有删除任何 `p''_S`。`code/verify_symbolic.py` 另外从六个原始坐标逐项重建 (4)–(5)。

## 4. 完整 Fisher 与加速度的精确矩阵

记

\[
D_s:=1-s^2,
\qquad
m(s):=\log(1-s^2),
\qquad
g(s):=\log\frac{1+s}{1-s}.
\tag{6}
\]

把 (4) 的八个平方分别除以 (2) 的八个概率并相加。置 `v=(P,Z,R)^T`，得到完整 Fisher

\[
F=v^TF_s v+\frac{4s}{D_s}H^2+2\Delta^2+4sN^2,\tag{7}
\]

其中

\[
F_s=\frac1{D_s}
\begin{pmatrix}
\frac{4-2s^2-s^4}{2}&s(2-s^2)&s^4\\
s(2-s^2)&2(2-s^2)&2s^3\\
s^4&2s^3&2s^2(2-s^2)
\end{pmatrix}.
\tag{8}
\]

尤其 `A_-` 的小分母已经保留在 `D_s=(1-s)(1+s)` 中。

由 (5)，并用

\[
\log A_-=-\log8+\log(1-s),\quad
\log A_+=-\log8+\log(1+s),\quad
\log A_0=-\log8,
\]

质量守恒消去共同的 `-log 8`，得到完整加速度

\[
A=\frac{m(s)}2\bigl(P^2-\Delta^2-4R^2\bigr)
+g(s)\bigl(H^2+N^2-2PZ\bigr).
\tag{9}
\]

(9) 中的 `PZ` 来自全部对角混合项；`H,N,R` 同时保留三条真实边方向及其混合。合并 (7)–(9)：

\[
\boxed{
\mathcal B_{K_\kappa}(D)
=v^TG_s v+c_H(s)H^2+c_\Delta(s)\Delta^2+c_N(s)N^2,
}\tag{10}
\]

其中

\[
G_s=F_s+
\begin{pmatrix}
m/2&-g&0\\-g&0&0\\0&0&-2m
\end{pmatrix},\tag{11}
\]

\[
c_H=g+\frac{4s}{D_s},\qquad
c_\Delta=2-\frac m2,\qquad
c_N=g+4s.
\tag{12}
\]

对 `0<s<1`，有 `g>0`、`m<0`，故三个标量系数严格为正。只剩证明 `G_s` 正定。

## 5. 三乘三块的解析正定证书

把 (11) 写开：

\[
G_s=\begin{pmatrix}
\frac m2+\frac{4-2s^2-s^4}{2D_s}&
\frac{s(2-s^2)}{D_s}-g&\frac{s^4}{D_s}\\
\frac{s(2-s^2)}{D_s}-g&
\frac{2(2-s^2)}{D_s}&\frac{2s^3}{D_s}\\
\frac{s^4}{D_s}&\frac{2s^3}{D_s}&
-2m+\frac{2s^2(2-s^2)}{D_s}
\end{pmatrix}.\tag{13}
\]

使用

\[
m'(s)=-\frac{2s}{D_s},\qquad g'(s)=\frac2{D_s},
\]

直接求导：

\[
G_s'=\frac1{D_s^2}
\begin{pmatrix}
s(s^4-s^2+1)&s^2(s^2+1)&2s^3(2-s^2)\\
s^2(s^2+1)&4s&2s^2(3-s^2)\\
2s^3(2-s^2)&2s^2(3-s^2)&4s(s^4-3s^2+3)
\end{pmatrix}.\tag{14}
\]

其三个顺序主子式精确为

\[
\Delta_1(G_s')=\frac{s(s^4-s^2+1)}{D_s^2}>0,\tag{15}
\]

\[
\Delta_2(G_s')=\frac{s^2(s^4-s^2+4)}{D_s^3}>0,\tag{16}
\]

\[
\det G_s'=\frac{48s^3}{D_s^3}>0.\tag{17}
\]

这里 `s^4-s^2+1>0`，其余因子也在 `0<s<1` 上严格为正。由 Sylvester 判据，`G_s'` 对每个 `s∈(0,1)` 正定。

另一方面

\[
G_0=\operatorname{diag}(2,4,0)\succeq0.
\]

故对 `s>0`，

\[
G_s=G_0+\int_0^sG_r'\,dr\succ0.\tag{18}
\]

将 (12) 与 (18) 代回 (10)，任意非零 `(P,Z,R,H,Δ,N)` 都给出严格正值。因此

\[
-H''(K_\kappa;D)>0\qquad(D\ne0).
\]

这证明 `σ=1` 的 R2-T1。

若 `σ=-1`，取对角符号矩阵 `S=diag(1,-1,1)`；若还需翻转 `κ` 的符号，再取 `diag(-1,-1,1)`。每个主子式在 `K↦SKS` 下不变，因此八个事件概率和熵不变，而 `D↦SDS` 是实对称方向的双射。故同一结论适用于全部 `κ!=0` 与 `σ=±1`。

## 6. 与旧弱耦合域的严格关系

本族所有 `v_i=x_i(1-x_i)=1/4`，所以

\[
e_{13}=4\kappa,\qquad e_{23}=4\sigma\kappa.
\]

PR #33 的旧条件 `|e_ij|<=1/4` 在本族上等价于

\[
|\kappa|\le\frac1{16}
\quad\Longleftrightarrow\quad s\le\frac1{32}.
\]

R2-T1 覆盖全部 `0<s<1`。例如 `κ=1/3` 时

\[
s=\frac89,\qquad |e_{13}|=|e_{23}|=\frac43,
\]

且 `K` 与 `I-K` 的顺序三阶行列式均为

\[
\frac18-\frac19=\frac1{72}>0.
\]

所以这是一个严格有效、连通、远在旧域外的有理中心。`s↑1` 时最小谱值、最大谱距以及 `p_0=p_{123}` 同时趋边界；(7)–(18) 仍逐点适用于每个严格中心。

新族并不包含整个旧域，旧域也不包含新族：旧域允许一般三条非零边与不等对角元；新族只是一条结构子流形，但在其上把耦合强度完整推进到有效边界。

## 7. 二点条件熵的事件自适应引理

本节给出 R2-T2 所需的独立解析引理。令

\[
A=\begin{pmatrix}x&a\\a&y\end{pmatrix},\qquad 0<A<I_2,
\]

并令 `C(A)=H(X_1|X_2)`。四个事件概率为

\[
p_{11}=xy-a^2,
\quad p_{10}=x(1-y)+a^2,
\quad p_{01}=(1-x)y+a^2,
\quad p_{00}=(1-x)(1-y)-a^2.
\]

条件成功概率为

\[
u=P(X_1=1\mid X_2=1)=x-\frac{a^2}{y},
\]

\[
v=P(X_1=1\mid X_2=0)=x+\frac{a^2}{1-y}.
\]

严格性保证 `0<u<=v<1`。置

\[
r=y(1-y),\qquad w=v-u=\frac{a^2}{r},
\]

并沿任意实方向

\[
E=\begin{pmatrix}d&h\\h&e\end{pmatrix}
\]

定义 `U=u'`、`V=v'`：

\[
U=d-\frac{2ah}{y}+\frac{a^2e}{y^2},
\quad
V=d+\frac{2ah}{1-y}+\frac{a^2e}{(1-y)^2}.
\tag{19}
\]

令

\[
L=\log\frac{v(1-u)}{u(1-v)}\ge0,
\quad A_u=\frac1{u(1-u)},\quad A_v=\frac1{v(1-v)}.
\]

四事件 Fisher 减去 `X_2` 边际 Fisher 后恰为

\[
yA_uU^2+(1-y)A_vV^2.\tag{20}
\]

另一方面，若 `δ=de-h^2`，四事件的加速度 log 比恰为 `-2δL`。由

\[
x=yu+(1-y)v,\qquad a^2=rw
\]

求一次导数并消去 `h`，得到恒等式

\[
\delta=\frac e2(U+V)-\frac{we^2}{4r}
-\frac{r(V-U)^2}{4w}\qquad(a\ne0).\tag{21}
\]

于是完整条件熵负 Hessian 为

\[
\begin{aligned}
-C''(A;E)
={}&\frac{Lw}{2r}\left(e-\frac{r(U+V)}w\right)^2\\
&+\begin{pmatrix}U&V\end{pmatrix}
\begin{pmatrix}
yA_u&-Lr/w\\-Lr/w&(1-y)A_v
\end{pmatrix}
\binom UV.
\end{aligned}\tag{22}
\]

现在证明第二个矩阵正定。令

\[
t=\frac{v(1-u)}{u(1-v)}\ge1.
\]

对 `t>=1`，

\[
\log t\le\frac{t-1}{\sqrt t}.\tag{23}
\]

确切地，写 `q=sqrt(t)>=1`，则右侧减左侧为

\[
q-q^{-1}-2\log q,
\]

其导数是 `(q-1)^2/q^2>=0`，且在 `q=1` 为零。代入本处的 `t`，(23) 给出

\[
L\le\frac{v-u}{\sqrt{u(1-u)v(1-v)}}=w\sqrt{A_uA_v}.\tag{24}
\]

因此 (22) 中二乘二矩阵的行列式满足

\[
\begin{aligned}
&rA_uA_v-\frac{L^2r^2}{w^2}\\
&\qquad\ge rA_uA_v(1-r)>0,
\end{aligned}\tag{25}
\]

因为 `0<r<=1/4`。两个对角元也严格为正，故 (22) 非负；当 `a!=0` 时，它对非零方向严格为正。

若 `a=0`，则 `u=v=x`。直接从

\[
C=yh(x-a^2/y)+(1-y)h(x+a^2/(1-y))
\]

在 `a=0` 求二阶导数，`a^2` 的一阶系数相消，得到

\[
-C''(A;E)=\frac{d^2}{x(1-x)}\ge0.\tag{26}
\]

所以 `C(A)` 对三个真实二点核坐标联合凹。又

\[
H_2(A)=h(y)+C(A),
\]

故

\[
-H_2''(A;E)=\frac{e^2}{y(1-y)}-C''(A;E)\ge0.\tag{27}
\]

该证明的关键是 (20) 与 (24) 使用相同的四事件条件分母，而不是把概率先取统一上、下界。

## 8. 任意二点强块加孤立点：八事件等式

令

\[
K=A\oplus[z],\qquad 0<A<I_2,\quad0<z<1,
\]

但方向 `D` 仍是任意三阶实对称矩阵，允许 `h13,h23` 同时非零。记二点块的四事件概率为 `u_S(t)`，第三点的两个边际概率为 `w_k(t)`，三点八事件概率为 `p_{S,k}(t)`。

在 `t=0`，

\[
p_{S,k}=u_Sw_k.
\]

交叉核元素在主子式中至少二次出现，所以在任意方向下仍有逐事件一阶恒等式

\[
p'_{S,k}=u'_Sw_k+u_Sw'_k.\tag{28}
\]

因此八项 Fisher 完整相加后

\[
\sum_{S,k}\frac{(p'_{S,k})^2}{p_{S,k}}
=\sum_S\frac{(u'_S)^2}{u_S}
+\sum_k\frac{(w'_k)^2}{w_k}.\tag{29}
\]

二阶交叉项并不逐事件消失，但边际化给出

\[
\sum_kp''_{S,k}=u''_S,
\qquad
\sum_Sp''_{S,k}=w''_k=0.\tag{30}
\]

又 `log p_{S,k}=log u_S+log w_k`，故全部八个加速度项满足

\[
\sum_{S,k}p''_{S,k}\log p_{S,k}
=\sum_Su''_S\log u_S.\tag{31}
\]

(28)–(31) 说明连接方向的 Fisher 与所有 `h13 h23` 型二阶混合并未被忽略；它们在完整事件和中精确相消。于是

\[
-H_3''(K;D)
=-H_2''(A;D_{\{1,2\}})+\frac{d_3^2}{z(1-z)}\ge0
\]

由 (27) 得证。这是 R2-T2。

## 9. 一般缺边连通族的无损事件坐标

考虑尚未完全解决的中心

\[
K=\begin{pmatrix}x&0&b\\0&y&c\\b&c&z\end{pmatrix},
\qquad0<K<I.
\]

令 `v1=x(1-x)`、`v2=y(1-y)`，并对 `i,j∈{0,1}` 置

\[
\phi_i=\frac{i-x}{v_1},\qquad \psi_j=\frac{j-y}{v_2}.
\]

因为 `K12=0`，`(X1,X2)` 的边际是独立 Bernoulli 乘积。四个条件概率精确为

\[
t_{ij}=P(X_3=1\mid X_1=i,X_2=j)
=z-b^2\phi_i-c^2\psi_j.\tag{32}
\]

沿任意六方向 `D`，令 `Tij=tij'`。从八事件商式直接求导：

\[
\boxed{
T_{ij}=d_3+b^2d_1\phi_i^2+c^2d_2\psi_j^2
-2bh_{13}\phi_i-2ch_{23}\psi_j
+2bch_{12}\phi_i\psi_j.
}\tag{33}
\]

从原方向

\[
(d_1,d_2,d_3,h_{12},h_{13},h_{23})
\]

到

\[
(d_1,d_2,T_{00},T_{10},T_{01},T_{11})
\]

的 Jacobian 为

\[
\frac{8b^2c^2}{v_1^2v_2^2},\tag{34}
\]

故 `bc!=0` 时变换无损。若

\[
\bar T=E[T_{X_1X_2}],
\]

\[
A_1=(1-y)(T_{10}-T_{00})+y(T_{11}-T_{01}),
\]

\[
A_2=(1-x)(T_{01}-T_{00})+x(T_{11}-T_{10}),
\]

\[
\Delta_{12}T=T_{11}-T_{10}-T_{01}+T_{00},
\]

逆变换是

\[
h_{12}=\frac{v_1v_2}{2bc}\Delta_{12}T,\tag{35}
\]

\[
h_{13}=\frac{b(1-2x)}{2v_1}d_1-\frac{v_1}{2b}A_1,
\quad
h_{23}=\frac{c(1-2y)}{2v_2}d_2-\frac{v_2}{2c}A_2,\tag{36}
\]

\[
d_3=\bar T-\frac{b^2}{v_1}d_1-\frac{c^2}{v_2}d_2.\tag{37}
\]

完整八事件 Fisher 因条件 score 正交而成为

\[
\boxed{
F=\frac{d_1^2}{v_1}+\frac{d_2^2}{v_2}
+\sum_{i,j}P_0(i,j)\frac{T_{ij}^2}{t_{ij}(1-t_{ij})}.
}\tag{38}
\]

这正是本轮所需的事件自适应分母。一般中心的加速度仍含三个条件 log-odds 权重与三点有限差分；把它们与 (38) 联合后的六乘六矩阵尚未获得全域解析证书。R2-T1 是 (32)–(38) 在 `x=y=z=1/2`、`b=±c` 下的完整闭合，而不是对一般路径族的数值外推。

## 10. 范围

- R2-T1 是连通强耦合中心族的完整六方向严格结论。
- R2-T2 是任意一条强边、另外两条中心边为零时的完整六方向半负定结论。
- 一般缺边连通中心、一般严格实三维中心仍未解决。
- 没有把统一平移 log 被积式、Loewner 梯度反单调性或固定全局正余量重新引入证明。
- 本文为作者证明；符号脚本是作者自检，不是独立审阅或形式化证明助理认证。
