# 测试开发学习讲义

## 第一章 软件测试基础理论

### 1.1 分层测试方案

分层测试是一套软件测试策略，把测试划分为多个层级，每个层级有独立的测试目标与范围，多用于大型、复杂软件项目，实现测试全面高效，尽早发现并修复缺陷。

| 测试层级       | 测试对象                 | 执行人员      | 核心目标                                       |
| -------------- | ------------------------ | ------------- | ---------------------------------------------- |
| 单元测试层     | 代码最小单元：函数、方法 | 开发人员      | 验证单个代码单元独立运行符合预期               |
| 组件测试层     | 多个单元组成的组件       | 测试人员      | 验证组件内部单元交互，发现组件内集成、功能缺陷 |
| 集成测试层     | 多个组件、模块组合       | 测试人员      | 校验组件之间协同工作，可增量式逐步集成测试     |
| 系统测试层     | 完整的整个软件系统       | 测试人员      | 覆盖全部功能、非功能，验证系统符合需求文档     |
| 用户验收测试层 | 交付后的完整系统         | 用户/客户代表 | 验证系统满足真实业务使用需求                   |

### 1.2 测试分类

#### 黑盒测试（功能测试）

不关心程序内部代码结构、实现逻辑，只依据需求文档，校验输入输出、页面交互、完整业务流程。

>适用场景：功能测试、接口测试、UI自动化测试

**常用用例设计方法**

1. **等价类划分**：把输入域划分为有效等价、无效等价，每一类选取少量代表性数据编写用例，减少重复测试。

>示例：用户名限制3‑10字符；有效等价取4位字符；无效等价取2位、11位字符。

2. **边界值分析法**：选取输入输出的临界边界作为测试用例，边界位置是缺陷高发点。

>示例：用户名3‑10位，重点测试2、3、10、11这几组数据。

3. **错误推测法**：依靠经验、直觉预判程序容易出错的场景，针对性设计测试用例。
4. **因果图法**：分析输入条件之间组合、制约关系，生成判定表，完成多条件组合用例设计。
5. **判定表**：罗列全部输入条件组合，以及每一组条件对应的输出结果，适合多分支复杂业务。
6. **正交试验设计**：从海量输入组合中挑选具备代表性的样本，减少用例数量。
7. **场景法**：梳理业务正常流程、异常流程，覆盖完整业务链路。

#### 白盒测试

深入程序代码内部，检查代码逻辑、分支、条件、执行路径是否正确。

>适用场景：单元测试、代码覆盖率校验

常见覆盖标准（覆盖程度由低到高）

1. **语句覆盖**：程序每一行代码至少执行一次，最低覆盖标准。
2. **判定覆盖**：所有if/else判断的真、假分支都被执行。
3. **条件覆盖**：判定语句中每一个子条件，都取到真、假两种结果。
4. **判定‑条件覆盖**：同时满足判定覆盖+条件覆盖。
5. **路径覆盖**：程序中全部独立执行路径都覆盖，较高的覆盖标准。

>注意：代码覆盖率达到100%不等于程序没有bug，覆盖率仅代表代码被执行，无法覆盖业务场景、真实业务逻辑。

### 1.3 性能相关基础概念

1. **压力测试**：模拟高负载，识别系统薄弱点，观察系统在极限负载下的运行表现。
2. **性能平坦区**：系统性能表现最优的区间，可以作为性能基线；持续加压，系统各项指标几乎没有变化。
3. **系统性能拐点**：负载超过阈值后，系统性能开始急剧下降的临界点。

**性能测试常用方法**：SEI负载测试计划过程、RBI方法、性能下降曲线分析法、Loadrunner与Segue提供的性能测试方法、PTGM模型。

#### 性能测试四大类指标

1. **业务指标**：并发用户数、TPS（每秒处理事务数）、成功率、响应时间。
2. **资源指标**：CPU利用率、内存利用率、磁盘I/O、内核参数（信号量、打开文件数）。
3. **应用指标**：空闲线程数量、数据库连接数、GC/FullGC次数、函数执行耗时。
4. **前端指标**：页面加载耗时、网络耗时（DNS解析、连接、数据传输时间等）。

>think time（思考时间）：脚本中两个请求之间设置的间隔时间，模拟真实用户操作停顿，让压测行为更贴合真实用户行为。

### 1.4 自动化测试

#### 为什么做自动化测试

1. 手工回归测试执行效率低下；
2. 手动测试存在人为偶然性，结果具备不确定性；
3. 手工回归很难做到充分的覆盖；
4. 仅靠人工评估，难以保障交付产品质量；
5. 系统业务越复杂，回归工作量越大；
6. 快速迭代模式下，构建失败容易引发连锁问题，带来大量重复工作。

#### 数据驱动测试

