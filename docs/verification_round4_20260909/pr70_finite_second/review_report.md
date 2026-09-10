# PR70 固定有限对象 SECOND 审查报告

固定 PR70 有限对象的结论：请求范围内的 P2/P5/P6 计算证据为 `CORRECT`。这只是有限对象验证。Novelty 为 `NOT_ASSESSED`；formal 为 `NOT_PERFORMED`。

## 1. 绑定与范围

**Verdict: CORRECT.**

`input_binding.json` 声明作者 head `f7be60759fd4d65184803b6585965dc7e5ccd624` 和 8 个文件。交付的 `input/` 下 8 个文件全部存在，且 SHA-256 全部匹配。

`machine_input_binding.json` 声明 PR85 raw head `611d5f70e8bb70237755ca4fdbe8ab14c8b715c1`、executable head `29d4d77d7dba65de933d196a89b4db2616234991`、author head `f7be60759fd4d65184803b6585965dc7e5ccd624` 和 74 个文件。交付的 `machine_input/` 下 74 个文件全部存在，且 SHA-256 全部匹配。

本轮未读取被禁止的 C1 FIRST、历史 SECOND、C3 裁定、machine topREADME、machine_notes、FINAL_HANDOFF 或 `[excluded private directory]`。C2 原始代码/输出只作为独立计算证据，不作为数学审查意见。

## 2. 冻结对象

**Verdict: CORRECT.**

`machine_input/inputs/object.json` 中的固定对象与作者 `input/post_checkpoint.md:14-19` 和 `input/post_checkpoint.md:79-96` 一致：

- `K=[[1/25,0,2/15],[0,3/4,1/4],[2/15,1/4,18/25]]`。
- `D=[[1,-7/5,11/9],[-7/5,1/5,0],[11/9,0,-1/7]]`。
- `tau=1/100000`。
- 导数在物理线 `K+tD` 上。
- C2 二进制 mask 顺序 `[0,1,2,3,4,5,6,7]` 对应作者事件顺序 `0,1,2,12,3,13,23,123`。

`input_echo.json` 回显同一对象、source PR 70、source head、自然对数、`atanh_terms=80` 和 `maximum_interval_width=1e-32`。

## 3. 执行封套

**Verdict: CORRECT.**

运行计划声明单个 600 秒 deadline、单 CPU thread、固定 `N=80`、数学失败后不重跑、失败时不提高精度或深度（`machine_input/execution/RUN_PLAN.md:5-13`）。`run_guard.sh` 通过创建/复用一个 deadline 文件、导出单线程数值环境、设置 checker 绝对 deadline、施加 16 GiB 虚拟内存上限、记录起止/PID 文件并用 `timeout` 运行来落实这些约束（`machine_input/execution/run_guard.sh:21-54`）。

原始执行证据：

- `start_utc.txt`: `2026-09-10T02:10:08Z`。
- `deadline_utc.txt`: `2026-09-10T02:20:08Z`。
- `exit.json`: exit code `0`，finished `2026-09-10T02:10:10Z`。
- `STATUS.json`: `MACHINE_PASS`，`all_checks=178`，elapsed `1.154991258867085`，PID `175598`。
- `RUN_LEDGER.json`: `prior_arithmetic_attempts: 0`，`repairs: []`，`budget_state: CLOSED_ON_SUCCESS; original deadline retained; no rerun or continuation`。
- `pid_absence.json`: PID `175598`，`present: false`，checked `2026-09-10T02:10:38Z`。
- `stderr.log` 为空。

prep manifest 还列出 `.gitattributes` 和一个顶层 `README.md`，它们不在本二审公开包中；其中顶层 README 也属于用户明确禁止读取的 machine topREADME 类别。所有已交付并参与计算的 prep 文件（`execution/`、`implementation/`、`inputs/`）均与 prep SHA-256 匹配。

## 4. 完整事件与 jets

**Verdict: CORRECT.**

