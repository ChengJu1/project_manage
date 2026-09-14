# 数据库基础-1

## 一、数据库基础概念

### 1.1 数据库定义
数据库（Database, DB）：长期存储在计算机中、有组织、结构化、可共享、统一管理的数据集合。

---
### 1.2 数据库管理系统（DBMS）
DBMS（Database Management System）：管理数据库的软件系统，负责创建、维护、查询、安全控制、并发控制、数据备份恢复。
常见 DBMS：
- 关系型：SQLite、MySQL、PostgreSQL、Oracle、SQL Server
- 非关系型：MongoDB、Redis
- 总结：数据库是数据容器，DBMS 是管理容器的工具。
---
### 1.3 关系数据库（Relational Database）
关系数据库：数据以二维表（行 + 列）形式组织，表与表之间可以建立关系（外键），符合关系模型。
特点：
- 数据存在多张表里
- 表之间可以关联、查询、联合
- 结构清晰、易维护、支持复杂查询
- 主流：SQLite、MySQL、Oracle
- 总结：关系数据库 = 多张 Excel 表 + 表之间可以互相关联。
---
### 1.4 数据库核心作用
- 数据集中存储：把大量数据统一存放，避免零散文件、重复、混乱。
- 高效数据管理：支持增删改查（CRUD），快速定位、筛选、统计数据。
- 数据安全可靠：支持权限控制、事务、备份、恢复，防止数据丢失、篡改、泄露。
- 数据共享并发：允许多用户、多程序同时安全访问，互不干扰。
- 数据结构化、规范化：统一格式、统一约束，减少冗余、保证一致性。
---
### 1.5 核心术语
- DB（Database）：数据库，存放数据的容器文件
- DBMS：数据库管理系统，管理数据库的软件
- Table（表）：关系数据库的基本单位，类似 Excel 表格
- Column/Field（字段 / 列）：表的列，含名称 + 类型 + 约束
- Row/Record（记录 / 行）：表的一行，代表一条完整数据
- Primary Key（主键）：唯一标识一行，非空、不重复
- Foreign Key（外键）：建立表与表之间的关系
---
### 1.6 CRUD 基本操作
```
C（Create）：创建 / 插入
R（Read）：查询
U（Update）：更新
D（Delete）：删除
```
---
### 1.7 SQLite vs MySQL/PostgreSQL 对比

| 特性 | MySQL/PostgreSQL/SQLServer  | SQLite
| --- | --- | --- |
| 类型     | 企业级关系数据库 | 轻量级嵌入式关系数据库
|架构	|C/S（客户端 / 服务器）	|无服务器、文件型数据库
|存储	|多文件、目录结构	|单个 .db 文件
|连接	|网络、IP + 端口 + 账号密码	|直接读写本地文件
|并发	|高并发、多用户、行级锁	|轻量并发、单写多读
|适用场景	|网站、后端系统、高并发服务	|桌面软件、移动端、小型项目

相关术语：
- C/S（Client/Server，客户端 / 服务器架构）程序分成两部分：客户端（用户操作界面）、服务器（数据库服务进程）。客户端通过网络访问服务器，服务器统一管理数据，支持多用户同时连接。
- 嵌入式数据库没有独立服务器进程，直接嵌入到应用程序内部，和程序一起运行。不需要单独安装、配置，直接读写本地文件即可。
- 行级锁（Row-level Lock）并发控制机制：修改数据时只锁住当前要改的那一行，不影响其他行读写。支持高并发，适合多人同时操作同一张表。
- 单写多读SQLite 的并发特点：同一时间只能有一个写操作，但可以有多个读操作同时进行。适合读多写少、并发量不大的场景。
---

### 1.8 熟悉DB Browser for SQLite软件
- 新建数据库
- 打开数据库
- 浏览数据库结构
- 浏览数据
- 插入数据
- 修改数据
- 删除数据
- 查询数据
- 数据库临时文件.db-journal

