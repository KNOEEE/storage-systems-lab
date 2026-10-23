# Storage Systems Lab

从本机持久化到分布式存储：原理、架构、源码与实验。

Learning storage systems through fundamentals, architecture, source-code walkthroughs, and hands-on experiments.

这是一条 **24 周、每周约 5 小时**的学习路线。以知识体系为主线，用 SQLite、RocksDB、etcd、HDFS、Ceph、TiKV 回答逐步深入的问题。OSTEP 与 DDIA 按主题选读，关键位置补充论文；每周把阅读、代码和实验连成一个完整问题。

## 学完要能做什么

- 画出一次写入从应用、数据库缓存、操作系统到存储设备的路径，解释提交与持久化的条件。
- 对比 B-tree 和 LSM 的数据组织，结合工作负载分析读、写、空间放大。
- 解释复制、共识、线性一致性、分片、MVCC 和原子提交分别提供的保证。
- 从一个系统的接口追到关键模块、函数和测试，用证据说明设计取舍。
- 用固定负载、环境记录和单变量实验完成一份可复现的技术报告。

## 从这里开始

1. 浏览 [24 周路线](ROADMAP.md)，确认当前阶段与本周问题。
2. 打开 [第一周：一次写入经过哪里？](curriculum/phase-01-local-storage/w01-write-path.md)。
3. 按 [Linux 环境说明](environments/linux/README.md) 检查 Python、SQLite 与 strace。
4. 阅读指定材料，先画预测路径，再运行 [SQLite 写入实验](labs/sqlite-io/README.md)。
5. 在 [第一周笔记](notes/weeks/w01.md) 填入原理、源码证据、实测结果与未验证事项，逐项完成周页的验收。

在仓库根目录运行下面的最小实验即可开始；只用 Python 标准库，不要求安装 SQLite 命令行或编译数据库：

```sh
python3 scripts/collect_system_info.py
python3 labs/sqlite-io/write_path.py --output-dir artifacts/w01/baseline
```

每次实验使用新的输出目录。系统调用跟踪的完整命令见实验说明；仅跑通最小实验还没有完成第一周。

## 阶段安排

| 阶段 | 周次 | 主问题 | 配套系统 | 阶段产出 |
|---|---|---|---|---|
| [本机存储](curriculum/phase-01-local-storage/README.md) | W01–W04 | 字节如何被组织、提交与恢复？ | SQLite | 写入路径、提交恢复图与 WAL 实验 |
| [存储引擎](curriculum/phase-02-storage-engines/README.md) | W05–W08 | 读写性能的代价在哪里？ | RocksDB | B-tree/LSM 对照与配置实验 |
| [复制与一致性](curriculum/phase-03-replication/README.md) | W09–W12 | 多份数据如何在故障下保持正确？ | etcd / raft | 提交应用时序图与故障记录 |
| [分布式文件系统](curriculum/phase-04-distributed-filesystems/README.md) | W13–W15 | 文件如何分块、复制与修复？ | HDFS / GFS 论文 | 文件读写与副本修复时序 |
| [数据放置](curriculum/phase-05-placement/README.md) | W16–W18 | 数据放哪里，能承受哪些故障？ | Ceph | CRUSH 映射实验与容错比较 |
| [分布式事务](curriculum/phase-06-transactions/README.md) | W19–W22 | 分片、版本与事务如何组合？ | TiKV / PD | 跨 Region 事务与恢复分析 |
| [综合验证](curriculum/phase-07-capstone/README.md) | W23–W24 | 如何用实验证明一个性能判断？ | 回到 RocksDB | 可复现的技术报告 |

详细的每周“理论—设计/源码—实验”配对见 [ROADMAP.md](ROADMAP.md)。所有进度初始为 planned；完成验收后再更新，不按日历自动推进。

## 每周怎么学

| 理论与设计 | 目标代码 | 实验与分析 | 闭卷总结 |
|---|---|---|---|
| 1.5 小时 | 1 小时 | 2 小时 | 0.5 小时 |

每周只维护一份整合笔记：**核心问题 → 原理假设 → 代码证据 → 实验结果 → 结论与边界**。阶段结束再汇总报告。源码只读解决本周问题的入口、结构、函数和测试；环境搭建超时则记录阻塞，调整任务，不靠跳过实验来标记完成。

## 仓库结构

```text
ROADMAP.md     24 周总路线，每周阅读、代码、实验与产出
curriculum/    分阶段课程、每周任务与验收标准
labs/          小型、独立、可重复执行的实验
projects/      跨周演进的研究项目约定
benchmarks/    固定负载、原始结果和性能报告约定
environments/  Linux 主环境与 macOS 的职责边界
upstreams/     上游源码入口、版本与 commit 记录
notes/         每周整合笔记与长期知识索引
reports/       阶段成果与综合报告
templates/     每周笔记、阶段报告与实验报告模板
scripts/       环境信息采集和课程链接检查
artifacts/     本地数据库、trace 等生成物，默认不提交
```

## 材料与范围

- [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/)：本机 I/O、文件系统和持久化，选读第 36、39、40、42 章等对应主题。
- [DDIA](https://dataintensive.net/)：存储引擎、复制、分片、事务与一致性。本课程章节号统一采用**第一版**；其他版本按主题定位。
- [MIT 6.5840](https://pdos.csail.mit.edu/6.824/)：只补对应讲义与论文，不额外要求完成整门课。
- 上游项目与原始论文入口统一见 [upstreams](upstreams/README.md)；开始源码实验前填写 [版本记录](upstreams/repos.yaml)。

第一轮聚焦上述六个系统，先理解传统提交路径和最小故障模型。CacheLib、Dgraph、3FS 等可在主线完成后按兴趣扩展。性能结论同时报告持久化设置、资源与尾延迟；进程退出实验和系统调用跟踪的结论必须限定在实际覆盖的故障范围内。

## 进度与仓库检查

- [ ] W01–W04：本机存储
- [ ] W05–W08：存储引擎
- [ ] W09–W12：复制与一致性
- [ ] W13–W15：分布式文件系统
- [ ] W16–W18：数据放置
- [ ] W19–W22：分布式事务
- [ ] W23–W24：综合验证

```sh
python3 scripts/validate_curriculum.py
```

该检查验证 24 周覆盖、阶段归属、周页必要字段及本地 Markdown 链接；它不代替学习验收或数据库正确性实验。
