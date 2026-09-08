# D10-B4 非作者验缝

日期：2026-09-08。最终裁决：**INCORRECT（当前稿含一条明确错误陈述）**。

裁决需要分层：Theorem 1 的“强负界处处严格”是假的；Theorem 2 所需
的非严格强负界是真的，其统一弱耦合证明成立；decomposition.md 的
曲率恒等式及符号成立。不得将本裁决误写为“弱耦合主机制被反例推翻”。
作者材料只读，未在此擅自修订命题。

## 1. 明确错误：theorem.md 第76行

紧接 `H''≤-4||delta||²`，原稿写“with strict inequality for every
nonzero delta”。取

```
n=2, beta=0, tau=(1/2,1/2), delta=(1,1).
```

则 K=I/2 严格可行，delta非零，而

`H''=-1/[(1/2)(1/2)]-1/[(1/2)(1/2)]=-8=-4||delta||²`。

所以这里不能写严格小于强负界。正确等号条件为：每个 delta_i≠0 的
坐标都满足 tau_i=1/2；delta=0 时当然也取等。非零方向的结论仍为
`H''≤-4||delta||²<0`，后一个严格不等号没有问题。

建议作者的最小修订仅是区分这两个不等号并记录等号条件；本验证不
自行改作者文件。Theorem 2 在第215–220行使用的是 `M(0,tau)≼-4I`，
没有使用错误的“≺-4I”，因此承重部分不受影响。

## 2. 全参数盒、全部方向的一致性：通过

这里的量词确实是

`固定 n,a,b,eta；存在epsilon>0；对所有beta及所有tau以及所有delta成立`，

而非逐tau、逐delta各选epsilon。理由如下。

1. n固定时 R_beta^-1 的每个元素是有限 beta 乘积。故 S_beta(tau)
   在紧盒[−epsilon0,epsilon0]^(n−1)×[a,b]^n上连续，并在beta→0时
   对tau一致趋于diag(tau)。可以统一选epsilon0使严格谱裕量保持正。
2. 在该紧集的一个开邻域内，所有精确事件概率均正；它们是K元素的
   多项式，也由L-ensemble表示为正解析函数。有限事件数和紧致性还
   给出一个可能极小但严格正的统一最小概率。因此 log p 及tau二阶
   导没有隐藏的零概率奇点，M(beta,tau)连续。
3. 对每个tau均有lambda_max M(0,tau)≤−4。一致连续性给出一个共同
   epsilon，使整个tau盒内lambda_max M(beta,tau)≤−2。也可反证：
   若没有统一epsilon，选beta_k→0与tau_k造成lambda_max>−2，再取
   tau_k的收敛子列，就与极限处lambda_max≤−4矛盾。
4. 对所有delta同时成立是谱界的直接结果：
   `delta^T M delta≤−2||delta||²`。等价地先在单位球面上证明，再用
   二次齐次性恢复任意delta。作者已经以矩阵谱界完成归一化义务；
   不缺额外“方向紧致性”步骤，也不需要每个方向重选beta阈值。
5. 同一个beta的无穷范数球覆盖全部符号图样，故阈值也不依赖符号。
   但epsilon允许依赖n，没有跨维一致性声明。

上述论证完全不使用作者4个对角检查或12个非零beta样例；样例无法
提供具体epsilon的全盒证书。证明给的是定性存在，不是eps=0.01的认证。

## 3. 严格可行、K-affine、异质及 connected：通过并限定语义

- U=R^-1 可逆且tau>0，S=U diag(tau)U^T>0。统一上界S<I保证K=I−S
  严格正收缩；P=S^-1>I，故L=P−I>0。
- beta固定时 K_beta(tau+t delta)=K_beta(tau)−t U diag(delta)U^T，
  确为K-affine。合同保持秩，所以方向秩等于delta支撑大小。
- 邻边 `−beta_i/tau_(i+1)` 非零，因此每一个L的路径图都连通。
- 第一/末对角之差的绝对值至少
  `|1/tau1−1/taun|−beta1²/tau2≥eta−epsilon²/a`。
  取epsilon²/a≤eta/2即可统一保留至少eta/2的异质裕量。符号不影响。

必须区分两种“connected”：作者 verdict 明确写“connected as a
tridiagonal path”，此解释成立。若将theorem末句或decomposition第186行
读成整个参数族拓扑连通，则一般不成立：T_(a,b,eta)包含
`1/tau1−1/taun≥eta` 与 `≤−eta` 两个分离部分，两部分非空时不存在
保持该条件的连接路径。固定beta符号不能消除tau的这个分离。
建议统一写成“每个核对应的L路径图连通”，不要称整个参数空间连通。

