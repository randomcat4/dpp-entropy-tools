# 逐步证明 — I05-W3-20260909

版本 v1.0。结论的完整量词见 frozen_statement.md。此文包含理论论证和有限几何常数的有理证书；外部论文不作为任何尚未证明的符号断言的前提。

## 1. 重建概率；保留固定秩面的全部支持

暂取任意实 n×3 等距矩阵 U，任意三行独立。记第 i 行转置为 r_i，w_ij=r_i×r_j，

\[
g_i=r_i^\top r_i,\quad h_{ij}=w_{ij}^\top w_{ij},
\quad q_S=\det(U_S)^2\ (|S|=3).
\]

由 UᵀU=I，

\[
\sum_i r_ir_i^\top=I.
\]

对 U 的二阶 compound matrix 应用 Cauchy–Binet，并在三维中把二次外积通过 Hodge 对偶识别成叉积，得到

\[
\sum_{i<j}w_{ij}w_{ij}^\top=\operatorname{adj}(U^\top U)=I.
\]

这也可逐个矩阵元从 2×2 子式的 Cauchy–Binet 公式得到。再对三阶子式应用同一公式，得

\[
\sum_i g_i=\sum_{i<j}h_{ij}=3,\qquad \sum_{|S|=3}q_S=1. \tag{1}
\]

full-spark 保证 g_i、h_ij、q_S 全为正。

对 0<A<I，写 d=det A，B=A(I−A)⁻¹，K=UAUᵀ。由包含概率作有限容斥，概率生成多项式为 det(I−K+KZ)，其中 Z 是变量的对角矩阵。因 I−K 可逆，把它因式分解并对主子式展开，得到

\[
p_A(S)=\det(I-A)\det((UBU^\top)_S). \tag{2}
\]

这里用了 det(I−UAUᵀ)=det(I−A) 和 K(I−K)⁻¹=UBUᵀ。L 表示只用来计算概率；整个求导路径始终是 A+tV，没有沿 B 或 L 作直线。

置

\[
D_1(A)=A^2+(1-\operatorname{tr}A)A+dI,
\quad D_2(A)=\operatorname{adj}A-dI.
\]

从 (2) 得

\[
\begin{aligned}
p_\varnothing&=\det(I-A),\\
p_i&=r_i^\top D_1(A)r_i,\\
p_{ij}&=w_{ij}^\top D_2(A)w_{ij},\\
p_S&=d q_S\quad(|S|=3). \tag{3}
\end{aligned}
\]

具体地，det(I−A)B=A adj(I−A)=D₁(A)：在 A 的特征向量上，两端特征值均为 λ_i(1−λ_j)(1−λ_k)。二点 Gram 行列式为 wᵀadj(B)w；det(I−A)adj(B)=adj(A)−dI，因为相应特征值是 (1−λ_i)λ_jλ_k。三点公式直接来自 detB。

|S|>3 的概率恒等于零；|S|≤3 的所有概率严格为正，因为 (2) 中相应矩阵正定且相应行独立。因此在 0<A<I 内，熵是有限个光滑函数之和；恒零项按 0log0=0 处理，导数也恒为零。没有丢弃稀有事件，也没有在边界作无依据的求导。

## 2. 合并顶层及新的几何多项式分解

将三点事件合并成质量 d，得分布 P。令

\[
c=-\sum_{|S|=3}q_S\log q_S.
\]

直接展开 −Σdq_S log(dq_S)，得到

