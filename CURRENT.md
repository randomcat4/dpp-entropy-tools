# 当前节点

核对日期：2026-10-03。公共主线基准为 `237097124869b3bb04c139d4c4599e6bda7d344d`；本页只重组现有公开证据，不新增证明认证。

本库的已审基线是 9 月 11 日的收束轮，而非旧首页的 9 月 9 日快照。一般实对称核的完整配置 Shannon 熵凹性、一般固定标量平稳符号的真实熵率凹性仍未由这份主线关闭；复核五点反例、实核问题及平稳率问题必须分别判断。

## 先读

1. [最终收束范围](docs/verification_round6_20260911.md)：完整事件、解析双审、独立有限复现和未闭合门。
2. [逐 PR 固定头与处置](docs/verification_round6_20260911/closeout_matrix.md)：尤其 PR116 的 compact middle 排除项及 PR136 的固定双谐波真率结论。
3. [逐文件准入表](docs/verification_round6_20260911/verified_import_whitelist_round6.json)：不得用作者包整体代替已审范围。

可复用基线包括：严格 A0 奇偶中心局部熵率理论、严格 L-infinity 中心差商与四次熵亏损、固定双谐波 `[1/2,3/2]` 真率曲率证书，以及限定三点/秩二/端点结论。各项前提和排除范围以收束矩阵及所链接复核为准，不能合成一般定理。

## 当前候选

| 入口 | 当前可读对象 | 尚缺什么 |
|---|---|---|
| [PR146](https://github.com/randomcat4/dpp-entropy-tools/pull/146)，`b4485a6c83cccff96dc8ef74187a1c56098d0a27` | 固定可测频率集的中心 Fisher 密度和稀疏密度真率 chord；自含作者证明 | 独立全审；体积一致 acceleration 控制。Fisher 密度不等于 Shannon 曲率 |
| [PR147](https://github.com/randomcat4/dpp-entropy-tools/pull/147)，`4ae748ae7c9cdf5580e94e4460db44c1dadd1eaf` | natural exchangeable 3+3 的 sharp joint-kernel 候选与 60 个精确有限样本 | 可读且绑定的四区域连续域证书、独立全审。有限样本不闭合全域 |

选择器有限一致性是独立小理论项目。其公开移交原件 [PR148](https://github.com/randomcat4/dpp-entropy-tools/pull/148) 明确总体 `OPEN / INCOMPLETE`，后续入口为 [RL01 PR123](https://github.com/cat5779/rl01/pull/123)。固定 P 的 pairwise 修复与固定块界不能冒充变化 P 的统一 Lipschitz selector；固定 `13/12` 不相容比也不是发散反例。

其余旧路线、失败来源和过时但正确的子结果从 [ARCHIVE](ARCHIVE.md) 访问。当前候选未经独立审查，不因本次导航整理升级。
