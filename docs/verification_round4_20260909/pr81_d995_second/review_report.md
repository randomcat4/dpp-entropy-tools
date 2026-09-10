# PR81 d995 SECOND review report

## 有界结论

`CORRECT` for the new d995 shared-corner analytic unit, within the stated scope.

我接受 `shared_corner_cell_theorem.md` 中的主解析链条：完整八事件与六方向接口保留；one-edge Gram lemma 成立；四角 shared-corner decomposition 与 PR70 成对核心相容；条件 `J<12AB` 足以推出严格 `Q_K(D)=-H''(K;D)>0`；固定形状 `A=1/4, B=4/9` 在全合法 `0<q<11/36` 上由简单解析估计给出 `J<12AB`。因此该单元闭合的是一个完整的 strict connected half-leaf fixed family，包括非零 Lambda 点；它不闭合一般 missing-edge 或一般实三点 Shannon concavity。

大有理数 minors、作者 checker PASS、诊断浮点值和 relaxed stress tests 没有被当作独立证据接受；它们也不是上述解析定理的必要前提。

## 1. 来源与绑定：`CORRECT`

`input_binding.json` 绑定五个作者来源；本机核对结果为 0 缺失、0 delivered SHA 不匹配、0 行数不匹配。三份 redacted 文件的 original SHA 与 delivered SHA 不同，但绑定明确说明这是非数学 review-history/status 文本的等行数删除。`source_binding.json` 记录了每个被读文件的实测 SHA-256、字节数和行数。

我没有把 `original_git_blob`/`original_sha256` 与本地 redacted `delivered_sha256` 混称。数学审阅以 delivered packet 为准，同时记录其 public-path/original provenance。

## 2. 完整八事件与六方向接口：`CORRECT`

PR70 来源给出三点 DPP 的八个 complete atoms，并明确 entropy 使用全部八个 atom、自然对数和真实 kernel-affine 方向：[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L13)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L21)。同一文件给出 connected missing-edge domain `0<x,y<1, A,B,q,qbar>0` 与 Schur-complement 解释：[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L23)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L33)。方向坐标变换 `(d,e,U)` 到真实六个矩阵方向可逆，公式见 [pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L40)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L49)，并特别提醒 marginal `Pij''` 不可丢弃：[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L56)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L60)。

新 d995 文件在 half-leaf 专门化中重新列出八个 atoms、`Q=-H''` 的 Fisher+acceleration 完整公式，并声明所有八个 atoms、complete Fisher、每个 acceleration 和六个实对称方向都保留：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L17)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L31)。其 half-leaf 方向坐标映射在 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L52)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L70)；`E` 可逆，因此 `(d,e,T)` 没有丢方向。

结论：完整事件和六方向接口没有被 relaxed scalar 模型替代。

## 3. One-edge Gram lemma：`CORRECT`

Lemma 3.1 的核心是把 edge quadratic 完成平方后，剩余二端点矩阵降为

```text
[[f(u+s)-3, 3-m_edge],
 [3-m_edge, f(u)-3]].
```

该矩阵的正定性来自 `r=f-3>0` 与

```text
(m_edge-3)^2 < [f(u)-3][f(u+s)-3].
```

作者的证明定义 `w=(f-3)^(-1/2)`，给出 `w''<=0` 的显式公式：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L135)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L146)。由于 `w` 在非平凡区间严格凹，`w(t)` 严格高于端点弦；再用递减函数 `x -> x^{-2}` 并积分 affine reciprocal-square，可得平均 `r` 严格小于端点几何平均：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L148)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L155)。完成平方与二端点矩阵在 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L157)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L170)。

我检查了代数结构：完成平方后确实得到该二端点矩阵；`f>=4` 给出正对角；严格弦不等式给出严格正行列式。因此 lemma 的 derivative/chord/Gram argument 闭合。

## 4. Shared-corner decomposition：`CORRECT`

`shared_corner_cell_theorem.md` 没有把四个边 scalars 放松成独立范围，而是固定同一组角点

```text
g(q), g(q+A), g(q+B), g(q+A+B)
```

并定义四条实际 opposite-edge integral 与共同 `lambda`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L74)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L107)。这与较早 `coupled_gram_fixed_shape.md` 所指出的最小缺失相关性一致：两个轴必须共享同四个 corner logits，而不能各自独立选 secant：[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L366)–[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L379)。

核心恒等式 (6) 在 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L188)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L198)。静态核查其结构与 PR70 full paired core 相容：在 `x=y=1/2` 时，PR70 的 `L,C,F,R` 成对核心给出 marginal `4d^2+4e^2`、paired `2Jde`、四条边的 Fisher endpoint weights、四条 edge integral 的 `d/e` cross terms，以及 `n=A k+B ell-J` 留下的唯一 alternating shared-cell 负项 `-J Delta^2/(32AB)`。这正是公式 (6)-(7) 的结构：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L200)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L210)。

结论：分解保留了 shared corner cell；没有回退到此前已知不足的 two independent Gram ellipses 或 free scalar relaxation。

## 5. `J<12AB` 充分定理：`CORRECT`

由四条 edge lemma 加上

```text
(T00-T10)^2+(T01-T11)^2 >= Delta^2/2,
(T00-T01)^2+(T10-T11)^2 >= Delta^2/2
```

作者得到 lower bound (8)：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L212)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L226)。条件 `J<12AB` 使 `3/8-J/(32AB)>0`。又因 strict legal half-leaf 有 `A+B<1`，故 `AB<1/4`，于是 `J<12AB<3<4`，二次型 `4d^2+4e^2+2Jde` 严格正，除非 `d=e=0`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L232)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L260)。

