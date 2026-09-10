# 开放 PR 收束矩阵

Status: **FINAL_SCOPED**。精确 head 均为处置时冻结对象；`ACCEPTED_SCOPED` 只接受“范围”列明的对象。

## 初始 18 个开放 PR

| PR | 精确 head | 最终核验与实际复现 | 公共处置 |
|---:|---|---|---|
| 66 | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | 原 Dobrushin A1/A2 导入存在承重适用性缺口；同一 `p>4` 结论由已接受 PR82 的 DPP-specific finite-response 路线重证。旧来源失败与新证明分开。 | **CLOSED_UNMERGED / SUPERSEDED_INVALID_ROUTE** |
| 86 | `bd12e6094e098499fae7e01729a4b29f021a14e2` | 完整 atom、角度排除、fixed-pair dilute theorem 解析复核通过；PR97/S2 新跑 4096 boxes，最小界 `0.012067200390564330`。 | **MERGED / ACCEPTED_SCOPED**, merge `8d3ed312b941df7b6fa568c0eb515b3733d464b8` |
| 90 | `5b32943874e0633f87fa67e7150b01e134a1581e` | C1 对 PR79--82、86、88、91 的历史 FIRST 档案；作为审阅来源保留，不把其中作者输出自动升级。 | **MERGED / VERIFIED_REVIEW**, merge `2e781b0b223f7cac247c07be2e3ae29587158ef8` |
| 94 | `a9db9f98dc6dac766dd9b214f056ee9b30109b23` | channel/mode 解析 FIRST+SECOND；S2 独立重建 16 identities、两个 64-event laws、3+3 matrices、endpoint、fiber、Fisher 与 `337/202500`。`WHOLE_CHORD.md` 被 PR95 覆盖，不重复计入。 | **MERGED / ACCEPTED_SCOPED**, merge `0c1d65518f18aadd0eaf15daeea5d2038b2938d9` |
| 97 | `03e0313a5802bfe52fba18fa01bf5ad97ab20d2f` | wedge、strong whole chord、strength family 的解析链通过；fresh exact runs 给出 `H''<-4/5` 与 family `H''<-1/2`。 | **MERGED / ACCEPTED_SCOPED**, merge `6e9fa0bc5735f0bf6fce0df8cb63620d0d4b7e3a` |
| 98 | `55649309437a78d9e5174386d8d260a4ee9c02a1` | 三份对象 exact Decimal parse/write/parse 通过；原 ZIP 不在独立输入中，未核 byte equality，未重跑 scout，无数学证书。 | **MERGED / ARCHIVE_ONLY / NON_CERTIFYING**, merge `134e3c5b538c1a251c6ee8b81632c60ecf3816e1`；排除于 clean import |
| 100 | `3a039fdc17ac812693b23b563eed0b30343b9a9a` | PR94 channel/mode 数学 FIRST；显式有限门由 PR143 后补闭合。 | **MERGED / VERIFIED_REVIEW**, merge `9447add445e5a6f523b03595c9f8279fdd0f6ca2` |
| 104 | `d980dbb04840bd21e6c62cf88ffd45a9b0d1b4f8` | common-diagonal sufficient criterion 与 double-boundary wedge 解析通过；独立 168-event jets、`K`/`I-K`、正负 gap 和六个 Sylvester minors 全通过。 | **MERGED / ACCEPTED_SCOPED**, merge `ce61845b601fb67b9b4c532aa3e2a7339e321f86` |
| 106 | `a175bf1d1b5a8c16537aa4924731de426dfc882d` | `p>=1` 局部凹性由 PR117 覆盖；独立的 `p>=1/2` 中心 Fisher 四次展开和 exact-score moment route obstruction 通过。后者不是熵反例。 | **MERGED / ACCEPTED_SCOPED_PLUS_SUPERSEDED**, merge `32734c742069e7756cf505a398d2bb7002984569` |
| 110 | `142420531ed7a41d1abc4c8040c6485bf21b1bc7` | 定理严格包含于已接受 PR117；来源条件抽查未见矛盾，不重复导入。 | **CLOSED_UNMERGED / SUPERSEDED** |
| 112 | `2ea07741114aa7cd20210dfc84becda378381e7b` | 旧 wide certificate 的 production source/output 缺失且旧 checker 有 recurrence sign/order failure；PR136 新路线不追认旧 provenance。`lifted_cone` §§1--5 仅作方法 lemma；§6 独立 exact reconstruction 通过。`entropy_shape.md` 有 `a,c` 标签对调，Gamma 仍未解。 | **CLOSED_UNMERGED / MIXED** |
| 115 | `dd52c147efc4a0908b8e9545628f031d1be97027` | 未完成 Poisson/Neumann 路线及作者 `n=6,7,8` signs 不提升；被 PR136 新证明覆盖。 | **CLOSED_UNMERGED / SUPERSEDED** |
| 116 | `3f276c09fe4da3aded2ab6cf457adb7fdc4254d8` | 特殊 whole chord、moments、endpoint phase、Fisher pole、uniform endpoint band、joint identities、lossless label reduction 解析通过；light/moments/负 `R`/负 acceleration 独立 finite 通过。冻结 endpoint checker 自身失败但公式独立通过。Bernstein box **REPRODUCTION_RESUMED / UNVERIFIED**；compact middle 未解。 | **MERGED / ACCEPTED_SCOPED_WITH_EXCLUSIONS**, merge `0360b0bd744ec9a3d05ef7699da6d56e22e185b0` |
| 120 | `83b89e8b9b4c542e5d1cd8b38b64b7ff2449ad41` | compact unequal-strength middle 解析链通过；fresh 1024-box run 最小 exact scaled Gershgorin margin 约 `0.11829569483797094`。equal-strength 与 obstruction 被 PR124 覆盖，不重复导入。 | **MERGED / ACCEPTED_SCOPED**, merge `7353c2e048754914379076d545cd6ffe0f80f285` |
| 124 | `344723af6affab240c9f87c395d4e8c1b7b19f6d` | pointwise resolvent obstruction、equal-strength half-leaf、punctured small-edge theorem经分单元 FIRST 与独立 SECOND 通过；obstruction 不是熵反例。 | **MERGED / ACCEPTED_SCOPED**, merge `3729264b95208a92accd08a01a9b37ce41bb17f0` |
| 130 | `4cae5c29effcf01b1fadc7452780b73a58ec94e7` | 严格 `L^infinity` 奇偶中心真实完整配置熵亏损 `Theta(t^4)`，FIRST 与 pre-FIRST SECOND 一致。 | **MERGED / ACCEPTED_SCOPED**, merge `b53bc5da672e6d16c4f4759fd136e6c6561e49a6` |
| 132 | `6370ca1ae64cfc9e58c491568445f02fadcf0a71` | PR124 正向解析单元 FIRST 与 PR120/124 source correspondence；不自行提升作者有限输出。 | **MERGED / VERIFIED_REVIEW**, merge `fae8fc0b3ff07c7597a62cc7267ae9742c78b9a3` |
| 136 | `39098dac760cea2d27f2955bed31f80c87913810` | 真 entropy rate 在完整 `[1/2,3/2]` 上 `h''<-1/3000`；解析 FIRST+SECOND。S2 本地隔离 GCC、2 CPU 完整 128-node fresh run 与独立 Fraction/DCT 审计通过，输出 SHA-256 `9F35777945F45EF205DD8B1297F3126DC1902F064163D680C87BE9E0709508F4`。 | **MERGED / ACCEPTED_SCOPED**, merge `f1c8b9a28dc6bb3abbfc8d69e3332c0550d8703d` |

