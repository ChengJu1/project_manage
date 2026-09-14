# Python 可迭代对象、迭代器、生成器面试+编程题库
分为三大类：**概念面试题（简答八股）、代码阅读题、实操编程题**，覆盖文档全部核心考点，适合笔试/面试自测。

## 一、概念面试题（简答，高频八股）
### 题1：请区分 可迭代对象(Iterable)、迭代器(Iterator)、生成器(Generator) 三者关系与区别
#### 参考答案
1. **可迭代对象 Iterable**
    只要实现 `__iter__` 方法，能被 `iter()` 转成迭代器、支持for循环的对象；
    常见：list/tuple/str/dict/set/range；
    特点：本身不是迭代器，不能直接next()。
2. **迭代器 Iterator**
    同时实现 `__iter__`（返回自身）+ `__next__`；
    支持 `next()` 单向惰性取值，遍历一次后耗尽；
    是可迭代对象的子集。
3. **生成器 Generator**
    迭代器的语法糖/子类，自动实现两个魔术方法；
    创建方式：带`yield`的函数、生成器表达式`(x for x in ...)`；
    额外支持 `send()`、`yield from`、暂停传值；
    惰性求值，内存占用极低。
    层级关系：`Iterable → Iterator → Generator`

### 题2：`__iter__` 和 `__next__` 各自作用？自定义类如何支持for循环？
#### 参考答案
- `__iter__(self)`：被`iter(obj)`调用，必须返回迭代器对象；
- `__next__(self)`：每次`next()`调用取一个值，无数据抛`StopIteration`；
自定义类支持for循环：类中实现`__iter__`返回自身，再实现`__next__`控制取值逻辑。

### 题3：迭代器有哪些核心特性？
#### 参考答案
1. 单向不可逆，只能向后取值；
2. 一次性消耗，遍历完毕后无数据；
3. 惰性计算，不一次性加载全部数据，节省内存；
4. 不支持索引、切片操作；
5. 只能通过`next()`取值。

### 题4：yield 和 return 的区别？生成器函数调用时会立刻执行函数内部代码吗？
#### 参考答案
1. return：直接终止函数，返回值；生成器中return会触发`StopIteration`；
2. yield：产出一个值，**暂停当前函数上下文**，下次next从暂停处继续执行；
3. 调用生成器函数只会创建生成器对象，**不会执行函数内部代码**，第一次next才开始运行。

### 题5：生成器表达式和列表推导式 `[]` / `()` 区别，适用场景？
#### 参考答案
1. 列表推导 `[x for x in iter]`：一次性生成完整列表，全部存入内存，数据量大易OOM；支持索引、切片、多次遍历；
2. 生成器表达式 `(x for x in iter)`：惰性求值，仅在next时计算单个值，内存极小；遍历一次耗尽，不支持索引；
场景：小数据、需要多次取值用列表；超大文件/无限序列/流式处理用生成器。

### 题6：`yield from` 作用是什么？
#### 参考答案
简化迭代嵌套，自动遍历传入的可迭代对象并逐个yield，等价于循环yield；
不用手动写`for i in sub: yield i`，同时支持子生成器接收send传值。

### 题7：判断 `list`、`iter(list)`、生成器分别是Iterable还是Iterator？
#### 参考答案
- list：仅Iterable，不是Iterator；
- iter(list)：既是Iterable也是Iterator；
- 生成器：既是Iterable也是Iterator。

### 题8：迭代器遍历一次就失效，为什么？
#### 参考答案
迭代器内部维护一个指针记录当前迭代位置，每next一次指针后移；当指针走到末尾，再次next抛出StopIteration，无重置逻辑，无法二次遍历。

## 二、代码阅读题（写出输出结果，分析原因）
### 阅读题1
```python
lst = [1, 2, 3]
it = iter(lst)
print(list(it))
print(list(it))
```
#### 输出 & 解析
```
[1, 2, 3]
[]
```
解析：迭代器一次性消耗，第一次list(it)取完所有元素，第二次无数据返回空列表。

### 阅读题2
```python
def gen():
    print("start")
    yield 1
    yield 2
g = gen()
print("创建生成器完毕")
next(g)
next(g)
next(g)
```
#### 输出 & 解析
```
创建生成器完毕
start
Traceback (most recent call last):
  File "xxx.py", line 7, in <module>
    next(g)
StopIteration
```
解析：调用gen()只创建对象，不执行内部代码；第一次next才打印start并返回1；两次next取完1、2，第三次next触发终止异常。

