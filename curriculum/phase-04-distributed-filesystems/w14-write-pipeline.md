---
week: 14
phase: distributed-filesystems
estimated_hours: 5
status: planned
---

# W14：多副本写入为什么要设计流水线？

## 核心问题

客户端发送的一段数据，怎样流过多个副本并得到确认？数据传输、控制请求和持久化承诺有何区别？

## 理论与设计（1.5 小时）

- [GFS 论文](https://research.google/pubs/the-google-file-system/)的交互部分：分别看控制流与数据流。
- [HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)的数据流水线；回顾 DDIA 第一版第 5 章的复制确认。

## 目标源码（1 小时）

固定 Hadoop 提交，定位客户端 `DataStreamer`、数据 packet、响应处理和服务端接收 / 确认结构。核对 `flush`、`hflush`、`hsync` 的 API 说明和当前路径，不能将任意 ACK 都解释成设备已持久化。

## 验证步骤（2 小时）

1. 使用 W13 环境与相同文件生成方式，设置明确的副本目标并上传。
2. 通过现有日志或小范围调试观察一段 packet 的发送与 ACK，记录实际工具与配置，避免全局打开大量调试日志。
3. 画出 Client 与各 DataNode 的时序，逐步标明数据字节、控制信息和确认。
4. 用一个正常完成的文件核对校验和；对中途节点异常路径先做源码推演，实际故障留给 W15。

## 交付物

- `notes/weeks/w14.md`：packet 与 ACK 时序、成功条件、相关源码入口。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 分清数据流与控制流。
- [ ] 解释流水线如何影响网络使用与确认延迟。
- [ ] 给出本次使用的写入 / 同步 API 对应保证。
- [ ] 不将 GFS 的租约与写入协议直接当成 HDFS 实现。

## 复盘

- 实际用时：
- 最容易误读的确认事件：
- W15 准备验证的故障预测：
