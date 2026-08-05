---
name: rolldek-gptimg-generate
description: 使用 RollDek GPT Image API 生成新图片。仅在用户要进行文生图、海报、插画、产品图、概念图或其他从提示词生成图片的任务时使用；不要用于参考图编辑。
compatibility: 需要先加载 rolldek-gptimg 公共规则，并设置 ROLLDEK_API_KEY。
---

# RollDek-gptimg-generate：文生图

## 适用场景

当用户要求“生成一张图”“根据描述画图”“制作海报/插画/产品图”等，从零开始生成图片时使用本 Skill。

如果用户提供了需要修改的图片，改用：

- 单张图：`rolldek-gptimg-edit`
- 多张参考图：`rolldek-gptimg-multi-reference`

## 请求

端点：

```text
POST https://rolldek.com/v1/images/generations
```

请求头：

```text
Authorization: Bearer ${ROLLDEK_API_KEY}
Content-Type: application/json
```

必填参数：

- `model`: `gpt-image-2` 或 `gpt-image-2-high`
- `prompt`: 中文或英文提示词

示例：

```bash
curl https://rolldek.com/v1/images/generations \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "湖蓝色调的山谷，清晨薄雾，极简插画风",
    "size": "1024x1536",
    "response_format": "url"
  }'
```

## 参数决策

- 默认模型：`gpt-image-2`
- 需要高质量时使用 `gpt-image-2-high` 和 `quality=high`
- `gpt-image-2` 的 `quality` 固定为 `medium`
- 未指定尺寸时使用 `auto` 或不传 `size`
- 未指定输出格式时使用 `b64_json`；需要直接下载时使用 `url`
- `n` 范围为 1–10，生成多张前必须提示按张计费

## Python CLI

使用公共脚本：

```bash
python3 ../RollDek-gptimg/scripts/rolldek_image.py \
  --prompt "高端香水产品海报，黑色背景，轮廓光，商业摄影" \
  --model gpt-image-2-high \
  --size 3840x2160 \
  --quality high \
  --output perfume.png
```

脚本使用 Python 标准库，不需要安装 SDK。

## 完成后

- 如果保存到本地，报告实际文件路径。
- 如果返回 URL，提醒用户 RollDek URL 约 6 小时失效，应及时下载或转存。
- 不输出 API Key。
