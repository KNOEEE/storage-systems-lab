# SQLite：跟踪一次写入

对应 [W01：一次写入经过哪里？](../../curriculum/phase-01-local-storage/w01-write-path.md)。目标是把 SQLite 的写入请求与 Linux 系统调用对应起来，再解释系统调用之下有哪些尚未观察到的层。

## 前提与边界

- 在仓库根目录执行以下命令，使用 Python 3.7 或更高版本及其标准库 `sqlite3`，无需安装 SQLite 命令行客户端。
- 系统调用跟踪使用 Linux 和 `strace`。Mac 可以运行负载并核对数据，但不能据此提交 Linux 跟踪结论。
- 只使用可丢弃的测试目录。脚本要求输出目录不存在；重跑时使用 `baseline-02`、`traced-02` 等新目录。
- 本实验不做杀进程、断电、清空系统缓存或修改设备配置；这些行为不属于本周任务。

脚本用一个显式事务完成建表与插入：128 行，每行 256 字节 ASCII payload，固定为 rollback journal 的 `DELETE` 模式和 `synchronous=FULL`。这一周只识别数据库、journal 与同步调用；原子提交顺序的完整分析留给 W03。

## 1. 运行负载与正确性检查

```sh
python3 labs/sqlite-io/write_path.py --output-dir artifacts/w01/baseline
```

输出目录新增两个文件：

- `database.sqlite3`：本次实验数据库。
- `result.json`：Python / SQLite / 内核版本、SQLite source ID、实际 journal 与同步配置、数据库大小和页数，以及正常关闭再打开后的内容与完整性检查。

成功条件是 `verification.normal_reopen_passed` 为 `true`，`rows_after_reopen` 为 `128`，`content_matches` 为 `true`，`integrity_check` 为 `["ok"]`。先查看实际结果，不能直接把这些预期填成个人实验结论。`transaction_seconds` 只记录这次运行耗时；一次小事务、特别是受跟踪的运行，不构成吞吐或延迟基准测试。

## 2. 检查 strace

```sh
command -v strace
strace --version
```

若没有安装，可在自己有权限维护的 Debian / Ubuntu 实验环境安装：

```sh
sudo apt-get update
sudo apt-get install strace
```

没有安装权限时，换到支持 `strace` 的 Linux 环境；先运行负载也可以，但笔记中的“系统调用跟踪”要保留为待验证。容器或托管开发环境可能禁止 `ptrace`，即使装了工具也会出现 `Operation not permitted`。此时记录限制，使用获准跟踪的实验环境，不把报错当成数据库行为。

## 3. 跟踪新的运行

完成第 1 步后，`artifacts/w01/` 已存在。跟踪日志和负载使用新的文件名、目录，避免覆盖之前的证据：

```sh
strace -f -yy -tt -o artifacts/w01/sqlite.strace \
  -e trace=open,openat,close,pread64,pwrite64,read,write,fsync,fdatasync,ftruncate,unlink,unlinkat \
  python3 labs/sqlite-io/write_path.py --output-dir artifacts/w01/traced
```

`-yy` 将文件描述符与路径关联，`-tt` 帮助对照顺序。日志同时包含 Python 启动、JSON 报告和 SQLite 的 I/O，不能把所有 `write` 都算成数据库写入。先按路径筛出数据库及其 journal：

```sh
rg 'database\.sqlite3|fsync|fdatasync' artifacts/w01/sqlite.strace
```

没有 `rg` 时使用 `grep -E 'database\.sqlite3|fsync|fdatasync' artifacts/w01/sqlite.strace`。较旧的 strace 若不支持 `-yy`，可以改为 `-y`，再根据 `open/openat` 返回的文件描述符手工关联；记录实际使用的命令。

预期能识别数据库文件的打开、数据库或 journal 上的页写入、同步调用、关闭，以及 journal 的处理。具体系统调用名称、数量、页大小与顺序受 SQLite 版本、VFS、文件系统和平台影响，以日志为准。`write(1, ...)` 通常是标准输出中的 JSON；`write` 到 `result.json` 是实验记录，也不属于数据库事务。

## 4. 留下可解释的证据

在 `notes/weeks/w01.md` 中填写下表，每一行复制一两条实际日志并解释文件路径、文件描述符与返回值，不需要粘贴整份 trace：

| 观察对象 | 实际证据 | 能说明什么 | 不能说明什么 |
|---|---|---|---|
| 数据库或 journal 的打开 | 待填写 | 进程请求打开了哪个文件 | 不能推断物理介质位置 |
| 页写入 | 待填写 | 进程向内核提交了字节和文件偏移 | 不能断言一次调用对应一次设备写入 |
| 同步请求 | 待填写 | 进程请求了特定的同步语义；核对返回值 | 不能仅靠 trace 验证硬件断电保证 |
| 正常重开校验 | 待填写 | 正常关闭后数据可读且检查通过 | 没有覆盖进程崩溃、内核崩溃和断电 |

再画一张路径图：`Python sqlite3 → SQLite Pager / VFS → Linux 系统调用 → 内核页缓存 / 文件系统 → 设备与设备缓存`。系统调用之间的边界有本次日志作证；SQLite 内部模块对应官方设计文档，内核及设备内部行为没有被本工具直接跟踪。

最后用自己的话回答：

1. Python 的 SQL 执行、`pwrite64` 返回和 `fsync` / `fdatasync` 返回，各自处于哪一层？
2. 为什么 128 条 INSERT 不等于 128 次设备 I/O？
3. 吞吐、IOPS 与延迟的计量对象和单位分别是什么？这份 trace 是否足以给出设备 IOPS？
4. 你亲自观察到了什么，哪些结论仍依赖文件系统、VFS 或设备假设？

## 参考资料

- [SQLite 架构：Pager 与 OS Interface](https://www.sqlite.org/arch.html)
- [SQLite PRAGMA：synchronous](https://www.sqlite.org/pragma.html#pragma_synchronous)
- [SQLite PRAGMA：journal_mode](https://www.sqlite.org/pragma.html#pragma_journal_mode)
- [strace 官方说明：文件描述符、路径与系统调用过滤](https://strace.io/)