\[
\mathcal H(A)=H(P)+cd,\quad
\mathcal H''=-\sum_j(P'_j)^2/P_j-\sum_jP_j''\log P_j+cd''. \tag{4}
\]

为联合处理各层，再对每个支持配置定义固定权重

\[
u_\varnothing=1,\quad u_i=g_i,\quad u_{ij}=h_{ij},\quad u_S=q_S\ (|S|=3),
\qquad Q_S(A)=p_A(S)/u_S.
\]

u 的总和是 8；它本身不是概率分布。只有 u_S Q_S(A) 才是概率。定义

\[
\Phi(A)=-\sum_S u_S Q_S(A)\log Q_S(A),\qquad
G(A)=-\sum_S u_S Q_S(A)\log u_S.
\]

于是 H=Φ+G。Φ 也不被当成某个自由仿射概率的熵；后面保留它的所有二阶项。

令

\[
R_g=\sum_i r_ir_i^\top\log g_i,
\quad R_h=\sum_{i<j}w_{ij}w_{ij}^\top\log h_{ij},
\quad T=R_g+R_h,
\]

\[
t_g=\operatorname{tr}R_g,\quad t_h=\operatorname{tr}R_h,
\quad \ell=t_g+t_h,\quad \beta=t_h-t_g+c.
\]

对 3×3 矩阵写 e₂(A)=((trA)²−tr(A²))/2。恒等式

\[
\operatorname{adj}A=A^2-(\operatorname{tr}A)A+e_2(A)I
\]

给出 D₁=A+adjA−e₂(A)I+dI。把它代入 G 的定义，得到精确多项式

\[
\boxed{G(A)=-\operatorname{tr}(R_gA)-\operatorname{tr}(T\operatorname{adj}A)
+t_g e_2(A)+\beta\det A.} \tag{5}
\]

这是跨层抵消的关键：单层、双层和顶层几何的三次项共同变为 βdetA，而不是分别估计 cdetA 后丢弃其他层。

对实对称 V 令 J=adjV。由三维行列式的极化，或者展开 det(A+tV) 中 t² 的系数，

\[
D^2\det(A)[V,V]=2\operatorname{tr}(AJ),
\quad D^2e_2(A)[V,V]=2\operatorname{tr}J,
\quad D^2\operatorname{adj}(A)[V,V]=2J. \tag{6}
\]

因此

\[
G''_A[V,V]=-2\operatorname{tr}(TJ)+2t_g\operatorname{tr}J
+2\beta\operatorname{tr}(AJ). \tag{7}
\]

特别地，任取标量中心 aI，定义

\[
M_a=2T-2(t_g+a\beta)I,
\quad \mathcal E=2T-\frac{2\ell}{3}I,
\quad m(a)=2(t_g+a\beta)-\frac{2\ell}{3}.
\]

则 tr𝓔=0，M_a=−m(a)I+𝓔，且

\[
G''_{aI}[V,V]=-\operatorname{tr}(JM_a),\qquad
G''_A-G''_{aI}=2\beta\operatorname{tr}((A-aI)J). \tag{8}
\]

(5)–(8) 是已完成的代数恒等式，本身尚不意味着凹性。

## 3. 标量中心的完整 Fisher 恒等式

写 b=1−a，τ=trV，μ_i=r_iᵀVr_i，ν_ij=w_ijᵀVw_ij。在 A=aI 处，四层概率及一阶导数分别为

\[
\begin{array}{c|c|c}
\text{层}&p&p'\\\hline
0&b^3&-b^2\tau\\
1&ab^2g_i&b(\mu_i-a\tau g_i)\\
2&a^2b h_{ij}&a(b\tau h_{ij}-\nu_{ij})\\
3&a^3q_S&a^2\tau q_S.
\end{array} \tag{9}
\]

把全部 (p′)²/p 相加。空层和顶层之和为 τ²；单层、双层平方展开后的交叉项之和为 −4τ²，纯 τ² 项为 3τ²。这里使用 Σμ_i=Σν_ij=τ 及 (1)。因此这些项正好抵消，留下

\[
\boxed{F_a(V)=\frac1a\sum_i\frac{\mu_i^2}{g_i}
+\frac1{1-a}\sum_{i<j}\frac{\nu_{ij}^2}{h_{ij}}.} \tag{10}
\]

该式虽最终仅显含行向量和叉积向量，但由完整四层 Fisher 求和得到；不是用低阶统计投影替换真实 Fisher。

此外，归一化概率在中心为

\[
Q_S(aI)=a^{|S|}b^{3-|S|}. \tag{11}
\]

由于 Σp_A(S)=1，且 Σ|S|p_A(S)=Σ_iP(i∈X)=trK=trA，沿任意 A-affine 方向有

\[
\sum_S u_S Q''_S(A)=0,
\qquad \sum_S |S|u_S Q''_S(A)=0. \tag{12}
\]

log Q_S(aI)=3logb+|S|log(a/b)，所以

\[
\sum_Su_SQ''_S(A)\log Q_S(aI)=0 \tag{13}
\]

对任意 A 也成立。由此在中心

\[
\mathcal H''_{aI}[V,V]=-F_a(V)-\operatorname{tr}(JM_a). \tag{14}
\]

(14) 仍是恒等式；下一节的严格证书与第 5 节的不等式才建立符号。

## 4. 给定 U 的有限几何证书

现在固定 frozen_statement.md 的五点 U。以下四个条件被精确算术验证：

\[
\begin{aligned}
&F_{1/2}(V)\ge\tfrac14\|V\|_F^2\quad\text{对全部实对称 V}; \tag{C1}\\
&\tfrac14\le m(a)\le\tfrac12\quad(0\le a\le1); \tag{C2}\\
&\|\mathcal E\|_{\rm op}\le\tfrac3{20},\qquad
\|\mathcal E\|_F\le\tfrac15; \tag{C3}\\
&|\beta|\le\tfrac18. \tag{C4}
\end{aligned}
\]

严格证书实际给出端点和范数的严格余量。以下说明如何在不信任任何浮点特征值的情况下复算每个条件。

### 4.1 对数的有理区间

对每个正有理 x，用整数 k 使 x=2ᵏy、1≤y<2，并令 z=(y−1)/(y+1)∈[0,1/3)。对 N=32，

\[
L_N(z)=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1},
\qquad
0\le\log y-L_N(z)
\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}. \tag{15}
\]

