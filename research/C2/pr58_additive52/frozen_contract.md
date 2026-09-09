# Frozen contract: PR58 joint-additive fixed witness

C2认领独立新单元 issue52 comment5604861257：PR58 joint-additive 的固定 s=9/10 样例，冻结数值作者头 **a4f05cc962985015b71635bf633acce9dfe76866**，只覆盖 ADDENDUM_JOINT_ADDITIVE.md section3 的字面矩阵、完整64事件、dual表和(3.4)–(3.7)。后继5ab3cae只作为C1/C3文字修订背景，不改本次数值绑定。

新目录research/C2/pr58_additive52；从字面输入独立重建，不导入/执行作者checker。检查严格Schur合法性、全部边际/条件a,b消去、dual行列和、完整Fisher/加速度及P0,A2,W,L,T和真实曲率；用严格有理对数余项与向外端点逐字核验小数界，出现首个精确不一致立即保留并停止，不用定性符号掩盖显示错误。

单独新窗口600秒，从首次算术启动固定，单进程/CPU/线程、16GiB、无GPU，含修复；不继承PR60或原PR58窗口。PR60辅助已exit0/PID174471已消失，完整包收尾中；原PR58 corridor/s10仍排在本单元之前。根实例统一串行启动，无重叠、扩样例/扫描、issue63whole-chord或自动延时。当前PREPARING，无新PID。C1有限证据FIRST与C3二审/集成另行负责。