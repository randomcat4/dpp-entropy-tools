STATUS: CORRECT

# D10-SV fresh audit: twin-pair semidefinite directions

验证者：非作者新上下文。
范围：只验证 `research/R3/deepening_10h/semidefinite_directions/` 的 S-T
twin-pair 受限子类定理；不认证一般 G-S PSD/NSD 方向命题、不认证实反例、
不认证新颖性。未修改作者文件；独立脚本只写入本 `verifications/` 目录。

## 1. 冻结命题与范围忠实性

- `frozen_claim.md:7-13` 明确把一般问题 G-S 保留为 INCOMPLETE；S-T 是
  后续单独列出的可核验子类，不是偷改一般问题。
- `frozen_claim.md:17-29` 的 S-T 量词为任意 `n>=2`、固定余部 `B`、相同
  外耦合两行 `y^T,y^T`，沿
  `D_pair=[[d,e],[e,d]]`，且整段 `J` 严格可行；PSD/NSD 条件写作
  `d>=|e|` 或 `-d>=|e|`。
- `frozen_claim.md:35-37` 已声明该类需要 twin 外耦合，非一般 PSD 方向覆盖。
  我的判定只覆盖这个结构子空间；在全 `Sym_n` 中它仍有等行外耦合的结构约束。

## 2. 数学证明核查

### exact event 语义

`derivation.md:8-16` 的
`p_K(S)=(-1)^(n-|S|) det(K-Q_S)` 与 Boolean Möbius 反演一致；它没有把
`det K[S,S]` 当 exact event。严格正收缩给所有 exact atoms 正，从而相应
`K-Q_S` 可逆；这足以支撑后续行列式微分。

### 等对角二点核与 Shepp-Olkin 常数

对 `C(t)=[[alpha,beta],[beta,alpha]]`，`derivation.md:68-82` 的分解正确：
谱参数 `lambda_+=alpha+beta`, `lambda_-=alpha-beta` 在 `(0,1)`，基数
`N` 服从两个独立 Bernoulli 之和，且因 `p10=p01`，

`H(C)=H(N)+P(N=1)log 2`.

沿斜率 `(d,e)`，

`P(N=1)=lambda_+ + lambda_- - 2 lambda_+ lambda_-`,

所以

`P(N=1)''=-4(d+e)(d-e)=-4(d^2-e^2)`.

`prior_scope.md:16-19` 只把 Hillion-Johnson 的 Shepp-Olkin 定理作为已知
Bernoulli-sum entropy 凹性使用；该定理正好给仿射参数路径下
`H(N)''<=0`。因此二点结论
`H(C)'' <= -4(d^2-e^2)log 2` 的常数、符号和适用条件均匹配。

### 条件化提升

`derivation.md:89-99` 的 Schur 补式

`p_K(S∪T)/w_T = (-1)^(2-|S|) det(C_T(t)-Q_S)`,

其中 `C_T(t)=A(t)-X B_T^{-1} X^T`，符号正确。因为 `X` 的两行相同，
`X B_T^{-1} X^T` 是全 1 矩阵的标量倍，故条件二点核仍为等对角、等外
偏移形式。

`derivation.md:101-104` 对条件核严格性的处理可接受：严格正收缩的余部
边缘给 `w_T>0` 与 `B_T` 可逆；四个条件 atoms 为正且和为 1。二点核的
对角元是条件单点包含概率，`det C_T` 与 `det(I-C_T)` 分别是条件双点与
空事件概率；配合二阶 Sylvester 判据得到 `0<C_T<I`。

于是 `derivation.md:106-109` 的链式熵分解

`H(K(t))=H(B)+sum_T w_T H(C_T(t))`

合法，且 `w_T` 不随 `t` 变。逐个 `T` 应用二点引理后，得到冻结界
`H''(K(t)) <= -4(d^2-e^2)log 2`。

### 严格性、rank-one 退化与 gap 符号

- 若 `|d|>|e|`，则 `d^2-e^2>0`，上界已严格为负。
- 若 `|d|=|e|` 且 `D!=0`，`D` 为 rank-one；各 principal determinant
  关于 `t` 至多一次，Möbius 组合也仿射。因此
  `H''=-sum_S (p'_S)^2/p_S`。又 `d!=0`，单点包含概率
  `P(1 in Y)=K_11(t)` 的导数为 `d`，所以不可能所有 exact-atom 导数全零；
  严格负成立。此处对应 `derivation.md:111-116`。
- `Delta=(H(t-h)+H(t+h))/2-H(t)` 的符号与项目约定一致；由二阶导上界积分
  得 `Delta <= -2(d^2-e^2)log(2)h^2`，因此它是排除正 gap 的结论，不是
  反例声明。

