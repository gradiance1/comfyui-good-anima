# Environment Storytelling / 场景叙事构图案例

## 核心认知

「背景」不是废纸。好的背景帮你讲故事，坏的背景抢主角戏。目标是：**背景足够说明场景，但不值得单独看。**

---

### Pattern 1：场景锚点 (Scene Anchor)

**Wrong Pattern**

- 场景要素太多 → 背景抢戏
- 场景要素太少 → 不知道在哪（白色虚空）
- 场景要素矛盾 → 教室里有沙滩椰子树

**Correct Prompt Control**

```
cafe, coffee cup on table, window beside,
soft daylight through window, simple interior,
blurred background, focus on girl
```

- **关键**：只选 2-3 个场景锚点，不要多
- **tag 不要** `detailed_background` + 长串场景描述

### Pattern 2：天气叙事

**Wrong Pattern**

- 写了下雨但衣服是干的 → 逻辑矛盾
- 写了夕阳但阴影方向是中午的 → 物理矛盾
- 天气 tag + 室内场景 → 窗外有雨但室内也下雨

**Correct Prompt Control**

```
# 雨天
rain, wet street, umbrella, water droplets on window,
gray tone, soft light, melancholic atmosphere
```

```
# 雪天
snow, white landscape, warm scarf, breath visible,
soft diffused light, quiet atmosphere
```

- **关键**：天气必须影响画面元素（湿发/积雪/逆光）
- **不推荐**：室内 + 室外天气 tag 同时强推

### Pattern 3：前中后景三层

**Wrong Pattern**

- 只有中景和背景 → 画面扁平
- 前景物体太大/太清晰 → 变主体
- 三层在同一焦距 → 没有层次

**Correct Prompt Control**

```
foreground: blurred flowers, midground: girl standing,
background: sunset city skyline,
depth between layers, focus on girl
```

- **关键**：nltags 写三层分配，tag 只能辅助
- **Tag 用**：`depth_of_field` + `layered_composition`

### Pattern 4：镜越构图 (Mirror Reflection)

**Wrong Pattern**

- 镜中反射角度不对 → 物理 bug（应该看到 A 但看到 B）
- 镜框/镜面脏 → 抢眼
- 镜中脸和现实脸表情不一致 → 像两个人

**Correct Prompt Control**

```
mirror view, reflection, facing mirror,
back turned to viewer, face visible in mirror,
soft bathroom lighting, steam
```

- **R18 特殊**：`mirror_view` + `from_behind` = 背面+脸+局部同时展示
- **物理检查**：nltags 写清楚谁站在哪、镜子里应该看到什么

---

### Pattern 5：比例锚点 (Scale Anchor)

**Wrong Pattern**

- 锚点太模糊：只说「room」不说里面有什么家具
- 锚点反效果：「她站在小桌子旁」→ 桌子变正常大小，她变小了
- 无锚点 + 远全景 → 人物变成背景里的一个小点

**Correct Prompt Control（锚点写法）**

```
1girl, full body, standing in doorway,
door frame at head height, desk beside her at waist level,
classroom chairs visible behind her
```

- **关键**：锚点 + 位置关系。不是两个独立 tag，是「X 在 Y 的什么位置」
- **安全检查**：一个人物至少有一个锚点。两个人物的场景各写一个锚点

### Pattern 6：内外光不连续 (Interior/Exterior Light Breach)

**Wrong Pattern**

- 室内和室外亮度和色温完全一致 → 像背景板贴在玻璃上
- 写了「透过窗户看到夜景」但室内灯光把窗外反光全消了

**Correct Prompt Control**

```
# 室内昏暗+窗外明亮（日式常见）
dim interior, bright window, sunlight streaming through,
shadowed figure, silhouette against window

# 室内温馨+窗外夜景（韩式常见）
warm interior light, night view through window,
cozy room, city lights visible, contrapposto lighting
```

- **规则**：室内外光要明确分出层级。谁亮谁暗，为什么

---

### Pattern 7：负空间的叙事力 (Negative Space as Storytelling)