## 二、SQL 基础语句
### 2.1 SQL注释
```sql
-- 单行注释（两个减号 + 空格）

/*
多行注释
可以写多行内容
*/
```
---
### 2.2 SQL语句核心关键字
|关键字	|作用|
|---|---|
|SELECT	|查询数据（最常用，查表格内容）|
|FROM	|指定从哪张表查数据|
|WHERE	|条件过滤（只查符合条件的数据）|
|INSERT	|插入 / 新增数据|
|UPDATE	|修改 / 更新数据|
|DELETE	|删除数据|
---
### 2.3 创建数据库
手动在DB Browser for SQLite创建数据库
---
### 2.4 创建表（CREATE TABLE）
```sql
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增主键
    name TEXT NOT NULL,                    -- 姓名（非空）
    age INTEGER,                            -- 年龄
    major TEXT,                             -- 专业
    score REAL CHECK (score >= 0)         -- 成绩（非负）
);
```
相关知识点：
- `CREATE TABLE`：创建表
- `IF NOT EXISTS`：如果表不存在才创建，避免重复建表报
- `PRIMARY KEY`：主键，唯一标识一行数据的 “身份证号”，特点：不允许重复、不能为NULL，一张表仅允许有一个主键
- `AUTOINCREMENT`：自增，插入数据时不用手动写 id，数据库会自动从 1、2、3… 往上加，仅适用于整数类型主键
- `NOT NULL`：非空约束，表示该列必须填值，不允许为空
- `INTEGER`：整数（年龄、序号、ID 都用它）
- `TEXT`：文本 / 字符串（姓名、专业、描述）
- `REAL`：浮点数 / 小数，用来存：成绩、身高、体重、价格、经纬度等带小数点的数字，等价于FLOAT / DOUBLE
- `CHECK`：检查约束，强制这一列必须满足你设定的条件，例如CHECK (score >= 0) 表示成绩不能是负数，否则插入会报错，其他条件：`score BETWEEN 0 AND 100`、`gender IN ('男', '女')`
---
### 2.5 插入数据（INSERT）
```sql
-- 1. 单条插入（指定字段）
INSERT INTO students (name, age, major, score)
VALUES ('张三', 20, '计算机科学', 92.5);

-- 2. 单条插入（部分字段）
INSERT INTO students (name, major)
VALUES ('李四', '电子工程');

-- 3. 批量插入（高效）
INSERT INTO students (name, age, major, score)
VALUES
    ('王五', 19, '机械工程', 79.5),
    ('赵六', 22, '计算机科学', 94.0),
    ('钱七', 20, '数学', 85.5);
```
相关知识点：
- SQL文本值推荐使用单引号包裹（几乎所有数据库通用）
- 部分数据库也支持双引号，例如SQLite支持，MySQL不支持
---
### 2.6 查询数据（SELECT）
```sql
-- 1. 查询所有字段+所有记录
SELECT * FROM students;

-- 2. 查询指定字段
SELECT name, age, major FROM students;

-- 3. 条件查询（WHERE）
SELECT name, score FROM students WHERE major = '计算机科学';

-- 4. 多条件查询（AND/OR）
SELECT * FROM students WHERE age > 19 AND score >= 80;

-- 5. 排序（ORDER BY：DESC降序，ASC升序）
SELECT name, score FROM students ORDER BY score DESC;

-- 6. 限制条数（LIMIT）
SELECT * FROM students ORDER BY score DESC LIMIT 3;

-- 7. 模糊查询（LIKE：%任意字符（0-N个字符），_单个字符）
SELECT * FROM students WHERE name LIKE '张%'; -- 姓张
SELECT * FROM students WHERE name LIKE '_三%'; -- 第二个字是三

-- 8. 聚合查询（COUNT/AVG/MAX/MIN）
SELECT COUNT(*) AS total FROM students;       -- 总人数
SELECT AVG(score) AS avg_score FROM students;-- 平均分
SELECT MAX(score) AS max_score FROM students;-- 最高分
```
模糊匹配`LIKE`相关知识点：
- `%`：匹配任意长度任意字符（包括 0 个字符）
- `_`：只匹配单个任意字符
- `NOT LIKE`：反向模糊查询
- SQLite 默认 LIKE 对英文字母不区分大小写（不同数据库需确认模糊匹配规则）

