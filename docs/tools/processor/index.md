# PorosData-Processor 工具调用

## 快速开始

### 安装依赖

```bash
pip install porosdata-processor
```

### 基本使用

```python
from porosdata.processor import DataProcessor

# 初始化处理器
processor = DataProcessor()

# 处理结构化数据
clean_data = processor.process_dataset(raw_data)
print(f"处理完成，质量评分: {clean_data.quality_score}")
```

## API 参考

### DataProcessor 类

#### 初始化参数

```python
DataProcessor(
    domain='materials_science',  # 处理领域
    strict_mode=True,           # 严格模式：遇到错误时停止处理
    enable_validation=True,     # 启用数据验证
    parallel_workers=4          # 并行处理工作线程数
)
```

#### 主要方法

##### process_dataset(data, **options)

处理单个数据集

**参数:**
- `data` (dict/DataFrame): 输入数据集
- `**options`: 处理选项

**返回值:**
- `ProcessedData` 对象，包含处理后的数据和质量报告

##### process_batch(datasets, **options)

批量处理多个数据集

**参数:**
- `datasets` (list): 数据集列表
- `**options`: 批处理选项

**返回值:**
- `BatchProcessResult` 对象

##### validate_data_quality(data)

验证数据质量

**参数:**
- `data`: 待验证的数据

**返回值:**
- 质量评估报告字典

## 高级用法

### 自定义处理流水线

```python
from porosdata.processor import ProcessingPipeline
from porosdata.processor.steps import NormalizationStep, OutlierDetectionStep

# 创建自定义流水线
pipeline = ProcessingPipeline([
    NormalizationStep(method='zscore'),
    OutlierDetectionStep(algorithm='isolation_forest'),
    # 添加更多处理步骤...
])

# 配置流水线参数
pipeline.configure({
    'normalization': {'target_range': [0, 1]},
    'outlier_detection': {'contamination': 0.1}
})

# 执行处理
result = pipeline.execute(raw_data)
```

### 领域特定处理器

```python
from porosdata.processor.domains import MaterialScienceProcessor

# 材料科学专用处理器
processor = MaterialScienceProcessor()

# 处理材料性能数据
material_data = {
    'hardness': [450, 480, 520, 490, 'N/A', 550],
    'temperature': ['300°C', '400°C', '500°C', '室温', 'RT'],
    'composition': ['Fe-50, Cr-25', 'Fe50Cr25', 'Fe₅₀Cr₂₅']
}

processed = processor.process_material_properties(material_data)

# 自动处理：
# - 单位标准化 (300°C → 573.15K)
# - 格式统一化 (Fe-50, Cr-25 → {'Fe': 0.5, 'Cr': 0.25})
# - 异常值检测和处理
```

### 实时数据流处理

```python
from porosdata.processor.stream import StreamProcessor

# 创建流处理器
stream_processor = StreamProcessor(batch_size=100, window_size=1000)

# 处理实时数据流
@stream_processor.on_batch_ready
def handle_batch(batch_data):
    processed_batch = processor.process_batch(batch_data)
    save_to_database(processed_batch)

# 开始处理
stream_processor.start_processing(data_stream)
```

## 数据质量控制

### 质量评估指标

```python
from porosdata.processor.quality import QualityAssessor

assessor = QualityAssessor()

# 全面质量评估
quality_report = assessor.evaluate_comprehensive(data)

print("质量报告:")
print(f"- 完整性评分: {quality_report.completeness_score}")
print(f"- 准确性评分: {quality_report.accuracy_score}")
print(f"- 一致性评分: {quality_report.consistency_score}")
print(f"- 异常值比例: {quality_report.outlier_ratio}")

# 识别问题数据
issues = quality_report.identify_issues()
for issue in issues:
    print(f"问题类型: {issue.type}, 位置: {issue.location}, 严重程度: {issue.severity}")
```

### 自动修复策略

```python
from porosdata.processor.repair import AutoRepair

repair_engine = AutoRepair()

# 配置修复策略
repair_engine.set_strategy({
    'missing_values': 'interpolation',  # 缺失值：插值修复
    'outliers': 'winsorize',           # 异常值：Winsorize 处理
    'inconsistencies': 'domain_rules'  # 不一致：基于领域规则修复
})

# 执行自动修复
repaired_data = repair_engine.repair(data, quality_report)
```

## 性能优化

### 大数据集处理

```python
# 内存优化处理
processor.enable_memory_optimization()

# 分块处理大型数据集
for chunk in processor.process_large_dataset(
    large_dataset,
    chunk_size=10000,
    overlap=100
):
    process_chunk(chunk)
    # 中间结果保存或进一步处理
```

### 并行处理配置

```python
from porosdata.processor.parallel import ParallelProcessor

# 配置并行处理
parallel_processor = ParallelProcessor(
    num_workers=8,
    chunk_strategy='adaptive',  # 自适应分块
    load_balancing=True        # 负载均衡
)

# 执行并行处理
results = parallel_processor.process_parallel(datasets)
```

### 监控和诊断

```python
from porosdata.processor.monitor import PerformanceMonitor

monitor = PerformanceMonitor()

with monitor.track_performance():
    result = processor.process_dataset(large_data)

# 获取性能报告
perf_report = monitor.get_report()
print(f"处理时间: {perf_report.total_time}")
print(f"内存使用峰值: {perf_report.peak_memory}")
print(f"CPU 利用率: {perf_report.cpu_utilization}")
```

## 输出格式

### 标准输出结构

```python
{
    'data': processed_dataframe,
    'metadata': {
        'original_shape': (1000, 20),
        'processed_shape': (980, 20),
        'processing_steps': ['normalization', 'outlier_removal', 'validation'],
        'quality_metrics': {
            'completeness': 0.95,
            'accuracy': 0.92,
            'processing_time': 45.2
        }
    },
    'quality_report': {
        'warnings': [...],
        'errors': [...],
        'recommendations': [...]
    }
}
```

### 自定义输出处理器

```python
from porosdata.processor.output import HDF5OutputHandler

# 保存为 HDF5 格式
hdf5_handler = HDF5OutputHandler(
    filename='processed_data.h5',
    compression='gzip',
    chunk_size=1000
)

processor.set_output_handler(hdf5_handler)
result = processor.process_dataset(data)  # 自动保存到 HDF5 文件
```