# 路线台账：覆盖、否定、替代与未完成

## 本轮新增覆盖与方法障碍

| 判断 | 精确范围 | 证据 |
| --- | --- | --- |
| 已覆盖 | 对角/常数中心完整合法线凹性及径向二次、四次严格性；W2/C3 共同骨干只计一次 | [径向审核](verification_20260909/w2/radial_quartic_audit.md) |
| 已覆盖 | 循环平均完整等号条件及每个被删 Fourier 模式的严格真实熵率 gap | [循环平均审核](verification_20260909/w2/cyclic_audit.md) |
| 已覆盖 | W1 rank-one 交叉块；实 `m×2` 及至多两实际坐标列/行支撑的全弦 | [W1 第二轮](../research/C1-verification-20260909/READY_BATCH_03.md) |
| 固定反例对象已排除 | S1 三个固定符号对、C3-M1 固定三符号的正真实熵率 pair gap | [S1](verification_20260909/base_prs.md)、[C3-M1](../research/C1-verification-20260909/children/c3/review_rate_certificate.md) |
| 已覆盖 | C2 固定框架的显式上面锥/各向异性界；W3 标量中心 `epsilon^2/1000` 球内的全方向负曲率 | [C2](verification_20260909/base_prs.md)、[W3](../research/C2/verification2/w3/REVIEW.md) |
| 已覆盖 | W4 三维 `|K_ij|<=sqrt(v_i v_j)/4` 归一化子域的完整六方向界和闭包弦凹性；连通两边图也足以使 Hessian 负定 | [W4 最终审核](../research/C1-verification-20260909/READY_BATCH_04.md) |
| 充分条件已否定 | `max Qlock>=C` 及仅由相同三个投影组成的凸组合；完整 Fisher 在反例点仍大于 C | [N3 审核和复算](verification_20260909/pr24.md) |
| 统一余量已否定 | 连通严格 beta 零集上不存在固定正安全余量；已证稀疏族从 `d alpha<1` 一侧趋近阈值 | [C1 解析与有限证书分离审核](../research/C2/verification2/beta/REVIEW.md) |
| 充分条件已否定 | N4 最高层预算、W1 的有害 Q 对数项非负断言；低层/其余曲率项在所给例子仍补偿 | [N4/C2](verification_20260909/base_prs.md)、[W1](../research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md) |
| 桥接恒等式已否定 | 两相关 DPP 逐坐标选择等于核仿射混合；整体相关块刷新等于一般 rank-two 径向 DPP | [W2](verification_20260909/w2/README.md)、[W1](../research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md) |

仍开放：一般非恒定中心标量弦、全实三维 beta 零集界、一般固定框架中谱带、任意稠密两边均大于二的 rank-two 交叉块，以及更高维一般实核问题。固定无命中、有限盒或特定符号的严格证书不能关闭这些全域问题。普通 Fourier 平方可和尾也不能直接替代体积一致的算子尾控制。

PR39 新增的非恒定中心 Wiener 连续弱区间及更强局部通道不可能性尚待非作者审阅；不因旧 W2 径向定理已经合入而提前关闭对应路线。

更新于 2026-09-09。这里“关闭”必须带上范围：定理覆盖只排除所述区域；方法被反例否定只否定该方法。有限搜索没有命中，不能关闭数学上的反例空间。

## 定理已经覆盖的区域

| 对象或路线 | 当前判断 | 不能外推到 | 证据 |
| --- | --- | --- | --- |
| 严格实二维核 | 全局凹性及非平凡严格弦结论已复核 | 一般三维以上 | [R1](../research/R1/verdict.md) |
| 对角中点；固定块边缘、从解耦中点只改跨块 | 有全局有限弦排除；块熵次可加给出严格损失 | 任意耦合中点上的任意跨块弦 | [R1](../research/R1/proofs/diagonal_midpoint_candidate.md)、[R3](../research/R3/deepening_10h/fixed_block_global/verdict.md) |
| 由一维、二维块组成的中点 | 任意方向的块组合界给出非平凡严格弦损失 | 任意更大不可约块 | [R1](../research/R1/verdict.md) |
| 严格交换对称三维家族 | 全六维 Hessian 已闭合；家族内严格弦凹性已复核 | 一般非对称中心，或仅中点对称的任意长弦 | [R1](../research/R1/proofs/n3_equicorrelation_hessian.md)、[R3](../research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/exchangeable_triangle_global_closed/verdict.md) |
| 固定内点谱裕量下的三维乘积对角邻域 | 一致凸管区域的 Hessian 和严格弦结果已复核 | 无谱缓冲的全边界和任意远离对角的核 | [证明](../research/R1/proofs/diagonal_perturbation_neighborhood.md)、[复核](../research/R1/verification/diagonal_perturbation_reviews.md) |
| R2 固定数据两项投影边界层级 | 完整零横向 tomography 前提下的 C2 障碍已关闭 | 只满足第一层为零的对象；一般移动数据 | [R2](../research/R2/verdict.md) |
| A1 固定末坐标与耦合方向的径向切片 | 四参数严格弦凹性已复核 | 耦合方向本身自由旋转 | [A1](../research/A1/verdict.md) |
| A2 显式移动框架及冻结一致性条件 | 对应路径的负主项和余项已复核 | 所有移动框架、非紧端点尺度、任意有限步长 | [A2](../research/A2/verdict.md) |
| 路径 K 仿射族的紧参数弱耦合区域 | 连续区域内统一负曲率已复核 | 任意强耦合路径族 | [路径解析结果](../research/R3/deepening_10h/path_affine_chords/general_family/analytic_curvature/verdict.md) |
| twin-pair 且受限半正定二点方向 | 任意异质余部下的特定方向已排除 | 一般半正定方向 | [定号方向](../research/R3/deepening_10h/semidefinite_directions/verdict.md) |

