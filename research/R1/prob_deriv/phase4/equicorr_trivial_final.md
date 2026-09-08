RETIRED_INCOMPLETE

# P4 trivial S3 sector final unit

本文件只审计冻结复合对称中心的 trivial \(S_3\) 扇区，即方向由 \(I\) 与 \(J-I\) 张成的二维平面。记
\[
0<\lambda,\mu<1,\qquad L=\log 3,
\]
其中 \(\lambda=a-c\) 是重数为 2 的特征值，\(\mu=a+2c\) 是重数为 1 的特征值。完整事件概率按 DPP 事件语义为
\[
p_0=(1-\lambda)^2(1-\mu),
\]
\[
p_1={ (1-\lambda)(2\lambda+\mu-3\lambda\mu)\over 3}
\quad\text{每个 singleton},
\]
\[
p_2={ \lambda(\lambda+2\mu-3\lambda\mu)\over 3}
\quad\text{每个 pair},
\]
\[
p_3=\lambda^2\mu .
\]
令
\[
r_0=p_0,\quad r_1=3p_1,\quad r_2=3p_2,\quad r_3=p_3 .
\]
则 \((r_0,r_1,r_2,r_3)\) 是
\[
N=B_\lambda+B_\lambda+B_\mu
\]
的概率分布，其中三个 Bernoulli 变量独立。因此完整事件熵精确分解为
\[
H(\lambda,\mu)=H(N)+(r_1+r_2)L. \tag{1}
\]
这里第二项不是常数；它的 Hessian 不定，所以不能仅引用 Shepp--Olkin 的 Bernoulli-sum 熵凹性。

## Hessian 分解

设
\[
G=\nabla^2_{\lambda,\mu}H(N),\qquad s=r_1+r_2.
\]
直接计算
\[
s=\mu+2\lambda-\lambda^2-2\lambda\mu,
\]
从而
\[
\nabla^2(sL)
=L\begin{pmatrix}-2&-2\\-2&0\end{pmatrix}
=:C. \tag{2}
\]
矩阵 \(C\) 的特征值为 \(L(-1-\sqrt5)\) 与 \(L(-1+\sqrt5)\)，因此 \(C\) 不定。完整 Hessian 为
\[
M:=\nabla^2 H=G+C.
\]

Shepp--Olkin 给出 \(H(N)\) 对 Bernoulli 参数 \((\lambda_1,\lambda_2,\mu)\) 的凹性；沿仿射切片 \(\lambda_1=\lambda_2=\lambda\) 限制后，
\[
G\preceq 0,\qquad \det G\ge 0. \tag{3}
\]
这只覆盖 Bernoulli-sum 熵项，不能覆盖完整事件熵。

由 (2) 得
\[
M_{\lambda\lambda}=G_{\lambda\lambda}-2L,
\]
\[
M_{\lambda\mu}=G_{\lambda\mu}-2L,
\]
\[
M_{\mu\mu}=G_{\mu\mu}. \tag{4}
\]
于是
\[
M_{\lambda\lambda}\le -2L<0. \tag{5}
\]
同时，因为每个 \(r_i\) 对 \(\mu\) 都是仿射函数，
\[
M_{\mu\mu}=G_{\mu\mu}
=-\sum_{i=0}^3 {(\partial_\mu r_i)^2\over r_i}<0 \tag{6}
\]
在内部严格成立；非零性来自四个内部概率均正，且 \(\partial_\mu r_i\) 不可能全部为零。

因此本单元已经闭合两个主对角二阶项，且 \(\lambda\lambda\) 方向还得到一个严格余量 \(-2\log3\)。剩余问题只剩 Hessian 行列式。

## 剩余的单一标量符号

由 (4) 展开，
\[
\det M
=\det G-2L\bigl(G_{\mu\mu}-2G_{\lambda\mu}+2L\bigr). \tag{7}
\]
所以完整凹性在本二维扇区中等价于以下单一标量不等式：
\[
\Phi(\lambda,\mu)
:=\det G-2L\bigl(G_{\mu\mu}-2G_{\lambda\mu}+2L\bigr)\ge 0
\quad (0<\lambda,\mu<1). \tag{8}
\]
这就是本轮未闭合的最小缺口。