## 本轮新建审阅/复现 PR

| PR | 精确 head | 内容 | 公共处置 |
|---:|---|---|---|
| 137 | `cd21363236534bc34ab328a3114631a5d4164d36` | PR136 解析 FIRST 与证书接口 | merged `30816208df095ab7ffb881a13aa32932d324efcf` |
| 138 | `d280112aa49f4ee67df868a1692bab28b892b2e7` | PR130 数学 FIRST | merged `a8cb76a67bc07c1ff9534a4f9edc0b9fd7989aa2` |
| 139 | `6069e0a30c82bc4cb4044ed0d01af55650a062bd` | PR136 独立完整有限生产与审计 | merged `ddec1559a420ed4765e47ab056ebdb20c75f8f12` |
| 140 | `313129680362565824a1388e6b7156b019cae746` | S1 backlog 精确头处置 | merged `eba2c1d37d64886242faea52e9ec954201f0aced` |
| 141 | `6900cff4924ef5aabc6b808f3d03db2a8fad5596` | PR106 exact score-moment obstruction addendum | merged `917be9e6daced79410e26298d8c490d7a0ea3a89` |
| 142 | `cb0ba417a612dcebb3adf84fe9cf4800814631d0` | PR116 解析 FIRST，精确列出 finite gates | merged `982a7e80fe0ed19d120f619fcf3fa060915423ce` |
| 143 | `e7ced4a02737ae34d76bb46f657fd2c52501faa6` | 其余 finite backlog 的独立复现、失败账本和 source bindings | merged `c81202c8473f1f266111f0123e1228cd34f8491e` |

## 未闭合而不导入的研究边界

- PR116 的 acceleration-only Bernstein `R>0` box 正在无限时长策略下继续重建；当前没有 verified certificate。
- PR116 自然二参数族的完整 compact-middle `Gamma` 符号、一般 moving-rank-two concavity、一般真实核结论均未闭合。
- 没有真实 Shannon 熵反例；所有 negative acceleration、negative conditional fiber、mixture bridge 均只作为方法障碍。
- 没有进行 novelty、priority 或 formal verification 认定。
