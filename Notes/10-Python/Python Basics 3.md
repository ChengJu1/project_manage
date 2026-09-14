# Python基础-3

## 1. 运算符

### 1.1 算术运算符
| 运算符 | 描述                     | 示例            | 运算结果  |
| ------ | ------------------------ | --------------- | --------- |
| +      | 加法 / 字符串拼接        | 3 + 2 / "a"+"b" | 5 / "ab"  |
| -      | 减法 / 取负              | 3 - 2 / -5      | 1 / -5    |
| *      | 乘法 / 字符串重复        | 3 * 2 / "a"*3   | 6 / "aaa" |
| /      | 除法（结果永远是浮点数） | 5 / 2           | 2.5       |
| //     | 整除（向下取整，注意负数） | 5 // 2        | 2         |
| %      | 取模（求余数）           | 5 % 2           | 1         |
| **     | 幂运算（次方）           | 2 ** 3          | 8         |

---


### 1.2 赋值运算符

| 运算符 | 描述             | 实例                                  |
| ------ | ---------------- | -------------------------------- |
| =      | 简单的赋值运算符 | c = a + b 将 a + b 的运算结果赋值为 c |
| +=     | 加法赋值运算符   | c += a 等效于 c = c + a               |
| -=     | 减法赋值运算符   | c -= a 等效于 c = c - a               |
| *=     | 乘法赋值运算符   | c *= a 等效于 c = c * a               |
| /=     | 除法赋值运算符   | c /= a 等效于 c = c / a               |
| %=     | 取模赋值运算符   | c %= a 等效于 c = c % a               |
| **=    | 幂赋值运算符     | c \**= a 等效于 c = c ** a            |
| //=    | 取整除赋值运算符 | c //= a 等效于 c = c // a             |

---
### 1.3 身份运算符

身份运算符用于比较两个对象的存储单元：`is` / `is not`：比较是否同一对象（id 相同）

| 运算符 | 描述            | 实例         |
| --------- | --------- | -------------- |
| is     | 判断两个标识符是不是引用自一个对象     | x is y，类似 id(x) == id(y) , 如果引用的是同一个对象则返回 True，否则返回 False |
| is not | 判断两个标识符是不是引用自不同对象 | x is not y ， 类似 id(a) != id(b)。如果引用的不是同一个对象则返回结果 True，否则返回 False. |

举个例子：
```python
a = [1,2]
b = [1,2]
print(a == b)  # True 值相等
print(a is b)  # False 不是同一个对象
```

---
### 1.4 比较运算符
返回布尔值 True/False
|运算符	|描述	|示例|
| ------ | --------- | ----------------------- |
|==	|等于（判断值是否相等）|	1 == 1 → True|
|!=	|不等于|	1 != 2 → True|
|>	|大于|	5 > 3 → True|
|<	|小于|	5 < 3 → False|
|>=	|大于等于|	5 >= 5 → True|
|<=	|小于等于|	3 <= 5 → True|

---
### 1.5 逻辑运算符
 |运算符	 |逻辑含义 |	规则 |
| ------ | ---------------- | ----------------------- |
 |and	 |逻辑与 |	两边都为 True，结果才为 True；一假则假 |
 |or	 |逻辑或 |	两边有一个为 True，结果就为 True；一真则真 |
 |not	 |逻辑非 |	取反：True → False，False → True |

---
### 1.6 成员运算符
| 运算符 | 描述                          |
| ------ | ----------------------------- |
| in     | 如果元素在序列中，返回 True   |
| not in | 如果元素不在序列中，返回 True |

---
### 1.7 条件语句

用于根据不同的条件执行不同的代码块，核心是通过判断条件的真假（True或False）来决定程序的执行路径。Python 的条件语句主要通过if、elif（else if 的缩写）和else关键字实现。

- 单分支：`if 条件:`
- 双分支：`if...else...`
- 多分支：`if...elif...else...`
- 嵌套 if：`if...if...else`
- 多条件判断（结合逻辑运算）：`and`、`or`、`not`

真假判定：
- 假：0、0.0、"" 空字符串、空容器、None
- 真：非0数字、非空字符串、非空容器

三元表达式：
```python
score = 70
res = "及格" if score >= 60 else "不及格"
print(res)
```

---
## 2. 循环语句

### 2.1 for 循环

for循环用于遍历可迭代对象（如列表、字符串、元组、字典、范围等），按顺序依次访问每个元素并执行代码块。

常见操作：
1. 遍历：列表、字符串、元组、字典
2. 生成数字序列：`range(start, end, step)`

