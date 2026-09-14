# Python基础-4

## 1. 异常

### 1.1 异常处理

异常处理（try-except）是指程序在运行过程中遇到错误（如语法错误、逻辑错误、资源缺失等）时，通过特定机制捕获错误、处理错误，避免程序直接崩溃的技术。

Python通过 try-except 语句实现异常处理。

---
### 1.2 异常处理的核心逻辑

程序正常执行时，代码会按顺序运行；

若遇到异常，程序会暂停当前流程，跳转到对应的异常处理代码块（except）；

处理完成后，程序可继续执行后续代码（而非直接崩溃）。

---
### 1.3 语法结构

```
try:
    # 可能出错代码
except 异常类型:
    # 异常处理
else:
    # 无异常执行
finally:
    # 一定执行
```

---
### 1.4 常见异常

| 异常类型          | 异常名称    | **触发场景**                 | **示例**                           |
| ----------------- | ----------- | ---------------------------- | ---------------------------------- |
| ValueError        | 值错误      | 数据类型正确，但值不符合要求 | `int("abc")`（字符串无法转为整数） |
| TypeError         | 类型错误    | 数据类型错误                 | `1 + "2"`（整数与字符串无法相加）  |
| FileNotFoundError | 文件未找到  | 尝试读取不存在的文件         | open("nonexist.txt", "r")          |
| IndexError        | 索引错误    | 列表 / 元组索引超出范围      | `[1,2,3][10]`                      |
| KeyError          | 键错误      | 访问字典中不存在的键         | `{"a":1}["b"]`                     |
| ZeroDivisionError | 除数为0异常 | 除数为 0                     | 5 / 0                              |

---
### 1.5 异常处理

1. 捕获指定异常：针对可能出现的指定异常，单独捕获并处理

```python
try:
	num = int(input("请输入一个整数："))
	print(f"你输入的整数：{num}")
except ValueError as e:
	print(f"出现值错误，具体错误内容：{e}")
```

2. 捕获多个异常：通过except块捕获多种可能错误

```python
try:
	a = int(input("请输入一个被除数："))
	b = int(input("请输入一个除数："))
except TypeError:
	print(f"出现类型错误，具体错误内容:{e}")
except ZeroDivisionError:
	print(f"出现被除数错误，具体错误内容：{e}")
```

3. 捕获所有异常：通过Except捕获所有异常，通常用于兜底

```python
try:
	lst = [1,2,3]
	print(lst[10])  # 处罚IndexError
excepte Exception as e:
	print("出现错误，具体错误原因:{e}")
```

---
### 1.6 `else`和`finally`的使用

`else`：仅在 try 块无异常时执行；

`finally`：无论是否有异常，都会执行（常用于释放资源，如关闭文件）。

```python
try:
	a = int(input("请输入一个被除数："))
	b = int(input("请输入一个除数："))
except TypeError:
	print(f"出现类型错误，具体错误内容:{e}")
except ZeroDivisionError:
	print(f"出现被除数错误，具体错误内容：{e}")
else:
	print(f"{a}/{b}={a/b}")
finally:
	print("无论是否异常，该行一定执行！")
```

---
### 1.7 `raise`的使用

用于显式地引发异常，可以在代码中主动触发特定的异常类型，从而控制程序的流程，处理错误或不符合预期的情况。

```python
num = int(input("请输入一个正整数："))
if num < 0:
	raise ValueError("输入的整数不符合预期，你输入的数字为{num}")
else:
	print(f"你输入的正整数为{num}")
```

---
### 1.8 自定义异常
Python 所有异常都继承自内置基类 Exception，自定义异常只需继承 Exception，推荐分层设计：
1. 基础自定义异常（总父类）
2. 细分业务异常（参数错误、权限错误、数据不存在等）

示例代码：
```python
# 自定义异常，继承 Exception
class MyCustomError(Exception):
    """通用自定义异常基类"""
    def __init__(self, msg: str, code: int = 500):
        # 自定义异常信息 + 错误码
        self.msg = msg
        self.code = code
        super().__init__(self.msg)

    # 重写字符串输出，打印更友好
    def __str__(self):
        return f"【错误码{self.code}】{self.msg}"


# 测试抛出自定义异常
def check_age(age):
    if age < 0:
        # 主动抛出自定义异常
        raise MyCustomError("年龄不能为负数", code=400)


if __name__ == "__main__":
    try:
        check_age(-5)
    except MyCustomError as e:
        print("捕获到自定义异常：", e)
        print("错误信息：", e.msg)
        print("错误码：", e.code)
```

