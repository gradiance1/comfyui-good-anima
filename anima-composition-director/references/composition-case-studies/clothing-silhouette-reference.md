# Clothing Silhouette & Material Reference / 服装轮廓与材质参考

> **T3 Runtime 参考** — 只在需要精确控制服装轮廓、材质光照、遮挡风险或特殊服装结构时读取。
> 本文件不决定构图主题，只帮助把服装需求转换成 Anima 更容易理解的 tag anchor 与自然语言控制句。

---

## 使用边界

Anima 同时理解 Danbooru-style tags 和自然语言 captions。服装相关 prompt 必须遵守项目共享规范：

- 普通 tag 使用小写空格：`red hair`、`school uniform`、`high slit`。
- 不把普通 tag 写成下划线形式；`score_7` 这类质量 tag 除外。
- 不确定是否稳定的复合概念，优先写入 `nltags` 自然语言。
- 服装、材质、光线不要重复表达；同一语义在 tag 和 nltags 里二选一。
- R18 服装可以保留，但描述必须服务画面结构，不写情绪暗示或隐喻。

## 核心原则

1. **服装先控制轮廓**：先决定贴身、宽松、硬块面、垂坠或飘动，再决定材质细节。
2. **材质依赖光线可见**：乳胶、皮革、丝绸、薄纱都需要对应高光、背光或边缘光。
3. **遮挡必须显式处理**：宽袖、大帽子、披风、拖尾容易吞脸、手、腰线和腿部动作。
4. **特殊设计用短句锁定位置**：开叉、镂空、拉链、绳衣等结构要说明位置和可见边缘。
5. **比例优先于细节**：服装再复杂，也不能牺牲脸、手、躯干方向和关节可读性。

---

## 一、服装轮廓类型

### 1.1 贴身类

**控制目标**：贴合身体边缘，强调胸腔、腰线、髋部和四肢方向。

**常用 anchor**：

```text
bodysuit, catsuit, skin tight, bodycon, form fitting
latex, leather, glossy, shiny, wet look
```

**nltags 示例**：

```text
The outfit follows the torso and hips without hiding the body structure.
Use a thin rim light to separate the dark fabric from the background.
Keep the waist and shoulder direction readable through the fitted fabric.
```

**常见风险**：

- 深色贴身衣 + 深背景 → 身体边缘丢失。
- 高反光材质 + 扭转姿势 → 高光可能误导关节方向。
- 远景里材质不可读 → 改用中景或增加边缘光。

### 1.2 束腰 / 沙漏类

**控制目标**：强化上半身支撑、腰部收束和胸腰髋比例。

**常用 anchor**：

```text
corset, bustier, cinched waist, narrow waist, hourglass figure
```

**nltags 示例**：

```text
The corset narrows the waist while keeping the torso structurally believable.
The bust and hips remain balanced around the tightened waistline.
Keep the lacing centered and aligned with the body axis.
```

**常见风险**：

- `wasp waist` 容易让腰断裂，除非用户明确要极端比例。
- 腰部过细时，必须用自然语言要求“比例仍然可信”。

### 1.3 宽松 / 层叠类

**控制目标**：用布料体积和垂坠方向扩展角色外轮廓。

**常用 anchor**：

```text
loose clothing, oversized, layered clothing, robe
wide sleeves, long sleeves, flowing fabric, billowing fabric
```

**nltags 示例**：

```text
The loose outer layer expands the silhouette without covering the face.
The sleeves hang away from the hands, leaving the fingers visible.
The fabric folds downward and reveals the body direction underneath.
```

**常见风险**：

- 宽袖吞手 → 写清手部露出。
- 大帽子遮脸 → 写清脸部无遮挡。
- 多层衣物遮腰线 → 用光或腰带找回身体方向。

### 1.4 硬块面 / 重甲类

**控制目标**：用肩甲、胸甲、披风、外套表现体量，不依赖肌肉 tag。

**常用 anchor**：

```text
armor, shoulder armor, breastplate, gauntlets
long coat, cape, cloak, heavy coat
```

**nltags 示例**：

```text
The shoulder armor widens the upper silhouette without enlarging the head.
The cape falls behind the body and does not cover the arms.
Use hard side light to separate each armor plate clearly.
```

**常见风险**：

- 盔甲堆太多 → 手臂和腰线消失。
- 披风前飘 → 吃掉腿部和武器。
- 肩甲过大 → 头显得异常小。

