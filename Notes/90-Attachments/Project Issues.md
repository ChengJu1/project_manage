- `SELECT`与`INSERT`都不能加字段类型

## 数据库迁移

SQLite中:
```SQLite
PRAGMA table_info(tool_audit_logs);
```
可以通过这个查询表结构，返回内容类似于名字是什么，类型是什么，有无初始值等

而`ALTER TABLE`则是可以修改已存在表格的结构，下面是语法:
```SQLite
ALTER TABLE 表名
ADD COLUMN 新字段 字段类型 约束;
```

## `fetchall()`

把表格中的每一行提取出来作为一个元组，然后所有行再拼一个列表
```Python

[(1, '张三', 18), (2, '李四', 20), (3, '王五', 22)]
```


## `connection.row_factory = sqlite3.Row`

告诉sqlite, 查询结果不要只给我普通 tuple，而是给我一种知道“每个值对应哪个列名”的 Row 对象。
这时候`fetchall()`返回的值就可以通过`row["列名"]`来访问了

## `executescript()`与`execute()`

### `execute()`
- 一次执行一条SQL语句，并且支持用?传入参数
```Python
connection.execute(
    """
    SELECT id, name
    FROM users
    WHERE id = ?
    """,
    (user_id,),
)
```
### `executescript()`
- 一次执行一整段 SQL 脚本，脚本中可以包含多条 SQL，每条语句使用分号隔开。
- 不支持?传参
```python
connection.executescript(
    "SELECT * FROM conversations WHERE id = ?",
    (conversation_id,), #会报错
)
```
