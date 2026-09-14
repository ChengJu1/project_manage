## `@tool`

类似于FastMCP中的`@server_name.tool`都是把普通的python函数注册成模型可调用的工具

主要区别
- 函数注册到哪个server
- 工具是怎么运行的

`@tool`主要是通过
```Python
create_sdk_mcp_server(...)
```
创建一个运行在后端进程内部的SDK MCP Server
比较适合需要直接访问后端对象的工具

`policy_server.tool`通过
```python
policy_server -m mcp_servers.policy_server
```
注册为独立的policy_server，可作为独立的子进程启动，通过stdio与Claude SDK通信

## Claude SDK中常用的类

- `AssistantMessage`：模型输出的一条完整消息。
- `ToolUseBlock`：模型发起工具调用。
- `UserMessage`：SDK 把工具结果送回模型时产生的消息。
- `ToolResultBlock`：工具执行结果。
- `StreamEvent`：模型正在逐步生成文字时的流式事件。
- `ClaudeAgentOptions`：Agent 的运行配置。
- `query`：启动 Agent Loop。

## SDK message 

`message` 是 SDK 返回的消息对象；它的具体类型决定里面有什么。文字在 `StreamEvent.event` 中，工具请求在 `AssistantMessage.content` 中，工具结果在 `UserMessage.content` 中。