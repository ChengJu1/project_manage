# 网页后端基础-1
## 一、Flask

### 1.1 Flask介绍

基于 Python 的**轻量级 Web 框架**，也叫**微框架**，核心只包含路由和模板引擎，其他功能通过扩展实现。

---

### 1.2 Flask 特点

代码简洁、开发灵活、学习成本低、第三方扩展库丰富。

- 代码简洁：只需要几行代码即可启动 Web 服务

- 适用场景：小型网站、后端 API 接口、快速原型开发、个人项目。

---

### 1.3  Flask 安装与启动

终端界面安装命令：`pip install flask`

---

### 1.4 Hello Flask

新建一个项目（文件夹），项目内新建一个python文件：

```python
# 导入Flask核心类
from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# 定义路由和视图函数
@app.route('/')
def index():
    # 返回给浏览器的内容
    return "Hello Flask！这是我的第一个Flask项目"

# 程序入口
if __name__ == '__main__':
    # 启动Flask服务，debug=True开启调试模式
    app.run(debug=True)
```

运行方式：

1. 保存为 `app.py`
2. 终端执行：`python app.py`
3. 浏览器打开：`http://127.0.0.1:5000/`

------
### 1.5 Flask标准项目结构

- `app.py`：项目主入口文件
- `templates/`：存放 HTML 模板文件
- `static/`：存放静态资源（CSS/JS/ 图片）

---

## 二、Flask路由

### 2.1 知识点

1. 路由装饰器：`@app.route('/路径')`，绑定 URL 与函数
2. 视图函数：处理请求并返回响应（字符串 / HTML/JSON）
3. 动态路由：URL 中传递变量，支持类型限制
4. 反向路由：`url_for(函数名)` 根据函数名生成 URL
5. 多路由绑定：一个函数对应多个 URL 路径

### 2.2 示例代码

```python
from flask import Flask, url_for, jsonify
app = Flask(__name__)

# 1. 基础路由
@app.route('/')
def index():
    return "首页"

# 2. 动态路由：字符串变量
@app.route('/user/<name>')
def user_info(name):
    return f"欢迎用户：{name}"

# 3. 动态路由：指定整数类型
@app.route('/age/<int:age>')
def user_age(age):
    return f"年龄：{age}"

# 4. 多路由绑定同一个视图
@app.route('/path1')
@app.route('/path2')
def multi_path():
    return "这个页面对应两个URL"

# 5. 反向路由：url_for 根据函数名生成链接
@app.route('/test-url')
def for_test_url():
    # 生成 user_info 函数对应的路由
    url = url_for('user_info', name='张三')
    return f"生成的链接：{url}"

# 6. 返回JSON
@app.route("/zhangsan")
def user():
    data = {"name": "zhangsan", "age": 18}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```

------

## 三、HTTP 请求方法

### 3.1 GET&POST

1. GET：用于获取数据，参数在 URL 中，不安全、可缓存

2. POST：用于提交数据，参数在请求体中，安全、不可缓存（201）

3. PUT：修改数据、PATCH：修改部分数据、DELETE：删除数据（返回状态码：204）

4. 路由指定方法：`methods=['GET', 'POST']`

5. 后端获取前端表单数据：

   - `request.args`：获取 GET 请求参数
   - `request.form`：获取 POST 表单数据


### 3.2 示例代码

1. 项目结构

```
project/
├─ app.py
└─ templates/
   ├─ login.html     # 登录页
   └─ result.html     # 结果页
```

2.后端代码app.py

```python
from flask import Flask, request, render_template

app = Flask(__name__)

# 打开登录页
@app.route('/')
def index():
    return render_template('login.html')

# 接收表单，渲染结果页
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # 只传数据，页面全在 templates
    return render_template('result.html', username=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)
```

3. 前端 templates/login.html（登录表单页）

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
    <h2>用户登录</h2>
    <form action="/login" method="post">
        用户名：<input type="text" name="username"><br><br>
        密码：<input type="password" name="password"><br><br>
        <input type="submit" value="登录">
    </form>
