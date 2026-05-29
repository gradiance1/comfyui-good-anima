# 参考图处理

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在用户提供参考图，或要求参考构图、视角、景深、布局时读取本文件。

## 判断参考范围

先确认用户要参考什么：

- 只参考构图/视角/景深：只提取构图信息。
- 参考角色/服装/颜色/道具/场景：需要明确写入 prompt 或 hard anchors。
- 没有说明参考范围：默认只参考构图，不复制角色、服装、颜色、道具或场景。

## 只参考构图时提取

- aspect ratio
- camera distance
- camera angle
- subject position
- foreground / midground / background
- light direction
- blur / focus behavior

不要复制：

- reference character
- outfit
- color scheme
- props
- setting

## 回写到 Anima prompt

- 稳定视觉词可以放 hard anchors。
- 复杂结构、景深、主体位置和脸部可读性写入 `nltags`。
- 如果参考图构图和用户指定尺寸冲突，保留用户尺寸并改写构图。
- 背景不是主体时，默认用轻微背景虚化或景深分离主体。
