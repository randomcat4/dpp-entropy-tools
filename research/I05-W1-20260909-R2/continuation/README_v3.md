# I05-W1 第二轮延续 — 最新入口

总体状态：**PARTIAL / CONTINUATION NOT YET INDEPENDENTLY REVIEWED**。

最新文件：

- `RESULT_FINAL.md`：准确裁决、已证明范围和未解决范围；
- `frozen_statement_v3.md`：最新冻结命题；
- `proof_v3.md`：第二轮原证明与 continuation 证明的完整阅读顺序；
- `attempts_continuation.md`：三条领域路线、失败桥梁和剩余义务；
- `sources_continuation.md`：原始来源与采用边界；
- `verification.md`：作者 exact 复算与独立审阅边界；
- `CODEX_VERIFICATION_TASKS_v2.md`：非作者解析审阅、非可逆定向流 LP、全区间曲率和严格反例门槛；
- `HANDOFF.md`：下一步顺序。

作者 exact 入口：

```sh
python -m pip install -r requirements.txt
python code/verify_continuation.py
python code/verify_continuation_v2.py
```

本轮新增的正结果是对角活动约化扇区上的任意秩跨块全弦凹性，以及逐条件线对角锚点判据。一般相关活动块的 rank-two 目标仍开放。外幂信息收缩路线已精确推广到非可逆 Markov 密度伴随，同时用 `-125/78` 有理矩严格排除了普遍可逆半群。相关准自由衰减也被证明不能自动下降为经典占据配置通道。
