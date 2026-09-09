# sources.md — 原始来源、页码及假设映射

任务 ID：I05-W1-20260909。检索日期：2026-09-09。
以下“页码”均指所链接 PDF 本身的页号，不把 arXiv 摘要页当作已核对证明。
实际打开全文、检索相关位置，并查看了下列关键页的渲染图。
定理 T 及本包障碍均在 proof.md 重建；没有外部未证定理作为隐含前提。
新颖性未认证；没有检索到同表述不等于不存在。

## [S1] Al Ahmadieh–Vinzant：实主子式与平方

Abeer Al Ahmadieh and Cynthia Vinzant,
*Characterizing principal minors of symmetric matrices via determinantal multiaffine polynomials*.

原始入口：https://arxiv.org/abs/2105.13444
全文：https://arxiv.org/pdf/2105.13444

核对位置：p.1 的 F_A 与 Rayleigh 差定义；p.9 的 Theorem 3.5 及证明。
实际使用：实对称行列式多仿射多项式的 Rayleigh 差为平方这一精确代数表示；
作为三类机制比较中的实结构定位，不作为熵符号定理。

假设映射：取该文唯一分解整环 R=实数域，F_L=det(diag x+L)，
x_1⋯x_n 系数为 1；L=K(I−K)^{-1} 仍实对称。
沿 K-affine 的 L'' 不为零，已在 attempts.md (A3) 保留。
本包独立用逆矩阵微分重建所需平方恒等式。
没有使用 Theorem 5.1 的轨道方程来声称 Fisher 控制。

## [S2] Mészáros：条件熵表示

András Mészáros, *Limiting entropy of determinantal processes*,
Annals of Probability 48(5), 2615–2643 (2020).

原始入口：https://arxiv.org/abs/1905.11459
全文：https://arxiv.org/pdf/1905.11459

核对位置：p.2 的证明思路；§4，pp.18–19，尤其 p.19 的有限熵链式和随机次序展开。
实际使用：逐点揭示、条件二元熵的表示方向。

假设映射：该段在图与投影核的框架内展开；本包并没有把其投影/局部极限假设移植到任意 K。
本包只使用有限 Shannon 链式法则，并在 proof.md §7.1 以 Schur 补重证一般严格收缩的条件核。
没有调用该文主极限定理，没有把条件熵表示当成参数曲率定理，
也没有声称对其积分或极限作二阶求导合法。

## [S3] Olshanski：准自由态到 DPP 的占据数限制

Grigori Olshanski, *Determinantal point processes and fermion quasifree states*,
Communications in Mathematical Physics 378 (2020), 507–555.

原始入口：https://arxiv.org/abs/2002.10723
全文：https://arxiv.org/pdf/2002.10723

核对位置：pp.3–4，Definition 1.2，§1.3，公式 (1.3)–(1.6)。
实际使用：协方差 K 的 gauge-invariant 准自由态，限制到占据数生成的交换代数后得到 DPP。

假设映射：本包只在有限维 0<K<I 上使用；proof.md §8.1 用外幂构造密度矩阵，
直接验证正性、归一化与 p_K 的对角元。
本包的谱熵与去相干熵计算是该有限构造的直接推导，不声称该文证明了 Shannon 熵凹性。
该文更深的等价/不交性结果没有用于本次结论。

## [S4] Lyons–Steif：原始平稳熵率问题

Russell Lyons and Jeffrey E. Steif,
*Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination*,
Duke Mathematical Journal 120(3) (2003), 515–575.

原始入口：https://arxiv.org/abs/math/0204324
全文：https://arxiv.org/pdf/math/0204324

核对位置：arXiv PDF p.53，§9，Conjecture 9.2；另检索了 §6 的条件熵讨论。
实际使用：确认固定符号的平稳熵凹性问题的表述与有限任意矩阵问题不同。

假设映射：符号 f,g 固定，参数混合为 (f+g)/2，结论对象是过程熵。
本次定理 T 的双块有限矩阵族没有被证明来自这样的固定标量符号对，
故不对该猜想作正面或反面结论。
不把 2003 年原文的“猜想”标签当作截至检索日的完整状态综述。

## [S5] Hino–Yano：信息几何，仅作旁路核查

Hideitsu Hino and Keisuke Yano,
*Duality induced by an embedding structure of determinantal point process*.

原始入口：https://arxiv.org/abs/2404.11024
全文：https://arxiv.org/pdf/2404.11024

核对位置：p.5 的 Theorem 1，公式 (5)–(7)，以及 p.12 的证明开头。
实际使用：仅确认其讨论的是嵌入 log-linear 模型的曲指数族与相关参数；
没有引用任何曲率结论作为 K-affine 熵凹性的依据。

假设映射：未完成对该参数图册在所有实符号模式下全局覆盖性的审计；
因此本包不依赖此图册。尤其不把 e-embedding 曲率或自然参数 Fisher Hessian
等同于本题 K-affine 的 Shannon 熵 Hessian。

## [S6] Gu：已知 rank-one 方向的原始项目报告

Yuzhou Gu, *6.881 Project Final Report: Entropy of Determinantal Point Processes*.

原文：https://sevenkplus.com/data/dpp.pdf

核对位置：p.1 的问题与结果范围；pp.5–6 的 Theorem 7 及完整行列式导数证明。
这是作者署名的课程项目报告；此处没有核实其为同行评审论文，不虚构出版年。

实际使用：核对 rank-one 方向时 p''=0 的原始证明，作为对照，避免把已知 rank-one 凹性当作突破。
本包的交叉秩一方向是整体 rank(D)=2、p''通常不为零，所需关键步骤是固定块边际的补偿。
未依赖该报告的基数熵或 thinning 结果；也没有把它们提升为整个随机子集熵的一般结论。

## 文献使用边界

没有引入未核对的定理页码；没有把搜索未命中视为不存在。
本包只对所列实际用到的桥接式负责，不声称完整审阅了六篇材料的全部定理。
未附第三方全文；本包的证明、精确输入和代码在无网络环境下自包含。
