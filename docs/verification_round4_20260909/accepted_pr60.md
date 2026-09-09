# PR60：全零约束缺边族与逐中心延拓的限定范围

状态：**ACCEPTED_SCOPED**。作者冻结头 `f869fd251c0d6fdad737b6d5efa287307795a87d` 的五个单元分别通过 C1 FIRST 与隔离 C3 SECOND，以 `ccdc63d3c16bbf7e09b20261b4b60242ba3ae010` 合入。下列范围不能由合并动作扩大。

## 主定理与全参数域

对象为严格连通实三点缺边核

```text
K = [[x,0,b0],[0,y,c0],[b0,c0,z]],  b0*c0 != 0,
A = b0^2/[x(1-x)], B = c0^2/[y(1-y)],
z = 1/2 - [A(2x-1)+B(2y-1)]/2,
0<x,y<1, A>0, B>0, A+B<1.
```

这正是文稿的严格 `Lambda=0` 缺边族，包含不等对角和任意非零边强比。边的负号用观测坐标中的对角符号共轭恢复，不能以一般谱旋转替代观察基。

令 `a=(1+r)/2`、`b=(1-r)/2`、`x=(1+mu)/2`、`y=(1+nu)/2`，取 `|mu|,|nu|,|r|<1`、`0<u<1`；作者参数化为 `A=u^2 a`、`B=u^2 b`。对每个固定非零实对称物理方向 D，完整八事件自然对数 Shannon 熵满足 `H''(K;D)<0`。更强地，沿指定零约束中心路径、固定物理方向坐标得到的 `M=d[-H'']/du` 正定。这里的熵方向导数始终取实际仿射线 `K+epsilon D`，不能把非线性 u 路径当成该方向。

全域证明依次保留全部事件、Fisher 与加速度，经已接受的 2+4 Schur 归约、长短矩阵 `Rbar=(u/4)Rstar`、`t=u^4`、完整行列式证书、正种子与惯性延拓，再沿固定 D 积分。证明不借用 PR57 的 r=0 正性。

## 条件熵与逐中心非零约束带

同一零约束族上，`C(K)=H(X3|X1,X2)` 在所有非零实对称六方向也严格负曲率。叶边缘的负 Hessian 在固定方向下恒为 `D11^2/[x(1-x)]+D22^2/[y(1-y)]`，所以扣除它不改变 M；零点初值与正 M 的积分给出条件结论。

固定任一上述中心 K0，令 T0 为 `-C''(K0)` 在 Frobenius 正交归一的六方向基中的矩阵，并置

```text
q0=(1-A-B)/2, pstar=min_S p_S(K0),
alpha=det(T0)/(tr T0)^5, m=pstar/2,
L=8*(10/m+3/m^2+log(1/m)),
rho=min(q0/2,pstar/2,alpha/(2L)).
```

在 `|delta|<=rho` 上，核 `K0+delta E33` 严格合法，且每个实对称 D 满足

```text
-C'' >= (alpha/2)||D||F^2,
-H3'' >= (alpha/2)||D||F^2 + D11^2/[x(1-x)] + D22^2/[y(1-y)].
```

每个非零 delta 都有 `Lambda!=0`。半径由该中心的完整事件和导数显式定义，但依赖中心，没有统一正宽度或已执行的数值半径证书。

## 有限算术与方法边界

完整全 r 证书使用独立构造的四事件分数/Gram、16 个长短矩阵恒等式、16 个多项式矩阵条目、两种精确行列式及零余数商 P，再构造完整 Q 系数盒。P 有 279 个整数项、次数 `(4,4,10,6)`；Q 的全部 1925 个位置含 1731 正项、194 零项，最小正系数 192、常数项 432。正图表使用 `X,Y,T>0,R>=0`，负 r 通过完整叶交换矩阵共轭覆盖。中间 Bareiss 枢轴只用于多项式精确除法，不作为每个参数点均非零的前提；行列式正本身也不能替代正种子与惯性步骤。

固定辅助见证另外取

