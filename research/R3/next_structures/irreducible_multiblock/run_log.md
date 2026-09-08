# NS-2 运行记录

状态：SCOUT。有界任务已正常退出，无本任务后台搜索遗留。

先完整读取仓库 AGENTS.md、R3/problem.md、R3/verdict.md、旧 structure/research_note.md，以及 noise_followup/README.md、completed_search_summary.json、index783_high_precision.json。旧噪声记录显示近零耦合方向不能作为有效信号；本轮据此预先固定支持边绝对值下界与异质对角分离下界。

工作目录确认在当前任务的 irreducible_multiblock 子目录；未读写 C:\\canglan。只编辑分配给本任务的目录；未操作共享索引，未回滚其他改动，未派生子智能体。计算在用户授权的隔离目录执行。公开文件不含服务器地址、端口、凭据或连接配置。没有查看或停止其他进程，没有安装系统依赖或改变全局环境。

## 事前限制与命令

计算前确认隔离输出目录尚未存在；脚本会拒绝覆盖已有 results，防止重复运行。环境依赖检查成功，NumPy 2.1.2、SciPy 1.14.1、mpmath 1.3.0 均已存在。实际主程序只需 NumPy 和标准库 Fraction；仅有正 gap 时调用 mpmath 复核。

执行的程序命令（不含私有连接信息）：

`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /opt/venv/bin/python probe.py --out results`

脚本内部同时将 NUMEXPR_NUM_THREADS 设为 1。只运行一个 CPU 进程，不使用 GPU；最大矩阵维数 12，最大枚举规模 4096，Hessian 支持维数 27，主要张量远小于 8 GiB。运行 PID、时间戳、种子、版本、分母与退出状态记录于 results/manifest.json。

## 实际结果

- 预设与实际基点均为 6+12+12=30，无重抽或增加预算。
- 先完成 n=8 的 6 个 Möbius 校验，全部通过，之后才执行 n=11、12。
- 解析 Hessian 30 个，有限差分对照 30 项，有限弦 90 条。
- 失败记录 0，FLOAT_CANDIDATE 0。因此高精度候选复核分支没有被触发；不宣称已经运行 60/100 位精度熵计算。
- 全部中心和弦端点用精确有理 LDL 检查严格谱裕量。证书中的 m 由浮点值提议，但通过/失败判断只使用 Fraction 精确有理算术。
- 脚本正常退出，退出码 0；报告总耗时 15.953538 秒。未运行第二轮、局部优化或大规模续搜。

只下载了本任务自己的结果。完成后报告 SCOUT，不因“全是负值”宣称一般凹性，也不因“结构不同”自动晋级 DEEP。独立验证留给新的上下文。
