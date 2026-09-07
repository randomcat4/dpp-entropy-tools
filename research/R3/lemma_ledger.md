# 引理依赖账

## LEMMA-1：精确事件的 L-ensemble 公式

- 陈述：严格正收缩 `K` 满足
  `p_K(S)=det(I-K)det([K(I-K)^{-1}]_S)`。
- 状态：`KNOWN`，但 R3 必须给自包含推导。
- 相对冻结命题：`STRICTLY_WEAKER`。
- 条件：有限维、`0<K<I`；边界延拓未纳入 v1。

## LEMMA-2：分组子空间谱分解

- 陈述：`K=A+U(C-diag(a))U^T` 在各组常数向量张成空间上等同于
  `C`，在第 `g` 组和为零子空间上等同于 `a_g I`。
- 状态：`PROVED_HERE`（待独立审计）。
- 相对冻结命题：`STRICTLY_WEAKER`。

## LEMMA-3：按计数的主子式公式

- 陈述：对 `L=K(I-K)^{-1}`，
  `det L_S=prod_g ell_g^{c_g} det(I+B D_c)`。
- 状态：`PROVED_HERE`（待独立审计）。
- 相对冻结命题：`STRICTLY_WEAKER`。
- 依赖：矩阵行列式引理；所有 `ell_g>0`。

## LEMMA-4：T2 分块损失界

- 陈述：见 T2 固定 commit `27dda692856da210e23ae74ce267b813d3221822`。
- 状态：`OPEN`（对 R3 尚未独立核对）。
- 相对主问题：`STRICTLY_WEAKER`，只给误差包围，不给实反例种子。
