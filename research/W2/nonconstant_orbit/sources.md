# 来源与假设映射

核对日期：2026-09-09。下列外部来源均为原始论文。新推导与来源已有定理分开记录；新颖性未认证。

## S1 — 唯一承重的外部 DPP 结构定理

Russell Lyons, *Determinantal Probability Measures*, arXiv:math/0204325v4 (18 June 2003), https://arxiv.org/pdf/math/0204325 。实际核对 Theorem 8.1，PDF第34页（0基页33，印刷页34），并查看页面截图。

使用部分：任意正收缩核的DPP具有负关联性。正文使用的是有限 Hermitian 正收缩参考 Q；不要求实矩阵。新稿第6节和旧稿第8–9节中，递减且非负、不交坐标支持的指数函数由负关联递推控制乘积矩。没有使用该定理另一个需要交换性的随机支配断言；不能把它的交换性条件错加到负关联上或错删出支配断言。

Theorem 8.1 的证明在该论文依赖前述投影、条件化和正收缩扩张结果；本稿依赖此定理而不宣称重证它。精确事件行列式、KL变分和匹配下界在本稿重建。

## S2 — 原始平稳熵率问题

Russell Lyons and Jeffrey E. Steif, *Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination*, arXiv:math/0204324v5 (23 January 2003), https://arxiv.org/pdf/math/0204324 。实际核对第9节 Conjecture 9.2，PDF第53页（0基页52，印刷页53），并查看截图。

这是任意符号对的熵凹性目标来源，不是本稿NC定理的证明。该原始猜想强于本稿受限结果。熵率存在只使用本稿重建的平稳性、次可加和有限字母熵界，不额外调用该文的混合或预测定理。

## S3 — 随机顺序路线背景，不提供本稿缺失曲率

András Mészáros, *Limiting entropy of determinantal processes*, arXiv:1905.11459v2，https://arxiv.org/html/1905.11459v2 。实际读取第4节开头的固定/均匀随机顺序链式熵表示、式(10)–(11)以及邻近极限论述。其本段以投影的graph-positive-contraction框架展开；不把其具体极限定理直接套在任意参数族。

新稿第2.2节只使用任意有限分布均有的链式规则，并自行微分 p_y(t)b(q_y(t))。原文的表示不自动给K-affine曲率，也不容许忽略权重导数。

## 本轮自行推导，未在上述来源中引用为既有定理

Boolean Fourier精确事件恒等式、复参数闭步模长界、NC的体积一致高阶余项控制、NC-channel的张成空间障碍，以及旧循环平均严格性和径向加强，均应以本稿作者证明审阅，不以文献引用替代认证。

Hadamard行范数界、Cauchy系数估计、log-sum/KL非负性、有限链式熵和次可加是标准基础工具；本稿写明了它们作用的具体对象和有限步骤。未把测量后的Shannon熵换为费米态的谱熵。

本轮检索包括DPP熵展开、闭步/对数行列式表示及相关条件熵方法；没有定位到同一完整定理，不等于文献不存在，也不认证首创。
