# 实验环境

主环境采用 Linux。第一阶段只需 Python 标准库中的 SQLite 和 strace；后续按阶段安装依赖，每次记录真实版本、启动参数和资源。跨系统实验可用独立容器或独立目录，不建立一个包含所有系统的全能环境。

| 环境 | 适合承担的任务 | 需要额外核对 |
|---|---|---|
| [CPU Linux](linux/README.md) | 全路线主环境，SQLite 跟踪，RocksDB，etcd/HDFS 等测试集群 | ptrace 权限、文件系统、可用 CPU/内存/磁盘 |
| macOS | 阅读、画图、Python/SQLite 正确性和部分单机实验 | strace 属于 Linux；系统调用与同步语义不能照搬，跟踪部分回 Linux 完成 |
| Linux 容器或云开发机 | 隔离进程、依赖和小型集群 | 同宿主进程不能验证机器级故障域；overlay/网络盘结果不能当作裸机 SSD 性能 |

每次性能实验都在 [实验报告](../templates/experiment-report.md) 中记录实际环境。资源不足时先缩小数据量，保持问题与对照条件一致；任何未执行的部分标为待验证。
