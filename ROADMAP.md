# 24 周存储系统学习路线

从一次本机写入出发，逐步理解存储引擎、复制、文件系统、数据放置和事务，再用一次可复现的实验把它们连起来。每周约 5 小时，按验收结果推进；周数表示学习顺序，不是日历截止日期。

## 每周的闭环

围绕同一个问题完成 **原理阅读 → 设计与源码 → 实验 → 闭卷解释**。两本主教材按主题选读：OSTEP 负责本机 I/O 和持久化，DDIA 负责存储引擎与分布式系统。下表 DDIA 章节均按**第一版**标注，其他版本按章节主题对应。

| 周次与核心问题 | 理论与设计 | 对应实现 | 验证与交付 |
|---|---|---|---|
| [W01：一次写入经过哪里？](curriculum/phase-01-local-storage/w01-write-path.md) | OSTEP：I/O 设备、文件与目录 | SQLite OS Interface | 跟踪系统调用，画应用—缓存—文件系统—设备路径 |
| [W02：文件里如何找到记录？](curriculum/phase-01-local-storage/w02-pages-and-btree.md) | DDIA 第 3 章 B-tree；OSTEP 文件系统布局 | SQLite B-tree / Pager | 对比页数、文件大小与索引布局 |
| [W03：修改到一半崩溃怎么办？](curriculum/phase-01-local-storage/w03-crash-recovery.md) | OSTEP 崩溃一致性；SQLite Atomic Commit | SQLite Pager / rollback journal | 在事务边界终止进程，检查恢复与完整性 |
| [W04：提交与 checkpoint 有何不同？](curriculum/phase-01-local-storage/w04-wal-checkpoint.md) | DDIA 第 7 章原子性与隔离性；SQLite WAL | SQLite WAL / checkpoint | 两连接读写，观察长读事务和 checkpoint |
| [W05：为什么需要 LSM？](curriculum/phase-02-storage-engines/w05-lsm-write-path.md) | DDIA 第 3 章 SSTable / LSM | RocksDB WAL / MemTable | 跑通 Put/Get/Delete，对照 SQLite 写路径 |
| [W06：多份数据中如何找到键？](curriculum/phase-02-storage-engines/w06-read-path.md) | DDIA 第 3 章索引；Bloom Filter | RocksDB 读路径 / Block Cache | 对比命中、不存在键及缓存统计 |
| [W07：为何写一点却整理很多？](curriculum/phase-02-storage-engines/w07-compaction.md) | 读、写、空间放大；版本回收 | RocksDB Flush / Compaction | 覆盖与删除，观察文件、空间和后台工作 |
| [W08：怎样公平评价配置？](curriculum/phase-02-storage-engines/w08-benchmarking.md) | DDIA 第 1 章负载，第 3 章取舍 | RocksDB db_bench / 统计 | 单变量对照，报告性能与持久化条件 |
| [W09：请求超时意味着什么？](curriculum/phase-03-replication/w09-timeouts.md) | DDIA 第 5、8 章复制与故障 | etcd 请求与客户端结果 | 三节点集群，区分成功、失败、未知 |
| [W10：多份日志怎样一致？](curriculum/phase-03-replication/w10-raft-log.md) | Raft 选主、日志复制与安全性 | raft Step / Ready / 集成循环 | 停止 leader，用日志解释选举与恢复 |
| [W11：写完之后读取一定看到吗？](curriculum/phase-03-replication/w11-consistency.md) | DDIA 第 9 章线性一致性 | etcd 读取与 apply | 比较线性一致与 serializable 读 |
| [W12：节点恢复和集群恢复相同吗？](curriculum/phase-03-replication/w12-snapshot-recovery.md) | Raft 快照；备份与灾难恢复 | etcd 快照备份 / 恢复 | 在隔离目录恢复并核对数据 |
| [W13：文件名怎样变成数据位置？](curriculum/phase-04-distributed-filesystems/w13-metadata.md) | GFS 设计假设；HDFS 架构 | NameNode / DataNode / Client | 上传跨块文件，画元数据与读路径 |
| [W14：副本写入为何需要流水线？](curriculum/phase-04-distributed-filesystems/w14-write-pipeline.md) | GFS 数据流与控制流；复制确认 | HDFS DataStreamer / ACK | 追一段数据和确认，画写入时序 |
| [W15：能读是否等于修复完成？](curriculum/phase-04-distributed-filesystems/w15-replica-repair.md) | 故障检测、冗余与修复 | HDFS 心跳 / 块报告 / 重复制 | 停一个 DataNode，区分服务恢复与冗余恢复 |
| [W16：对象、块、文件接口如何选？](curriculum/phase-05-placement/w16-storage-interfaces.md) | 接口语义；DDIA 第 6 章数据划分 | RADOS / RGW / RBD / CephFS | 对同一需求比较应用承担的工作 |
| [W17：扩容会移动哪些数据？](curriculum/phase-05-placement/w17-crush-placement.md) | 故障域、放置与重平衡；CRUSH | CRUSH map / 放置规则 | crushtool 模拟分布与映射变化 |
| [W18：副本与纠删码怎样取舍？](curriculum/phase-05-placement/w18-erasure-coding.md) | 容量、容错、修复开销 | Ceph 副本 / EC Pool | 明确假设后做容量计算与故障推演 |
| [W19：复制组怎样扩展成集群？](curriculum/phase-06-transactions/w19-regions-routing.md) | DDIA 第 6 章范围与哈希划分 | TiKV Region / PD / 多 Raft | 查看范围、副本和客户端路由 |
| [W20：迁移时谁有权处理写入？](curriculum/phase-06-transactions/w20-region-changes.md) | DDIA 第 6 章重平衡；配置版本 | Region 拆分 / 迁移 / 调度 | 追一次变化，解释旧路由处理 |
| [W21：事务怎样看见不同版本？](curriculum/phase-06-transactions/w21-mvcc.md) | DDIA 第 7 章快照隔离；Percolator | MVCC / 锁 / 时间戳 | 两个并发事务预测并验证可见性 |
| [W22：跨分片如何原子提交？](curriculum/phase-06-transactions/w22-distributed-commit.md) | DDIA 第 9 章原子提交与 2PC | TiKV 传统 prewrite / commit | 确认跨 Region，推演失败与恢复 |
| [W23：相关性是否就是原因？](curriculum/phase-07-capstone/w23-hypothesis.md) | 负载、尾延迟与放大；实验设计 | RocksDB 统计 / 整理日志 | 固定覆盖写负载，提出可证伪假设 |
| [W24：配置改变后真的更好吗？](curriculum/phase-07-capstone/w24-experiment-report.md) | 性能、持久化、恢复与成本取舍 | 与假设相关的一段实现 | 单变量对照，完成可复现技术报告 |

