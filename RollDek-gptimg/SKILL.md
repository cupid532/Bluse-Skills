---
name: rolldek-gptimg
description: 通过 RollDek OpenAI-compatible Images API 调用 GPT Image 2 进行文生图、图像编辑和多参考图合成。仅在用户明确要求使用 RollDek、rolldek.com、RollDek GPT Image，或需要通过 RollDek API 生成/编辑图片时使用；不要把它当作 OpenAI 官方接口。
compatibility: 需要 RollDek API Key，并可访问 https://rolldek.com/v1；可使用 OpenAI Python/Node.js SDK 或标准 HTTP 请求。
metadata:
  provider: RollDek
  api_compatibility: OpenAI Images API
  documentation: https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f
---

# RollDek-gptimg

使用 RollDek 的兼容 OpenAI Images API 调用 `gpt-image-2` 系列模型。

## 重要边界

这是 **RollDek 专属 Skill**，不是 OpenAI 官方 API Skill：

- API Base URL 固定为 `https://rolldek.com/v1`。
- API Key 必须是 RollDek Key，不要把 Key 写入代码、Skill、日志或 Git。
- 虽然请求格式兼容 OpenAI Images API、可以使用 OpenAI SDK，但请求实际发送到 RollDek。
- 不要在没有用户明确同意的情况下，把请求切换到 `api.openai.com` 或其他服务商。

## 配置

优先从环境变量读取：

```bash
export ROLLDEK_API_KEY="你的 RollDek API Key"
```

不建议使用 `OPENAI_API_KEY` 回退变量；只有在用户明确说明该 Key 实际属于 RollDek 时才可以使用它。推荐只使用 `ROLLDEK_API_KEY`，避免误把官方 OpenAI Key 发给 RollDek。

执行前检查：

1. 确认 API Key 存在，但只报告“已配置/未配置”，绝不打印值。
2. 确认用户是否需要生成还是编辑。
3. 确认输出是 URL 还是 base64；默认优先 `url` 便于下载，若用户要求内嵌或本地解码则使用 `b64_json`。
4. 生成前向用户复述关键参数，尤其是模型、质量、尺寸和 `n`，因为 `n` 按张计费。

## 模型与质量规则

| 模型 | 质量 |
|---|---|
| `gpt-image-2` | 质量固定为 `medium`；传入 `quality` 不会改变实际质量 |
| `gpt-image-2-high` | 支持 `medium`/`high`；不传时默认为 `high` |

两个模型都支持文生图、图像编辑、多参考图、1K/2K/4K 和两种响应格式。

## 文生图

端点：`POST https://rolldek.com/v1/images/generations`

必填字段：

- `model`: `gpt-image-2` 或 `gpt-image-2-high`
- `prompt`: 中英文均可

可选字段：

- `size`: 官方支持的 `宽x高` 像素值，例如 `1024x1024`、`1024x1536`、`3840x2160`；默认 `auto`
- `quality`: 按模型规则填写 `medium` 或 `high`
- `n`: `1`–`10`，默认 `1`；按张计费
- `response_format`: `url` 或 `b64_json`；默认 `b64_json`

cURL 示例：

```bash
curl https://rolldek.com/v1/images/generations \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2-high",
    "prompt": "高端香水产品海报，黑色背景，轮廓光，商业摄影",
    "size": "3840x2160",
    "quality": "high",
    "response_format": "url"
  }'
```

## 图像编辑

端点：`POST https://rolldek.com/v1/images/edits`

使用 `multipart/form-data`：

- `model`: 必填
- `image`: 参考图文件，PNG/JPEG/WebP，最多 16 张
- `prompt`: 必填
- `size`: 可选；不传时沿用参考图尺寸
- `quality`、`n`、`response_format`: 按文生图规则使用

单图示例：

```bash
curl https://rolldek.com/v1/images/edits \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -F "model=gpt-image-2" \
  -F "image=@input.png" \
  -F "prompt=保留主体和构图，只把背景改成日落海滩" \
  -F "response_format=url"
```

多图示例：重复 `image[]`（也接受重复的 `image`），顺序就是提示词中的“第一张/第二张”：

```bash
curl https://rolldek.com/v1/images/edits \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -F "model=gpt-image-2" \
  -F "image[]=@teapot.png" \
  -F "image[]=@duck.png" \
  -F "prompt=把第二张图里的黄色小鸭子放在第一张图的茶壶旁边，保持相同桌面和光线"
```

超过 16 张参考图会返回 HTTP 400；图片越多，输入 token 越高，应按需传入。

## 响应处理

成功响应结构：

```json
{
  "created": 1781837823,
  "data": [
    { "b64_json": "iVBORw0KGgo..." }
  ]
}
```

- 默认 `response_format` 是 `b64_json`，内容是纯 base64，不带 `data:` 前缀。
- `response_format=url` 时，`data` 元素包含 `url`；URL 约 6 小时失效，应及时下载或转存。
- `n > 1` 时按顺序返回多项 `data`。
- 不要把完整 base64 或 API Key 输出到聊天、提交到 Git 或写入普通日志。

## 推荐实现方式

优先使用随 Skill 提供的脚本：

```bash
python3 /绝对路径/RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "湖蓝色调的山谷，清晨薄雾，极简插画风" \
  --model gpt-image-2 \
  --size 1024x1536 \
  --response-format url
```

图像编辑：

```bash
python3 /绝对路径/RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "给这只海獭戴上一顶贝雷帽" \
  --image otter.png \
  --output edited.png
```

多参考图：

```bash
python3 /绝对路径/RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "把第二张图的物体放到第一张图旁边，保持光线一致" \
  --image first.png --image second.png \
  --output result.png
```

脚本默认使用 Python 标准库，不需要安装 SDK。运行前设置 `ROLLDEK_API_KEY`。只有用户要求返回 URL 时才使用 `--response-format url`；本地输出图片时使用默认 base64 响应并用 `--output` 解码保存。

## 故障排查

- `401/403`：检查是否使用 RollDek Key、Authorization 头和 `ROLLDEK_API_KEY`，不要回退到官方 OpenAI。
- `400`：检查模型、尺寸、质量、`n` 范围、图片格式和参考图数量。
- URL 无法访问：RollDek URL 约 6 小时失效，立即下载并转存。
- 输出质量与预期不符：`gpt-image-2` 始终是 medium；需要 high 时使用 `gpt-image-2-high` 并传 `quality=high`。
- 生成多张前必须确认费用影响：`n=2` 就按两张计费。

详细接口以 RollDek 官方文档为准：
https://rolldek.com/docs/#/README?id=%e6%a8%a1%e5%9e%8b%e4%b8%8e%e8%b4%a8%e9%87%8f