## 2. 代码调试与规范

### 2.1 定义
代码调试（Code Debug）是软件开发过程中至关重要的环节，用于定位和修复代码中的错误。Python 提供了多种调试工具和技术，帮助开发者高效地排查问题。

代码风格遵守PEP8代码规范：https://peps.python.org/pep-0008/#introduction

---
### 2.2 代码陷阱示例

可变默认参数为空列表引发的bug示例：
```python
def calc_total(nums, res=[]):
	for n in nums:
		res.append(n)
	return sum(res)

if __name__ == "__main__":
	arr1 = [2, 3, -5]
	print(f"arr1的总和：{calc_total(arr1)}")
	arr2 = [1, 4]
	print(f"arr2的总和：{calc_total(arr2)}")
```

示例陷阱梳理：
1. 函数内定义的变量的作用域仅在函数内，函数执行结束时，会自动销毁释放；
2. 函数默认参数为可迭代对象（列表、字典、集合、字符串）时，该对象在函数内定义时仅创建1次，常驻内存，不会自动清空；
3. 多次调用函数时，需关注是否存在旧数据叠加的问题。

---
### 2.3 常用代码调试方法

1. `print()`：指定行下打印变量值

2. `try-except`：捕获并分析异常信息

3. `PyCharm Debug`：演示断点、单步、查看变量值、继续、终止

4. `pdb调试`：Python 内置的命令行交互式调试器（Python Debugger），不需要额外安装，标准库自带，专门用来断点调试代码，无需IDE，支持打断点、单步执行、查看变量等

---
### 2.4 pdb调试

1. 代码内插入断点（最常用）
Python3.7+ 推荐（官方新语法）
```python
def calc(a, b):
    breakpoint()  # 自动启动pdb断点
    res = a + b
    return res

calc(10, 20)
```

2. 兼容所有 Python 版本（旧写法）
```python
import pdb

def calc(a, b):
    pdb.set_trace()  # 自动启动pdb断点
    res = a + b
    return res

calc(10, 20)
```

3. 命令行启动调试整个脚本
```python
python -m pdb demo.py
```

4. pdb 核心常用命令

|命令	|全称	|作用|
|-------|------|-----|
|l	|list	|查看当前断点附近代码，l 10 查看第 10 行附近|
|n	|next	|单步跳过：执行当前行，到下一行（不进入函数内部）|
|s	|step	|单步进入：如果当前行是函数调用，跳进函数内部|
|r	|return	|执行到当前函数结束，跳出函数|
|c	|continue	|继续运行，直到下一个断点 / 程序结束|
|p 变量名	|print	|打印变量值（p a 查看 a），直接写变量名也能打印|
|pp	|pretty print	|格式化打印字典、列表，更美观|
|q	|quit	|退出 pdb，终止程序|
|b 行号	|break	|在指定行打断点 b 15；b 查看所有断点|
|cl 断点编号	|clear	|删除断点|
|u	|up	|向上切换调用栈（查看上层函数）|
|d	|down	|向下切换调用栈|
|!表达式	|—	|临时执行代码、修改变量 !a=100|

5. 使用示例
```
(Pdb) l          # 查看代码
(Pdb) p num1      # 打印num1值：5
(Pdb) !num1=100   # 临时修改变量
(Pdb) s           # 进入add函数内部
(Pdb) p x,y       # 查看函数参数
(Pdb) r           # 运行到函数return，回到main
(Pdb) c           # 直接跑完程序
```

---
### 2.5 代码检查工具 flake8
flake8 是 Python 代码静态检查工具（linter），一次性整合三类工具：
pyflakes：检测代码逻辑错误、未定义变量、导入无效、语法隐患（不检查格式）
pylint（轻量化替代逻辑）：不，准确拆分：
pycodestyle（原 pep8）：检查代码是否符合 PEP8 编码规范（缩进、空格、行长、空行、命名等格式）
mccabe：检测代码圈复杂度（if/for/while 嵌套太深，代码难以维护）
简单说：flake8 = pyflakes + pycodestyle + mccabe，一键同时查语法 bug、代码格式、复杂度。

