# sources.md — 实际检索的一手来源与假设映射

任务 ID：I05-W1-20260909-R2

本轮先检索条件熵、条件 DPP、实主子式几何、信息几何和费米 Gaussian 通道。下面区分“实际用于证明的外部结果”“只用于选择或排除路线的背景”以及“项目内先前工件”。本包的主定理与有限维条件化公式均在 `proof.md` 自包含推导，不把下列文献当成未写出的黑箱。

## 1. András Mészáros, *Limiting entropy of determinantal processes*

- arXiv: https://arxiv.org/abs/1905.11459
- Annals of Probability 48 (2020), no. 5, 2615–2643。
- 实际查看：引言印刷页 2（PDF 页 2），作者说明以随机次序和 Shannon 条件熵链式法则把总熵写成条件熵之和；正文随后研究极限中的条件过程。
- 本轮用途：提示“保留完整配置后条件化”而不是投影低阶统计量。我们采用的是有限块完整配置链式分解。
- 未使用：其极限熵、sofic 熵、投影核或局部收敛定理。该文没有给本轮 `K(t)` 曲率符号。

## 2. Alexander I. Bufetov, Yanqi Qiu, Alexander Shamov, *Kernels of conditional determinantal measures and the Lyons–Peres completeness conjecture*

- arXiv: https://arxiv.org/abs/1612.06751
- Journal of the European Mathematical Society 23 (2021), 1477–1519。
- 实际查看：摘要和条件测度主线；论文证明在其无限/投影设置中，对一个区域内完整配置作条件化仍保持 determinantal 结构。
- 本轮用途：确认“完整配置条件化仍可能是 DPP”不是概念上不合理的方向。
- 未使用：论文中的无限维条件核定理、完备性和尾 `sigma`-代数。我们的有限公式
  `C-t^2 B^T(A-E_{S^c})^{-1}B` 直接由完整事件单行列式和 Schur 补推导，并单独证明它是严格收缩核。

## 3. Grigori Olshanski, *Determinantal point processes and fermion quasifree states*

- arXiv: https://arxiv.org/abs/2002.10723
- 实际查看：§1.2–§1.3，印刷页 3–4。Definition 1.2 以正收缩 `K` 定义 gauge-invariant quasifree state；式 (1.6) 说明把它限制到占据数生成的交换子代数得到对应 determinantal measure。
- 本轮用途：建立量子路线的准确桥接：有限 DPP 的完整配置分布是固定坐标占据数测量后的经典分布。
- 未使用：不能把本题 Shannon 熵替换成 quasifree state 的谱熵，也没有从该文获得测量后处理&��凹性定理。

## 4. David S. Wang and Brian Swingle, *Recovery Map for Fermionic Gaussian Channels*

- arXiv: https://arxiv.org/abs/1811.04956
- 实际查看：印刷页 2–3。作者说明某些 Gaussian channels 把 Gaussian states 保持在 Gaussian 类中，并以 `G -> B G B^T + A` 描述 covariance 作用。