range用法：
- `start`：起始值，默认 0
- `end`：结束值（**取不到该数**，左闭右开）
- `step`：步长，默认 1，支持负数（倒序）
举个例子：
```python
for i in range(5):        # 0,1,2,3,4
for i in range(1, 11):    # 1~10
for i in range(10, 0, -1):# 10~1 倒序
```

---
### 2.2 while 循环

while循环在条件为True时重复执行代码块，适用于循环次数不确定的场景。

注意：while循环需手动更新条件，避免死循环（`while True`），大多数情况需要搭配`break`退出。

常见操作：

1. 循环计数
2. 用户输入判断
3. while-else结构
4. range(start, end, step)

---
### 2.3 循环控制

- `break`：立即终止当前循环，跳出循环体。
- `continue`：跳过当前循环的剩余部分，直接进入下一次循环。
- `pass`：占位，不执行任何操作。


---
## 3. 函数

### 3.1 定义

函数（function）是一段封装了特定功能的可重用代码块，通过函数名可以多次调用，避免重复编码，提高代码的可读性和维护性。函数可以接收输入参数（参数）并返回输出结果。

---
### 3.2 基本语法
函数的基本结构函数通过def关键字定义：
```
def 函数名(参数1, 参数2...):
	函数体
	return 返回值（可选）
```

---
### 3.3 无参数、无返回值的函数

```python
def hello():
	print("hello!Python!")
```

---
### 3.4 有参数、无返回值的函数

```python
def hello(name):
	print(f"hello!{name}!")
```

---
### 3.5 有参数、有返回值的函数

```python
def hello(name):
	return f"hello!{name}!"
```

---
### 3.6 带默认参数的函数

```python
def hello(name="张三"):
	return f"hello!{name}""
```

---
### 3.7 位置参数（*args）
作用：接收不定长参数，让函数能兼容任意个数的入参，常写在通用函数、装饰器里。
- *：解包 / 打包位置参数
- args（约定变量名，可改）：把多余的位置参数打包成元组 (tuple)
- 放在普通位置参数后面
```python
def total(*args):
	return sum(args)

def func(a, b, *args):
    print(a, b)
    print(args)

func(1, 2)
func(1, 2, 3, 4, 5)
```

---
### 3.8 关键字参数（**kwargs）
作用：接收不定长参数，让函数能兼容任意个数的入参，常写在通用函数、装饰器里。
- **：打包关键字参数
- kwargs（约定变量名，可改）：把多余关键字参数打包成字典 (dict)
- 必须放在 *args 后面
```python
def print_kwargs(**kwargs):
	for k, v in kwargs.items():
		print(f"{k}: {v}")
```
固定顺序：普通参数 → *args → kwargs
```python
def func(a, b, *args, **kwargs):
    print("普通参数：", a, b)
    print("位置元组：", args)
    print("关键字字典：", kwargs)

func(1, 2, 3, 4, name="李四", score=90)
```

---
### 3.9 嵌套函数
函数内部定义另一个函数，内部函数可访问外部函数的变量。

```python
def outer_func(message):
	def inner_func():
		print(message)
	inner_func()
```

---
### 3.10 函数解包
```python
def user_info():
	return "Alice", 18, "SC"

name, age, major = user_info()
```

## 4. lambda 匿名函数
lambda 用来创建小型匿名函数，语法简洁，适合简单逻辑，无需用 def 定义命名函数。

---
### 4.1 基础语法
```
lambda 参数列表: 表达式
```
- 没有函数名，故称匿名函数
- 只能有单一表达式，不能写赋值语句（a=10，不包含设置默认参数）、打印语句（print）、`if 分支块`、`for 循环`、`return`
- lambda 设计初衷：计算并返回，自动将表达式计算后的结果作为返回值
- 参数可多个、无参数、带默认参数

表达式和语句块的区别：
- ✅ 合法：`lambda x: "A" if x > 60 else "B"` （这是表达式）
- ❌ 非法：`lambda x: if x > 60: return "A" else: return "B"` （这是语句块）
简单来说：表达式是为了得到一个值，而语句是为了执行一系列操作。
直观解释：
1. 输入 `3 + 4` 并回车 ➡️ 解释器会直接显示 `7`（因为它是表达式，有输出）。
2. 输入 `x = 3 + 4` 并回车 ➡️ 解释器没有任何输出（因为它是赋值语句，只执行了动作，不产生值）

lambda 与 普通函数的示例：
```python
# 普通函数
def add(x, y):
    return x + y

# 等价 lambda
add_lam = lambda x, y: x + y

print(add(1,2))      # 3
print(add_lam(1,2))  # 3
```

两者区别：
1. `lambda` 一行写完，仅限简单表达式
2. 不能写多行代码、复杂逻辑、函数文档
3. 多用于临时、一次性调用

