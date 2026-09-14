# 网页后端基础-3

## 一、蓝图（Blueprint）

### 1.1 知识点

- 为什么使用蓝图：项目变大后，路由、模型、视图混在一起很乱；蓝图用来模块化、分层、解耦。
- 核心三步：
  1. 创建蓝图：`Blueprint('名字', __name__)`
  2. 在蓝图上写路由：`@bp.route('/xxx')`
  3. 注册蓝图：`app.register_blueprint(bp)`
- 项目结构：

```
project/
├─ app.py          # 入口：创建app、注册蓝图、初始化db
├─ models.py       # 数据库模型
└─ routes.py       # 蓝图 + 路由
```

### 1.2 示例代码

1. models.py（模型）

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
```

2. routes.py（蓝图 + 路由）

```python
from flask import Blueprint, render_template
from models import User

# 1. 创建蓝图
bp = Blueprint('user', __name__)

# 2. 蓝图路由：首页
@bp.route('/')
def index():
    return render_template('page.html')

# 蓝图路由：用户列表
@bp.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)
```

3. app.py（入口）

```python
from flask import Flask
from models import db
from routes import bp

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# 初始化db
db.init_app(app)

# 3. 注册蓝图
app.register_blueprint(bp)

# 建表（首次运行）
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

4. 前端模板（templates/）

- index.html

```html
<h2>首页（蓝图版）</h2>
<p><a href="/users">查看用户列表</a></p>
```

- user_list.html

```html
<h2>用户列表</h2>
{% for u in users %}
<p>{{ u.id }} - {{ u.username }}</p>
{% endfor %}
```

------

## 二、数据分页

### 2.1 知识点

- 原理：`LIMIT`（每页条数）+ `OFFSET`（偏移量）
- 公式：`offset = (page - 1) * per_page`
- 参数：`page`（当前页）、`per_page`（每页条数）
- 流程：取参数 → 算偏移 → 查数据 → 算总页数

---

### 2.2 示例代码

1. 后端代码app.py

```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# 初始化100条测试数据（仅首次运行）
with app.app_context():
    db.create_all()
    if User.query.count() == 0:
        for i in range(1, 101):
            db.session.add(User(name=f"用户{i}"))
        db.session.commit()

# 分页路由
@app.route('/')
def page():
    # 获取参数，默认第1页、每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    # 查询数据
    users = User.query.limit(per_page).offset(offset).all()
    total = User.query.count()
    total_pages = math.ceil(total / per_page)

    return render_template('page.html', users=users, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
```

2. 前端模版 templates/page.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>分页列表</title>
</head>
<body>
    <h2>用户列表（分页）</h2>
    <ul>
        {% for user in users %}
        <li>{{ user.id }} - {{ user.name }}</li>
        {% endfor %}
    </ul>

    <!-- 分页导航 -->
    <p>
        {% if page > 1 %}
            <a href="/?page={{ page-1 }}">上一页</a>
        {% endif %}
        第 {{ page }} / {{ total_pages }} 页
        {% if page < total_pages %}
            <a href="/?page={{ page+1 }}">下一页</a>
        {% endif %}
    </p>
</body>
</html>
```

---

## 相关知识

- [[Web Development Knowledge Map]]
- [[Backend Basics 1]]：Flask 路由与模板。
- [[Backend Basics 2]]：Flask-SQLAlchemy 与 CRUD。
- [[Database Basics 2]]：数据库操作和测试数据生成。
- [[Test Development Notes#第三章 接口测试|接口测试]]