把测试数据和测试脚本进行分离，同一套脚本读取多组不同输入数据执行测试。

- 优点：脚本和数据模块化；一套脚本复用，消除脚本内部的数据冗余。
- 缺点：大批量数据场景下，数据校验耗时；数据维护成本高，需要额外编码。

#### 测试开发工程师核心工作

测试开发核心目标：提升软件质量，提升整体测试、开发效率；通过自动化脚本、自研工具赋能测试流程，和开发团队协同保障各环境下软件符合预期。

1. **自动化测试**：编写自动化脚本、搭建自动化框架，实现测试数据自动生成、用例自动执行，降低手工成本，提升测试准确度。
2. **测试工具与框架**：使用成熟开源工具框架，同时可以根据业务需求开发定制内部测试工具，执行用例、生成报告、分析结果。
3. **持续集成与持续测试**：配合开发团队搭建CI流程，提供测试环境，实现代码变更自动触发测试，快速反馈问题。
4. **性能与负载测试**：设计性能测试方案，开发压测脚本，采集分析性能指标，输出优化参考依据。
5. **缺陷管理**：配合缺陷跟踪工具，记录、跟进、闭环软件缺陷。

## 第二章 Python单元测试框架

### 2.1 unittest（Python内置单元测试框架）

unittest是Python标准库自带的单元测试框架，不需要额外pip安装。支持测试自动化、共享初始化与清理逻辑、测试用例集合管理、结果输出。

### 核心概念

1. **测试用例 test case**
   测试的最小执行单元，继承`unittest.TestCase`；测试方法名**必须以`test`小写开头**，框架才会自动识别执行；一个用例可以包含测试固件(前置后置) + 业务测试逻辑。

2. **测试固件 test fixture**
   测试执行前后的准备与清理逻辑。例如：创建数据库连接、打开浏览器；测试结束关闭连接、关闭浏览器。分为方法级、类级、模块级。

3. **测试套件 test suite**
   多个测试用例/测试类的集合。可以手动挑选部分用例组装，实现自定义批量执行。

4. **测试执行器 test runner**
   负责加载测试套件、执行测试用例，收集并打印测试结果；`unittest.main()`就是内置的简单测试执行器。

### 夹具执行级别

| 级别   | 方法                                 | 执行时机                                            |
| ------ | ------------------------------------ | --------------------------------------------------- |
| 方法级 | `setUp()` / `tearDown()`             | **每一条test_测试方法执行前后都会运行**             |
| 类级   | `setUpClass()` / `tearDownClass()`   | **整个测试类只执行1次**，需要加`@classmethod`装饰器 |
| 模块级 | `setUpModule()` / `tearDownModule()` | **整个py脚本文件只执行1次**，写在类外面，普通函数   |

>⚠️注意：`setUpClass`、`tearDownClass`必须加上`@classmethod`装饰器，否则运行报错。

### 完整可直接运行示例代码

 ` unittest-1.py`

```python
import unittest

# 模块级固件：整个py文件运行前后执行一次，写在类外面
def setUpModule():
    print("\n>>>>>> 模块前置：整个脚本开始执行")

def tearDownModule():
    print("\n>>>>>> 模块后置：整个脚本全部执行完毕")


class TestStringMethods(unittest.TestCase):
    # 类级固件，必须加 @classmethod
    @classmethod
    def setUpClass(cls):
        print("\n------类前置：本测试类只执行这一次")

    @classmethod
    def tearDownClass(cls):
        print("\n------类后置：本测试类全部用例执行结束")

    # 方法级固件：每条test_方法执行前运行
    def setUp(self):
        print("\n++++++方法前置：单个用例开始")

    def test_upper(self):
        """测试字符串大写转换"""
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        """测试判断字符串是否全大写"""
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        """测试字符串分割，同时捕获异常"""
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # 断言抛出指定异常
        with self.assertRaises(TypeError):
            s.split(2)

    # 方法级固件：每条test_方法执行完毕运行
    def tearDown(self):
        print("++++++方法后置：单个用例执行结束")


if __name__ == '__main__':
    unittest.main(verbosity=2)  # verbosity=2输出详细执行信息
```

运行说明：`verbosity=2`打印详细用例名称；不加参数为简洁输出。

### 常用断言方法（TestCase内置）

| 断言方法                        | 作用                 |
| ------------------------------- | -------------------- |
| `self.assertEqual(a,b)`         | 判断a等于b           |
| `self.assertNotEqual(a,b)`      | 判断a不等于b         |
| `self.assertTrue(x)`            | x结果为True          |
| `self.assertFalse(x)`           | x结果为False         |
| `self.assertIn(item,container)` | item是否包含在容器内 |
| `self.assertRaises(异常类型)`   | 断言代码抛出指定异常 |

