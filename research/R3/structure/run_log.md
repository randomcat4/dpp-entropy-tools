# 运行记录

状态 INCOMPLETE。无后台遗留搜索作业。全部路径只涉及分配给 structure 的目录；没有访问 C:\\canglan。

## 环境探测

1. 检查远端任务目录（当时尚不存在）、已有进程、负载与内存。负载约 4.20，已有两个其他 Python 进程各约一个 CPU；没有停止或修改它们。整条探测命令最后使用默认 python 导入 NumPy 失败，退出码 1，错误为 ModuleNotFoundError。此项是环境探测失败，不计入数学采样分母。
2. /opt/venv/bin/python 成功导入 NumPy 2.1.2、SciPy 1.14.1；附带的进程 cwd 查询因命令转义未产生结果，整条命令退出码 1。后续不依赖该查询。没有改变依赖或环境配置。
3. 创建本任务远端目录并上传独立自编脚本，命令退出码 0。没有 clone 源码仓库；因此不存在共享 checkout 或未读仓库 AGENTS.md 的问题。

## 三批计算

工作目录均为 /root/i05-real-20260908/R3/agents/structure。进程环境 OMP_NUM_THREADS=1、OPENBLAS_NUM_THREADS=1、MKL_NUM_THREADS=1；脚本亦设置 NUMEXPR_NUM_THREADS=1。解释器为 /opt/venv/bin/python；不使用 GPU。最大组数 6，最大主 Hessian 批次张量数量远小于 12 GiB；搜索至多短时并行两条单线程进程。

| 批次 | 参数 | 数学采样数 | 退出码 | 秒数 |
|---|---|---:|---:|---:|
| batch01 | --out batch01 --trials 240 --validate，默认种子 2026090803 | 240 + 32 小维校验 | 0 | 2.7113 |
| batch02 | --out batch02 --trials 2400 --seed 2026090804 | 2400 | 0 | 25.1734 |
| batch03 | --out batch03 --trials 320 --seed 2026090805 --sizes '[[2,2,2,2,3],[2,2,2,2,2,2],[3,3,3,3,3],[2,3,2,3,2,3]]' | 320 | 0 | 66.6407 |

batch01 完成后才开启 batch02。batch03 启动时 batch02 已接近完成；两条单线程进程短时并行，合计最多 2 CPU 线程，仍小于分配上限 4。全部已正常退出。

初版脚本每点立即写账本，但没有恢复选项。三批结束后加入 --resume，以同种子重放随机数状态而跳过已完成计算，并拒绝不带 --resume 覆盖现有账本。恢复功能未用于原始三批；不得把其未测试能力当作数学验证证据。

汇总脚本退出码 0；完整账本 2960 行，FAILED=0，CANDIDATE=0，NO_HIT=2960。参数/方向 JSON、谱裕量、熵值、gap、随机种子、批次和连通性数据均在合并 candidate_ledger.csv 中。详细起始时间以远端 manifest 的 epoch 为准，未把远端系统日期改成会话日期。
