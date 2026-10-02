"""清理软删除超过 30 天的上传文件。

直接运行时只列出候选文件；传入 --apply 才会删除磁盘文件和数据库记录。
旧记录如果没有 deleted_time，无法判断删除已过多久，因此不会被清理。
"""

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4


# 软删除后保留的天数。只有删除时间早于“现在减 30 天”的记录才符合条件。
RETENTION_DAYS = 30


def safe_upload_path(upload_root: Path, proj_id: int, standard_name: str) -> Path:
    """生成文件路径，并确认它始终位于对应项目的上传目录内。"""
    # Path(...).name 只取路径最后的文件名，例如 "a/b.pdf" 的 name 是 "b.pdf"。
    # 若它与原值不同，说明数据库里的值带了目录，不能直接拼接成待删除路径。
    if not standard_name or Path(standard_name).name != standard_name:
        raise ValueError(f"无效的服务器文件名：{standard_name!r}")

    project_dir = upload_root / str(proj_id)
    path = project_dir / standard_name
    # is_symlink() 判断路径本身是否为符号链接，返回 True 或 False。
    # 符号链接相当于指向别处的“跳转入口”，清理时不能顺着它删到其他目录。
    if project_dir.is_symlink() or path.is_symlink():
        raise ValueError(f"拒绝清理符号链接：{path}")
    # resolve() 把路径变为绝对路径，并处理 .. 和符号链接；parent 取上一级目录。
    # 两次比较分别确认项目目录属于 uploads、文件属于该项目目录。
    if project_dir.resolve().parent != upload_root or path.resolve().parent != project_dir.resolve():
        raise ValueError(f"文件路径超出项目上传目录：{path}")
    return path


def backup_database(connection: sqlite3.Connection, db_path: Path) -> Path:
    # 执行永久清理前先备份数据库。时间加随机后缀可避免多次运行时覆盖备份。
    # strftime() 把时间格式化成字符串；uuid4().hex 生成随机十六进制字符。
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # with_name() 保留原目录，只替换文件名；db_path.stem 是不带扩展名的名字。
    backup_path = db_path.with_name(
        f"{db_path.stem}.before-cleanup-{stamp}-{uuid4().hex[:8]}{db_path.suffix}"
    )
    # sqlite3.connect() 打开备份目标；connection.backup() 把当前数据库复制过去。
    backup = sqlite3.connect(backup_path)
    try:
        connection.backup(backup)
    finally:
        # 无论复制成功还是抛异常，都关闭备份数据库连接。
        backup.close()
    return backup_path