证明：log((1+z)/(1−z)) 的导数是 2/(1−z²)；对有限几何级数积分，余项为正，再以分母 2N+1 估计正尾和。log2 用同一公式 z=1/3。负整数 k 乘区间时交换端点。全部运算是分数四则运算；没有未定积分或不受控极限。

运行 `python3 code/verify.py --output-dir output` 得到有理外包区间

\[
\begin{aligned}
c&\in[1.90016187646094964396,1.90016187646094964397],\\
t_g&\in[-1.395759756661,-1.395759756660],\\
t_h&\in[-3.183749558375,-3.183749558374],\\
\beta&\in[0.112172074747,0.112172074748],\\
m(0)&\in[0.261486696701,0.261486696702],\\
m(1)&\in[0.485830846196,0.485830846197].
\end{aligned} \tag{16}
\]

这些显示端点是十进制有理数，而非浮点置信区间。m(a) 仿射于 a，所以端点界证明 (C2)，β 区间证明 (C4)。JSON 中的对数相关区间向外舍入到 10⁻²⁴ 网格；程序内部的符号判断使用舍入前的完整分数区间。

### 4.2 Fisher 证书 (C1)

取坐标 v=(V₁₁,V₂₂,V₃₃,V₁₂,V₁₃,V₂₃)，G_F=diag(1,1,1,2,2,2)，则 ||V||F²=vᵀG_Fv。对 x∈R³ 设

\[
f(x)=(x_1^2,x_2^2,x_3^2,2x_1x_2,2x_1x_3,2x_2x_3)^\top.
\]

由 (10)，F₁/₂(V)=vᵀCv，其中明确的有理矩阵是

\[
C=2\sum_{x\in\{r_i,w_{ij}\}}\frac{f(x)f(x)^\top}{x^\top x}.
\]

对 C−G_F/4 作精确 LDLᵀ 分解。递推式为

\[
d_i=C^*_{ii}-\sum_{k<i}L_{ik}^2d_k,
\quad L_{ji}=\frac{C^*_{ji}-\sum_{k<i}L_{jk}L_{ik}d_k}{d_i},
\quad C^*=C-G_F/4.
\]

其六个枢轴的严格有理外包区间为

\[
\begin{aligned}
&[1.943390640,1.943390641],\quad[1.871852536,1.871852537],\\
&[0.853386562,0.853386563],\quad[2.057146120,2.057146121],\\
&[1.326121151,1.326121152],\quad[0.163703956,0.163703957].
\end{aligned} \tag{17}
\]

全部为正，且程序以分数恒等式重新相乘核对 LDLᵀ=C*。这证明 C*>0，从而证明 (C1)。完整 C、G_F、C*、L 和六个精确有理枢轴都在 output/certificate.json 中。输入 U 和上式已完全确定这项有限证书，不依赖任何缺失样本。

### 4.3 几何各向异性证书 (C3)

设

\[
E_0=10^{-6}\begin{pmatrix}
71&72690&52507\\
72690&-42720&-74600\\
52507&-74600&42650
\end{pmatrix}.
\]

由 (15) 逐项计算可证 |𝓔_ij−(E₀)_ij|≤10⁻⁶。记 e=10⁻⁶。于是 ||𝓔−E₀||op≤3e。精确 LDLᵀ 证明两个有理矩阵

