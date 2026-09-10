# PR80 作者脚本静态代码审查

本文件只审查 `input/code/` 两个作者脚本和 `input/output/` 两个作者摘要的静态证据地位。未运行、未导入，也未复算 determinant/log/entropy/interval。

## 总体裁定

**Verdict: SOURCE_ONLY.**

脚本结构与 PR80 文本声称的有限诊断方向一致，但不是独立 computational certificate。输出文件也不是 raw stdout，而是作者编辑摘要；因此 `PASS` 标签不能提升为 SECOND 通过。

## `verify_s09_signed_fibers.py`

**静态结构：SOURCE_ONLY but internally coherent.**

该脚本：

- 嵌入一组 `A,C,U,V` 矩阵并定义 `B=U*V.T`、`s=9/10`（`input/code/verify_s09_signed_fibers.py:10-27`）。
- 用 signed complete-event determinant 构造 block laws `pA,pC`（`input/code/verify_s09_signed_fibers.py:33-63`）。
- 实现 rational atanh log interval 与 endpoint reversal（`input/code/verify_s09_signed_fibers.py:64-113`）。
- 构造 64 个 `(a,b,q,u,y)` 数据并 assert `q>0`（`input/code/verify_s09_signed_fibers.py:120-135`）。
- assert 每个 fiber 的 fixed-margin coefficient cancellation（`input/code/verify_s09_signed_fibers.py:137-143`）。
- assert left/right bad ratio pair counts 为 `75/66`（`input/code/verify_s09_signed_fibers.py:145-172`）。
- assert Cauchy slack identity 与 nonnegative reserve（`input/code/verify_s09_signed_fibers.py:174-186`）。
- assert negative events precisely equal `(0,6),(1,5),(2,5),(3,0)`，并 assert all left/right fiber averages have positive lower endpoint（`input/code/verify_s09_signed_fibers.py:188-217`）。

这些 asserts 是作者代码中的静态事实。由于本轮没有运行脚本，且没有 C2 execution ledger、raw stdout、environment、first-failure discipline 或 independent implementation，不能把这些 counts/signs/lower bounds 接受为独立证书。

## `verify_s09_fiber_window_bound.py`

**静态结构：SOURCE_ONLY; lower-bound direction visible.**

该脚本：

- import `verify_s09_signed_fibers` 中的 `F,pA,pC,data,log_iv,iv_scale`（`input/code/verify_s09_fiber_window_bound.py:1-4`）。因此运行它会触发 base script 的 top-level asserts/output。
- 对 fixed-left 使用 `pC`，对 fixed-right 使用 `pA`，与 reference fiber weights 的文本一致（`input/code/verify_s09_fiber_window_bound.py:13-16`）。
- 用 `qmin/qmax`、`lambda_iv(qmax/qmin)`、`Ev2/Ez/Eabsz` 计算 theorem lower expression（`input/code/verify_s09_fiber_window_bound.py:17-37`）。
- assert 每个 `lo>0`，再打印 8 个 left 和 8 个 right approximations（`input/code/verify_s09_fiber_window_bound.py:39-52`）。

README 已澄清 `lo` 是 conservative lower bound，而 `hi` 只是 companion conservative value，不是 theorem right side 的 proved upper enclosure（`input/README.md:11`）。因此任何 “lower/upper interval” 解读都应撤回，只能保留 lower endpoint 的作者 SOURCE_ONLY 证据地位。

## 输出文件

**Verdict: SOURCE_ONLY.**

`input/output/verify_s09_signed_fibers.txt` 声称：

- left/right bad ratio pair counts 为 `75/66`；
- four negative complete one-event integrands；
- 16 个 fiber curvature displays 为正；
- global true `t^2 I''` display 为正；
- all signs decided by exact rational endpoints。

见 `input/output/verify_s09_signed_fibers.txt:1-31`。

`input/output/verify_s09_fiber_window_bound.txt` 声称：

- 8 个 left fiber theorem lower values 和 8 个 right values 均为正；
- minimum left/right lower bound displays 为 `1.1494168702064782` 与 `0.702423465205957`；
- checker uses exact rational event data/moments and outward rational atanh enclosures。

见 `input/output/verify_s09_fiber_window_bound.txt:1-25`。

但 `input/README.md:9` 明确说这两个 output files 是 edited author summaries，不是 literal raw stdout。故这些 output 不能作为独立执行证据。

## 阻止升级为证书的缺口

**Verdict: INCOMPLETE for finite arithmetic certification.**

缺少：

- C2 或等价 independent implementation；
- raw execution transcript；
- environment/runtime binding；
- first-failure/timeout/no-rerun ledger；
- fixture equality binding to the cited PR58 joint-additive source；
- exact rational endpoint dump for every claimed count/sign/lower bound；
- output hash manifest tying raw stdout to script invocation。

因此，脚本对数学审查的贡献是：它们说明作者想检查什么、公式如何编码、哪些 finite facts 作者声称已 assert；它们不能替代独立 arithmetic certificate。
