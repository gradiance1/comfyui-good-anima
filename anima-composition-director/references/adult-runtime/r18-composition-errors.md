# R18 Composition Errors / R18 构图错题集

> **R18 专项** — 仅限于 R18 场景的构图错误模式。通用构图错误参见 `composition-errors.md`。

---

## RE01：R18 局部特写，失去整体构图

### Failure Pattern（错误模式）

画面只有局部特写——胸部或股间的大特写——没有身体轮廓、没有表情、没有环境。虽然确实 R18 了但像医学解剖图。

### Correct Pattern（正确做法）

- 局部特写至少保留一个锚点：表情/手/身体曲线
- 经典的黄金组合：**局部 + 表情** 或 **局部 + 手部动作**
- 用 `close_up` + `face` 来保证至少脸和局部同框
- 纯局部特写只用于极少数场合（序列图中的插入格）

### Prompt Use

```
❌ 错：pussy close up, wet, glistening（医学解剖）
✅ 对：pussy close up, thighs framing, hand touching, flushed face visible at top edge
```

### Tags vs nltags

- Tag 控制尺度：`close_up` 比 `extreme_close_up` 安全
- nltags 补语境：「Show her glistening pussy in the lower frame, her flushed face visible above her heaving chest, one hand resting on her inner thigh」
- **基本原则**：局部必须附带全身的「一角」，给人想象整体

---

## RE02：R18 体位下身体弯曲超过人体极限

### Failure Pattern（错误模式）

交配位(mating press)、种子压、69 等折叠角度大的体位，角色的脊椎、颈椎或髋关节弯曲到人类不可能的角度。看起来像橡皮人。

### Correct Pattern（正确做法）

- 极限角度体位：用局部构图代替全身构图。不让模型画整个身体
- 全身展示时：选择角度不太极端的体位
- 如果必须全身+极端角度：nltags 写明「Keep the spine within natural human range of motion」
- 安全体位表：传教士/后入/骑乘位 > 火车便当/种付 > 极端折叠/全身压迫

### Prompt Use

```
❌ 错：mating press, full body, legs over head completely folded
✅ 对：mating press, upper body close-up, legs framing the shot, flushed face visible
```

### Tags vs nltags

- Tag：极限角度时不要硬推 `full_body`，改 `upper_body` 或 `close_up`
- nltags：「Show her upper body and face clearly. Her legs are folded close but her spine stays within a natural curve.」
- **金律**：如果你觉得这个动作你自己做不出来，模型大概率也画不对

---

## RE03：R18 体位选择导致面部不可见

### Failure Pattern（错误模式）

画面只有身体局部或背面，角色面部完全不可见。常见于後背位、背面騎乗位等角度，失去了表情这个最重要的情感锚点。

### Correct Pattern（正确做法）

- 选择能同时展示面部和局部的角度：
  - 传教士 → 正面/侧面/轻微仰视
  - 騎乗位 → 正面（展示胸+表情）
  - 后入 → 斜后方（展示臀+侧脸）
  - M 字开腿 → 正面平视
  - 对坐位 → 侧面（展示拥抱表情）
- 如果必须背面 → 用 mirror_view 或 over_shoulder 补面部
- 安全优先级：传教士/骑乘/对坐 > 后入斜角 > 纯背位

### Prompt Use

`❌ 错：doggystyle, from behind, ass focus, back view（看不到脸）
✅ 对：doggystyle, from behind, looking back, turned head, eye contact, side profile visible`

### Tags vs nltags

- Tag 控制角度：rom behind + looking back / urned head / eye_contact
- nltags 补面部：「Keep her face visible in the frame. Her head is turned back toward the viewer with eye contact.」
- **基本原则**：R18 构图必须同时回答「看到了什么」和「她什么表情」

---

---

## RE04：R18 POV 下身体部位归属混乱

### Failure Pattern（错误模式）

POV 场景中分不清画面中的手/身体部位属于谁。常见于自拍 POV、69、相互爱抚、scissoring 等肢体交织场景。

### Correct Pattern（正确做法）

- POV 必须包含至少一个「自己的身体锚点」：
  - male POV → own hands visible, bdomen, highs
  - female POV → own breasts, hands, highs
- 用位置关系锁定归属：手在前景 = 我的，对方在中景
- 69/scissoring 等相互场景 → 明确分区：上方身体 vs 下方身体
- 颜色/肤色区分：接触的两人如果有肤色差，会帮助模型理解归属

### Prompt Use

`❌ 错：POV, cowgirl, facing viewer（没有身体锚点，和普通视角没区别）
✅ 对：POV, first person perspective, own hands visible, cowgirl on top, facing viewer, intimate distance, self hands on her waist`

### Tags vs nltags

- Tag：「POV」+「self_hands_visible」/「own_body_in_frame」比纯「POV」安全 100 倍
- nltags 写死归属：「The viewer's hands are visible in the lower foreground. The partner is positioned above, her face and upper body clearly belonging to her, not the viewer.」
- **金律**：POV 场景如果看不到任何「自己的身体」，那就是第三人称

