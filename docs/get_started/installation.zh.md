# 安装指南

请根据使用场景选择安装方式，可用于本地验证、源码开发或服务器批处理。
{: .lead}

## 推荐安装方式

对于大多数用户，建议先从已发布包开始：

```bash
pip install porosdata-processor
```

这种方式适合快速验证基础文本处理能力，并完成小规模本地测试。

## 从源码安装

如果需要查看源码、调整处理行为或验证本地修改，可以使用源码安装：

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

如果仓库中提供扩展依赖配置，也可以在开发环境中使用对应的安装方式。

## 环境说明

安装前建议确认以下基础条件：

- Python `3.8+`
- 可写入的本地环境或虚拟环境
- 足够容纳原始数据、中间结果和最终结果的磁盘空间

对于较大的批处理项目，更推荐 Linux 环境和 SSD 或 NVMe 存储。

## 安装验证

安装完成后，可先确认包是否可用：

```python
import porosdata_processor
print(porosdata_processor.__version__)
```

如果计划运行批处理任务，也建议检查命令行入口：

```bash
python -m porosdata_processor --help
```

## 首次运行前需要准备什么

建议在第一次运行前先准备以下三项内容：

1. 原始文献或上游解析结果
2. 中间结果的输出目录
3. 一组用于验证流程的小样本

## 下一步建议

- 继续阅读 [快速开始](quickstart.md)
- 查看 [端到端工作流](end-to-end-workflow.md)
- 参考 [使用示例](../references/examples.md)

## 快速链接

- [首页](../index.md)
- [快速开始](../get_started/quickstart.md)
{: .tight-list}