\[
(3/20-3e)I+E_0,\qquad(3/20-3e)I-E_0
\]

均正定；它们的枢轴区间分别为

\[
\begin{aligned}
+E_0:&\ [0.150068000,0.150068000],\ [0.072067387,0.072067388],\ [0.035423807,0.035423808],\\
-E_0:&\ [0.149926000,0.149926000],\ [0.157474039,0.157474040],\ [0.073622229,0.073622230].
\end{aligned}
\]

因此 −3I/20<𝓔<3I/20，证明算子范数界。另有直接分数比较

\[
\|\mathcal E\|_F^2\le\sum_{i,j}(|(E_0)_{ij}|+e)^2
=\frac{15428479159}{500000000000}<\frac1{25},
\]

证明 Frobenius 范数界。以上没有把谱数值近似当作严格符号。

## 5. 真正的中心补偿不等式

将任意实对称 V 写成 V=sI+W，其中 trW=0，令 x=||W||F。由紧框架恒等式，

\[
\sum_i\frac{(r_i^\top Vr_i)^2}{g_i}
=3s^2+\sum_i\frac{(r_i^\top Wr_i)^2}{g_i},
\]

叉积层同理。由于 a(1−a)≤1/4、1/a≥1、1/(1−a)≥1，(10) 与 (C1) 给出

\[
F_a(V)\ge12s^2+\frac12F_{1/2}(W)
\ge12s^2+\frac18x^2. \tag{18}
\]

无迹分解还给出

\[
\operatorname{adj}(sI+W)=s^2I-sW+W^2-\tfrac12x^2I.
\]

用 M_a=−mI+𝓔、tr𝓔=0 展开，而不是假定 V 与任何矩阵交换：

\[
\operatorname{tr}(JM_a)
=-3ms^2-s\operatorname{tr}(W\mathcal E)
+\frac m2x^2+\operatorname{tr}(W^2\mathcal E). \tag{19}
\]

由 (C2)–(C3)，|tr(W𝓔)|≤x/5，且 tr(W²𝓔)≥−3x²/20。将 (18) 的 7/8 与 (19) 相加，得到

\[
\begin{aligned}
\tfrac78F_a(V)+\operatorname{tr}(JM_a)
&\ge9s^2+\left(\frac7{64}+\frac18-\frac3{20}\right)x^2-\frac15|s|x\\
&=9s^2+\frac{27}{320}x^2-\frac15|s|x.
\end{aligned}
\]

由 (|s|−x/10)²≥0，最后一项的绝对值至多 s²+x²/100。因此

\[
\tfrac78F_a(V)+\operatorname{tr}(JM_a)
\ge8s^2+\frac{119}{1600}x^2
\ge\frac{119}{1600}(3s^2+x^2).
\]

所以

\[
\boxed{\tfrac78F_a(V)+\operatorname{tr}(JM_a)
\ge\tfrac{119}{1600}\|V\|_F^2.} \tag{20}
\]

这对全部 0<a<1 成立，是在完整四层上证明的严格补偿储备。保留 1/8 的 Fisher 余量，是为了控制非标量中心的变化。

## 6. 向非交换开放范围转移：全部误差项

现在固定 a∈(0,1)，ε=min(a,1−a)，A=aI+Z，δ=||Z||op≤ε²/1000，ρ=δ/ε≤1/2000。因为 δ<ε，A 的谱严格包含于 (0,1)。以下方向 V 完全任意；不要求 [Z,V]=0。

### 6.1 概率相对变化的统一界

D₁(A) 在 A 的特征向量上的特征值为 λ_i(1−λ_j)(1−λ_k)，D₂(A) 为 (1−λ_i)λ_jλ_k。由于所有 λ_i∈[a−δ,a+δ]，每个因子相对其中心值的比在 [1−ρ,1+ρ] 中。

Q_i 和 Q_ij 是相应矩阵沿单位向量 r_i/√g_i、w_ij/√h_ij 的 Rayleigh 商；即使这些向量不与 A 的特征向量重合，仍在该矩阵的极端特征值之间。空层和顶层是三个因子的乘积。因此对全部支持配置 S，

\[
(1-\rho)^3\le\frac{Q_S(A)}{Q_S(aI)}\le(1+\rho)^3,
\quad Q_S(aI)\ge\varepsilon^3. \tag{21}
\]

于是

