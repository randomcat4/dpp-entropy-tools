# PR79 静态代码与证据打包审核

## 方法

本轮只静态读取：

- `input/tail_budget.py`
- `input/run_record.txt`
- `input/RESULT.md`
- `pr77_source/proof.md`
- `input_binding.json`

未运行 `tail_budget.py`，未重算几何级数、阈值比较、熵、行列式或对数。

## `tail_budget.py` 静态审核

状态：公式结构可接受；数值输出待检。

脚本使用 `fractions.Fraction`，没有第三方依赖。它定义的常数：

- `rho = 49/64`
- `C0 = 1033420800/1263214441`
- `M2, M3, M4`
- `U1, U2`
- `A0, A1, A2`

见 `input/tail_budget.py:1`-`14`，对应 PR77 `pr77_source/proof.md:456`-`497` 中的 CMI 尾项常数。

核心函数：

```text
er2_prefactor(r)
tail(R)
```

见 `input/tail_budget.py:17`-`37`。结构上，它把

```text
e_r^2 = C0^2 rho^(4r-12)
```

写成

```text
C0^2 rho^(-12) (rho^4)^r
```

再把二次多项式乘几何尾和求和。这个结构与 PR77 的 (8.14)--(8.16) 接口一致。

脚本底部打印 `R=18` 到 `24` 的预算并断言四个阈值比较：

```text
tail(20) > 1/2500
tail(21) < 1/2500
tail(21) > 1/5000
tail(22) < 1/10000
```

见 `input/tail_budget.py:40`-`55`。这些断言即使运行通过，也只是尾预算比较，不是曲率证书；脚本注释在 `input/tail_budget.py:48`-`50` 已正确说明有限条件曲率外包络仍然需要另行提供。

## `run_record.txt` 审核

状态：作者 checkpoint，不是独立证据。

`input/run_record.txt:1`-`15` 记录命令和期望输出。`input/run_record.txt:17` 明确说这是 author run/checkpoint，不是 independent review 或 C2 execution。

证据打包不足点：

- 没有冻结完整 stdout；
- 没有给出所有精确有理分子/分母；
- 没有输出文件哈希；
- 没有 C2 独立执行记录；
- 没有把预算数值和阈值比较转成绑定的机器可核验 artifact。

因此，`PASS` 不能被本轮接受为算术证书。

## 与 `RESULT.md` 的一致性

`RESULT.md` 对脚本作用的说明是准确的。它说脚本“sums this explicit majorant; it does not compute the actual absolute curvature tail”，见 `input/RESULT.md:27`。这与脚本只对 PR77 上界多项式求和的行为一致。

`RESULT.md:40`-`49` 对阈值比较的解释也正确：这些比较只能说明某个共同上界预算对给定有限 margin 是否足够，不能给出最小必要深度，也不能单独推出有限或真曲率符号。

## 未发现的代码层面错误

在静态阅读范围内，我没有发现 `tail_budget.py` 把 PR77 公式接口写错、把预算误写成实际尾项、或把阈值断言误称为曲率证书的问题。

主要问题不是代码公式，而是证据地位：没有独立执行、没有完整绑定输出、没有 C2 原始证据。

## 最小修复建议

若 PR79 要把预算数值推进到可外部接受，应提供：

1. 完整机器生成输出，包含每个 `B_R` 的精确有理数；
2. 输出文件的 SHA256 和生成命令；
3. 明确的 C2 独立执行/复核 artifact；
4. 与每个参数 cell 的有限条件曲率外包络相结合的最终不等式，例如 `sup h_R''(J)+B_R<0`。

在这些材料出现前，PR79 的预算脚本只能作为作者公式实现和待检 checkpoint。

