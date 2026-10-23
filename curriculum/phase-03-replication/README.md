# 阶段 3：复制、一致性与故障恢复

- 周次：W09–W12；配套项目：etcd 与 `etcd-io/raft`。
- 进入条件：能区分内存状态、日志持久化与数据库可见状态。

## 学习顺序

1. [W09：超时与结果未知](w09-timeouts.md)
2. [W10：Raft 日志复制](w10-raft-log.md)
3. [W11：读取保证](w11-consistency.md)
4. [W12：快照与恢复](w12-snapshot-recovery.md)

先理解故障与时间的不确定性，再将论文中的状态对应到库的事件处理和宿主集成。第一轮不要求实现完整 Raft。集群操作只针对自己创建的本地测试节点。

## 阶段成果

一张“请求—日志—提交—应用—响应”图和一份故障记录，按 [阶段模板](../../templates/phase-report.md) 写入 `reports/phase-03.md`。

过关问题：**哪些步骤必须先持久化？写请求超时后，凭什么判断它是否生效？**

## 主要资料

- DDIA 第一版第 5 章复制、第 8 章分布式故障、第 9 章一致性与共识。
- [Raft 论文扩展版](https://raft.github.io/raft.pdf)：第 5 节与第 7 节。
- [raft 集成说明](https://github.com/etcd-io/raft)、[etcd API 保证](https://etcd.io/docs/v3.6/learning/api_guarantees/)、[灾难恢复](https://etcd.io/docs/v3.6/op-guide/recovery/)。etcd 命令使用与安装版本匹配的文档。