严格性论证也闭合：若 lower bound 为零，则 `d=e=0`、`Delta=0`，四个 edge squares 强制四个 pair sums 为零；这些线性方程只允许 alternating vector `(t,-t,-t,t)`，再由 `Delta=4t` 得 `t=0`，所以 `T=0`，继而 `U=0`，可逆方向映射给出 `D=0`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L262)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L269)。

因此 Theorem 5.1 在其 stated half-leaf domain 中证明 `Q=-H''>0` 对所有非零真实六方向成立。借 PR70 的 positive pivot/equivalence，这推出继承的 `E_H>0` 与 `det E_H>0`；PR70 的相应二阶核心与 pivot 解释在 [pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L231)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L253)。

## 6. 固定形状 `A=1/4, B=4/9` 全合法 q 区间：`CORRECT`

固定形状定义为

```text
A=1/4, B=4/9, A+B=25/36, 12AB=4/3,
0<q<11/36.
```

见 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L282)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L290)。这满足 strict legal 条件：`A>0`、`B>0`、`A+B<1`、`q>0`、`qbar=11/36-q>0`。`b=1/4,c=1/3` 的符号由 diagonal sign conjugation 覆盖：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L33)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L42)。

`J(q)` 关于 `q <-> 11/36-q` 对称且严格凸；严格凸函数在闭区间内部低于相等端点值，所以 `J(q)<J(0)`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L292)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L303)。端点值为 `h(1/4)+h(4/9)-h(25/36)`，故小于 `h(1/4)+h(4/9)`。简单界

```text
log 2 < 7/10,
log(4/3)<1/3,
h(1/4)<3/5,
h(4/9)<log 2<7/10
```

给出 `J(q)<13/10<4/3=12AB`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L305)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L325)。其中 `log 2<7/10` 的指数级数证据写在 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L314)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L319)；`log(4/3)<1/3` 也由 `exp(1/3)>1+1/3=4/3` 直接给出。无需任何数值 interval 或 filament scan。

结论：固定形状在完整 open legal q interval 上满足 Theorem 5.1 条件，因此 `Q=-H''` 对所有非零真实方向严格正。

## 7. Strictness/coercivity：`CORRECT` for qualitative analytic coercivity; quantitative minors `NOT_CERTIFIED`

作者给出更强的显式 lower bound `Qstar`：[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L329)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L338)。该 bound 的来源可由 (8)、`f>=4`、`J<13/10`、`AB=1/9` 直接读出：

- edge square 系数给出 A-edge 的 `1/4` 和 B-edge 的 `64/81`；
- `4d^2+4e^2+2Jde >= (4-J)(d^2+e^2) > 27(d^2+e^2)/10`；
- `3/8-J/(32AB) > 3/320`。

即使不认证六个 Sylvester minors，也可用零空间论证证明 `Qstar` 正定：若 `Qstar=0`，先由 `27(d^2+e^2)/10` 得 `d=e=0`，由 `3 Delta^2/320` 得 `Delta=0`；四个 edge-sum squares 再给出 `T00+T10=T01+T11=T00+T01=T10+T11=0`，故 `T=(t,-t,-t,t)`，而 `Delta=4t=0`，所以 `T=0`。于是全部坐标为零。有限维正定二次型自动给出某个 uniform coordinate coercivity constant。

作者列出的六个 leading principal minors 在 [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L340)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L351)。本轮未做 Gram/minor arithmetic，因此不把这些有理 minors 认证为独立数量证书；但 qualitative strictness/coercivity 不依赖它们。

## 8. 其他 PR81/PR70 单元的角色

`input/proof.md` 的 paired-logit compression、`J` symmetry/convexity 和 imbalance bounds 是合理的来源接口，并且它明确声明一般 determinant target 仍未闭合：[proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/proof.md#L248)–[proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/proof.md#L267)，scope ledger 也未把 scalar bounds 冒充为 universal entropy theorem：[proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/proof.md#L269)–[proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/proof.md#L279)。

`input/coupled_gram_fixed_shape.md` 的 relaxed negative determinant、large rational minors、same-q secant diagnostics 与 stress test 均被作者标为 diagnostic / non-sufficiency / not theorem：[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L222)–[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L260)，[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L366)–[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L393)。这些不构成独立数学证据；但它们也不阻断新的 shared-corner 解析证明，因为后者使用更强的共同四角分解，而不是 relaxed determinant search。

`pr70_source/thinning_bridge.md` 保持了 full entropy、conditional entropy 与 one-sided statement 的逻辑区别，并提醒边际 Fisher 不能被 side certificate 取代：[thinning_bridge.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/thinning_bridge.md#L5)–[thinning_bridge.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/thinning_bridge.md#L12)，[thinning_bridge.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/thinning_bridge.md#L94)–[thinning_bridge.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/thinning_bridge.md#L106)。这与 d995 不把一般 one-sided/conditional target 当作 full entropy conclusion 的边界一致。

## 9. 未闭合项

`CRITICAL_GAPS` relative to broader ambitions, not to the d995 fixed-family theorem:

- 一般 strict half-leaf arrows failing `J<12AB` 未闭合。
- 一般 missing-edge arrows、unequal leaf diagonals、general real three-point Shannon concavity 未闭合。
- novelty `NOT_ASSESSED`。
- formal proof `NOT_PERFORMED`。
- 作者 checker PASS、diagnostic floating values、large rational minors 未独立认证。

## 最小修复建议

对 d995 解析主定理无需数学修复。若作者想让文本更自含，可在 Theorem 5.1 前后补一段从 PR70 `L,C,F,R` 到公式 (6) 的展开说明；当前报告认为该恒等式可由给定公式静态追踪闭合，但正文中“direct transformation”略压缩。另可把 `log(4/3)<1/3` 的一句 `exp(1/3)>4/3` 写出，以免读者误以为用了数值近似。
