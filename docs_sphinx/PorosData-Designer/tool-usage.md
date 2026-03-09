# PorosData-Designer 工具调用

## 快速开始

### 安装依赖

```bash
pip install porosdata-designer
```

### 基本使用

```python
from porosdata.designer import ExperimentDesigner

# 初始化设计器
designer = ExperimentDesigner()

# 基于现有数据进行实验设计
design_result = designer.design_experiments(
    existing_data=training_data,
    target_property='hardness',
    num_experiments=20
)

print(f"推荐实验方案: {design_result.experiments}")
```

## API 参考

### ExperimentDesigner 类

| 方法 | 功能描述 | 参数 | 返回值 |
|------|----------|------|--------|
| `design_experiments()` | 设计新的实验方案 | `existing_data`, `target_property`, `**options` | `DesignResult` 对象 |
| `optimize_design_space()` | 优化实验设计空间 | `parameters`, `constraints`, `objectives` | 优化后的设计空间配置 |
| `evaluate_design_quality()` | 评估设计方案的质量 | `design`, `validation_data` | 质量评估指标字典 |

::: tip 详细参数说明
有关完整的API参数列表和类型定义，请参考 :doc:`../api-reference`。
:::

## 核心功能详解

### 数据设计逻辑：从材料特性到LLM指令

PorosData-Designer 的核心创新在于将传统材料科学数据转换为适合大语言模型理解的指令格式。以下是核心的数据转换流程：

#### 1. 材料特性向量化表示

```python
from porosdata.designer.representation import MaterialRepresentation

# 创建材料表示器
representer = MaterialRepresentation()

# 处理晶体结构数据
crystal_data = {
    'formula': 'TiO2',
    'crystal_system': 'tetragonal',
    'lattice_parameters': {'a': 4.593, 'c': 2.959},  # Å
    'space_group': 'P4₂/mnm',
    'band_gap': 3.2  # eV
}

# 转换为结构化表示
structured_repr = representer.structure_material(crystal_data)
print(structured_repr)
# 输出: {
#   'composition': {'Ti': 0.33, 'O': 0.67},
#   'structure': {'type': 'rutile', 'bandgap_ev': 3.2},
#   'properties': {'lattice_a': 4.593, 'lattice_c': 2.959}
# }
```

#### 2. 指令模板生成引擎

```python
from porosdata.designer.templates import InstructionTemplateEngine

# 初始化指令模板引擎
template_engine = InstructionTemplateEngine()

# 为不同任务类型生成指令模板
templates = template_engine.generate_templates_for_domain('materials_science')

# 示例：性能预测模板
prediction_template = {
    'task': 'property_prediction',
    'instruction': '基于材料{formula}的晶体结构和成分信息，预测其{target_property}的数值范围。',
    'input_format': '材料: {formula}\n晶体结构: {structure}\n关键参数: {parameters}',
    'output_format': '预测值: {predicted_value} {unit}\n置信区间: {confidence_interval}\n推理依据: {reasoning}',
    'constraints': ['必须基于已知物理定律', '提供不确定性估计']
}
```

#### 3. 推理链构建算法

```python
from porosdata.designer.reasoning import ReasoningChainBuilder

# 构建推理链
reasoning_builder = ReasoningChainBuilder()

# 为复杂材料问题创建推理步骤
reasoning_chain = reasoning_builder.build_chain(
    material_data=structured_repr,
    target_property='band_gap',
    reasoning_type='physics_based'
)

# 生成的推理链示例:
# 步骤1: 识别晶体结构类型 (rutile TiO2 → 宽带隙半导体)
# 步骤2: 考虑原子轨道重叠 (Ti 3d - O 2p 相互作用)
# 步骤3: 应用经验公式 (bandgap ≈ f(晶格参数, 离子性))
# 结论: 预测带隙为3.0-3.4 eV
```

#### 4. JSONL数据集格式转换

```python
from porosdata.designer.formats import JSONLDatasetFormatter

# 初始化格式化器
formatter = JSONLDatasetFormatter()

# 转换为标准JSONL格式
jsonl_dataset = formatter.convert_to_instruction_format(
    material_dataset=processed_data,
    instruction_template=prediction_template,
    include_metadata=True,
    add_reasoning_steps=True
)

# 生成的JSONL行示例:
sample_entry = {
    "instruction": "预测TiO2的金红石晶型的带隙值。",
    "input": "晶体结构: 金红石型四方晶系\\n晶格参数: a=4.593Å, c=2.959Å\\n空间群: P4₂/mnm\\n成分: TiO₂",
    "output": "TiO₂金红石晶型的带隙预测为3.0-3.2 eV。\\n\\n推理过程:\\n1. 金红石TiO₂是典型的宽带隙氧化物半导体\\n2. 晶格参数表明较强的Ti-O键\\n3. 基于DFT计算和实验数据，带隙通常在3.0-3.3 eV范围\\n4. 考虑量子限制效应，预测值为3.0-3.2 eV",
    "metadata": {
        "source": "materials_project_database",
        "confidence": 0.92,
        "domain": "electronic_materials",
        "reasoning_depth": 3
    }
}
```