---
### 4.2 无参数

```python
f = lambda: "Hello lambda"
print(f())  # 输出: Hello lambda
```

---
### 4.3 单个参数

```python
f = lambda x: x * 2
print(f(3))  # 输出: 6
```

---
### 4.4 多个参数

```python
f = lambda x, y: x + y
print(f(2, 5))  # 输出: 7
```

---
### 4.5 带默认参数

```python
f = lambda x, y=3: x * y
print(f(2))   # 输出: 6
print(f(2,4)) # 输出: 8
```

---
### 4.6 lambda搭配高阶函数

lambda 极少单独赋值使用，主要配合高阶函数：`map()`、`filter()`、`sorted()`

---
### 4.7 `map()`

`map()`是Python内置高阶函数之一，作用：把一个函数依次作用到序列的每一个元素上，返回迭代器。
- 基础语法：map(函数, 可迭代对象1, 可迭代对象2...)，例如：列表、元组、字符串等可迭代对象
- 返回值：map 迭代器，需要用 list() / tuple() 转成容器才能直观查看

基于map()实现对列表进行幂等处理：
```python
def square(x):
    return x ** 2

nums = [1,2,3]
res = list(map(square, nums))
print(res)  # [1, 4, 9]
```

---
### 4.8 lambda +  map()

对序列每个元素执行同一逻辑：
```python
nums = [1,2,3,4]
res = list(map(lambda x: x**2, nums))
print(res)  # [1, 4, 9, 16]
```

---
### 4.9 lambda + map() + 多迭代对象

对两个列表进行叠加处理：
```python
a = [1,2,3]
b = [10,20,30]
# 两数相加
res = list(map(lambda x,y: x+y, a, b))
print(res)  # [11, 22, 33]
```

---
### 4.10 lambda + map() 实现类型转换

```python
str_nums = ["1", "2", "3"]
# 全部转整数
res = list(map(int, str_nums))
print(res)  # [1, 2, 3]
```

---
### 4.11 `filter()`

`filter()`是内置高阶函数，作用：根据判断条件过滤可迭代对象，只保留结果为 `True` 的元素。
- 基础语法：filter(判断函数, 可迭代对象)
- 第一个参数：条件函数（返回布尔值 `True/False`）
- 第二个参数：列表、元组等可迭代对象
- 返回值：`filter` 迭代器，需用 `list()`/`tuple()` 转为容器查看

---
### 4.12 lambda + filter() 过滤元素

仅保留表达式结果为 `True` 的元素：
```python
nums = [1,2,3,4,5,6]
# 保留偶数
res = list(filter(lambda x: x % 2 == 0, nums))
print(res)  # [2, 4, 6]
```

拆解代码：
```
逐个取出 nums 中的元素，传给 lambda x: x % 2 == 0
逻辑：x % 2 == 0 判断是否是偶数
1：1%2=1 → False → 舍弃
2：2%2=0 → True → 保留
3：False、4：True、5：False、6：True
filter 筛选后得到迭代器，list() 转成列表，最终结果 [2,4,6]
```

---
### 4.13 lambda + sorted() 自定义排序

使用语法：`sorted(序列, key=排序规则)`

```python
# 按元素长度排序
words = ["apple", "hi", "banana"]
res = sorted(words, key=lambda s: len(s))
print(res)  # ['hi', 'apple', 'banana']

# 二维列表按指定列排序
data = [[2,3], [1,9], [5,1]]
# 按第二个元素升序
res = sorted(data, key=lambda x: x[1])
print(res)  # [[5, 1], [2, 3], [1, 9]]

# 按 字典键 (key) 排序。
d = {"banana": 3, "apple": 1, "orange": 2}
sorted_items = sorted(d.items(), key=lambda x: x[0])
print(dict(sorted_items))

# 按 字典值 (value) 排序（最常用）
d = {"张三": 20, "李四": 18, "王五": 22}
sorted_items = sorted(d.items(), key=lambda x: x[1])
print(sorted_items)
new_d = dict(sorted_items)
print(new_d)
```

---
### 4.14 lambda + 三元表达式

lambda 内不能用多行`if`，但支持三元表达式（`表达式1 if 条件 else 表达式2`）：

```python
# 大于0返回正数，否则返回0
f = lambda x: x if x > 0 else 0
print(f(-5))  # 0
print(f(8))   # 8
```

---
### 4.15 嵌套lambda

```python
f = lambda x: lambda y: x + y
g = f(10)
print(g(5))  # 15

# ============================
# 外层函数，接收 x
def f(x):
    # 内层函数，接收 y
    def g(y):
        return x + y
    # 返回内层函数
    return g

g = f(10)
print(g(5))  # 15
```

