# I05-W1-20260909 result

整体状态：PARTIAL。完整定义与适用范围在 frozen_statement.md。
主结果是任意维数、固定内部块、秩一交叉块标量缩放的全配置熵凹性定理。
一般实核目标与固定标量平稳目标均没有在本包中解决。

建议阅读顺序：RESULT.md → frozen_statement.md → proof.md → attempts.md。
sources.md 给原始文献定位；verification.md 给证明和代码的核验边界；
HANDOFF.md 给至多两个精确的后续任务。CLAIM.md 保存初始认领。

## 复算

测试环境：Python 3.13.5、SymPy 1.14.0。

```sh
python -m pip install -r requirements.txt
python code/verify.py
```

脚本从自己的位置解析 data/，不依赖当前工作目录、私有文件路径、网络或云端文件。
严谨符号证书不使用浮点运算。执行将重建 data/ 中全部正式核验输出。
验证对象包括全部配置、包含概率、完整 Fisher、条件分解、非交换四点例、
复 Hermitian 受限例，以及更高交叉秩的代数障碍。

code/explore_symbolic.py 和 data/exploration_output.txt 保留初期确定性符号诊断；
其数值打印仅作探索，不能替代 code/verify.py 的严格有理区间。

输入矩阵另列于 inputs/exact_inputs.json；用户原始任务文件保留在 inputs/uploaded/。
没有附带整篇第三方论文，数学论证并不依赖下载论文后才能执行。