### 跳过测试 & 预期失败

- `@unittest.skip("原因")`：无条件跳过用例
- `@unittest.skipIf(条件,"原因")`：条件成立时跳过
- `@unittest.skipUnless(条件,"原因")`：条件不成立时跳过
- `@unittest.expectedFailure`：标记用例预期会失败；实际失败算预期，实际成功反而标记失败

```python
import sys
import unittest

class TestSkipCase(unittest.TestCase):
    @unittest.skip("直接跳过该用例，用于功能尚未开发完成")
    def test_nothing(self):
        self.fail("这里不会执行到")

    @unittest.skipIf(sys.platform == "win32", "Windows环境跳过执行")
    def test_linux_only(self):
        self.assertEqual(1,1)

    @unittest.skipUnless(sys.platform == "win32", "仅Windows运行，其他系统跳过")
    def test_win_only(self):
        self.assertEqual(2,2)

    @unittest.expectedFailure
    def test_expected_fail(self):
        # 预期这个用例是失败的
        self.assertEqual(1, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

### 子测试 subTest

作用：在同一个测试方法内部循环多组测试数据，**某一组数据失败不会阻断后续循环继续执行**，会分别标记哪一组参数出错。
注意：subTest只是子分支，**不会生成多条独立的测试用例记录**，整个函数仍然算作1条用例。

可运行代码示例：

```python
import unittest

class TestSubTestDemo(unittest.TestCase):
    def test_even(self):
        """测试0‑5数字是否全部为偶数"""
        for i in range(0, 6):
            # i为子测试标识，失败日志会打印i的值
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

执行结果：i=1、3、5会报错，但是不会终止循环，0,2,4仍然会跑完。

### 测试套件 TestSuite 手动组装用例

可以手动选择要执行哪些测试类、哪些用例，自定义执行顺序。

```python
import unittest

# 模块级固件：整个py文件运行前后执行一次，写在类外面
def setUpModule():
    print("\n>>>>>> 模块前置：整个脚本开始执行")

def tearDownModule():
    print("\n>>>>>> 模块后置：整个脚本全部执行完毕")


class TestStringMethods(unittest.TestCase):
    # 类级固件，必须加 @classmethod
    @classmethod
    def setUpClass(cls):
        print("\n------类前置：本测试类只执行这一次")

    @classmethod
    def tearDownClass(cls):
        print("\n------类后置：本测试类全部用例执行结束")

    # 方法级固件：每条test_方法执行前运行
    def setUp(self):
        print("\n++++++方法前置：单个用例开始")

    def test_upper(self):
        """测试字符串大写转换"""
        print("执行test_upper")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        """测试判断字符串是否全大写"""
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        """测试字符串分割，同时捕获异常"""
        print("执行test_split")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # 断言抛出指定异常
        with self.assertRaises(TypeError):
            s.split(2)

    # 方法级固件：每条test_方法执行完毕运行
    def tearDown(self):
        print("++++++方法后置：单个用例执行结束")

def suite():
    suite = unittest.TestSuite()
    # 添加单个测试方法
    suite.addTest(TestStringMethods("test_upper"))
    suite.addTest(TestStringMethods("test_split"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
```

### unittest实现简单数据驱动

unittest没有像pytest的parametrize装饰器，一般两种方案：

1. 在方法内部循环 + `self.subTest()`
2. 动态生成测试方法

示例：subTest实现登录多组数据测试

```python
class TestLoginDDT(unittest.TestCase):
    def test_login_param(self):
        # 多组测试数据：用户名，密码，预期结果
        case_data = [
            {"user":"admin","pwd":"123456","expect":True},
            {"user":"","pwd":"123456","expect":False},
            {"user":"admin","pwd":"","expect":False},
        ]
        for case in case_data:
            with self.subTest(case=case):
                # 模拟登录逻辑
                result = bool(case["user"] and case["pwd"])
                self.assertEqual(result, case["expect"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

### 面试简答题

Q：unittest和pytest fixture区别？
A：unittest只有setUp/tearDown，只有方法、类、模块三级；pytest fixture更加灵活，支持function/class/module/session，支持传参、依赖注入，通过yield同时做前置后置。unittest实现多组数据依赖subTest，pytest直接用parametrize生成独立用例。

Q：subTest有什么作用？
A：在一个测试方法循环多组输入，其中某一组数据断言失败不会中断整个循环，日志会打印出错的参数；缺点是所有子测试仍然算作一条测试用例。

Q：setUp和setUpClass区别？
A：setUp每条测试方法都会执行；setUpClass整个测试类只执行一次，必须加`@classmethod`，适合类内多个用例共用的初始化操作，减少重复执行。

### 2.2 pytest（主流第三方单元测试框架）

pytest 是Python非常流行的第三方单元测试框架，语法简洁，不需要类的约束，普通函数即可编写用例；拥有强大插件生态，支持前置后置固件、参数化、失败重跑、自定义标记等，既可以写单元测试，也可用于接口、自动化回归测试。

注意：pytest不是Python内置库，需要手动安装。

### 安装

```bash
pip install pytest
```

### 用例查找规则（自动发现）

pytest会递归遍历当前以及子目录，自动识别测试文件、测试函数：

1. **测试文件**：文件名以 `test_` 开头 或者 以 `_test` 结尾；
2. **测试函数**：文件内函数名以 `test_` 开头；
3. **测试类**：类名以`Test`开头（**不能带`__init__`构造方法**）；类里面测试方法以`test_`开头。

说明：不符合命名规则的函数/文件不会被自动收集执行。

### 基础示例

新建文件 `test_demo.py`，完整可运行。

```python
def test_add_case():
    """普通测试函数，不需要继承任何类"""
    assert 10 + 20 == 30
    assert -1 + 1 == 0