## 5. 作用域

### 5.1 变量作用域

作用域：**变量的生效范围**，分为 局部作用域、全局作用域。

局部变量：定义在函数内部，仅函数内可用，函数结束就销毁。

全局变量：定义在函数外部，整个文件都能访问。

- 函数外：全局变量
- 函数内：局部变量（默认无法修改全局变量）
- 关键字 `global`：在函数内修改全局变量

---
### 5.2 仅读取全局变量（不用 global）
```python
# 全局变量
num = 100

def read_num():
    # 仅读取全局变量，无需 global
    print("函数内读取全局变量：", num)

# 调用函数
read_num()
print("函数外全局变量：", num)
```

---
### 5.3 函数内直接赋值
如果不使用 global，在函数内对全局变量赋值，Python 会默认创建新的局部变量，
而非修改全局变量；若先读取再赋值，直接报错。

```python
num = 100

def change_num():
    # 试图修改全局变量，未加 global
    print(num)   # 报错：局部变量在赋值前被引用
    num = 200

change_num()
```

---
### 5.4 使用 global 正确修改全局变量
global 只能写在函数内部，绝对不能放在函数外面。
定义全局变量
```python
num = 100

def change_num():
    # 声明 num 是全局变量
    global num
    # 读取 + 修改全局变量
    print("修改前：", num)
    num = 200
    print("函数内修改后：", num)

# 调用函数
change_num()
# 函数外查看，全局变量已被修改
print("函数外全局变量：", num)
```

---
### 5.5 局部变量和全局变量重名
函数内不加 global，同名变量是局部变量，和外部全局变量互不干扰
```python
name = "张三"  # 全局变量

def func():
    name = "李四"  # 局部变量，不影响全局
    print("函数内局部变量：", name)

func()
print("函数外全局变量：", name)
```

## 6. 递归函数

### 6.1 定义
递归：函数自己调用自己，用来解决重复、可拆分的问题。 
必备两个条件：
- 递归出口（终止条件）：必须有，否则无限递归报错；
- 递归递推：函数不断调用自身，向出口靠近。

---
### 6.2 基础示例：阶乘

公式：`n! = n * (n-1)!`，`0! = 1! = 1`（出口），数学规定0 ! = 1

```python
def factorial(n):
    # 递归出口
    if n == 1 or n == 0:
        return 1
    # 递归调用
    return n * factorial(n - 1)

print(factorial(5))   # 120
```

执行流程：

```
factorial(5) → 5*factorial(4) → 4*factorial(3) … → factorial(1)=1
```

---
### 6.3 递归易错点

- 忘记递归出口 → 栈溢出报错 `RecursionError`；

```python
# 错误写法：缺少递归出口
def fact(n):
    # 只写递归调用，没有结束条件
    return n * fact(n - 1)

# 运行代码
fact(5)
```

- 递归层数太深，Python 默认递归深度有限（默认约 1000 层）。

```python
# 错误写法：缺少递归出口
def much_level(n):
    print(n)
    much_level(n + 1)  # 一直自增调用

# 从 1 开始递归，层数会持续上涨
much_level(1)
```

## 7. 装饰器

### 7.1 定义
装饰器：在不修改原函数代码、不改变原函数调用方式的前提下，给函数新增功能。 

本质：高阶函数 + 嵌套函数 + 闭包

---
### 7.2 装饰器模板

```python
# 定义装饰器
def decorator(func):
    # 内层函数：增加额外逻辑
    def wrapper():
        print("执行前：新增功能")
        func()          # 执行原函数
        print("执行后：新增功能")
    return wrapper

# 方式1：语法糖 @ （推荐）
@decorator
def say_hello():
    print("Hello World")

# 调用
say_hello()
```

输出：

```python
执行前：新增功能
Hello World
执行后：新增功能
```

---
### 7.3 原理拆解

```python
def decorator(func):
    def wrapper():
        print("前置逻辑")
        func()
        print("后置逻辑")
    return wrapper

def say_hello():
    print("Hello")

# 手动装饰
say_hello = decorator(say_hello)
say_hello()
```

---
### 7.4 装饰带参数的原函数

如果原函数有参数，内层 `wrapper` 也要接收参数：

```python
def decorator(func):
    def wrapper(a, b):
        print("开始计算")
        res = func(a, b)
        print("计算结束")
        return res
    return wrapper

@decorator
def add(x, y):
    return x + y

print(add(3, 5))
```

---
### 7.5 可变参数（通用）装饰器

适配任意参数： `*args, **kwargs`