为了使 (8) 完全可审查，\(G\) 可不用任何数值近似写成
\[
G_{uv}
=-\sum_{i=0}^3
\left[
(\partial_{uv}r_i)\log r_i
+
{(\partial_u r_i)(\partial_v r_i)\over r_i}
\right],
\qquad u,v\in\{\lambda,\mu\}, \tag{9}
\]
其中 \(\sum_i \partial_{uv}r_i=0\)，故没有遗漏来自 \(-r\log r\) 的常数项。具体地，
\[
r_0=(1-\lambda)^2(1-\mu),
\]
\[
r_1=(1-\lambda)(2\lambda+\mu-3\lambda\mu),
\]
\[
r_2=\lambda(\lambda+2\mu-3\lambda\mu),
\]
\[
r_3=\lambda^2\mu .
\]

也可把 \(M_{\lambda\lambda}\) 与 \(M_{\lambda\mu}\) 的 log 部分写为两个基本 log 比值。令
\[
\alpha=\log {r_1^2\over 3r_0r_2},\qquad
\beta=\log {r_2^2\over 3r_1r_3}.
\]
Poisson-binomial 分布的 ultra-log-concavity 给出 \(\alpha,\beta\ge0\)，且在 \(\lambda=\mu\) 时二者同为 \(0\)。用这些量可以重写
\[
M_{\lambda\lambda}
=2\bigl((1-\mu)\alpha+\mu\beta\bigr)
-\sum_{i=0}^3{(\partial_\lambda r_i)^2\over r_i},
\]
\[
M_{\lambda\mu}
=2\bigl((1-\lambda)\alpha+\lambda\beta\bigr)
-\sum_{i=0}^3{(\partial_\lambda r_i)(\partial_\mu r_i)\over r_i}.
\]
这些公式解释了为什么单独控制 log 比值不足以自动推出行列式符号：行列式中存在 Fisher 型有理项与 log 比值项的二次补偿，而补偿必须按 (8) 同时处理。

## 对角线一致性与严格性边界

在 \(\lambda=\mu=r\) 上，完整分布退化为三个独立 Bernoulli\((r)\) 坐标的乘积分布。直接代入得到
\[
\nabla^2 H(r,r)
=-{1\over 3r(1-r)}
\begin{pmatrix}
4&2\\
2&1
\end{pmatrix}. \tag{10}
\]
因此
\[
\det\nabla^2 H(r,r)=0,
\]
零方向为 \((1,-2)\)，即固定平均对角 \(a=(2\lambda+\mu)/3\) 的纯非对角二阶方向。这与冻结二阶结论中“纯非对角零曲率”一致，也说明 (8) 若成立只能是半正行列式，不可能在全内部处处严格。

## 为什么本轮退休

本轮没有再做网格扫描，也没有安装依赖。尝试用 Shepp--Olkin 与修正项精确合并后，得到：

1. \(M_{\lambda\lambda}<0\) 已由 \(G\preceq0\) 和 \(-2\log3\) 余量闭合；
2. \(M_{\mu\mu}<0\) 已由 \(\mu\)-仿射性直接闭合；
3. 唯一未闭合项是 (8) 的标量行列式补偿 \(\Phi(\lambda,\mu)\ge0\)。

一个更弱的充分条件
\[
G_{\mu\mu}-2G_{\lambda\mu}+2L\le0
\]
在对角线附近不成立，因此不能用它代替 (8)。剩余的正确证明必须展示 \(\det G\) 如何精确补偿该正项；本单元未能找到这样的代数证书。按“若仍卡同一两条不等式即停止”的规则，当前路线退休，状态记为 `RETIRED_INCOMPLETE`。

## 命令与失败记录

- 未启动子智能体；未访问 R2/R3；未访问 `C:\canglan\`；未安装依赖；未运行新网格。
- 一次非网格符号因式分解尝试因本地缺少 `sympy` 失败，退出码 `1`；未安装依赖，未修改任何文件。
- 前置代数恒等式检查曾确认 (7) 的展开关系，退出码 `0`；该检查只用于核对公式，不作为凹性证明。