---

## 二、材质与光线

### 2.1 光泽度

| 光泽等级 | 视觉目标           | 常用 anchor                                  | 推荐自然语言                                                     |
| :------- | :----------------- | :------------------------------------------- | :--------------------------------------------------------------- |
| 哑光     | 不反光，边缘柔和   | `matte`, `cotton`, `canvas`                  | The fabric absorbs light and shows soft edges.                   |
| 柔光     | 有轻微高光         | `silk`, `satin`, `soft sheen`                | The fabric catches soft highlights along the folds.              |
| 高光     | 强烈反射，边缘清楚 | `glossy`, `shiny`, `latex`, `patent leather` | Bright highlights trace the curves and outer edges.              |
| 半透     | 透光但不抢主体     | `sheer`, `translucent`, `tulle`, `mesh`      | Backlight passes through the fabric and outlines the silhouette. |

### 2.2 常见材质处理

| 材质 | 构图价值       | 风险         | 控制方式                 |
| :--- | :------------- | :----------- | :----------------------- |
| 乳胶 | 高光勾身体边缘 | 反光吃掉结构 | 用边缘光和暗背景分离轮廓 |
| 皮革 | 稳重、硬边缘   | 黑皮革容易糊 | 加侧光或局部高光         |
| 丝绸 | 柔软垂坠       | 褶皱可能乱   | 用长线条描述垂坠方向     |
| 蕾丝 | 层次和花纹     | 花纹抢脸     | 限制到局部或用浅景深     |
| 薄纱 | 透光、轻量     | 层数多会糊   | 用背光控制外轮廓         |
| 渔网 | 网格节奏       | 网格切碎身体 | 近景使用，避免远景全身   |
| 金属 | 强块面和高光   | 环境反射混乱 | 简化背景，保留硬边缘     |

**材质 nltags 示例**：

```text
The latex reflects a narrow highlight along the shoulder and waist.
The silk folds downward and shows the weight of the fabric.
The sheer fabric is backlit, but the body outline remains clear.
The leather edges catch side light without blending into the background.
```

---

## 三、服装作为构图控制器

### 3.1 大衣 / 披风 / 长外套

**控制目标**：扩展肩背和垂直感，稳定男性、王族、骑士、反派等角色轮廓。

**控制句**：

```text
The long coat extends the vertical silhouette without covering the legs.
The cape spreads behind the shoulders and leaves both hands visible.
The hem follows the standing pose and does not hide the feet.
```

**风险**：

- 披风遮住武器或手。
- 外套下摆吞掉腿部动作。
- 肩背扩展过度导致头显小。

### 3.2 宽袖 / 大帽子 / 头纱

**控制目标**：适合小体型、魔法、宗教、婚礼或神秘角色，但必须保护脸和手。

**控制句**：

```text
The wide sleeves frame the body while keeping both hands visible.
The large hat sits above the face and does not cover the eyes.
The veil is translucent and keeps the facial features readable.
```

**风险**：

- 袖子吃掉手势。
- 帽檐遮眼，表情丢失。
- 头纱与头发混成一团。

### 3.3 腰带 / 围裙 / 背带

**控制目标**：在宽松服装里找回腰线和身体方向。

**控制句**：

```text
The belt marks the waistline clearly under the loose outer layer.
The apron divides the torso and skirt without hiding the body axis.
The straps follow the chest direction and help show the torso angle.
```

**风险**：

- 围裙比例过大，角色变成矩形。
- 腰带位置错误，造成上下身比例崩。

---

## 四、特殊设计与 R18 服装结构

> 本节包含 R18 服装的直接描述和对应 prompt 写法。
> 安全等级在上层安全 tag 中设置：`safe` / `sensitive` / `nsfw` / `explicit`。

### 4.1 高开叉

**控制目标**：把视线引向腿部动作和裙摆边缘。`high slit` + `side view` 是最稳定的组合。

**常用 anchor**：

```
high slit, side slit, long dress, thigh exposed
```

**nltags 示例**：

```
The side slit opens along one leg and follows the standing pose.
The fabric edge stays clean and does not distort the hip.
Keep the visible leg connected naturally to the body.
```

**风险**：

- 正面站姿看不到开叉结构
- 开叉过高时髋部边缘容易崩
- 双腿大幅分开会产生不自然三角区域

