# PR81 delta 1e20 SECOND review

## 有界结论

`CORRECT` for the delta `shared_corner_parallel_refinement` analytic result, within the stated scope.

我接受本 delta 的数学主张：one-edge `kappa(u,s)` 是实际 endpoint quadratic 在 `(X-Y)^2` 模式上的最优系数；两条 opposite edges 的 parallel/harmonic combination 给出正确的 `Delta^2` 下界；若实际 half-leaf rectangle 满足

```text
KA+KB > J/(32AB),
```

则完整六方向 Shannon Hessian 严格负定，等价的继承二维核心满足 `E_H>0` 与 `det E_H>0`。该 refinement 严格包含旧的 coarse sufficient condition `J<12AB`，但不声称 universal `KA+KB>=J/(32AB)`，也不重新证明一般 half-leaf、unequal leaf 或 general missing-edge concavity。

作者 checker、输出 PASS、failure ledger 中的 “independent reconstruction” 均未被我当作独立审阅或 C2 证书。

## 1. 来源与绑定：`CORRECT`

四个 delta 文件均与 `delta_1e20_input_binding.json` 的 SHA-256 和行数一致：0 缺失、0 hash mismatch、0 line-count mismatch。机器实测绑定写入 `delta_1e20_source_binding.json`。

本轮只读取 delta 绑定及四个 delta 文件，并沿用自己此前已读的 d995 数学上下文；未读取 sibling 或后续 live source。

## 2. Optimal edge `kappa`：`CORRECT`

Refinement 从完成 leaf-diagonal square 后的 endpoint quadratic 出发：

```text
M_edge(X,Y)=[f1 X^2+f0 Y^2-2mXY]/8.
```

见 [shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L17)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L21)。旧 inverse-root argument 给出 `m^2<f0 f1`，从而 endpoint matrix 正定并且 `f0+f1-2m>0`：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L23)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L28)。

对正定二次型 `M_edge`，在约束 `X-Y=1` 下的最小值为

```text
(f0 f1-m^2)/[8(f0+f1-2m)],
```

这正是定义的 `kappa(u,s)`。等价地，令 `M_edge-kappa(X-Y)^2` 的二阶矩阵行列式为零也得到同一值。作者在 [shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L30)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L48) 给出这一路径。该论证是标准 Schur/Rayleigh 商计算，闭合；无需运行脚本。

旧 `3/8` lemma 给出 `kappa>=3/8`，所以新系数确实是对 uniform `3/8` 的 pointwise sharpening。

## 3. Opposite-edge parallel combination：`CORRECT`

四个实际 edge kappas 定义在同一 half-leaf rectangle 的四条边上：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L50)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L62)。对水平差

```text
r_plus=T00-T10,
r_minus=T01-T11,
Delta=r_plus-r_minus,
```

最小化 `kA_plus r_plus^2+kA_minus r_minus^2` under fixed `Delta` 给出 coefficient

```text
KA = kA_minus*kA_plus/(kA_minus+kA_plus).
```

这就是 weighted Cauchy / parallel-sum 系数；文本见 [shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L64)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L75)。垂直边同理给出 `KB Delta^2`。代入 d995 已审的 exact corner identity 后得到 lower bound (7)：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L77)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L86)。

关键点正确：`KA`、`KB`、`J` 和四个 kappas 都来自同一组 corner values，不是独立优化变量。

## 4. Refined sufficient theorem：`CORRECT`

Theorem 2 断言 strict connected half-leaf arrow 若满足

```text
KA+KB > J/(32AB),
```

则完整 Shannon Hessian 在所有六个真实物理方向上严格负定：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L88)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L99)。证明使用两个正性块：

1. binary potential 在 `[-log 2,0]`，故 `0<J<2 log 2<2<4`，所以 `4d^2+4e^2+2Jde` 正定；见 [shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L100)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L108)。
2. 条件 `KA+KB>J/(32AB)` 使 alternating cell coefficient 严格正。

若 lower bound 为零，则 completed edge squares、`(d,e)` block 和 cell mode 全为零；这复用 d995 Theorem 5.1 的 strictness argument，推出 `d=e=T=0`，再由已审的可逆方向映射推出物理方向 `D=0`。因此非零方向上严格正的 `Q=-H''` 成立。

该充分定理的结论边界也正确：因为每个 `kappa>=3/8`，每个 opposite-edge parallel pair 至少为 `3/16`，所以 `KA+KB>=3/8`；旧条件 `J<12AB` 即 `J/(32AB)<3/8`，是新条件的 coarse corollary：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L110)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L116)。这证明 refinement 至少不弱于旧充分条件。

## 5. 结论边界与 failure ledger：`CORRECT`

文本明确说明：固定形状 `A=1/4,B=4/9` 已由 d995 coarse corollary 完全闭合，refinement 对该证明不是必要条件：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L118)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L121)。对一般 half-leaf arrows，剩余问题是实际标量不等式 `KA+KB>=J/(32AB)`，并且没有 universal proof 被声称：[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L122)–[shared_corner_parallel_refinement.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md#L130)。

Failure ledger 也保持同一边界：独立 scalar bounds、one-axis secants 和 relaxed negative diagnostics 都不能替代 shared-corner condition；没有 universal half-leaf 或 unequal-leaf theorem 被声称：[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L5)–[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L10)。资源 ledger 明确无 PR60 证书重跑、无 issue73 job、无长消元、无 formal proof assistant 或 independent arithmetic reviewer：[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L36)–[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L44)。

我没有把 ledger 中 “independent reconstruction performed in this unit” 当作独立 SECOND 审阅；ledger 自身也说 public checker 仍是 same-author computational evidence：[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L12)–[failure_ledger_shared_corner.md](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md#L22)。

## 6. 作者脚本和输出的证据地位：`SOURCE_ONLY`

`shared_corner_cell_check.txt` 第一行即说明这是 same-author exact checker run, not independent review：[shared_corner_cell_check.txt](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt#L1)–[shared_corner_cell_check.txt](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt#L6)。PASS 列表只作为作者记录，不作为本 SECOND 的计算证书：[shared_corner_cell_check.txt](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt#L8)–[shared_corner_cell_check.txt](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt#L18)。

`verify_shared_corner_cell.py` docstring 同样声明不替代 independent review：[verify_shared_corner_cell.py](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/verify_shared_corner_cell.py#L1)–[verify_shared_corner_cell.py](https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/research/I05-22-R5-logmean-imbalance/verify_shared_corner_cell.py#L8)。静态源码显示它主要验证旧 shared-corner cell decomposition、one-edge `3/8` completion、fixed-shape rational gates、三方向 complete-event comparison 和 quantitative Gram minors；它没有作为新 `kappa/KA/KB` refinement 的独立 C2 证书使用。该脚本未被运行或导入。

## 未闭合项

`CRITICAL_GAPS` relative to broader goals, not to this delta theorem:

- universal `KA+KB>=J/(32AB)` 未证明；
- 一般 half-leaf arrows、unequal leaf diagonals、general missing-edge entropy concavity 未闭合；
- issue73 filament/point/subdivision 工作未启动；
- novelty `NOT_ASSESSED`；
- formal verification `NOT_PERFORMED`；
- checker PASS、脚本 reconstruction、18 行输出未独立认证。

## 最小修复建议

无需修复本 delta 的数学主论证。若作者想让读者更快验证，可在 Lemma 1 后补一行显式 Schur/Rayleigh 计算：对 `M_edge` 的矩阵求 `1 / ([1,-1] B^{-1} [1,-1]^T)` 得到 (2)。这只是说明增强，不影响正确性。