另外，eta>1/a−1/b时T为空；eta=1/a−1/b时tau端点坐标受约束，T在
全tau盒中没有内点。枚举的全称结论此时仍有效或真空有效，但若要强调
非空、具有tau方向内部的连续族，应在应用时选择
`0<eta<1/a−1/b`。这不是证明偷缺的必要前提，而是“非退化族”宣传语
应补足的非空性边界；不能据任意eta>0自动宣称有非空区域。

## 4. 有限弦与方向长度

固定beta，在盒内的任意线段上都有统一Hessian界，故只要
tau±h delta及整段在盒内，就有

`[H(tau−h delta)+H(tau+h delta)]/2−H(tau)≤−h²||delta||²`。

tau处在盒边界时，任意delta不一定产生留在盒内的双向弦；但严格核
域是开集，且中心Hessian严格负，仍给每个固定delta的充分短可行
双向弦。不能把统一beta阈值误读为对所有未归一化delta都有同一个
t步长：方向放大时安全步长须缩小。原稿没有显式提出这种错误步长量词。
“严格负Hessian推出严格短弦凹”成立；单独的严格凹性一般不反推每点
Hessian严格负，所以原稿“Equivalently”宜理解为本处推论而非一般逻辑等价。

## 5. ell,A,B 与残差符号：通过

所有量在alpha=1的精确事件律p_t下取期望。设
`ell=log w, A=ell', B=ell'', mu=E A, c=E ell`。
由于 `p'/p=A−mu`，有

`d E f/dt=E f'+Cov(f,A)`，
`H'=−Cov(ell,A)`。

独立展开协方差导数得到

`d Cov(ell,A)/dt = Var(A)+Cov(ell,B)+E[(ell−c)(A−mu)²]`。

故作者写的三个负号全部正确，没有缺均值项或把B写成−ell''。
进一步用

`p''/p = B−E B +(A−mu)²−Var(A)`

得到

`R=−Cov(ell,B)−E[(ell−c)(A−mu)²]=−Σ p'' log p`，
`Var(A)=Σ(p')²/p`。

因此该分解与精确事件加速度/Fisher 分解完全一致。“唯一残差来源”
作为这一固定分解中所有非Fisher项的总和成立，且H''>0当且仅当
R>Var(A)。它不是证明R的符号，也不是证明某种数学分解唯一；两项
不能各自擅加正/负号。它基本是任意平滑正权有限概率模型的恒等式，
不是路径结构独有的符号定理。全局控制R仍未完成。

本族非零delta事实上还有Var(A)>0：若Var(A)=0，全部精确事件一阶导
均零，故单点包含概率导数全零。但令j为首个delta_j≠0的坐标，U的
下三角性与U_jj=1给 `dK_jj/dt=−delta_j≠0`，矛盾。作者只用非负
方差已经足够，不依赖这个加强结论。

## 6. 递推、样例与计算交叉核对

每个L主子矩阵按最大连续选中段分块，权重为对应区间行列式乘积。
最后一个坐标不选或最后一个连续段起点a的类别互斥且穷尽，所以
`Z_m(alpha)=Z_(m−1)(alpha)+Σ_a Z_(a−2)(alpha) kappa(a,m)^alpha`
以及Z0=Z−1=1正确。严格L保证所有段权正，对alpha,t有限和可微，
`H=F−partial_alpha F|alpha=1`与交换导数没有收敛性缺口。

独立脚本不导入作者实现：

- 精确有理反例验证Theorem1错误的严格号：n2，H''=界=−8。
- n3/n4两个固定有理案例，8+16个事件，用L主子式Taylor计算得到的
  p,p',p''与K包含主子式direct-Möbius的Taylor系数逐项精确一致。
- 65位代入残差恒等式，直接Hessian与分解差分别2e-67、1e-67。
- 运行退出0，0.0072174072265625秒；仅标准库，0随机样本。

这些24事件检查只校验算术和符号，不支撑Theorem2的全称证明。
完整参数、精确概率系数与输出见 independent_check.py/json。

## 7. 裁决范围与冻结摘要

当前整稿：INCORRECT，理由是第1节的可复核反例；不是INCOMPLETE的
“未找到证明”。Theorem2主要四项及残差身份本身没有发现关键缺口。
请作者修正明确假句，明确图连通/参数连通及非空性措辞，再由非作者
对修订版本给最终裁决；本报告不代作者修订后自动发放CORRECT。

所审theorem.md SHA256：
`4DC22ECDAAEFDAD01EFBA9D32A89808027751BCD9F4837719DC180D8C2184CC1`。
所审decomposition.md SHA256：
`140611DE956E9B5C1058455335753C568630B71675937923AFF31015854C2914`。

使用math-theorem技能的非作者验缝角色：只输出结论和定位，不修改作者
前提或文件；未运行Lean，不作机械认证或新颖性认证。
