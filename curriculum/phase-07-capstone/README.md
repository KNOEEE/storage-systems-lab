# 阶段 7：综合实验与技术报告

- 周次：W23–W24；配套项目：回到 RocksDB。
- 进入条件：完成前六阶段，能够描述负载、持久化条件、资源和证据边界。

## 学习顺序

1. [W23：提出可证伪的性能假设](w23-hypothesis.md)
2. [W24：对照实验与最终报告](w24-experiment-report.md)

研究持续覆盖写时的延迟波动。用同一套工作负载连接本机 I/O、LSM 整理、统计观测和工程取舍，不再引入新项目。只选一个可在两周内验证的变量。

## 最终成果

报告写入 `reports/phase-07.md`，从 [阶段模板](../../templates/phase-report.md) 开始，包含：**工作负载 → 问题 → 原理假设 → 实现依据 → 实验 → 结论与边界**。保留能复现实验的入口、完整配置和原始结果位置。

过关问题：**观察到性能变化后，哪些证据说明原因，哪些只能说明相关？改进付出了什么代价？**

## 主要资料

- DDIA 第一版第 1 章性能描述与第 3 章存储引擎。
- [RocksDB Benchmarking tools](https://github.com/facebook/rocksdb/wiki/Benchmarking-tools)。数据库行为用 `db_bench`，底层 I/O 假设可另设 `fio` 实验；两类结果分别解释。
