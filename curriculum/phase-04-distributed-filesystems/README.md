# 阶段 4：分布式文件系统

- 周次：W13–W15；配套项目：HDFS，设计对照使用 GFS 论文。
- 进入条件：理解复制确认、故障检测和副本恢复的区别。

## 学习顺序

1. [W13：元数据与读取路径](w13-metadata.md)
2. [W14：写入流水线](w14-write-pipeline.md)
3. [W15：副本修复](w15-replica-repair.md)

GFS 用于理解设计思路，HDFS 文档、代码和实验负责验证实际实现；不要把两者的具体机制等同。只研究文件存储，不展开 YARN 和 MapReduce。

测试集群可使用四个 DataNode 和目标三副本，给副本修复保留接收节点。先完成小规模启动与上传，再进行故障实验；无需部署生产 HA 集群。

## 阶段成果

文件读写时序图和“故障—检测—继续服务—恢复冗余”过程图，按 [阶段模板](../../templates/phase-report.md) 写入 `reports/phase-04.md`。

过关问题：**文件还能读取，与系统已恢复目标副本数之间有什么差别？**

## 主要资料

- [The Google File System](https://research.google/pubs/the-google-file-system/)：设计假设、架构、交互与容错部分。
- [HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)。使用所安装版本对应的架构、命令与部署文档。
