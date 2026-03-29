# 为 PorosData 做贡献

我们欢迎社区贡献！本指南将帮助您开始为 PorosData 项目做贡献。
{: .lead}

## 开发环境设置

### 前置要求

- Python 3.8+
- Git
- 虚拟环境 (推荐)
{: .tight-list}

### 克隆和设置

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .[dev]
```

## 开发工作流

### 1. 选择问题

访问我们的 [GitHub Issues](https://github.com/KiventYip/porosdata-processor/issues) 页面，选择一个要处理的问题。如果您是新手，请寻找标记为 `good first issue` 的问题。

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-number-description
```

### 3. 进行更改

遵循我们的编码标准：
- 使用类型提示
- 编写全面的测试
- 更新文档
- 遵循 PEP 8 样式指南
{: .tight-list}

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_specific_feature.py

# 运行覆盖率测试
pytest --cov=porosdata_processor
```

### 5. 更新文档

如果您的更改影响 API 或添加新功能，请更新相关文档文件。

### 6. 提交更改

```bash
git add .
git commit -m "feat: add new feature description"
```

使用约定式提交格式：
- `feat:` 表示新功能
- `fix:` 表示错误修复
- `docs:` 表示文档更改
- `test:` 表示测试相关更改
{: .tight-list}

### 7. 创建拉取请求

推送您的分支并在 GitHub 上创建拉取请求。包括：
- 更改的清晰描述
- 相关问题的引用
- 如果是 UI 更改，请提供截图
- 测试结果
{: .tight-list}

## 代码标准

### Python 样式

我们遵循 PEP 8 及一些修改：
- 行长度：88 个字符 (Black 默认)
- 字符串使用双引号
- 字符串格式化使用 f-string
{: .tight-list}

### 测试

- 为所有新函数编写单元测试
- 目标代码覆盖率 >90%
- 使用描述性的测试名称
- 测试边界情况和错误条件
{: .tight-list}

### 文档

- 使用 Google 风格的文档字符串
- 保持 README 更新
- 记录破坏性更改
{: .tight-list}

## 插件开发

### 插件结构

```python
from porosdata_processor.plugins.base import BasePlugin

class MyCustomPlugin(BasePlugin):
    """插件描述。"""

    def __init__(self, config=None):
        super().__init__(config)

    def process(self, text: str) -> str:
        """处理输入文本。"""
        # 实现代码
        return processed_text

    def validate_config(self):
        """验证插件配置。"""
        # 验证逻辑
        pass
```

### 插件注册

在 `porosdata_processor/plugins/__init__.py` 中注册您的插件：
{: .section-intro}

```python
from .my_plugin import MyCustomPlugin

__all__ = ['MyCustomPlugin']
```

## 获取帮助

- **讨论**: 在 [GitHub Discussions](https://github.com/KiventYip/porosdata-processor/discussions) 中提问
- **问题**: 通过 [GitHub Issues](https://github.com/KiventYip/porosdata-processor/issues) 报告错误或请求功能
- **Discord**: 加入我们的社区 Discord 服务器
{: .tight-list}

## 认可

贡献者将：
- 在 CONTRIBUTORS.md 中列出
- 在发布说明中提及
- 对于重大贡献，邀请加入核心团队
{: .tight-list}