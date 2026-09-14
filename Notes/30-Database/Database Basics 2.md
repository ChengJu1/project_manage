# 数据库基础-2

## 一、Python 操作 SQLite

通过 Python 实现数据库连接，可以让程序自动、动态、安全地管理数据，而不是手动写 SQL、手动存文件、手动改数据。

---

### 1.1 核心模块与连接
- `sqlite3`：Python 内置的轻量级关系型数据库操作模块，无需额外安装。
- `sqlite3.Error`：模块定义的标准异常类，用于捕获数据库操作中所有可预见的错误。

```python
# python内置sqlite3的库
import sqlite3
from sqlite3 import Error
```
---
### 1.2 数据库连接与创建

若数据库不存在则创建，存在则跳过。

SQLite 是文件型数据库，通过 sqlite3.connect() 建立连接时：

- 若指定的数据库文件不存在 → 自动创建该文件
- 若文件已存在 → 直接建立连接，操作已有数据

```python
def create_connection(db_name="test.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        print(f"成功连接数据库：{db_name}")
        return conn
    except Error as e:
        print(f"连接错误：{e}")
        return conn
    # 注意：连接需手动关闭，或用with上下文
```
> 注意：conn 是数据库连接对象，代表应用程序与数据库之间的通信通道，后续所有操作都依赖它。
---
### 1.3 游标
游标（Cursor） 是数据库系统中建立在数据库连接（Connection）之上的临时工作对象，是应用程序与数据库之间进行数据交互的核心操作载体。

- 数据库连接（conn） 比作 你和数据库之间打通的一条管道
- 游标（cursor） 就是 通过这条管道发送 SQL 命令、并带回数据结果的工具
- 所有 SQL 语句必须通过游标才能执行。

游标是数据库操作的核心接口，类比为 “数据操作手柄”，它的作用包括：
- 调用 execute() / executemany() 执行增删改查SQL操作。
- 通过 fetchone() / fetchall() / fetchmany() 获取查询结果。
- 写操作（INSERT/UPDATE/DELETE）通过游标执行后，由连接提交 / 回滚事务。
- 所有数据库交互行为必须依赖游标完成，不能直接使用连接执行SQL语句。
> 对比：conn 是管道，cursor 是操作手柄
---
### 1.4 事务机制
SQLite 默认开启事务机制（Transaction），所有写操作（INSERT/UPDATE/DELETE）都在事务中执行，必须手动提交才能持久化到数据库。
conn.commit()：提交事务，将所有修改写入数据库文件
conn.rollback()：回滚事务，撤销当前事务中所有未提交的修改
事务的核心作用：保证数据的一致性与完整性，避免部分操作失败导致的数据混乱。

---
### 1.5 资源管理与连接关闭
数据库连接是有限资源，操作完成后必须通过 conn.close() 关闭连接，否则可能导致：
- 数据库文件被锁定，其他进程无法访问
- 数据修改无法正常写入（未提交事务丢失）
- 系统资源泄漏
---
### 1.6 Python 插入数据
向数据库表中添加新记录，支持单条和批量插入。
1. 参数化查询（防 SQL 注入核心规范）
采用 ? 占位符 实现参数化 SQL 语句（SQLite 标准参数标记），禁止手动字符串拼接 SQL。
从根源防御 SQL 注入攻击，保障数据库安全；
自动处理数据类型转换、特殊字符转义，提升代码健壮性；
分离 SQL 语句结构与动态参数，符合数据库开发最佳实践。

2. 批量插入（executemany() 高性能方案）
使用游标对象的 executemany() 方法实现批量数据插入：
一次性提交多条数据，显著减少数据库 IO 交互次数，性能远优于循环执行execute()；
统一事务管理，保证批量数据插入的原子性（要么全部成功，要么全部失败）；
适配大批量测试数据、业务数据导入场景，提升程序执行效率。

3. 执行结果反馈（游标状态属性）
通过 cursor.rowcount 获取数据库受影响的记录行数：
单条插入：返回值固定为 1，代表成功插入 1 条记录；
批量插入：返回实际插入的总记录数，可用于数据校验与日志输出；
是程序与数据库交互结果的权威反馈依据，用于业务逻辑判断、操作提示。

