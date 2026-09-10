# PR80 独立 SECOND 审查报告

结论：PR80 的符号恒等式、ratio-cone 充分定理、reserve/square-completion 恒等式、reference fiber weights 和 fiber window/moment lower-bound theorem 在精确量词下为 `CORRECT`。固定 `s=9/10` 的新 pair/fiber 数字诊断没有 C2/raw 独立证书，仍为 `INCOMPLETE` 或 `SOURCE_ONLY`。

## 1. 来源绑定

**Verdict: CORRECT.**

`input_binding.json` 绑定 PR80 head `1a322ace19fd8ccc679f849780850dde31deb3d2`。列出的 10 个文件全部存在并匹配 SHA-256：`input/` 8 个作者文件，`pr58_source/` 2 个纯数学来源文件。绑定文件 SHA-256 为 `025522e3dd378287fa289274f8734285638628932e8cb43c610d4ad932179a64`。

本轮未读取任何 FIRST、其他 SECOND、C3 意见、公开评论或后续 live 版本。

## 2. Exact conditional paired identity

**Verdict: CORRECT, conditional on the stated accepted complete-law curvature identity.**

PR80 从 strict rank-two path `K(t)=[[A,tB],[tB^T,C]]`、`s=t^2`、complete-law likelihood `q=1+u=1-sa+s^2b`、`y=s^2b` 出发（`input/RESULT.md:17-39`）。它引用 complete-law curvature identity

`t^2 I''(t)=E_mu[Phi(u)+4y^2/q+y psi(u)]`

并在每个 fixed conditional fiber 使用 `E u=0`、`E y=0`（`input/RESULT.md:31-37`）。

在这个前提下，Theorem 2.1 的 pair identity（`input/RESULT.md:41-69`）代数闭合。证明只用独立 copy covariance identity 和 one-copy symmetrization：

- `2E[u log q]` 转为 `E[L(q,q')(Delta u)^2]`（`input/RESULT.md:73-77`）；
- `10E[y log q]` 转为 `5E[L(q,q')Delta y Delta u]`（`input/RESULT.md:79-83`）；
- `8E[y u/q]` 转为 `4E[Delta y Delta u/(q q')]`（`input/RESULT.md:85-93`）；
- Fisher/quadratic terms 以完整 one-copy symmetrization 保留（`input/RESULT.md:95-101`）。

该结论没有删除 rare event，没有取绝对值，没有做 spectral rotation，也没有改变物理参数。这里的 `CORRECT` 是对 PR80 从已声明 base identity 到 pair identity 的代数审查；base complete-law identity 的更早来源不是本轮重新形式化证明。

## 3. Fisher、acceleration 与 mixed 项

**Verdict: CORRECT.**

PR80 文本明确保留 complete-law curvature 中的 `Phi(u)`、`4y^2/q` 与 `y psi(u)`，且 pair kernel `J` 中保留 mixed term

`[5 L(q,q') + 4/(q q')] Delta u Delta y`

见 `input/RESULT.md:61-67`。`ADDENDUM_S09_SIGNED_FIBERS.md` 也说明没有删除 event、rare atom、Fisher term 或 acceleration term（`input/ADDENDUM_S09_SIGNED_FIBERS.md:15-21`）。因此，该部分是完整符号保留，不是只保留正项的截断证据。

## 4. Free pairwise PSD 反驳与 ratio-cone theorem

**Free pairwise PSD route: CORRECT.**

PR80 反驳过松的 free-vector PSD route：若把 `(Delta u,Delta y)` 当自由二维向量，则在 `q'=q>0` 时需要 `(5+4/q)^2<=8`，但左侧严格大于 `25`（`input/RESULT.md:103-141`）。这是方法反驳，不是 entropy concavity 反例。

**Ratio-cone sufficient theorem: CORRECT.**

Theorem 4.1 只在每个实际 DPP pair 满足

`F(q,q',Delta y/Delta u)>=0`

