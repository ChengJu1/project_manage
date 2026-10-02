"""Add UploadFile.uploaded_time and recover it from existing stored names.

Run once from the repository root with Python. The original database is backed
up before the table is changed. Re-running after success is harmless.
"""

from datetime import datetime
from pathlib import Path
import sqlite3


DATABASE = Path(__file__).resolve().parents[1] / "instance" / "site.db"


def time_from_standard_name(standard_name: str) -> datetime:
    try:
        timestamp = standard_name.rsplit("_", 2)[1]
        return datetime.strptime(timestamp, "%Y%m%d%H%M%S%f")
    except (IndexError, ValueError) as exc:
        raise ValueError(f"Cannot recover upload time from {standard_name!r}") from exc


def migrate() -> None:
    if not DATABASE.is_file():
        raise FileNotFoundError(DATABASE)

    with sqlite3.connect(DATABASE, timeout=10) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(upload_file)")}
        if "uploaded_time" in columns:
            print("upload_file.uploaded_time already exists; no changes made")
            return

        expected = {
            "fid", "file_name", "standard_name", "uploaded_by",
            "proj_id", "is_deleted",
        }
        if columns != expected:
            raise RuntimeError(f"Unexpected upload_file schema: {sorted(columns)}")

        old_rows = connection.execute(
            "SELECT fid, file_name, standard_name, uploaded_by, proj_id, is_deleted "
            "FROM upload_file ORDER BY fid"
        ).fetchall()
        migrated_rows = [
            (
                fid, file_name, standard_name, uploaded_by, proj_id,
                time_from_standard_name(standard_name).strftime("%Y-%m-%d %H:%M:%S.%f"),
                is_deleted,
            )
            for fid, file_name, standard_name, uploaded_by, proj_id, is_deleted in old_rows
        ]

        backup_path = DATABASE.with_name(
            f"site.before-upload-time-{datetime.now():%Y%m%d-%H%M%S}.db"
        )
        with sqlite3.connect(backup_path) as backup:
            connection.backup(backup)

        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "CREATE TABLE upload_file_new ("
                "fid INTEGER NOT NULL PRIMARY KEY, "
                "file_name VARCHAR(64) NOT NULL, "
                "standard_name VARCHAR(64) NOT NULL UNIQUE, "
                "uploaded_by VARCHAR(64) NOT NULL, "
                "proj_id INTEGER NOT NULL, "
                "uploaded_time DATETIME NOT NULL, "
                "is_deleted BOOLEAN NOT NULL, "
                "FOREIGN KEY(proj_id) REFERENCES project (id)"
                ")"
            )
            connection.executemany(
                "INSERT INTO upload_file_new "
                "(fid, file_name, standard_name, uploaded_by, proj_id, uploaded_time, is_deleted) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                migrated_rows,
            )
            connection.execute("DROP TABLE upload_file")
            connection.execute("ALTER TABLE upload_file_new RENAME TO upload_file")
            if connection.execute("PRAGMA foreign_key_check").fetchall():
                raise RuntimeError("Foreign key check failed")
            connection.commit()
        except Exception:
            connection.rollback()
            raise

    print(f"Migrated {len(migrated_rows)} file records; backup: {backup_path}")


if __name__ == "__main__":
    migrate()
