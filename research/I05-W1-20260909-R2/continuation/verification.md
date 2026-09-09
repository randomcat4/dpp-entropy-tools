# verification.md

状态：**AUTHOR EXACT CROSS-CHECKS PASSED / INDEPENDENT REVIEW PENDING**。

本文件汇总 PR #43 的两条作者复算链；之前的版本只记录了后写的活动扇区／Markov 链，遗漏了三点与相关 `3+3` 链。

## A. 第二轮 continuation 早期正定理复算

运行：

```sh
python research/I05-W1-20260909-R2/code/verify_continuation.py
```

保存输出：`../data/continuation_verification_output.txt`，末行：

```text
ALL CONTINUATION CHECKS PASSED
```

精确覆盖：

1. 三点严格核和不定秩二方向的全部八个事件多项式；
2. `adj(D)=gamma nn^T`、条件四循环分解及六个条件两点 Rayleigh 差；
3. 显式相关 `3+3` 例中 `A,C,I-A,I-C` 的严格性；
4. `rank(B)=2`、左右零空间、`M_0=B^TB` 的特征多项式；
5. 八个左配置：空／满条件方向为 `-5M_0/3`、`5M_0/2`，其余六个为不定秩二；
6. 精确合法半径
   \[
   \tau^2=4091/15000-\sqrt{1663}/150;
   \]
7. 全部 64 个联合事件上的 rank-two 外幂似然恒等式及 resolvent 矩消去。

作者复算曾发现示例脚本把一个诊断方向的常数误写为 `adj(D)=-9*ones(3)`；精确值是 `-5*ones(3)`，对应 `gamma=-15`。解析定理从始至终使用一般恒等式 `adj(D)=gamma nn^T`，不依赖该错误常数；脚本已经修正并完整重跑。

输出中的两个 100 位负曲率值只是诊断，没有向外舍入区间，不承担定理证明。

## B. 后写活动扇区、Markov 与量子障碍复算

运行：

```sh
python -m pip install -r research/I05-W1-20260909-R2/continuation/requirements.txt
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
python research/I05-W1-20260909-R2/continuation/code/verify_continuation_v2.py
```

保存输出分别为 `verification_output.txt` 和 `verification_output_v2.txt`，末行为：

```text
ALL CONTINUATION CHECKS PASSED
ALL CONTINUATION V2 CHECKS PASSED
```

精确覆盖：

1. `3+5` 活动扇区例在多个有理 `t` 上的严格收缩性；
2. 全部 256 个联合事件与每个左配置的 32 个条件事件；
3. `rank(B)=2`、活动右坐标与约化块结构；
4. 对角三点刷新核的 8 个状态、64 个转移概率、平稳性和一／二次外幂缩放；
5. mixed-discriminant 展开；
6. 两模准自由测量障碍；
7. 可逆外幂半群障碍 `E[dG_{12}]=-125/78`；
8. 固定相关三点非可逆伴随生成元 LP 输入。

## C. 尚未独立审阅的范围

上述全部是同一网页作者会话中的 exact 交叉复算，不是新的非作者审阅。新上下文必须至少独立审阅：

- 条件 Schur、`m x 2` 与两坐标支撑提升；
- 三点不定秩二定理的条件四循环分解和边界；
- 外幂充分统计的 KL／互信息保持和压缩 Hessian；
- 三点条件方向判据；
- 相关非坐标 `3+3` 结构族及精确合法半径；
- 活动扇区／对角锚点；
- Markov 伴随方向、完整 Fisher 系数、可逆障碍和量子障碍。

最新规范见 `CODEX_VERIFICATION_TASKS_v2.md`。涉及对数或全参数区间的新数值证书必须使用向外舍入区间或带显式余项的有理级数。
