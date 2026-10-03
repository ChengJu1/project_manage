
###  1. `is` 判断两个引用是否指向同一个对象，`==` 判断两个对象在逻辑上是否相等，通常通过 `__eq__()` 实现。两者都会返回布尔值。判断 `None` 应使用 `is None`；不要用 `is` 比较字符串或数字，因为对象驻留可能造成偶然结果。

### 2. “单例”指程序运行期间，这类对象只有一个实例，所有地方拿到的都是同一个对象。

```python
	a = []
	b = [] 
	a == b # return True 
	a is b # 返回 False
```

### 3. 为什么用`is None`而不是`== None`

`None` 是 `NoneType` 的单例。`x is None` 判断 `x` 是否指向唯一的 `None` 对象，而且身份判断不能被重载；`x == None` 会调用 `x.__eq__()`，其行为可能被自定义，所以不够可靠。

### 4.为什么可变对象不能直接作为函数默认参数？为什么使用 `None` 能解决？

默认参数表达式在函数定义时只求值一次。如果默认值是列表或字典，后续所有未传该参数的调用都会复用同一个对象，因此上次调用的修改会保留下来。使用 `None` 作为哨兵，可以在每次调用时创建新的可变对象。

```Python
def add_item(item, items=[]):
items.append(item)
return items

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]，不是预期的 [2]
```

但是使用None就可以避免这种问题:

```python
def add_item(item, items=None):
if items is None:
items = []

items.append(item)
return items
```

### 5. 可迭代对象、迭代器和生成器分别是什么？它们之间有什么关系？

可迭代对象：能通过 `iter(obj)` 获得迭代器，因此可以用于 `for`。
迭代器：实现 `__next__()`，保存当前迭代状态；`iter(iterator)` 通常返回自身。
生成器：一种特殊迭代器，由生成器函数或生成器表达式创建，通过 `yield` 按需产生值。

```python
numbers = [10, 20]       # 可迭代对象
iterator = iter(numbers)  # 迭代器

next(iterator)  # 10
next(iterator)  # 20
next(iterator)  # 抛出 StopIteration
```

生成器示例:

```python
def generate_numbers():
    yield 10
    yield 20

generator = generate_numbers()

iter(generator) is generator  # True
next(generator)               # 10
```

### 6. Python 的 GIL 限制了什么？它没有限制什么？I/O 密集和 CPU 密集任务应该如何选择线程、进程或协程？

GIL 全称是 Global Interpreter Lock，全局解释器锁。它的核心规则是：

```text
在同一个 Python 进程中，同一时刻通常只有一个线程能够执行 Python 字节码。
python字节码其实就是python代码编译后的结果
```

### 7. 进程、线程、协程

- **进程**是运行中的程序实例，拥有独立的内存空间和系统资源。不同进程不能直接共享普通变量，需要通过队列、管道、共享内存等方式通信。多个进程可以拥有各自的 Python 解释器和 GIL，因此适合利用多核 CPU 执行 CPU 密集任务。
- **线程**是进程中的执行单元，同一进程内的线程共享内存和资源。标准 CPython 中，由于 GIL，同一时刻通常只有一个线程执行 Python 字节码，因此多线程难以加速纯 Python 的 CPU 密集任务，但适合阻塞式 I/O。
- **协程**是由事件循环调度的轻量级任务，通常运行在单个线程中。协程在执行到 `await` 时暂停自身，让事件循环执行其他就绪任务，因此适合大量非阻塞 I/O。协程共享所在进程的内存，但不能通过协程直接实现 CPU 并行。

### 8. 阻塞与非阻塞式I/O

####  阻塞式 I/O

```
response = requests.get(url)
print(response.text)
```

`requests.get()` 没返回之前，当前线程不能继续执行下一行。

```
发起请求 → 当前线程停住等待 → 收到结果 → 继续执行
```

注意，是“当前线程被阻塞”，并不代表整个操作系统都停止了。其他进程或其他线程仍然可以运行。

#### 非阻塞异步 I/O

```
response = await client.get(url)
print(response.text)
```

当前协程仍然要等到请求完成，才能执行下一行；但是它在等待时会把线程的执行权交还给事件循环，让其他协程运行。

```
协程 A 发起请求 → await 暂停 A
                         ↓
事件循环执行协程 B、C
                         ↓
A 的请求完成 → 恢复协程 A
```

### 9. 调用一个 `async def` 函数后会立刻执行吗？coroutine、Task、event loop 和 `await` 分别承担什么角色？

调用 `async def` 函数通常不会立即执行函数体，而是返回协程对象。Task 将协程包装成可以被事件循环调度的任务。事件循环负责运行和恢复各个 Task；当协程执行到尚未完成的 `await` 时，当前协程暂停并交还控制权，事件循环可以运行其他就绪任务，等待结果完成后再恢复它。
#### 问题1：是否会立即执行

不会（普通函数如果调用的话就会立即执行）

