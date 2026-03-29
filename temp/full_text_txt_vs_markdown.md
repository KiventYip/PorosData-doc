# full_text 产物：TXT 与 Markdown 格式说明

- doc_type: design_reference
- status: reference_only
- updated_at: 2026-03-18 09:37:49
- current_contract_note: if this document mentions historical JSONL or prior audit structure, use `docs/ai_ready_and_datamining_designer.md`, `docs/usage_guide.md`, and current `data/structured/*_structured.json` as the active contract.



**适用文件**：`data/structured/full_text/{doc_id}/{doc_id}_structured.txt`  
**当前内容**：与 JSONL 中 `content` 一致，为**带 Poros 标签的完整正文**（含 `<poros_doc>`、`<poros_paragraph>`、`<poros_equ>`、`<poros_chem>`、`<poros_asset>` 等），外加简短头部（Document ID、分隔线）。用途：人工查看、审计脚本校验。

---

## 一、能否转换为 Markdown？

**可以**，但有两种不同含义：

1. **仅改扩展名**  
   内容不变，仅把 `00001_structured.txt` 存为 `00001_structured.md`。Markdown 允许内嵌 XML 式标签，多数渲染器会当作文本显示。  
   - 优点：不丢信息，审计逻辑只需改为读 `.md` 或同时接受 `.txt`/`.md`。  
   - 缺点：对人眼可读性几乎无提升。

2. **真正转为 Markdown 语义**  
   把 Poros 标签映射为 Markdown 结构，例如：`<poros_title>` → `## 标题`，`<poros_paragraph>` → 段落（空行分隔），`<poros_equ>$...$</poros_equ>` → 保留 `$...$` 行内公式，`<poros_asset>Fig. 1</poros_asset>` → *Fig. 1* 或链接。  
   - 优点：在编辑器/GitHub 中更易读，标题层级、段落分明。  
   - 缺点：**不再保留完整 Poros 标签树**，若用此文件做 Schema/LaTeX/EOS 校验，需继续使用“未转换”的原文（即当前 .txt 或 JSONL 的 content）。

因此：**“能转”** 指技术上可以生成一份 Markdown；若要保持**与现有审计与交付约定一致**，需要保留一份**未转换的、带完整 Poros 标签的**正文（即当前 .txt 或 JSONL 中的 content）。

---

## 二、若改为仅输出 Markdown 会有什么影响？

- **审计脚本**  
  `scripts/audit_structured_data.py` 当前依赖 `{doc_id}_structured.txt`，读取后去掉头部，对**剩余内容**做 Schema、LaTeX、EOS、根标签校验。  
  - 若**用“真正转换”后的 Markdown**（无 Poros 标签）**替代** .txt：校验会失败或无法进行（没有标签可校验）。  
  - 若**仅把同一份 Poros 内容改成 .md 扩展名**：需在脚本中改为从 `_structured.md` 读取（或同时支持 .txt/.md），并保持“去掉头部、只校验正文”的逻辑，则无功能影响。

- **文档与约定**  
  `docs/ai_ready_and_datamining_designer.md` 和交付验收报告约定 full_text 产物包含 `{doc_id}_structured.txt`（带 Poros 标签的完整正文）。  
  - 若改为**只产出 .md 且为“真正转换”**：与当前约定不一致，且无法用同一文件既做人工友好展示又做 Poros 校验。  
  - 若**保留 .txt 再额外增加 .md**：约定仍满足，无负面影响。

- **下游**  
  任何依赖“带 Poros 标签的全文”的流程（训练、抽取、质检）都应使用 JSONL 的 `content` 或与之一致的 .txt。若只提供“转成 Markdown 语义”的版本，下游要么无法做基于标签的解析，要么必须再依赖 JSONL，导致 .md 仅为展示用。

**结论**：  
- **用“真正转换”的 .md 完全取代 .txt**：会破坏审计与现有约定，不推荐。  
- **用“同一 Poros 内容”仅改扩展名为 .md**：可行，但需改审计脚本并更新文档中的文件名约定，收益主要是扩展名习惯，内容可读性不变。  
- **在保留 .txt 的前提下额外增加 .md（可选）**：无负面影响，可兼顾“约定与审计”与“人工阅读体验”。

---

## 三、保持 TXT 好还是改为 Markdown 好？

| 维度 | 保持 .txt（当前） | 改为仅 .md（真正转换） | 保留 .txt + 可选 .md |
|------|-------------------|------------------------|----------------------|
| 与交付约定一致 | ✅ 一致 | ❌ 约定要求“带 Poros 标签的正文” | ✅ 一致 |
| 审计脚本 | ✅ 无需改 | ❌ 无法对 .md 做 Poros/LaTeX 校验 | ✅ 无需改（.md 仅附加） |
| 人工查看 | 一般（需习惯标签） | 较好（标题、段落清晰） | 较好（用 .md 查看） |
| 单一事实来源 | ✅ .txt 与 JSONL content 一致 | ❌ 需以 JSONL 为准 | ✅ .txt 仍为准，.md 为导出视图 |
| 实现成本 | 无 | 需转换逻辑 + 改审计/约定 | 需转换逻辑，仅多写一个文件 |

**建议**：

- **主流程继续使用并保留 .txt**  
  - 作为“带 Poros 标签的完整正文”的**唯一与 JSONL content 一致的副本**，用于审计、约定符合性及所有依赖标签的下游。
- **若希望更好的人工可读性**  
  - **在保留 .txt 的前提下**，增加**可选的** Markdown 导出：由同一份 Poros 正文生成 `{doc_id}_structured.md`（标题→`##`、段落空行、公式保留 `$...$`、图引用用强调或链接），供人在编辑器/GitHub 中阅读。  
  - 不把 .md 纳入交付验收必选项，审计与文档约定仍只要求 .txt（及 JSONL）。

**总结**：  
- **可以**从当前 .txt 转出一份 Markdown（尤其是“真正转换”为 MD 语义时），但**不应**用该 Markdown **替代** .txt 作为主产物。  
- **保持 .txt 作为主格式**，必要时**额外**提供 .md 作为阅读视图，既能满足约定与审计，又能改善可读性且无副作用。