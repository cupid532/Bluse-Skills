# 更新记录

## 2026-08-05

### 重构为按用途分类的独立 Skills

- 将原本集中在一个 `SKILL.md` 的内容拆分为多个独立 Skill 文件。
- `RollDek-gptimg`：公共配置、服务商边界、模型和安全规则。
- `RollDek-gptimg-generate`：文生图。
- `RollDek-gptimg-edit`：单图编辑。
- `RollDek-gptimg-multi-reference`：多参考图合成与编辑。
- `RollDek-gptimg-output`：尺寸、质量、数量、响应格式和结果保存。
- README 仅作为技能索引，不再承载全部使用说明。
- 保留公共的零依赖 Python CLI：`RollDek-gptimg/scripts/rolldek_image.py`。

### 首次新增 RollDek GPT Image 能力

- 使用 `https://rolldek.com/v1`，兼容 OpenAI Images API 请求格式。
- 支持 `gpt-image-2` / `gpt-image-2-high`。
- 支持文生图 `/images/generations`、图像编辑 `/images/edits` 和最多 16 张参考图。
- 增加 RollDek 与 OpenAI 官方 API 的边界说明、费用提示和 API Key 安全提示。
