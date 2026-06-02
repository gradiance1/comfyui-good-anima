# Composition Failure Guardrails / 构图失败防漂移索引

> **T3 Runtime 参考** — 只在已经进入构图规划、或生成结果出现明确失败症状时读取。
> 本目录不是构图教材，不教模型通用美术知识；只记录 Anima 容易漂移的失败模式、保护句和 tag/nltags 分工。

## 使用边界

- 不默认读取本目录；简单单人图、用户已有清晰 prompt、普通光影/情绪关系不读。
- 先判断失败症状，再读取最多 1 个相关文件；不要批量加载整套资料。
- 只提取能防止漂移的执行约束：脸部可读性、属性归属、主体占比、落地线索、冲突消解。
- 不把案例文字原样复制进 prompt；最终只回写短英文 `nltags` 或少量已确认 hard anchors。
- 成人/特殊专项不在本索引触发；只有用户明确请求对应内容时，另读 `../adult-runtime/_index.md`。

## 失败症状路由

| 失败症状 / 风险 | 读取文件 | 只提取什么 |
| --- | --- | --- |
| 主体太小、头像/半身/全身尺度不合适 | `single-character.md` | 主体占比、景别一致、背景降噪 |
| 多人身份、发色、服装、动作互换 | `character-interaction.md` | 位置 + 角色 + 外观 + 动作绑定 |
| 俯视/仰视/POV/广角导致脸或肢体崩 | `perspective-camera.md` | 一个核心镜头、前中后景、脸部保护 |
| 逆光脸黑、背景过亮、景深抢主体 | `lighting-and-depth.md` | fill light、rim light、背景虚化和明暗分离 |
| 动作峰值不清楚、手脚粘连、武器遮脸 | `dynamic-action.md` | 主动作、方向留白、手/脸/道具可读性 |
| 色彩互相打架、主体融进背景 | `color-mood.md` | 冷暖/明暗分离，减少弱氛围词 |
| 大场景漂浮、环境抢戏、故事道具太多 | `environment-storytelling.md` | 地面接触、尺度参照、一个主故事 |
| 头身比、体型差、复杂服装吞结构 | `form-proportion.md` | 相对比例、服装遮挡、身体结构保护 |
| 服装材质或特殊设计表达不稳定 | `clothing-silhouette-reference.md` | 服装大轮廓、材质光泽、1-2 个关键细节 |
| 生成后不知道哪里不对 | `composition-judgment.md` | 快速判断主焦点、明暗、主体比例 |
| 上面都无法定位 | `composition-errors.md` | 失败模式 → 原因 → 修正句 |

## 常用修正句

这些句子是示例，不是固定模板。按画面只选需要的 1-3 句。

```text
Keep the face sharp and readable with a weak fill light.
Place the main subject in the center midground, not too small.
Keep foreground objects away from the face and hands.
Separate the two characters with clear spacing and distinct outfits.
Use a soft background blur so the environment does not overpower the face.
Add a visible ground contact shadow under the feet.
Keep the weapon silhouette clear without covering the eyes.
```

## 文件结构

```text
composition-case-studies/
  _index.md                         # 本文：失败症状路由，不是教材入口
  single-character.md               # 单人尺度、主体占比、背景降噪
  character-interaction.md          # 多人归属、视线、肢体关系
  perspective-camera.md             # 特殊镜头失败保护
  lighting-and-depth.md             # 光源、补光、景深、明暗分离
  dynamic-action.md                 # 动作方向、手脚、武器/道具可读性
  color-mood.md                     # 色彩分离与主体可读性
  environment-storytelling.md       # 场景尺度、落地、故事道具收敛
  form-proportion.md                # 比例、体型差、服装吞结构
  clothing-silhouette-reference.md  # 服装轮廓与材质表达
  composition-judgment.md           # 生成后判断
  composition-errors.md             # 通用错题集
```