```python
import sqlite3
from sqlite3 import Error

# 1. 单条插入（参数化，防注入）
def insert_user(conn, name, age, email):
    sql = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, age, email))
        conn.commit()
        print(f"插入成功，ID：{cursor.lastrowid}")
    except Error as e:
        print(f"插入错误：{e}")
        conn.rollback()

# 2. 批量插入
def batch_insert_users(conn, user_list):
    sql = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, user_list)
        conn.commit()
        print(f"批量插入成功，共{cursor.rowcount}条")
    except Error as e:
        print(f"批量插入错误：{e}")
        conn.rollback()

# 调用示例
if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    # 单条数据
    insert_user(conn, "张三", 30, "zhangsan@example.com")
    # 批量数据
    users = [("李四", 25, "lisi@example.com"),("王五", 35, "wangwu@example.com")]
    batch_insert_users(conn, users)
    conn.close()
```

---

### 1.7 SQL 注入示例
```python
if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    # ❌ 危险：直接拼接SQL语句，存在注入风险
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()

    # ✅ 安全写法：使用 ? 占位符（参数化查询）
    # query = "SELECT * FROM users WHERE name = ? AND password = ?"
    # user = conn.execute(query, (username, password)).fetchone()

    conn.close()

    if user:
        print(f"✅ 登录成功！欢迎 {user['name']}，邮箱：{user['email']}")
    else:
        print("❌ 用户名或密码错误")
```

最简通用绕过用户登录：

- 用户名输入：`' OR 1=1 --`
- 密码随便填，比如 `123`

```
SELECT * FROM users 
WHERE name = '' OR 1=1 --' AND password = '123'
```

`--` 是 SQL 注释符，会把后面的 `' AND password = '123` 全部注释掉。

实际执行SQL：`SELECT * FROM users WHERE name = '' OR 1=1`，永远为真，直接登录成功。

---

### 1.8 Python 查询数据
从数据库中检索数据，支持查询全部记录或指定条件的记录。
1. fetchall()：获取查询结果集中的所有记录，以元组列表形式返回。
适用场景：数据量较小的查询，如列表展示、统计分析。
注意：数据量过大时会占用大量内存，需谨慎使用。
fetchone()：获取查询结果集中的第一条记录（元组形式），常用于按主键查询或判断记录是否存在。
fetchmany(size)：获取结果集中指定数量的记录，适用于分页查询场景。

2. 通过 WHERE 子句实现精准筛选，配合参数化查询（? 占位符）：
- 避免直接拼接 SQL 字符串，从根源防止 SQL 注入攻击；
- 支持多条件组合（AND/OR）、模糊匹配（LIKE）、范围查询（>, <, BETWEEN）；

3. 查询结果以元组列表形式返回，需通过索引或字段顺序解析数据：
- 元组按字段顺序存储，例如 row[0] 对应 id，row[1] 对应 name；
- 可通过设置 conn.row_factory = sqlite3.Row 将结果转为Row对象，可通过字典形式按字段名访问（如 row['name']），提升代码可读性与可维护性。

4. 空结果与异常处理
- 空结果判断：通过 if not rows 或 if user is None 判断查询是否返回数据，避免后续处理因空值报错；
- 异常捕获：使用 try-except 捕获 sqlite3.Error，处理查询过程中的连接失败、SQL 语法错误、约束冲突等问题；
- 资源释放：无论查询成功或失败，都需在 finally 中关闭数据库连接，避免资源泄漏与文件锁定。
```python
import sqlite3
from sqlite3 import Error

# 1. 查询所有用户
def get_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if not rows:
            print("无用户数据")
            return []
        print("所有用户：")
        for row in rows:
            print(f"ID:{row[0]},姓名:{row[1]},年龄:{row[2]},邮箱:{row[3]}")
        return rows
    except Error as e:
        print(f"查询错误：{e}")
        return []

# 2. 按ID查询单个用户
def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            print(f"查询结果：{user}")
        else:
            print("用户不存在")
        return user
    except Error as e:
        print(f"查询错误：{e}")
        return None


# 调用示例
if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    # 全量数据
    get_all_users(conn)
    # 指定数据
    get_user_by_id(conn, 2)
    conn.close()
```
---
### 1.9 Python 更新数据
更新表中已存在的记录，支持修改部分字段。
1. UPDATE 语句的标准结构为：UPDATE 表名 SET 字段1=?, 字段2=? WHERE 条件
2. 通过 cursor.rowcount 获取本次更新操作的受影响行数，用于结果判断：
rowcount > 0：表示成功更新了对应数量的记录；
rowcount == 0：表示未找到符合 WHERE 条件的记录，更新未生效；
常用于业务逻辑判断与用户提示，例如 “未找到目标用户，更新失败”。
```python
import sqlite3
from sqlite3 import Error

def update_user_age(conn, user_id, new_age):
    sql = "UPDATE users SET age = ? WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (new_age, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"成功更新ID:{user_id}的年龄为{new_age}")
        else:
            print("未找到用户，更新失败")
    except Error as e:
        print(f"更新错误：{e}")
        conn.rollback()


# 调用示例
if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    update_user_age(conn, 1, "18")
    conn.close()
```
---
### 1.10 Python 删除数据
从表中移除记录，支持单条删除和批量删除。
1. DELETE 语句的标准结构为：DELETE FROM 表名 WHERE 条件