## 3. 计算复核

### 作者记录的只读核查

作者 `sanity.py` 会重写 `results/`（见 `sanity.py:17-18` 与
`sanity.py:184-188`），因此本验证没有直接运行作者脚本；作者输出只按
只读材料核对。`verdict.md:19-33` 记录作者有限分母为：

- n=4,11 两个固定实例；
- 每个 `t=-1/2,0,1/2`，共 6 个核点、2 条有限弦；
- 6192 个 exact events 的 direct-Möbius 与 signed determinant 对照；
- 2064 个条件 Schur identities；
- 0 随机样本、0 失败断言、0 正 gap 候选。

我的独立脚本读取作者 `results/sanity.json` 中 n=11 矩阵并核查：

- `D_pair` 特征值为 `3/10, 1/10`，rank 2，`d^2-e^2=3/100`；
- `y` 全非零且两行外耦合一致；
- 坐标图连通，非直和；
- `D` 不可能是 thinning 方向 `cM`；
- 端点 Gershgorin 下界分别为
  `[-1/2]: K 3/10, I-K 16/45, min 3/10`，
  `[+1/2]: K 82/225, I-K 1/5, min 1/5`。

由于每行的 `K_ii-sum|K_ij|` 与 `1-K_ii-sum|K_ij|` 都是“仿射减凸”的凹函数，
端点为正即覆盖整段 `[-1/2,1/2]` 的严格正收缩裕量。

### 独立 n=4 有理例子

新增不同参数的 n=4 检查在
`verifications/fresh_semidefinite_check.py:196-253`：

```
a=1/2, b=1/9, y=(1/100,-1/120),
B=[[2/5,1/20],[1/20,3/5]],
d=1/10, e=1/30, d^2-e^2=2/225.
```

脚本独立实现 Bareiss determinant、Boolean Möbius exact atoms、signed
determinant exact event、Schur 条件化、二点 Hessian 公式和图连通检查
（见 `fresh_semidefinite_check.py:26-193`）。

运行结果：

- 区间 `[-1,1]` 端点 Gershgorin 最小裕量 `427/1800>0`；
- 3 个核点、48 个 exact event signed-determinant 对照全部通过；
- 中心 16 个条件 Schur identities 全部通过；
- `H''(0)=-0.081521430631781477793735326605453141880044631948664307775502362072253776365865930`；
- 解析上界
  `-4(d^2-e^2)log2=-0.024645233086575833223723808762957389087128893666142409035401955893098439892255813`；
- `H''-bound=-0.056876197545205644570011517842495752792915738282521898740100406179155336473610117<0`；
- 条件分解加权 Hessian 与直接 exact-atom Hessian 在 80 位 Decimal 精度下吻合；
- `Delta(h=1)=-0.0411121735003746005241565860462171213338517962664354879397179010437800411723715<0`；
- 该例 rank 2、连通、非直和、非 thinning。

### 2x2 PSD rank-one 混合 Hessian

`derivation.md:45-64` 的混合 Hessian 正值复算为
`2 log(13/5)-18/13 = 0.5264075054394881075208408320628773151747177963679941736281798537631867438488894`
且严格大于 `46/117`。这只否定“PSD rank-one 方向之间交叉项非正，所以可
叠加”的证明捷径；它不是沿单一 PSD/NSD 方向的 `H''` 反例，也不否定 S-T。

## 4. 实际命令、退出码与分母

工作目录：

`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`

命令：

1. `C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\semidefinite_directions\verifications\fresh_semidefinite_check.py`
   - 第一次退出码：1。
   - 原因：验证脚本初稿把 repo 根目录层级算错，读到了 repo 外层路径；无数学断言失败。
2. 同一命令，修正脚本路径后重跑。
   - 退出码：0。
   - Python：3.12.14。
   - seed：无。
   - random draws：0。
   - failed assertions：0。

验证分母：

- 独立 n=4 families：1；
- 独立 n=4 kernel points：3；
- 独立 n=4 exact events：48；
- 独立 n=4 Schur identities：16；
- 作者 n=11 record checked：1；
- mixed-Hessian shortcut check：1；
- random draws：0；
- failed assertions：0。

## 5. 最终裁决

S-T twin-pair 受限子类定理通过本轮新上下文验缝：条件化闭包、二点熵分解、
Shepp-Olkin 引用方向、`-4(d^2-e^2)log2` 常数、rank-one 严格性、gap 符号、
以及 n=11 非退化证书均未发现关键缺口。

保留边界：一般 G-S 半正定方向问题仍为 INCOMPLETE；S-T 依赖固定余部与
twin 外耦合，不覆盖一般 PSD/NSD 方向，也不构成实 DPP 熵凹性的正 gap 反例。
