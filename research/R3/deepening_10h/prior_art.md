# 先行工作账

状态：第一轮范围审计完成；这不是穷尽性的截至 2026 文献综述，任何
“首个/未解决”表述仍需另做前向引用核验。

## 已定位的直接相关来源

### Lyons / Kulesza--Taskar：原凹性猜想

- Russell Lyons, *Determinantal probability measures*, Publ. Math. IHÉS 98
  (2003), 167--212：离散 determinantal measure 的基础来源。
- Alex Kulesza 与 Ben Taskar, *Determinantal Point Processes for Machine
  Learning*（2012），将 `H(K)` 对边缘核 `K` 的凹性列为 Lyons 猜想，并
  说明当时只有数值支持、没有一般证明。

关系：这是原问题来源，不支持当前已解或未解状态的 2026 最终断言。

### Yuzhou Gu：三个直接部分结果

- *Entropy of Determinantal Point Processes*，MIT 6.881 课程项目报告，
  当前可访问 PDF：<https://sevenkplus.com/data/dpp.pdf>。
- Theorem 1：DPP 基数 `|Y|` 的熵对 `K` 凹。
- Corollary 6：从零核到任意 `K` 的缩放弦 `H(tK)>=tH(K)`。
- Theorem 7：若 `rank(K_1-K_2)=1`，则全配置 Shannon 熵沿该弦凹。

关系：秩一方向和 thinning 路线已经被占位，D10-C 候选必须使用秩至少
二的方向。该来源是课程报告而非已确认的同行评审论文；本轮已独立审查
Theorem 7 与 Corollary 6 的适用范围，结论为可用，但不能把同结论当作
新发现。

### Hino--Yano：信息几何范围边界

- Hino 与 Yano, *Information geometry of determinantal point processes*,
  arXiv:2404.11024，研究 DPP 的 log-linear 嵌入、Fisher 信息和
  `e`-curvature。

关系：这些几何对象不会自动给出本项目沿边缘核 K-仿射路径的 Shannon
Hessian 符号。本问题多出事件概率二阶加速度项；若要桥接，必须额外证明
该项被 Fisher 项控制。本轮范围审计确认原 T1 分支没有越界声称。

### 点过程熵次可加

- *On the entropy and mutual information of point processes*（2016 IEEE
  ISIT）明确给出不交区域上的点过程熵次可加。

关系：FT-A 的信息论不等式本身属于一般熵次可加；本项目可能新增的只是
把等号条件用 DPP 跨块核 `X` 完全刻画，并将其变成 R3 的全局排除器。

### 强 Rayleigh 与准自由费米背景

- Anari--Oveis Gharan--Rezaei（COLT 2016）等工作确认 DPP 属于强
  Rayleigh 测度并研究采样/负依赖；目前首轮检索没有定位到直接证明一般
  `H(K)` 凹性的论文。
- Dierckx--Fannes--Pogorzelska, *Fermionic Quasi-free States and Maps in
  Information Theory*（arXiv:0709.1061）给出准自由费米态的信息论工具和
  一体算子表示；它研究的量子态熵不是自动等于固定占据基测量得到的 DPP
  Shannon 熵。

关系：二者是桥接背景，不是目标命题的先行证明。

本阶段至少核对以下四类关系：

1. DPP 子配置熵的块次可加是否已被明确写作核空间定理；
2. 强 Rayleigh / 实稳定测度文献是否已有相关 Shannon 熵凹性或反例；
3. 自由费米态的占据数测量熵与相关矩阵插值是否已有同结论；
4. 路径三对角 `L` 的加权独立集/区间递推是否为经典转移矩阵特例。

## 当前状态判断

- 一般凹性：从本轮检索不能确认截至 2026-09-08 已解决；标为
  `STATUS_UNCERTAIN`，继续追踪前向引用。
- FT-A：不等式被一般熵次可加占位；严格等号的 DPP 核刻画是否已有明确
  写法尚未确认。
- FT-B：尚未定位直接讨论 `L -> K` 后三点路径闭包的来源。
- FT-C：互信息恒等式是标准链式分解；价值只可能来自它导出的新结构
  必要条件或反例，而不是恒等式本身。

本轮没有做新颖性认证。`CORRECT` 只表示项目内部数学/实现范围经独立
核验，不表示文献首创。