## 阶段成果与过关问题

| 阶段 | 周次 | 必须留下的成果 | 过关问题 |
|---|---|---|---|
| [本机存储](curriculum/phase-01-local-storage/README.md) | W01–W04 | 提交与恢复图、SQLite 实验记录 | 写入返回、事务提交、数据文件更新、可恢复分别意味着什么？ |
| [存储引擎](curriculum/phase-02-storage-engines/README.md) | W05–W08 | B-tree / LSM 对照、RocksDB 实验 | 同一个负载为何暴露不同瓶颈？ |
| [复制与恢复](curriculum/phase-03-replication/README.md) | W09–W12 | 请求—日志—提交—应用—响应图、故障记录 | 超时后的写入究竟是否生效？ |
| [分布式文件系统](curriculum/phase-04-distributed-filesystems/README.md) | W13–W15 | 文件读写时序、故障与修复过程 | 继续服务和恢复副本数之间发生了什么？ |
| [放置与接口](curriculum/phase-05-placement/README.md) | W16–W18 | CRUSH 映射实验、副本 / EC 比较 | 三份副本为什么不保证任意两台机器故障时可用？ |
| [分片与事务](curriculum/phase-06-transactions/README.md) | W19–W22 | 引擎、Raft、Region、MVCC、事务架构图 | Raft 为什么不能替代跨分片事务？ |
| [综合验证](curriculum/phase-07-capstone/README.md) | W23–W24 | 可复现技术报告 | 证据支持了什么，什么仍未验证？ |

## 范围与执行约定

- 每周只写一份 [整合笔记](templates/weekly-note.md)，把问题、原理、代码证据和实验结果放在一起。
- 源码阅读围绕目标结构、函数和测试，记录所用提交；不逐行通读六个项目。
- 第一轮不从零实现完整 Raft，不展开 HDFS 的 YARN / MapReduce，不搭完整 Ceph 集群，不深入 SQL 优化或 TiKV 全部事务优化。
- 在隔离目录和测试集群里做故障实验。进程退出、网络故障、主机崩溃、断电分别记录，不能相互替代。
- 基准报告必须包含工作负载、环境、同步与持久化配置。`db_bench` 与 `fio` 测量的对象不同，不能互相替代。

从 [课程使用方式](curriculum/README.md) 和 [W01](curriculum/phase-01-local-storage/w01-write-path.md) 开始。
