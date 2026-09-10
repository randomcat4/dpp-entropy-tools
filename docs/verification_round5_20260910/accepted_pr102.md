# PR102 — 任意多重 DPP 边界与秩二双尺度稳定性的限定接受

Status: **ACCEPTED_SCOPED / MIXED_SOURCE_ARCHIVE**。冻结作者头 `16a25c3810977d67207a95f935990df0a807bff9`。只接受 `RESULT.md` Sections 1–3 与 `ADDENDUM_TWO_SCALE_STABILITY.md` Sections 1–5 的解析单元；两个显式 `3+3` fixture、其全弦常数及全部作者计算保持未认证。S1 FIRST 与先行公开的 S3 fresh SECOND 对这一分界完全一致。

## 一般有限仿射端点定理

令有限真实仿射路径

`K(t)=K(T)+(t-T)D`

从 `t<T` 的严格内点进入 `t=T` 的合法边界。则完整配置 Shannon 熵满足

`H''(t) -> -infinity`，当 `t -> T-`。

端点允许 `K(T)` 有任意多个零特征值、`I-K(T)` 有任意多个零特征值，并允许两侧同时活动。证明在端点核上的方向压缩给出一阶正定谱簇；真实基数生成行列式

`E[z^|X|]=det(I-K+zK)`

迫使某个端点禁戒基数组具有 `Theta(epsilon)` 质量。由于该质量是观察坐标下非负完整事件概率的有限和，至少一个完整原子组一阶消失。它在 Fisher 和中提供 `A/epsilon` 极点，而全部一阶余项、双根的不利加速度和其余原子合计至多为 `O(log(1/epsilon))`，故完整曲率趋于负无穷。

这里谱分解只用于计算真实基数概率，不在谱基中替换配置熵。所有完整原子、Fisher 与加速度项均保留。

## 秩二纯双根与双尺度稳定

交叉秩二径向路径的完整似然为 `q=1-sa+s^2b`。单个双根原子确有有界 Fisher 和不利的对数加速度发散；但上述基数组定理强制另有一阶完整事件组。因此“全部消失原子都是双根”的抽象模式不能由严格内点进入的仿射 DPP 实现。它是否定一种反例机制，不是熵反例。

重复秩二端点被扰动后，以 `eta` 记两个活动广义特征值的分裂尺度，以 `delta` 记端点距离。full/empty 原子给出

`c(eta+delta)/delta`

的 Fisher 下界，邻接真实基数组给出 `c/(eta+delta)`；两者经 AM-GM 统一为 `c delta^(-1/2)`。点态 L-ensemble 恒等式只用于证明全部完整原子 `p_E>=c_0 delta^(2N)`，所以完整加速度损失仅为对数级；物理路径始终是 `K`-仿射。

因此，若一个交叉秩二种子已经独立知道其整个严格最大弦具有

`Gamma_0=-H_0''(t)/t^2 >= g>0`，

则存在相对开参数邻域，使每个邻近成员在它自己的最大合法弦上满足

`H''(t)<=-(g/2)t^2`，

从而 `H+(g/24)t^4` 在闭弦凹。该定理处理重复端点分裂及 `K/I-K` 同时活动，但明确**不负责证明种子的紧致中段余量**。

## 未认证的作者有限单元

以下内容随源码作为研究档案进入 main，但保持 **PENDING_INDEPENDENT_ARITHMETIC**：

- `RESULT.md` Sections 4–7 的第一个稠密相关 `3+3` fixture 及 `H''<=-(1/100)t^2`；
- 双尺度附录 Section 6 对该 fixture 的专门化；
- 整个 `ADDENDUM_SIMULTANEOUS_ENDPOINT.md` 的 13 个似然类型、同时双 `K`/双 complement fixture 及 `H''<=-(1/10)t^2`；
- 两个 JSON、两个 SymPy checker、两个作者 stdout、64 事件与全部承重有理常数。

两份审阅都确认作者程序静态上使用完整 Möbius 事件、精确有理极值和完整曲率，而不是时间网格；但作者 `PASS` 仍不是独立有限证书，不能由合并动作升级。

## 不能外推的结论

本文不证明任意稠密相关 rank-two 的紧致中段符号或普遍全弦凹性，不覆盖交叉秩高于二的多尺度层级、真实熵率、新颖性或形式化验证。Hough–Krishnapur–Peres–Virag 只支持标准基数 Bernoulli 描述；作者已经直接重证所需生成行列式。Kulesza–Taskar 的 L-ensemble 也只作点态原子恒等式，未引入 `L`-仿射路径。

## 来源、双审与合并

- 作者 [一般结果](../../research/I05-30-multiple-endpoint-20260910/RESULT.md)、[双尺度稳定附录](../../research/I05-30-multiple-endpoint-20260910/ADDENDUM_TWO_SCALE_STABILITY.md) 与 [来源/失败台账](../../research/I05-30-multiple-endpoint-20260910/SOURCES_AND_FAILURES.md)。
- S1 FIRST [冻结范围](../../research/S1-pr102-multiple-boundary-first-20260910/frozen_scope.md)、[报告](../../research/S1-pr102-multiple-boundary-first-20260910/review_report.md)、[来源审计](../../research/S1-pr102-multiple-boundary-first-20260910/source_review.md) 与 [绑定](../../research/S1-pr102-multiple-boundary-first-20260910/source_binding.json)。
- S3 先于 FIRST 的 [fresh SECOND](https://github.com/randomcat4/dpp-entropy-tools/pull/102#issuecomment-5617075807) 与 [两审交叉门](https://github.com/randomcat4/dpp-entropy-tools/pull/102#issuecomment-5617093325)。

FIRST 档案 PR119 以 `dece41304b0612288b97576a8d7915ed0ac165f5` 合入，第二父为 `021201bb6434fc2dbcc8b8de13c71df276297551`。作者 PR102 以 `a2cdc406ad8b04d9362a87e02a53b399827646b7` 合入，第二父为精确冻结头 `16a25c3810977d67207a95f935990df0a807bff9`。接受范围仅以本文为准。
