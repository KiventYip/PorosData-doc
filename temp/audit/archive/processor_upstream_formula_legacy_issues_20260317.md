# Processor / 上游公式清洗遗留问题清单（Designer 视角）

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

## 基本信息

- 审计视角：`Designer` 包构建与交付视角
- 审计对象：
  - `data/processed`
  - `data/structured_data`
- 审计目的：
  - 识别哪些公式/材料式问题在 `Designer` 输入阶段已经存在
  - 区分“上游遗留问题”与“Designer 新引入问题”
  - 为 `Processor` / 上游清洗链路提供可执行修复清单
- 审计时间：`2026-03-17`

## 审计结论

从 `Designer` 的输入输出对照看，当前仍有一批**根因位于 `Processor` / 上游公式清洗**的遗留问题。

这些问题的共同特征是：

- 在 `data/processed` 中已经存在；
- `Designer` 当前最多只能做到“停止放大”或“保守保留”；
- 若不在上游修复，会继续以原文残留的形式进入 `full_text` / `multimodal` 产物，影响训练可读性、实体抽取和公式消费稳定性。

本轮审计未发现 `Designer` 在修复后继续新制造 `\Delta` 花括号损坏；但仍确认存在多类**上游坏公式原样遗留**问题。

## 审计方法

1. 对 `data/processed` 搜索典型坏公式模式；
2. 对 `data/structured_data` 搜索同类残留模式；
3. 对照 `Designer` 当前行为，区分：
   - `Processor` / 上游已损坏，`Designer` 原样保留；
   - `Processor` / 上游已损坏，`Designer` 做了止血但未根治；
   - `Designer` 自身新增损坏。

## 问题清单

### P1. 残缺的 LaTeX 环境被上游直接带入正文

- 问题类型：行内公式被错误转成 `\begin{array}...\end{array}`，且括号内容被拆坏
- 根因归属：`Processor` / 上游公式清洗
- 影响：
  - 公式不可可靠渲染
  - 语义本应是简单括号说明，实际变成残缺环境公式
  - 同一坏样本会同时污染 `full_text`、`multimodal`、JSONL

上游输入样本：

```146:146:data/processed/00001/mineru_2.1.10_output/00001/auto/00001_content_list.json
"text": "Fig. 3 compares the structure factors $S (q)$ of different amorphous $Z \\mathbf{r}$ -based alloys $\\begin{array} { r } { (q = 4 \\pi \\mathrm{sin} \\theta / \\lambda } \\end{array})$ is the absolute value of the scattering vector. ..."
```

当前交付样本：

```30:30:data/structured_data/full_text/00001/00001_structured.txt
<poros_paragraph>... $\begin{array} { r } { (q = 4 \pi \mathrm{sin} \theta / \lambda } \end{array})$ is the absolute value of the scattering vector. ...</poros_paragraph>
```

波及范围：

- `processed_data` 命中样本：`00001`
- `structured_data` 命中样本：`00001/full_text`、`00001/multimodal`

建议上游修复动作：

- 识别“简单括号说明被误转为 `array` 环境”的模式；
- 当 `\begin{array}` 内仅承载单个括号表达式时，优先恢复为普通行内公式：
  - 目标形态：`(q = 4 \pi \sin \theta / \lambda)`
- 对 `\begin{...}` / `\end{...}` 做环境成对与括号平衡检查，不安全时优先降级而不是强保留坏环境。

验收标准：

- `processed_data` 中不再出现 `\begin{array} ... \end{array})` 这类“环境+外挂右括号”结构；
- `structured_data` 中对应样本恢复为正常括号公式或安全降级文本。

### P2. `\Delta` 前缀合金式误识仍在上游存在

- 问题类型：`\Delta` 被并入材料式，形成 `\DeltaNi`、`\DeltaNb` 等伪元素串
- 根因归属：`Processor` / 上游公式清洗
- Designer 当前状态：
  - 已停止把这类输入改坏成 `<poros_chem>$Ni - Nb {- Y}}$</poros_chem>`
  - 但仍会**原样保留上游脏输入**

上游输入样本：

```113:115:data/processed/00001/mineru_2.1.10_output/00001/auto/00001_content_list.json
"text": "Most of the metallic glasses ... rapidly quenched $\\mathrm{\\DeltaNi - Nb {- Y}}$ alloys is reported. ..."
```

当前交付样本：

```21:21:data/structured_data/full_text/00001/00001_structured.txt
<poros_paragraph>... rapidly quenched $\mathrm{\DeltaNi - Nb {- Y}}$ alloys is reported. ...</poros_paragraph>
```

同类残留：

```25:25:data/structured_data/full_text/00001/00001_structured.txt
<poros_paragraph>... Amorphous <poros_equ>$\mathbf{Ni -}$</poros_equ> $\mathrm{\DeltaNb {- Y}}$ alloys were obtained ...</poros_paragraph>
```

风险：

- 材料式抽取会失败或不稳定；
- 训练视图中会保留不可解释 token；
- 后续若其他包继续做规则抽取，可能再次误判。

建议上游修复动作：

- 在公式/材料式清洗阶段区分：
  - 真实物理量：如 `\Delta T`、`\Delta G`
  - 被误并入合金串的伪前缀：如 `\DeltaNi`、`\DeltaNb`
- 对 `\mathrm{\DeltaNi - Nb {- Y}}` 之类输入做定向归一化，恢复为 `Ni-Nb-Y` 或 `Ni–Nb–Y`
- 修复时同时重建花括号与连字符，不允许仅删除 `\Delta` 前缀而留下残余花括号。

验收标准：

