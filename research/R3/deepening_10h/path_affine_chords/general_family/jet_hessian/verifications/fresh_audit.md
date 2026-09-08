STATUS: CORRECT

# D10-B3 fresh non-author audit

范围：本报告只核验 D10-B3 修正版 `jet_hessian/` 的二阶 jet DP、低维
exact-event 对照、n=93 冻结异常解释，以及修正后 n=5..100/4608 有限扫描的
可复现统计。它不证明固定-beta 族凹性，也不把有限搜索定理化。

只读材料：

- `jet_hessian/derivation.md`
- `jet_hessian/jet_hessian.py`
- `jet_hessian/run_log.md`
- `jet_hessian/verdict.md`
- `jet_hessian/results/summary.json`
- 既有 `jet_hessian/verifications/anomaly_*` 证据

新增文件仅：

- `jet_hessian/verifications/fresh_b3_audit_check.py`
- `jet_hessian/verifications/fresh_audit.md`

未运行作者脚本的主命令，因为 `jet_hessian.py` 的 CLI 会写回作者
`results/`；本轮用独立脚本在验证目录内重建检查。

## 1. 数学递推核查

### K-affine 与 L 入口

`derivation.md:31-37` 给出

`tau(t)=tau_0+t delta`,

`K(t)=K(0)-t R^{-1}diag(delta)R^{-T}`。

这确实是 K 空间仿射线。`derivation.md:46-67` 的
`w_i=1/tau_i`、`w_i'=-delta_i/tau_i^2`、`w_i''=2 delta_i^2/tau_i^3` 以及
三对角 `L=R^T diag(1/tau) R-I` 的对角/边项公式正确。作者实现对应
`jet_hessian.py:141-160`；我脚本的独立实现见
`fresh_b3_audit_check.py:83-99`。

### interval continuant jets

`derivation.md:78-107` 的 continuant

`kappa(a,b)=d_b kappa(a,b-1)-e_{b-1}^2 kappa(a,b-2)`

及一、二阶 jet 展开正确；作者实现见 `jet_hessian.py:183-198`。我重新实现
同一递推并在所有区间 determinant 正时继续，否则报错，见
`fresh_b3_audit_check.py:102-121`。

### selected-run DP 与 exact event 语义

三对角 `L` 的主子式按选中点的连续 run 分解。最后一个坐标要么不选，要么
属于最后连续选中段 `[start,end]`，其前缀长度为 `0 if start==0 else start-1`。
作者代码的空前缀约定在 `jet_hessian.py:219-231`，我独立实现为
`fresh_b3_audit_check.py:125-137`；该 selected-run 分解是互斥且穷尽的。

熵公式 `H=log Z-T/Z` 在 `derivation.md:153`，作者改用稳定商
`jdiv` 见 `jet_hessian.py:77-95` 与 `jet_hessian.py:233`。这避免了旧
`jinv` 的 `Z^{-3}` 中间量；旧公式仍保留为诊断函数 `jet_hessian.py:69-74`，
并只在异常解释中被调用 `jet_hessian.py:1404-1407`。

`derivation.md:133-135` 的 `T_m` 展示式少了显式加号；按上下文应读作
`T_{m-1} + sum block*T_prefix + sum Z_prefix*block log block`。作者代码
`jet_hessian.py:221-229` 与 exact-event gate 均支持这个读法。此为非阻断
排版/陈述瑕疵，不影响本轮对实现和结论的 CORRECT 判定；若进入论文文本，
建议显式补 `+`。

## 2. exact-event Hessian gate

作者 exact-event gate 位于 `jet_hessian.py:622-700`：先由
`K=I-R^{-1}diag(tau)R^{-T}` 的包含主子式微分得到 inclusion jets，再做
Boolean Möbius 反演到 exact atoms；熵导数公式使用 `sum p'=sum p''=0`。
这不是把 `det K_S` 误作 exact event。作者低维入口在
`jet_hessian.py:723-801`。

我的独立 n=5 rank2 有理 gate：

- events：32；
- min atom：`1/55440`；
- exact Möbius `H2`：
  `-0.00410850374951372109885718735311506334468536733695630370224737695554621232820612431298521088`；
- DP `H2`：
  `-0.0041085037495137210988571873531150633446853673369563037022473769555462123282061243129852080`；
- 误差：`H 2e-89`，`H1 1.9e-90`，`H2 2.88e-90`。

该 gate 见 `fresh_b3_audit_check.py:159-257`。它独立验证了 low-dimensional
exact-event Hessian 语义；有限维对照不升级为一般定理。

作者 summary 的 n=5,6,7 gate 也记录为 PASS：
`summary.json:3-19`，最大差分别约 `5.77e-15, 1.78e-15, 1.07e-15`。

## 3. n=93 冻结异常与下溢解释

作者 summary 记录的冻结异常见 `summary.json:146-172`：

- n=93, rank2, trial 15, seed `20260908`；
- support `[45,85]`；
- legacy unstable `H2=184.7448188718266`；
- stable float `H2=-0.007024918933640795`；
- Decimal precision-110 `H2=-0.007024918933615582731289762931...`；
- strict DPP margin lower bound `1/50`。

既有 anomaly triage 独立重建了参数流并匹配全数组，见
`anomaly_triage.md:10-18`；它还用不同的 normalized run-category DP 拒绝该
正号，见 `anomaly_triage.md:52-60`。

我的 fresh 脚本再次读取冻结参数并独立计算：