---

---

## RE05：R15-R17 暗示构图变成直接暴露

### Failure Pattern（错误模式）

用户要求 R15-R17（擦边/软色情），但 prompt 中的 tag 导致局部直接暴露，从「暗示」变成了「展示」，失去 R15-R17 特有的想象空间。

### Correct Pattern（正确做法）

- 使用 10 种「不展示」技法之一，必须有一个明确的「遮挡锚点」：
  1. **Hand Obstruction** → hand over pussy, hand covering breasts, inger peek
  2. **Limb Blocking** → legs crossed hiding pussy, rm covering chest
  3. **Shadow Play** → shadow over body, silhouette, dramatic shadow
  4. **Hair Cover** → hair covering nipples, hair between legs, wet hair on body
  5. **Object Obstruction** → pillow covering, lanket drape, owel on body
  6. **Angle Trick** → rom behind, op down view, over shoulder
  7. **Fabric Draping** → wet shirt, see-through, sheer fabric, ranslucent cloth
  8. **The Arch** → rched back, ent backward, spine curve, ecstasy pose
  9. **POV Crawl** → crawling toward viewer, POV, eye contact, coming closer
  10. **Suggestion Pose** → clothes slipping off, shoulder bare, skirt lift, unbuttoning
- R15-R17 黄金法则：
  1. 一张画让读者想象「前后故事」
  2. 「若隐若现」最强——完全隐藏=不色，完全展示=R18
  3. 表情就是一切（局部看不到时表情最重要）
  4. 用水·汗·湿润表现「正在此刻」

### Prompt Use

`❌ 错：1girl, lying on bed, naked, seductive, pussy visible（直接 R18）
✅ 对：1girl, lying on bed, sheet draped over body, one hand resting between thighs, wet hair covering chest, flushed face, looking at viewer, teasing smile`

### Tags vs nltags

- Tag 控制尺度：close_up 比 extreme_close_up 安全；遮挡物 tag 是 R15-R17 的必需品
- nltags 补语境：「Her body is mostly hidden beneath a thin white sheet. Only the curve of her shoulder and one hand are visible. Her face is the brightest element in the frame.」
- **核心原则**：遮挡物必须「自然」——是场景的一部分，不是后期打码

---

---

## RE06：3P/群交身体遮挡关系混乱

### Failure Pattern（错误模式）

三人及以上同框时，各角色身体部位（手/腿/头/躯干）层层堆叠，模型无法分配「谁的身体在哪里」。前后夹击时，中间层人物的身体轮廓消失，前景人物和背景人物的四肢混成"一团肉"。

### Correct Pattern（正确做法）

- 3P 构图最多写两组身体接触，不要链式关系
- 用 `depth of field` / `blur foreground` 区分近景和远景
- 夹击位：前景人物用 `silhouette` / `cowboy shot` 剪裁，中景主体清晰，后景虚化
- 安全人数上限：spitroast（前后夹击）= 3 人，但每个人只和另一个人身体接触
- **不要**写三人同时 `intertwined`，会出无法辨认的肉块

### Prompt Use

```
❌ 错：3boys, spitroast, intertwined, tangled, group sex, full body（一团肉）
✅ 对：spitroast, from side, depth of field, foreground silhouette, midground sharp, background blur, one girl between two boys
```

### Tags vs nltags

- Tag 只写人数+体位：`spitroast` / `triple penetration` 等
- nltags 写死空间：「One partner is in the foreground (out of focus), the main subject is in sharp midground, the third partner is a soft silhouette in the background.」

---

---

## RE07：体型差体位（小马大车/大人小孩）比例崩溃

### Failure Pattern（错误模式）

体型差异巨大的两人同框时，模型把两人画成相同身高。小个子悬吊在女性身上时被等比放大；大个子女性+小个子男性画成同尺寸的人。`考拉抱`/`背驮式`/`骑头式口交` 中比例完全失真。

### Correct Pattern（正确做法）

- 体型差体位必须用 nltags 写死比例关系：「The smaller character's head reaches the larger character's chest. Their feet do not touch the ground.」
- 安全角度：侧面平视最不容易比例崩坏（比正面好）
- 避免 `full body`——用 `medium shot` / `upper body` 裁剪掉腿部体差区域
- 安全体位：对坐位(Lotus) > 背后式 > 考拉抱 > 骑头式口交（越悬挂越危险）

### Prompt Use

```
❌ 错：onee-shota, full body, carrying, tall female short male（同尺寸）
✅ 对：onee-shota, upper body, tall female carrying small male, height difference, body size difference
```

### Tags vs nltags

- Tag：`height difference` / `size difference` / `onee-shota`
- nltags：「She stands nearly twice his height. His head reaches only to her chest. She lifts him easily, his feet dangling far above the ground.」

