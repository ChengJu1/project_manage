# 网页后端基础-2

## 一、Flask-SQLAlchemy

### 1.1 知识点

- ORM（对象关系映射）：用 Python 类代替 SQL 语句操作数据库，不用写原生 SQL。
- Flask-SQLAlchemy：Flask 的数据库扩展，专门用来操作 SQLite、MySQL 等数据库。
- SQLite：轻量、文件型数据库，不用安装服务。

### 1.2 安装

```
pip install flask-sqlalchemy
```

### 1.3 数据库配置

```python
# 配置 SQLite 数据库文件
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
```

------

## 二、模型定义

### 2.1 知识点

- 继承 `db.Model` → 对应数据库一张表
- 常用字段：
  - `Integer()`：整数
  - `String(长度)`：字符串
  - `primary_key=True`：主键

### 2.2 示例代码

```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# 1. 创建 Flask 实例
app = Flask(__name__)

# 2. 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# 3. 创建 SQLAlchemy 实例
db = SQLAlchemy(app)

# 4. 定义模型（建表）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# 5. 第一次运行自动建表
with app.app_context():
    db.create_all()
```

### 2.3 URL和URI的区别？
一句话总结：URL 是 URI 的一个子集。

- **URI**：统一资源标识符，用来**唯一标识一个资源**（只负责“叫什么名字”）
- **URL**：统一资源定位符，用来**定位、找到这个资源**（不仅有名字，还告诉在哪、怎么访问）

1. 概念拆解

URI（Uniform Resource Identifier）统一资源标识符

作用：**唯一标识某一个资源**，不一定能访问。
格式：`[资源类型/方案:] [方案特定部分/标识名]`

示例：
```
urn:isbn:9787111532644
```
`urn:isbn:9787111532644` 这是一个URI，代表一本书，**但你不能用它去网络访问这本书**，它只是一个编号。

URN（统一资源名称）是URI的另一个子类，只做命名，不提供访问路径。
✅ URI = URL + URN

URL（Uniform Resource Locator）统一资源定位符

作用：**定位资源，包含访问协议、位置，可以直接拿来访问**。
必须包含：**协议 + 位置**。

示例：
```
https://www.baidu.com/index.html
```
它既是 **URL**，同时也是 **URI**。

所有URL都是URI，但**不是所有URI都是URL**。

2. 直观对比表
|项目|URI|URL|
|---|---|---|
|全称|统一资源标识符|统一资源定位符|
|核心|标识资源身份|定位资源位置|
|能否访问|不一定，只是ID|可以直接访问|
|包含协议|可选|必须要有(http/https/file等)|
|关系|父类，包含URL、URN|URI的子集|

3. 例子区分

1. `https://example.com/demo.html`
✅ URI ✅ URL（有协议，可以访问）

2. `urn:uuid:6e8bc430-9c3a-11d9-839a-08002be4f46c`
✅ URI ❌ URL（只是唯一编号，没有访问地址）

4.开发里常见误区

1. 很多人混用，写接口文档经常把接口地址叫URI，**技术上是没问题的**，因为接口地址本身也是URL，自然属于URI。
2. RESTful API中，常说的**URI**，指资源标识；完整带http的地址，也是URL。

极简记忆口诀

>**URL告诉你资源在哪里；URI告诉你它是谁。**
>URL一定是URI，URI不一定是URL。


------

## 三、数据库 CRUD 操作

### 3.1 知识点

- **增（Create）**：`db.session.add()` → `commit()`
- **查（Read）**：`all()`、`get()`、`filter_by()`
- **改（Update）**：查 → 改属性 → `commit()`
- **删（Delete）**：查 → `delete()` → `commit()`

```

## 相关知识

- [[Web Development Knowledge Map]]
- [[Backend Basics 1]]：Flask 基础、路由和模板。
- [[Backend Basics 3]]：蓝图与数据分页。
- [[Database Basics 1#二、SQL 基础语句|SQL 基础]]
- [[Database Basics 2#一、Python 操作 SQLite|Python 操作 SQLite]]
- [[Test Development Notes#第三章 接口测试|接口测试]]
