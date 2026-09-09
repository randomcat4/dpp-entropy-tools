\begin{pmatrix}b&a&-1\end{pmatrix}.
\tag{3.8}
\]

`G` 正定：由 (3.3)，`y != 0` 时事件导数向量 `x != 0`，而四个 `A_i` 全正，所以 `F>0`。

记

\[
P=A_0A_1A_2A_3,
\qquad
E=A_0A_3(A_0+A_3)+A_1A_2(A_1+A_2).
\]

直接展开 (3.7)–(3.8)，并只使用 `sum A_i=1`，得到精确恒等式

\[
\boxed{
\det(G-\lambda Q)
=\frac{16r+4\lambda E-\lambda^3P}{16rP}.
}
\tag{3.9}
\]

`lambda^2` 系数完全消去。`code/verify.py` 用符号有理式独立检查 (3.9)，但后续符号论证不依赖浮点计算。

### 3.3 两个标量不等式

令

\[
X=A_0A_3,
\qquad Y=A_1A_2,
\]

则 `r=Y-X>0`、`P=XY`、`Lambda=log(Y/X)>0`。首先

\[
\sqrt P\,\Lambda\le r.
\tag{3.10}
\]

事实上，令 `z=sqrt(Y/X)>1`，则 (3.10) 等价于

\[
2z\log z\le z^2-1.
\]

右减左在 `z=1` 为零，其导数是 `2(z-1-log z)>=0`，故成立。于是

\[
P\Lambda^2\le r^2.
\tag{3.11}
\]

其次，

\[
E>4r^2.
\tag{3.12}
\]

令 `p=sqrt(X)`、`q_0=sqrt(Y)` 和 `theta=A_0+A_3`。AM–GM 给

\[
\theta\ge2p,
\qquad1-\theta=A_1+A_2\ge2q_0,
\qquad p+q_0\le\frac12.
\]

因此

\[
E=X\theta+Y(1-\theta)\ge2(p^3+q_0^3).
\]

写 `sigma=p+q_0`，则 `2sigma<=1`，并且

\[
\begin{aligned}
2(p^3+q_0^3)-4(q_0^2-p^2)^2
&=2\sigma\left[p^2-pq_0+q_0^2-2\sigma(q_0-p)^2\right]\\
&\ge2\sigma\left[p^2-pq_0+q_0^2-(q_0-p)^2\right]\\
&=2\sigma p q_0>0.
\end{aligned}
\]

因为 `r=q_0^2-p^2`，即得 (3.12)。

### 3.4 Hessian 非正

对任意 `0<=lambda<=2Lambda`，由 (3.11)，

\[
\lambda^3P
\le\lambda(2\Lambda)^2P
\le4\lambda r^2.
\]

故 (3.9) 的分子满足

\[
16r+4\lambda E-\lambda^3P
\ge16r+4\lambda(E-r^2)>0.
\tag{3.13}
\]

于是 `G-lambda Q` 在 `[0,2Lambda]` 上从不奇异。它在 `lambda=0` 正定；实对称矩阵的惯性只能在特征值经过零时改变，所以 `G-2Lambda Q` 仍正定。结合 (3.5)，

\[
H''(L)[V,V]
=-y^{\mathsf T}(G-2\Lambda Q)y<0
\]

对 `c != 0` 和非零 `V` 成立。

若 `c=0`，则 (3.2) 给 `A_1A_2=A_0A_3`，所以 `Lambda=0`，未除以 `r` 的式 (3.5) 直接给

\[
H''(L)[V,V]=-F\le0.
\]

因此完整熵在严格实 `2 x 2` 收缩核的凸域上 Hessian 半负定，沿任意合法真实仿射直线凹。虽然纯非对角方向在对角中心可有瞬时二阶导数为零，但整条非平凡弦仍严格：离开该单点后 `c != 0`，二阶导数严格负；纯对角非零方向则 `F>0`。连续延拓处理合法边界。

## 4. 两坐标支撑方向的任意维提升

先证明一个独立有用的结论。令 `L(z)=L_0+zD` 是任意维严格实 DPP 核的真实仿射线，且 `D` 只支撑在坐标集合 `J` 的主块 `J x J` 上，其中 `|J|<=2`。把其余坐标记为 `R=J^c`，分块写

\[
L(z)=\begin{pmatrix}
A&F\\F^{\mathsf T}&C+zD_J
\end{pmatrix}.
\]

