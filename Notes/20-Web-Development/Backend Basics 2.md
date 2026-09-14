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

### 3.2 示例代码

项目结构

```
project/
├── app.py            # 主程序（路由）
├── models.py         # 数据库模型(单独剥离)
├── instance/users.db # 数据库
└── templates/        # 前端模板
```

1. models.py

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 用户模型（完全剥离）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
```

2. app.py

```python
from flask import Flask, render_template, request, redirect, url_for

# 从 models 导入 db 和 User
from models import db, User

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# 绑定 app 和 db
db.init_app(app)

# 自动建表
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('list_user'))


@app.route('/list')
def list_user():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        db.session.commit()
        return "修改成功！<a href='/list'>返回列表</a>"
    return render_template('update.html', user=user)

@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return "删除成功！<a href='/list'>返回列表</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "注册成功！<a href='/login'>去登录</a>"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == pwd:
            return "登录成功！<a href='/list'>进入用户列表</a>"
        return "用户名或密码错误"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
```

3. 前端模版templates/list.html（用户列表）

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>用户列表</title>
</head>
<body>
    <h2>用户列表</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>用户名</th>
          	<th>密码</th>
            <th>操作</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.password }}</td>
          
            <td>
                <a href="/update/{{ user.id }}">修改</a> &nbsp;
                <a href="/delete/{{ user.id }}" onclick="return confirm('确定删除？')">删除</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    <br>
    <a href="/register">注册</a> |
    <a href="/login">登录</a>
</body>
</html>
```

4. 前端模版templates/update.html（更新用户）

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>修改用户</title>
</head>
<body>
    <h2>修改用户</h2>
    <form method="post">
        用户名：<input type="text" name="username" value="{{ user.username }}" required><br><br>
        密码：<input type="password" name="password" required><br><br>
        <input type="submit" value="保存修改">
    </form>
    <br>
    <a href="/list">返回列表</a>
</body>
</html>
```
5. 前端模版templates/register.html（注册用户）
```python
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>注册</title>
</head>
<body>
    <h2>用户注册</h2>
    <form method="post">
        用户名：<input type="text" name="username" required><br><br>
        密码：<input type="password" name="password" required><br><br>
        <input type="submit" value="注册">
    </form>
    <br>
    <a href="/login">已有账号？去登录</a>
</body>
</html>
```
6. 前端模版templates/login.html（用户登录）

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
    <h2>用户登录</h2>
    <form method="post">
        用户名：<input type="text" name="username" required><br><br>
        密码：<input type="password" name="password" required><br><br>
        <input type="submit" value="登录">
    </form>
    <br>
    <a href="/register">没有账号？去注册</a>
</body>
</html>
```

## 相关知识

- [[Web Development Knowledge Map]]
- [[Backend Basics 1]]：Flask 基础、路由和模板。
- [[Backend Basics 3]]：蓝图与数据分页。
- [[Database Basics 1#二、SQL 基础语句|SQL 基础]]
- [[Database Basics 2#一、Python 操作 SQLite|Python 操作 SQLite]]
- [[Test Development Notes#第三章 接口测试|接口测试]]
