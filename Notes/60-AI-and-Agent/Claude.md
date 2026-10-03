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

### Claude code中的上下文压缩机制(五层)
#### 第一层Tool Result预算裁剪：

处理机制:
1. 每个工具声明一个返回结果的最大值，当超过这个阈值的时候不会简单截断，而是持久化到磁盘
2. 然后上下文context中指标留一个指向持久化存储地址的链接
#### 第二层History Snip:

处理机制：
1. 通过裁剪历史记录中的冗余消息释放token，释放完token之后，释放量传给后续的autocompact阈值检查，如果不传的话可能会导致过早触发auto compact.
#### 第三层Microcompact:

处理机制:
- 清理历史中不再需要的旧工具结果，关键设计是这个方法有两个完全不同的路径，根据缓存状态选择。

**路径A**

基于时间的Microcompact(缓存已冷)

当用户离开一段时间后再回来(超过配置的分钟数时)，这时候缓存已经冷了，而且无论如何下次聊天都需要重新上传完整前缀。

这种情况下Microcompact会只保留最近几个可压缩工具的结果，其他全换成占位符(因为无论如何都要重建，替换内容也不会导致缓存失效，消息丢失)

**路径B**

用户一直活跃对话，这时候就无法直接修改消息内容，会导致`cache key`发生变化，导致缓存前缀失效，要重新上传与计费。

因此，缓存编辑路径完全不修改本地消息。它使用一种巧妙的 API 级机制：

1. 在工具结果块上添加 `cache_reference` 字段（等于 `tool_use_id`），让服务端能够定位缓存中的具体位置
2. 构造 `cache_edits` 块，告诉服务端"删除这些 `cache_reference` 指向的内容"
3. 服务端在缓存中就地删除，不需要客户端重新上传前缀

这两条路径是互斥的，而且时间触发的优先级更高，如果时间触发了，就会直接跳过。

**路径 C：API 端原生 context management**

除了上面两条客户端路径，`src/services/compact/apiMicrocompact.ts` 还提供一条**让 API 自己清理**的路径——不在客户端动消息，而是在请求体里塞 `context_management.edits` 策略数组，让服务端在打 prefix cache 时顺便做清理。

```text
设计决策：为什么 `clear_tool_uses_20250919` 要设置 `clear_at_least: 140K`？

官方文档的 [Context editing 说明](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 明确指出：_Tool result clearing invalidates cached prompt prefixes when content is cleared. To account for this, clear enough tokens to make the cache invalidation worthwhile._ 清理工具结果会直接破坏 prompt cache 前缀——这意味着本次请求的缓存写入成本（cache_creation_input_tokens）必然发生。如果只清掉几千 token，付出了一整次缓存重写的代价却没换回多少上下文空间，得不偿失。`clear_at_least: 140K` 确保每次触发都清出足够量（180K 触发阈值 − 40K 目标 = 140K），让缓存失效的代价换来实质性的空间收益。

与此形成对比的是 `clear_thinking_20251015`：官方文档说明 _When thinking blocks are kept in context, the prompt cache is preserved_——保留 thinking blocks 不破坏缓存，所以不需要 `clear_at_least` 约束。但当 thinking blocks 被清除（`clearAllThinking=true`，即 `keep: { thinking_turns: 1 }`）时同样会破坏缓存，只是那时已经是 1h idle 等到 cache TTL 过期后才触发，缓存反正要重写，所以也不需要特别保底
```

#### 第四层: 上下文折叠（投影式）

投影式上下文折叠——关键特性是它不修改原始消息。它创建消息的折叠视图，将不重要的早期消息替换为摘要。这使得折叠可以跨轮次持久化，且可以在需要时回退。

#### 第五层: Autocompact

这是最后的手段——当所有轻量级压缩都无法将 Token 使用量控制在安全范围内时，系统 fork 一个子 Agent 来生成整个对话的摘要。

**5a 子路径的输出：**

保留尾部 10K~40K token 原文 + 把前面段用 `summary.md` 内容包成 `isCompactSummary` 消息替代。`sessionMemoryCompactConfig` 默认值

### 前缀缓存策略

每次API请求，服务端都需要对输入做一遍KV cache计算。但如果每次都完整重新计算的话，延迟和成本都无法接受。

前缀缓存的原理：服务端记住上一次请求的KV Cache结果，下次请求的时候如果前缀完全一致就直接复用计算结果，只需要处理新增部分。