安装：`pip install flake8`

1. 检查单个文件
```
flake8 test.py
```

示例：
```
.\2.4flake8.py:3:1: F403 'from pandas import *' used; unable to detect undefined names
.\2.4flake8.py:3:1: F401 'pandas.*' imported but unused
.\2.4flake8.py:5:1: F401 'sys' imported but unused
.\2.4flake8.py:23:43: E712 comparison to True should be 'if cond is True:' or 'if cond:'
.\2.4flake8.py:43:32: E702 multiple statements on one line (semicolon)
.\2.4flake8.py:43:32: E231 missing whitespace after ';'
.\2.4flake8.py:43:55: E702 multiple statements on one line (semicolon)
.\2.4flake8.py:43:55: E231 missing whitespace after ';'
.\2.4flake8.py:43:80: E501 line too long (104 > 79 characters)
.\2.4flake8.py:43:95: E702 multiple statements on one line (semicolon)
.\2.4flake8.py:43:95: E231 missing whitespace after ';'
.\2.4flake8.py:51:9: E722 do not use bare 'except'
```

解释：
```
.\2.4flake8.py:3:1: F403 'from pandas import *' used; unable to detect undefined names F403 禁止通配符导入 import *
.\2.4flake8.py:3:1: F401 'pandas.*' imported but unused F401 导入模块 / 包后全程未使用
.\2.4flake8.py:5:1: F401 'sys' imported but unused F401 导入未使用
.\2.4flake8.py:23:43: E712 comparison to True should be 'if cond is True:' or 'if cond:' E712 禁止使用 == True / == False 布尔常量等值判断
.\2.4flake8.py:43:32: E702 multiple statements on one line (semicolon) E702 禁止分号 ; 在同一行写多条独立语句
.\2.4flake8.py:43:32: E231 missing whitespace after ';' E231 标点符号后必须加空格
.\2.4flake8.py:43:55: E702 multiple statements on one line (semicolon) 
.\2.4flake8.py:43:55: E231 missing whitespace after ';'
.\2.4flake8.py:43:80: E501 line too long (104 > 79 characters) E501 单行代码长度超过限制（flake8 默认 79 字符）
.\2.4flake8.py:43:95: E702 multiple statements on one line (semicolon)
.\2.4flake8.py:43:95: E231 missing whitespace after ';'
.\2.4flake8.py:51:9: E722 do not use bare 'except' E722 禁止无捕获类型的裸 except
```

2. 检查整个项目目录
```
flake8 ./
```
输出示例：
```
./demo.py:10:5: F821 undefined name 'xxx'
./demo.py:15:1: E302 expected 2 blank lines, found 1
./demo.py:22:8: C901 'calc' is too complex (12)
```
分段解释：
文件路径:行号:列号: 错误码 描述
前缀分类：
F：pyflakes 逻辑错误（严重，必须修复）
E：PEP8 格式错误
W：PEP8 格式警告
C：mccabe 复杂度超标

3. flake8常用参数
```
# 忽略指定错误码
flake8 --ignore E501,W291 ./

# 忽略多个错误，逗号分隔
flake8 --ignore F401,E501 ./

# 自定义单行最大长度（默认79，现在很多项目用88）
flake8 --max-line-length=88 ./

# 修改复杂度阈值（超过10才告警）
flake8 --max-complexity=10 ./

# 只展示指定类型错误
flake8 --select F ./  # 只查逻辑错误

# 排除文件夹
flake8 --exclude venv,__pycache__,dist ./
```

4. 配置文件
项目根目录新建 setup.cfg / tox.ini / .flake8，不用每次输长命令。示例 .flake8 文件：
```
[flake8]
max-line-length = 88
max-complexity = 10
ignore = F401,E501
exclude = venv/,dist/,build/,*.pyc
select = E,W,F,C
```

## 3. 日期时间（datetime）

Python内置库日期时间（datetime）包含多个处理日期和时间的类

### 3.1 处理日期（年、月、日）
datetime.date
```python
from datetime import date
today = date.today()
print("今日日期: {today}")
print("今日是{today.year}年{today.month}月{today.day}日")
```

---
### 3.2 处理时间（时、分、秒、微秒）
datetime.time