2. 通过 cursor.rowcount 获取本次删除操作的受影响行数，用于结果判断：
rowcount > 0：表示成功删除了对应数量的记录；
rowcount == 0：表示未找到符合 WHERE 条件的记录，删除未生效；
常用于业务逻辑判断与用户提示，例如 “已成功删除 3 条记录” 或 “未找到目标数据，删除失败”。

3. 物理删除与逻辑删除的取舍
- 物理删除：直接使用 DELETE 语句从数据库中移除记录，数据不可恢复，适用于低风险、无回溯需求的场景；
- 逻辑删除：不真正删除数据，而是通过添加 is_deleted 字段（0 = 未删除，1 = 已删除）标记记录状态，查询时过滤该字段，数据可回溯，是生产环境的主流做法；
- 两种方式可结合使用：先逻辑删除，再定期通过任务清理物理数据，兼顾业务需求与数据安全。
```python
import sqlite3
from sqlite3 import Error


def delete_user(conn, user_id):
    sql = "DELETE FROM users WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"成功删除ID:{user_id}的用户")
        else:
            print("用户不存在")
    except Error as e:
        print(f"删除错误：{e}")
        conn.rollback()

# 2. 删除所有用户（谨慎，加确认）
def delete_all_users(conn):
    confirm = input("确定删除所有用户？不可恢复！(y/n)：")
    if confirm.lower() != "y":
        print("取消删除")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        print(f"已删除所有用户，共{cursor.rowcount}条")
    except Error as e:
        print(f"删除错误：{e}")
        conn.rollback()


# 调用示例
if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    delete_user(conn, 1)
    delete_all_users(conn)
    conn.close()
```

### 1.11 关键知识点总结
|知识点|说明|
|---|---|
|sqlite3.connect()	|建立 / 创建数据库连接，自动创建不存在的文件
|conn.cursor()	|获取游标对象，用于执行 SQL 和获取结果
|PRIMARY KEY AUTOINCREMENT	|主键自增，实现记录唯一标识
|NOT NULL	|非空约束，确保字段必须填写
|UNIQUE	|唯一约束，避免字段值重复
|conn.commit()	|提交事务，将修改写入数据库
|conn.rollback()	|回滚事务，撤销错误操作
|conn.close()	|关闭数据库连接，释放资源
|try-except	|捕获 sqlite3.Error 异常，处理数据库操作错误

### 1.12 使用`with`连接数据库资源
Python插入数据示例中涉及数据库资源连接关闭，类似于Python在进行文件I/O时需要进行file.close()行为，同样可以使用`with`关键字：
```python
def create_table_with_context(db_name="users.db"):
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    );
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            print("表创建成功（自动提交事务）")
    except Error as e:
        print(f"操作失败：{e}")
```
---

## 二、假数据生成
在开发、测试、演示等场景中，我们常需要大量 “看起来真实但无隐私风险” 的数据（如模拟用户信息、订单记录、地址等），这类数据被称为 “假数据”。
Python 的Faker库是生成假数据的主流工具，它支持多语言、多类型数据生成，且用法简洁灵活，能高效满足各类假数据需求。