时推出 `t^2 I''>=0`，进而在 `t!=0` 时推出 `H''<=0`（`input/RESULT.md:143-177`）。证明使用 exact pair identity，再只在 actual DPP ratio 上使用 Cauchy lower bound。该 theorem 是充分条件，不是必要条件。

**Coverage of `s=9/10` fixture: INCOMPLETE / disproved for that mechanism by author SOURCE_ONLY diagnostic.**

`input/RESULT.md:217-245` 明确说 `s=9/10` coverage 是 requested/pending，不从旧正曲率事实推出。后续 `ADDENDUM_S09_SIGNED_FIBERS.md:23-42` 报告该 ratio-cone 在 `s=9/10` fixture 的两个 conditional orientations 上有 `75/66` 个 bad unordered pairs，因此不能解释该 fixture。该数值诊断没有 C2/raw 独立证书，只能作为 `SOURCE_ONLY`。

## 5. Diagonal/offdiagonal strictness 与 reserve identity

**Verdict: CORRECT.**

Theorem 4.1 的 diagonal strictness witness 是正确的：在 cone hypotheses 下，若存在正质量 one-copy atom 且 `u` 或 `y` 非零，则 diagonal pair `T=T'` 给出

`J=4(u^2+y^2)/q>0`

见 `input/RESULT.md:165-173`。

`ADDENDUM_S09_SIGNED_FIBERS.md:44-70` 给出 Cauchy slack identity：

`x^2/q+x'^2/q' = (x-x')^2/(q+q') + (q'x+qx')^2/[q q'(q+q')]`。

把它应用到 `x=u` 和 `x=y` 后，pair contribution 精确等于 ratio-cone lower piece 加上两个 nonnegative reserve squares（`input/ADDENDUM_S09_SIGNED_FIBERS.md:56-62`）。因此 offdiagonal pair 的充分严格条件 `F>0`、`q'u+qu'!=0` 或 `q'y+qy'!=0` 是有效的充分条件（`input/ADDENDUM_S09_SIGNED_FIBERS.md:64-70`）。

这些是 pair-local 代数结论；不认证具体 fixture 的 bad-pair counts。

## 6. Square completion 与 coefficient class

**Verdict: CORRECT.**

`ADDENDUM_S09_SIGNED_FIBERS.md:72-88` 给出完整 one-event integrand 的恒等式：

`Phi(u)+4y^2/q+y psi(u) = 4(u+y)^2/q + 2(u+5y) log q`。

这是从 `Phi(u)=4u^2/q+2u log q`、`psi(u)=8u/q+10log q` 直接展开得到的完整 equality，不是 bound。由于 `log q` 与 `u=q-1` 同号，事件级 sufficient condition

`u(u+5y)>=0`

等价于 `(a-sb)(a-6sb)>=0`（`input/ADDENDUM_S09_SIGNED_FIBERS.md:90-116`）。该 coefficient class 是充分条件；作者也明确说 `s=9/10` fixture 有四个 negative one-event integrands，不由 eventwise positivity 覆盖（`input/ADDENDUM_S09_SIGNED_FIBERS.md:118-128`）。

## 7. Reference fiber weights

**Verdict: CORRECT.**

PR80 的 pair identity 和 fiber bounds 使用 product-reference weights `p_C` 或 `p_A`。`ADDENDUM_FIBER_WINDOW_MOMENT.md:19-31` 明确说这些是 complete-law curvature identity 中的 reference weights，不是 full DPP 的 `q`-reweighted conditional law。

静态代码也按这个约定：`verify_s09_fiber_window_bound.py` 在 fixed-left case 使用 `pC`，否则使用 `pA`（`input/code/verify_s09_fiber_window_bound.py:13-30`）。这只是静态一致性证据，不是独立运行证书。

## 8. Fiber window/moment theorem

**Verdict: CORRECT as an analytic theorem.**

`ADDENDUM_FIBER_WINDOW_MOMENT.md` 定义

`lambda(q)=log(q)/(q-1)`

