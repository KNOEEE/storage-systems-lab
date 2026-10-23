# 阶段 6：分片、MVCC 与分布式事务

- 周次：W19–W22；配套项目：TiKV 与 PD。
- 进入条件：能解释 LSM、Raft、放置与客户端路由。

## 学习顺序

1. [W19：Region 与请求路由](w19-regions-routing.md)
2. [W20：Region 变化与旧路由](w20-region-changes.md)
3. [W21：MVCC 与可见性](w21-mvcc.md)
4. [W22：跨 Region 原子提交](w22-distributed-commit.md)

先解释每个机制各自的保证，再追一笔事务穿过这些机制的路径。第一轮使用传统 Percolator prewrite / commit；在所用版本中核对是否启用了异步提交、1PC 等优化，避免用优化路径的结果解释传统模型。不展开 SQL 执行与查询优化。

## 阶段成果

将存储引擎、Raft、Region、MVCC、事务串起来的架构与时序图，按 [阶段模板](../../templates/phase-report.md) 写入 `reports/phase-06.md`。

过关问题：**为什么 Raft 的复制一致性不能替代跨分片原子提交？**

## 主要资料

- DDIA 第一版第 6 章分区、第 7 章事务、第 9 章原子提交。
- [TiKV Data Sharding](https://tikv.org/deep-dive/scalability/data-sharding/)。
- [TiKV Distributed Transaction](https://tikv.org/deep-dive/distributed-transaction/introduction/)、[Percolator](https://tikv.org/deep-dive/distributed-transaction/percolator/)。
