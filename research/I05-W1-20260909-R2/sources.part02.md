- 本轮用途：检验是否能用 Gaussian 通道衰减跨块 covariance，再以相对熵数据处理推出结果。
- 未使用：本文的 Petz 恢复定理。本轮没有得到固定占据数测量与该量子通道交换的经典后处理式；`proof.md` §10 还严格证明最直接的整块刷新在 rank two 的 `Q` 阶失效。

## 5. Abeer Al Ahmadieh and Cynthia Vinzant, *Characterizing principal minors of symmetric matrices via determinantal multiaffine polynomials*

- arXiv: https://arxiv.org/abs/2105.13444
- Journal of Algebra 638 (2024), 255–278。
- 实际查看：Lemma 3.4 和 Theorem 3.5，印刷页 9。Lemma 3.4 把 determinantal polynomial 某变量的次数与相应矩阵方向的秩联系；Theorem 3.5 以 Rayleigh differences 为平方刻画对称矩阵主子式像。
- 本轮用途：确认 rank-two 的 `s` 次数和实主子式系数之间存在强代数约束，并评估“最高混合判别式自动有利”的可能性。
- 未使用：该文没有 Shannon 熵符号结论。`proof.md` §9 的严格例说明 `Q` 的对数加权本身可以有害，因此 Rayleigh 平方不能直接替代完整 Fisher/条件熵控制。

## 6. Hideitsu Hino and Keisuke Yano, *An embedding structure of determinantal point process*（预印本题名曾为 *Duality induced by an embedding structure of determinantal point process*）

- arXiv: https://arxiv.org/abs/2404.11024
- Information Geometry 7 (2024), 523–542。
- 实际查看：§3.2 的 Lemma 2，印刷页 8。DPP 嵌入的 expectation parameters 是边际核主子式 `det K_I`；作者同时强调 DPP 是 curved exponential family，完整 Fisher 不等于单一势函数的全 Hessian。
- 本轮用途：核对 `K` 主子式确实是统计模型的期望坐标，但避免把自然参数/期望参数几何中的直线误当作真实 `K`-affine 直线。
- 未使用：其 embedding curvature 或 duality 没有直接给本轮 Shannon 熵凹性。

## 7. 项目内先前二维工件（不是外部文献，也不是新颖性证据）

- URL: https://github.com/randomcat4/dpp-entropy-tools/blob/main/research/R1/proofs/n2_concavity.md
- 内容：实 `2 x 2` DPP 完整配置 Shannon 熵在边际核凸域上的全局凹性证明，含矩阵铅笔行列式消去。
- 本轮处理：没有把它作为不可见前提。`proof.md` §3 重写了完整证明，`code/verify.py` 独立符号检查关键行列式恒等式。该先前工件意味着二维输入本身不是本轮新颖性主张；本轮新增贡献候选是条件化径向提升及其跨块 rank-two 后果。

## 8. 检索结论的限度

