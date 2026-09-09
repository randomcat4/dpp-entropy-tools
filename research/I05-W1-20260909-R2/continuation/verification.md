# verification.md

状态：**AUTHOR CROSS-CHECK PASSED / INDEPENDENT REVIEW PENDING**。

运行环境使用 Python 3 和 SymPy 1.14.0。入口：

```sh
python -m pip install -r research/I05-W1-20260909-R2/continuation/requirements.txt
python research/I05-W1-20260909-R2/continuation/code/verify_continuation.py
```

作者实际运行退出码为 0，末行：

```text
ALL CONTINUATION CHECKS PASSED
```

脚本只用精确整数/有理 SymPy 运算完成以下检查：

1. `3+5` 活动扇区例中 `A,C,K(1/5),K(1/2),K(1)` 和各条件核的严格收缩性。
2. 三个 `t` 值上全部 256 个联合完整事件，以及每个左配置下 32 个右条件事件的 Schur 分解。
3. `rank(B)=2`、三个活动右坐标和约化块结构。
4. 对角三点例的 8 个状态、64 个刷新转移概率、平稳性、可逆性、`T G=theta G` 与 `T detG=theta^2 detG`。
5. 二维 mixed-discriminant 展开逐状态恒等式。
6. 两模准自由测量障碍的相同输入配置分布及不同输出满事件概率。
7. 固定相关三点生成元 LP 输入的事件概率、四个特征和零均值矩，并生成 `inputs/generator_instance.json`。

这些复算不证明外部对角锚点直线定理，也不构成新的非作者审阅。一般相关 rank-two 结论仍需 `CODEX_VERIFICATION_TASKS.md` 中的解析审阅、exact LP/Farkas 证书和全区间熵曲率认证。

误差说明：本脚本没有依赖浮点符号，因此没有数值舍入误差项。后续涉及对数和全区间曲率时，必须使用向外舍入区间或带显式余项的有理级数；具体阈值见 Codex 任务文件。