### 4.2 露背

**控制目标**：把视觉焦点转移到肩胛骨、背部线条和回头动作。

**常用 anchor**：

```
backless dress, bare back, from behind, looking back
```

**nltags 示例**：

```
The open back reveals the shoulder blades from a rear angle.
The dress edge follows the spine and lower back cleanly.
Use side light to separate the back from the background.
```

### 4.3 镂空

**控制目标**：用局部开口建立视觉锚点，常见于胸口、腰侧、背部或腿部。

**常用 anchor**：

```
cutout dress, chest cutout, side cutout, waist cutout
```

**nltags 示例**：

```
The cutout exposes a small area while keeping the torso shape clear.
The fabric edge follows the body curve without breaking anatomy.
Limit the cutouts to one or two clear focal points.
```

### 4.4 开裆 / 拉链结构

**控制目标**：特殊服装结构，需要明确位置、遮挡和姿态限制。

**常用 anchor**：

```
open crotch, crotch zipper, easy access, bodysuit
```

**nltags 示例**：

```
The garment has a controlled opening aligned with the body centerline.
The crotch area is open, exposing the skin between the legs.
Use a simple seated or standing pose to keep the structure readable.
```

**风险**：

- 复杂姿势会让布料边缘和骨盆结构混乱
- 远景里结构不可读，容易变成随机开口
- 必须避免让服装结构破坏人体比例

### 4.5 绳衣 / 束缚结构

**控制目标**：用绳线分割身体平面，形成节奏和方向。红色 = 日式绳艺，黑色/白色 = 西式时尚。

**常用 anchor**：

```
rope harness, shibari, rope pattern, tied up, red rope
```

**nltags 示例**：

```
The ropes form clear diagonal lines across the torso.
The rope pattern follows the body surface without cutting anatomy apart.
Keep the hands, shoulders, and waist readable between the rope lines.
```

**风险**：

- 绳线太密会切碎身体
- 绳线穿过关节会造成断肢感
- 深色背景下黑绳不可读

### 4.6 露出服装 / 人体彩绘

**核心**：「反衣服」——通过减少布料、透明化或直接在皮肤上作画，让身体本身成为视觉主体。

**常用 anchor**：

```
naked apron, apron only, nude, back view, bare ass, see-through, wet shirt, nipples visible, body painting, painted torso, pasties, thong, g-string
```

**nltags 示例**：

```
She wears only a small apron tied around her waist. Her back and buttocks are completely bare.
The soaked white shirt turns translucent against her skin. Her nipples are clearly visible through the wet fabric.
The body paint follows the contours of her chest and hips instead of real clothing.

```

**各类型风险**：

| 类型     | 风险                    | 控制方式                         |
| :------- | :---------------------- | :------------------------------- |
| 裸体围裙 | 围裙遮腰线，角色比例崩  | 围裙系在腰上，从背后拍           |
| 透湿衬衫 | 透明度和肤色冲突        | 硬光背光，强调湿透质感           |
| 人体彩绘 | 图案被关节拉伸变形      | 用 `body painting` 显式锁定      |
| 极致露出 | 遮挡不足，NSFW 级别过高 | 明确 `pasties` / `g-string` 位置 |
| 绑带装   | 绑带太细切碎身体        | 限制绑带宽度和数量               |

**完整 prompt 示例 — 裸体围裙**：

```
tags: 1girl, cat ear maid, naked apron, apron only, back view, bare ass, thigh highs, looking back at viewer

nltags: She wears nothing but a tiny frilled apron tied around her waist and long white thigh-highs. From behind, the apron leaves her back and buttocks completely exposed. She glances back with a teasing smile.
```

**完整 prompt 示例 — 透湿白衬衫**：

```
tags: 1girl, wet look, white shirt, see-through, completely soaked, nipples visible, rain, wet hair, standing, garden

nltags: Her thin white shirt is plastered to her skin by the rain, the soaked cotton turning translucent. Her nipples are clearly visible through the fabric. Water drips from the hem down her thighs.
```

### 4.7 触手服 / 生物紧身衣

**核心**：一种半自主的生物共生体服装，没有拉链，靠主动缠绕贴合身体。在 Anima 中，触手服的关键是表面纹理（吸盘/鳞片）+ 生物发光 + 动态触手不遮脸。

**常用 anchor**：

