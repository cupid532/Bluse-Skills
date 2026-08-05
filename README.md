# Bluse-Skills

个人 Agent Skills 集合。

## 当前 Skill

### RollDek-gptimg

`RollDek-gptimg/` 是一个 **RollDek 专属**的 GPT Image Skill：

- 通过 `https://rolldek.com/v1` 调用 RollDek API
- API 请求格式兼容 OpenAI Images API，但不是 OpenAI 官方服务
- 支持 `gpt-image-2` 与 `gpt-image-2-high`
- 支持文生图、图像编辑、多参考图、1K/2K/4K、`n` 和 URL/base64 响应
- 附带零依赖 Python CLI，可生成图片、编辑图片并把响应保存到本地

文档入口：[RollDek-gptimg/SKILL.md](./RollDek-gptimg/SKILL.md)

官方参考文档：[RollDek GPT Image 文档](https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f)

### 快速开始

```bash
export ROLLDEK_API_KEY="你的 RollDek API Key"
python3 RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "湖蓝色调的山谷，清晨薄雾，极简插画风" \
  --size 1024x1536 \
  --output valley.png
```

安全提醒：不要把 API Key 写入文件、日志或提交到仓库。`n` 按生成张数计费；使用 URL 响应时，RollDek 返回的 URL 约 6 小时失效。
