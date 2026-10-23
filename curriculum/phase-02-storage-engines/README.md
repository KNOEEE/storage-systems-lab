# 阶段 2：存储引擎与读写放大

- 周次：W05–W08；配套项目：RocksDB，对照 SQLite。
- 进入条件：能解释页、journal、提交与 checkpoint，完成阶段 1 验收。

## 学习顺序

1. [W05：LSM 写入路径](w05-lsm-write-path.md)
2. [W06：读取路径与过滤器](w06-read-path.md)
3. [W07：Flush、Compaction 与放大](w07-compaction.md)
4. [W08：配置与基准实验](w08-benchmarking.md)

用 DDIA 第 3 章串联 WAL、MemTable、SST、缓存和后台整理。直接使用上游的 `db_bench` 和现有测试；不先写一套通用压测框架。

## 阶段成果

一页 B-tree / LSM 对照和一份 RocksDB 单变量实验，写入 `reports/phase-02.md`，使用 [阶段模板](../../templates/phase-report.md)。

过关问题：**给定同一个负载，两类组织方式可能遇到什么瓶颈？** 答案必须包含访问模式、缓存与持久化条件。

## 主要资料

- DDIA 第一版第 3 章 Storage and Retrieval，第 1 章负载与性能。
- [RocksDB Overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)。
- [Benchmarking tools](https://github.com/facebook/rocksdb/wiki/Benchmarking-tools)。
