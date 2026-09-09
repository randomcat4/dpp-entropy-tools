# sources_continuation.md

本轮来源只用于定义、外部已知输入和方法边界；三点不定秩二定理、外幂充分统计、三点条件判据及相关 `3+3` 族均在 PR #43 中自包含推导。新颖性未认证。

## 1. 本轮采用的外部输入：对角锚点直线凹性

另一独立团队的仓库材料：

- `research/C3/`
- 固定提交 `648f1906468e3e548410f98a6b1a53a978f2ea11`
- 入口 `research/C3/proof.md`、`frozen_statement_v2.md`、`verification.md`

本 PR 只采用以下有限维结论：对任意严格对角 Hermitian 核 `D` 和固定 Hermitian 方向 `V`，`u\mapsto H(D+uV)` 在整条合法直线上凹。PR #43 新证明的是它如何经完整事件条件 Schur 分解提升到跨块族。

## 2. 有限 DPP 与条件化背景

Russell Lyons, **Determinantal probability measures**, Publications Mathématiques de l'IHÉS 98 (2003), arXiv:`math/0204325`。

用途：有限 DPP 的包含概率、条件化和补集背景。PR 中的逐完整事件 Schur 恒等式仍从事件行列式直接证明，不用引用代替关键代数。

J. Ben Hough, Manjunath Krishnapur, Yuval Peres, Bálint Virág, **Determinantal processes and independence**, Probability Surveys 3 (2006), arXiv:`math/0503110`。

用途：谱 Bernoulli／投影 DPP 混合作为潜在信息收缩背景。没有把潜在谱变量当作观测配置的充分统计量。

## 3. 负相关与稳定多项式背景

Julius Borcea, Petter Brändén, Thomas M. Liggett, **Negative dependence and the geometry of polynomials**, JAMS 22 (2009), arXiv:`0707.2340`。

用途：强 Rayleigh 与负相关背景。三点证明实际使用的条件两点 odds 符号在正文中直接从 DPP 协方差平方重建；没有从强 Rayleigh 性直接跳到 Shannon 熵曲率。

## 4. 费米准自由态与 Gaussian 通道

Sergey Bravyi, **Lagrangian representation for fermionic linear optics**, Quantum Information and Computation 5 (2005), arXiv:`quant-ph/0404180`。

B. Dierckx, M. Fannes, M. Pogorzelska, **Fermionic Gaussian channels**, Journal of Mathematical Physics 49 (2008), arXiv:`0709.1061`。

用途：准自由态及其协方差仿射通道背景。PR 只使用一个显式满足收缩条件的通道，并自行计算相同输入配置分布产生不同输出配置分布，从而排除统一经典占据通道。

## 5. PR #43 自包含的新数学部分

以下不依赖外部符号定理：

- 实三点不定秩二方向的完整事件二次系数与条件四循环分解；
- 三点条件方向三分判据；
- Jacobi 互补主子式与惯性给出的相关非坐标 `3+3` 结构族；
- rank-two resolvent 特征的 KL／互信息充分统计等号；
- 压缩 `Sym_2` Hessian 的完整 Fisher 加唯一外幂标量公式；
- mixed-discriminant 的一／二次特征展开；
- Markov 密度伴随交织与生成元曲率公式；
- 可逆外幂半群的 `-125/78` 障碍；
- 准自由测量的有理障碍。

## 6. 来源不支持的结论

上述来源均没有直接证明：任意两侧相关大块、一般非坐标 rank-two 跨块径向族的整条配置熵凹性。谱混合、强 Rayleigh 性和量子数据处理都不能自动补足完整 Fisher 与固定观测基测量之间的桥梁。
