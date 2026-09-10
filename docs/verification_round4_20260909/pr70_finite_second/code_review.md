# C2 固定 PR70 checker 静态代码审查

范围：只做静态检查。未执行 `independent_pr70_checker.py`、作者脚本或任何数学 checker。检查对象为源码、原始 JSON 输出、执行记录和哈希。

## Verdict

在请求的固定有限对象范围内，没有发现会使 P2/P5/P6 机器证据失效的代码级缺陷。实现范围窄，使用 exact rational，且 gate 有序。`CHECKS.jsonl` 中 178 个记录 gate 全部通过，原始输出文件与 `machine_input_binding.json` 匹配。

一个非数学 provenance caveat：`output_hashes.json` 记录了 `invocation_private.txt` 的 hash，但交付包因 redaction 省略该 private invocation 文件；`PREPARATION_SHA256.json` 还提到 `.gitattributes` 和顶层 `README.md`，它们也未交付于本 review package。ledger 已解释 private invocation redaction。这不影响 computation-bearing code/input/execution 的哈希一致性；这些文件全部与 prep 匹配。

## 代码路径观察

**独立事件构造：CORRECT.**

`det_leibniz` 用 permutation expansion 构造 inclusion determinants（`independent_pr70_checker.py:102-112`），`signed_event` 用 absent-event diagonal shift 和 recursive Laplace determinant expansion 构造 complete-event determinants（`independent_pr70_checker.py:115-151`）。代码在使用前比较全部 8 个 mask 的两套 event polynomials（`independent_pr70_checker.py:300-313`）。Gates 2-17 覆盖全部 8 个比较和 center atom positivity。

**Jet convention：CORRECT.**

`jet` 将多项式系数映射为 `(p,p',p'')`，并对二次项乘以 2（`independent_pr70_checker.py:154-156`）。`events.json` 声明系数为 physical `t` 的 ascending powers。Gates 24-47 比较作者 P2 的全部 literal atom jets。

**合法性与概率：CORRECT.**

代码评估 `K-tau D`、`K`、`K+tau D` 及 complements；计算 leading Sylvester minors；检查每个 minor 的 positivity 和 literal equality（`independent_pr70_checker.py:327-347`）。同时检查三个点的 probability normalization 和 atom positivity。Gates 48-110 覆盖这些检查。

**P3/P2 quotient route：CORRECT.**

Checker 同时用 generic jet product/inverse 规则和显示的 P3 公式计算 `(P^2/r)''`（`independent_pr70_checker.py:349-360`），随后检查 `Phi0`、`Phi1`、`Phi_pair` exact fractions 和 negative literal interval（`independent_pr70_checker.py:363-369`）。Gates 111-123 覆盖此路径。

**P5 side/full/conditional route：CORRECT.**

代码对每个 side/marginal row 分别保留 direct `r log r - r log P` derivative 和 `P*q*log(q)` perspective derivative，并显式记录 `retained_Psecond_term` 与 `retained_rsecond_constant`（`independent_pr70_checker.py:380-397`）。它先检查 side totals，再检查 summed sides 与 full-minus-leaf curvature 的结构恒等式（`independent_pr70_checker.py:400-408`）。Gates 124-158 覆盖这些检查和全部四个 P5 intervals。

**Log intervals：CORRECT.**

Log 代码固定 `NTERMS=80`，将每个正有理 argument 归一化为 `2^k*y` 且 `1<=y<2`，计算 atanh series，并记录 rational nonnegative tail（`independent_pr70_checker.py:218-258`）。区间 scaling 对负系数反转端点（`independent_pr70_checker.py:169-175`），decimal rendering 使用向外 integer floor/ceiling（`independent_pr70_checker.py:177-187`）。Gates 135-174 检查 positive log arguments；P5 和 P6 使用 separate width、sign 和 literal containment gates（`independent_pr70_checker.py:277-288`）。

**P6 Jensen route：CORRECT.**

Checker 从全部 8 个 atom probabilities 计算 complete entropy，然后既用 linear log form 又用 three entropy intervals 组装 midpoint Jensen difference（`independent_pr70_checker.py:419-430`）。Gates 175-178 检查 assembly overlap、width、strict negative sign 和 literal containment。

**执行 wrapper：CORRECT.**

`run_guard.sh` 创建单一 600 秒 deadline，设置单线程数值环境，为 checker 设置 absolute deadline，记录 start/deadline/affinity/PID 文件，在 `timeout` 下启动 arithmetic process，并记录最终 exit（`run_guard.sh:21-54`）。`RUN_LEDGER.json` 记录 `prior_arithmetic_attempts: 0`、`repairs: []` 和 `CLOSED_ON_SUCCESS`。

## 非阻塞限制

- Checker 只是 exact finite-object checker。它不验证 global determinants 或 universal entropy claims。
- Prep manifest 比本公开 review package 更宽。已交付并参与计算的文件与 prep 匹配；但单靠本包无法完整复现 prep manifest，因为 `.gitattributes` 和 machine 顶层 `README.md` 缺席。
- `output_hashes.json` 包含 redacted private invocation 文件名。由于执行证据已由 `RUN_LEDGER.json`、`stdout.log`、`exit.json`、PID 文件和 `environment.json` 提供，这属于 packaging/provenance caveat，不是数学失败。
