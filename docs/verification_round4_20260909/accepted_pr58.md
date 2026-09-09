# PR58：完整事件补偿、双边投影与两个有限见证

状态：**ACCEPTED_SCOPED**。最终作者头 `89aa874c24dd5a3ea98f8474826392560b1d0397` 的原始解析、原始有限、新增解析及修订有限单元分别完成 C1 FIRST 与隔离 C3 SECOND，合并提交 `e158da11499436f9696ffd740e41ce804faf3f12`。

## 一般解析单元

固定严格实对称内部块 A,C 和秩二交叉块 B，沿真实仿射核 `K(t)=[[A,tB],[tB^T,C]]`。对全部完整事件 `(S,T)`，令参考律 `mu=p_A tensor p_C`、`s=t^2`、`q_s=P_s/mu=1-sa+s^2b>0`、`u=q_s-1`、`y=s^2b`。此处 P_s 为完整事件律，下式标量 P 与它不同。

```text
Phi(u)=4u²/q+2u log q, psi(u)=8u/q+10 log q,
P=E_mu Phi(u), A2=4 E_mu[y²/q], R0=E_mu[q psi²],
I(t)=H(A)+H(C)-H(K(t)),
t² I''=P+A2+E_mu[y psi]=P+A2+s²W,
W=E_mu[b psi].
```

接受完整 Cauchy 补偿界 `t² I''>=P+A2-(1/2)sqrt(A2 R0)`。它是可容许 W<0 的充分条件；不主张 W>=0 蕴涵此判据。系数 1/2、Fisher 与加速度、全部稀有事件均保留。

区间版本也接受：若 `0<L<=s<=R`、`0<q_-<=q_s<=q_+`、`|psi|<=Psi`、`E_mu[u²]>=M2>0`，且 `B2=E_mu[b²]`，则

```text
t² I'' >= 4M2/q_+ - R² Psi sqrt(B2 q_+/q_-).
```

右侧为正可由正左边与精确有理平方不等式认证；使用 A2 上界只发生在负平方根项内，之后才舍去正 A2。

固定两边完整边缘给出每条条件纤维的 a,b 消去。把 psi 分别减去其真实条件均值，得到预算 R_S、R_T，界中可用 `R_*=min(R0,R_S,R_T)` 代替 R0。进一步令

```text
Radd=inf_(f,g) E_(P_s)[(psi-f(S)-g(T))²],
t² I'' >= P+A2-(1/2)sqrt(A2 Radd).
```

`y/q` 在 L²(P_s) 中与全部加性函数正交，因此双边判据不弱于各单边判据。均值去除后，在 `U=L²_0(p_A)`、`V=L²_0(p_C)` 中令 `K:V->U` 为条件期望；全支持保证其范数严格小于 1。固定零均值规范的正规方程 `f+Kg=m, g+K*f=n`、`I-KK*` 逆与残差公式成立。实秩二似然的三个对称 Gram 坐标及行列式坐标给出 `rank K<=4`，没有旋转观测基。

任意行和、列和均为零的表 c 满足抽象对偶界 `Radd>=(sum c psi)²/(sum c²/P_s)`。这只是最佳加性残差的下界。Erbar–Maas 的可逆链/运输测地线条件不会自动变成这里的物理径向轨迹或所需二阶熵耗散不等式；非可逆/隐状态方案的剩余桥接保持开放。

## 原始固定 3+3 区间与 s=10 见证

对象精确限定为 [RESULT.md 第4节的 A,C,U,V](../../research/I05-23-middle-20260909/RESULT.md)，B=UV^T；两侧相关、交叉块稠密秩二、非坐标情形。独立 PR72 从这些有理矩阵重建完整 64 个六维事件多项式，检查全部主/补主 Möbius 恒等式、全局与双侧纤维消去、精确顶点和端点极值。四个区间 `[3,9]`、`[8,12]`、`[11,14]`、`[14,15]` 覆盖 `3<=s<=15`，所有严格平方补偿余量和 27 个作者有理比较均通过。因此该固定核线在 `3<=t²<=15` 严格负熵曲率。

同一固定对象在 s=10 有 `W(10)=E_mu[b psi]<0`，而完整量

```text
t² I'' > 0.17037745196806863130550498470533808479721333392335 > 0.
```

N=80 有理 atanh 对数尾界保留全部 64 事件、5120 项。W 区间宽小于 `5.83e-83`，完整曲率宽小于 `8.71e-79`。RESULT (5.1) 的长小数已明确改为负的精确有理上端点的近似显示；严格符号由有理端点决定。这否定 W 的全称非负充分条件，未给出熵凹性反例。

PR72 `e557d93e864582c9f9e7bd4384ed21d6ae2f66e2` 的执行源码 `86617882b7db97f5db39bf613d876a5d5bcf9107` 未变。唯一运行 16:09:13–16:09:18 UTC，按秒级标记约5秒，exit0，PID 已退出；原2700秒截止16:54:13未改。未声称拥有更细时间测量，没有失败或重跑。

## 新增 s=9/10 双边投影不足见证

对象精确限定为 [joint addendum 第3节的新 A,C,U,V 和8×8表](../../research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md)，s=9/10；两轴子集 mask 顺序均为0..7。以下修订范围已通过相应 FIRST 与隔离 SECOND：

