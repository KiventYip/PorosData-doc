# OCR 噪音分布审计报告

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

## 1. 概述

本报告对 MinerU PDF 转 JSON 输出进行 OCR 噪音差异化对齐审计，数据源为 `data/raw` 下的原始 `*_content_list.json`。审计范围覆盖五类 OCR 典型噪音，并给出经脚本核实的量化统计。

### 1.1 数据源与核查方式

| 项目 | 说明 |
|------|------|
| **Structured Data** | `docs/examples_demo/mineru_processed_example.json`（处理后示例） |
| **Original OCR** | `data/raw/{doc_id}/mineru_2.1.10_output/.../content_list.json` |
| **核查脚本** | `scripts/ocr_audit_stats.py`（可复现统计） |
| **样本文档** | 00001（金属玻璃综述）、00004（Pd-Ni-P 薄膜）、00005 |

### 1.2 核查统计摘要（脚本输出）

以下数据由 `python scripts/ocr_audit_stats.py` 于审计时运行得到：

| 错误类别 | 模式标识 | 00001 次数 | 00004 次数 | 00005 次数 | 合计 |
|----------|----------|------------|------------|------------|------|
| 术语漂移 (10-ray LaTeX) | `\mathbf{10}`-ray | 7 | 0 | 0 | 7 |
| 术语漂移 (10-ray 纯文) | 10-ray | 4 | 0 | 0 | 4 |
| 术语漂移 (B.V.) | B.5. | 1 | 0 | 0 | 1 |
| 符号损坏 (©) | `$©$` | 1 | 0 | 0 | 1 |
| 幻觉 (\Au) | `\mathrm{\Au}` | 1 | 0 | 0 | 1 |
| 幻觉 (Δ) | `\mathrm{\Delta` | 5 | 0 | 0 | 5 |
| 幻觉 (\K) | `\mathrm{\K}` | 3 | 0 | 0 | 3 |
| 换行噪音 | shortrange | 1 | 0 | 0 | 1 |
| 间隙 (单位/字母) | `\mathrm{X y}` 等 | 80 | 0 | 0 | 80 |
| 间隙 (下标数字) | `_{8 0}` 等 | 86 | 0 | 0 | 86 |
| 间隙 (公式数字) | `1 0^5` 等 | 21 | 20 | 0 | 41 |
| 间隙 (nm/mm/GPa) | 常见单位 | 18 | 0 | 0 | 18 |

---

## 2. 五类 OCR 噪音清单

### 2.1 间隙检查 (Space Errors)

**错误类型**：公式/单位中数字、字母被拆散，出现多余空格。

**典型样本**

| Structured（正确/期望） | Original（OCR 输出） |
|------------------------|----------------------|
| `$1\mathrm{nm}$` | `$1 \mathrm{n m}$` |
| `$10^{5}$–$10^{6} \mathrm{K/s}$` | `$1 0^{5} – 1 0^{6} \mathrm{\bar{K} / s}$` |
| `$\mathrm{Au}_{80}\mathrm{Si}_{20}$` | `$\mathrm{\Au}_{8 0} \mathrm{S i}_{2 0}$` |
| `$\geqslant 2\mathrm{GPa})$` | `$\geqslant 2 \mathrm{G P a} )$` |
| `$10\mu\mathrm{m}$` | `$1 0 \mu \mathrm{m}$` |
| `$Z\mathbf{r}-$` | `$Z \mathbf{r} -$` |

**发生频率评估**：**High**（00001 中约 185+ 次相关模式）

**自动修复规则建议**

```regex
# 1. 公式内数字间空格：1 0 → 10（限定 $...$ 内）
(?<=\$)([0-9])\s+([0-9])

# 2. 单位内空格：\mathrm{ X } → \mathrm{X}
\\mathrm\s*\{\s*([A-Za-z])\s+([A-Za-z])\s*\}

# 3. 下标数字空格：_{8 0} → _{80}
_\{\s*([0-9])\s+([0-9])\s*\}
```

---

### 2.2 幻觉指令 (Hallucination)

**错误类型**：LaTeX 中出现原文不存在的命令或符号。

**典型样本**

| Structured | Original | 说明 |
|------------|----------|------|
| `$\mathbf{X}$-ray` | `$\mathbf{10}$-ray` | X 被识别为 10 |
| `$\mathrm{Au}$` | `$\mathrm{\Au}$` | `\Au` 非标准 LaTeX |
| Ni–Nb–Y | `$\mathrm{\Delta Nb{-Y}}$` | Ni 被识别为 Δ |
| `$\mathrm{K}$` | `$\mathrm{\K}$` | `\K` 不存在 |