```python
def decorator(func):
    # 接收任意位置参数、关键字参数
    def wrapper(*args, **kwargs):
        print("函数开始运行")
        result = func(*args, **kwargs)
        print("函数运行结束")
        return result
    return wrapper

@decorator
def f1(x):
    return x * 2

@decorator
def f2(a, b):
    return a + b

print(f1(10))
print(f2(2, 8))
```

---
### 7.6 装饰器场景示例

举个例子：统计函数运行时间
```python
import time

def count_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f"函数耗时：{end - start:.4f} 秒")
        return res
    return wrapper

@count_time
def time_test():
    for i in range(1000000):
        pass

time_test()
```

## 8. 面向对象编程（OOP）

### 8.1 OOP基础概念
面向对象编程（Object-Oriented Programming）：以类和对象为核心组织代码，是主流编程思想。
- 类（Class）：模板，抽象描述一类事物的属性（特征）和方法（行为）。
- 对象（实例/Instance）：类的具体产物，根据模板创建出的真实个体，拥有类定义的属性和方法。

> 一句话总结：类是模板，对象是模板造出来的实例。

---
### 8.2 OOP 四大核心特性
1. 抽象：提取事物通用特征与行为，忽略无关细节，提炼成类。
2. 封装：将属性和方法绑定在一起，隐藏内部细节，仅对外提供访问接口，保障数据安全。
3. 继承：子类复用父类的属性和方法，实现代码复用，可扩展/重写功能。
4. 多态：不同类的对象，调用**同名方法**时表现出不同行为。

---
### 8.3 类的定义 & 实例化
语法格式：
```python
# 定义类
class 类名:
    # 实例初始化方法
    def __init__(self, 参数):
        self.属性 = 参数  # 绑定实例属性

    # 实例方法（第一个参数必须是 self，代表当前实例对象）
    def 方法名(self):
        逻辑代码

# 实例化对象：类名()
对象变量 = 类名(传参)
```

示例：
```python
class Student:
    # 初始化方法：创建对象时自动执行
    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age

    # 实例方法
    def study(self):
        print(f"{self.name} 正在学习")

# 创建对象（实例化）
stu1 = Student("小明", 18)
stu1.study()  # 调用方法
print(stu1.name)  # 访问属性
```

---
### 8.4 对象生命周期
对象从诞生到销毁分为5个生命周期阶段：

1. 类定义阶段：执行 `class` 代码块，创建类对象，类属性、方法绑定完成
2. 实例化创建阶段：调用 `()` 生成空实例对象（分配内存）
3. 实例初始化阶段：给实例属性赋值、完成自定义初始化逻辑
4. 对象存活使用阶段：程序中正常调用实例属性、方法，对象被引用
5. 垃圾回收销毁阶段：引用计数归 0，解释器回收内存，清理资源

主要涉及3个特殊魔法方法：

1. `__new__(cls)` 构造方法
   - 执行时机：**最先执行**，负责分配内存、创建空实例。
   - 参数 `cls`：代表当前类本身，必须返回创建的对象。
2. `__init__(self)` 初始化方法
   - 执行时机：`__new__` 创建对象后自动执行，**绑定实例属性、做初始化**。
   - 最常用方法，创建对象时传参本质是传给 `__init__`。
3. `__del__(self)` 析构方法
   - 执行时机：对象**引用计数为0**时，Python 垃圾回收自动调用，用于收尾操作。
   - 禁止手动调用，循环引用时会由垃圾回收机制兜底处理。

示例代码：
```python
class Person:
    def __new__(cls):
        print("1. 分配内存，创建空对象")
        return super().__new__(cls)

    def __init__(self):
        print("2. 初始化对象属性")

    def __del__(self):
        print("3. 对象被销毁，内存回收")

p = Person()
del p  # 手动删除引用，引用计数归0，触发 __del__
```

---
### 8.5 对象引用计数规则
- 变量指向对象 → 引用计数 +1
- 变量重新赋值、`del` 删除引用、局部变量出作用域 → 引用计数 -1
- 引用计数 = 0、局部变量出作用域（无外部引用） → 触发 `__del__`，回收内存

`sys.getrefcount(obj) `函数来获取某个对象的引用计数。请注意：调用 getrefcount() 本身会临时增加对象的引用计数（因为它接收了对象作为参数），所以结果通常会比预期多 1。

---
### 8.6 类的成员与访问控制
类的成员分为属性和方法，Python 通过命名规则实现访问权限控制（语法约定）。

1. 三种成员权限

| 命名规则 | 类型 | 访问规则|
|--------|------|----------|
| `name` | 公有成员 | 类内部、子类、外部代码均可自由访问 |
| `_name` | 受保护成员 | 约定：仅类内部、子类使用，外部不建议直接访问（语法不限制） |
| `__name` | 私有成员 | Python 自动做名称改写，外部无法通过原名直接访问，实现真正隐藏 |


