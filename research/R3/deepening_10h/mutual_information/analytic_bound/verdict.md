# D10-C2 裁决

STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW

一般 rank-two PSD 全称局部不等式：INCOMPLETE。固定十一维非 thinning 族：得到带精确系数证书与统一余项界的排除证明候选。

固定 M 与 D 见 derivation.md。D 秩2且 PSD，两个边缘与跨块方向都非零。对全部 |t|≤1/32，证明候选给出

`Delta(t)<=-t²/2`，

即 `G(t)<=KL(q||p_0)+JS(p_-,p_+)-t²/2`。等号 G=KL+JS 只在 t=0 成立。统一严格谱裕量为17/320，跨块 Frobenius 范数大于13/64，全部对角间隔大于1/50；不依赖近解耦或重复行型退化。

解析展开明确显示：G 首项为二阶，JS 首项为正二阶，KL 首项为正四阶。该例严格二阶代价系数 L2>0.555789，而几何推动系数约0.020253；导致失败的主要局部代价是 JS/Fisher 项，不是四阶 KL。

证书覆盖完整2048事件，p、a、b 均为有理数；对数使用有理级数余项上下界。统一 |H''''|<941，再由 Taylor 余项推出整个连续区间，未把有限取点负号当作定理。三个 n=4 小维核通过直接 Möbius 的逐事件精确相等检查。两项 Decimal 数值检查仅作 sanity，不进入证明。

产物：derivation.md、sanity_certificate.py、extend_radius.py、results/certificate.json、results/radius_1_over_32.json、results/exact_coefficients.jsonl。

没有增加随机样本。两个脚本均正常退出，退出码0，只使用本目录及标准库；未访问其他工作目录、服务器或 C:\\canglan。作者不自称 CORRECT。下一步由新上下文验证证明和证书；一般 L2≥0 的全称符号仍是未闭合障碍。