## 已被否定的方法或推理跳步

| 被否定的主张 | 保存的原因 | 对主问题的影响 |
| --- | --- | --- |
| 仅靠算子范数控制给出与维数无关的总熵连续性 | T2 的 B1 边界族 | 不否定全局凹性；要求正确的维数依赖。[边界族](../research/T2/boundaries/boundary_families.md) |
| 无谱缓冲时仍存在统一的 Frobenius 平方熵差常数 | T2 的 B2 边界族 | 保留缓冲条件或改变界的形式，不否定凹性。 |
| 互信息沿所有有关弦都凸，从而逐块完成证明 | R1 保存了严格可行、精确的互信息充分条件反例 | 同一弦的完整事件熵 gap 仍为负；只关闭该全称充分条件。[R1 入口](../research/R1/README.md) |
| 条件加速度总非正，可以直接丢掉 | A1 有正条件加速度的有理证书 | 总曲率仍负；后续证明必须保留并控制该项。[A1](../research/A1/verdict.md) |
| 二维固定谱基的逐层符号可以原样推广到三维 | 三维单事件二阶导数及条件基数层可以为正 | 补集层抵消仍可能救回总熵；只关闭简单逐项论证。[二维与三维阻断](../research/R3/deepening_10h/dense_hessian/commuting_spectral/low_dim_exact/verdict.md) |
| 同时正交对角化就可以当作原观察坐标的独立乘积 | 配置熵不是只依赖谱的函数 | 保留固定谱基投影通道，不能丢弃观察基。[通道](../research/R3/deepening_10h/dense_hessian/commuting_spectral/analytic_channel/verdict.md) |
| 固定数据首项可直接代入随 epsilon 缩小的方向 | A2 的精确尺度交叉例子显示主项层级变化 | 旧固定数据定理不因此失效；移动情形须重新证明一致性。[A2](../research/A2/verdict.md) |
| 主子式可直接当精确事件概率计算 Shannon 熵 | T3 早期核心公式已修复 | 保留 Möbius/独立参考门槛；旧错误输出不能成为候选。[T3](../research/T3/README.md) |

## 已被后续结果覆盖的旧缺口

- **A1 的半填充对称三角形平凡块**：旧裁决保留“未证明”；当前已由 R1/R3 更广的交换对称三维定理覆盖。A1 的径向切片定理和加速度障碍仍有独立用途。
- **R3 exchangeable_triangle_global_attempt 的中间区域及四个角落**：最终 `exchangeable_triangle_global_closed` 单元覆盖了它们。旧尝试保留为历史，不再作为该家族的当前阻塞。
- **R3 顶层某些 Lambda=0 宽泛措辞**：不能据此宣布整个子流形完成。后续专门单元明确为 INCOMPLETE，并含待独立复核的参数化与邻域候选。[专门裁决](../research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/lambda_zero_subfamily/verdict.md)
- **R3 早期分组降维被否定版本**：修正后按每组参数及小维 Möbius 交叉检查归档；保留旧否定，不能继续引用旧版本的过宽假设。

## 仍开放或仅有候选

| 剩余方向 | 精确状态 |
| --- | --- |
| 一般三维秩一标量界 `rho<=1` | 与剩余 Hessian 问题等价的阻塞，不是一个已经证完的辅助引理。 |
| R1 的 `F>=D_*` | 是更强的充分条件；单边归约部分 odds 区间已覆盖，剩余大 odds 和双边族仍开放。不能因该条件没完成而撤销对称熵定理。 |
| 一般对称路径、全部 Lambda 零子流形 | 专门单元仍有缺口；部分局部球、恒等式和参数化只标候选。 |
| 非紧指数退化尺度 | 紧参数楔形已有局部结果，剩余统一常数的重建不能由有限点替代。 |
| 一般固定谱基、一般 PSD/NSD 方向、更高维连通核 | 仍只有受限定理、机制归约和有限 SCOUT。 |
| T3 端到端证书链 | 原型测试与一个种子通过，整链验收仍待完成。 |

R1 的 8,053 个超门槛浮点正值经 90/140 位复查没有存活；R3 原始约 `7.11e-15` 正 gap 和路径下溢伪阳性均被追清。它们是计算候选的淘汰记录，不是对数学上所有实反例的排除。各路计数存在复查和重用，不能简单相加成唯一样本总数。
