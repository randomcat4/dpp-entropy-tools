# sources_continuation.md

以下均为本轮实际核对的原始来源。主证明在包内自包含；文献用于建立跨域桥接、确认可用结构及界定未使用范围。

## 1. A. I. Bufetov, Y. Qiu, A. Shamov, *Kernels of conditional determinantal measures and the Lyons–Peres completeness conjecture*

- arXiv: https://arxiv.org/abs/1612.06751
- JEMS 23 (2021), 1477–1519。
- 用途：核对“对一个区域的完整配置作条件化后仍可能是 determinantal”这一结构背景。
- 未作为黑箱：本包有限维条件核 `C-t^2B^T(A-E_{S^c})^{-1}B` 直接由完整事件单行列式和 Schur 补证明。

## 2. G. Olshanski, *Determinantal point processes and fermion quasifree states*

- arXiv: https://arxiv.org/abs/2002.10723
- 用途：核对规范不变准自由态限制到占据数交换子代数后得到 DPP，因而配置熵是固定测量后的经典熵。
- 未使用：不能把配置 Shannon 熵替换为准自由态谱熵，也没有从该文得到经典后处理。

## 3. Fermionic Gaussian-channel 一手入口

- E. Greplová and G. Giedke, *Degradability of Fermionic Gaussian Channels*, arXiv:1604.01954, Phys. Rev. Lett. 121, 200501 (2018)。
- D. S. Wang and B. Swingle, *Recovery Map for Fermionic Gaussian Channels*, arXiv:1811.04956。

用途：确认 Gaussian 通道在 covariance／关联矩阵层面闭合，并可写成线性衰减加噪声。未使用其 degradability 或 Petz 恢复结论。真正缺口是固定占据数测量不与一般相关固定点通道交换。

## 4. J. Borcea, P. Brändén, T. M. Liggett, *Negative dependence and the geometry of polynomials*

- arXiv: https://arxiv.org/abs/0707.2340
- JAMS 22 (2009), 521–567。
- 用途：strongly Rayleigh／实稳定框架保证 DPP 的负依赖、条件与外场闭合，并解释条件两点 odds 的次模符号。
- 未使用：该文没有直接给配置 Shannon 熵沿真实 `K`-仿射方向的二阶不等式。

## 5. R. Lyons, *Determinantal probability measures*

- arXiv: https://arxiv.org/abs/math/0204325
- Publ. Math. IHÉS 98 (2003), 167–212。
- 用途：DPP 基本定义、负关联及条件结构背景。
- 未使用：没有把负关联本身当作高维熵凹性证明。

## 6. A. Al Ahmadieh and C. Vinzant, *Characterizing principal minors of symmetric matrices via determinantal multiaffine polynomials*

- arXiv: https://arxiv.org/abs/2105.13444
- Journal of Algebra 638 (2024), 255–278。
- 用途：核对秩与变量次数、实主子式 Rayleigh 平方以及外幂系数的代数可实现性。
- 未使用：Rayleigh 平方没有自动给 `Q`-log 或完整熵 Hessian 的符号。

## 7. 用户提供的独立团队输入

“任意有限 Hermitian 核、过固定严格对角核的整条合法真实仿射直线配置熵凹”由用户说明已被另一团队证明。本包把它明确标成导入引理，用于一侧对角定理及 `3+3` 结构族的两个极端条件配置。本会话没有进行新上下文独立审阅，也不声明其新颖性。