\[
\left|\log\frac{Q_S(A)}{Q_S(aI)}\right|
\le\frac{3\rho}{1-\rho}. \tag{22}
\]

这里使用 log(1+ρ)≤ρ、−log(1−ρ)≤ρ/(1−ρ)，均由积分 1/(1±t) 的单调界直接得到。

### 6.2 归一化概率的二阶导数界

令 σ=||V||F²、J=adjV。若 V 的特征值为 λ₁,λ₂,λ₃，则

\[
\|J\|_* =|\lambda_1\lambda_2|+|\lambda_1\lambda_3|+|\lambda_2\lambda_3|
\le\lambda_1^2+\lambda_2^2+\lambda_3^2=\sigma,
\quad \|J\|_{\rm op}\le\sigma/2. \tag{23}
\]

第一式由三个非负数 |λ_i| 的成对差平方和非负得到；第二式由 2|λ_iλ_j|≤λ_i²+λ_j² 得到。

根据 (3) 和 (6)，对任意 0<B<I（这里 B 只是当前位置，不是第 1 节的 L 坐标），归一化概率的二阶导数恰为

\[
\begin{aligned}
Q''_\varnothing(B)&=2\operatorname{tr}((I-B)J),\\
Q''_i(B)&=2\widehat r_i^\top J\widehat r_i-2\operatorname{tr}((I-B)J),\\
Q''_{ij}(B)&=2\widehat w_{ij}^\top J\widehat w_{ij}-2\operatorname{tr}(BJ),\\
Q''_S(B)&=2\operatorname{tr}(BJ)\quad(|S|=3),
\end{aligned} \tag{24}
\]

其中帽号表示单位化。由 ||B||op、||I−B||op≤1 及 (23)，

\[
|Q''_S(B)|\le C_{|S|}\sigma,
\qquad (C_0,C_1,C_2,C_3)=(2,3,3,2). \tag{25}
\]

这些 Hessian 是实对称双线性型；(25) 对所有 V 成立，所以它们相对于 Frobenius 内积的算子范数至多 3。由谱定理或极化，

\[
|D^2Q_S(B)[Z,V]|\le3\|Z\|_F\|V\|_F.
\]

从 aI 到 A 的线段完全留在 0<B<I 内。沿此线段应用微积分基本定理，并用 ||Z||F≤√3δ，得到

\[
|DQ_S(A)[V]-DQ_S(aI)[V]|
\le3\sqrt3\delta\|V\|_F. \tag{26}
\]

这一步处理了真正的非交换混合导数；没有沿谱坐标把 V 对角化。

### 6.3 完整 Fisher 的稳定下界

写 F_A(V)=Σu_S(DQ_S(A)[V])²/Q_S(A)。置

\[
X_S=\sqrt{u_S/Q_S(aI)}DQ_S(aI)[V],
\quad Y_S=\sqrt{u_S/Q_S(aI)}(DQ_S(A)[V]-DQ_S(aI)[V]).
\]

由 (1)、(21)、(26)，

\[
\sum_SX_S^2=F_a(V),\qquad
\sum_SY_S^2\le\frac{216\delta^2}{\varepsilon^3}\sigma. \tag{27}
\]

常数 216=8×27，来自全部固定权重总和 8。

对任意实数 x,y，2xy≥−x²/10−10y² 给出

\[
(x+y)^2\ge\tfrac9{10}x^2-9y^2.
\]

由 (21)，

\[
F_A(V)\ge\frac{(9/10)F_a(V)-9\sum_SY_S^2}{(1+\rho)^3}.
\]

由于 (9/10)/(1+1/2000)³>7/8，而 (1+ρ)⁻³≤1，得

\[
\boxed{F_A(V)\ge\tfrac78F_a(V)-\frac{1944\delta^2}{\varepsilon^3}\sigma.} \tag{28}
\]

这里未丢弃任何配置的 Fisher。

### 6.4 log 加速的完整控制

使用 (13)，定义保留全部配置的加速余项

\[
\mathcal R_a(A,V)=\sum_Su_SQ''_S(A)
\log\frac{Q_S(A)}{Q_S(aI)}.
\]

由 (1)、(22)、(25)，

\[
\begin{aligned}
|\mathcal R_a(A,V)|
&\le\frac{3\rho}{1-\rho}\sigma(2\cdot1+3\cdot3+3\cdot3+2\cdot1)\\
&=\frac{66\rho}{1-\rho}\sigma. \tag{29}
\end{aligned}
\]

