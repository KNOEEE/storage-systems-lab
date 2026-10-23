---
week: 13
phase: distributed-filesystems
estimated_hours: 5
status: planned
---

# W13：文件名如何变成数据位置？

## 核心问题

客户端读一个大文件时，哪些请求发给元数据服务，哪些直接发给存储节点？

## 理论与设计（1.5 小时）

- [GFS 论文](https://research.google/pubs/the-google-file-system/)：设计假设、整体架构、元数据与客户端交互。
- [HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：NameNode、DataNode、块与客户端职责。
- 回顾 OSTEP 的 Files and Directories。记录 GFS 与 HDFS 的设计对应和差异，不能直接套用细节。

## 目标源码（1 小时）

固定 Hadoop 提交，定位 `DFSClient`、`DFSInputStream` 和获取块位置的逻辑，沿一次 open / read 分清元数据 RPC 和数据读取。只追一段跨块读取。

## 验证步骤（2 小时）

1. 先跑通隔离的 HDFS 测试环境，记录配置、块大小、副本因子和节点信息。
2. 生成大于配置块大小的固定内容文件，保留校验和并上传。
3. 用所用版本的文件系统检查或管理工具查看块与副本位置，记录文件名到块标识的映射。
4. 下载并核对校验和，画一次读取路径，注明 NameNode 是否转发文件内容。

## 交付物

- `notes/weeks/w13.md`：环境入口、块布局、校验和与读取图。

## 验收标准（含 0.5 小时闭卷总结）

- [ ] 解释命名空间、块标识和节点位置的区别。
- [ ] 用上传文件的实际布局说明跨块读取。
- [ ] 指出元数据请求与文件字节传输各自的路径。
- [ ] 记录至少一处 GFS 与所用 HDFS 不能等同的机制。

## 复盘

- 实际用时与部署障碍：
- 逻辑架构与实际请求路径的差异：
- 尚未追到的异常路径：