```python
from datetime import time
t = time(14, 30, 45)
print(f"指定时间：{t}")
```

---
### 3.3 同时处理日期和时间（最常用）
datetime.datetime

```python
from datetime import datetime
now = datetime.now()
print("当前日期和时间:{now}")
```

---
### 3.4 日期时间的计算（常用于日期加减）
datetime.timedelta：

```python
from datetime import datetime, timedelta

now = datetime.now()

# 1. 计算未来时间（加1天、2小时、30分钟）
future = now + timedelta(days=1, hours=2, minutes=30)
print("1天后2小时30分：", future.strftime("%Y-%m-%d %H:%M"))

# 2. 计算过去时间（减3天）
past = now - timedelta(days=3)
print("3天前：", past.strftime("%Y-%m-%d"))

# 3. 计算两个日期的差值
date1 = datetime(2026, 5, 1)
date2 = datetime(2026, 4, 17)
diff = date1 - date2
print("相差天数：", diff.days)  # 输出：34
```

---
### 3.5 日期转字符串

```python
from datetime import datetime
now = datetime.now()
now_str = str(now)
```

---
### 3.6 字符串转日期
使用`strptime(str, format)`将字符串解析为`datetime`类型对象

```python
from datetime import datetime
datetime_str = "2023-10-05 19:30:45"
datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
print(datetime_obj, type(datetime_obj))
```

---
### 3.7 时间戳
1. 时间戳是从 1970 年 1 月 1 日 00:00:00 UTC 开始的秒数（或毫秒数）
2. 1970 是 Unix 诞生的年代
3. 时间戳全世界完全一样，和时区无关，但转出来的本地时间不一样
4. UTC：协调世界时（Coordinated Universal Time），全球统一的标准时间

```python
import time
from datetime import datetime, timedelta, timezone

# 获取当前时间戳
current_timestamp  = time.time()

# 将时间戳转为当前日期和时间
# 未指定时区时，默认使用电脑本地时区
current_datetime = datetime.fromtimestamp(current_timestamp)
print(f"当前日期:{current_datetime}")

# 写法1:将时间戳转为全球统一基准标准时间，通过+8小时获取北京时间
utc_time = datetime.fromtimestamp(current_timestamp, timezone.utc)
# 转成北京时间（UTC+8）
beijing_time1 = utc_time + timedelta(hours=8)
print(f"beijing_time1: {beijing_time1}")

# 写法2:直接指定北京时间
beijing_timezone = timedelta(hours=8)
beijing_time2 = datetime.fromtimestamp(current_timestamp, timezone(beijing_timezone))
print(f"beijing_time2: {beijing_time2}")

# 将datetime对象转为时间戳
timestamp_20260517 = datetime(2026, 5, 17).timestamp()
```

---
### 3.8 时间等待

```python
import time

time.sleep(2)  # 等待2秒
```

---
### 3.9 判断日期为周几

```python
from datetime import datetime
dt = datetime.strptime("2026-05-17", "%Y-%m-%d")
weekday = dt.weekday()  # 获取2026年5月17日为周几，其中0表示周一，6表示周日
```

---
### 3.10 应用场景：计算函数的运行时间

```python
import time

def total(nums):
	start_time = time.time()
	time.time(3)
	end_time = time.time()
	return sum(nums), end_time - start_time

res, cost_time = total(1,2,3)
print(f"运行结果:{res}，运行耗时:{cost_time}")
```

## 4. 文件 I/O

### 4.1 定义
文件 I/O（输入 / 输出） 用于实现程序与外部文件的交互，包括读取文件内容、写入数据到文件等操作。Python 提供了简洁的文件操作接口，主要通过open()函数打开文件，再结合相关方法进行读写。

---
### 4.2 语法
open(file, mode='r', encoding=None)

---
### 4.3 文件操作的基本流程
1. 打开文件 ：使用open()函数，指定文件路径和打开模式，返回文件对象。
2. 操作文件 ：通过文件对象的方法（如read()、write()）进行读写。
3. 关闭文件：使用close()方法关闭文件，释放资源（推荐用with语句自动关闭）。