::: note 算法实现细节
贝叶斯优化、多目标优化等底层算法实现已转移至 :doc:`research-insights` 的技术深度模块。
:::

## 高级用法

### 多目标实验设计

```python
from porosdata.designer.multiobjective import MultiObjectiveDesigner

# 创建多目标设计器
mo_designer = MultiObjectiveDesigner(
    objectives=['hardness', 'ductility', 'cost'],
    weights=[0.4, 0.4, 0.2]
)

# 定义参数空间
parameter_space = {
    'temperature': {'min': 800, 'max': 1200, 'unit': '°C'},
    'time': {'min': 1, 'max': 24, 'unit': 'hours'},
    'pressure': {'min': 1, 'max': 100, 'unit': 'MPa'},
    'alloy_composition': {
        'Fe': {'min': 0.5, 'max': 0.9},
        'Cr': {'min': 0.05, 'max': 0.25},
        'Ni': {'min': 0.05, 'max': 0.25}
    }
}

# 执行多目标优化
pareto_front = mo_designer.find_pareto_optimal_designs(
    parameter_space=parameter_space,
    existing_data=historical_data,
    num_candidates=50
)

# 选择最优方案
best_design = mo_designer.select_optimal_design(pareto_front, criteria='balanced')
```

### 主动学习数据构建

```python
from porosdata.designer.active_learning import ActiveLearningDesigner

# 创建主动学习设计器
al_designer = ActiveLearningDesigner(
    strategy='uncertainty_sampling',
    batch_size=10
)

# 迭代式数据收集
for iteration in range(5):
    # 获取最具信息量的候选样本
    candidates = al_designer.suggest_next_experiments(
        current_data=available_data,
        candidate_pool=unlabeled_pool,
        num_suggestions=10
    )

    # 执行实验并获取结果（模拟）
    experimental_results = conduct_experiments(candidates)

    # 更新数据集
    available_data = al_designer.update_dataset(
        available_data,
        new_results=experimental_results
    )

    print(f"迭代 {iteration+1}: 数据集大小 = {len(available_data)}")
```

### 自适应实验设计

```python
from porosdata.designer.adaptive import AdaptiveDesigner

# 创建自适应设计器
adaptive_designer = AdaptiveDesigner()

# 定义适应性策略
strategy = {
    'initial_design': 'latin_hypercube',  # 初始设计：拉丁超立方
    'adaptation_trigger': 'performance_drop',  # 适应触发条件
    'adaptation_method': 'reinforcement_learning'  # 适应方法
}

# 执行自适应设计过程
design_process = adaptive_designer.run_adaptive_design(
    initial_data=seed_data,
    parameter_space=design_space,
    strategy=strategy,
    max_iterations=20,
    convergence_threshold=0.01
)

# 查看设计演化过程
design_process.plot_convergence_history()
design_process.plot_parameter_exploration()
```

## 设计质量评估

### 设计效率指标

```python
from porosdata.designer.evaluation import DesignEvaluator

evaluator = DesignEvaluator()

# 全面设计评估
evaluation_report = evaluator.evaluate_comprehensive(
    design=experimental_design,
    historical_data=all_data,
    validation_criteria=['efficiency', 'robustness', 'information_gain']
)

print("设计评估报告:")
print(f"- 空间填充度: {evaluation_report.space_filling}")
print(f"- 预测准确性: {evaluation_report.predictive_accuracy}")
print(f"- 鲁棒性评分: {evaluation_report.robustness_score}")
print(f"- 信息增益: {evaluation_report.information_gain}")
```

### 敏感性分析

```python
# 参数敏感性分析
sensitivity_analysis = evaluator.analyze_parameter_sensitivity(
    design=experimental_design,
    model=predictive_model,
    parameters=parameter_list
)

# 可视化敏感性
sensitivity_analysis.plot_sensitivity_map()
sensitivity_analysis.plot_tornado_diagram()
```

## 知识驱动设计

### 本体论集成

