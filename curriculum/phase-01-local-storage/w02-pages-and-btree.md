---
week: 2
phase: local-storage
estimated_hours: 5
status: planned
---

# W02：文件里如何找到一条记录？

## 核心问题

数据库如何把表和索引组织在一个文件里？数据库页与文件系统块是不是同一个概念？

## 理论与设计（1.5 小时）

- DDIA 第一版第 3 章：B-tree、索引与页更新；只读与页式组织有关的部分。
- OSTEP：File System Implementation，选读 inode、数据块与目录布局。
- [SQLite 架构](https://sqlite.org/arch.html)中的 B-tree 与 Pager。先预测：创建索引后，文件大小和页数会怎样变化？

## 目标源码（1 小时）

在固定 SQLite 提交中定位 `btree.c`、`pager.c`，寻找打开 B-tree、定位记录和读取页的接口。记录一个表根页与索引根页之间的关系；不展开 SQL 解析与虚拟机全部指令。

## 验证步骤（2 小时）

1. 在 `artifacts/w02/` 创建测试库，记录 SQLite 版本、`page_size`、`page_count`、`freelist_count` 和文件大小。
2. 建表并以固定记录数和字段长度插入数据，再测一次。创建一个二级索引，重复观测。
3. 查询 `sqlite_master` 的 `rootpage`，把表与索引对应到根页；该名称兼容较旧 SQLite。可用 `dbstat` 时补看页分布；该扩展缺失不妨碍基本任务。
4. 通过 `EXPLAIN QUERY PLAN` 比较索引前后的查找方式。把逻辑访问路径与实际文件大小分开解释。

## 交付物

- 在 `notes/weeks/w02.md` 放页组织图、SQL、观测表和源码提交；原始数据库留在 `artifacts/w02/`。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 解释数据库页、文件系统块与文件偏移的区别。
- [ ] 用实际根页与页数变化说明表和二级索引各占用哪些结构。
- [ ] 说明索引为什么可能加速读取，也会增加更新工作。
- [ ] 不把文件大小变化直接当作设备写入字节数。

## 复盘

- 实际用时与困难：
- 哪个预测被数据修正：
- 第 3 周需要解释的恢复问题：