常数 22 中的四项依次来自空层、单层、双层、顶层。先作 (5) 和 (13) 的跨层精确抵消，再估计这个余项；不是分别丢弃低层加速后证明更强的错误界。

几何部分由 (8)、(23)、(C4) 满足

\[
|G''_A-G''_{aI}|\le2|\beta|\delta\sigma\le\delta\sigma/4. \tag{30}
\]

### 6.5 合并所有误差并完成定理

从 H=Φ+G、(13) 以及有限概率的熵求导公式，

\[
\mathcal H''_A[V,V]=-F_A(V)-\mathcal R_a(A,V)+G''_A[V,V].
\]

代入 (8)、(20)、(28)–(30)，

\[
\mathcal H''_A[V,V]\le
-\left(\frac{119}{1600}
-\frac{1944\delta^2}{\varepsilon^3}
-\frac{66\rho}{1-\rho}-\frac\delta4\right)\sigma. \tag{31}
\]

因为 ε≤1/2、δ≤ε²/1000、ρ≤1/2000，三项误差分别不超过

\[
\frac{243}{250000},\qquad \frac{66}{1999},\qquad \frac1{16000}.
\]

最后是严格的有理数比较：

\[
\frac{119}{1600}-\frac{243}{250000}-\frac{66}{1999}-\frac1{16000}
=\frac{161215319}{3998000000}
=\frac1{25}+\frac{1295319}{3998000000}>\frac1{25}.
\]

因此，对所声明参数范围内的全部 A、全部实对称 V，

\[
\boxed{\mathcal H''_A[V,V]\le-\frac1{25}\|V\|_F^2.}
\]

V=0 时等号成立；V≠0 时严格小于零。证明完成。

## 7. 回到题面补偿不等式与弦

把刚证明的不等式代回完全重建的 (4)，得到

\[
\sum_j(P'_j)^2/P_j+\sum_jP_j''\log P_j
\ge cd''+\|V\|_F^2/25.
\]

这里的符号来自第 4–6 节的定理，不是仅由 (4) 的等价重写宣称得到。

若整个对称线段留在一个定理闭球中，对 f(t)=H(A+tV) 应用

\[
\frac{f(h)+f(-h)}2-f(0)
=\frac12\int_0^h(h-s)(f''(s)+f''(-s))\,ds,
\]

得到弦差≤−h²||V||F²/50。有限闭球严格处于 0<A<I，函数在其附近光滑，这个积分没有奇异端点。

## 8. 非交换且顶层自身失控的明确例子

取

\[
A_* =\operatorname{diag}(5001/10000,4999/10000,1/2),
\quad V_* = I+(E_{12}+E_{21})/10.
\]

有 ||A_*−I/2||op=1/10000<1/4000，[A_*,V_*]₁₂=1/50000，故确实不交换。det(A_*+tV_*) 可以直接展开为

\[
\left[(1/2+t)^2-10^{-8}-t^2/100\right](1/2+t).
\]

所以

\[
d=\frac{24999999}{200000000},\quad
 d'=\frac{74999999}{100000000},\quad d''=\frac{299}{100}.
\]

由 c>19/10，一个纯有理数比较给出

\[
cd''>\frac{19}{10}\frac{299}{100}
>\frac54\frac{(d')^2}{d}.
\]

而第 6 节的定理给出 H''≤−151/1250；完整事件求和的有理区间计算进一步给出

\[
H''\in[-10.895113009930,-10.895113009929].
\]

全部概率和两阶导数随包提供。此例仅证明该开放范围确实包含“顶层几何曲率超过顶层 Fisher”的非交换情形，绝不是正弦反例。

## 9. 可移植的充分判据及准确限制

第 1–3、5–7 节对任意实 full-spark n×3 等距 U 都成立。只要它的几何常数满足 (C1)–(C4)，同样得到半径 ε²/1000、曲率余量 1/25 的定理。因此产物不仅是一个固定点 Hessian 的符号检查，还给出了由紧框架 Fisher 间隙、几何各向异性和跨层三次系数组成的充分判据。

本次仅对题面指定的 U 验证这些条件，不断言所有 full-spark U 满足它们。没有证明 ε²/1000 之外的普遍补偿。δ 不小时 (29) 的绝对值界会失去所需余量；这是本证明的实际覆盖边界，不是目标命题的反例。

尚未独立审阅；以上程序交叉核验属于作者自检。