### 阅读题3
```python
g = (i*2 for i in range(3))
print(g[0])
```
#### 输出 & 解析
报错：`TypeError: generator object is not subscriptable`
解析：生成器不支持索引取值，只能用next/for循环遍历。

### 阅读题4
```python
def echo():
    res = yield "first"
    yield f"receive:{res}"
g = echo()
print(next(g))
print(g.send("python"))
```
#### 输出
```
first
receive:python
```
解析：send会把参数传给当前暂停的yield表达式作为返回值，同时执行一次next。

### 阅读题5
```python
from collections.abc import Iterable, Iterator
lst = [1,2]
print(isinstance(lst, Iterable), isinstance(lst, Iterator))
it = iter(lst)
print(isinstance(it, Iterable), isinstance(it, Iterator))
```
#### 输出
```
True False
True True
```

## 三、实操编程题（面试手写代码，附标准答案）
### 编程题1：自定义迭代器类，实现输出1~n的数字（不使用生成器yield）
要求：实现`__iter__`、`__next__`，支持for循环遍历
#### 参考答案
```python
class NumIterator:
    def __init__(self, max_num):
        self.max = max_num
        self.cur = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.cur += 1
        if self.cur > self.max:
            raise StopIteration
        return self.cur

# 测试
obj = NumIterator(5)
for i in obj:
    print(i)  # 1 2 3 4 5
```

### 编程题2：用生成器函数改写上面功能，输出1~n
#### 参考答案
```python
def num_gen(max_num):
    cur = 1
    while cur <= max_num:
        yield cur
        cur += 1

# 测试
g = num_gen(5)
print(list(g))  # [1,2,3,4,5]
```

### 编程题3：生成器实现无限斐波那契数列，取前10个数字
#### 参考答案
```python
def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 取前10项
f = fib_gen()
res = [next(f) for _ in range(10)]
print(res)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### 编程题4：写生成器逐行读取超大文本文件，避免一次性加载全部内容
#### 参考答案
```python
def read_big_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 使用示例
# for line in read_big_file("big_log.txt"):
#     print(line)
```

### 编程题5：使用yield from 合并两个生成器，输出所有数字
```python
def gen1():
    yield 1
    yield 2

def gen2():
    yield 3
    yield 4
```
#### 参考答案
```python
def merge_gen():
    yield from gen1()
    yield from gen2()

print(list(merge_gen()))  # [1, 2, 3, 4]
```

### 编程题6：实现一个生成器表达式，筛选1~100中所有偶数
#### 参考答案
```python
gen = (x for x in range(1, 101) if x % 2 == 0)
print(list(gen))
```

### 编程题7：手写for循环底层等价逻辑（手动iter+next+捕获StopIteration）
遍历列表`[10,20,30]`，不使用for
#### 参考答案
```python
lst = [10, 20, 30]
it = iter(lst)
while True:
    try:
        val = next(it)
        print(val)
    except StopIteration:
        break
```

## 四、拔高面试思考题（进阶）
### 思考题1：同一个生成器对象多次for循环会发生什么？为什么？
答案：第二次循环无输出。生成器迭代一次后指针走到末尾，持续抛出StopIteration，无法重置；如需多次遍历，每次循环要重新创建生成器。

### 思考题2：什么场景必须自定义迭代器类（不用yield生成器）？
答案：迭代逻辑复杂、需要维护多组独立状态、需要在迭代过程中做复杂资源管理、需要自定义迭代器额外方法时，适合手写`__iter__`+`__next__`类。

### 思考题3：生成器相比普通列表处理大数据的优势？
答案：惰性加载，内存只保存当前单个元素，几十GB文件也不会内存溢出；无需一次性开辟大内存空间；支持无限序列，列表无法实现无限数据。

## 相关知识

- [[Python Knowledge Map]]
- [[Python Basics 3#3. 函数|Python 函数]]
- [[Python Basics 4#4. 文件 I/O|文件读写]]
- [[Test Development Notes#第二章 Python单元测试框架|为迭代逻辑编写单元测试]]
- [[Knowledge Gaps]]