</body>
</html>
```

4. 前端 templates/result.html（结果页）

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>结果</title>
</head>
<body>
    <h2>提交成功</h2>
    <p>用户名：{{ username }}</p>
    <p>密码：{{ password }}</p>
    <p><a href="/">返回登录</a></p>
</body>
</html>
```
5. 运行
- 运行 app.py
- 浏览器打开：http://127.0.0.1:5000

------

## 四、Jinja2 模板引擎

### 4.1 知识点

1. 模板渲染：`render_template('文件名')` 渲染 HTML 模板

2. 变量输出：`{{ 变量名 }}`

3. 控制结构：

   - `{% if %}` 判断
   - `{% for %}` 循环

4. 过滤器：`|safe`（解析 HTML）、`|upper`（大写）

5. 模板继承：父模板定义区块，子模板继承并覆盖

### 4.2 项目结构

```
项目文件夹
├─ app.py
└─ templates/
   ├─ base.html   （父模板）
   └─ index.html  （子模板）
```

1. 父模板 base.html

```html
<!-- 公共父模板 -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
</head>
<body>
    <div>公共头部导航</div>
    <!-- 定义可替换的内容区块 -->
    {% block content %}{% endblock %}
    <div>公共底部</div>
</body>
</html>
```

2. 子模板 index.html

```html
<!-- 继承父模板 -->
{% extends 'base.html' %}

<!-- 重写标题区块 -->
{% block title %}模板页面{% endblock %}

<!-- 重写内容区块 -->
{% block content %}
    <h2>变量展示：{{ name }}</h2>
    
    <!-- if 判断 -->
    {% if age >= 18 %}
        <p>已成年</p>
    {% else %}
        <p>未成年</p>
    {% endif %}

    <!-- for 循环 -->
    <h3>爱好列表：</h3>
    <ul>
        {% for h in hobby %}
            <li>{{ h }}</li>
        {% endfor %}
    </ul>

    <!-- 过滤器使用 -->
    <p>大写：{{ msg | upper }}</p>
    <p>解析HTML：{{ html_str | safe }}</p>
{% endblock %}
```

3. app.py 代码

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    # 给模板传递数据
    data = {
        "name": "张三",
        "age": 20,
        "hobby": ["读书", "编程", "运动"],
        "msg": "hello flask",
        "html_str": "<span style='color:red'>红色文字</span>"
    }
    # 渲染模板并传参
    return render_template('page.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
```

------

## 五、静态文件

### 5.1 知识点

1. `static/`：专门存放 CSS、JS、图片、字体等静态资源
2. 引入方式：`/static/文件路径`
3. 规范：所有静态资源必须放在 `static` 文件夹中
4. imgs、images

### 5.2 项目结构

```
项目文件夹
├─ app.py
├─ static/
│  ├─ css/
│  │  └─ style.css
│  └─ images/
│     └─ logo.png
└─ templates/
   └─ index.html
```

1. static/css/style.css

```css
.box{
    color: blue;
    font-size: 20px;
}
```

2. templates/index.html

```html
<!DOCTYPE html>
<html>
<head>
    <!-- 引入CSS静态文件 -->
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="box">使用了静态CSS样式</div>
    <!-- 引入图片 -->
    <img src="/static/images/logo.png" width="100">
    {{ name }}
</body>
</html>
```

3. app.py

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('page.html', name="来源于后端的用户名")

if __name__ == '__main__':
    app.run(debug=True)
```

## 相关知识

- [[Web Development Knowledge Map]]
- [[Python Basics 3#7. 装饰器|Python 装饰器]]
- [[Web Basics#3. HTTP/HTTPS 核心|HTTP 请求与响应]]
- [[Frontend Basics 1]]：HTML 与模板页面。
- [[Backend Basics 2]]：Flask-SQLAlchemy 与 CRUD。
- [[Test Development Notes#第三章 接口测试|接口测试]]
