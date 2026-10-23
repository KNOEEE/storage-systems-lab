# 仓库辅助工具

均只使用 Python 标准库，兼容 Python 3.7+；从仓库根目录执行：

```sh
python3 scripts/collect_system_info.py
python3 scripts/validate_curriculum.py
```

- `collect_system_info.py`：输出实际环境的 JSON，不读取认证或环境变量，不修改系统配置。
- `validate_curriculum.py`：检查 24 周编号、阶段归属、周页元信息和必要段落，以及 Markdown 的本地文件链接；网络链接不在此检查中。

第一周实验入口在 [SQLite lab](../labs/sqlite-io/README.md)。课程验收仍由笔记中的证据完成。

## 仓库搭建时的验证

2026-10-23，在 Linux / Python 3.7.3 / SQLite 3.27.2 上运行负载，128 行内容匹配、正常重开及完整性检查通过。重复输出目录被拒绝且已有结果保持不变。

使用临时目录内解包的 strace 4.26，在允许 ptrace 的执行环境验证了实验页的跟踪参数，实际观察到 journal/数据库的 `pwrite64`、`fdatasync` 和文件关闭。没有把 strace 安装到系统；普通受限沙箱的 ptrace 报错也已核对，对应环境指南中的限制。

以上是脚本可运行性的验证，不是学习者的周任务成果，也不包含断电或性能结论。
