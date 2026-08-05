# Bluse-Skills

个人 Agent Skills 集合，按用途分类存放。

## 图片处理

### RollDek-gptimg

目录：[`img/RollDek-gptimg/`](./img/RollDek-gptimg/)

一个集成的 RollDek GPT Image Skill，支持：

- 文生图
- 单图编辑
- 多参考图编辑
- 模型与质量选择
- 1K / 2K / 4K 尺寸
- 多图生成
- URL / base64 响应
- 本地图片保存

这是 **RollDek 专属调用**，请求地址为 `https://rolldek.com/v1`，只是兼容 OpenAI Images API 格式，不是 OpenAI 官方接口。

官方文档：[RollDek GPT Image](https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f)

设置 API Key：

```bash
export ROLLDEK_API_KEY="你的 RollDek API Key"
```

> 不要把 API Key 写入文件、日志或 Git。`n` 按生成张数计费。
