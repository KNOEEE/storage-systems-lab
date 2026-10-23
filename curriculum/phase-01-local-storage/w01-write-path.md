---
week: 1
phase: local-storage
estimated_hours: 5
status: planned
---

# W01：一次写入经过哪里？

本周核心问题：**执行一次 SQLite 事务时，哪些字节经过哪些层？SQL 成功、写系统调用返回和同步请求成功分别意味着什么？**

前置知识：能阅读简单 Python/SQL，知道进程、内存和文件的大致含义。不要求熟悉数据库源码，也不要求编译 SQLite。

## 目标

- 画出应用、SQLite Pager/VFS、系统调用、内核页缓存/文件系统和设备的路径，区分 SQLite 缓存与 OS 页缓存。
- 从真实 trace 识别数据库与 journal 的打开、写入、同步及关闭，关联文件描述符和返回值。
- 说明吞吐、IOPS、延迟的计量对象与单位，解释为什么系统调用次数不是设备 IOPS。
- 将观察、实现依据和未验证事项写在同一份笔记中。

## 五小时安排

可按 5 次、每次 1 小时完成；下面的步骤始终追同一个写入问题。

| 次序 | 时间 | 阅读 / 操作 | 当场留下的证据 |
|---|---:|---|---|
| 1 | 60 分钟 | OSTEP I/O 与文件接口选读；运行环境自检 | 一张预测路径图、版本记录、3 个待验证问题 |
| 2 | 60 分钟 | 30 分钟读 SQLite 架构/VFS；30 分钟定位源码接口 | 两种缓存的区别；xWrite/xSync 到 Unix 实现的映射 |
| 3 | 60 分钟 | 30 分钟继续看目标代码；30 分钟跑通固定负载 | 文件/函数记录；正常重开正确性证据 |
| 4 | 60 分钟 | 在 Linux 对一次新的运行做 strace，按路径筛选 | 打开、页写入、同步、关闭各一组真实日志 |
| 5 | 60 分钟 | 30 分钟整理观察与预测；30 分钟闭卷重画和回答 | 完整的 [第一周笔记](../../notes/weeks/w01.md)、验收结果 |

总计：理论与设计 1.5h，代码 1h，实验与分析 2h，闭卷总结 0.5h。安装环境在第 1 次内处理；若工具/权限问题持续超过 20 分钟，记录阻塞并先完成阅读、代码与负载，跟踪部分仍待完成。

## 理论与设计阅读：带着预测去读

