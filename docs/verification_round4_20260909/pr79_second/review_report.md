# PR79 独立第二审报告

## 总结论

PR79 作为“整区间曲率证书尚未完成前的预算/接口/路线边界稿”是基本正确的；作为整区间曲率证明或数值证书则仍然不成立。

可接受的部分：

- `B_R` 被正确表述为来自 PR77 条件互信息二阶尾项公式的显式共同上界预算，而不是实际尾项值。
- 有限深度条件曲率上界必须与 `B_R` 相加后仍严格小于 0，才能推出真熵率曲率负号；PR79 正确保留了这个逻辑。
- Riccati/hidden-filter 路线没有被误称为有限状态 HMM；作者正确列出连续状态、分支概率、统一收缩或谱隙、参数 jets、测度响应和每格点 `1/2` 因子等缺口。
- RPF/Poisson/CMI 接口保留了完整 Fisher、加速度和测度响应项，没有把 Fisher 负项单独当成曲率符号证明。

不能接受为已证的部分：

- `B_18` 到 `B_24` 的具体小数、`B_20`、`B_21`、`B_22` 的阈值比较和作者 `PASS`，都只是作者来源，未被本轮独立认证。
- 本轮没有新的 C2 数值契约，因此这些预算数值仍是待检。
- PR79 没有给出覆盖 `[1/2,3/2]` 的有限条件曲率外包络，也没有给出 Riccati 不变量集合/收缩/响应证书。
- 整区间命题

```text
h''(t)<0 for every 1/2<=|t|<=3/2
```

仍为 INCOMPLETE。

## 单元状态

| 单元 | 状态 | 判断 |
| --- | --- | --- |
| 绑定与冻结范围 | CORRECT | `input_binding.json:1`-`35` 只绑定 PR79 三个源文件和 PR77 作者源 `proof.md`；重新哈希一致。 |
| `B_R` 公式接口 | CORRECT as interface | `input/RESULT.md:19`-`28` 与 PR77 `pr77_source/proof.md:511`-`538` 的尾项公式一致。 |
| `B_R` 具体数值和阈值 | CRITICAL_GAPS | `input/RESULT.md:29`-`49` 和 `input/tail_budget.py:40`-`55` 只是作者算术声明；本轮禁止重算，且无 C2 原始证据。 |
| 有限深度/真熵率上界逻辑 | CORRECT | `sup h_R'' + B_R < 0` 的证书逻辑正确；预算本身不证明符号。 |
| 正负区间转移 | CORRECT with condition | 若正区间真熵率符号证书完成，物理 gauge/evenness 可转移到负区间；它不能替代正区间证书。 |
| Riccati/filter 路线 | CORRECTLY INCOMPLETE | `input/RESULT.md:51`-`76` 正确承认连续 Schur 状态和缺失桥梁。 |
| RPF/Poisson 响应接口 | CORRECT as source interface | `input/RESULT.md:77`-`92` 与 PR77 `pr77_source/proof.md:381`-`405`、`407`-`538` 一致。 |
| 作者证据打包 | INSUFFICIENT FOR CERTIFICATION | `input/run_record.txt` 是作者 checkpoint；未提供完整机器可核验输出、输出哈希或 C2 执行证据。 |
| 整区间曲率结论 | CRITICAL_GAPS/INCOMPLETE | `input/RESULT.md:117`-`130` 正确保持未完成。 |

## `B_R` 上界预算

PR79 的 `B_R` 定义是源层面正确的。PR77 给出

```text
|d_r''(t)|
 <= [A2+4(r+1)A1+(4(r+1)^2+4(r+1))A0] e_r^2
```

见 `pr77_source/proof.md:511`-`514`，并且

```text
e_r=C0 rho^(2r-6)
```

见 `pr77_source/proof.md:456`-`467`。因此

```text
e_r^2 = C0^2 rho^(4r-12)
```

PR79 在 `input/RESULT.md:19`-`25` 中定义的

```text
B_R = sum_{r>=R} [A2 + 4(r+1)A1 + (4(r+1)^2+4(r+1))A0]
                    * C0^2 * rho^(4r-12)
```

正是 PR77 公式接口的逐项绝对值共同上界。因此，若 PR77 的公式和常数接口成立，则

```text
sum_{r>=R}|d_r''(t)| <= B_R
```

是正确语义。

`tail_budget.py` 的结构也与这个公式匹配：`er2_prefactor` 写成多项式因子乘 `C0*C0*rho**(-12)`，再用 `q=rho**4` 汇总几何级数，见 `input/tail_budget.py:14`-`37`。我没有运行或重算这些有理数。

## 有限深度上界逻辑

PR79 对有限深度和真熵率的关系表述正确。PR77 的接口是