```

执行命令：

```bash
pytest test_demo.py
```

>pytest 使用原生`assert`做断言，会自动解析表达式，失败输出详细对比信息，不需要像unittest一样记大量`self.assertEqual`断言方法。

### 捕获异常 pytest.raises

用于断言某段代码会抛出指定异常；使用`with`上下文管理器捕获异常信息。
新建 `test_exception.py`

```python
import pytest

def test_index_err():
    lst = []
    # 断言下面代码会抛出IndexError
    with pytest.raises(IndexError) as e:
        print(lst[0])

    # e.value 获取异常实例，可以进一步断言异常信息
    assert "list index out of range" in str(e.value)
```

执行：`pytest test_exception.py -v`

### 用例执行控制

#### 1. 指定单个函数执行 `::`

语法：`pytest 文件名::函数名`

```bash
pytest test_demo.py::test_add_case
```

#### 2. 关键词过滤 `-k`

通过用例函数名的字符串模糊匹配，匹配到的用例才执行。

```bash
# 执行名字包含add的用例
pytest test_demo.py -k "add" -v
```

#### 3. 自定义标记 mark

使用`@pytest.mark.标记名`给用例打标签，可以按标签批量执行用例。

>注意：自定义标记，建议在pytest.ini注册标记，消除运行警告。

新建 `test_mark.py`

```python
import pytest

@pytest.mark.finished
def test_func1():
    assert 1 == 1

@pytest.mark.unfinished
def test_func2():
    assert 1 != 1
```

执行指定标记用例：

```bash
# 只运行标记为finished的用例
pytest test_mark.py -m "finished" -v
# 取反，运行不是unfinished的用例
pytest test_mark.py -m "not unfinished" -v
```

>补充：项目根目录新建`pytest.ini`文件，注册自定义标记，消除告警

```ini
[pytest]
markers =
    finished: 已经完成的用例
    unfinished: 未开发完成用例
```

### 跳过测试 & xfail（预期失败）

- `@pytest.mark.skip(reason="原因")`：无条件跳过该用例，不执行；
- `@pytest.mark.skipif(条件, reason="")`：满足条件才跳过；
- `@pytest.mark.xfail(reason="原因")`：**预期该用例执行会失败**；
  - 如果运行确实失败：结果标记xfail，不算失败；
  - 如果运行反而成功：标记xpass，代表预期失败但是实际通过。

`test_skip_xfail.py`完整代码：

```python
import pytest
import sys

@pytest.mark.skip(reason="接口已经过期，暂时跳过")
def test_skip_demo():
    assert 1 == 1

@pytest.mark.skipif(sys.platform == "win32", reason="windows平台跳过")
def test_skipif_demo():
    assert 2 == 2

@pytest.mark.xfail(reason="版本1.0暂不支持该逻辑，已知会失败")
def test_xfail_demo():
    assert False
```

执行命令：

```bash
pytest test_skip_xfail.py -v
```

### 参数化测试 parametrize（数据驱动）

`@pytest.mark.parametrize`装饰器，传入多组测试数据，**每组数据会生成一条独立的测试用例**。对比unittest的`subTest`，这是真正多条用例，分别统计执行结果。

`test_param.py`完整示例

```python
import pytest

# a,b输入参数；expect为预期结果
@pytest.mark.parametrize("a,b,expect", [
    (1, 2, 3),
    (0, -1, -1),
    (999, 1, 1000)
])
def test_add(a, b, expect):
    assert a + b == expect


# 使用pytest.param给每组用例设置id，报告中显示自定义名称
@pytest.mark.parametrize("user,pwd,expect_ok", [
    pytest.param("admin", "123456", True, id="正常账号密码"),
    pytest.param("", "123456", False, id="用户名为空"),
    pytest.param("admin", "", False, id="密码为空"),
])
def test_login(user, pwd, expect_ok):
    # 模拟登录逻辑
    res = bool(user and pwd)
    assert res == expect_ok