1. [OSTEP 第 36 章：I/O Devices](https://pages.cs.wisc.edu/~remzi/OSTEP/file-devices.pdf)：重点理解 OS、驱动和设备的位置，建立层次图。
2. [OSTEP 第 39 章：Files and Directories](https://pages.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf)：选读打开/读写、偏移与同步相关内容。记录 `write` 与同步请求之间的差别，不要求本周通读整章。
3. [SQLite Architecture](https://sqlite.org/arch.html)：只读 B-Tree、Page Cache、OS Interface 三节，找到 Pager 与 VFS 的职责。
4. [VFS](https://sqlite.org/vfs.html) 与 [sqlite3_io_methods](https://sqlite.org/c3ref/io_methods.html)：只看 `xWrite`、`xSync` 的接口含义。

先在笔记中写下三个预测：哪些文件会被打开？数据库写入前后可能出现哪些调用？哪些步骤仅靠 strace 无法直接看到？完整原子提交的推导放在 W03；本周先识别层与接口。

## 目标代码：只追文件 I/O 这一段

在 [官方 SQLite 镜像](https://github.com/sqlite/sqlite) 浏览或检出源码；把实际 tag/commit 填到 [版本清单](../../upstreams/repos.yaml)。Python 绑定运行库的版本和 source ID 从实验输出获取，源码浏览与运行版本分别记录；不同版本只能做模块级对照，不能直接认定行号或分支相同。

| 入口 | 本周只回答的问题 |
|---|---|
| `src/sqlite.h.in` 中的 `sqlite3_io_methods` | 谁提供 `xWrite`、`xSync` 这类文件操作？ |
| `src/os.c` 中的 `sqlite3OsWrite` / `sqlite3OsSync` | SQLite 如何把调用转给 VFS 文件方法？ |
| `src/os_unix.c` 中的 `unixWrite` / `unixSync` 及调用的辅助函数 | 哪一层真正调用 POSIX 写入/同步接口？有哪些平台条件分支？ |
| `src/pager.c`（本周只定位） | 哪一模块管理数据库页、提交和恢复？ |

如果有同级 SQLite 源码检出，可在其中用以下方式定位，不按文件从头读：

```sh
rg -n 'sqlite3OsWrite|sqlite3OsSync' src/os.c
rg -n 'unixWrite|unixSync|seekAndWrite|full_fsync' src/os_unix.c
```

交付 3–5 个关键入口的“文件/函数—职责—证据”记录，连成 `Pager → OS wrapper → VFS → Unix 文件操作` 的局部路径即可。

## 实验：预测 → 运行 → 对照

完整命令与排错见 [SQLite I/O lab](../../labs/sqlite-io/README.md)。在仓库根目录进行。

### 1. 环境与基线（30 分钟）

```sh
python3 scripts/collect_system_info.py
python3 labs/sqlite-io/write_path.py --output-dir artifacts/w01/baseline
```

脚本在一个显式事务中建表并插入 128 行，每行 256 字节 payload，固定 `journal_mode=DELETE` 与 `synchronous=FULL`；关闭后重开，核对所有内容与完整性。把 `result.json` 的版本、实际配置和校验字段摘入笔记。数据库与 JSON 留在本地生成物目录。

已有目录会拒绝复用。再次运行改成 `baseline-02`；不要删除旧证据来迁就命令。

### 2. 系统调用跟踪（60 分钟）

完成基线后，父目录 `artifacts/w01/` 已存在。以下命令用于第一次跟踪；重跑时同时更换 trace 文件名和负载目录：

```sh
strace -f -yy -tt -o artifacts/w01/sqlite.strace \
  -e trace=open,openat,close,pread64,pwrite64,read,write,fsync,fdatasync,ftruncate,unlink,unlinkat \
  python3 labs/sqlite-io/write_path.py --output-dir artifacts/w01/traced
rg 'database\.sqlite3|fsync|fdatasync' artifacts/w01/sqlite.strace
```

从 trace 中各选一组实际证据：

- 数据库或 journal 的 `open/openat`：路径、打开标志、返回的文件描述符。
- 文件写入：对象、偏移、字节数、返回值；可能是 `pwrite64` 或其他平台路径。
- `fsync/fdatasync`：哪个描述符同步、调用是否成功；若没有出现，检查版本、配置和跟踪条件并记录，不补造日志。
- 关闭或 journal 处理：说明与你前面的预测如何对应。

区分 stdout、`result.json` 与数据库 I/O。trace 涵盖 Python 启动、事务与重开校验，不代表其中每条调用都发生在 COMMIT 内。

### 3. 解释与计量练习（30 分钟）

将真实 trace 的片段连回最初路径图，标记本工具观察到的边界：

```text
Python sqlite3 / SQL
        ↓
SQLite B-tree / Pager（数据库页缓存）
        ↓
SQLite VFS → 写入 / 同步系统调用  ← 本次 trace 的观察边界
        ↓
Linux 内核页缓存 / 文件系统
        ↓
块层 / 驱动 → 设备与设备缓存
```

用两个**计算练习，不是实测结果**核对单位：10 秒传输 100 MiB，对应 10 MiB/s；10 秒完成 1,000 次已定义的操作，对应 100 ops/s。只有明确为设备 I/O 时才能称为设备 IOPS。延迟是一次操作的耗时，平均值和 P99 回答不同的问题；系统调用次数与持续时间均不能直接替代设备指标。

## 交付物

- [notes/weeks/w01.md](../../notes/weeks/w01.md)：填写预测、原理、目标代码、路径图、真实证据与闭卷回答。
- 本地 `artifacts/w01/baseline/result.json`、`artifacts/w01/traced/result.json` 与 trace；生成物默认不提交。
- [upstreams/repos.yaml](../../upstreams/repos.yaml)：运行版本/source ID，和实际浏览或检出的源码版本。

## 验收标准

- [ ] 不看资料画出写入路径，明确 SQLite 缓存与 Linux 页缓存的位置。
- [ ] 用文件与函数解释 VFS 的作用；源码浏览版本与运行版本分别记录。
- [ ] 跑通固定负载，正常重开后 128 行内容匹配，`integrity_check` 为 `ok`。
- [ ] 提供真实文件打开、写入、同步和关闭/处理的证据；能关联描述符、路径与返回值。
- [ ] 解释 SQL 执行成功、写调用返回、同步调用成功三个状态的含义及成立条件。
- [ ] 区分吞吐、IOPS 和延迟；解释 INSERT 数量、系统调用数量、设备 I/O 数量为什么不等价。
- [ ] 明确正常重开并未验证断电恢复，strace 也没有观察设备内部行为。

工具受限时可以继续其他步骤，但跟踪项未完成就保持 `in-progress`。

## 复盘：最后 30 分钟

关掉资料和代码，重画路径并口述：用户态缓存和内核缓存是什么关系？为什么一条 INSERT 不对应一次磁盘写入？`fsync` 成功是否足以从这个实验推断所有断电情况？

在周笔记填写实际用时、最意外的现象、一个仍未解释的问题。全部验收完成后再更新本页状态。下一周进入 [阶段目录](README.md) 的 W02，回答“如何在文件中找到一条记录？”
