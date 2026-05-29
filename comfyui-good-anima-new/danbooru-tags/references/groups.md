# Danbooru Group 选择

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在需要选择精细 group、处理中文/日文俗称、或解释分类边界时读取本文件。

## 常用 group

| Group                                  | 用途                                 |
| -------------------------------------- | ------------------------------------ |
| `artist` / `artists`                   | 画师                                 |
| `character` / `characters`             | 角色                                 |
| `series` / `ip` / `copyright`          | 作品/IP                              |
| `appearance` / `body`                  | 发色、发型、瞳色、耳、角、翅膀、体型 |
| `expression`                           | 表情/神态                            |
| `pose` / `action` / `camera`           | 姿势、动作、视角、构图、景别         |
| `clothing` / `outfit`                  | 基础服装                             |
| `clothing_detail` / `detail`           | 服装细节、毛边、兜帽、披风           |
| `handwear`                             | 手套、爪手套                         |
| `accessory` / `accessories`            | 配饰                                 |
| `scene` / `background` / `composition` | 场景、背景、天气、构图               |
| `lighting` / `light` / `atmosphere`    | 光影、阴影、逆光、景深、氛围         |
| `meta`                                 | highres、official art 等元信息       |

画师标签只来自 CSV 原始 artist 分类，必须保留 `@`。其他分类不带 `@`，不能当画师标签。

## 分类边界

- 精细 group 是优先过滤，不是绝对真理；部分 Danbooru 服装、构图、属性词实际属于 `general`。
- 查询常见视觉概念时，一次 batch 内放“主词 + 英文/罗马音别名 + 部件拆解”。
- 中文、日文俗称先翻译/转写成 Danbooru 常用英文或罗马音；中文原词只能作为辅助变体。
- 对可能被 group 白名单漏掉的概念，同一 batch 可同时放 `group=...` 与 `category=general` 变体。
- `newest / recent / mid / early / old` 和 `year xxxx` 是 Anima time period 控制词，不需要用 CSV 命中证明。
- 可检索旧画风锚点包括 `retro_artstyle`、`faux_retro_artstyle`、`heisei_retro`、`traditional_media`。
- `deviantart` 等 dataset 风格词可能位于作品/IP 桶；是否使用由 `comfyui-animatool` 的风格意图决定，本 CLI 只报告候选。

## 画师名解析

画师称呼解析的核心规则见 `comfyui-animatool/SKILL.md` 的「画师称呼解析」章节：网络搜索确认 canonical name → 别名转 `@artist` → CLI 校验 → confirmed 后写入 prompt。扩展细节见 `comfyui-animatool/references/prompt-assembly.md`。

此处补充 group 层面规则：

- 画师标签只来自 CSV 原始 artist 分类，必须保留 `@`。
- 网络搜索只用于解析称呼和别名，不替代 Anima CSV / Danbooru tag 校验。