---
### 4.4 `open()`函数的常用参数
- file：文件路径（绝对路径或相对路径）
- mode：打开模式（决定操作类型），常用模式如下：
  - `'r'`：只读（默认模式），文件不存在则报错
  - `'w'`：只写，覆盖原有内容；文件不存在则创建
  - `'a'`：追加，在文件末尾添加内容；文件不存在则创建
  - `'r+'`：读写，可读取和修改文件
  - `'b'`：二进制模式（如`'rb'`读二进制文件，`'wb'`写二进制文件）
- encoding：编码格式/字符编码
  - UTF-8：通用国际编码，支持全世界所有语言（中文、英文、日文等），兼容性最好，通常不会乱码
  - GBK：中文系统专用编码，主要支持中文和英文，跨平台易乱码，通常在Windows中文环境使用

---
### 4.5 读取文件（`r`模式）
1. 手动关闭文件

```python
file = open("x.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()
```

2. 使用with关键字，自动关闭文件（推荐），必须搭配`as`关键字

```python
with open("x.txt", "r", encoding="utf-8") as file:
	content = file.read()
	print(content)
```

3. 打印文件文本内容时，输出对应行号

```python
with open("x.txt", "r", encoding="utf-8") as file:
	lines = file.readlines()  # 按行方式读取
	for num, line in enumerate(lines):
		print(f"第{num}行：{line.strip()}")
```

`strip()`方法：删除字符串左右两端的空白字符（空格、换行、制表符等）

---
### 4.6 文件写入文本（`w`模式，覆盖写入）
```python
with open("y.txt", "w", encoding="utf-8") as file:
	file.write("Hello, Python\n")  # 写入单行
	file.writelines(["Hello, Java\n"，"Hello, C++\n"])
```

---
### 4.7 文件追加文本（`a`模式，追加写入）
```python
with open("z.txt", "a", encoding="utf-8") as file:
	file.write("Hello, HTML\n")
```

---
### 4.8 文件常见方法总结

| 方法                 | 功能                                     |
| -------------------- | ---------------------------------------- |
| read(size)           | 读取size字节内容，默认读取全部             |
| readline()           | 读取一行内容（包括换行符）                 |
| readlines()          | 读取所有行，返回列表                      |
| write(str)           | 写入字符串（文本模式）或字节（二进制模式）  |
| writelines(iterable) | 写入可迭代对象（如列表）的元素             |
| close()              | 关闭文件                                 |

---
### 4.9 应用场景
日志记录，将程序运行日志写入文件

```python
import datetime

def write_log(message):
    """写入日志，包含时间戳"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[{now}] {message}\n"
    with open("app.log", "a", encoding="utf-8") as file:
        file.write(log)

write_log("程序启动")
write_log("用户登录成功")

# 结果：app.log中追加带时间戳的日志
```

## 5. CSV 文件操作

对CSV、JSON、EXCEL文件操作前，前置依赖安装

```bash
# csv 内置无需安装
# json 内置无需安装
# excel 需要第三方库
pip install pandas openpyxl xlsxwriter
```

两种方案：**内置 csv 模块**（轻量）、**pandas**（数据分析首选）

### 5.1 写入CSV

```python
import csv

data = [
    ["姓名", "年龄", "城市"],
    ["张三", 20, "北京"],
    ["李四", 22, "上海"]
]

# 写入
with open("test.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# 单行写入
with open("test.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["王五", 25, "深圳"])
```

### 5.2 读取CSV

```python
import csv

# 按行读取列表
with open("test.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 读取为字典（带表头）
with open("test.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["姓名"], row["年龄"])
```

### 5.3 Pandas 操作CSV

```python
import pandas as pd

# 写入
df = pd.DataFrame([
    {"姓名": "张三", "年龄": 20},
    {"姓名": "李四", "年龄": 22}
])
df.to_csv("pd_test.csv", index=False, encoding="utf-8-sig")

# 读取
df = pd.read_csv("pd_test.csv", encoding="utf-8-sig")
print(df)
# 筛选数据
print(df[df["年龄"] > 20])
```

## 6. JSON 文件操作

内置 `json` 库，无需额外安装
核心方法：`json.dumps()` 对象转字符串 / `json.dump()` 写入文件；`json.loads()` 字符串转对象 / `json.load()` 读文件

### 6.1 写入JSON文件

