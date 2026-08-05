---
name: rolldek-gptimg-edit
description: 使用 RollDek GPT Image API 编辑一张参考图片。仅在用户要修改、重绘、换背景、添加或移除元素，同时提供一张参考图时使用；多张参考图请使用 rolldek-gptimg-multi-reference。
compatibility: 需要先加载 rolldek-gptimg 公共规则，并设置 ROLLDEK_API_KEY。
---

# RollDek-gptimg-edit：单图编辑

## 适用场景

适用于：

- 给现有图片添加或移除元素
- 修改背景、颜色、光线或风格
- 保留主体与构图进行局部变化
- 根据一张参考图进行图像编辑

如果有两张或更多参考图，改用 `rolldek-gptimg-multi-reference`。

## 请求

端点：

```text
POST https://rolldek.com/v1/images/edits
```

使用 `multipart/form-data`，字段包括：

- `model`: `gpt-image-2` 或 `gpt-image-2-high`
- `image`: PNG、JPEG 或 WebP 参考图
- `prompt`: 清晰描述需要改变的内容
- `size`: 可选；不传时沿用参考图尺寸
- `quality`、`n`、`response_format`: 按公共 Skill 的模型规则使用

cURL 示例：

```bash
curl https://rolldek.com/v1/images/edits \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -F "model=gpt-image-2" \
  -F "image=@otter.png" \
  -F "prompt=给这只海獭戴上一顶贝雷帽" \
  -F "response_format=url"
```

## 编辑提示词原则

1. 说明需要保留的内容，例如“保留主体、构图和姿态”。
2. 明确需要改变的区域和元素。
3. 说明期望的风格、光线、颜色或材质。
4. 不要只写“变好看”，要描述可执行的视觉变化。

示例：

```text
保留人物的脸部、姿势和服装，只把背景替换为雨后的东京街道，保持人物边缘自然，使用夜间霓虹灯光。
```

## Python CLI

```bash
python3 ../RollDek-gptimg/scripts/rolldek_image.py \
  --model gpt-image-2 \
  --image input.png \
  --prompt "保留主体和构图，只把背景改成日落海滩" \
  --output edited.png
```

## 限制与完成后

- 参考图最多 16 张；本 Skill 只处理一张。
- 不传 `size` 时沿用参考图尺寸。
- 本地保存后报告文件路径。
- 使用 URL 响应时提醒 URL 约 6 小时失效。