```text
Radd > 192.45644754663817,
T=4(P+A2)²/A2 < 166.441251953051541,
W(9/10)<0,
t² I'' > 4.653598245398841 > 0.
```

Radd 的严格下界超过使补偿下界为正所必需的阈值 T，因此即使最优双边加性补偿判据也不是必要条件；同点真实熵曲率仍负。

独立 PR76 的原运行冻结于 `bbc9bc19b915ebad0ea8e8bea00580d4eebc5246`，最终证据头 `a7979c33b6e82431b6ddf1d39ac69e254d7b655a`。原文阈值 `T<166.44125195305153` 被既有有理包络 `[166.441251953051540106785812,166.441251953051540106785813]` 严格否定；首错状态 **STOPPED_FIRST_EXACT_MISMATCH** 永久保留。

C3 的原计算请求还误把 `V=E_mu[y psi]` 命名为 W；更正在启动后到达。原输出名 W 实际为 V，不能据此否定作者 W 的小数。当前文字撤掉未认证的作者 W 小数，只从现存 V<0 与 `V=s²W` 推出 W<0；阈值换成由既有包络支持的较粗严格上界。完整曲率也用原有直接求导包络支持。没有重新运行、篡改原程序/输出或宣称出现新的全字面界 MACHINE_PASS。

运行16:21:24–16:22:48 UTC，秒级标记84秒，exit20；PID在16:24:10确认消失，原600秒截止16:31:24未改。零基础设施失败、修复、重跑或精度第二轮。输入新增 REQUEST_CORRECTION.md 仅为运行后的说明，不是当时执行输入。

## 版本与独立性边界

作者版本链：原始 `1770ed29e8487b8f39aebb4c9466406c7493e580`；增加joint三文件 `a4f05cc962985015b71635bf633acce9dfe76866`；充分条件排序两句 `7d3dd405faea365e3ddcfd8c1b6f38ae47e34387`；算子定义域一符号 `5ab3cae1c49da8334057596f46a4bd8fc449b98c`；近似小数/表次序两句 `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`；最后joint文字修复 `89aa874c24dd5a3ea98f8474826392560b1d0397`。每项修订单独绑定；原先缺口与失败保留。

原始解析 SECOND 与新增 joint SECOND 使用不同隔离上下文；各自有限后续审查只获得原始 C2 计算者源码/输入/输出/执行记录，没有 FIRST、其他 SECOND 的材料或结论。C2 是独立计算责任人，不是数学 FIRST。C3没有执行新算术。

一般相关稠密秩二全合法弦、甚至上述固定例的整个合法弦，仍未解决。issue63的长计算未运行。有限配置熵结论不提升成真实熵率结论；一般实核凹性、熵反例、新颖性与形式化均不在范围内。

## 审查与来源记录

- [C1 FIRST 档案](../../research/C1-verification-round5-20260909/units/pr58/review_report.md)及各后续闭合：[原始区间](../../research/C1-verification-round5-20260909/units/pr58/corridor_review_report.md)、[新增解析](../../research/C1-verification-round5-20260909/units/pr58/delta_review_report.md)、[原始新增有限缺口](../../research/C1-verification-round5-20260909/units/pr58/additive_machine_review.md)、[最终文字修复](../../research/C1-verification-round5-20260909/units/pr58/bounds_repair_review.md)。
- 原始 SECOND：[冻结范围](pr58_second/frozen_scope.md)、[解析完整报告](pr58_second/review_report.md)、[比较措辞闭合](pr58_second/wording_closure.md)、[有限范围](pr58_second/corridor_scope.md)、[完整有限报告](pr58_second/corridor_review_report.md)、[小数呈现闭合](pr58_second/decimal_display_closure.md)、[有限来源绑定](pr58_second/corridor_source_binding.json)、[副本映射](pr58_second/publication_mapping.json)。
- 新增隔离 SECOND：[解析完整报告](pr58_joint_second/review_report.md)、[表次序闭合](pr58_joint_second/table_order_closure.md)、[有限范围](pr58_joint_second/machine_scope.md)、[有限完整报告](pr58_joint_second/machine_review_report.md)、[有限来源及补丁绑定](pr58_joint_second/machine_source_binding.json)、[副本映射](pr58_joint_second/publication_mapping.json)。
- [六个作者版本的完整哈希与差异绑定](pr58_source_delta.json)。程序与原始输出未被文字修复改动；原 W 小数未认证而撤下，不把请求引起的比较错误记作作者错误。
- 原始 [PR72 机器记录](../../research/C2/pr58_corridor50/machine_notes.md)与 [PR76 首错/请求更正记录](../../research/C2/pr58_additive52/machine_notes.md)已分别归档。两者均为独立计算者的证据，再由数学 FIRST/SECOND 审查其用途；后者终态仍为停止于首错。

C3 完整读取各报告、核对原始区间25文件与新增有限28文件的哈希及两个修订补丁，未执行行列式、对数或熵计算。两次独立机器合同均为单进程/CPU/线程、16 GiB、无 GPU。独立审阅、有限运行、来源/链接检查和 CI/形式化是不同证据层，不能互相替代。
