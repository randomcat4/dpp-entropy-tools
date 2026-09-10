# PR125 — 严格 `L^infinity` 符号的中心二阶差商与标量 KL 上界

Status: **ACCEPTED_SCOPED**。冻结作者头 `87897b307818e9eab84ad465b24b4aeb037a1dc1`，全部 4 个作者文件。S3 在未读取 S1 结论前完成全部作者源与承重来源的 fresh SECOND；随后完整读取 S1 PR131 的版本绑定 FIRST。两审对完整配置测量、非交换准自由 KL、混合 Toeplitz 极限、熵率 passage、中心对称性和排除项一致。没有运行计算，也没有评估新颖性。

## 接受的一般 KL 上界

若实符号 `c,f in L^infinity(T)` 满足同一严格谱条带

`a<=c,f<=1-a`

几乎处处成立，则有限 Toeplitz DPP 的完整占据配置律满足

`limsup_(n->infinity) n^(-1) D(P_(n,f)||P_(n,c))`

`<= integral_T d_Ber(f(theta)||c(theta)) dtheta`。

有限 gauge-invariant quasi-free state 的固定 occupation measurement 由全部 inclusion moments 和 Boolean Möbius 反演给出完整 DPP 原子律，因此数据处理方向是经典 KL 不大于量子 KL。量子对象只提供上界，没有把配置 Shannon 熵替换为 von Neumann 熵。非交换有限维准自由相对熵是 trace spectral 函数的 Bregman divergence；谱条带上的 divided-difference Hessian 给出 `1/[2a(1-a)]` Hilbert--Schmidt 常数。

作者的混合 Toeplitz trace lemma 用有限带多项式、Fejér `L^2` 逼近、Hilbert--Schmidt telescoping 和谱区间一致多项式逼近证明。它不假定两个 Toeplitz 压缩交换，也不要求 Fourier `ell^1`。因此有限量子 KL 的精确密度极限就是上述标量 Bernoulli KL 积分。

## 半周期路径的真实中心差商

令严格半周期偶中心 `c` 与非零半周期奇方向 `g` 都在 `L^infinity`，并把 `t` 限制在共同严格谱条带内。奇偶坐标边缘固定，`t=0` 时两边独立，故完整有限律满足

`D(P_(n,t)||P_(n,0))=H_n(c)-H_n(c+tg)`。

除以体积并取真实平稳熵率得到

`J(t)=h(c)-h(c+tg)>=0`。

对角 gauge `U_j=(-1)^j` 保持每个占据/空缺原子并把 `t` 变为 `-t`，所以 `J(-t)=J(t)`，真实中心二阶差恰为 `-2J(t)`。一般 KL 上界给出

`0<=J(t)<=integral_T d_Ber(c+tg||c)`

以及

`limsup_(t->0) J(t)/t^2 <= (1/2) integral_T g^2/[c(1-c)]`。

只导入已接受 PR53 的 regularity-free matching floor 时，对每个选定的非零奇 Fourier 系数还有

`J(t)>=(1/2)d_Ber(mu^2-|g_hat(k)|^2t^2 || mu^2)`。

这给出真实中心二阶差商的显式夹逼，但不证明 `h''(0)` 存在。

## 非 Wiener 族与方法障碍

由半周期偶、奇的 sign-cosine 组成的严格符号族属于 `L^infinity` 而不属于 `A_0`，所以本结论确实越过 Wiener 范围。另一方面，若先对全部闭路位移取绝对值并要求对所有长度和截断共同的几何常数，偶闭路系数与 `L^(2r)` 范数迫使所有截断一致有界；Fejér 核在零点再迫使 Fourier magnitude 可和。该论证只说明这条绝对闭路接口有 `A_0` 门槛，不是熵反例。

## 排除项与合并

本接受不包含 `C^2`、`C^4`、`h''(0)` 存在、离中心局部凹性、整个合法区间、一般标量弦、一般有限实核凹性、HMM 表示、谱熵替换、熵反例、新颖性、最优性或形式化验证。

- 作者源见 [总览](../../research/I05-DPP-36-Linf-second-difference-20260910/README.md)、[尖锐 KL 上界](../../research/I05-DPP-36-Linf-second-difference-20260910/sharp_scalar_KL_upper_bound.md)、[逆向审计与方法障碍](../../research/I05-DPP-36-Linf-second-difference-20260910/reverse_audit_and_A0_barrier.md)及[审阅合同](../../research/I05-DPP-36-Linf-second-difference-20260910/review_contract.md)。
- S1 FIRST 见 [冻结范围](../../research/S1-pr125-first-20260910/frozen_scope.md)、[报告](../../research/S1-pr125-first-20260910/review_report.md)、[来源审计](../../research/S1-pr125-first-20260910/source_review.md)和[绑定](../../research/S1-pr125-first-20260910/source_binding.json)。
- S3 fresh SECOND 见 [PR125 公开报告](https://github.com/randomcat4/dpp-entropy-tools/pull/125#issuecomment-5620443183)。

FIRST 档案 PR131 以 `0ee4298c22d518d43bf51d28bf50214b48899238` 合入，第二父为审阅头 `20a40b476c8b9e2d71900abddc40f233149363b0`。作者 PR125 以 `f5b711604c3c9b9b882f43f9a43624250e2bd432` 合入，第二父为精确冻结头 `87897b307818e9eab84ad465b24b4aeb037a1dc1`。接受范围仅以本文为准。