---
### 2.1 Faker库的核心优势
- 多类型覆盖：支持生成姓名、手机号、地址、邮箱、日期、公司、文本、数字等几十种常见数据类型；
- 多语言支持：可生成中文（大陆 / 台湾 / 香港）、英文、日文等多语言假数据，适配不同地区场景；
- 高真实性：生成的数据格式符合现实规则（如手机号为 11 位、邮箱含@和域名、身份证号符合校验规则）；
- 可扩展性：支持自定义数据类型（如生成符合业务规则的订单号、会员等级）；
- 轻量易用：API 设计简洁，一行代码即可生成一条假数据，学习成本低。
---
### 2.2 Faker安装
```
pip install faker
```
---
### 2.3 Faker基础方法
```python
from faker import Faker

# 初始化中文生成器
from faker import Faker

# 初始化中文生成器
fake = Faker("zh_CN")

# 1. 个人信息
print("姓名：", fake.name())                # 张三
print("手机号：", fake.phone_number())      # 13812345678
print("邮箱：", fake.email())               # zhangsan@example.com
print("信用卡号：", fake.credit_card_number())   # 110101199003071234

# 2. 地址信息
print("省份：", fake.province())             # 广东省
print("城市：", fake.city())                # 上海市
print("街道地址：", fake.street_address())             # 科技园路 55 号
print("完整地址：", fake.address())             # 北京市朝阳区建国路88号

# 3. 时间信息
print("日期：", fake.date())                # 2000-01-01
print("时间：", fake.time())                # 14:20:59
print("日期时间：", fake.date_time())        # 2024-05-20 14:30:00

# 4. 业务信息
print("公司：", fake.company())             # 北京科技有限公司
print("职业：", fake.job())                 # 软件工程师

# 5.其他
print("随机整数：", fake.random_int(100,10000)) # 5000
print("随机文本：", fake.text(max_nb_chars=200)) # 这是一段用于测试的随机描述文本
print("单句文本：", fake.sentence()) # 今天的天气非常适合户外活动
```
---
### 2.4 批量生成100条用户数据
```python
from faker import Faker
import pandas as pd

fake = Faker("zh_CN")
Faker.seed(42)  # 固定随机种子（保证每次运行生成相同数据，便于复现）

# 生成100条用户数据，存储为列表字典格式
user_data = []
for _ in range(100):  # 循环100次，生成100条数据
    user = {
        "用户ID": fake.uuid4(),      # 生成唯一UUID（模拟用户唯一标识）
        "姓名": fake.name(),
        "手机号": fake.phone_number(),
        "邮箱": fake.email(),
        "注册日期": fake.date_between(start_date="-2y", end_date="today"),  # 近2年的注册日期
        "所在城市": fake.city(),
        "职业": fake.job()
    }
    user_data.append(user)

# 转换为DataFrame，保存为Excel文件
df = pd.DataFrame(user_data)
df.to_excel("批量用户假数据.xlsx", index=False)  # index=False: 不保存行号
print("100条用户假数据已保存到Excel！")
```
---
### 2.5 自定义假数据
例如生成 “固定前缀 + 随机数字” 的订单号、“特定格式” 的会员卡号等，可通过自定义实现数据扩展、拼接字符串实现
```python
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_order_id():
    # 1. 固定前缀：ORD-
    prefix = "ORD-"
    # 2. 日期部分：当前年月（如202405）
    date_part = datetime.now().strftime("%Y%m")
    # 3. 随机6位数：补0至6位（如001234）
    random_part = fake.random_int(min=1, max=999999)
    random_part_str = f"{random_part:06d}"  # 格式化为6位字符串，不足补0
    # 4. 拼接成订单号
    return f"{prefix}{date_part}-{random_part_str}"

# 生成5条自定义订单号
for _ in range(5):
    print(generate_order_id())

# 输出示例：
# ORD-202405-045678
# ORD-202405-012345
# ORD-202405-098765
```
---

## 中间表
可以表示多对多的关系，比如一个学生可以选多门课，一门课也能有很多学生，通过中间表来构建一个多对多关系

``` python
project_members = db.Table(
    "project_members",
    db.Column("user_id",
              db.Integer,
              db.ForeignKey("user.id")),
    db.Column("project_id",
              db.Integer,
              db.ForeignKey("project.id")),
)
```

```text
学生表       选课表             课程表
1 小明       学生1 → 课程10      10 数学
2 小红       学生1 → 课程20      20 英语
	         学生2 → 课程10
```


## `db.relationship`
语句基本格式如下：
```python
属性名 = db.relationship(
	"关联的模型名", # 其实就是想连接的对象是谁
	secondary=中间表变量
)
```
## 相关知识

- [[Database Knowledge Map]]
- [[Database Basics 1#二、SQL 基础语句|SQL 基础]]
- [[Python Basics 4#4. 文件 I/O|Python 文件操作]]
- [[Backend Basics 2]]：Flask-SQLAlchemy 与 CRUD。
- [[Test Development Notes#1.4 自动化测试|自动化测试数据准备]]
- [[Project Issues]]
