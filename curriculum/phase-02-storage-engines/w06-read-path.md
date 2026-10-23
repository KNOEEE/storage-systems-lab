---
week: 6
phase: storage-engines
estimated_hours: 5
status: planned
---

# W06：数据分散在多处，读取怎么找？

## 核心问题

一个键可能在 MemTable、多个 SST 与缓存里，读取如何决定返回哪个版本，又如何减少不必要的访问？

## 理论与设计（1.5 小时）

- DDIA 第一版第 3 章：有序文件、索引和 LSM 读取取舍。
- 补 Bloom Filter 的假阳性与无假阴性前提，结合 [RocksDB Overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview) 中的读取组件。先预测存在键与不存在键的差异。

## 目标源码（1 小时）

从 `DB::Get` 追到 MemTable 查询、SST 查找与 table reader，定位过滤器和 Block Cache 的使用边界。记录当前版本统计项名称与意义；不要把缓存命中当成设备读取。

## 验证步骤（2 小时）

1. 固定键值长度、记录数、随机种子和查询次数，先装载并 Flush 数据。
2. 对存在键与不存在键各跑一组查询，保留延迟、读取统计和配置。
3. 重复一组相同查询观察缓存预热影响；另选过滤器或缓存的一个配置做单变量对照。
4. 对照假设解释观测。若无法控制 OS 页缓存，记录这个限制，不宣称测到了纯设备延迟。

## 交付物

- `notes/weeks/w06.md`：Get 路径图、负载定义、统计对照；原始输出放 `artifacts/w06/`。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 说明读取怎样合并来自不同位置的版本。
- [ ] 区分 Block Cache 命中、页缓存命中与设备读取。
- [ ] 正确解释 Bloom Filter 的假阳性及适用条件。
- [ ] 用统计支持或否定一个明确假设。

## 复盘

- 实际用时：
- 哪项统计最容易误读：
- 仍无法归因的观测：
