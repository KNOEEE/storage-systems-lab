---
week: 4
phase: local-storage
estimated_hours: 5
status: planned
---

# W04：提交、checkpoint 和读取是什么关系？

## 核心问题

WAL 模式下事务已经提交，为什么数据库主文件可能还没更新？一个长读事务会怎样影响 checkpoint？

## 理论与设计（1.5 小时）

- DDIA 第一版第 7 章：原子性、隔离性与快照读取的区别。
- [SQLite WAL](https://sqlite.org/wal.html)：工作方式、checkpoint、并发读写。对照 W03，单独画出 WAL 提交与搬回主文件的步骤。

## 目标源码（1 小时）

固定 SQLite 提交，定位 `wal.c` 里写 frame、提交标记、开始读事务和 checkpoint 的入口，核对与 Pager 的边界。不要求读完整 WAL-index 实现。

## 验证步骤（2 小时）

1. 新建测试库，读回 `journal_mode=WAL`、`synchronous` 和 `wal_autocheckpoint`，记录实际配置。
2. 连接 A 显式开启读事务并读取；连接 B 提交新记录。分别观察 A 与新读连接的结果。
3. 保持 A 的事务，记录 WAL 大小并执行 `PRAGMA wal_checkpoint(PASSIVE)`，保存返回的 busy、log、checkpointed 字段。PASSIVE 返回值不能仅凭 busy 一项判定是否完全完成。
4. 结束 A 的读事务，再执行 checkpoint，比较可推进的范围。区分日志帧已复制、WAL 可重用和 WAL 文件截断。

## 交付物

- `notes/weeks/w04.md`：两连接时序、checkpoint 返回值和主文件 / WAL 观察；完成 `reports/phase-01.md`。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 用实验说明提交与 checkpoint 不是同一步。
- [ ] 解释长读事务持有的快照与 checkpoint 推进限制。
- [ ] 区分 WAL 与 W03 的 rollback journal 恢复机制。
- [ ] 闭卷回答阶段 1 过关问题，并标明未验证的断电条件。

## 复盘

- 实际用时：
- 对提交与持久化的理解发生了什么变化：
- 转向 LSM 前仍未解决的问题：