```python
import json

info = {
    "name": "小明",
    "age": 18,
    "hobbies": ["篮球", "编程"]
}

# 写入文件，indent格式化输出
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)
```

### 6.2 读取JSON文件

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    res = json.load(f)
print(res["name"], res["hobbies"][0])
```

### 6.3 字符串与对象互转（内存操作）

```python
import json

# 对象 → json字符串
s = json.dumps(info, ensure_ascii=False)
print(s)

# json字符串 → python对象
obj = json.loads(s)
print(obj["age"])
```

### 6.4 Pandas 读写JSON

```python
import pandas as pd

# json转df
df = pd.read_json("data.json")
# df导出json
df.to_json("out.json", orient="records", force_ascii=False)
```

## 7. Excel 文件操作（.xlsx/.xls）

三大常用方式：

1. pandas + openpyxl（读写.xlsx，主流）
2. openpyxl 原生操作单元格（精细控制）
3. xlsxwriter 用于生成带格式图表Excel

### 7.1 Pandas 快速读写Excel（推荐批量数据）

```python
import pandas as pd

# 构造数据
df = pd.DataFrame({
    "姓名": ["小红", "小刚"],
    "分数": [90, 88]
})

# 写入Excel
df.to_excel("student.xlsx", sheet_name="成绩", index=False)

# 读取Excel
df = pd.read_excel("student.xlsx", sheet_name="成绩")
print(df)
```

### 7.2 openpyxl 原生精细操作单元格（修改、合并、填值）

```python
from openpyxl import Workbook, load_workbook

# 1. 新建Excel写入
wb = Workbook()
ws = wb.active
ws.title = "员工表"

# 写入单元格
ws["A1"] = "工号"
ws["B1"] = "薪资"
ws.append(["001", 8000])
ws.append(["002", 12000])

wb.save("staff.xlsx")

# 2. 读取已有Excel
wb = load_workbook("staff.xlsx")
ws = wb["员工表"]
# 遍历所有行
for row in ws.iter_rows(values_only=True):
    print(row)
```

### 7.3 xlsxwriter 生成带格式Excel

```python
import xlsxwriter

wb = xlsxwriter.Workbook("format.xlsx")
ws = wb.add_worksheet()
# 定义格式
bold = wb.add_format({"bold": True, "font_size": 12})
ws.write("A1", "标题", bold)
ws.write("A2", 100)
wb.close()
```

## 8. 三种文件格式

### 8.1 CSV ↔ JSON

```python
import pandas as pd

# csv转json
df = pd.read_csv("pd_test.csv", encoding="utf-8-sig")
df.to_json("csv2json.json", orient="records", force_ascii=False)

# json转csv
df = pd.read_json("csv2json.json")
df.to_csv("json2csv.csv", index=False, encoding="utf-8-sig")
```

### 8.2 Excel ↔ CSV

```python
import pandas as pd

# excel 转 csv
df = pd.read_excel("student.xlsx")
df.to_csv("excel2csv.csv", index=False, encoding="utf-8-sig")

# csv 转 excel
df = pd.read_csv("excel2csv.csv", encoding="utf-8-sig")
df.to_excel("csv2excel.xlsx", index=False)
```

### 8.3 常用场景总结

| 文件 | 内置工具 | 第三方工具 | 适用场景 |
| --- | --- | --- | --- |
| CSV | csv | pandas | 纯文本表格，轻量交换数据 |
| JSON | json | pandas | 接口数据、嵌套结构化数据 |
| Excel | 无 | openpyxl/pandas/xlsxwriter | 复杂报表、带格式、业务表格 |

### 8.4 关键注意点

1. 中文乱码：
    - csv：`encoding="utf-8-sig"`
    - json：`ensure_ascii=False`
2. csv写入必须加 `newline=""` 避免空行
3. openpyxl 仅支持 `.xlsx`，老 `.xls` 需要 xlrd 旧版本
4. 超大文件优先用内置模块逐行读取，避免pandas一次性加载内存溢出

## 相关知识

- [[Python Knowledge Map]]
- [[Python Basics 3]]：函数、装饰器与面向对象。
- [[Python Basics 5 Iterables Iterators and Generators]]：逐行处理超大文件。
- [[YAML Notes]]：另一种常用配置文件格式。
- [[Database Basics 2#二、假数据生成|使用 Faker 生成数据]]
