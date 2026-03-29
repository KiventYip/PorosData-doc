# Processor 运行、性能与部署说明

## 1. 输出目录与临时文件

- 正式输出目录默认是 `data/processed`
- 处理过程中允许出现真正的临时文件：`*.tmp`
- `*.tmp` 的用途是原子写入：先写临时文件，成功后再替换正式 `json`
- 异常中断时，程序会在运行前和运行结束时自动清理输出目录下残留的 `*.tmp`
- 这不是“临时输出目录”方案，正式交付结果仍然直接落在 `data/processed`

当前约定：

- 输入：`data/raw`
- 输出：`data/processed`
- 报告：`data/processed/processing_report.json`

## 2. 为什么整体运行会慢

`processor` 当前是典型的 CPU 密集型 + 文本规则密集型流程，慢的主要原因通常不是磁盘，而是下面几项叠加：

1. `--enable-evaluation` 会额外加载 GPT-2 tokenizer，并做 token 压缩率统计
2. 长文本、复杂公式、结构化显示公式会触发更重的修复路径
3. 高风险文本块会进入隔离子进程，并且有 90 到 120 秒的超时保护
4. Windows 下多进程启动成本比 Linux 更高
5. 每个文件除了正文清洗，还要做 JSON 读写、图片目录复制、交付字段清洁和控制字符清理

结论：

- 不是 GPU 瓶颈
- 不主要是磁盘瓶颈
- 大多数场景下首先是 CPU 和单块复杂文本的耗时
- 内存不足会放大问题，但通常表现为 worker 数被自动压低，而不是直接报错

## 3. 本地 POC 的参考结果

基于 `data/raw` 全量 POC，一次参考运行结果如下：

- 输入文件数：38
- 处理文件数：38
- 总条目数：2166
- 总耗时：约 424.06 秒
- 平均每文件：约 11.16 秒
- 条目吞吐：约 5.11 items/s
- 平均 token 压缩率：0.124
- 清理控制字符总数：38
- 自动 worker 数：2

这次结果说明：

- 流程是正常跑完的
- 当前速度偏慢，但不是“挂死”
- `enable-evaluation` 的 tokenizer 与长文本隔离子进程是主要耗时来源

## 4. 如何判断是不是正常运行

现在建议观察这几类日志：

1. 主进程心跳日志
2. 文件级进度日志
3. 高风险文本块日志
4. 超时回退日志

正常运行时，你会看到类似信息：

- `Processing progress: 26.3% (10/38 files)`
- `Heartbeat: 10/38 files completed, 28 pending, elapsed ...`
- `Using isolated subprocess for high-risk text block`
- `Text block still processing in isolated subprocess: elapsed=...`

这些日志代表：

- 进程没挂
- 文件还在推进
- 某些长块只是慢，不一定坏

以下日志要重点关注：

- `Subprocess text cleaning timeout ... using original text`
- `Overall batch timeout ...`
- `process execution failed`
- `Memory usage ... exceeded configured limit ...`

它们分别表示：

- 某个文本块太慢，已回退为原文，文件仍可继续完成
- 整批任务等太久
- 子进程异常
- 当前内存压力偏大

## 5. 什么时候是硬件问题

可以按下面判断：

- CPU 长时间高占用、内存稳定：通常是正常的 CPU 密集运行
- CPU 低、日志长时间不动、无心跳：需要排查是否卡住
- 可用内存过低、worker 自动变少：说明内存是约束项
- 机械硬盘或网络盘：会拖慢 JSON 和图片复制，但通常不是首瓶颈

对这个项目来说，优先级通常是：

1. CPU
2. 内存
3. 本地 SSD / NVMe
4. Windows 与 Linux 的进程模型差异

## 6. 服务器推荐配置

### 小规模验证

- 4 vCPU
- 16 GB RAM
- SSD
- `--max-workers 2`
- 建议先不开 `--enable-evaluation`

### 常规生产

- 8 vCPU
- 32 GB RAM
- NVMe SSD
- `--max-workers 4` 到 `6`
- 如需评估，建议单独开批次或先用 4 workers

### 大批量长期运行

- 16 vCPU
- 64 GB RAM
- NVMe SSD
- Linux 优先
- `--max-workers 6` 到 `8`
- 评估模式与正式清洗可分两次运行

补充：

- 不需要 GPU
- 不建议只堆内存而不给 CPU
- Linux 服务器通常比 Windows 更适合长时间多进程任务

## 7. 推荐运行方式

### 正式交付

```powershell
python examples/run_pipeline.py `
  --input-dir "data/raw" `
  --output-dir "data/processed" `
  --force-reprocess `
  --max-workers 4 `
  --memory-limit 8192 `
  --heartbeat-seconds 30
```

### 带 token 评估

```powershell
python examples/run_pipeline.py `
  --input-dir "data/raw" `
  --output-dir "data/processed" `
  --force-reprocess `
  --enable-evaluation `
  --max-workers 4 `
  --memory-limit 8192 `
  --heartbeat-seconds 30
```

如果你主要关心交付质量而不是 token 统计，建议：

- 日常批量清洗时默认不开 `--enable-evaluation`
- 只在抽检、审计或 POC 时开启

## 8. 为什么“难判断是否正常运行”

之前的主要问题是：

- 缺少固定频率的主进程心跳
- 长文本隔离子进程在超时前几乎没有中间状态输出
- 用户只能看到“有输出”或“没输出”，很难判断是在慢跑还是挂住

现在的改进方向是：

- 主进程定时输出 heartbeat
- 长文本隔离子进程处理中定时输出“still processing”
- 最终报告保留总体吞吐、控制字符清理、token 效率等摘要

## 9. 建议的使用策略

为了同时兼顾速度与稳定性，建议这样使用：

1. 开发调试时：`--max-workers 2`
2. 正式批量时：先不开 `--enable-evaluation`
3. 审计或验收时：再开 `--enable-evaluation`
4. 超长文档多时：降低并行度，优先稳定
5. 统一看 `processing_report.json` 和日志心跳判断健康状态

## 10. 还可以继续优化的方向

如果后续要继续提速，优先级建议如下：

1. 默认将“清洗”和“token 评估”分离
2. 对超长块做更细粒度切分或更保守的公式修复策略
3. 在 Linux 服务器上运行
4. 对长块建立更细的耗时统计报表
5. 增加“单文件耗时 Top N”输出，快速定位慢文件