```

运行：`pytest test_param.py -v`，可以看到一共生成6条用例。

### Fixture固件（前置/后置）

fixture是pytest核心特性，用来实现测试的初始化（前置）、清理（后置），替代unittest的`setUp/tearDown`。

- 通过`@pytest.fixture`声明固件函数；
- `yield` 之前代码：**预处理（测试执行之前运行）**
- `yield` 返回数据，可以注入给测试函数；
- `yield` 之后代码：**后处理（测试执行结束后运行，无论用例成功失败都会执行清理）**

#### fixture 4种scope作用域

| scope      | 说明           | 生命周期                                   |
| ---------- | -------------- | ------------------------------------------ |
| `function` | 函数级（默认） | **每一条测试函数执行前后运行一次**         |
| `class`    | 类级           | **每个测试类执行前后运行一次**             |
| `module`   | 模块级         | **整个py文件执行前后运行一次**             |
| `session`  | 会话级         | **整个pytest执行会话，全部用例只运行一次** |

>session级别适合整个测试套件共用资源：比如启动一次数据库连接，所有py文件复用。

完整示例 `test_fixture.py`

```python
import pytest

# module模块级固件：整个py文件只执行一次
@pytest.fixture(scope="module")
def db_conn():
    print("\n===== 模块固件：打开数据库连接 =====")
    yield  # 此处可以return数据，测试函数接收参数；也可以yield返回
    print("\n===== 模块固件：关闭数据库连接 =====")

# function函数级固件，默认scope="function"
@pytest.fixture
def init_test_data():
    print("\n-----函数固件：初始化测试数据-----")
    yield {"username": "test_user"}
    print("\n-----函数固件：清理测试数据-----")

# 测试函数，参数名字和fixture函数名保持一致，自动注入
def test_query(db_conn, init_test_data):
    print(f"执行测试用例，获取数据：{init_test_data}")
    assert init_test_data["username"] == "test_user"

def test_query2(db_conn):
    print("第二条测试，复用模块级db_conn")
    assert True
```

>执行必须加 `-s`，才可以看到print打印输出

```bash
pytest test_fixture.py -v -s
```

#### fixture使用小提示

1. fixture可以互相调用，固件之间可以依赖；
2. yield后面的清理代码，**无论用例失败、异常，都会执行，保证资源释放**；
3. session级别的fixture，建议放在`conftest.py`，整个项目所有测试文件都可以直接使用，不需要import导入。

### conftest.py 说明（拓展重点）

`conftest.py`是pytest特殊配置文件：

1. 在该文件写的fixture，同目录以及子目录下所有测试脚本**不需要import，直接拿来当参数使用**；
2. 用来存放公共固件、公共钩子，做项目级自动化框架必备。

### 常用命令汇总

```bash
pytest test.py -v               # -v 详细输出用例信息
pytest -k keyword -v            # 按关键词筛选执行用例
pytest --reruns 2               # 用例失败自动重跑最多2次
pytest -s                       # 打印脚本内部print输出内容
pytest test.py::test_func -v    # 指定执行某一个测试函数
pytest -m finished -v           # 按标记执行用例
pytest --reruns 2 -x             # 失败重跑，一旦出现用例失败立刻停止全部测试
```

### unittest vs pytest 对比（面试简答）

1. 用例编写：unittest必须继承TestCase类；pytest普通函数就可以写用例，断言直接用`assert`。
2. 前置后置：unittest只有方法/类/模块三级；pytest fixture支持function/class/module/session四级，支持依赖注入、yield清理。
3. 数据驱动：unittest靠subTest（仍然算1条用例）；pytest `parametrize`直接生成多条独立用例。
4. 生态：pytest插件丰富（失败重跑、allure报告等）。

### 高频面试简答题

>Q：pytest fixture的scope分别有什么？
>A：function函数级（每条用例）、class类级（每个测试类）、module模块级（py文件）、session会话级（整个测试执行）。

>Q：`yield` 在fixture里面作用？
>A：yield之前做测试前置初始化；yield返回数据给测试函数；yield之后代码做后置清理；无论用例成功失败，后置代码都会执行。

>Q：pytest.mark.parametrize 和 unittest subTest区别？
>A：parametrize每组参数生成**独立测试用例**，分开统计成功失败；subTest只是循环内的子分支，全部算一条测试用例，子用例失败不会终止循环，但统计结果还是一条。

>Q：conftest.py作用？
>A：pytest专用配置文件，存放公共fixture，同目录下测试文件不需要导入就可以直接调用固件，实现固件复用。

### 2.3 coverage 代码覆盖率统计

`coverage` 是Python代码覆盖率统计工具，**既可以配合 `pytest`，也可以配合 `unittest`**，用来统计单元测试覆盖到的代码行数、分支，量化白盒测试的充分程度。

注意：**覆盖率100% ≠ 代码没有bug**，只能代表代码被执行到，不能保证业务逻辑正确。

安装：

```bash
pip install coverage
```

### 方式一：配合 pytest（最常用）

#### 完整示例文件

新建文件 `calc.py`（业务被测代码）

```python
def add(a, b):
    if a > 0 and b > 0:
        return a + b
    elif a < 0 or b < 0:
        return a - b
    else:
        return 0
