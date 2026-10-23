---
week: 17
phase: placement
estimated_hours: 5
status: planned
---

# W17：数据放在哪里，扩容后怎样变化？

## 核心问题

怎样在满足故障域约束的同时分布数据？新增设备后，哪些映射需要改变？

## 理论与设计（1.5 小时）

- DDIA 第一版第 6 章：重平衡与路由。
- [Ceph Architecture](https://docs.ceph.com/en/latest/architecture/)中 CRUSH、Pool、PG 与故障域的关系。
- [crushtool 手册](https://docs.ceph.com/en/latest/man/8/crushtool/)及其链接的 CRUSH 论文设计部分。实际命令选用工具版本对应文档。

## 目标源码（1 小时）

固定 Ceph 提交，定位 CRUSH map 的 bucket、rule 表示与规则执行逻辑；从 `crushtool` 的测试入口追一次映射。说明模拟输入与真实对象 / PG 映射之间的关系。

## 验证步骤（2 小时）

1. 用 `crushtool` 构造小规模、等权且层级明确的测试 map，设置跨 host 的三副本规则，保存文本与编译后 map。
2. 固定输入范围与样本数，导出映射，统计每设备分布并检查副本是否跨 host。
3. 新增一台 host 及其设备，保持原设备标识和权重不变，重复完全相同的输入。
4. 比较每个输入的副本集合，分别报告“任一副本集合发生变化的输入比例”和分布差异，写清统计定义。

## 交付物

- `notes/weeks/w17.md`：map、规则、重现命令与变化比例；原始映射放 `artifacts/w17/`。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 能解释设备、bucket、rule 和故障域。
- [ ] 用程序或表格检查副本跨故障域约束。
- [ ] 扩容前后使用相同输入，明确变化指标口径。
- [ ] 不把映射变化比例直接当成实际迁移字节或恢复时间。

## 复盘

- 实际用时：
- 分布是否符合预期，偏差可能来自什么：
- 本次工具模拟未覆盖什么：
