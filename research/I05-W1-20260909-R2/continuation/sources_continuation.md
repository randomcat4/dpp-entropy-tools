# sources_continuation.md

本轮先核对原始来源，再自行推导所需桥接。来源只用于定义、已知输入和方法边界；除第 1 项外，没有任何来源被当作现成的 DPP 配置熵凹性定理。新颖性未认证。

## 1. 本轮采用的外部已证明输入：对角锚点直线凹性

另一独立团队的冻结材料：

- 仓库目录：`research/C3/`
- 固定提交：`648f1906468e3e548410f98a6b1a53a978f2ea11`
- 主要入口：`research/C3/proof.md`、`research/C3/frozen_statement_v2.md`、`research/C3/verification.md`

本轮只采用用户明确给出的有限维结论：对任意严格对角 Hermitian 核 `D` 和固定 Hermitian 方向 `V`，`u -> H(D+uV)` 在整条合法直线上凹。其原证明通过逐坐标独立刷新构造通道。本轮没有重做或扩大该团队的审阅，只证明它如何经条件 Schur 分解传递到新的跨块族。

## 2. 有限 DPP、条件化和谱混合

Russell Lyons, **Determinantal probability measures**, Publications Mathématiques de l'IHÉS 98 (2003), arXiv:`math/0204325`。

用途：有限 DPP 的包含概率、条件化/补集等标准背景。本文逐完整事件的 Schur 恒等式仍在正文中从事件行列式直接证明，不用引用替代代数步骤。

J. Ben Hough, Manjunath Krishnapur, Yuval Peres, Bálint Virág, **Determinantal processes and independence**, Probability Surveys 3 (2006), arXiv:`math/0503110`。

用途：谱 Bernoulli/投影 DPP 混合是潜在信息收缩路线的背景。本文没有把潜在谱变量当作观测配置的充分统计量，也没有由该表示宣称熵凹性。

## 3. 强负相关与 Markov 链背景

Julius Borcea, Petter Brändén, Thomas M. Liggett, **Negative dependence and the geometry of polynomials**, Journal of the American Mathematical Society 22 (2009), arXiv:`0707.2340`。

用途：强 Rayleigh/负相关背景。本文没有从负相关直接推出 Shannon 熵曲率，也没有把一般 Glauber 动力学假定成所需外幂特征半群。

## 4. 费米准自由态和 Gaussian/quasi-free 通道

Sergey Bravyi, **Lagrangian representation for fermionic linear optics**, Quantum Information and Computation 5 (2005), arXiv:`quant-ph/0404180`。

用途：费米 Gaussian/准自由态及线性通道的协方差描述背景。

B. Dierckx, M. Fannes, M. Pogorzelska, **Fermionic Gaussian channels**, Journal of Mathematical Physics 49 (2008), arXiv:`0709.1061`。

用途：规范不变准自由通道可在一粒子协方差层作仿射变换的背景。本文只使用一个满足 `0<=A_0<=I` 的显式衰减实例，并自行逐事件证明：相关固定点通道一般不下降为只作用于占据配置概率的经典随机核。

## 5. 本文自包含、没有外借符号结论的部分

下列步骤均在证明文件中直接给出：

- 条件完整事件分解 `p_{K(t)}(S,T)=p_A(S)p_{C-sM_S}(T)`；
- 对角活动约化扇区的熵链提升；
- 二维 Cauchy--Binet/mixed-discriminant 公式
  `det(sum z_i v_i v_i^T)=sum_{i<j}z_i z_j det(v_i,v_j)^2`；
- 外幂特征 Markov 交织；
- 生成元熵导数与完整 Fisher 公式；
- 两模准自由测量障碍的有理概率计算。

## 6. 精确适用边界

上述文献没有直接证明本轮一般目标：两侧相关大块、一般非坐标 `rank(B)=2` 的整条径向配置 Shannon 熵凹性。特别地：

- 谱混合不提供观测配置上的自动 Markov 闭合；
- 强 Rayleigh 性不自动给所需二阶熵耗散不等式；
- 量子相对熵数据处理不自动传递到固定占据基的经典测量熵；
- 一般正交单粒子变换不保持观测配置 Shannon 熵。