```

新建测试文件 `test_calc.py`（pytest用例）

```python
from calc import add

def test_add_positive():
    assert add(1,2) == 3

def test_add_negative():
    assert add(-1,2) == -3
```

#### 执行coverage命令

```bash
# 收集覆盖率，使用pytest执行用例
coverage run -m pytest test_calc.py -v

# 控制台查看覆盖率报告
coverage report -m

# 生成html可视化报告，输出到htmlcov文件夹
coverage html
```

执行完 `coverage html`，打开 `htmlcov/index.html` 即可浏览器看彩色源码覆盖率，红色代表未执行代码。

**报告字段说明**

| 字段   | 含义                                    |
| ------ | --------------------------------------- |
| Stmts  | 可执行代码总行数                        |
| Miss   | 没有被测试执行到的行数                  |
| Branch | 分支覆盖率（if/else等逻辑分支是否走到） |
| Cover  | 整体覆盖率百分比                        |

---

### 方式二：配合 unittest

同样使用上面业务代码 `calc.py`，新建unittest测试文件 `test_calc_unittest.py`

```python
import unittest
from calc import add

class TestCalc(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(1,2), 3)

    def test_add_negative(self):
        self.assertEqual(add(-1,2), -3)

if __name__ == '__main__':
    unittest.main()
```

coverage执行命令（运行unittest脚本）

```bash
# 执行unittest脚本并采集覆盖率
coverage run test_calc_unittest.py

# 控制台输出报告
coverage report -m

# 生成网页报告
coverage html
```

重点区别：

1. `coverage run -m pytest 脚本名`：`‑m` 调用模块模式，给pytest使用；
2. `coverage run 脚本名.py`：直接运行py文件，给unittest脚本使用。

### 常用可选参数

```bash
# 只统计指定业务模块，排除测试脚本本身
coverage run --source=calc -m pytest test_calc.py -v
coverage report -m
```

`--source=模块名`：只统计被测业务代码，**不会把测试用例代码算进覆盖率**，日常工作强烈建议加上。

### 面试简答

Q：coverage可以结合哪些测试框架？
A：可以结合pytest、unittest。`coverage run -m pytest`用于pytest；`coverage run xxx.py`直接运行unittest脚本。`--source`参数指定被测源码，过滤掉测试脚本。

Q：Branch分支覆盖率是什么？
A：统计if‑elif‑else各个逻辑分支是否被执行，不仅仅统计代码行。开启分支统计：`coverage run --branch -m pytest test_calc.py`。

## 第三章 接口测试

### 3.1 requests库（Python接口请求库）

安装

```bash
pip install requests
```

GET请求示例

```python
import requests
url = "https://httpbin.org/get"
params = {"username": "test", "age": 18}
headers = {"User-Agent": "test-dev"}
resp = requests.get(url, params=params, headers=headers)
assert resp.status_code == 200
print(resp.json())
```

POST‑JSON请求示例

```python
import requests
url = "https://httpbin.org/post"
json_data = {"account": "admin", "password": "123456"}
resp = requests.post(url, json=json_data)
res = resp.json()
assert "args" in res
```

会话保持，自动维护cookie，复用登录态

```python
import requests
session = requests.Session()
session.post(url, json={"user":"test"})
session.get("https://httpbin.org/user")
```

### 3.2 Swagger接口文档工具

后端框架自动生成在线接口文档，可直接在页面调试接口，统一前后端、测试对接标准。

- 功能：在线调试接口，展示参数、响应、字段类型、枚举、必填项，支持配置全局鉴权token。
- 访问路径：服务地址+/swagger.html 或者 /docs
- 测试使用场景：梳理入参、提取自动化字段、复现线上接口问题。

## 第四章 Mock测试

### 4.1 Mock核心作用

单元测试、接口测试中隔离外部依赖（第三方支付、下游接口等），不调用真实服务，返回预设数据；用来模拟超时、报错、空返回等异常场景。

### 4.2 unittest.mock 内置mock库示例

```python
import unittest
from unittest import mock
import requests

# 业务待测试函数：调用第三方支付接口
def pay_order():
    """发起支付，返回接口的code码"""
    resp = requests.get("https://third-pay.com/pay")
    return resp.json()["code"]