**发生频率评估**：**High**（00001：\mathbf{10} 7 次，\mathrm{\Delta 5 次，\mathrm{\K} 3 次）

**自动修复规则建议**

```regex
# 1. 10-ray → X-ray（射线衍射语境）
\$\\mathbf\{10\}\$\s*-ray  →  $\mathbf{X}$-ray

# 2. \Au → Au
\\mathrm\{\\Au\}  →  \mathrm{Au}

# 3. \Delta Nb → Ni-Nb（需上下文约束）
\\mathrm\{\\Delta\s*Nb  →  \mathrm{Ni-Nb

# 4. \K → K
\\mathrm\{\\K\}  →  \mathrm{K}
```

---

### 2.3 术语一致性 (Term Drift)

**错误类型**：系统性识别错误，字母/数字混淆或缩写误识。

**典型样本**

| 正确术语 | OCR 输出 | 出现位置 |
|----------|----------|----------|
| X-ray | **10-ray** | 00001 Abstract、正文、Conclusion |
| X-ray diffraction | 10-ray diffraction | 全文多处 |
| Ni–Nb–Y | ΔNb–Y | 合金成分描述 |
| short-range | shortrange | Conclusion |
| B.V. | B.5. | 版权声明 |

**发生频率评估**：**High**（10-ray：LaTeX 7 次 + 纯文 4 次；B.5. 1 次）

**自动修复规则建议**

```regex
# 1. 10-ray → X-ray
\b10-ray\b  →  X-ray

# 2. shortrange → short-range
\bshortrange\b  →  short-range

# 3. B.5. → B.V.（版权语境）
B\.5\.  →  B.V.
```

---

### 2.4 符号损坏 (Symbol Corruption)

**错误类型**：公式内混入非数学符号、命令错误、括号错位等。

**典型样本**

| Structured | Original | 问题 |
|------------|----------|------|
| © 2007 Elsevier B.V. | `$©$ 2007 Elsevier B.5.` | © 在公式内、B.5. |
| — | `$\mathrm{\bar{3}}$` | 673 中 7 被误为上划线 |
| — | `$T_{1}=864\ :\mathrm{K}$` | 多余 `\ :` |

**发生频率评估**：**Medium**（00001：`$©$` 1 次，`\mathrm{\K}` 3 次）

**自动修复规则建议**

```regex
# 1. 版权符号移出公式
\$[©®™]\$  →  直接保留符号

# 2. 多余冒号
\\s*:\\s*\\mathrm\{  →   \mathrm{
```

---

### 2.5 换行噪音 (Line-break Noise)

**错误类型**：段落合并后连字符丢失、单词粘连或截断。

**典型样本**

| 正确形式 | OCR 输出 | 原因 |
|----------|----------|------|
| short-range | shortrange | 行末 short- 与 range 合并丢失连字符 |
| supercooled | super cooled | 换行导致多余空格（本文较少） |

**发生频率评估**：**Low**（00001：shortrange 1 次）

**自动修复规则建议**

```regex
# 常见科学术语连字符恢复
\bshortrange\b  →  short-range
\blowerrange\b  →  lower-range
\bhighresolution\b  →  high-resolution
```

---

## 3. 修复优先级建议

| 优先级 | 错误类型 | 建议措施 |
|--------|----------|----------|
| **P0** | 10-ray → X-ray | 在 text_cleaner 或专用 step 中增加术语替换 |
| **P0** | 公式内数字/单位空格 | Shield 保护下对 `$...$` 内做空间压缩 |
| **P1** | \Au、Δ→Ni、\K | 增加 LaTeX 命令修正 step |
| **P1** | shortrange 等 | 加入 patterns 术语修正表 |
| **P2** | ©、`\ :` 等 | 后处理规则 |

---

## 4. 附录

### 4.1 核查脚本说明

运行以下命令可复现本报告中的统计：

```bash
python scripts/ocr_audit_stats.py
```

输出 JSON 包含 `counts`（各模式总次数）与 `doc_stats`（每篇文档分项统计）。

### 4.2 数据说明

- **00001**：金属玻璃综述（Mattern, 2007），OCR 噪音最集中，为本报告主要样本。
- **00004**：Pd-Ni-P 薄膜论文，原始 OCR 中 X-ray 正确，主要是公式内数字空格（约 20 处）。
- **00005**：未检出上述五类典型模式。

### 4.3 版本与数据时间

- 报告生成：基于 2025-03 审计
- MinerU 输出：`mineru_2.1.10_output`
- 数据路径：`data/raw/`
