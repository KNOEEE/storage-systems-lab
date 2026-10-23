# 阶段 5：数据放置、故障域与存储接口

- 周次：W16–W18；配套项目：Ceph。
- 进入条件：能够解释数据与元数据分离、副本确认和冗余修复。

## 学习顺序

1. [W16：对象、块与文件接口](w16-storage-interfaces.md)
2. [W17：CRUSH 放置与扩容](w17-crush-placement.md)
3. [W18：多副本与纠删码](w18-erasure-coding.md)

把接口语义、数据放置和故障容忍分开解释，再组合成设计。第一轮使用 `crushtool` 模拟映射，不要求搭完整 Ceph 集群。映射实验不能证明恢复速度或线上可用性。

## 阶段成果

一份映射变化实验和一页副本 / 纠删码比较，按 [阶段模板](../../templates/phase-report.md) 写入 `reports/phase-05.md`。

过关问题：**为什么三份数据不等于能承受任意两台机器故障？你的规则依赖哪些故障域假设？**

## 主要资料

- DDIA 第一版第 6 章：分区与重平衡相关主题。
- [Ceph Architecture](https://docs.ceph.com/en/latest/architecture/)。
- [crushtool 手册](https://docs.ceph.com/en/latest/man/8/crushtool/)。`latest` 指向开发文档，实际实验须选择已安装版本的文档。