示例：
```python
class Test:
    def __init__(self):
        self.pub = "公有"
        self._pro = "受保护"
        self.__pri = "私有"

t = Test()
print(t.pub)    # 正常访问
print(t._pro)   # 语法允许，但不推荐外部使用
# print(t.__pri) # 报错，外部无法直接访问私有属性
```

2. 属性管控：Getter / Setter
私有属性不能直接修改，为了**数据校验、逻辑拦截**，提供两种取值/赋值方式。

传统 get/set 方法（基础写法）
手动定义方法获取、修改私有属性，适合简单场景。
```python
class Student:
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    # Getter：获取属性
    def get_name(self):
        return self.__name

    # Setter：修改属性（增加数据校验）
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError("分数必须在 0~100 之间")

stu = Student("小红", 90)
print(stu.get_name())
stu.set_score(88)
# stu.set_score(101)  # 触发异常
```

---
### 8.7 @property 装饰器（Python 推荐写法）
1. 定义：让私有属性像普通属性一样读写，代码更简洁，是项目主流用法。
- `@property`：装饰 Getter 方法，用于**读取**属性
- `@属性名.setter`：装饰 Setter 方法，用于**修改**属性

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # 私有属性

    # 读取余额
    @property
    def balance(self):
        return self.__balance

    # 修改余额（带校验）
    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self.__balance = amount
        else:
            raise ValueError("余额不能为负数")

acc = BankAccount("Alice", 1000)
print(acc.balance)   # 读取，调用 property
acc.balance = 2000   # 赋值，调用 setter
# acc.balance = -100  # 触发异常
```

2. 大多用来读取私有下划线变量

我们平时写 `@property` 基本都是配套 `_xxx` 私有实例变量：

```python
class Person:
    def __init__(self):
        self._age = 18  # 单下划线约定私有

    @property
    def age(self):
        # 读取内部私有变量
        return self._age

p = Person()
print(p.age)  # 不用括号，拿到 _age 的值
```

这里的作用：对外暴露 `p.age`，但不让别人直接改 `p._age`，实现封装。

3. @property 不仅能读取 `_xxx`，它可以任意计算逻辑

它的函数里不一定非要返回某个私有属性，可以实时计算、拼接、判断，这才是它的核心价值。

例如动态计算，无对应 _xxx 变量

```python
class Rect:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    @property
    def area(self):
        # 没有 self._area 这个变量，实时现场计算
        return self.width * self.height

r = Rect(3,4)
print(r.area) # 12，每次访问都会重新算一遍
```

这里根本不存在 `_area`，但依然能用 `@property`。

4. 多属性拼接

```python
class User:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

u = User("张", "三")
print(u.full_name)
```

同样没有 `_full_name` 存储字段，只是实时拼接。

5. 带校验、转换逻辑

```python
class Student:
    def __init__(self):
        self._score = 95

    @property
    def score(self):
        val = self._score
        # 加工后再返回，不是单纯直接返回 _score
        if val >= 60:
            return "及格"
        else:
            return "不及格"
```

6. @property 的真正本质

它是把一个方法函数，改造成像实例属性一样访问（不加括号）的描述器。
函数内部你想写什么逻辑都行：读私有变量、实时计算、数据转换、权限判断、接口请求……没有限制。

7. 总结

- 表象：绝大多数场景下，我们用它读取 `self._xxx` 私有变量；
- 本质：不限定只能读私有变量，函数内可任意逻辑；
- 双下划线 `__xxx` 几乎不和 property 配合使用。

---
### 8.8 继承
- 父类（基类）：被继承的类
- 子类（派生类）：继承父类的类，自动拥有父类所有公有/受保护属性和方法
- 作用：代码复用、功能扩展

语法：
```python
class 子类名(父类名):
    # 子类自己的属性和方法
```

示例代码：

```python
# 父类
class Phone:
    def call(self):
        print("可以打电话")

# 子类直接继承，不重写任何方法
class Smartphone(Phone):
    pass

p = Smartphone()
p.call()
```

---
### 8.9 方法重写
  子类定义与父类**同名方法**，会覆盖父类方法，实现功能改写。

```python
# 父类：交通工具
class Vehicle:
    def run(self):
        print("交通工具在路上行驶")

# 子类：自行车，继承Vehicle
class Bike(Vehicle):
    def run(self):
        print("自行车靠脚蹬前进")