作者在 `input/proof.md:19-21` 说明 complete entropy 使用全部八个 atoms，并在真实物理线 `K+tD` 上取导；`input/post_checkpoint.md:43-54` 列出全部 8 个 PR70 event jets。

C2 独立构造：

- inclusion minors 由排列展开取得，再做 subset Mobius inversion（`independent_pr70_checker.py:102-140`）。
- signed complete-event determinants 由 absent diagonal shift 与递归 Laplace 展开取得（`independent_pr70_checker.py:143-151`）。
- jets 使用二阶导数因子 `2`（`independent_pr70_checker.py:154-156`）。

`CHECKS.jsonl` gates 2-17 通过全部 8 个 dual polynomial 比较与中心 atom positivity。Gates 24-47 通过全部 24 个 literal `(p,p',p'')` 比较。`events.json` 精确记录所有 8 行 jets；例如第 0 行为 `(31/11250, -109307/9450000, -6137/354375)`，第 7 行为 `(173/30000, 144523/1050000, -269057/39375)`。

## 5. 叶边缘、归一化与三点合法性

**Verdict: CORRECT.**

C2 将四个 leaf marginal 多项式与独立构造的二点律比较（`independent_pr70_checker.py:303-315`）。Gates 18-21 通过。Gates 22-23 通过 full polynomial normalization 与 jet normalization。

对 `K-tau D`、`K`、`K+tau D` 及其 complements，C2 计算 leading Sylvester minors 并与作者 P6 字面值比较（`independent_pr70_checker.py:327-343`）。Gates 48-83 通过全部六组三元组的 positivity 与 literal matching。匹配值为：

- `minus_K`: `3999/100000`, `1874526239/62500000000`, `81722984551974671/14175000000000000000`。
- `minus_complement`: `96001/100000`, `15000276239/62500000000`, `4340182176969481/1575000000000000000`。
- `center_K`: `1/25`, `3/100`, `173/30000`。
- `center_complement`: `24/25`, `6/25`, `31/11250`。
- `plus_K`: `4001/100000`, `1875473739/62500000000`, `81762005761973329/14175000000000000000`。
- `plus_complement`: `95999/100000`, `14999723739/62500000000`, `5579765768960953/2025000000000000000`。

Gates 84-110 通过三个点的 probability normalization 与全部 8 个 atom positivity。

## 6. P2 / P3 quotient 核验

**Verdict: CORRECT.**

作者 P3 quotient identity 位于 `input/post_checkpoint.md:39-41`；P2 精确分数位于 `input/post_checkpoint.md:21-35`。

C2 对每个 side/marginal 同时用 generic jet product/inverse 规则和 P3 公式计算 `(P^2/r)''`（`independent_pr70_checker.py:349-360`）。Gates 111-118 通过全部 8 个 P3 row 比较。Gates 119-121 通过三个 P2 精确分数：

- `Phi0 = -17195245284290193050175018195000/102736068486597078628140399487`。
- `Phi1 = 459391680374575413414186538171831635000/2825836508547416584007832972390257641`。
- `Phi_pair = -125413424484215487448116244468280440113219969455538795750000/26102637294738394550409051443126654598253142521608171454843`。

Gates 122-123 通过 strict negative sign 与 literal interval containment。`intervals/Phi_pair.json` 中的 outward decimal enclosure 为 `[-4.8046265619871114230253298325745148413179, -4.8046265619871114230253298325745148413178]`，包含于作者区间。

## 7. P5 曲率 gates

**Verdict: CORRECT.**

作者 P5 区间位于 `input/post_checkpoint.md:68-77`。`input/proof.md:227-259` 明确说明 full entropy 保留双 side 与 marginal Fisher。

C2 保留 separate full Fisher、full acceleration、leaf Fisher、leaf acceleration、side terms 和 retained `P''` terms：