```python
from porosdata.designer.knowledge import OntologyBasedDesigner

# 创建基于本体的设计器
ontology_designer = OntologyBasedDesigner(
    ontology_file='materials_ontology.owl',
    reasoning_engine='hermit'
)

# 基于领域知识的设计
knowledge_driven_design = ontology_designer.design_with_knowledge(
    target_material='high_entropy_alloy',
    performance_requirements={
        'hardness': {'min': 400, 'max': 600, 'unit': 'HV'},
        'ductility': {'min': 0.2, 'unit': 'true_strain'}
    },
    constraints={
        'cost': {'max': 50, 'unit': 'USD/kg'},
        'processing_temperature': {'max': 1200, 'unit': '°C'}
    }
)

# 解释设计决策
explanations = ontology_designer.explain_design_decisions(knowledge_driven_design)
for explanation in explanations:
    print(f"设计依据: {explanation.reason}")
    print(f"知识来源: {explanation.knowledge_source}")
    print(f"置信度: {explanation.confidence}")
```

### 因果推理

```python
from porosdata.designer.causal import CausalDesigner

# 创建因果设计器
causal_designer = CausalDesigner()

# 建立因果图
causal_graph = causal_designer.build_causal_graph(training_data)

# 因果效应分析
causal_effects = causal_designer.analyze_causal_effects(
    graph=causal_graph,
    intervention='change_alloy_composition',
    outcome='material_property'
)

# 基于因果的设计优化
causal_optimized_design = causal_designer.optimize_with_causal_knowledge(
    causal_graph=causal_graph,
    objectives=design_objectives,
    constraints=design_constraints
)
```

## 可视化与交互

### 设计空间可视化

```python
from porosdata.designer.visualization import DesignVisualizer

visualizer = DesignVisualizer()

# 设计空间可视化
visualizer.plot_design_space(
    design_result=design_result,
    dimensions=['temperature', 'composition', 'hardness'],
    plot_type='3d_scatter'
)

# 优化轨迹可视化
visualizer.plot_optimization_trajectory(
    design_history=design_process.history,
    objective='hardness',
    parameters=['temperature', 'time']
)
```

### 交互式设计界面

```python
from porosdata.designer.interactive import InteractiveDesigner

# 创建交互式设计器
interactive_designer = InteractiveDesigner()

# 启动交互式设计会话
design_session = interactive_designer.start_session(
    initial_design=seed_design,
    user_constraints=user_defined_constraints
)

# 处理用户反馈
@design_session.on_user_feedback
def handle_feedback(feedback):
    if feedback.type == 'constraint_addition':
        design_session.update_constraints(feedback.new_constraints)
    elif feedback.type == 'design_rejection':
        design_session.refine_design_space(feedback.rejected_design)

# 运行交互式优化
final_design = design_session.run_interactive_optimization()
```

## 性能优化

### 大规模设计优化

```python
from porosdata.designer.scalable import ScalableDesigner

# 创建可扩展设计器
scalable_designer = ScalableDesigner(
    parallelization='distributed',
    memory_efficient=True
)

# 大规模参数空间优化
large_scale_result = scalable_designer.optimize_large_space(
    parameter_space=high_dimensional_space,
    num_candidates=1000,
    batch_size=100,
    max_evaluations=5000
)
```

### 实时设计支持

```python
from porosdata.designer.realtime import RealtimeDesigner

# 创建实时设计器
realtime_designer = RealtimeDesigner(
    update_frequency='per_minute',
    adaptation_speed='fast'
)

# 实时实验指导
realtime_guidance = realtime_designer.provide_realtime_guidance(
    current_experiment=ongoing_experiment,
    recent_results=new_data,
    time_remaining=experiment_time_left
)

print(f"实时建议: {realtime_guidance.next_action}")
print(f"预期改进: {realtime_guidance.expected_improvement}")
```

## 输出格式

### 标准设计结果

```python
{
    'experiments': [
        {
            'id': 'exp_001',
            'parameters': {
                'temperature': 950.5,
                'time': 4.2,
                'composition': {'Fe': 0.7, 'Cr': 0.15, 'Ni': 0.15}
            },
            'predicted_performance': {
                'hardness': {'value': 485, 'uncertainty': 15},
                'ductility': {'value': 0.28, 'uncertainty': 0.05}
            },
            'design_rationale': '基于贝叶斯优化，平衡探索与利用'
        }
    ],
    'design_metadata': {
        'method': 'bayesian_optimization',
        'iterations': 50,
        'convergence_metric': 0.023,
        'design_space_coverage': 0.85
    },
    'quality_assessment': {
        'efficiency_score': 0.92,
        'robustness_score': 0.88,
        'information_gain': 1.45
    }
}
```

### 设计报告导出

```python
from porosdata.designer.reporting import DesignReportGenerator

# 生成详细设计报告
report_generator = DesignReportGenerator()

# 导出多种格式
report_generator.export_report(
    design_result=design_result,
    formats=['pdf', 'html', 'json'],
    include_visualizations=True,
    include_explanations=True
)
```