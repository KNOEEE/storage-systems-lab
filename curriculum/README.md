# 课程与执行方式

路线见 [ROADMAP](../ROADMAP.md)。课程按阶段和周组织，实验代码按能力保存在 `labs/`，避免每周复制一套代码。与 `llm-inference` 一样，以任务、交付物和验收标准连接阅读与实践。

| 阶段 | 周次 | 入口 |
|---|---|---|
| 本机 I/O、页组织与恢复 | W01–W04 | [phase-01-local-storage](phase-01-local-storage/README.md) |
| 存储引擎与放大 | W05–W08 | [phase-02-storage-engines](phase-02-storage-engines/README.md) |
| 复制、一致性与恢复 | W09–W12 | [phase-03-replication](phase-03-replication/README.md) |
| 分布式文件系统 | W13–W15 | [phase-04-distributed-filesystems](phase-04-distributed-filesystems/README.md) |
| 数据放置、故障域与接口 | W16–W18 | [phase-05-placement](phase-05-placement/README.md) |
| 分片、MVCC 与事务 | W19–W22 | [phase-06-transactions](phase-06-transactions/README.md) |
| 综合实验 | W23–W24 | [phase-07-capstone](phase-07-capstone/README.md) |

## 每周 5 小时

| 时间 | 任务 | 本周留下什么 |
|---|---|---|
| 1.5 小时 | 按核心问题选读教材与设计文档 | 一段机制解释和实验预测 |
| 1 小时 | 在固定版本源码里寻找结构、函数和测试 | 带提交号的调用链或状态图 |
| 2 小时 | 固定变量、运行实验、整理原始证据 | 命令、日志、观察及与预测的差异 |
| 0.5 小时 | 合上资料重新解释，做短复盘 | 验收答案、未解问题和实际用时 |

环境准备占用实验时间。若部署耗尽本周预算，记录进度再继续，不把实验替换成未经执行的结论。

## 每周如何开始与结束

1. 打开本周页面，先读核心问题和验收标准。
2. 从 [weekly-note 模板](../templates/weekly-note.md) 创建 `notes/weeks/wNN.md`。
3. 写下预测，再读资料与源码。版本记录遵循 [upstreams](../upstreams/README.md)；不要在不同提交之间拼接调用链。
4. 实验数据库、跟踪文件和大日志放到 `artifacts/wNN/`；可提交的短证据及相对路径写入周记。
5. 对照验收项检查，在周记里记录证据。满足后将周页的 `status` 从 `planned` 改为 `completed`；未通过可用 `in-progress`。
6. 阶段末按 [phase-report 模板](../templates/phase-report.md) 创建 `reports/phase-NN.md`，回答阶段过关问题。

一周可以有多个小实验，但只维护一份整合笔记。实验失败也可以成为有效证据，前提是清楚记录命令、环境、预期与实际结果。

## 阅读约定

- OSTEP 使用[作者免费在线版本](https://pages.cs.wisc.edu/~remzi/OSTEP/)，按章名定位；章节页码可能随版本不同。
- DDIA 使用**第一版**章号：第 1 章可靠性、可扩展性与可维护性，第 3 章存储与检索，第 5 章复制，第 6 章分区，第 7 章事务，第 8 章分布式系统的麻烦，第 9 章一致性与共识。其他版按主题对应。
- 论文只选读与本周问题有关的部分。官方设计文档说明目标机制，当前实现仍须在所用源码版本中核对。
- 周页里的源码名称是检索入口，不是完整调用链或永久有效的路径；若名称变更，在周记记录实际位置。

## 什么算完成

能够闭卷解释本周问题；能够指出实现依据；能够复现一次验证；能够说出证据边界。性能结论额外要求固定负载、环境信息、原始结果和重复运行。

新任务按 [周模板](week-template.md) 编写，不能只留下“读一章”或“看一个仓库”。
