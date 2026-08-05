# 更新记录

## 2026-08-05

### 目录结构简化

- 将 RollDek GPT Image 相关内容合并为一个集成 Skill。
- 按用途增加 `img/` 图片类别目录。
- Skill 位置统一为 `img/RollDek-gptimg/`。
- 文生图、图像编辑、多参考图和输出控制全部由同一个 Skill 处理。
- README 仅保留分类目录和 Skill 索引。
- 保留零依赖 Python 调用脚本。
