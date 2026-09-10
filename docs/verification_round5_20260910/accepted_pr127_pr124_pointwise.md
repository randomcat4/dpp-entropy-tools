# PR127 / PR124 — 精确逐点 resolvent 方法障碍

Status: **ACCEPTED_SCOPED**。PR127 是对 PR124 冻结作者头 `344723af6affab240c9f87c395d4e8c1b7b19f6d` 中单个逐点 resolvent 单元的独立 FIRST；审阅头为 `9db0cad138c551368c8617959c932530232ae662`。PR124 整包及其中正向定理没有因此获得接受或合并。

## 接受的窄结论

在作者给出的严格 half-leaf 核与完整六坐标真实对称方向

`A=1/4, B=16/25, q=109/1000, qbar=1/1000, r=1/50000,`

`D=(-18,-72,40,146,108,5)`

上，全部八个占据/空缺事件的 principal-minor Möbius 重建、两叶边缘与条件 jets 给出

`Phi_r''=`

`-47488558049748267993080620088778228551027375300000000000`

`/2044542058422113103788725284171055940635901533282467 < 0`。

`A,B,q,qbar>0` 通过两个 Schur complement 证明 `0<K<I`；严格性又使该完整六坐标方向成为合法局部物理切向。独立短 checker 使用精确有理数、全部 inclusion 主子式和八原子 Möbius 反演直接复现同一负分数。

## 逻辑边界

这个见证只否定旧全称目标 `Phi_r''>=0` 对每个 `r` 都成立，因而否定依赖该逐点正性的证书路线。它不决定

`G1''=integral_0^infinity r Phi_r'' dr`

的符号；同一作者见证上的完整 Shannon 曲率仍是严格凹向。因此它不是完整熵反例，也不是 integrated `G1''` 反例。

PR124 的 equal-strength 正定理、punctured small-edge 定理、一般 half-leaf/三点 Shannon 凹性、新颖性与形式化均未在本单元审阅。PR127 以 `0526c97746e4efbb226f14a33f0518f36a1b8395` 合入；精确审阅头为 `9db0cad138c551368c8617959c932530232ae662`。

- FIRST [报告](../../research/S1-pr124-pointwise-first-20260910/review_report.md)、[冻结范围](../../research/S1-pr124-pointwise-first-20260910/frozen_scope.md)和[源绑定](../../research/S1-pr124-pointwise-first-20260910/source_binding.json)。
- PR124 作者 [证明](https://github.com/randomcat4/dpp-entropy-tools/blob/344723af6affab240c9f87c395d4e8c1b7b19f6d/research/I05-35-halfleaf-resolvent-obstruction/proof.md)与[独立八事件 checker](https://github.com/randomcat4/dpp-entropy-tools/blob/344723af6affab240c9f87c395d4e8c1b7b19f6d/research/I05-35-halfleaf-resolvent-obstruction/code/verify_independent_event_fraction.py)。