def clean(connection: sqlite3.Connection, db_path: Path, upload_root: Path,
          cutoff: datetime, apply: bool) -> int:
    # isoformat(sep=" ") 把 datetime 转成“年-月-日 时:分:秒”形式的字符串。
    # SQLite 中的时间存成文本；这里用相同格式做“早于截止时间”的比较。
    cutoff_text = cutoff.isoformat(sep=" ")
    # 只选已软删除、删除时间已知且超过保留期的记录。
    # 问号是 SQL 参数占位符，实际值作为第二个参数传入。
    rows = connection.execute(
        "SELECT fid, proj_id, standard_name FROM upload_file "
        "WHERE is_deleted = 1 AND deleted_time IS NOT NULL AND deleted_time <= ? "
        "ORDER BY fid",
        (cutoff_text,),
    ).fetchall()  # fetchall() 一次取出查询结果的所有行，组成列表。

    # 删除前先检查所有候选路径；其中任意一个不安全，就不开始本轮清理。
    planned = [(fid, proj_id, standard_name,
                safe_upload_path(upload_root, proj_id, standard_name))
               for fid, proj_id, standard_name in rows]

    print(f"清理截止时间：{cutoff}")
    print(f"符合条件：{len(planned)} 条")
    # is_file() 检查路径是否指向普通文件，返回布尔值；这里仅用于显示状态。
    for fid, _, _, path in planned:
        print(f"  #{fid} {'存在' if path.is_file() else '文件缺失'}：{path}")

    # 默认只预览。用户明确传入 --apply 后才会继续执行删除。
    if not apply:
        print("预览模式：未删除文件或数据库记录。")
        return 0
    if not planned:
        print("没有需要清理的记录。")
        return 0

    # 先完成数据库备份，再处理磁盘文件和数据库记录。
    backup_path = backup_database(connection, db_path)
    print(f"数据库备份：{backup_path}")
    cleaned = 0
    failed = 0
    for fid, proj_id, standard_name, _ in planned:
        try:
            # 对当前记录开启写事务，并重新读取状态：预览后用户可能已经恢复了文件。
            # BEGIN IMMEDIATE 会提前取得 SQLite 写锁，减少复核与删除之间的状态变化。
            connection.execute("BEGIN IMMEDIATE")
            # fetchone() 只取一行；查不到时返回 None，便于识别记录已变化。
            current = connection.execute(
                "SELECT proj_id, standard_name FROM upload_file "
                "WHERE fid = ? AND is_deleted = 1 "
                "AND deleted_time IS NOT NULL AND deleted_time <= ?",
                (fid, cutoff_text),
            ).fetchone()
            if current != (proj_id, standard_name):
                # rollback() 撤销当前尚未提交的数据库事务。
                connection.rollback()
                print(f"  #{fid} 状态已变化，跳过。")
                continue

            # 再检查一次路径。is_file() 为 True 时，unlink() 删除这个磁盘文件。
            # exists() 判断路径是否存在；文件缺失可继续清理记录，其他类型则报错。
            path = safe_upload_path(upload_root, proj_id, standard_name)
            if path.is_file():
                # unlink() 删除 path 指向的磁盘文件，例如删除 uploads/12/报告.pdf。
                # 它不会删除数据库记录；若文件不存在，直接调用通常会报 FileNotFoundError。
                path.unlink()
            elif path.exists():
                raise OSError(f"目标不是普通文件：{path}")

            # 最后删数据库记录。若这一步失败，数据库事务会回滚；下次运行仍能找到
            # 这条软删除记录，并在“磁盘文件已缺失”的情况下继续完成清理。
            cursor = connection.execute(
                "DELETE FROM upload_file WHERE fid = ? AND is_deleted = 1 "
                "AND deleted_time IS NOT NULL AND deleted_time <= ?",
                (fid, cutoff_text),
            )
            # rowcount 是本次 DELETE 实际影响的行数，正常情况应恰好删除一条。
            if cursor.rowcount != 1:
                raise sqlite3.DatabaseError(f"记录 #{fid} 未被删除")
            # commit() 提交本条记录的数据库修改，使删除真正生效。
            connection.commit()
            cleaned += 1
            print(f"  #{fid} 已清理。")
        except (OSError, sqlite3.Error, ValueError) as exc:
            # 单条记录失败只回滚这条数据库操作，继续检查后面的记录。
            # 注意：数据库回滚不能恢复已经 unlink 的磁盘文件，上面的重跑逻辑用于收尾。
            connection.rollback()
            failed += 1
            print(f"  #{fid} 清理失败：{exc}")

    print(f"完成：{cleaned} 条；失败：{failed} 条。")
    # 退出码 0 表示全部成功；1 表示至少有一条失败，便于命令行或定时任务发现问题。
    return 1 if failed else 0


def main() -> int:
    # argparse 负责读取命令行参数：不加参数是预览，加 --apply 才真正清理。
    parser = argparse.ArgumentParser(description="清理软删除超过 30 天的文件")
    parser.add_argument("--apply", action="store_true", help="执行永久清理；默认仅预览")
    # parse_args() 读取启动脚本时输入的参数，并得到 args.apply 这个布尔值。
    args = parser.parse_args()

    # 从脚本自身的位置推算项目根目录，避免从不同目录启动时找错数据库或上传目录。
    # __file__ 是脚本路径；resolve() 得到绝对路径；两个 parent 回到项目根目录。
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "instance" / "site.db"
    upload_root = project_root / "uploads"
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    # sqlite3.connect() 遇到不存在的数据库会新建空文件，故连接前先确认路径。
    # is_file() 确认数据库文件存在；is_dir() 确认上传目录存在。
    if not db_path.is_file():
        raise FileNotFoundError(db_path)
    if not upload_root.is_dir() or upload_root.is_symlink():
        raise ValueError(f"上传目录不存在或是符号链接：{upload_root}")

    connection = sqlite3.connect(db_path, timeout=30)
    try:
        # 启用外键约束，让 SQLite 在删记录时遵守数据库中的关联规则。
        connection.execute("PRAGMA foreign_keys = ON")
        return clean(connection, db_path, upload_root.resolve(), cutoff, args.apply)
    finally:
        # close() 释放数据库连接；即使清理过程中报错也会执行。
        connection.close()


if __name__ == "__main__":
    # 直接运行脚本才执行 main()；被其他 Python 文件导入时不会自动清理。
    raise SystemExit(main())