**Wrong Pattern**

- 负空间太多+没有焦点 → 像抠图素材
- 负空间+亮色背景 → 失去沉重感
- 人物太小+没有锚点 → 看不出来在干什么

**Correct Prompt Control**

```
small figure, vast empty space, silent atmosphere,
negative space composition, lonely figure,
wide shot, distant view, solitary, endless sky
```

- **比例**: 人物占画面 5-15% = 孤独/自由感；>30% = 回到普通构图
- **色**: 冷色 = 孤独、暖色 = 希望/自由

### Pattern 8：框中框 (Frame within Frame)

**Wrong Pattern**

- 框太大/太小 → 框失去了约束功能
- 框内和框外的亮度和色彩完全一致 → 框失了区别能力
- 框的边缘不清晰 → 像污损

**Correct Prompt Control**

```
frame within frame, looking through doorway,
window framing, archway framing,
tunnel view, through leaves, silhouette frame
```

- **关键**: 框内=亮+细节、框外=暗+模糊。或者反之。
- **不要**: 框和主体用相同的对比度

---

### Pattern 9：R15-R17 暗示构图（The Art of NOT Showing）

**Wrong Pattern**

- 完全遮挡 → 不知道在干什么，失去性感
- 完全暴露 → 变成 R18，失去 R15-R17 的定位
- 遮挡物太突兀 → 像故意打码
- 遮挡物没有和场景融合 → 像后期处理的 censorship

**Correct Prompt Control**

| 技法               | 中文     | 说明                                     | 核心 tag                                              |
| ------------------ | -------- | ---------------------------------------- | ----------------------------------------------------- |
| Hand Obstruction   | 用手遮挡 | 用手遮挡局部或乳头。指缝间隐约可见是关键 | hand over pussy, hand covering breasts, finger peek   |
| Limb Blocking      | 用肢体遮 | 用大腿或手臂遮挡局部                     | legs crossed hiding pussy, arm covering chest         |
| Shadow Play        | 用影遮   | 用灯光只把局部打暗。影子的剪影强调形状   | shadow over body, silhouette, dramatic shadow         |
| Hair Cover         | 用发遮   | 用长发覆盖乳头或胯间                     | hair covering nipples, hair between legs              |
| Object Obstruction | 用物遮   | 用枕头·被子·椅子·桌子等遮挡局部          | pillow covering, blanket drape, towel on body         |
| Angle Trick        | 用角度遮 | 背后·正上·斜向等让局部自然被裁掉         | from behind, top down view, over shoulder             |
| Fabric Draping     | 用布透   | 薄布·衬衫·蕾丝透出肌肤                   | wet shirt, see-through, sheer fabric, translucent     |
| The Arch           | 弓背     | 后仰姿势。让人感受性能量但看不到局部     | arched back, bent backward, spine curve, ecstasy pose |
| POV Crawl          | POV 爬行 | 向镜头爬来的构图。眼神交汇+唇部性感      | crawling toward viewer, POV, eye contact              |
| Suggestion Pose    | 暗示姿势 | 捕捉「正打算脱」的瞬间                   | clothes slipping off, shoulder bare, skirt lift       |

**R15-R17 黄金法则**

1. 一张画让读者想象「前后故事」
2. 「若隐若现」最强——完全隐藏=不色，完全展示=R18
3. 表情就是一切（局部看不到时表情最重要）
4. 用水·汗·湿润表现「正在此刻」

**Tag 示例**

```text
# 用手遮挡 + 开腿
hand over pussy, legs spread wide, one hand resting between thighs,
flushed face, looking at viewer, wet hair

# 透过布料 + 透出
wet shirt, see-through fabric, nipple outline visible through cloth,
looking back over shoulder, teasing smile, water droplets

# 影 + 背後
silhouette, backlit, shadow over body, from behind,
soft window light, shape visible but detail hidden, turned head
```

**nltags 示例**

