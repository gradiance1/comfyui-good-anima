# Perspective & Camera / 透视与镜头构图案例

## 核心认知

透视不是 tag 能完全解决的问题。Tag 告诉模型「从哪看」，但 nltags 告诉模型「看到什么」。

---

### Pattern 1：低角度仰视（Low Angle）

**Wrong Pattern**

- 极端仰视 → 鼻孔见光死
- 仰视 + 低头 → 双下巴 + 脸崩
- 仰视 + 复杂背景 → 透视线的冲突

**Correct Prompt Control**

```
1girl, from below, looking down at viewer, slight low angle,
confident expression, chin up, simple background
```

- **强度**：`slight low angle` > `low angle` > `extreme low angle`
- **安全**：配合 `looking down at viewer` 让面部朝向镜头
- **不要配**：`looking up` + `from below` = 脖子折叠

### Pattern 2：高角度俯视（俯瞰）

**Wrong Pattern**

- 俯视 + 低头 → 只看到头顶和发旋，表情全丢
- 极端俯视 → body proportion 崩坏（头大身小过度）
- 俯视 + 站姿 → 头肩比异常

**Correct Prompt Control**

```
1girl, from above, lying on bed, looking up at viewer,
high angle, soft expression, messy hair, pillow
```

- **关键**：俯视时一定要让主体 `looking up` 或至少露出眼睛
- **配合**：`bed` / `floor` / `mat` 等水平面道具来强化俯视感

### Pattern 3：过肩镜头 (Over-the-Shoulder / OTS)

**Wrong Pattern**

- 前景肩膀太清晰 → 抢焦
- 前景肩膀挡了对面人物的脸
- 两个人在同一条视线上 → 只能看到后脑勺

**Correct Prompt Control**

```
over-the-shoulder, blur foreground shoulder,
focus on facing girl, eye contact, conversation,
depth of field, shallow focus
```

- **关键**：`blur_foreground` + `depth_of_field` 让前景模糊
- **R18 特殊**：OTS + 局部入镜 = 绝妙擦边构图

### Pattern 4：广角/鱼眼透视

**Wrong Pattern**

- 人物在画面边缘 → 被拉伸变形（脸歪手长）
- 多条透视线冲突 → 画面混乱
- 广角 + 多人 → 边缘的人全变形

**Correct Prompt Control**

```
fisheye lens, wide angle, center focus,
dynamic action pose, exaggerated perspective,
1girl only, center frame（多人不要用）
```

- **警告**：广角 + 多人 = 灾难，只建议单人用
- **安全**：主体放中心、背景简单、不要有直线图案（如格子墙）

### Pattern 5：主观视角 (POV)

**Wrong Pattern**

- POV + 看不到自己的身体部分 → 和普通视角没区别
- POV + 静态场景 → 为什么要 POV？

**Correct Prompt Control**

```
POV, first person perspective,
own hands visible, reaching out,
facing partner, intimate distance
```

- **关键**：POV 必须包含 `own_body_in_frame` / `self_hands_visible`
- **R18 用**：`POV` + `self_hands_visible` + 局部描写

---

### Pattern 6：荷兰角 / 倾斜构图 (Dutch Angle / Canted Shot)

**Wrong Pattern**

- 倾斜角度太大（>20 度）→ 读者脖子痛，失去美感
- 倾斜+平静场景 → 像手机没拿稳
- 荷兰角+多人对称 → 眩晕

**Correct Prompt Control**

```
dutch angle, tilted frame, slightly tilted composition,
uneasy atmosphere, distorted perspective,
one girl standing, confident expression
```

- **强度**：`slightly_tilted` > `dutch_angle` > `extreme_tilted`
- **安全**：单人、简单背景、放松的姿势
- **不要配**：对称构图、多人、建筑摄影

### Pattern 7：强制透视 / 夸张近大远小

**Wrong Pattern**

- 放大的部位直接把远处的人物全挡住了
- 反差太大 → 背景人物变成火柴人
- 强制透视 + 多人 → 其他人变成怪胎比例

**Correct Prompt Control**

```
exaggerated perspective, foreground dominant,
hand stretched toward camera, distant body visible,
dramatic foreshortening, wide angle lens
```

- **关键**：只有一个前景放大物+一个背景主体
- **Tag**：`wide_angle_lens` + `dramatic_foreshortening`
- **安全**：前後关系通过 nltags 写死

---

### R18 POV 子模式

**Pattern 5a：上方 POV（骑乘位）**

**Wrong Pattern**

- 上方 POV 但女性不 facing viewer → 只看到头顶和发旋
- 没有 own body visible → 和普通仰视角没区别

**Correct Prompt Control**

```
POV, first person perspective, from below, cowgirl_position,
facing viewer, own body visible, intimate distance, breasts in frame
```

- **关键**：from below + facing viewer + own body visible
- **Tag**：self_hands_visible + cowgirl_position

---

**Pattern 5b：下方 POV（传教士）**

**Wrong Pattern**

- from below + 女性 looking up → 下巴和鼻孔见光死
- 极端低角度 → 脸崩（E003）

**Correct Prompt Control**

```
POV, first person perspective, from below, missionary,
legs over shoulder, looking down at viewer, own thighs visible
```

- **关键**：from below + looking down at viewer（女性俯视镜头）
- **Tag**：legs over shoulder + looking down at viewer

---

**Pattern 5c：背后 POV（后入）**

**Wrong Pattern**

- 没有 own hips/thighs visible → 和普通背面视角没区别
- 只有臀 → 像第三人称的背后角度

**Correct Prompt Control**

```
POV, first person perspective, from behind, doggystyle,
ass up, own hips visible, reaching out
```

- **关键**：POV + from behind + own body in frame
- **nltags**：「The viewer's hips and hands are visible in the lower frame. The partner is on all fours in front, her back and ass clearly belonging to her.」

---

**Pattern 5d：面部 POV（口交/坐脸）**

**Wrong Pattern**

- 面部 POV 但看不到女性表情 → 失去情感连接
- 只有局部没有脸 → 像医学视角

**Correct Prompt Control**

```
POV, first person perspective, facesitting, from below,
smother, looking down at viewer, intimate distance
```

- **关键**：POV + from below + facesitting + looking down
- **安全**：配合 looking down at viewer 保证面部可见

---

**Pattern 5e：自拍 POV**

**Wrong Pattern**

- 只有局部没有表情 → 医学解剖感
- 只有表情没有局部 → 普通互动
- 手/身体部位归属不明 → E015

**Correct Prompt Control**

```
POV, first person perspective, penetration visible,
partner face visible, close intimate, eye contact
```

- **关键**：POV + insertion visible + partner face visible
- **Tag**：first person perspective + close intimate
