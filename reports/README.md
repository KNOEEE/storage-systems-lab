# 阶段与最终报告

阶段报告从 [模板](../templates/phase-report.md) 创建，按下面名称提交。所有阶段初始均未完成；第一阶段完成前不预填结论。

| 文件名 | 对应范围 | 必须包含的证据 |
|---|---|---|
| `phase-01.md` | W01–W04 | 本机写入路径、提交与恢复图、WAL/checkpoint 实验 |
| `phase-02.md` | W05–W08 | B-tree/LSM 对照、固定负载的配置实验 |
| `phase-03.md` | W09–W12 | 请求到响应时序、超时与选主记录、备份恢复核对 |
| `phase-04.md` | W13–W15 | 文件读写路径、继续服务与恢复冗余的分段时序 |
| `phase-05.md` | W16–W18 | 放置映射统计、故障域与副本/纠删码比较 |
| `phase-06.md` | W19–W22 | Region、Raft、MVCC 与跨分片事务的关联图 |
| `phase-07.md` | W23–W24 | 问题、假设、实现依据、实验、结论与代价 |

最终报告采用 [实验报告模板](../templates/experiment-report.md)，完整实验放 `benchmarks/reports/`，阶段报告链接该文件即可。