```text
h''(t)=h_R''(t)-sum_{r>=R}d_r''(t)
```

见 `pr77_source/proof.md:517`-`523`。因此，如果某个参数 cell 上有经过外包络认证的有限条件曲率上界

```text
h_R''(t) <= U_R(J)
```

且已验证

```text
U_R(J)+B_R < 0,
```

则可推出该 cell 上真熵率曲率严格为负。`input/RESULT.md:49` 正确指出，`B_R` 的下界不是实际尾项的下界；它只能说明这个特定粗上界对某个有限 margin 可能太粗，不能推出最小必要深度，也不能排除更强有限上界或更锐尾界。

这点在 `input/RESULT.md:117`-`122` 的 “Next exact gate” 中也写清楚了：必须给出覆盖 `[1/2,3/2]` 的 `h_R''(J)` 外包络并与已验证上界预算相加，或者给出更锐的 Riccati 总误差证书。

## 正区间与负区间

PR79 正确把预算讨论限于正区间 `t in [1/2,3/2]`，见 `input/RESULT.md:27`。对负区间的转移只能在正区间证书完成后，使用物理 gauge/evenness 转移。

该 evenness 对固定符号是合理的：最近邻系数随 `t` 变号，而对角和次近邻不变，可由交替符号对角共轭把 `K_t` 变到 `K_{-t}`；完整事件行列式在这种 gauge 下不变，所以熵率为偶函数。这个转移不提供正区间证书本身。

## Riccati/hidden-filter 路线

PR79 对 Riccati 路线的状态判断是正确的。`input/RESULT.md:53`-`67` 明确说，两点分组后的 Schur 更新

```text
F_{alpha,t}(S)=D_alpha(t)-E(t)S^{-1}E(t)^T
```

不是有限状态 HMM。状态 `S` 位于连续可达集合；不能直接套用有限状态 HMM 的 Blackwell 或 Han-Marcus 理论来得到曲率响应。

作者列出的五个缺口也是必要的：

1. 四个分支共同不变的可达集合；
2. 分支权重确为完整两点条件概率，并满足正性/归一化；
3. 在固定范数或度量中对所有 `t in [1/2,3/2]` 有统一收缩或谱隙；
4. 一阶、二阶参数 jets 和不变测度响应；
5. 每两点 cell 熵率转换为每原始格点熵率的 `1/2` 因子。

`input/RESULT.md:69`-`76` 还正确指出，PR77 的逐项 inverse-decay 常数不能自动变成足够锐的全局矩阵范数收缩常数。缺少明确不变量 box/cone 或其他 metric 时，Riccati 路线不能产出证书。

## RPF/Poisson 和 CMI 接口

PR79 对 PR77 RPF/Poisson 接口的转述是正确的。PR77 源中

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v))
```

见 `pr77_source/proof.md:381`-`386`。随后 PR77 明确说明第二、第三项包含完整条件加速度和不变测度响应，不能由 Fisher 负项单独定号，见 `pr77_source/proof.md:389`-`405`。

PR79 在 `input/RESULT.md:79`-`92` 保留了同一完整响应式，并把 CMI 尾项桥梁作为另一条结构不同的桥梁。这是正确的接口描述。它没有删除 Fisher、加速度、测度响应，也没有把有限 hidden state 当作前提。

需要注意的是，`input/RESULT.md:77` 的 “PROVED INTERFACE” 只能理解为作者源层面的接口已经写出；它不是对 PR77 常数、PR77 数值证书或 PR79 整区间结论的独立接受。

## 证据打包

PR79 的证据打包不足以独立接受任何具体预算数值。`input/run_record.txt:1`-`17` 只是作者运行记录，明确说这是 author run/checkpoint，不是独立 review 或 C2 execution。

`tail_budget.py` 使用标准库 `Fraction`，静态结构适合精确有理预算；但它没有冻结机器可核验的完整输出文件，没有输出哈希，也没有把完整有理分子/分母纳入绑定。`run_record.txt:17` 说精确有理数可由脚本重建；这对作者 checkpoint 足够，但对外部接受仍不够。由于本任务禁止运行脚本，这些数值保持待检。

## 剩余缺口

PR79 没有闭合以下缺口：

- 没有独立验证 `B_R` 的具体数值或阈值比较；
- 没有给出覆盖 `[1/2,3/2]` 的有限深度条件曲率外包络；
- 没有给出 Riccati 连续状态的严格不变量集合、统一收缩/谱隙、参数 jets 和测度响应；
- 没有把 PR77 中点 gap、三点曲率或 Fisher 下界升级为整区间符号；
- 没有给出形式化证明。

因此，PR79 当前可接受范围是：一个正确限定的预算/接口/失败账说明稿。它不是 whole-interval curvature 证明。

