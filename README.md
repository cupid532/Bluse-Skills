# Bluse-Skills

个人 Agent Skills 集合。

## RollDek GPT Image Skills

这些 Skill 都是 **RollDek 专属调用**，不是 OpenAI 官方 API：请求发送到 `https://rolldek.com/v1`，但请求格式兼容 OpenAI Images API。

| Skill | 用途 |
|---|---|
| [RollDek-gptimg](./RollDek-gptimg/SKILL.md) | 公共配置、服务商边界、模型和安全规则 |
| [RollDek-gptimg-generate](./RollDek-gptimg-generate/SKILL.md) | 文生图 |
| [RollDek-gptimg-edit](./RollDek-gptimg-edit/SKILL.md) | 单张参考图编辑 |
| [RollDek-gptimg-multi-reference](./RollDek-gptimg-multi-reference/SKILL.md) | 多张参考图合成与编辑 |
| [RollDek-gptimg-output](./RollDek-gptimg-output/SKILL.md) | 尺寸、质量、数量、响应格式和文件保存 |

公共脚本位于 [`RollDek-gptimg/scripts/`](./RollDek-gptimg/scripts/)。

官方文档：[RollDek GPT Image](https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f)

> 安全：使用前设置 `ROLLDEK_API_KEY`。不要把 API Key 写入 Skill、日志或 Git。`n` 按图片张数计费。