# 调用
bike = Bike()
bike.run()
```

---
### 8.10 内置函数`super()`
当子类重写了父类的 `__init__` 或普通方法后，若想保留父类原有逻辑，再扩展新功能，使用 `super()` 调用父类方法，即`super().xxx()`主动触发上层父类链里的 xxx 方法，用来复用父类逻辑。

Python3 简化语法：`super()` 无需传参。

示例代码：子类扩展初始化方法
```python
# 父类
class Computer:
    def __init__(self, brand):
        self.brand = brand

    def show(self):
        print(f"品牌：{self.brand}")

# 子类
class Laptop(Computer):
    def __init__(self, brand, size):
        # 调用父类的__init__
        super().__init__(brand)
        self.size = size

    def show(self):
        super().show()  # 调用父类show方法
        print(f"屏幕尺寸：{self.size}英寸")

pc = Laptop("华为", 14)
pc.show()
```

---
### 8.11 方法解析顺序 (MRO，Method Resolution Order) 
当类存在多继承时，一个对象调用方法，Python 需要一套固定规则，决定从哪个父类开始、按什么顺序查找方法 / 属性，这套查找顺序就叫 MRO。

举个例子：
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

---
### 8.12 查看一个类的MRO
```python
print(D.__mro__)
# (D, B, C, A, object)
print(D.mro())
# [D, B, C, A, object]
```

---
### 8.13 C3 线性化核心规则（MRO 生成规则）
C3 的全称：Class Combination Composition Calculation，直译：类组合合并算法，业内统一简称 C3 线性化（C3 Linearization）。

三个 C 分别对应：
- Class：处理类的继承关系
- Combination：合并多条父类继承链
- Composition：保证继承结构的组合顺序一致性

具体规则：
- 规则 1：子类永远出现在父类前面，子类一定比它所有父类先被查找。
例：D 在 B、C、A 前面；B、C 在 A 前面。

- 规则 2：父类继承顺序保持原有书写顺序
class D(B, C) 先写 B 后写 C，MRO 里 B 一定在 C 前面，不能颠倒。

- 规则 3：不能出现冲突（局部优先，无循环）
禁止出现矛盾继承，比如：
```python
# 报错：无法生成合法MRO
class X(Y): pass
class Y(X): pass
```

- 规则 4：菱形继承只保留一份公共父类
像上面 D (B,C)，B 和 C 都继承 A，MRO 中 A 只出现一次，不会重复。

总结：
MRO 是 Python 规定的从上到下、从左到右、子类优先的类查找顺序；
super() 不是固定找直接父类，而是顺着 MRO 取下一个类，完美适配多继承。

---
### 8.14 多态
多态依托继承+方法重写实现：多个子类继承同一个父类，并重写同名方法；使用统一的调用方式，不同子类对象执行不同逻辑。

示例代码：
```python
# 父类：所有员工通用
class Staff:
    def __init__(self, name, id_card):
        self.name = name
        self.id_card = id_card

    def clock_in(self):
        print(f"{self.name} 打卡上班")

    def get_salary(self):
        pass

# 子类1：全职员工，继承所有员工功能
class FullStaff(Staff):
    def get_salary(self):
        print(f"{self.name} 按月发月薪")

# 子类2：兼职员工，继承所有员工功能
class PartStaff(Staff):
    def get_salary(self):
        print(f"{self.name} 按小时结工资")

# 测试
a = FullStaff("李四", "110xxx")
a.clock_in()
a.get_salary()

b = PartStaff("王五", "120xxx")
b.clock_in()
b.get_salary()
```

---
### 8.15 类方法（Class Method）

类方法需要使用 @classmethod 装饰器来定义，它的第一个参数约定俗成地命名为 cls，代表类本身。与 self 只能操作具体的实例不同，cls 能够直接访问和修改类的状态、甚至创建类的实例。

在 Python 中，类方法和普通方法（实例方法）的核心区别在于它们绑定的对象不同：普通方法绑定的是实例对象（Instance），而类方法绑定的是类本身（Class）。

```python
class BankAccount:
    # 1. 类属性：所有账户共享的“当前基准利率”
    interest_rate = 0.02  

    def __init__(self, owner, balance):
        # 2. 实例属性：每个客户独有的“姓名”和“余额”
        self.owner = owner  
        self.balance = balance 

    # 【普通方法】：计算单个账户的利息
    # 必须依赖具体实例的余额 (self.balance)，所以用普通方法
    def calculate_interest(self):
        return self.balance * BankAccount.interest_rate

    # 【类方法】：修改全局共享的“基准利率”
    # 操作的是所有账户共享的类属性，所以用类方法
    @classmethod
    def set_interest_rate(cls, new_rate):
        cls.interest_rate = new_rate
        print(f"银行通知：全局基准利率已调整为 {new_rate}")

    # 【类方法】：备选构造器（从字符串解析开户）
    # 不需要已有实例，而是提供另一种创建对象的方式
    @classmethod
    def from_string(cls, account_str):
        owner, balance_str = account_str.split(",")
        balance = float(balance_str)
        return cls(owner, balance)  # 使用 cls 创建并返回新实例
    

