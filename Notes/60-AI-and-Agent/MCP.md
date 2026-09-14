# FastMCP 学习笔记

## 创建并启动 MCP Server

```python
policy_server = FastMCP("policy_server")
```

这行代码会创建一个名为 `policy_server` 的 MCP Server。

```python
policy_server.run(transport="stdio")
```

这行代码用于启动 `policy_server`。

`transport` 指采用哪种通信方式。其中，`stdio` 表示标准输入输出。

### 与普通 HTTP Server 的区别

FastAPI 等普通 HTTP Server 会监听网络端口，例如 `localhost:8000`。

Stdio MCP 不监听端口，而是通过进程的标准输入输出进行通信。

## 注册 MCP 工具

```python
@policy_server.tool()
```

这个装饰器会把普通函数注册为 MCP 工具。FastMCP 看到该装饰器后，会把对应函数加入 `tools/list`。

### 工具说明

工具说明，即函数说明，位于函数内部，并且必须写在函数声明的下一行。普通 Python 调用者可以查看该说明，FastMCP 也可以把它放入 `tools/list`。

### 参数类型标注

参数类型标注可以让 FastMCP 稳定地生成参数 schema，也能让代码审查更容易。

例如：

```python
get_num(num: str)
```

## Pydantic 配置与校验

### ConfigDict

```python
class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
```

这表示所有继承自 `StrictModel` 的配置模型都不允许出现未声明的额外字段。

### Literal

Pydantic 中的 `Literal` 表示一个字段只能等于指定的固定值。

```python
type: Literal["cli"]
```

上面的字段只允许使用 `"cli"` 这一种值。

### Field

`Field` 是 Pydantic 中为字段增加校验规则、默认值和说明信息的工具。

例如：

```python
Field(min_length=1)
```

这表示字段的最小长度为 `1`。

## MCP 中的 module

`module` 用于说明这个 MCP Server 的 Python 启动模块在哪里。

## MCP 与 Claude SDK 的关系

Claude SDK 最终需要以下两项信息：

- `command`：运行哪个程序。
- `args`：向程序传递哪些参数。

MCP 会把：

```python
module = "mcp_servers.policy_server"
```

转换为：

```python
command = "当前 Python 解释器"
args = ["-m", "mcp_servers.policy_server"]
```

同时ClaudeSDK还需要：
- server名称
- 允许模型调用的工具名称

`xxx_adapter`的作用就是把`agent manifest`转化为Claude SDK能看懂的知识

## 相关知识

- [[AI and Agent Knowledge Map]]
- [[Python Basics 3#7. 装饰器|Python 装饰器]]
- [[Web Basics#3. HTTP/HTTPS 核心|HTTP 与 HTTPS]]
- [[Python Basics 4#6. JSON 文件操作|JSON]]
- [[YAML Notes|YAML]]
- [[FastMCP.docx|原始 Word 笔记]]
- [[Pydantic model_validate]]
