# Form & Body Proportion / 造型与人体比例案例

## 核心认知

AI 最常见的失败不是「不会画」，而是「画了但比例不对」。教模型比例不是教它画素描，而是告诉它「在什么场景下比例怎么定、哪里容易崩」。

---

### Pattern 1：头身比——最基本的比例语言

**Correct Prompt Control**

```
# 萝莉/幼女 (3-5头身)
loli, petite, small body, short stature,
flat chest, young girl, child proportions

# 标准少女 (6-7头身)
teenage girl, standard proportions, medium height,
athletic build, normal body type

# 成熟女性 (7.5-8头身)
mature female, tall, long legs,
slender, adult proportions, model-like

# 需要在同一画面中区分头身比 → nltags
「The younger girl on the left has small child-like proportions at about 4 heads tall. The older girl on the right stands at about 7 heads tall.」
```

**高发错误**

- `loli` + `tall` = 矛盾（要么幼女要么高个）
- `child` + `mature body` = 人体恐怖谷
- 单一 tag 控制头身比不够精确 → 必须用 nltags + 对比锚点

### Pattern 2：头部构造——脸不崩的关键

**Correct Prompt Control**

```
# 正面：最安全
facing viewer, front view, symmetrical face

# 半侧：最常用、最自然
three-quarter view, looking slightly to side

# 正侧：只需一半
profile, side view, facing left

# 极端角度必须加约束
from below, looking down at viewer, perfect face, correct facial proportions
```

**永远记住**: 正面脸 > 半侧 > 正侧 > 极端角度 = 稳定性递减

### Pattern 3：体块理解——身体不是一根线

**Correct Prompt Control**

```
# 自然站立
standing, slight hip tilt, relaxed shoulders,
contrapposto, one leg bearing weight

# 上半身扭转
twisting torso, upper body turned left, hips facing forward,
dynamic twist, spiral pose

# 前倾/后仰
leaning forward, upper body angled, bent at waist,
slight forward lean, reaching out
```

- **nltags 控制体块**: 「Her shoulders face left while her hips remain facing forward, creating a natural twist.」
- **绝对不要**: 写「rotate torso 30 degrees」— 模型看不懂角度值

### Pattern 4：年龄体型速查表

| 年龄段   | 头身比   | 体型特征                   | 用 tag                          | 易错点         |
| :------- | :------- | :------------------------- | :------------------------------ | :------------- |
| 3-6 岁   | 3-4 头身 | 圆脸、短四肢、无腰线       | `toddler, child, very young`    | 头太大         |
| 7-10 岁  | 4-5 头身 | 脸稍长、四肢变长、微量腰线 | `young girl, elementary school` | 身体太细       |
| 11-13 岁 | 5-6 头身 | 发育初期、肩变宽           | `middle school, early teen`     | 突然长高变奇怪 |
| 14-16 岁 | 6-7 头身 | 接近成人、体态成形         | `teenage, high school`          | 标准比例       |
| 17+岁    | 7-8 头身 | 成人                       | `mature, adult`                 | —              |

**关键**: 不要在同一个 prompt 混用不同年龄段的体型 tag。写 `loli, mature` 会让模型疯掉。

### Pattern 5：头肩比和脸身比的快速对照

**Correct Prompt nltags**

```
「Her shoulders are about two head-widths across. Her hands are proportionate to her body, not oversized. Her feet are planted naturally on the ground.」
```

### Pattern 6：角色间的相对比例

**Correct nltags**

```
「The two girls stand side by side. The taller one on the left is visibly one head taller than the shorter one on the right. Their head sizes are roughly equal, but their body heights differ clearly.」
```

---

### Pattern 7：角色呈现类型与体型轮廓

**核心原则**：不是按性别二分（男/女），而是按 **体型 → 轮廓语言 → 气质 → 角色功能** 分类。同一性别可以有完全不同的构图策略，不同性别可以有相似的轮廓处理。

#### 角色呈现类型速查

| 类型            | 头身比   | 肩宽(头宽) | 腰胯特征           | 轮廓语言                        | 典型角色                               |
| :-------------- | :------- | :--------- | :----------------- | :------------------------------ | :------------------------------------- |
| 少女/萝莉       | 4-6 头身 | 1.5-2      | 腰线柔、胯窄       | S 曲线、裙摆/飘带、柔光侧逆光   | 魔法少女、学园角色                     |
| 成熟女性        | 7-8 头身 | 2-2.5      | 腰胯明显、沙漏型   | S 曲线、长发/披风、光影立体     | 御姐、女骑士、女教师                   |
| 少年            | 5-7 头身 | 2-2.5      | 窄肩直线 → 发育中  | 直线轮廓开始出现、外套/运动服   | 少年漫主角、运动少年                   |
| 青年男性        | 7-8 头身 | 2.5-3      | 肩宽腰窄、V 型     | 肩背三角、直线块面、披风大衣    | 男主、战士、王族                       |
| 中性(少年型)    | 5-7 头身 | 2          | 无明显性征         | 干净轮廓、服装层次、脸部优先    | 短发少年型、制服中性角色、轻甲中性角色 |
| 中性(少女型)    | 5-7 头身 | 1.8-2      | 弱腰线、无明显胯宽 | 中性剪裁、制服/西装、利落线条   | 战双/方舟中性女角                      |
| 壮体型          | 7-8 头身 | 3+         | 肩极宽、胸厚       | 梯形轮廓、重甲/厚衣、硬光低机位 | 狂战士、重骑士、兄贵                   |
| Q 版            | 2-3 头身 | 1-1.5      | 无                 | 圆润球体、大头小身              | Chibi、吉祥物                          |
| 小体型(非 Q 版) | 4-5 头身 | 1.5        | 腰线模糊           | 小轮廓+大细节不冲突             | 合法萝莉、妖精                         |
| 高挑体型        | 8 头身+  | 2.2-2.8    | 长比例             | 垂直延展、九头身视觉            | 模特、精灵、偶像                       |

