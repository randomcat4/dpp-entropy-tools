# PR112 — 固定真实熵率的极窄解析区间

Status: **ACCEPTED_SCOPED**，只针对 PR112 的单个作者文件 `explicit_rate_interval.md`，精确 blob `b8aab2981230b61d399d9a9411ee8547f8593958`，位于作者头 `2ea07741114aa7cd20210dfc84becda378381e7b`。S3 先独立完成该单元的解析审阅；S1 随后从作者源与已接受 PR77 输入完成版本绑定 FIRST PR134。两审结论、常数、归一化与排除项一致。没有运行计算，也没有评估新颖性。

## 接受的定理

对物理仿射符号

`f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)`，

令 `h(t)` 为平稳 DPP 的真实完整占据配置 Shannon 熵率，按原始格点归一化。则在精确区间

`J=[1-2^(-27),1+2^(-27)]`

上有

`h''(t)<-1/2000`。

因此 `h(t)+t^2/4000` 在 `J` 上凹，并且对 `u,v in J` 与 `0<=lambda<=1`，

`h(lambda u+(1-lambda)v)-lambda h(u)-(1-lambda)h(v)`

`>=lambda(1-lambda)(u-v)^2/4000`。

## 证明与精确常数

本单元只导入已接受 PR77 的两个输入：同一真实熵率、同一物理仿射参数上的 `h''(1)<-1/1000`，以及 `t=1` 附近完整事件 predictor 比较常数

`rho=2/3, C=288/85, A=11/64, B=49/192`。

在复盘 `|z-1|<=1/8` 上，每个完整占据/空缺事件矩阵有 `7/64` 的严格对角优势，predictor 留在以 `1/2` 为中心、半径小于 `1/4` 的盘内。逐分支因子化保留两种完整事件，给出复总变差增长 `sigma=9/8`。解析 Bregman 界与 predictor 比较的净级数比是

`sigma rho^4=2/9`，

所以条件熵增量级数正常收敛，并在实轴上识别为真实每原坐标熵率。精确界给出 `|h(z)|<5/2`；半径 `1/16` 的 Cauchy 公式于是给出

`|h'''(t)|<=61440`。

在半宽 `2^(-27)` 上，

`61440/2^27=15/32768<1/2000`，

与 PR77 中心锚点合并即得上述严格曲率界。这里的复变量就是物理参数 `t` 的解析延拓，没有平方参数、双层或块归一化替换。

## 排除项与合并边界

本接受明确排除作者已撤回且缺失生产证据的 `[49/40,51/40]`、整个 `[1/2,3/2]`、lifted-cone 包、任何 PR91 输入、PR112 其他文件、宽区间计算证书及其旧 checker。PR112 作者整包仍为 draft/open，未合入 main；证据撤回不构成熵反例。

- 作者精确文件：[PR112 冻结 blob](https://github.com/randomcat4/dpp-entropy-tools/blob/2ea07741114aa7cd20210dfc84becda378381e7b/research/I05-DPP-27-lifted-cone-20260910/explicit_rate_interval.md)。
- S1 FIRST：[冻结范围](../../research/S1-pr112-explicit-rate-interval-first-20260910/frozen_scope.md)、[审阅报告](../../research/S1-pr112-explicit-rate-interval-first-20260910/review_report.md)与[源绑定](../../research/S1-pr112-explicit-rate-interval-first-20260910/source_binding.json)。
- S3 独立窄审：[PR112 评论](https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5618759072)；证据撤回 delta：[后续裁决](https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5620635525)。

FIRST 档案 PR134 以 `8174b5784c5239593236d7f495a55681b182a42d` 合入，第二父为审阅头 `4bf6e3adc940816d3f8b925addb45e1a58f11c99`。接受范围仅以本文为准。
