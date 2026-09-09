# sources.md — 来源与依赖边界

核对日期：2026-09-09。

## 1. 有限离散 DPP 的定义与边际核背景

Alex Kulesza, Ben Taskar, *Determinantal Point Processes for Machine Learning*.

- arXiv: https://arxiv.org/abs/1207.6083
- 本轮使用边界：只用于核对有限离散 DPP 的标准定义、`0<=K<=I` 的边际核条件、单点与二点包含概率及对角核对应独立 Bernoulli 的背景。
- 逻辑依赖：R2-T1 与 R2-T2 的八事件概率、导数和符号结论均在 `proof.md` 内重新推导，不把综述中的任何熵凹性结论作为前提。

## 2. 实主子式 / Rayleigh 平方背景

Abeer Al Ahmadieh, Cynthia Vinzant, *Characterizing principal minors of symmetric matrices via determinantal multiaffine polynomials*.

- arXiv: https://arxiv.org/abs/2105.13444
- 本轮使用边界：作为上一轮实主子式与条件 Rayleigh 平方机制的背景。本轮 R2-T1 在专门中心上直接展开八事件，不依赖未重建的外部推论。

## 3. DPP 熵问题的既有 rank-one 方向背景

Yuzhou Gu, *Entropy of Determinantal Point Processes*.

- 作者报告：https://sevenkplus.com/data/dpp.pdf
- 本轮使用边界：仅作为项目背景，说明 rank-one 差方向已有初等凹性机制。R2-T1 允许任意六方向，不能由 rank-one 方向结论推出。

## 4. PR #33

- https://github.com/randomcat4/dpp-entropy-tools/pull/33
- 继承内容：`|eij|<=1/4` 的完整六方向子域定理、八事件恒等式、实条件平方，以及两条严格失败路线。
- 本轮新增：R2-T1、二点条件熵引理、R2-T2、一般缺边连通族的事件坐标化。

## 5. 自包含性与新颖性

主要符号证明只使用有限和微分、二乘二与三乘三 Sylvester 判据、初等 log 不等式和对角符号共轭。没有把外部论文中的未证明结论导入主证明。

未做穷尽文献检索，**新颖性未认证**。本目录的“已证明”只指给出了作者侧完整推导，不等于同行评审或证明助理形式化。