```python
def normal():
    print("开始执行")
    return 42

result = normal()
```

但是`async def`函数不会立即执行，而是会创接一个`coroutine object`(协程对象)，而协程对象可以理解为“一项尚未开始或尚未完成的异步工作”。

#### 问题2: Event loop：事件任务调度器

Event loop 负责：
- 运行协程。
- 判断哪些任务现在可以继续运行。
- 记录哪些任务正在等待 I/O。
- 当 I/O 完成时恢复对应任务。

```python
import asyncio

asyncio.run(async_work())
```

`async def` 定义协程函数，调用后产生协程对象。协程通过 `await`、`create_task()` 或 `gather()`交给事件循环调度。事件循环不断运行当前就绪的任务；任务遇到需要等待的 `await` 时被暂停，事件循环转而推进其他任务，等待条件满足后再恢复它，直到相关任务全部完成。

事件循环的工作可以总结为：

1. 找出当前可以运行的 Task。
2. 运行某个 Task，直到它：
    - 遇到需要等待的 `await`；
    - 正常执行完成；
    - 抛出异常。
3. 如果它需要等待，就先运行其他就绪 Task。
4. 等待条件满足后，再回来恢复原来的 Task。
5. `asyncio.run(main())` 管理的主协程及相关任务完成后，关闭事件循环。
#### 问题3：TASK：被事件循环调动的协程

```python
async def main():
    coroutine = async_work()
    task = asyncio.create_task(coroutine)

    result = await task
    print(result)


asyncio.run(main())
```

`create_task()` 的意思是：将这个协程注册到当前事件循环，让它尽快开始运行。

#### 问题4：`await`

暂停当前协程，把控制权释放给事件循环

#### 问题5：实现两个任务的并行

如下仍然是串行：

```python
await work("A")  # 等 A 完成
await work("B")  # 然后才开始 B
```

想要实现并行要先`asyncio.create_task`或者`await asyncio.gather`

```python
task1 = asyncio.create_task(work("A"))
task2 = asyncio.create_task(work("B"))

await task1
await task2
```

### 10. `request.form`获取到的都是字符串

### 11. `datetime.strptime(日期字符串, "%Y-%m-%d").date()`

striptime的意思就是按照后面规定的方式解析前面的字符串,其中比较常见的日期格式有：

```python
"%Y/%m/%d"           # 2026/09/17
"%d-%m-%Y"           # 17-09-2026
"%m/%d/%Y"           # 09/17/2026
"%Y年%m月%d日"        # 2026年09月17日
"%Y-%m-%d %H:%M"     # 2026-09-17 14:30
"%Y-%m-%d %H:%M:%S"  # 2026-09-17 14:30:25
```

常用符号有：

```python
%Y  四位年份
%y  两位年份
%m  月份
%d  日期
%H  24小时制
%I  12小时制
%M  分钟
%S  秒
%p  AM/PM
```

### 12. PRG(Post/Redirect/Get)
用户在前端提交表单时，采用这种方式防止用户重复提交，提交后弹窗，重定向到首页，然后重新发送Get请求渲染网页。

### 13. SQLAlchemy 查询
`Project.query.filter(...)` 和 `Project.query.filter(...).all()` 返回的东西有什么区别？为什么通常要等筛选条件全部加完才调用 `.all()`？
第一个是尚可继续组合条件的查询对象；第二个执行查询并返回由模型对象组成的 Python 列表。
#### 14. 和Redis有关的三级缓存
本地缓存 → Redis 缓存 → 数据库
第一层：本地缓存
本地缓存存在python进程的内存中
- 速度最快，不需要网络请求
- 只对当前python进程有效
- 程序重启之后数据就会消失
- 多个服务器之间不能自动共享
第二层：Redis缓存
Redis是独立运行的内存数据库，python通过网络访问
- 比本地缓存稍慢，但仍然很快
- 多个 Python 服务可以共享
- 可以设置过期时间
- 支持字符串、哈希、列表、集合等结构
- 可以做缓存、分布式锁、排行榜和限流
- 详情见 [[Redis]]
第三层：数据库(MySQL, PostgreSQL, SQLite)
- 访问速度通常比缓存慢
- 数据持久保存
- 数据库一般是最终可信的数据来源
- 支持复杂查询、事务和数据约束

### 15 .Python 中的Path

*path.resolve()*

把路径转换成规范的绝对路径
假设当前运行python的位置是:
`/Users/xinyuan/project`

```python
from pathlib import Path

path = Path("hello.txt")

print(path)
print(path.resolve())
```
输出:
```text
hello.txt
/Users/xinyuan/project/hello.txt
```

*path.read_text()*

对path这个Path的实例，读其中的所有内容，返回字符串

```Python
from pathlib import Path

path = Path("hello.txt")

content = path.read_text(encoding="utf-8")

print(content)
```

*glob()*

按照规则，在文件夹中查找文件或者文件夹（返回类型是一个生成器）

```Python
Path("文件夹").glob("匹配规则")
```