---
name: rolldek-gptimg-multi-reference
description: 使用 RollDek GPT Image API 根据多张参考图进行合成、重排或编辑。仅在用户提供两张或更多图片，并要求组合元素、保持跨图风格或将一个图中的对象放入另一个图中时使用。
compatibility: 需要先加载 rolldek-gptimg 公共规则，并设置 ROLLDEK_API_KEY。
---

# RollDek-gptimg-multi-reference：多参考图

## 适用场景

适用于：

- 将第二张图中的对象放到第一张图中
- 组合多个角色、物体或场景
- 参考一张图的构图，另一张图的主体或风格
- 多图产品合成和视觉统一

## 请求

端点：

```text
POST https://rolldek.com/v1/images/edits
```

同一个字段重复出现即可传多张图。推荐使用 `image[]`：

```bash
curl https://rolldek.com/v1/images/edits \
  -H "Authorization: Bearer ${ROLLDEK_API_KEY}" \
  -F "model=gpt-image-2" \
  -F "image[]=@teapot.png" \
  -F "image[]=@duck.png" \
  -F "prompt=把第二张图里的黄色小鸭子放在第一张图的茶壶旁边，保持同样的桌面和光线"
```

`image[]` 和重复的 `image` 都可以；图像顺序必须与提示词中的“第一张/第二张”等指代一致。

## 操作步骤

1. 按用户描述确定图片顺序。
2. 在提示词中明确引用关系，例如“第一张图的背景”“第二张图的主体”。
3. 指定要保持的光线、透视、比例、材质和风格。
4. 确认参考图不超过 16 张。
5. 多图输入会增加输入 token；生成多张还会按 `n` 额外计费。

## Python CLI

```bash
python3 ../RollDek-gptimg/scripts/rolldek_image.py \
  --model gpt-image-2 \
  --image first.png \
  --image second.png \
  --prompt "把第二张图的物体放到第一张图旁边，保持光线、透视和桌面一致" \
  --output result.png
```

## 限制

- 每次最多接收 16 张参考图；第 17 张起会返回 HTTP 400。
- 图片越多，输入 token 越高，应按需要传入。
- `size` 不传时沿用参考图尺寸；需要统一画布时显式指定尺寸。
