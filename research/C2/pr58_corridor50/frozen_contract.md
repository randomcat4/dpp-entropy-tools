# Frozen contract: PR58 original 64-event corridor and s10 signs

C2认领PR58原始四文件包的独立机器重构：严格冻结**1770ed29e8487b8f39aebb4c9466406c7493e580**，原有有理3+3 fixture、全部64事件、四个s区间[3,9],[8,12],[11,14],[14,15]及s=10的W/真实曲率证书。新目录research/C2/pr58_corridor50。

从文字里的A,C,U,V有理矩阵及K(t)重建完整6×6 signed-determinant事件多项式、产品权重和每个q_s=1-sa+s²b，再独立算全部区间极值、精确矩、Psi/M2/平方裕量。s=10使用严格有理log级数余项，分别保存W和真实t²I''的区间、宽度及完整原始分数；不执行或导入作者checker，作者文字输出只作下游比较。

给此有限对象设置新的首单元上限**2700秒墙钟、单算术进程/CPU/线程、16GiB、无GPU**，低于用户总8CPU/32GiB上限。与新PR60辅助600秒单元分别计时、串行运行；各自预算从首次启动固定并包含必要修复。成功、首个精确不一致或截止即停，不暗扩、不跑通用扫描或whole-chord任务。当前PREPARING，无新算术PID。

**a4f05cc新增joint-additive及另一套s=9/10 fixture不在本合同内；issue63长whole-chord也不启动。** C2只提供机器证据，C1/C3保留分析首审、二审与集成边界。W负只否定该充分符号条件，不称为熵反例。