class TestPayMock(unittest.TestCase):
    def test_pay_mock_success(self):
        """mock模拟第三方支付成功返回，不会真实发起http请求"""
        with mock.patch("requests.get") as mock_get:
            mock_resp = mock.Mock()
            mock_resp.json.return_value = {"code": 200, "msg": "success"}
            mock_resp.status_code = 200
            mock_get.return_value = mock_resp

            res_code = pay_order()
            self.assertEqual(res_code, 200)
            mock_get.assert_called_once_with("https://third-pay.com/pay")

    def test_pay_mock_error(self):
        """mock模拟第三方接口返回业务失败的场景"""
        with mock.patch("requests.get") as mock_get:
            mock_resp = mock.Mock()
            mock_resp.json.return_value = {"code": 500, "msg": "支付服务异常"}
            mock_resp.status_code = 500
            mock_get.return_value = mock_resp

            res_code = pay_order()
            self.assertEqual(res_code, 500)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
```

### 4.3 独立Mock服务

例如moco、mock‑server，搭建本地服务，定义接口返回，适合自动化流程整体依赖隔离。

## 第五章 UI自动化

### 5.1 Web自动化

#### Selenium

环境准备

```bash
pip install selenium
# 需要下载对应版本ChromeDriver浏览器驱动
```

基础代码示例

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://httpbin.org/html")
driver.find_element(By.TAG_NAME, "h1")
driver.quit()
```

常用元素定位：ID、CSS选择器、XPath。

**显式等待（推荐，替代固定sleep）**，等待条件满足就执行，节省执行时间

```python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login")))
login_btn.click()
```

补充：隐式等待为全局设置，查找所有元素都等待固定时长；显式等待针对单个元素，性能更好。

#### Playwright（微软新一代Web自动化工具）

特性：跨浏览器（Chromium、WebKit、Firefox）；跨平台Windows/Linux/macOS；支持Python/Java/JS/.NET多语言。

安装

```bash
pip install pytest-playwright
playwright install
```

**Codegen录制脚本**：录制浏览器操作，自动生成自动化代码

```bash
# 基础录制
playwright codegen
# 指定网页
playwright codegen www.baidu.com
# 模拟手机设备
playwright codegen --device="iPhone 11"
# 保存登录状态
playwright codegen --save-storage login.json
# 读取登录状态
playwright codegen --load-storage login.json www.github.com
# 输出脚本文件
playwright codegen -o run_baidu.py
```

**Trace Viewer追踪调试**：执行过程保存截图、DOM快照、日志，用于排查用例失败

```python
from playwright.sync_api import sync_playwright, expect

def test_demo():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    # 开启trace
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto("https://ceshiren.com/")
    page.locator("#search-button").click()
    page.locator("#search-term").fill("Appium")
    page.keyboard.down("Enter")
    expect(page.locator(".topic-title")).to_contain_text("Appium")
    page.screenshot(path="demo.png")
    # 结束trace，保存zip包
    context.tracing.stop(path="trace.zip")
    browser.close()
    pw.stop()
```

查看trace文件：`playwright show-trace trace.zip`

常用API：

- `page.goto(url)`：跳转网页
- `page.locator("selector").click()`：点击元素
- `page.locator().fill("文本")`：输入
- `expect(locator).to_contain_text("xxx")`：断言文本
- `page.screenshot(path="xxx.png")`：页面截图

### 5.2 Android APP自动化

#### uiautomator2

环境依赖：Python + adb工具 + 安卓设备/模拟器

```bash
pip install --pre uiautomator2
pip install Pillow
python -m uiautomator2 init
```

示例代码

```python
import uiautomator2 as u2
d = u2.connect("127.0.0.1:5555")
d.app_start("com.example.demo")
d(resourceId="username").set_text("test")
d(text="登录").click()
print(d.toast.get_message())
d.app_stop("com.example.demo")
```

定位优先级：resourceId > text > xpath。

#### Monkey测试（安卓压力随机测试）

Monkey是adb自带工具，向APP发送大量随机事件（点击、滑动、按键），检测APP崩溃、ANR。

常用命令示例

```bash
adb shell monkey -s 888 -v -v -v --throttle 500 -p com.xxx.app --ignore-crashes --ignore-timeouts 1000 > monkey_log.txt
```

关键参数

| 参数                    | 说明                |
| ----------------------- | ------------------- |
| `-p`                    | 指定被测APP包名     |
| `-s`                    | 随机种子，复现问题  |
| `--throttle N`          | 事件间隔，单位ms    |
| `-v / -v -v / -v -v -v` | 日志详细等级        |
| `--ignore-crashes`      | 崩溃后继续执行      |
| `--ignore-timeouts`     | ANR无响应后继续执行 |
| `--pct-touch 30`        | 触摸事件占比30%     |
| `--pct-motion`          | 滑动手势事件占比    |