- stable float `H2=-0.007024918933640795`；
- Decimal `H2=-0.007024918933615582731289762931`；
- 与作者 precision-110 summary 的差约 `3.94e-31`；
- `h=0.0005` 的 value-only chord：
  - central `H2=-0.00702491895031949107089843420973463051394706845699376510096053815786884`；
  - midpoint gap `-8.7811486878993638e-10`。

下溢机制也复现：

- legacy inverse formula 复得 `184.7448188718266`，与作者值差 `0`；
- `1/Z^3` 的 float 值为 `0.0`；
- 对应 Decimal 为 `4.143045588912394237886349994E-355`；
- 预测上移误差
  `184.7518437907601821165382672`，解释旧正号的量级和符号。

结论：n=93 正号是旧 reciprocal-jet normalization 的中间下溢/消去假阳性，
不是可提升候选。

## 4. n=93 可行性、rank2、非 thinning

作者推导说明 `P=S^{-1}` 的谱证书策略在 `derivation.md:208-224`，summary
记录 lower bound `1/50` 于 `summary.json:160`。我的脚本将冻结十进制字符串
作为 exact rationals，在 `t=±1/10` 对三对角
`P(t)=R^T diag(1/(tau+t delta))R` 检查：

- `P(t)-4I` 的 93 个 LDL 枢轴全部正；
- `50I-P(t)` 的 93 个 LDL 枢轴全部正；
- 最小枢轴浮点摘要：
  - `t=-1/10`：`P-4I` 最小约 `3.0922679212228976`，`50I-P` 最小约 `8.762647849887912`；
  - `t=1/10`：`P-4I` 最小约 `3.0937509028649197`，`50I-P` 最小约 `4.663234155034177`。

因此端点满足 `4I<P<50I`，等价得到
`1/50 I<S(t)<1/4 I`。由于 `S(t)=R^{-1}diag(tau+t delta)R^{-T}` 对 t 仿射，
该谱裕量覆盖整段 `[-1/10,1/10]`。`delta` 支持大小为 2，且 `R^{-1}` 可逆，
所以 `Kdot=-R^{-1}diag(delta)R^{-T}` rank 为 2；而严格中心 `K` 满秩，故
该方向不可能是 thinning 比例方向。

相关 fresh 代码见 `fresh_b3_audit_check.py:442-489` 与
`fresh_b3_audit_check.py:492-533`。

## 5. 修正后 n=5..100 / 4608 扫描复现

作者扫描逻辑在 `jet_hessian.py:1002-1099`，summary 记录为
`summary.json:32-48`：

- n：5..100；
- trials per n：24；
- buckets：rank2 与 full_rank；
- total evaluations：4608；
- positive stable-float normalized `H2>1e-10`：0；
- global max / closest-to-zero：n=34, rank2, trial 8，
  normalized `-3.2491091342052325`。

我的脚本从 seed `20260908` 重放相同 beta/center/delta 生成规则，独立计算
stable quotient jet 与 `||Kdot||_F^2`，见
`fresh_b3_audit_check.py:286-431`。复现结果：

- total evaluations：4608；
- failures：0；
- positive normalized `H2>1e-10`：0；
- global max：n=34, rank2, trial 8；
- `H2=-0.4014773021872555`；
- `||Kdot||_F^2=0.12356534840909898`；
- normalized `-3.2491091342052325`；
- 与 summary 的 global max value 差：`0.0`。

这支持“修正后同范围扫描无正号”的统计可复现性。它仍只是有限搜索分母：
96 个 n 值 × 24 trials × 2 buckets = 4608 次评估，不能推出固定-beta 族或
一般实 DPP 熵凹性。

## 6. 运行命令、退出码、分母

工作目录：

`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`

命令：

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\path_affine_chords\general_family\jet_hessian\verifications\fresh_b3_audit_check.py
```

运行记录：

1. 第一次退出码 1。原因是 fresh 验证脚本初稿中我把 `random_center` 的全局
   `scale` 错写成逐坐标重抽样，导致扫描 RNG/样本流偏移；低维 gate 和 n=93
   稳定检查已通过，但扫描 global max 不匹配。此为验证脚本错误，不是作者结论
   错误。
2. 修正后同命令退出码 0，耗时约 17.02 秒，Python 3.12.14。

最终分母：

- low-dimensional exact families：1；
- low-dimensional exact events：32；
- n=93 frozen centers：1；
- n=93 rank2 directions：1；
- n=93 value-only chords：1；
- scan n values：96；
- trials per n：24；
- buckets per trial：2；
- scan evaluations：4608；
- random seed：20260908；
- failed assertions after fix：0。

线程/资源：脚本设置 `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=1`；
标准库，无 GPU，无远端，无依赖安装。

## 7. Verdict

D10-B3 修正版对其实际声明是 CORRECT：

- O(n^2) selected-run second-order jet DP 与 exact-event Hessian low-dimensional
  gate 对齐；
- n=93 legacy positive signal 被稳定 float、Decimal、value-only chord 与下溢误差
  公式共同拒绝；
- 冻结 n=93 点严格可行、rank2、非 thinning；
- 修正后 n=5..100 / 4608 扫描统计可复现，正号计数为 0。

保留边界：这不是固定-beta 族凹性定理，更不是全实域 DPP 熵凹性证明；未来任何
float 正号仍需 Decimal、log-scaled 或 interval-certified replay 后才能提升为
候选。
