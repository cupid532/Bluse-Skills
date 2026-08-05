---
name: rolldek-gptimg-output
description: 管理 RollDek GPT Image 的输出参数和结果处理。用于选择尺寸、质量、生成数量 n、URL/base64 响应格式，以及下载 URL 或把 base64 图片保存到本地。
compatibility: 需要先加载 rolldek-gptimg 公共规则。
---

# RollDek-gptimg-output：输出控制

## 尺寸

`size` 使用官方支持的宽×高像素值：

- 1K、2K、4K 均支持
- 示例：`1024x1024`、`1024x1536`、`3840x2160`
- 不指定时使用 `auto`
- 编辑请求不传 `size` 时沿用参考图尺寸

不要任意拼接未确认支持的像素尺寸；遇到尺寸错误时先改用已知支持的尺寸。

## 质量

| 模型 | 规则 |
|---|---|
| `gpt-image-2` | 固定 `medium`，传 `quality` 也不会改变实际质量 |
| `gpt-image-2-high` | 支持 `medium` 或 `high`；不传时默认 `high` |

需要高质量输出时：

```json
{
  "model": "gpt-image-2-high",
  "quality": "high"
}
```

## 数量 n

- 范围：1–10
- 默认：1
- 按张计费；`n=2` 就是两张的费用
- 生成多张前必须向用户说明费用影响
- 返回结果在 `data` 数组中按顺序排列

## 响应格式

### base64

默认是 `b64_json`：

```json
{
  "data": [
    { "b64_json": "iVBORw0KGgo..." }
  ]
}
```

它是纯 base64，不带 `data:` 前缀。需要本地文件、内嵌传递或离线处理时使用。

### URL

传入：

```json
{ "response_format": "url" }
```

响应元素为：

```json
{ "url": "https://..." }
```

URL 约 6 小时失效，获取后应立即下载或转存。不要把短期 URL 当作永久资源。

## Python CLI

本地保存 base64 响应：

```bash
python3 ../RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "一只红色狐狸" \
  --output fox.png
```

请求 URL 并下载到本地：

```bash
python3 ../RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "一只红色狐狸" \
  --response-format url \
  --output fox.png
```

生成多张时，若输出文件是 `fox.png`，脚本会生成：

```text
fox-2.png
fox-3.png
...
```

## 安全与结果处理

- 不要在聊天中打印完整 base64，除非用户明确需要。
- 不要记录 API Key。
- 返回 URL 时报告 URL 的临时有效期。
- 保存成功后报告实际文件路径和数量。
