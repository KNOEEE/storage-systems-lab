---
week: 19
phase: transactions
estimated_hours: 5
status: planned
---

# W19：一个复制组如何扩展成集群？

## 核心问题

键怎样落到 Region，Region 如何复制，客户端怎样找到它？PD 与每个 Raft 组的职责是什么？

## 理论与设计（1.5 小时）

- DDIA 第一版第 6 章：范围 / 哈希分区、路由与热点。
- [TiKV Data Sharding](https://tikv.org/deep-dive/scalability/data-sharding/)与其中的多 Raft 说明。将物理节点、Region、Region 副本分开画。

## 目标源码（1 小时）

固定 TiKV、PD 及客户端版本，定位 Region 元数据、客户端 Region cache 与 raftstore 的入口。选择一个简单 KV 请求，记录路由查询、RPC、复制与引擎访问的边界。

## 验证步骤（2 小时）

1. 启动隔离的本地测试环境，记录节点数、版本、各进程数据目录和 PD 入口；不连接工作集群。
2. 写入一组已知顺序的键，通过所用版本的诊断工具查看 Region 范围与副本位置。
3. 选择两个键，说明它们分别属于哪个 Region、当前 leader 在哪里。不要假设一个用户 key 等于一个 Region。
4. 画出请求路由与多 Raft 组图，对照实现说明 PD 不承担哪些逐请求工作。

## 交付物

- `notes/weeks/w19.md`：集群入口、键范围与副本表、请求路由图。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 区分节点、Region、peer 和 leader。
- [ ] 用实际元数据定位一个键的范围与副本。
- [ ] 解释单个 Raft 组与多组分片各解决什么问题。
- [ ] 记录客户端与服务端版本，避免跨版本拼接路径。

## 复盘

- 实际用时与环境障碍：
- 路由预测与观测差异：
- 下一周希望追踪哪次范围变化：
