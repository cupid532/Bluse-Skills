# 更新记录

## 2026-08-05

### 新增 RollDek-gptimg

- 新增 `RollDek-gptimg` Skill，明确定位为 RollDek 专属 GPT Image 调用能力。
- 使用 `https://rolldek.com/v1`，兼容 OpenAI Images API 请求格式。
- 支持文生图 `/images/generations`。
- 支持图像编辑 `/images/edits`。
- 支持最多 16 张参考图、`gpt-image-2` / `gpt-image-2-high`、尺寸、质量、数量和响应格式参数。
- 新增无第三方依赖的 `scripts/rolldek_image.py`，支持本地生成、编辑、下载 URL 响应和解码 base64 响应。
- 增加 RollDek 与 OpenAI 官方 API 的边界说明、费用提示和 API Key 安全提示。
