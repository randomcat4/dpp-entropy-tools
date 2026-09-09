# 来源范围独立核对

核对日期：2026-09-09。此文件只审计冻结产物对原始来源的使用边界，不认证新颖性。

## 1. 已知 rank-one 方向

Yuzhou Gu, *6.881 Project Final Report: Entropy of Determinantal Point Processes*  
原文：https://sevenkplus.com/data/dpp.pdf

核对了报告 pp.5–6 的 Theorem 7。其结论是全配置 DPP Shannon 熵沿整体 rank-one 核方向凹，证明利用该方向下每个事件概率的二阶导数为零。冻结产物没有把这一已知结果当作新定理；本任务的方向整体秩为二，关键额外步骤是固定双块边际对加速度项的全事件补偿。

该来源是作者项目报告；本核对不把它描述成同行评审论文。

## 2. 实主子式的 Rayleigh 平方

Abeer Al Ahmadieh and Cynthia Vinzant, *Characterizing principal minors of symmetric matrices via determinantal multiaffine polynomials*  
原始入口：https://arxiv.org/abs/2105.13444

核对了 Theorem 3.5 及相邻证明。Rayleigh 差的平方表示确实提供实对称主子式的代数结构，但原文没有给出本任务全配置 Shannon 熵沿任意 K-affine 弦的符号定理。冻结产物只把它作为被比较的机制入口，使用范围准确。

## 3. 条件熵与准自由态桥接

András Mészáros, *Limiting entropy of determinantal processes*  
原始入口：https://arxiv.org/abs/1905.11459

Grigori Olshanski, *Determinantal point processes and fermion quasifree states*  
原始入口：https://arxiv.org/abs/2002.10723

前者支持条件熵/揭示次序的表示方向，后者支持有限维占据数测量与 DPP 的准自由态联系。两者都没有直接给出冻结定理的 K-affine Shannon 熵曲率符号。冻结证明分别重建了所需有限维条件核和有限准自由态对角分布，没有把来源中的表示定理升级为凹性定理。

## 4. 平稳目标和信息几何

Russell Lyons and Jeffrey E. Steif, *Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination*  
原始入口：https://arxiv.org/abs/math/0204324

Hideitsu Hino and Keisuke Yano, *Duality induced by an embedding structure of determinantal point process*  
原始入口：https://arxiv.org/abs/2404.11024

前者的固定标量符号熵率问题与有限任意矩阵弦不同；后者的信息几何参数也不自动等于 K-affine 参数。冻结产物没有从受限双块定理推断平稳熵率结论，也没有把自然参数曲率替换为本题曲率。

## 5. 检索结论

以“rank-one cross block scaling”“fixed marginals”“DPP Shannon entropy concavity”“mutual information”等组合进行了有限目标检索，并搜索了本仓库现有研究树。没有定位到与“固定任意内部块、交叉块为 `tuv*`、全配置熵整条合法弦凹”完全相同的表述。

该结果只说明本次有限检索未命中；它不能排除不同术语下的等价定理，因此新颖性保持“未认证”。