```text
「She sits with her legs spread wide, one hand resting delicately between her thighs.
Her fingers barely hide what lies beneath. Her eyes are half-lidded and inviting.」

「A thin white shirt clings to her skin, soaked through and nearly transparent.
The fabric traces every curve, but nothing is fully revealed.」
```

**关键**：遮挡物必须「自然」——是场景的一部分，不是后期打码。

---

### Pattern 10：体位决定空间 (Position-Dictated Space)

**Wrong Pattern**

- 宽画幅塞竖立站抱 → 大量无用留白
- 窄竖幅塞横向展开的后入 → 手肘/头被裁出画框
- 极端近距离体位用全身构图 → 失去亲密感

**Correct Prompt Control**

- 后入/横向体位 → canvas 1536×1024 (3:2)
- 站抱/竖立体位 → canvas 1024×1536 (2:3)
- 坐脸/极端近距 → 配合 close-up + 1:1 画框
- nltags 不需要写体位-空间匹配，这由 canvas 参数控制

---

### Pattern 11：空间压迫叙事 (Space as Oppression)

**Wrong Pattern**

- 压迫空间用广角 → 空间显大，压迫感丢失
- 开放羞耻空间没有旁观者 → 失去"被看"的紧张
- 空间大小和人物情绪不匹配 → 叙事矛盾

**Correct Prompt Control**

- 压迫空间：nltags 明确视觉压迫源——「The low ceiling presses down, leaving only a narrow strip of breathing room above her head.」
- 开放羞耻：nltags 写旁观者——「Strangers in the background glance her way, some pretending not to notice.」
- 空间反差：nltags 写对比——「She sits on silk sheets in the luxury suite, while through the shattered window, the ruined city smolders.」

---

### Pattern 12：水作为感官增强介质 (Water as Sensory Medium)

**Wrong Pattern**

- 水中+干爽头发 → 物理矛盾
- 水汽+锐利边缘 → 画面语言冲突
- 暴雨+静态发型 → 失去动态感

**Correct Prompt Control**

- 水下身体：`underwater` + nltags「Her body blurs and ripples beneath the water surface, the edges softened by refraction.」
- 淋浴间：`shower, steam, wet skin` + nltags「Steam fills the small shower stall, softening every edge. Water trails down her skin, catching the light.」
- 暴雨户外：`rain, wet clothes, see-through` + nltags「Rain plasters her clothes to her body, every contour visible through the soaked fabric.」

---

### Pattern 13：公共与私密的边界博弈 (Public-Private Threshold)

**Wrong Pattern**

- 纯私密无风险 = 平淡
- 纯公共无隐匿 = 无法叙事
- 隐藏空间中没有"被发现线索" = 失去紧张感

**Correct Prompt Control**

- 公私双层：nltags「Above the table, she maintains a calm smile for the dinner guests. Below, unseen by anyone, her hand traces along his thigh.」
- 可被闯入：nltags「The fitting room curtain hangs slightly open—just a crack. Through it, the busy store is visible. She holds her breath.」
- 被迫暴露：nltags「The spotlight pins her to the stage. Hundreds of eyes in the darkened auditorium watch her every move.」

---

### Pattern 14：时间锚点叙事 (Temporal Anchor)

**Wrong Pattern**

- 深夜场景+全亮度 = 失去时间锚
- 停电场景+多个光源 = 矛盾
- 紧迫场景+慵懒表情 = 叙事冲突

**Correct Prompt Control**

- 深夜：`night, dark room, dim lighting` + nltags「Only the pale glow of moonlight through the window illuminates her silhouette.」
- 黎明：`dawn, early morning, cold light` + nltags「The first grey light of dawn seeps through the curtains. She stirs, still half-asleep, her form soft and unfocused.」
- 停电：`power outage, candlelight, dark room` + nltags「A single candle flickers on the nightstand. Everything beyond its small circle of light is swallowed by absolute darkness.」
- 演出后台：`dressing room, backstage, mirror reflection` + nltags「The countdown clock on the wall reads 3:00. Half of her stage makeup is still undone. Her hands move faster than her reflection can follow.」
