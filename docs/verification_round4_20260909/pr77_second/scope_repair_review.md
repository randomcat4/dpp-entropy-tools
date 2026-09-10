# PR77 文字范围修订增量审核

## 结论

本轮文字范围修订是正确的。它没有试图改写数学证明本体，也没有把数值证据提前升级为独立接受；它只把两个原先容易越界的表述收窄到应有范围。

具体说：

- `proof.md` Section 9 现在明确是“固定有限块二阶”论证。有限块恒等式和有限块二阶结论可以接受。
- 真熵率层面只保留值恒等式，并明确说明这一步不能推出导数层面的极限交换。
- 真熵率导数桥梁被明确标为仍未建立、仍然 `INCOMPLETE`。
- `README.md` 现在明确说明提交的 `output/*.json` 是作者策划过的摘要，不是各 checker 的完整原始输出，也不是独立证书。

此前二审报告中的核心保留仍然有效：中点数值间隙、三点曲率阈值、Fisher 协方差多项式和相关精确常数仍等待 C2 原始证据；本轮修订没有、也不应当解决这些数值单元。

## 绑定与补丁核对

`scope_repair_input_binding.json:1`-`20` 声明当前 head 为 `2564e25a8b62a72992b9451988cd42e2d5a81834`，前一 head 为 `8de8b0007f9374b7a5decb9b0a2f1c939fe897be`，仅 `README.md` 和 `proof.md` 改动，其余 21 个文件未变。

我重新计算了本轮四个读取文件的 SHA256，并写入 `scope_repair_source_binding.json`。结果与绑定声明一致。因此本轮可以按“两处文字范围修订”处理。

## Section 9 修订审核

状态：CORRECT。

patch 将标题从

```text
Beam-splitter comparison at second order
```

改为

```text
Beam-splitter comparison: finite-block second order
```

见 `scope_repair.patch:7`-`8`，修订后正文见 `scope_repair_input/proof.md:540`。

新的 Section 9 先固定 `n` 个原始格点的有限块，定义 `Q_{u,n}`、`I_out,n` 和 `E_occ,n`，再写有限块值恒等式

```text
2H_n(t_*)-H_n(t_*-u)-H_n(t_*+u)
 =I_out,n(u)+E_occ,n(u).
```

见 `scope_repair_input/proof.md:548`-`553`。这是正确的有限块熵分解：输出两边缘都是 `t_*` 的 DPP，`I_out,n` 是输出占据变量的经典互信息，剩余项就是占据熵增益。

修订文本随后说，除以 `n` 后取平稳熵率极限只给出对应的值恒等式，但“不证明可以对这些极限求导”，见 `scope_repair_input/proof.md:555`。这个限定正是此前缺口所在，表述正确。

有限块二阶部分也被正确限定。层符号共轭使每个固定有限块的完整占据事件关于 `u` 为偶函数；在 `u=0` 严格正性下，

```text
Q_{u,n}-Q_{0,n}=O_n(u^2),
I_out,n(u)=O_n(u^4).
```

见 `scope_repair_input/proof.md:557`-`562`。这里下标 `n` 明确允许常数依赖块长，因此没有暗中给出统一体积极限余项。于是有限块二阶恒等式

```text
I_out,n''(0)=0,
E_occ,n''(0)=-2H_n''(t_*)
```

见 `scope_repair_input/proof.md:564`-`569`，是可接受的。

最关键的是，修订文本明确说真熵率导数版本仍需要“体积一致四阶余项”或“双层输出过程的解析响应桥梁”，且该桥梁本节没有建立；这些真熵率导数断言仍为 `INCOMPLETE`，也不作为 Sections 6-8 中点和点曲率证书的前提，见 `scope_repair_input/proof.md:571`。这正确修复了原先把有限块二阶直觉过快上推到真熵率导数层面的风险。

## README 证据地位说明审核

状态：CORRECT。

`README.md` 新增 “Evidence packaging clarification”，见 `scope_repair_input/README.md:69`-`73`。该段明确说明：

- 已提交的 `output/*.json` 是“缩略、策划过的作者摘要”；
- 它们不是每个 checker 字面输出的完整 JSON；
- `PASS` 字段不是独立证书；
- 中点和点曲率程序可输出包含原始区间和 tail 的 `.full.json`，但作者快照未包含；
- pair-Fisher 摘要使用展示多项式，而不是 checker 的系数列表 schema；
- run record 不替代源文件/输出哈希或原始区间证据；
- 独立重建必须补足这些 artifact，有限数值声明才能被外部接受。

这与静态代码审核中发现的 ledger/schema 问题一致，也正确保留了 C2 数值审核的必要性。

README 同时新增说明：Section 9 只限于固定有限块；真熵率值恒等式保留，但真熵率导数 passage 仍未完成，且不是中点或点曲率证书的前提。见 `scope_repair_input/README.md:73`。该摘要与修订后的 `proof.md:548`-`571` 一致。

## 剩余状态

本轮修订没有引入新的数学越界主张，也没有消除原二审中需要 C2 的数值证据缺口。

仍然不能独立接受的内容包括：

- `h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2 > 1/10000` 的深度 18 有向对数/行列式数值间隙；
- `h''(1/2)<-1/2500`、`h''(1)<-1/1000`、`h''(3/2)<-1/500` 的三点真熵率曲率阈值；
- pair-Fisher 协方差多项式和 `16/286141` 定量下界；
- 整个区间 `1/2<=|t|<=3/2` 的曲率负号；
- Section 9 的真熵率导数桥梁。

这些保留并不是本轮修订失败；它们是本轮修订正确保留下来的边界。

## 最小后续要求

若要把有限数值声明从作者证明推进到外部接受，仍需 C2 提供完整原始证据包：完整 `.full.json`、原始区间、tail、有向舍入记录、源/输出哈希，以及能对应冻结命令和冻结输出的 provenance。

若要推进 Section 9 的真熵率二阶断言，需要新增双层输出过程的统一解析响应或体积一致四阶余项；当前修订已正确声明这一步不存在。