---

---

## RE08：足交/足责构图——脚部与身体归属混乱

### Failure Pattern（错误模式）

足交画面中脚的归属不明确。正面足交时，女性的脚出现在画面下方但模型不清楚脚与身体的距离；背面足交时，脚从背后伸出但身体轮廓模糊。双人足交中四只脚同时出现，完全分不清谁是谁。

### Correct Pattern（正确做法）

- 正面足交+POV：画面中必须包含女性小腿的一段作为连接，不能只有脚
- 背面足交：用 `looking back` / `over shoulder` 让女性转脸，面部锚定归属
- 双人足交：只画两位女性的脚，不要画身体——用明确的画面裁剪
- 最佳角度：侧面（`from side`）展示脚 → 腿 → 身体 → 脸的全连接

### Prompt Use

```
❌ 错：footjob, POV, soles only（不知道谁的脚）
✅ 对：footjob, from side, one girl lying on stomach, soles visible, looking back, legs connected to body
```

### Tags vs nltags

- Tag：`footjob` + `from side` + `feet focus`（需要至少一个体态锚点）
- nltags：「Her feet press together around him, her legs stretching back to her body visible in the frame. She looks back over her shoulder with a teasing smile.」

---

---

## RE09：反向体位——"谁在上谁在下"朝向迷失

### Failure Pattern（错误模式）

传统体位被反转时（亚马逊位/反向坐臀/反女牛仔），模型对重力方向和身体上下关系混乱。`Amazon` 体位中男性双腿被抬起但头朝下，模型经常把男性画成正躺而非仰卧腿被抬起。`反向坐臀式` 中两人可能被画成同一朝向。

### Correct Pattern（正确做法）

- 反向体位必须在 nltags 中明确朝向
- 相机角度选侧面（`side view`），比正面/背面安全
- 至少保留一个"正向锚点"：能看到一个人的面部表情来确认朝向
- nltags：「The male faces away from her head, descending onto her raised pelvis while she lies supine beneath him. Her legs are lifted and folded.」

### Prompt Use

```
❌ 错：amazon position, full body（姿势混乱，两人朝向不明）
✅ 对：amazon position, side view, female on top, male lying on back, legs lifted, facing upward
```

### Tags vs nltags

- Tag 只给体位名称（`amazon` / `reverse lotus`），不给身体朝向假设
- nltags 明确朝向和重力：「She straddles him from above in reverse. He lies on his back with his legs raised. Her back faces his face.」

---

---

## RE10：多人非插入性交互——距离感崩坏

### Failure Pattern（错误模式）

以手/乳/发为"连接物"的交互中，连接物的远近关系完全丢失。双人乳交中乳房应紧贴阴茎，但模型画成乳房和阴茎不在同一深度层——乳房在远景、阴茎在前景。舔耳手交中嘴在耳旁但手却在画面另一侧。

### Correct Pattern（正确做法）

- 非插入交互：减少参与者数量（2 人最佳，3 人高危）
- 连接物的远近关系用 `close-up` + nltags 写死
- 如果必须 2 人+手/乳同时交互 → 侧面角度优先
- **不要**用 `group sex` / `orgy` 来触发多人非插入——会随机画一堆人

### Prompt Use

```
❌ 错：paizuri, blowjob, group sex, multiple girls（乳房和嘴不在同一深度）
✅ 对：paizuri, close-up, from side, both breasts pressed around shaft, lips at tip, one girl
```

### Tags vs nltags

- Tag 只写交互媒介+人数：`paizuri` + `1girl` 或 `handjob` + `from side`
- nltags：「Both breasts are pressed tightly around the shaft at the same depth. Her lips close over the tip in the same focal plane.」

---

---

## RE11：悬吊/抱持体位——重力锚点缺失

### Failure Pattern（错误模式）

女性被完全抱离地面时，模型不理解"全身重量由男性手臂支撑"→ 女性悬浮空中或男性手臂穿过身体。全纳尔逊位中膝盖折叠到肩附近，但模型把大腿画成不可能角度（髋关节错位）。

### Correct Pattern（正确做法）

- 悬吊体位必须有明确重力锚点：男性手臂托臀部时臀部须有按压痕迹（nltags 写明）
- 全纳尔逊位：侧面+锁死髋关节角度
- 立式六九：nltags 写「legs wrap around neck for stability, spine stays natural」
- **安全规则**：如果你觉得这个动作现实中没健身的人做不出来，就别让模型画全身

### Prompt Use

```
❌ 错：suspended congress, full body, from front（悬浮无支撑）
✅ 对：suspended congress, from side, upper body, female legs wrapped around male waist, arms around his neck
```

### Tags vs nltags

- Tag 只给体位名称：`suspended congress` / `full nelson`
- nltags 写死重力：「Her full weight rests in his arms. His hands press into her thighs, creating visible indentations. Her legs wrap around his waist for stability.」

---
