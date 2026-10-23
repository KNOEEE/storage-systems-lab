# 上游源码与材料

外部源码保存在同级仓库，或本目录下已忽略的 `checkouts/`。本仓库保存任务、关键路径、实验入口和必要的小补丁。开始每个阶段时，在 [repos.yaml](repos.yaml) 填写实际 tag/commit、版本、编译参数及文档版本；null 表示尚未固定，不能当作已复现实验。

| 系统 | 原始来源 | 主要阅读范围 |
|---|---|---|
| SQLite | [官方 Fossil](https://sqlite.org/src/)、[官方 GitHub 镜像](https://github.com/sqlite/sqlite) | `src/btree.c`、`src/pager.c`、`src/wal.c`、`src/os_unix.c` |
| RocksDB | [facebook/rocksdb](https://github.com/facebook/rocksdb)、[官方 Wiki](https://github.com/facebook/rocksdb/wiki) | 写路径、Get、MemTable、SST、Flush、Compaction、db_bench |
| etcd | [etcd-io/etcd](https://github.com/etcd-io/etcd)、[官方文档](https://etcd.io/docs/) | 请求与读取、Raft 集成、快照与恢复 |
| Raft 库 | [etcd-io/raft](https://github.com/etcd-io/raft) | `Step`、`Ready`、持久化/发消息/应用的调用约定 |
| HDFS | [apache/hadoop](https://github.com/apache/hadoop)、[HDFS 架构](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html) | NameNode、DataNode、DFSClient、DataStreamer |
| Ceph | [ceph/ceph](https://github.com/ceph/ceph)、[架构文档](https://docs.ceph.com/en/latest/architecture/) | RADOS、PG、CRUSH、crushtool、冗余与恢复 |
| TiKV / PD | [tikv/tikv](https://github.com/tikv/tikv)、[tikv/pd](https://github.com/tikv/pd)、[Deep Dive](https://tikv.org/deep-dive/) | Region、路由与调度、MVCC、传统 prewrite/commit |

## 两本主教材

- [OSTEP 免费章节](https://pages.cs.wisc.edu/~remzi/OSTEP/)：按周指定主题选读，链接原文，不把整本书复制到仓库。
- [DDIA](https://dataintensive.net/)：章节号按第一版。第 1 章负载与性能，第 3 章存储引擎，第 5 章复制，第 6 章分片，第 7 章事务，第 8 章分布式故障，第 9 章一致性与共识。

## 关键论文与官方设计文档

- [SQLite Architecture](https://sqlite.org/arch.html)、[Atomic Commit](https://sqlite.org/atomiccommit.html)、[WAL](https://sqlite.org/wal.html)。
- [Raft 论文](https://raft.github.io/raft.pdf)，配合 [MIT 6.5840](https://pdos.csail.mit.edu/6.824/) 对应主题。
- [GFS 论文原始入口](https://research.google/pubs/the-google-file-system/)：用来理解设计假设；HDFS 的实现以自己的文档和源码为准。
- [CRUSH 论文](https://ceph.io/assets/pdfs/weil-crush-sc06.pdf)与 [crushtool 文档](https://docs.ceph.com/en/latest/man/8/crushtool/)。
- [Percolator 论文原始入口](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)：理解事务模型，具体 TiKV 行为再用所固定版本核对。

## 代码证据怎么记录

周笔记写明上游仓库、tag/commit、文件、函数、需要成立的顺序或条件，以及这段实现如何解释实验现象。链接优先使用固定 commit 的 permalink。只浏览默认分支时明确写“源码浏览版本未固定”；Python SQLite 的运行库版本与网页展示的源码版本也要分别记录。
