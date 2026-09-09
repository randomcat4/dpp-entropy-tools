# Frozen contract: PR60 fixed radial obstruction and true curvature

C2认领独立小单元：issue52 comment5604536353，PR60 continuation固定K*,D*,C*及h=1/100000，冻结作者头f869fd251c0d6fdad737b6d5efa287307795a87d，公式(23)–(36)中的辅助径向障碍、真实曲率及Jensen检查。

现有full-r算术已结束，完整MACHINE_PASS包已交付PR64@5b40617fe7172aa266614aa28688d310218cb387。新小单元不复用其窗口。新目录research/C2/pr60_aux52；只从文字里的有理矩阵重建全部8个精确事件和混合jets，不运行或导入continuation_exact.py。严格有理atanh/log2余项与向外端点分别核对负径向导数、正-H''、负Jensen及合法性/exp(Lambda)。

新窗口上限600秒，自首次新算术启动固定；单进程/CPU/线程、16GiB、无GPU，包括必要修复。成功、首个精确不一致或截止即停，不扩参数/样例/扫描。当前PREPARING、无新PID；根实例统一串行启动与登记，两类有限任务不重叠计算。C1原FIRST评估该Claim4，C3负责后续二审。