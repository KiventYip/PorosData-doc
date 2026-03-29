# PorosData-Processor 开发者指南

## 🏗️ 核心架构

### 处理流程

```
原始文本
 → _pre_shield_processing  (控制字符清理 + local_text_compression)
 → Shield.protect           (LaTeX / 代码 / 引用 → 占位符)
 → Pipeline.execute          (按 Config.default_pipeline 顺序执行步骤)
 → Shield.restore           (占位符 → 原始内容)
 → _clean_formula_trailing_spaces
 → _post_shield_processing  (最终空白清理)
 → LLM-Ready 文本
```

### 1. TextCleaner — 主接口层

```python
class TextCleaner:
    def __init__(self, pipeline=None, config=None, evaluator=None, sentinel=None, strict_mode=False):
        ...

    def clean(self, text: str, eval_mode: bool = False) -> Union[str, Dict[str, Any]]:
        # 1. _pre_shield_processing (控制字符 + local_text_compression)
        # 2. Shield.protect
        # 3. Pipeline.execute (在已保护文本上)
        # 4. Shield.restore
        # 5. _post_shield_processing
        # 6. 评估分析（eval_mode=True 时）
        ...

    @classmethod
    def with_tokenizer_evaluation(cls, tokenizer_model="gpt2", ...): ...
    @classmethod
    def with_quality_assurance(cls, tokenizer_model="gpt2", ...): ...
```

工厂方法说明：
- `with_tokenizer_evaluation()`: 创建带 `TokenizerEvaluator` 的实例
- `with_quality_assurance()`: 创建带 `TokenizerEvaluator` + `DataSentinel` 的实例，启用质量审计

### 2. Shield — LaTeX 保护系统

```python
class Shield:
    PROTECTION_ORDER = [
        "fenced_code_blocks",    # 代码块 (最高优先级)
        "inline_code",           # 行内代码
        "latex_environments",    # \begin{env}...\end{env}
        "latex_display_math",    # $$...$$ / \[...\]
        "latex_inline_math",     # $...$
        "latex_commands"         # \command{...}
    ]
```

熔断阈值：如果保护后文本长度 < 原始长度的 20%，说明出现异常，抛出 ValueError。

### 3. Pipeline — 处理管线

Pipeline 接受步骤名列表，通过 `PluginRegistry` 解析为可调用函数。
内置步骤定义在 `steps.py` 中，通过 `@PluginRegistry.register(name)` 注册。

默认 Pipeline 顺序（见 `Config.default_pipeline`）：

1. `unicode_normalization` — NFC 规范化
2. `scientific_ocr_repair` — P0/P1 级 OCR 修复
3. `term_consistency_mapping` — P2 级术语一致性
4. `patterns_cleaning` — 通用正则清理
5. `citation_rules` — 引用格式标准化
6. `document_numbering_rules` — 编号规范化
7. `greek_to_latex` — 希腊字母转换
8. `normalize_whitespace` — 空白规范化
9. `remove_extra_spaces` — 多余空格清理

注意：`local_text_compression` 不在 Pipeline 内，而是在 `TextCleaner._pre_shield_processing` 中执行（需要访问原始 `$...$`）。

### 4. DataSentinel — 质量保障系统（可选）

仅在使用 `TextCleaner.with_quality_assurance()` 工厂方法时激活。

```python
class DataSentinel:
    def audit_processing_result(self, original, processed, shield, compression_rate, step_name):
        # 影子校验 - 完整性验证
        # 边界自愈 - 损坏检测与修复
        # 结构守恒 - 公式数量验证
        # 压缩监控 - Token 效率预警
        # 隔离处理 - 失败案例保存到 quarantine/
```

---

## 🚀 性能优化

### Streaming Engine

基于 `ijson` 实现 O(1) 空间复杂度的 JSON 流式处理（由标准批处理入口内部调用的 `run_processor.py` 实现）：

```python
items = ijson.items(input_file, 'item')  # 逐条解析，不加载整个文件
```

### 多进程架构

- **ProcessPoolExecutor**: CPU 密集型并行化
- **进程数计算**: `max(1, min(cpu_count, memory_based_workers, 32))`
- **超时保护**: 单文档 120s 超时，防止阻塞整个批次

### 缓存策略

```python
_tokenizer_cache = weakref.WeakValueDictionary()  # 进程级 Tokenizer 缓存
_text_cleaner_cache = weakref.WeakValueDictionary()
```

---

## 🔧 扩展机制

### 注册自定义步骤

```python
from porosdata_processor.plugin_system import PluginRegistry

@PluginRegistry.register("custom_cleaner")
def custom_cleaner(text: str) -> str:
    return text.replace('old_pattern', 'new_pattern')
```

注册后即可在 Pipeline 中使用：

```python
cleaner = TextCleaner(pipeline=[
    "unicode_normalization",
    "custom_cleaner",
    "patterns_cleaning"
])
```

### 自定义术语映射

```python
from porosdata_processor import TermConsistencyEngine

engine = TermConsistencyEngine()
engine.add_mapping(r'\bshortrange\b', lambda m: 'short-range', 'P1')
```

---

## 📊 性能基准

| 指标 | 说明 |
|------|------|
| 内存 | O(1)（流式处理） |
| 文件大小 | 支持 TB 级 |
| 处理速度 | 278.5 items/s（多进程） |
| Tokenizer 超时 | 120s |

---

## 🔒 安全特性

- **Shield 系统**: 多层内容保护，确保 LaTeX 不被意外修改
- **隔离区机制**: 质量保障模式下，失败案例保存到 `quarantine/`
- **回滚机制**: LaTeX 结构验证失败时自动回滚到原始内容
- **幂等性**: 所有 OCR 修复满足 `f(f(x)) = f(x)`

---

## 🐛 故障排除

| 错误 | 解决方案 |
|------|----------|
| `ijson` 缺失 | `pip install ijson` |
| Token 加载超时 | 检查网络或使用本地模型路径 |
| 内存不足 | 减少 `--max-workers` 或增加 `--memory-limit` |
| 公式保护失败 | 检查 LaTeX 语法正确性 |
