---
week: 5
phase: storage-engines
estimated_hours: 5
status: planned
---

# W05：为什么需要 LSM？

## 核心问题

将修改追加到日志、暂存在有序内存结构，与直接更新树上的页，各自改变了什么代价？

## 理论与设计（1.5 小时）

- DDIA 第一版第 3 章：SSTable、LSM-tree，以及与 B-tree 的比较。
- [RocksDB Overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)：只聚焦 WAL、MemTable、SST 和 Flush。先画一条你预测的 Put 路径。

## 目标源码（1 小时）

固定 RocksDB 提交，从公开 `DB::Put` / `Write` 接口寻找写入批次、WAL 与 MemTable 的衔接，记录相关类和一项基础读写测试。以所用版本的实现为准。

## 验证步骤（2 小时）

1. 用上游示例或最小调用程序，跑通 Put、Get、Delete；记录构建方法、提交、数据库目录与持久化参数。
2. 写一组可核对的键值，重开数据库检查结果，观察 LOG、WAL 和 SST 文件。
3. 主动 Flush 后再观察文件及重开结果；解释 Flush 与同步 WAL 的不同作用。
4. 将 W01–W04 的 SQLite 路径与本次 LSM 路径放在同一张图里，标明仍未知的部分。

## 交付物

- `notes/weeks/w05.md`：可复现入口、文件观察、SQLite / RocksDB 写路径对照。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 解释 WAL、MemTable、SST 各自承担什么。
- [ ] 用重开核对数据，写清同步与日志配置。
- [ ] 说明顺序追加为何没有消除后续整理成本。
- [ ] 不从一次小实验直接推出普遍的性能优劣。

## 复盘

- 实际用时与构建障碍：
- 路径预测与实现差异：
- 第 6 周读路径需要解决什么：
