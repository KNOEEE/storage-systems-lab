# 性能实验约定

W08 和 W23–W24 主要用 RocksDB 自带的 `db_bench`。先写清问题和负载，再运行工具；SQLite 的系统调用跟踪不承担设备性能评测。

1. 在 [workloads](workloads/README.md) 记录固定的数据量、键值大小、访问分布、并发、时长和完整参数。
2. 记录版本、commit、编译选项、环境、缓存状态及持久化配置。
3. 每轮保存原始输出到 [results](results/README.md)；大文件默认忽略。
4. 使用 [实验报告模板](../templates/experiment-report.md) 在 [reports](reports/README.md) 写结论。

同时观察吞吐、延迟分位数、空间、CPU/I/O 以及与假设相关的指标。控制一个变量，记录重复次数和全部异常。变更同步或 WAL 设置属于保证变化，应单独报告，不能归结为无条件加速。
