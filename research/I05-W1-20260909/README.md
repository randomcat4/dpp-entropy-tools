# I05-W1-20260909：秩一交叉块全弦熵凹性

本目录归档任务 `I05-W1-20260909` 的冻结研究包和后续独立实现核验。总体状态仍为 **PARTIAL**：一般实对称有限核的 K-affine 全配置 Shannon 熵凹性，以及固定标量平稳 DPP 熵率凹性，均未在本任务中解决。

已证明的受限定理是：固定两个内部 Hermitian 严格收缩块 `A,C` 和向量 `u,v`，对

\[
K(t)=\begin{pmatrix}A&tuv^*\\tvu^*&C\end{pmatrix},
\]

完整配置 Shannon 熵在全部合法 `t` 区间上凹。该方向在非退化时整体秩为二，可同时改变多条交叉边，内部块不要求对角化、交换或具有坐标对称性。证明的关键是全部事件概率对 `s=t²` 的精确仿射性，以及两个完整块边际固定后得到的熵—相对熵恒等式。精确量词、边界和非主张见 [`result/frozen_statement.md`](result/frozen_statement.md)，完整证明见 [`result/proof.md`](result/proof.md)。

## 核验结论

[`INDEPENDENT_REVIEW.md`](INDEPENDENT_REVIEW.md) 的结论为 **PASS_WITH_SCOPE**：没有发现受限定理、秩二方法障碍或三个严格诊断例中的阻断性错误；原包核验脚本在干净目录中逐字节复现，另写的 Möbius 反演实现也独立重建了全部相关事件概率和符号。

这里的“独立实现”是指不导入提交者核验模块、改用另一概率构造和另一组断言进行交叉检查。它不是第二名人类同行审稿人，也不是证明助手认证；因此保留冻结文件 [`result/verification.md`](result/verification.md) 中原有的“尚未独立审阅”记录，不回写或伪造作者当时的验证状态。新颖性仍未认证。

## 目录

- `result/`：冻结结果包的全部正文、输入、脚本和正式输出，字节保持不变。
- `review/`：独立实现核验脚本、实际输出、冻结包复跑输出、来源核对和哈希绑定。
- `INDEPENDENT_REVIEW.md`：复核范围、推导检查、计算覆盖和剩余限制。

## 复现

测试环境为 Python 3.13.5、SymPy 1.14.0、mpmath 1.3.0。在本目录运行：

```sh
python -m pip install -r result/requirements.txt
python result/code/verify.py
python review/independent_check.py
```

第一条核验路径使用原包的精确有理对数区间证书；第二条不导入原核验脚本，以包含概率的 Möbius 反演构造完整事件概率。预期最后一行分别为：

```text
ALL EXACT CHECKS PASSED
INDEPENDENT CHECKS PASSED
```

原始交付 ZIP 的 SHA-256 为：

```text
09309a68d6c26e4a156e3b52e2bdec543e6ebd5d3ac8f60d716da277c513f5ee
```
