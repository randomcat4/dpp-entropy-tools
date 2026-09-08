# D10-C 运行与分母

状态：INCOMPLETE。所有本轮计算已正常结束，没有后台遗留搜索。

工作目录先确认在当前 repo。完整读取 AGENTS.md、deepening_10h 下的 problem.md、assumptions.md、frozen_theorem_v1.md、local_toolbox.md、cross_category_probe.md、hazards.md、lemma_ledger.md。收到先行工作边界后读取 Gu 报告原文，将 rank-one 和 thinning 排除，不把已知结论作为本轮新进展。

仅编辑 mutual_information/；未搜索、读取或修改 C:\\canglan，未更改共享文件或索引，未查看/停止其他进程，未派生子智能体。此次计算全部在本地完成，公开产物没有服务器连接信息或凭据。

## 环境与错误记录

PATH 中的 python 为 Windows 应用别名，调用失败（退出码 1）。改用现有捆绑 Python 3.12.14；NumPy 2.3.5 可用，SciPy 和 mpmath 导入探测失败（各次退出码 1）。没有安装依赖。计算脚本只用 NumPy、标准库 Fraction 与 Decimal；不存在因依赖失败而遗漏的数学候选。

各脚本设置 OMP_NUM_THREADS、OPENBLAS_NUM_THREADS、MKL_NUM_THREADS、NUMEXPR_NUM_THREADS 为 1，顺序执行；无 GPU。最大联合事件枚举 2048，最大完整 Hessian 参数维数 66，主要数组规模小于 1 GiB。

## 正常计算

| 程序 | 内容 | 退出码 |
|---|---|---:|
| probe.py | 冻结的 78 个秩二不定号提议，77 接受、1 过滤；231 条弦 | 0 |
| mi_hessian_diagnostic.py | 同样九个基点的完整 MI Hessian及9条定向弦，无新随机提议 | 0 |
| validate_diagnostic.py | 九个方向的精确有理秩与非径向性、12次小维端点 Möbius 对照 | 0 |
| paired_sign_diagnostic.py | 九个既有向量对的受控符号配对，54次弦评价，无新随机提议 | 0 |

主程序随机种子 202609081903，实际程序时间约 1.49 秒；Hessian 诊断约数秒；符号配对约 0.42 秒。精确起始时间、PID、版本、退出码见各结果文件。没有以“10小时”名义占满时间或扩大原始随机分母。

主账本 309 行，包含全部接受方向、弦结果和被过滤提议。诊断分母分别保存在其 JSON 中，汇总入口是 results/evidence_index.json。总计 294 次有限弦评价，不宣称它们是 294 条互不相同的弦；配对实验可能在共同步长上复算既有不定号弦。

全部严格谱证书使用 Fraction 精确有理 LDL 主元正性。候选熵仍为 float64；任何正 gap 才调用 Decimal 60/100 位复算。本轮三个阶段均无正 gap，因此未执行高精度熵分支，也没有外向取整区间正号证书。
