# I05 W2：非恒定轨道中心与标量熵率

本轮状态：PARTIAL。新增定理有完整作者证明，尚未独立非作者审阅，新颖性未认证。一般全合法区间目标没有闭合，没有真实熵率反例。

提交位置：研究分支 `research/W2-nonconstant-orbit-20260909`，Draft PR https://github.com/randomcat4/dpp-entropy-tools/pull/34 。本轮不修改 main。网页端完成证明与小规模代数自检；服务器重计算和独立非作者审阅留给 Codex，不声称已经开展或通过。

## 正文入口

`RESULT.md` 给当前结果与边界；`frozen_statement.md` 冻结命题；`proof.md` 含新定理全部证明与三路线桥接；`previous_proof.md` 是上一轮完整 529 行正文，含循环平均严格等号、显式率 gap、径向四次加强。`attempts.md`、`sources.md`、`verification.md` 与 `HANDOFF.md` 分别记录失败方法、来源、实际自检与接续义务。

## 复算

需要 Python 3.10+ 与 SymPy；本轮实际环境 Python 3.13.5、SymPy 1.14.0。可使用独立虚拟环境：

```sh
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/audit_new.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python previous/code/verify_round2.py
```

脚本按自身路径定位输入，所以可从任意工作目录运行。新脚本输出 `output/new_audit.json`；旧脚本输出 `previous/output/exact_audit.json` 及完整配置数据 `previous/output/exact_finite_distributions.json`。旧脚本开头保留原目录下的历史运行说明，不改变其数学实现。

新检查是两个固定四点对象、一个四点通道障碍和长度至 6 的闭步恒等式，不是参数扫描，也没有有限窗到熵率数值外推。数学证明不依赖这些点检。`output/run_record.json` 记录本轮实际运行。旧结果不重复计作本轮工作量。

本地交付 ZIP 额外含 `archive/previous_round2_full.zip`，保存旧完整产物及历史；公开 PR 不复制旧包中对私有研究库的读取记录。公开数学正文、旧复算代码和输入均已自包含，不依赖该历史 ZIP。
