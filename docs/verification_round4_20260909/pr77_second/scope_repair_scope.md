# PR77 文字范围修订增量审核范围

## 审核对象

本轮只审核 PR77 从

```text
8de8b0007f9374b7a5decb9b0a2f1c939fe897be
```

到

```text
2564e25a8b62a72992b9451988cd42e2d5a81834
```

之间的精确文字范围修订。此前独立二审报告保持原样，不在本轮改写或覆盖。

## 读取文件

本轮只读取并绑定以下文件：

- `scope_repair_input/README.md`
- `scope_repair_input/proof.md`
- `scope_repair.patch`
- `scope_repair_input_binding.json`

未读取 C1 首审、其他二审、C3 裁定、PR78、实时后继、私有交接、远程脚本或 `[excluded private directory]` 下任何材料。

## 绑定核对

`scope_repair_input_binding.json` 声明：

- 前一 head：`8de8b0007f9374b7a5decb9b0a2f1c939fe897be`
- 当前 head：`2564e25a8b62a72992b9451988cd42e2d5a81834`
- 未变文件：21 个
- 变更文件：`README.md`、`proof.md`
- patch SHA256：`80e037b25dd40a4f45c60b974b8b82f61e6b2a415420cf521b7c2dd9724ab46c`

我用机器重新计算的 SHA256 已写入 `scope_repair_source_binding.json`。重新计算结果与绑定中 `README.md`、`proof.md` 和 patch 的哈希一致。

## 审核边界

本轮不运行数学计算，不运行作者脚本，不复算行列式、对数区间、曲率阈值、协方差多项式或 Fisher 常数。

数值单元仍等待独立 C2 原始证据。作者输出摘要中的 `PASS` 字段仍不构成独立证书。

本轮只判断两类文字修订是否正确界定：

1. `proof.md` Section 9 的有限块二阶论证、真熵率值恒等式和仍缺失的导数桥梁；
2. `README.md` 对作者 JSON 输出摘要证据地位的说明。