```
symbiont, tentacle suit, living clothing, organic texture, bioluminescent, tentacle hair, suction cups, glowing lines, writhing tentacles
```

**nltags 示例**：

```
A living suit of dark organic material pulses against her skin. Bioluminescent lines trace across her chest and thighs like veins. Several tendrils extend from her back, moving independently.
The suction cups along her sides are faintly visible in the light.
The tentacle suit clings to every curve but does not cover her face or hands.
```

**风险**：

- 触手和头发混在一起 → 加 `tentacle hair` / `hair tentacles` 区分
- 触手太多挡住身体 → 限制数量，删 `too many tentacles`
- 吸盘纹理被统一色调吃掉 → 用自然语言写吸盘具体位置
- 生物发光和环境光冲突 → 发光色 + 环境光取同一色系

**完整 prompt 示例 — 触手服共生体**：

```
tags: 1girl, tentacle suit, symbiont, living clothing, bioluminescent, pink and black, glowing lines, suction cups, tentacle hair, standing, legs apart, dark background, rim light

nltags: A living suit of dark organic material pulses against her skin, bioluminescent pink veins running across her chest and thighs. Several tendrils extend from her lower back, moving as if alive. The suit clings to every contour, the suction cups faintly visible along her sides.
```

### 4.8 拘束服装 / 束缚装

**核心**：通过物理限制改变或固定身体姿态。「被限制」的张力感是核心视觉语言。

**各类型速查**：

| 类型       | 姿态限制             | 光线偏好                | 常用 anchor                                            |
| :--------- | :------------------- | :---------------------- | :----------------------------------------------------- |
| 皮质拘束衣 | 强迫挺胸、限制抬臂   | 硬光/戏剧光强调皮革高光 | `straitjacket`, `leather restraint`, `buckled`         |
| 乳胶全拘束 | 完全限制关节弯曲     | 聚光灯勾轮廓            | `latex hood`, `catsuit`, `zippered`, `blindfold`       |
| 金属镣铐   | 固定特定姿势         | 硬光强调金属冷感        | `shackles`, `spreader bar`, `chains`, `locked`         |
| 充气拘束   | 四肢膨胀变圆无法行动 | 柔光减弱膨胀体积感      | `inflatable`, `rubber`, `bloated`                      |
| 感官剥夺   | 视觉失焦触觉敏感     | 微光/月光               | `hood`, `blindfold`, `ball gag`, `sensory deprivation` |

**完整 prompt 示例 — 皮拘 + 跪姿**：

```
tags: 1girl, leather straitjacket, bondage gear, black straps, kneeling, bound, looking up, spotlight, dark studio, shadow on face

nltags: She is bound in heavy black leather, her arms locked behind her in a straitjacket. The spotlight catches the glossy leather at her shoulders. She looks up, eyes slightly wide, lips caught between submission and defiance.
```

**完整 prompt 示例 — 感官剥夺**：

```
tags: 1girl, latex hood, blindfold, ball gag, rope bondage, kneeling, dark background, soft rim light

nltags: She is bound and blinded, a leather hood covering her eyes, her mouth filled and silenced. Her only connection to the world is the rope pressing into her skin and the soft light warming her exposed shoulders.
```

---

## 五、服装 × 构图速查

| 需求     | 推荐镜头             | 光线策略           | 避免                 |
| :------- | :------------------- | :----------------- | :------------------- |
| 贴身胶衣 | 中景、半身、侧身     | 硬光、边缘光       | 深色背景无 rim light |
| 丝绸长裙 | 全身或三分之二身     | 柔光、侧逆光       | 褶皱方向混乱         |
| 披风骑士 | 全身、低机位         | 侧光、硬光         | 披风遮手和腿         |
| 宽袖法师 | 半身或中景           | 柔光、背光         | 袖子吞手势           |
| 婚纱拖尾 | 全身、低机位         | 背光、窗光         | 上半身特写看不到拖尾 |
| 高开叉裙 | 侧身、中景           | 暖侧光、边缘光     | 正面宽站姿           |
| 露背礼服 | 背面、侧后方         | 侧光、轮廓光       | 长发遮背             |
| 镂空服装 | 半身、中景           | 简洁主光           | 多镂空切碎身体       |
| 绳衣结构 | 中景、正面或三分之二 | 简洁背景、硬边缘光 | 远景或复杂背景       |

---