# 1. 常规方式创建实例
account1 = BankAccount("张三", 10000)

# 2. 使用【类方法】创建实例（解析字符串自动开户）
account2 = BankAccount.from_string("李四,20000")

# 3. 使用【普通方法】查看个人利息（依赖各自的余额）
print(account1.calculate_interest())  # 输出: 200.0 (10000 * 0.02)
print(account2.calculate_interest())  # 输出: 400.0 (20000 * 0.02)

# 4. 使用【类方法】修改全局利率（影响所有账户）
BankAccount.set_interest_rate(0.05)

# 5. 再次计算，发现利息变多了（因为利率被类方法修改了）
print(account1.calculate_interest())  # 输出: 500.0 (10000 * 0.05)
```

总结：
- 普通方法：需要读取或修改属于某个具体对象的独有数据（即 self.xxx），或者行为依赖于对象当前的状态，使用普通方法。
- 类方法：一个功能跟具体的实例无关，而是跟整个“类”相关时（比如统计创建了多少个对象、修改全局配置），或者为这个类提供一种更优雅的创建对象的方式（如从 JSON 字符串解析生成对象）时，使用类方法。

---
### 8.16 静态方法（Sttaic Method）

1. 定义
- 静态方法属于类本身，不属于实例对象：
- 定义时用装饰器 @staticmethod 标记
- 方法不需要 `self（实例参数）`、也不需要 `cls（类参数）`
- 本质就是放在类里的普通函数，不访问类属性、实例属性
- 调用方式：类名.静态方法() / 实例.静态方法()

2. 语法格式
```python
class 类名:
    @staticmethod
    def 方法名(普通参数):
        # 逻辑，不能用 self / cls
        pass
```

3. 基础示例
```python
class MathTool:
    # 静态方法：无self、无cls
    @staticmethod
    def add(a, b):
        return a + b

# 1. 通过类直接调用（推荐）
print(MathTool.add(3, 5))  # 8

# 2. 通过实例调用（也支持，但不推荐）
obj = MathTool()
print(obj.add(10, 20))  # 30
```

4. 静态方法无法访问实例 / 类变量
```python
class Demo:
    cls_val = 100  # 类属性

    def __init__(self):
        self.ins_val = 200  # 实例属性

    @staticmethod
    def test():
        # 报错！静态方法看不到 self、cls
        # print(self.ins_val)
        # print(Demo.cls_val)  # 可以直接写类名访问，但不能自动获取

        print("我是静态方法，只能用传入参数")

Demo.test()
```

5. 静态、实例方法、类方法对比

|类型	|装饰器	|第一个参数	|可访问实例属性	|可访问类属性	|调用方式|
|---|---|---|---|---|---|
|实例方法	|无	|self	|✅ 直接 |✅通过 self.class	|实例.方法 ()|
|类方法	|@classmethod	|cls	|❌	|✅ |cls. 属性	|
|静态方法	|@staticmethod	|无强制参数	|❌	|只能写类名.属性	|类 / 实例均可调用|

直观对比：
```python
class Test:
    num = 10

    # 实例方法
    def inst_func(self):
        print("实例方法", self.num)

    # 类方法
    @classmethod
    def cls_func(cls):
        print("类方法", cls.num)

    # 静态方法
    @staticmethod
    def static_func():
        print("静态方法", Test.num)

t = Test()
t.inst_func()
Test.cls_func()
Test.static_func()
```

6. 静态方法使用场景示例：数据校验工具
```python
class User:
    def __init__(self, phone):
        if not User.check_phone(phone):
            raise ValueError("手机号格式错误")
        self.phone = phone

    # 静态工具：校验手机号
    @staticmethod
    def check_phone(phone):
        if len(phone) == 11 and phone.isdigit():
            return True
        return False

print(User.check_phone("13800138000"))  # True
u = User("13912345678")
```

7. 静态方法注意事项
- 静态方法里写 self：直接报错，不存在 self；
- 想用静态方法修改实例变量：做不到，改用实例方法；

## 相关知识

- [[Python Knowledge Map]]
- [[Python Basics 2]]：Python 容器类型。
- [[Python Basics 4]]：异常、调试与文件操作。
- [[MCP#注册 MCP 工具|FastMCP 工具装饰器]]
- [[Backend Basics 1#二、Flask路由|Flask 路由装饰器]]
- [[Test Development Notes#第二章 Python单元测试框架|Python 单元测试]]
