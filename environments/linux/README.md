# CPU Linux：主实验环境

## 第一周依赖与自检

- Python 3.7+，带标准库 `sqlite3`；记录内嵌的 SQLite 版本，不能只记录系统 `sqlite3` 命令版本。
- strace，供系统调用跟踪使用；需要当前环境允许跟踪自己启动的进程。
- Git；无需在第一周编译 SQLite、安装数据库服务或获取 root 权限来运行负载。

在仓库根目录执行：

```sh
python3 --version
python3 -c 'import sqlite3; print(sqlite3.sqlite_version)'
strace -V
python3 scripts/collect_system_info.py
```

Debian/Ubuntu 缺少依赖时，可在有包管理权限的实验环境安装：

```sh
sudo apt-get update
sudo apt-get install python3 strace git
```

受管理的开发机可请环境维护者提供 strace。若遇到 `Operation not permitted`，先检查容器/平台的 ptrace 策略，在允许跟踪自己子进程的 Linux 环境完成实验；记录原始错误。可以先完成负载正确性检查，跟踪验收继续保持未完成。

## 记录真实环境

`collect_system_info.py` 只输出 JSON，不写文件、不读取认证信息或环境变量。记录 Python/SQLite 版本、SQLite source id、内核、strace 版本、Git commit，以及当前目录所在挂载的 `df -T` 输出；平台不支持的工具以 null 表示。

第一周脚本还会在自己的 `result.json` 中记录负载、持久化配置和正确性结果。将必要字段摘入周笔记；原始文件放在 `artifacts/w01/`。

## 后续阶段按需准备

| 阶段 | 新增工具或环境 | 准备原则 |
|---|---|---|
| W05–W08、W23–W24 | RocksDB 的独立构建与 db_bench | 固定 commit、编译选项、数据目录与完整参数 |
| W09–W12 | etcd / etcdctl / etcdutl 与三节点目录 | 三个不同客户端/peer 端口；记录成员 ID，备份与恢复另用目录 |
| W13–W15 | 兼容版本的 JDK 与 Hadoop | 需要多个独立 DataNode；实验资源是否足够在阶段开始前确认 |
| W16–W18 | crushtool | 先验证放置映射，不要求部署完整 Ceph |
| W19–W22 | 与所选 TiKV 版本匹配的本地测试环境 | 先确认传统事务路径和跨 Region 请求，再观察优化路径 |

单机多个节点适合演示协议行为，不能推导跨机架可用性或真实修复带宽。