- full/leaf curvature 构造：`independent_pr70_checker.py:262-267` 和 `371-373`。
- side direct derivative 与 quotient/product derivative，包括 `retained_Psecond_term`：`independent_pr70_checker.py:380-397`。
- 结构恒等式 `G0+G1 = -Hfull'' + Hleaf''`：`independent_pr70_checker.py:403-408`。
- interval evaluation 与 P5 比较：`independent_pr70_checker.py:409-417`。

Gates 124-133 通过 side derivative-row 与 side-total dual checks。Gate 134 通过 `conditional_structural_identity`。Gates 147-158 通过四个 P5 量的 width、broad sign 与 literal containment。

记录的 outward decimal intervals：

- `G0`: `[6.3836477267924650532084343120505471181471, 6.3836477267924650532084343120505471181472]`。
- `G1`: `[9.2177300388618574492302078622332257604485, 9.2177300388618574492302078622332257604486]`。
- `-Hconditional''`: `[15.6013777656543225024386421742837728785956, 15.6013777656543225024386421742837728785957]`。
- `-Hfull''`: `[41.8563777656543225024386421742837728785956, 41.8563777656543225024386421742837728785957]`。

这些具有作者 P5 的正符号，但不提供全局 one-sided 或 full-entropy theorem。

## 8. N80 对数与区间 gates

**Verdict: CORRECT.**

作者在 `input/post_checkpoint.md:100-107` 描述归一化 atanh log 包围与端点反转。C2 固定使用 `NTERMS=80`，不是自适应精度（`independent_pr70_checker.py:18-19`、`218-258`）。区间 scaling 函数对负乘数反转端点（`independent_pr70_checker.py:169-175`），decimal rendering 使用向外 integer floor/ceiling（`independent_pr70_checker.py:177-187`）。

`log_inventory.json` 记录 `N=80`、28 个 log arguments、`log2_file=logs/log2.json`、normalization `argument=2^k*y; 1<=y<2; w=(y-1)/(y+1)`、tail formula `2*w^(2*N+1)/((2*N+1)*(1-w^2))`，以及 negative multiplier rule `swap lower and upper before scaling`。

Gates 135-174 通过全部 28 个 positive log argument checks。P5 与 Jensen 各自有 separate width、broad sign 和 literal containment gates（`independent_pr70_checker.py:277-288`），所以符号通过没有与字面区间包含混在一起。

## 9. P6 完整 Shannon Jensen gate

**Verdict: CORRECT.**

作者 P6 位于 `input/post_checkpoint.md:92-98`。它明确是 complete-event Jensen difference，不是 full entropy counterexample。

C2 从 `K-tau D`、`K`、`K+tau D` 的全部 8 个 atom probabilities 计算 entropy（`independent_pr70_checker.py:270-274`、`419-430`）。`jensen_assembly.json` 同时记录 linear log-form interval 与 three-entropy assembly interval；gate 175 通过二者 overlap。Gates 176-178 通过 width、strict negative sign 与 literal containment。

Jensen outward interval 为 `[-0.0000000020928189192765834280721741836172, -0.0000000020928189192765834280721741836171]`，包含于作者 P6 `[-0.000000002092818919276583428073, -0.000000002092818919276583428072]`。

该负值对显示的合法三点具有 Shannon concavity 符号。它不是凹性违例，也不是 negative full-entropy Hessian certificate。

## 10. 解释

**Finite-object conclusion: CORRECT.**

对固定 PR70 rational `K,D,tau`，C2 独立 raw implementation 与 outputs 支持：

- P2 的 exact negative `Phi_pair''`；
- P5 中 side、conditional、full 四个曲率区间为正；
- 六组 endpoint/center kernels 由 Sylvester minors 证实为正；
- P6 complete Shannon Jensen interval 严格为负，具有凹性符号。

**Global conclusion: INCOMPLETE.**

本轮证据不证明也不反驳全局 `G1''>=0`、全局 conditional entropy concavity、全局 full entropy determinant positivity 或三维 Shannon concavity。辅助 paired-resolvent 负曲率仍只是有限方法 obstruction，不得提升为全局熵命题。
