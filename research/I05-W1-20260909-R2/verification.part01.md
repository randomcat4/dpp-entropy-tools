# verification.md — 作者自检、精确复算与误差说明

任务 ID：I05-W1-20260909-R2

## 1. 审阅状态

- 作者自检：完成。
- 同会话第二种实现交叉复算：完成。
- 新上下文非作者审阅：**尚未独立审阅**。
- 形式化证明助手认证：无。
- 新颖性审阅：无。

因此本包的 `PROVED` 是冻结受限定理的作者级数学裁决，不等于独立同行认证。

## 2. 运行环境

实际环境：

```text
Python 3.13.5
SymPy 1.14.0
mpmath 1.3.0
```

严格计算只依赖标准库 `fractions.Fraction` 和 SymPy。`mpmath` 仅在开发期作高精度直观对照，不承担最终符号；正式脚本不导入它。

安装与运行：

```sh
python -m pip install -r requirements.txt
python code/verify.py
python code/export_exact_data.py
```

正式 `verify.py` 的末行必须是：

```text
ALL EXACT AND INTERVAL CHECKS PASSED
```

完整实际输出保存在 `data/verification_output.txt`。

## 3. 精确检查范围

`code/verify.py` 实际完成：

1. 用 SymPy 对四事件概率符号变量展开，验证二维证明中的
   
   `det(G-lambda Q)=(16r+4 lambda E-lambda^3 P)/(16rP)`；
2. 对 `2+2` 有理 rank-two 例，从单行列式公式构造全部 16 个完整事件；
3. 对 `3+2` 有理例构造全部 32 个完整事件；
4. 用 Sylvester 顺序首主子式严格检查 `K(+t),K(-t),I-K(+t),I-K(-t)` 正定；
5. 对每个左块完整配置和每个右块配置逐项核对
   
   `p_K(S,T)=p_A(S)p_{C-t^2 B^T X_S^{-1}B}(T)`；
6. 核对左右两个完整边际，及 `R,Q` 对两边际的全部贡献均为零；
7. 精确核对 `sum_S p_A(S)X_S^{-1}=0`；
8. 在 `2+2` 满秩例上核对 rank-two 外幂似然比、`E G=0` 与 `E det G=0`；
9. 核对整块刷新与径向 DPP 的差恰为 `lambda(1-lambda)s^2Q` 且非零；
10. 对 `Q` 对数项、Jeffreys 项和完整曲率给严格有理端点区间。

`code/export_exact_data.py` 输出 `data/exact_event_data.json`，其中含两个例的全部 `P0,R,Q,P_s`、条件核和条件事件概率，便于不依赖脚本逻辑逐项复算。

## 4. 对数区间与误差界

所有矩阵、概率、系数和 Fisher 有理项均为精确 `Fraction`。唯一超越量是正有理数的自然对数。对 `x>0`，令


a = (x-1)/(x+1).

脚本使用恒等式

```text
log x = 2 sum_{k=0}^{N-1} a^(2k+1)/(2k+1) + R_N
```

及纯有理余项界

```text
|R_N| <= 2 |a|^(2N+1) / ((2N+1)(1-a^2)).
```

当 `a>=0` 时余项非负；当 `a<0` 时余项非正，因此脚本还利用了正确的单侧方向。正式取 `N=220`，再按每个有理系数的符号传播区间。显示的小数端点用 floor/ceiling 向外舍入；底层有理端点才是权威证书。

得到：

```text
<Q,log(P_s/P_0)>
  in [-0.453573880156865070680274635197,