并证明它在 `(0,infinity)` 上为正且严格递减（`input/ADDENDUM_FIBER_WINDOW_MOMENT.md:33-47`）。在 fiber 上若 `q_-<=q<=q_+`，设 `c` 与 `delta` 控制 `lambda` 的中点和半宽（`input/ADDENDUM_FIBER_WINDOW_MOMENT.md:49-65`）。随后逐点使用：

- `4v^2/q >= 4v^2/q_+`；
- `z lambda(q) >= c z - delta |z|`；

得到 lower bound

`C_f >= 4 E[v^2]/q_+ + 2c E[z] - 2delta E|z|`

见 `input/ADDENDUM_FIBER_WINDOW_MOMENT.md:67-91`。该 theorem 允许 negative events，并只通过 actual fiber moments 付出 `E|z|` 预算。

**Fixed `s=9/10` lower bounds: INCOMPLETE.**

作者列出 8 个 left fiber 和 8 个 right fiber 正 lower bounds（`input/ADDENDUM_FIBER_WINDOW_MOMENT.md:99-141`），但这些具体 lower endpoints 来自作者脚本/摘要，没有 C2 证书。本 SECOND 不能把它们升级为独立 arithmetic certificate。

## 9. 作者脚本与输出证据地位

**Verdict: SOURCE_ONLY.**

`input/README.md:7-15` 明确给出证据边界：

- `output/*.txt` 是 edited author summaries，不是 committed scripts 的 literal raw stdout；
- window script import signed script 时会先输出 signed prelude，而 saved window summary 省略该 prelude；
- signed summary 也编辑了 minimum-q line 并添加解释文本；
- window script 中 `lo` 是 conservative lower bound；`hi` 不是 theorem right side 的 proved upper enclosure；
- literal matrices embedded in `code/verify_s09_signed_fibers.py` define this packet's author finite object；
- 它们等于 cited PR58 fixture、每个 pair count、全部 signs 和 window-moment bounds 仍需 independent source/arithmetic binding；
- 没有新 C2 contract。

脚本静态结构显示它确实包含 exact rational/SymPy asserts、log interval code、ratio-cone bad-pair asserts、negative event asserts、fiber positivity asserts（`input/code/verify_s09_signed_fibers.py:10-233`），窗口脚本也 import 该基础脚本并计算 theorem lower endpoints（`input/code/verify_s09_fiber_window_bound.py:1-52`）。但因为本轮不能运行/导入，且 outputs 不是 raw stdout，这些只作 `SOURCE_ONLY`。

## 10. 未闭合项

**Verdict: INCOMPLETE.**

以下项目未由本包闭合：

- 代码内 `A,C,U,V` 等于目标 PR58 `ADDENDUM_JOINT_ADDITIVE.md` fixture。该 cited file 不在允许的 `pr58_source/` 两文件中。
- `s=9/10` ratio-cone bad pair counts `75/66`。
- worst F signs 与具体 pair indices。
- 四个 negative one-event integrand signs。
- 16 个 signed-fiber positive averages。
- window/moment theorem 的 16 个 concrete lower bounds。
- `global true t^2 I''` 与旧 PR76/PR58 positive curvature value 的 equality。
- general dense correlated whole chord。
- novelty 与 formal proof。

## 11. 总结

PR80 的主要符号结构是可靠的：exact paired identity、mixed-term 保留、ratio-cone sufficient theorem、reserve identity、square completion、reference fiber weights 和 fiber window/moment theorem 都在其精确前提下闭合。

PR80 的固定 `s=9/10` 数字叙事仍未独立认证。当前可接受的说法是：作者源码和编辑摘要提供了 SOURCE_ONLY 诊断，指出 ratio-cone 不能覆盖该 fixture，并提出 fiber compensation/window-moment 机制；但没有 C2/raw 证书前，不得把具体 counts、signs、lower bounds 或 fixture equality 升级为 SECOND-accepted arithmetic facts。
