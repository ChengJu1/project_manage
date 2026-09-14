## model_validate

```python
manifest = AgentManifest.model_validate(raw_manifest)
```

这个指的是按照`AgentManifest`的内容去校验`raw_manifest`的内容，比如会校验下列数据：

`json.loads()`后得到的`raw_manifest`python字典如下：
```Python
{
  "id": "policy_qa_assistant",
  "name": "制度问答助理",
  "description": "通过 MCP 查询公司制度，并提供带来源的回答",
  "system_prompt": "prompts/policy.md",
  "skills": [
    "skills/policy_skill.md"
  ],
  "tools": [
    {
      "type": "mcp",
      "name": "policy_server",
      "transport": "stdio",
      "module": "mcp_servers.policy_server",
      "actions": [
        "search_policy",
        "get_policy_detail"
      ]
    }
  ],
  "permissions": {
    "dry_run_by_default": true,
    "require_approval": []
  }
}
```

`model_validate`先校验最外层内容

```
id             是不是字符串
name           是不是字符串
description    是不是字符串
system_prompt  是不是字符串
skills         是不是非空列表
tools          是不是非空列表
permissions    是否符合权限配置
```

然后会检查`tools`中的第一项

```python
{
  "type": "mcp",
  "name": "policy_server",
  "transport": "stdio",
  "module": "mcp_servers.policy_server",
  "actions": [
    "search_policy",
    "get_policy_detail"
  ]
}
```

`tools` 中的每一项允许是 `CliToolManifest` 或 `McpToolManifest`。Pydantic 根据两个模型的字段规则和 `type` 的 `Literal` 限制，判断当前数据符合 `McpToolManifest`（写了`Literal`才是逐字符对齐）。
```
type       必须是 mcp
name       必须是字符串
transport  必须是 stdio
module     必须是字符串
actions    必须是非空字符串列表
```

然后是权限校验（必须严格一个字符一个字符匹配）

检查结束后`manifest`就会变成一个`AgentManifest`对象（也就是代表可以通过`manifest.name/id`等查看内容）

### 通过 `model_validate` 不代表所有运行条件都没问题

`model_validate()` 通过只能说明：

- 配置字段存在。
- 字段类型正确。
- Literal 值正确。
- 列表长度正确。
- 没有多余字段。
- 审批 action 存在于工具白名单。

它不会检查：

- `prompts/policy.md` 是否真的存在。
- `skills/policy_skill.md` 是否真的存在。
- `mcp_servers.policy_server` 能否成功启动。
- MCP Server 是否真的注册了这些 action。
- Markdown 制度文件是否存在。