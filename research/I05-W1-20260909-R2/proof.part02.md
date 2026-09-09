因此 `C_S(s)` 和 `I-C_S(s)` 的所有主子式，特别是所有顺序首主子式，均严格为正。Sylvester 判据给出

\[
0<C_S(s)<I.
\tag{2.2}
\]

所以条件分布不只是形式上的带符号行列式，而是真正的严格 DPP。

### 2.3 熵的精确链式分解

左右边际核始终分别为 `A,C`，故左块完整事件权重 `p_A(S)` 与 `t` 无关。Shannon 链式法则和 (2.1) 给出

\[
\boxed{
H(K(t))=H(A)+\sum_{S\subseteq[m]}p_A(S)H(C-sM_S).
}
\tag{2.3}
\]

定义

\[
G(s)=H(K(\sqrt s)),\qquad 0\le s<\tau^2,
\]

其中 `(-tau,tau)` 是严格合法 `t` 区间。则 (2.3) 就是冻结式 (A2)。

### 2.4 一个有用的零均值恒等式

对任意实对称方向 `D`，在 `A` 附近微扰，(1.1) 给出

\[
\left.\frac{d}{dz}p_{A+zD}(S)\right|_{z=0}
=p_A(S)\operatorname{tr}(X_S^{-1}D).
\]

总概率恒为一，故对所有对称 `D`，

\[
0=\sum_Sp_A(S)\operatorname{tr}(X_S^{-1}D).
\]

Frobenius 配对在对称矩阵空间上非退化，因此

\[
\boxed{
\sum_Sp_A(S)X_S^{-1}=0,
\qquad
\sum_Sp_A(S)M_S=0.
}
\tag{2.4}
\]

当需要微分时，(2.4) 直接给 `G'(0)=0`。后面的全局证明甚至不需要在零点微分，而只用独立分布是固定边际下的最大熵耦合。

## 3. 自包含低维输入：实 `2 x 2` 完整熵全局凹

本节证明后续唯一需要的维数特定引理。

### 3.1 四个完整事件及 Hessian

写

\[
L=\begin{pmatrix}a&c\\c&b\end{pmatrix},
\qquad
V=\begin{pmatrix}u&w\\w&v\end{pmatrix},
\]

并令 `d=ab-c^2`、`q=uv-w^2`。严格收缩时四个完整概率为

\[
A_0=1-a-b+d,
\quad A_1=a-d,
\quad A_2=b-d,
\quad A_3=d.
\tag{3.1}
\]

它们严格为正、和为一，并满足

\[
A_1A_2-A_0A_3=c^2=:r\ge0.
\tag{3.2}
\]

沿 `L+zV`，令

\[
\alpha=d'(0)=bu+av-2cw.
\]

四概率的一阶导数是

\[
x=(-u-v+\alpha,\;u-\alpha,\;v-\alpha,\;\alpha),
\tag{3.3}
\]

二阶导数是

\[
p''=2q(1,-1,-1,1).
\tag{3.4}
\]

因此完整 Shannon 熵的二阶方向导数为

\[
H''(L)[V,V]=-F+2q\Lambda,
\tag{3.5}
\]

其中

\[
F=\sum_{i=0}^3\frac{x_i^2}{A_i},
\qquad
\Lambda=\log\frac{A_1A_2}{A_0A_3}\ge0.
\tag{3.6}
\]

这里第一项是完整四事件 Fisher 代价；第二项没有删去任何事件。

### 3.2 `c != 0` 时的矩阵铅笔

若 `c != 0`，则 `r>0`。用 `y=(u,v,alpha)^T` 作坐标。由

\[
w=\frac{bu+av-\alpha}{2c},
\]

这是从 `(u,v,w)` 到 `y` 的可逆线性变换。存在对称矩阵 `G,Q` 使

\[
F=y^{\mathsf T}Gy,
\qquad q=y^{\mathsf T}Qy,
\]

其中

\[
G=\begin{pmatrix}
A_0^{-1}+A_1^{-1}&A_0^{-1}&-A_0^{-1}-A_1^{-1}\\
A_0^{-1}&A_0^{-1}+A_2^{-1}&-A_0^{-1}-A_2^{-1}\\
-A_0^{-1}-A_1^{-1}&-A_0^{-1}-A_2^{-1}&
\sum_{i=0}^3A_i^{-1}
\end{pmatrix},
\tag{3.7}
\]

\[
Q=\begin{pmatrix}0&1/2&0\\1/2&0&0\\0&0&0\end{pmatrix}
-\frac1{4r}
\begin{pmatrix}b\\a\\-1\end{pmatrix}