#### 轮廓语言对照

**女性常见轮廓语言**：

- 曲线：S 曲线、腰胯线、胸 → 腰 → 臀过渡
- 动态元素：发丝/裙摆/飘带/披帛的流动
- 光影：柔光、侧逆光、光泽反射
- 姿态：Contrapposto（重心在一脚）、手触腰/发

**男性常见轮廓语言**：

- 直线：肩背三角形、V 型躯干、直线块面
- 重量：重心稳定、脚站位宽、身体垂直轴
- 轮廓延伸：披风/外套/武器/肩甲的横向扩展
- 光影：硬光、低机位、侧光强调肌肉/骨骼结构
- 姿态：双手抱胸、手插口袋、单手叉腰

**中性角色轮廓处理**：

- 不强调腰胯或肩宽，用服装层次代替身体轮廓
- 脸部可读性优先 → 避免强行性别化的 tag
- 制服/西装/轻甲 = 最安全的中性服装
- nltags: 「Her/his figure is lean and androgynous, with no exaggerated curves or broad shoulders.」

#### 常见崩点与对策

**男性全身：肩窄、头小、腿怪**

```
# 崩：1boy, full body, standing
# 对：1boy, full body, wide shoulders, confident posture, long coat
# nltags: 「His shoulders are broad, about three head-widths across. His legs are long and straight, proportionate to his upper body.」
```

**中性/少年不被画成少女的关键**

```
# 崩：1girl with short hair...
# 对：1boy, young teenager, short hair, androgynous figure, no breasts
# nltags: 「The character has a lean, pre-pubescent body with no visible chest or hip curves.」
```

⚠️ 注意：对 Anima 模型而言，`1girl` vs `1boy` 是强路由 tag。角色身份是男性/少年 → 优先 `1boy`；角色身份是女性但气质中性 → 使用 `1girl` + `tomboy` / `androgynous` / `flat chest` / `short hair`。不要为了「中性」随意切换身份 tag。

**壮体型：照片墙感、比例失去控制**

```
# 对：1boy, muscular, muscular male, wide shoulders, thick neck, large frame
# 避免写太多肌肉tag导致Hulk化 → 用体格tag + 服装覆盖
# nltags: 「His build is large and imposing, with broad shoulders and a thick chest. Despite his size, his proportions remain human.」
```

**CP 体型差——最重要的一对 nltags**

```
# 关键：锁定相对高度和头部大小一致
nltags: 「The two stand side by side. The man is visibly one head taller than the woman. Their head sizes are roughly equal; the height difference comes from body length, not head scale.」
```

### Pattern 8：极端比例·截断/遮挡/光影掩体策略

只在用户明确要求极端体型/夸张比例时读取本节。不要把它当作普通人体比例规则。

这类需求的主要风险是：全身展示、极端体型词、复杂姿势同时出现时，模型很难保持清晰身体结构。

**三种策略：**

**方案 A：截断（推荐）**
不用全身展示，改用上半身/局部构图。模型只需要处理局部比例，不必同时解决全身结构。

```
huge breasts, upper body, busty,
disproportionate chest, small frame
```

- 优点：模型不需要处理下半身结构
- 缺点：看不到全身的效果

**方案 B：遮挡**
用衣服、姿势或道具挡住身体中容易崩的过渡部位。

```
huge breasts, sitting behind low table,
chest resting on table edge, upper body visible
```

- 桌子挡住了肋骨 → 腰的过渡 → 模型不需要画那一段

**方案 C：光影掩体**
用强光影让身体过渡消失在阴影中。

```
huge breasts, dramatic lighting,
dark shadow on waist, rim light on silhouette,
backlight, only outline visible
```

- 阴影吃掉腰 → 盆骨的过渡，只保留胸部+头的剪影

**高风险组合**

- 极端体型 + `full_body` + 裸露 + 复杂姿势，会显著增加比例崩坏概率。
- 如果用户坚持全身展示，用简单站/坐姿、明确遮挡或强光影减少结构压力。
