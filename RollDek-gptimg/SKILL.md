---
name: rolldek-gptimg
description: RollDek GPT Image 的公共配置和调用边界。用于所有需要通过 RollDek 调用 GPT Image 2 的任务；根据具体用途继续加载 rolldek-gptimg-generate、rolldek-gptimg-edit、rolldek-gptimg-multi-reference 或 rolldek-gptimg-output。
compatibility: 需要 RollDek API Key，并可访问 https://rolldek.com/v1。
metadata:
  provider: RollDek
  api_compatibility: OpenAI Images API
  documentation: https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f
---

# RollDek-gptimg 公共规则

## 服务商边界

这是 RollDek 专属调用 Skill，不是 OpenAI 官方 API Skill。

- Base URL：`https://rolldek.com/v1`
- 文生图：`POST /images/generations`
- 图像编辑：`POST /images/edits`
- Key：RollDek API Key
- 请求格式：兼容 OpenAI Images API，但实际服务商是 RollDek

不要在没有用户明确同意的情况下切换到 `api.openai.com` 或其他服务商。

## 配置

```bash
export ROLLDEK_API_KEY="你的 RollDek API Key"
```

只报告 Key“已配置/未配置”，绝不打印 Key。不要将 Key 写入代码、Skill、日志或 Git。

不建议使用 `OPENAI_API_KEY`。只有用户明确说明该变量中的 Key 实际属于 RollDek 时才允许使用。

## 模型

- `gpt-image-2`：质量固定为 `medium`。
- `gpt-image-2-high`：支持 `medium` 和 `high`；不传质量时默认为 `high`。

两个模型都支持文生图、图像编辑、多参考图、1K/2K/4K 和 URL/base64 响应。

## 工作流

1. 先确认用户是要生成新图还是编辑参考图。
2. 根据用途加载对应的专用 Skill。
3. 确认模型、尺寸、质量、生成数量 `n` 和输出格式。
4. `n > 1` 前提醒用户按张计费。
5. 不将完整 base64 或 API Key 输出到聊天或普通日志。

公共 CLI：

```bash
python3 RollDek-gptimg/scripts/rolldek_image.py --help
```

详细接口以官方文档为准：
https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f