**日志关键字识别**

- `CRASH`：程序崩溃；`ANR`：应用无响应；`Dropped`：事件丢失。
  常见异常：空指针、内存溢出OOM、类找不到、参数非法等。

强制停止Monkey：

```bash
adb shell
ps | grep monkey
kill 进程ID
```

### 5.3 Windows桌面应用自动化

#### pywinauto

用于Windows桌面程序自动化。
安装：`pip install pywinauto`

两种后端backend：

1. `win32`（默认）：MFC、VB6、老式WinForm程序。
2. `uia`：WPF、Qt5、新版WinForms、微软商店应用。

两个核心对象

1. `Application`：绑定单个进程，普通桌面软件使用。
2. `Desktop`：跨进程，用于多实例窗口。

示例

```python
from pywinauto import Application

app = Application("uia").start("notepad.exe")
title = "无标题‑记事本"
# 菜单选择
app[title].menu_select("编辑->时间/日期(&D)")
# 输入文字
app[title].Edit.type_keys("hello test", with_spaces=True)
# 打印控件标识，用于定位
print(app[title].print_control_identifiers())
```

控件查看工具：Spy++、Inspect。

### 5.4 PyAutoGUI（屏幕层面自动化）

不识别控件，基于屏幕坐标做鼠标、键盘模拟，适合无控件API的桌面程序。

```bash
pip install pyautogui
```

```python
import pyautogui
# 鼠标
w,h = pyautogui.size()
pyautogui.moveTo(200,200,duration=1)
pyautogui.click()
# 键盘
pyautogui.typewrite("hello")
pyautogui.hotkey("ctrl","c")
# 设置每个操作默认延迟
pyautogui.PAUSE = 1
# 截图
img = pyautogui.screenshot()
img.save("screen.png")
```

## 第六章 高频简答题汇总

1. **黑盒测试和白盒测试区别**
   黑盒测试不关注代码实现，基于需求文档验证功能，多用于接口、UI测试；白盒测试分析代码分支、路径，多用于单元测试，用代码覆盖率衡量充分度。

2. **为什么边界值容易出现缺陷？**
   开发编码时经常忽略区间临界值，正常输入不容易暴露问题，临界位置容易发生越界、截断、逻辑判断错误。

3. **Mock使用场景**
   单元测试隔离第三方、下游服务；自动化测试绕开不稳定外部接口；模拟超时、500、空数据等异常，覆盖异常测试场景。

4. **pytest fixture对比setUp的优势**
   支持函数、模块、会话多级别；支持参数传递，脚本复用性更强；yield语法可以同时实现前置初始化与后置清理。

5. **隐式等待与显式等待区别**
   隐式等待是全局设置，查找所有元素都会等待固定时长；显式等待针对单个元素，条件满足立刻向下执行，执行效率更高。

6. **coverage覆盖率100%是否代表没有bug？**
   不等于。覆盖率仅代表代码被走到，无法覆盖业务逻辑、边界场景、异常流程。

7. **curl与Postman适用场景**
   curl适合无图形界面服务器调试，可嵌入脚本调用；Postman可视化操作，支持环境变量、批量执行，适合前期接口调试、梳理用例。

8. **uiautomator2适用范围**
   仅支持安卓APP自动化，依赖adb，通过控件id、页面文字定位控件，用于APP业务流程回归测试。

9. **Playwright相比Selenium的优势**
   原生支持多浏览器，内置等待机制，无需手动写大量等待逻辑；自带录制、Trace追踪调试工具，安装简单，稳定性更好。

10. **Monkey测试的作用，如何判断APP发生崩溃？**
    Monkey向APP发送大量随机操作，用于稳定性、压力测试；日志出现`CRASH`关键字代表程序崩溃，出现`ANR`代表应用无响应。

11. **POM页面对象模型的作用**
    页面定位与业务操作和测试脚本分离；页面改版只修改页面类，不用大量修改测试脚本，提升脚本可维护性和复用性。

12. **pywinauto和PyAutoGUI区别**
    pywinauto识别Windows控件，可以按控件名称、按钮定位；PyAutoGUI基于屏幕像素坐标，不识别控件，兼容性强但分辨率变化脚本容易失效。

## 相关知识

- [[Test Development Knowledge Map]]
- [[Python Knowledge Map]]
- [[Web Basics#3. HTTP/HTTPS 核心|HTTP 与 HTTPS]]
- [[Browser DevTools Notes#4. Network 网络面板|浏览器 Network 面板]]
- [[Database Basics 2#二、假数据生成|Faker 假数据]]
- [[Git Notes|Git]]