```text
K*=[[11/100,0,33/500],[0,1/200,3/1000],[33/500,3/1000,199/200]],
D*=[[0,-1,0],[-1,-1/50,2/25],[0,2/25,0]],
C*=K*-diag(K*), h=1/100000.
```

它检查固定对角、仅缩放已有边的径向负 Hessian 导数为负，同时真实 `-H''>0` 且三核 Jensen 差为负。这仅阻断该辅助单调性路线，不是熵凹性反例，不反驳指定零约束路径的 M 定理。该见证的审查与全 r 证书分开。

单侧 perspective 桥接受的是 `-C(K)=G1(K)+G1(I-K)`、完整单侧二阶恒等式和第三坐标缩放律。剩余耦合不等式 `F1(D)>=2 tr(N1 adj D)` 仍未证明。

任意离开已覆盖域的长弦、一般非零约束缺边核、一般实三点全域、零边轴或奇异端点的严格 Hessian、有限/无限体积熵率、熵反例、新颖性和全量形式化均不由这些单元解决。

## 双审、独立算术及版本记录

- C1 FIRST：[原始逐单元报告](https://github.com/randomcat4/dpp-entropy-tools/blob/972646e03be0062a233ae2c434ad1bff3e520913/research/C1-verification-round5-20260909/units/pr60/review_report.md)、[全 r 机器证据闭合](https://github.com/randomcat4/dpp-entropy-tools/blob/972646e03be0062a233ae2c434ad1bff3e520913/research/C1-verification-round5-20260909/units/pr60/machine_review_report.md)、[独立辅助见证闭合](https://github.com/randomcat4/dpp-entropy-tools/blob/972646e03be0062a233ae2c434ad1bff3e520913/research/C1-verification-round5-20260909/units/pr60/aux_review_report.md)。
- C3 SECOND：[原始冻结范围](pr60_second/frozen_scope.md)、[原始报告](pr60_second/review_report.md)、[全 r 缺口闭合](pr60_second/machine_evidence_closure.md)、[全 r 接受范围](pr60_second/machine_scope.md)、[辅助范围](pr60_second/auxiliary_scope.md)、[辅助完整报告](pr60_second/auxiliary_review_report.md)。最初 author-only 包缺少原始证书而得到 INCOMPLETE 的历史保持不变；后来提供的是 C2 独立计算者的原始源码和分数包，未提供 FIRST 报告、代码、输出或结论。
- [原始来源绑定](pr60_second/source_binding.json)、[全 r 增补绑定](pr60_second/source_binding_addendum.json)、[辅助绑定](pr60_second/auxiliary_source_binding.json)、[公开副本映射](pr60_second/publication_mapping.json)。C3 仅做源码、原始证据、哈希与结构检查，没有重新计算熵或行列式。
- 独立全 r [PR64 证据](../../research/C2/pr60_independent52/FINAL_HANDOFF.md)冻结于 `5b40617fe7172aa266614aa28688d310218cb387`，执行源码 `ee33372042d27911a97a14aefc6cb068404d190b`。首次运行的机械索引失败保留；只修一行索引后，同一截止窗口内的第二次运行于 15:31:39–15:32:32 UTC 成功，用时 52.957 秒，原截止 16:13:03 UTC 未变，两次 PID 均已退出。
- 独立辅助 [PR71 证据](../../research/C2/pr60_aux52/machine_notes.md)冻结于 `8878516c0ad12e60884419fc03525b2a7caa7be3`，执行源码 `ee8f0a105798494474b1afd41f69af96794c8f5f`。唯一运行于 15:59:05–15:59:06 UTC 成功，内部计时 0.57009441 秒，原 600 秒合同截止 16:09:05 UTC 未变，PID 已退出。没有失败、修复或重跑。

两条独立机器链分别限制为单进程、单 CPU/线程、16 GiB、无 GPU。机器 PASS 与解析桥接由不同职责完成；SECOND 没有执行作者或独立计算者的程序。合并与档案完整性检查均不是 CI、形式化或新颖性证明。