## 六、Prompt 组合模板

### 6.1 贴身高光服装

```text
tags:
1girl, catsuit, latex, glossy, standing, side view, rim light, dark background

nltags:
The outfit follows the torso and hips without hiding the body structure.
Bright highlights trace the shoulder, waist, and outer leg.
The dark background stays separated from the body by rim light.
```

### 6.2 宽松层叠服装

```text
tags:
1girl, loose clothing, robe, wide sleeves, layered clothing, soft lighting

nltags:
The outer robe expands the silhouette without covering the face.
The wide sleeves hang beside the body and leave the hands visible.
The fabric folds downward and reveals the standing direction.
```

### 6.3 重甲披风角色

```text
tags:
1boy, armor, shoulder armor, cape, standing, low angle, hard lighting

nltags:
The shoulder armor widens the upper body without shrinking the head.
The cape falls behind the figure and keeps both arms visible.
Hard side light separates the armor plates and cape edge.
```

### 6.4 高开叉礼服

```text
tags:
1girl, long dress, high slit, side view, standing, thigh visible, warm light

nltags:
The side slit follows one leg and keeps the hip shape believable.
The dress edge stays clean and aligned with the standing pose.
The visible leg remains naturally connected to the body.
```

### 6.5 绳衣结构

```text
tags:
1girl, rope harness, shibari, kneeling, simple background, side light

nltags:
The ropes form readable diagonal lines across the torso.
The rope pattern follows the body surface without breaking anatomy.
Keep the shoulders, hands, and waist clear between the lines.
```

### 6.6 露背婚纱

```text
tags:
1girl, wedding dress, backless dress, veil, long train, from behind, backlight

nltags:
The open back is visible from a rear three-quarter angle.
The veil is translucent and does not hide the face.
The long train spreads behind the body and stays separate from the floor.
The backlight separates the veil and train from the dark interior.
```

---

## 服装改造维度框架

> 核心公式：**原服装 × 改造方向 = 最终效果**。7 个维度是通用策略框架，不是固定标签列表。具体标签通过 `danbooru-tags` 实时查询——这里只给**改造方向和组合逻辑**。

### 维度 1：透明化

把原服装面料替换为透明/半透明材质。

- 策略：`see-through` / `transparent` + 原服装名（`see-through shirt`, `transparent dress`）
- 湿透变体：`wet clothes` + `see-through` → 自然透明效果
- 关键约束：透明+无内衣 → 必须处理可见性；不想显点加 `covered nipples`

### 维度 2：裁剪/缩短

大幅缩短原有服装，定向暴露。

- 策略：在原服装名前加 `micro` / `cropped` / `highleg`
- 暴露逻辑：缩裙长 → 露腿根、缩上衣 → 露腰/下胸
- 关键约束：裁剪后暴露的部位需与下装/内衣协调

### 维度 3：镂空/开口

在服装上开洞，定向暴露特定身体部位。

- 策略：`[部位] cutout` — cleavage / underboob / navel / crotch / side
- 关键约束：多个 cutout 可叠加但不超 3 个

### 维度 4：破损化

撕裂/破坏制造"暴力后/意外"的暴露。

- 策略：`torn [服装]` / `damaged [服装]`
- 关键约束：破损配相应的身体反应（blush/shame/covering 或 defeat/apathy）

### 维度 5：胶衣/乳胶化

高光紧贴材质替代原面料。

- 策略：`latex` / `pvc` / `shiny` + 原服装类型
- 视觉关键：高光反射+贴合身体曲线；光源必须一致

### 维度 6：裸+配饰

脱到全裸但保留标志性配饰，靠配件暗示原身份。

- 策略：`completely nude` + 保留 1-2 个身份配件
- 经典组合：裸+兔耳+领结（兔女郎）、裸+围裙（裸围裙）、裸+警帽（裸警）

### 维度 7：非对称化

单侧裸露或单侧穿着，制造"匆忙/意外"的不对称。

- 策略：`off shoulder` / `one leg out` / `one stocking rolled down` / `one sleeve`
- 关键约束：不对称元素 1-2 个即可

### 组合规则

- 单次服装改造 ≤3 个维度
- 同向维度叠加增强：micro + cutout + torn → 极度暴露
- 反向维度互斥：torn 和 latex 通常不共存
- 职业制服是最佳改造载体：高正经度 × 高暴露度 = 最大反差
