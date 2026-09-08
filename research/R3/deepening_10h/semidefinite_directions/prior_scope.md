# 先行工作范围：D10-S

检索日期 2026-09-08。查询覆盖 DPP entropy concavity、positive semidefinite
directions、Loewner ordered kernels、rank-one、monotone coupling、strong Rayleigh
及 Bernoulli-sum entropy。只把原论文/作者报告作为数学依据。

## 已核对的邻近结果

1. [Gu, Entropy of Determinantal Point Processes](https://sevenkplus.com/data/dpp.pdf)：
Theorem 7 明确覆盖任意秩一核方向。Corollary 6 的原文结论为
`H(X(tK))≥t H(X(K))`，t∈[0,1]，即从0出发的弦不等式；不在此把该
陈述自动扩大为任意两个非零 thinning 尺度间的二阶凹性。
Theorem 1 是基数熵，不是全配置熵。本路线 rank2、固定非零余部，
不重报上述特殊弦。报告中未见一般 Loewner 有序端点凹性定理。

2. [Hillion–Johnson, A proof of the Shepp–Olkin entropy concavity conjecture,
Theorem 1.2](https://arxiv.org/pdf/1503.01570)：独立 Bernoulli 和的熵对
参数向量凹。本文 S-T 是这个已知工具加特殊条件化闭包的推论；不把
该工具或此类直接推论称为新颖的主定理。

3. [Yu–Johnson, Concavity of entropy under thinning](https://arxiv.org/abs/0904.1446)：
独立整数值变量的 thinning/相加框架是应用近邻，不提供本稿一般
K(t)=M+tD 的独立相加表示。

4. [Lyons, Determinantal probability measures](https://arxiv.org/pdf/math/0204325)：
该旧版本 Theorem 8.1 的随机支配陈述额外要求两核可交换；
该论文 Conjecture 9.2 是全配置熵凹性问题。单调耦合的存在不等于
熵的二阶控制；本文未据此断言 G-S。

一般不要求可交换的 Loewner 随机支配，见作者后续综述
[Determinantal Probability: Basic Properties and Conjectures, Theorem 2.9](https://arxiv.org/pdf/1406.2707)。
该综述 Theorem 2.11 也给谱 Bernoulli 混合；此处不把潜在谱指标熵
等同于观测坐标配置熵。

5. [Borcea–Brändén–Liggett, Negative dependence and the geometry of polynomials](https://arxiv.org/abs/0707.2340)：
实稳定/强 Rayleigh 是 DPP 的负依赖框架；静态性质并未在本次推导中
补齐事件加速度与 Fisher 项之间的缺口。

## 限制与新颖性

本次有界检索未确认“任意 PSD/NSD 核仿射方向全配置熵凹”的对应已知
一般定理。未确认不等于没有先例，也不等于此子问题已被权威列为开放。
S-T 仅作可核验的排除子类；其是否已被隐含覆盖仍待专门新颖性审计。
两个有限有理实例只验实现及条件化公式，不用于声称定理新颖。
