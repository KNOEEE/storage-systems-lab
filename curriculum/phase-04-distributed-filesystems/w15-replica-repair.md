---
week: 15
phase: distributed-filesystems
estimated_hours: 5
status: planned
---

# W15：还能读取，是否代表恢复完成？

## 核心问题

一个 DataNode 故障后，系统何时发现、何时能继续服务、何时恢复目标副本数？

## 理论与设计（1.5 小时）

- [HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：心跳、块报告、数据复制与容错。
- [GFS 论文](https://research.google/pubs/the-google-file-system/)的故障检测与重新复制部分；比较两者的目标，不默认检测时延相同。

## 目标源码（1 小时）

固定 Hadoop 提交，定位 NameNode 中块管理与副本不足处理、DataNode 心跳 / 块报告入口。关注谁发现缺副本、谁安排复制以及谁实际传输数据。

## 验证步骤（2 小时）

1. 使用四个自己的测试 DataNode，目标三副本；上传后确认每个块的实际健康副本数。
2. 根据已记录 PID 停止一个持有目标块的 DataNode。记录停止、被识别失效、读取成功与补足副本四个时刻。
3. 在仍有可用副本时读取并核对校验和；观察新的副本位置和恢复流量的可用证据。
4. 若有限时间内未完成修复，记录相关超时配置、当前副本状态与日志，不能以读取成功代替修复完成。

## 交付物

- `notes/weeks/w15.md`：故障时间线、修复前后副本位置；完成 `reports/phase-04.md`。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 独立解释故障发生、检测、继续服务和恢复冗余。
- [ ] 通过块位置和数量核对修复，而不只看客户端读成功。
- [ ] 说明备用容量与放置约束对修复的影响。
- [ ] 回答阶段 4 过关问题，并标注未实际完成的步骤。

## 复盘

- 实际用时：
- 哪个阶段耗时最多：
- 还有哪些故障域未模拟：