- `processed_data` 中不再出现 `\DeltaNi` / `\DeltaNb` 作为材料式前缀；
- `structured_data` 中对应位置恢复为正常材料式，而不是保留脏 token。

### P3. 截断的连字符材料式仍在上游存在

- 问题类型：材料式只保留到元素 + 连字符，后半段丢失，如 `$\mathbf{Ni -}$`、`$\mathrm{Zr -}$`
- 根因归属：`Processor` / 上游公式清洗
- Designer 当前状态：
  - 已避免把这类半截式误标为 `<poros_chem>`
  - 但仍只能原样保留为普通公式/普通文本

上游输入样本：

```126:126:data/processed/00001/mineru_2.1.10_output/00001/auto/00001_content_list.json
"text": "... Amorphous $\\mathbf{Ni -}$ $\\mathrm{\\DeltaNb {- Y}}$ alloys were obtained ..."
```

```266:266:data/processed/00013/mineru_2.1.10_output/00013/auto/00013_content_list.json
"text": "$T_{\\mathrm{c}}$ is observed. ... corresponding amorphous $\\mathrm{Zr -}$ Cu films ..."
```

```36:36:data/processed/00011/mineru_2.1.10_output/00011/auto/00011_content_list.json
"text": "Mechanical alloying produces $\\mathbf{Zr -}$ and $\\mathbf{M} \\mathbf{g}$ -based metallic glasses ..."
```

```110:110:data/processed/00020/mineru_2.1.10_output/00020/auto/00020_content_list.json
"text": "... Fig. 1 shows the DSC curves ... ($\\mathrm{Cu_60 -}$ $\\mathrm{Zr}_{30} \\mathrm{Ti}_{10})_{100 - x} \\mathrm{Sn}_{x}$ ..."
```

当前交付样本：

```25:25:data/structured_data/full_text/00001/00001_structured.txt
<poros_paragraph>... Amorphous <poros_equ>$\mathbf{Ni -}$</poros_equ> $\mathrm{\DeltaNb {- Y}}$ alloys were obtained ...</poros_paragraph>
```

```12:12:data/structured_data/full_text/00011/00011_structured.txt
<poros_paragraph>... Mechanical alloying produces <poros_equ>$\mathbf{Zr -}$</poros_equ> and <poros_equ>$\mathbf{M} \mathbf{g}$</poros_equ> -based metallic glasses ...</poros_paragraph>
```

波及范围：

- `processed_data` 明确命中样本：`00001`、`00011`、`00013`、`00020`
- `structured_data` 当前仍可见残留样本：`00001`、`00011`、`00020`

建议上游修复动作：

- 对 `元素 + 连字符` 且后续紧邻另一段材料式/元素片段的情况，做跨 token 合并；
- 修复 `Zr - Cu`、`Ni - Nb - Y`、`Cu_60 - Zr_30Ti_10` 这类被切断的材料式；
- 对无法安全合并的半截材料式，至少去除 LaTeX 包装并降级为普通文本，而不是保留“半个公式”。

验收标准：

- `processed_data` 中不再出现 `$\mathbf{Ni -}$`、`$\mathrm{Zr -}$` 这类半截材料式；
- `structured_data` 中不再出现以 `<poros_equ>` 或裸 `$...$` 形式残留的半截合金 token。

## 非问题项说明

以下 `\Delta` 相关表达**不应**作为上游坏公式修复目标误伤：

- `\Delta T`
- `\Delta G`
- `\Delta S`
- `\Delta T_{\mathrm{x}}`
- `\Delta T_{\mathrm{g}}`

这些属于正常物理量符号，在 `processed_data` 与 `structured_data` 中大量存在，不能用简单的“见 `\Delta` 就删”规则处理。

## 对 Designer 的影响判断

从 `Designer` 交付视角，这批遗留问题带来的影响主要是：

1. `content` 可读性下降  
2. `chemical_formulas` 与公式识别稳定性下降  
3. `multimodal` 图注/索引同步继承坏公式  
4. 下游训练与抽取会消费到不完整公式 token  

但这些问题的**主修复责任不应继续留在 `Designer` 包内**。  
`Designer` 当前应承担的是：

- 停止放大坏输入；
- 对不安全公式做保守降级；
- 在审计和交付清单中明确“这是上游遗留问题”。

## 建议转交给 Processor / 上游的修复任务

### U1. 修复残缺 LaTeX 环境

- 输入模式：`\begin{array} ... \end{array})`
- 目标：恢复为正常行内括号公式或安全降级文本

### U2. 修复 `\Delta` 并入材料式

- 输入模式：`\mathrm{\DeltaNi - Nb {- Y}}`
- 目标：恢复为 `Ni-Nb-Y` / `Ni–Nb–Y`

### U3. 修复截断的连字符材料式

- 输入模式：`$\mathbf{Ni -}$`、`$\mathrm{Zr -}$`
- 目标：跨片段合并为完整材料式，或降级为非公式纯文本

### U4. 为上游清洗增加公式安全校验

- 检查项：
  - 括号/花括号平衡
  - `\begin{...}` / `\end{...}` 成对
  - 连字符材料式是否只保留半段
  - `\Delta` 是否错误并入材料式

## 最终结论

从 `Designer` 包构建视角看，这批问题已经可以明确归类为：

- **不是 `Designer` 的建模策略问题**
- **不是当前 `Designer` 修复后新制造的问题**
- **而是 `Processor` / 上游公式清洗尚未完成闭环的遗留问题**

建议将本清单作为跨包修复输入，和 `docs/audit/designer_remediation_workitems_2026-03-17.md` 配套使用：

- `Designer` 清单负责“本包止血与输出契约”
- 本清单负责“上游根因修复与责任回传”
