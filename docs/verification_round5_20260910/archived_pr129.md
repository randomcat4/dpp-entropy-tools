# PR129 — `t=5/4,Q=0` 的修复单点非阻塞归档

Status: **ACCEPTED_ARCHIVE_ONLY / STOPPED_INCOMPLETE**。冻结头 `d012375e5d1e85498b3304bb56577700d7f3434a`。本归档接受修复后的单点输出、预检和停止边界，不接受整域证书或 trial `PASS`。

## 修复与预检

PR91 残差的正确提取为

`D_Q^2 r1 = D_Q^2 partial_t(B+Lu) - D_Q^2 v + D_Q^2 Lv`，

其中只有第一项取参数一阶，`-v+Lv` 在固定参数取零阶。独立 expression-DAG 符号微分与 interval Jet 在 `r0`、`r1` 的全部六个 Hessian 分量及 `r2` 上一致；高精度有限差分只作诊断，不是证书证据。冻结输入非零、285 项次序一致，形式点的四个权重为正且精确和为一。

## 单点结果

在合法点 `Q=0,t=5/4`，正式精确/外向计算得到 PR91 必要阻塞表达式的点下界

`-0.003330007824007023767653501284027148106155 < 0`。

因此这个点没有提供正的 trial-scheme obstruction；公开状态 `NO_POINT_OBSTRUCTION_FOUND` 只描述这一点和这一检验。负的必要下界不建立全局残差上界，也不证明冻结 PR98 trial 满足整域 gate。没有进行状态域覆盖、参数区间覆盖或第二个点运行。

## 永久排除

旧 attempt-3 把 `Lv` 错误地也对 `t` 微分，并漏掉固定参数的 `-v+Lv` Hessian；其 `RIGOROUS_TRIAL_SCHEME_OBSTRUCTION` 原始输出永久无效，只作为失败来源保留。当前归档不是熵/曲率结论，不是 `[1/2,3/2]` 或单点的证书 `PASS`，也不能替代独立整域证明。

PR129 以 `0a5852415ad0ebcf5a98d9c42fc599905616fd1d` 合入，第二父为精确归档头 `d012375e5d1e85498b3304bb56577700d7f3434a`。S3 的公开边界审阅见 [PR129 评论](https://github.com/randomcat4/dpp-entropy-tools/pull/129#issuecomment-5620607464)。源内权威入口为 [verdict](../../research/C2-issue74-t125-r1-repair-20260910/verdict.md)、[lemma ledger](../../research/C2-issue74-t125-r1-repair-20260910/lemma_ledger.md)和[正式结果](../../research/C2-issue74-t125-r1-repair-20260910/formal/result.json)。
