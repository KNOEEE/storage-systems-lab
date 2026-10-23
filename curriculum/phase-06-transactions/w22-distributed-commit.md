---
week: 22
phase: transactions
estimated_hours: 5
status: planned
---

# W22：跨分片更新如何全部成功或全部失败？

## 核心问题

每个 Region 都有 Raft 后，一笔跨 Region 事务还需要哪些协议？客户端中途消失时，参与者如何确定结果？

## 理论与设计（1.5 小时）

- DDIA 第一版第 9 章：原子提交与两阶段提交；回顾第 7 章事务原子性。
- [TiKV Distributed Transaction](https://tikv.org/deep-dive/distributed-transaction/introduction/)与 [Percolator](https://tikv.org/deep-dive/distributed-transaction/percolator/)：传统 prewrite、primary commit 与锁清理。

## 目标源码（1 小时）

固定 TiKV 与客户端提交，定位 prewrite、commit、检查事务状态和锁解析的入口，配合一个恢复测试。明确本次是否使用传统路径，不能将 1PC 或 async commit 的行为套进传统时序。

## 验证步骤（2 小时）

1. 先从 Region 元数据确认两个目标键属于不同 Region，再构造同时修改它们的事务。
2. 运行正常事务，保留路由信息、客户端输出和可用服务端日志，画 primary / secondary 的时序。
3. 选择“prewrite 后客户端消失”或“primary 提交后响应丢失”中的一种失败，用上游故障注入测试验证；不具备注入条件则明确做协议推演。
4. 说明事务结果如何查询或由锁解析确认，分别标注 Region 内复制保证与跨 Region 原子性。

## 交付物

- `notes/weeks/w22.md`：跨 Region 证据、传统事务时序与失败恢复；完成 `reports/phase-06.md` 的组合架构图。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 提供两个键确实跨 Region 的证据。
- [ ] 解释 primary、secondary 与事务状态的关系。
- [ ] 区分“已提交但尚未清理完锁”与“事务未决定”。
- [ ] 回答 Raft 为什么不能替代跨分片原子提交。

## 复盘

- 实际用时：
- 哪条优化路径需要留到以后：
- 哪个失败场景尚未验证：