常用条件符号：
- `=` 等于
- `>` 大于
- `<` 小于
- `>=` 大于等于
- `<=` 小于等于
- `!=` 或 <> 不等于
- `AND` 且（多个条件同时满足）
- `OR` 或（满足一个即可）
- `LIKE` 模糊查询

---
### 2.7 更新数据（UPDATE）
```sql
-- 1. 更新单个字段
UPDATE students SET age = 21 WHERE name = '张三';

-- 2. 更新多个字段
UPDATE students SET age = 22, score = 89.5 WHERE name = '李四';

-- 3. 批量条件更新
UPDATE students SET score = score + 1 WHERE major = '计算机科学';

-- 4. 计算更新
UPDATE students SET score = score * 1.05 WHERE age < 20;
```
---
### 2.8 删除数据（DELETE）
```sql
-- 1. 条件删除
DELETE FROM students WHERE age > 22;

-- 2. 精准删除（按主键，推荐）
DELETE FROM students WHERE id = 3;

-- 3. 多条件删除
DELETE FROM students WHERE major = '数学' AND score < 80;

-- 危险！删除所有记录（保留表结构）
DELETE FROM students;

-- 极度危险！删除表及所有数据（慎用）
DROP TABLE IF EXISTS students;
```

### 2.9日期降序就代表从新到旧

```Mysql
ORDER BY create_at DESC
```
### 3 实践题
```
任务 1：设计并创建 “员工信息表”
需求：先创建名为 cmp 的数据库，创建名为 employees 的表，
用于存储公司员工的关键信息，需包含数据约束（确保数据有效性）。

表结构设计（共 5 个核心字段）：
操作要求：写出创建表的 SQL 语句，确保约束生效。
约束：
- emp_id 为主键
- emp_name 不能为空
- department 不能为空
- position 不能为空
- salary 不能为负数
```

|字段名（Field Name）|数据类型（Data Type）	|约束（Constraint）	|说明（Description）
|---|---|---|---|
|emp_id	|INTEGER|PRIMARY KEY|员工唯一编号（如 1001、1002，手动输入或自增均可）
|emp_name	|TEXT|NOT NULL|员工姓名（必填，不可为空）
|department	|TEXT|NOT NULL|所属部门（如 “技术部”“行政部”“销售部”）
|position	|TEXT|NOT NULL|职位（如 “程序员”“行政专员”“销售经理”）
|salary	|INTEGER	|CHECK (salary > 0)	|月薪（正数，单位：元，如 5000、8000）

```
任务 2：插入员工示例数据
需求：向 employees 表插入 5 条员工数据，使用批量插入。
```
|emp_id（员工编号）	|emp_name（员工姓名）	|department（所属部门）	|position（职位）	|salary（月薪 / 元）
|---|---|---|---|---|
|1001	|张三	|技术部	|后端程序员	|12000
|1002	|李四	|销售部	|销售专员	|8000
|1003	|王五	|行政部	|行政专员	|6000
|1004	|赵六	|技术部	|前端程序员	|11000
|1002	|钱七	|销售部	|销售经理	|15000
```
任务 3：员工数据查询操作
需求：针对 employees 表，完成 以下查询：
查询 “销售部” 且 “月薪 ≥ 10000” 的员工姓名、职位与薪资；
查询 “姓名以‘李’开头” 或 “职位包含‘程序员’” 的员工信息；
计算所有员工的平均月薪（四舍五入保留1位小数，参考方法：ROUND）
```

```
任务 4：员工数据更新操作
单条更新：因张三（emp_id=1001）职级晋升
将其职位改为 “后端技术主管”，薪资调为 18000；
```

```
任务 5：员工数据删除操作
精准删除：因李四（emp_id=1002）离职，删除其员工记录

```

## 相关知识

- [[Database Knowledge Map]]
- [[Database Basics 2]]：使用 Python 操作 SQLite。
- [[Backend Basics 2]]：在 Flask 中使用 SQLAlchemy。
- [[Test Development Notes]]：测试数据与数据库校验。
