# 阶段 1：本机 I/O、页组织与崩溃恢复

- 周次：W01–W04；每周约 5 小时。
- 配套项目：SQLite；主要实验环境为 Linux。
- 进入条件：能执行命令、阅读基础 Python 或 C，区分进程与文件。

## 学习顺序

1. [W01：一次写入经过哪里？](w01-write-path.md)
2. [W02：页与 B-tree](w02-pages-and-btree.md)
3. [W03：rollback journal 与崩溃恢复](w03-crash-recovery.md)
4. [W04：WAL 与 checkpoint](w04-wal-checkpoint.md)

用 OSTEP 的 I/O、文件系统和崩溃一致性解释 SQLite 的 OS Interface、B-tree、Pager 和日志。第一轮不进入 SQL 解析器与查询优化。

## 阶段成果

把写入路径、两种日志模式和恢复条件整理成图，附能复现的实验。按 [阶段模板](../../templates/phase-report.md) 写入 `reports/phase-01.md`。

过关问题：**“写入成功”“事务提交”“数据文件已经更新”“断电后可恢复”分别需要什么条件？** 明确进程异常退出并未模拟断电。

## 主要资料

- [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/)：I/O Devices、Files and Directories、File System Implementation、Crash Consistency。
- DDIA 第一版第 3 章 B-tree，第 7 章原子性与隔离性。
- [SQLite Architecture](https://sqlite.org/arch.html)、[Atomic Commit](https://sqlite.org/atomiccommit.html)、[WAL](https://sqlite.org/wal.html)。
