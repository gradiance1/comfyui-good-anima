# Composition Errors / 构图错题集

> **优先级最高** — 每次构图翻车就追加一条。模型知道怎么画对，但不知道什么情况下会画错。

---

## E001：单人立绘，主体太小/太空

### Failure Pattern（错误模式）

画面中间一个小人，四周全是空白。背景简单但主体没有撑起画面，显得像未完成。

### Correct Pattern（正确做法）

- 主体占比 40-60%，用膝盖以上/半身/胸部以上来控制
- 如果一定要全身：加地面阴影、加背景道具(椅子/柱子/花)、加动态 pose
- 用 `waist_up` / `upper_body` / `cowboy_shot` 来明确裁剪

### Prompt Use

```
❌ 错：1girl, full body, standing, plain background
✅ 对：1girl, upper body, standing, hands in pockets, city street background, depth
```

### Tags vs nltags

- Tag 解决：`upper body` / `cowboy shot` / `from above`（控制框架）
- nltags 解决：主体和背景的具体位置关系（如果 tag 不够用）
- **不要** `full_body` + 无构图约束，会出缩在角落的小人

---

## E002：双人同框，两个人互不相关

### Failure Pattern（错误模式）

两个人并排站着，各自看各自的方向，不像在同一个画面里。

### Correct Pattern（正确做法）

- 至少定义一个联系点：视线接触/手部接触/共享道具
- 常用布局：面对面、并排看同一方向、前后位（一人挡另一人肩）
- 用 `looking_at_another` / `eye_contact` / `holding_hands` 锁死关系

### Prompt Use

```
❌ 错：2girls, standing side by side, black hair girl, white hair girl
✅ 对：2girls, facing each other, eye contact, holding hands, black hair girl looking at white hair girl
```

### Tags vs nltags

- Tag 解决关系类型：`eye_contact` / `holding_hands` / `conversation`
- nltags 解决位置：「Place the black-haired girl on the left, facing right toward the white-haired girl」
- **不要**只列两个人但不写他们怎么互动

---

## E003：强透视（仰视/俯视）导致脸部变形

### Failure Pattern（错误模式）

低角度仰视或高角度俯视时，脸崩了——下巴太尖、眼睛位置不对、五官歪了。

### Correct Pattern（正确做法）

- 控制角度强度：用 `slight_low_angle` 代替 `extreme_low_angle`
- 面部朝向镜头：极端角度下正面脸比侧脸安全
- 补偿 tag：`perfect_face` / `beautiful_face` 可以稳定面部质量
- 如果要极端角度：nltags + 固定种子 + highres 修复

### Prompt Use

```
❌ 错：from below, extreme low angle, looking up
✅ 对：slight low angle, from below, facing viewer, perfect face
```

### Tags vs nltags

- Tag 控制角度强度：`from_below` > `low_angle` > `slight_low_angle`
- nltags 只在极端角度必须时用，写清楚「face stays centered and proportional」
- **anatomy 崩溃时第一步**：降角度强度，不要硬扛

---

## E004：多人场景，前景角色挡住主角脸

### Failure Pattern（错误模式）

三人以上同框，前景角色的头/手/道具正好挡在主角脸上。

### Correct Pattern（正确做法）

- 明确深度分配：前景/中景/背景 各放什么
- 主角放中景，前景角色只露肩膀/背影
- 用 `depth_of_field` / `blur` 来区分层次
- nltags 写死位置关系

### Prompt Use

```
❌ 错：3girls, one in front of another
✅ 对：3girls, one silhouette in foreground, main subject in midground, one person blurred in background
```

### Tags vs nltags

- Tag 解决层次：`depth_of_field` / `blur` / `silhouette`
- nltags 解决具体位置：「Place the main subject at center midground, let the foreground character be an out-of-focus silhouette on the left edge」
- **不要**期待 tag 能自动处理好三人以上的相对位置

---

## E005：背景比主体还抢眼

### Failure Pattern（错误模式）

背景画得很精细——繁复的花纹、华丽的建筑、复杂的自然景观——但主体反而被淹没了。

### Correct Pattern（正确做法）

- 背景细节密度控制在主体之下
- 用 `dramatic_background` 但不能用 `detailed_background` 当主角
- 主体用高对比色（亮色主体+暗背景，或反之）
- 背景虚化：`depth_of_field` / `background_blur` / `bokeh`

### Prompt Use

```
❌ 错：detailed background, intricate cathedral interior, stained glass
✅ 对：simple dark background, rim light on subject, shallow depth of field
```

### Tags vs nltags

- Tag 控制背景复杂度：`simple_background` / `dark_background` / `blurry_background`
- Tag 突出主体：`rim_lighting` / `high_contrast` / `spotlight`
- nltags 只在需要精确背景时才用（比如背景有叙事需求时）
- **基本原则**：背景 tag 越少越好。如果背景需要写 3 个 tag 以上，可能已经在抢戏了

---

## E006：切线（Tangent）—— 不同物体的边缘刚好贴上

### Failure Pattern（错误模式）

两个人物的轮廓刚好挨在一起，或者人物轮廓线和背景线条刚好相切，造成视觉粘连。

### Correct Pattern（正确做法）

- 要么明确重叠（一个人在前、一人在后，有遮挡关系）
- 要么明确分离（中间有负空间/空隙）
- 不要让边缘「刚好碰到」
- 用 `clear_separation` 或 nltags 来避免

### Prompt Use

```
❌ 错：two people standing side by side, shoulders touching（切线陷阱）
✅ 对：two people, one slightly in front of the other, staggered positioning
```

### Tags vs nltags

- Tag 不能直接解决切线问题，这是 nltags 的领域
- nltags：「Keep the two figures separated by a clear gap at shoulder level. Do not let their outlines touch.」
- **注意**：切线在高分辨率(1536+)下更明显

---

## E007：光源方向不连续

### Failure Pattern（错误模式）

画面中光源来自两个互相矛盾的方向——人物背光但背景阳光明媚，或者窗光从左但树影从右。

### Correct Pattern（正确做法）

- 一个场景只定义一个光源方向
- 光源 tag 和背景 tag 必须物理一致
- 规则：室内=窗光/灯光、室外=太阳/阴天、逆光=必须补面光
- 检查清单：光源方向 → 背景亮度 → 人物亮度 → 阴影方向，必须连贯

### Prompt Use

```
❌ 错：backlighting, bright sunny day background（矛盾：逆光但背景大太阳）
✅ 对：backlighting, sunset sky behind, warm rim light, soft fill on face（宵暗=逆光合理）
```

### Tags vs nltags

- Tag：`backlighting` + `sunset/dusk/twilight`（合理） / `backlighting` + `noon_sun`（矛盾）
- nltags 只用于补「trick light」：「Use a soft bounce fill from the front so her face stays visible despite the strong backlight」
- **不要**同时用两个光源方向 tag（如 `light_from_left` + `light_from_right`）

## E008：三人以上，肢体归属混乱

### Failure Pattern（错误模式）

三到四个人的手臂、腿纠缠在一起，分不清谁的手搭在谁肩上、谁的腿勾着谁。

### Correct Pattern（正确做法）

- 3 人：最多写两组身体接触（A→B 牵手、B→C 搭肩），不要全连在一起
- 亲密贴贴限制 2 人，第三人有自己的独立空间
- 颜色区分：接触的两人穿不同色服装，或肤色差
- 如果真的全部纠缠在一起 → 换全身剪影/阴影构图

### Prompt Use

```
❌ 错：3girls intertwined, arms around each other, legs tangled（肢体杂交）
✅ 对：3girls, center girl holding hands with left girl, right girl resting hand on center's shoulder（明确关系）
```

### Tags vs nltags

- Tag：「holding_hands」/「arm_around_shoulder」比「intertwined」安全 100 倍
- nltags 写死归属：「The left girl's hand is on the center girl's waist. The right girl's arm rests on the center girl's shoulder. Keep each character's limbs clearly separated.」

## E009：表情与场景/姿势严重不匹配

### Failure Pattern（错误模式）

战斗场景里角色在微笑、拥抱场景里角色一张苦脸、ahegao 脸出现在非性姿势中。

### Correct Pattern（正确做法）

- 检查清单：场景情绪 → 应该是什么表情 → 当前 tag 是什么表情 → 有没有矛盾
- 情绪冲突：战斗=紧张/大叫、拥抱=柔和/微笑、害羞场景=脸红/别开眼
- 表情要匹配姿势的物理性：仰头+大叫=战斗 OK、仰头+微笑=不自然
- R18 特别：ahegao 只配性行为或高潮场景，torogao 可配温存/事前暧昧

### Prompt Use

```
❌ 错：fighting scene, sword raised, gentle smile（战斗+微笑=恐怖）
✅ 对：fighting scene, sword raised, grimacing, shouting battle cry
```

### Tags vs nltags

- Tag 只定义表情名称，不保证匹配场景
- nltags 建立因果：「Her face is tense and focused, mouth slightly open as she shouts. The strain shows in her furrowed brows.」
- **金律**：写完 prompt 后，读一遍看表情 tag 和场景 tag 有没有违和感

## E010：人物与环境比例完全失调

### Failure Pattern（错误模式）

人物只到门框一半高、站在桌子旁边但比桌子矮、在教室里头顶只到黑板下沿。

### Correct Pattern（正确做法）

- 人物在室内：至少写一个比例锚点。门框、桌子、椅子、楼梯是最有效的
- 人物在室外：建筑、树木、路灯、车、路牌
- 如果不需要精确比例：跳过低锚点、用腰部以上/特写
- 如果要全身+场景 → nltags 写死比例：「She stands in the doorway, her head reaching two-thirds of the door height」

### Prompt Use

```
❌ 错：1girl, full body, standing beside a desk（比例随机）
✅ 对：1girl, full body, standing beside desk, desk at waist height, door frame behind her
```

### Tags vs nltags

- Tag 不能建尺度关系，这是 nltags 的作用
- nltags：「The desk reaches her waist. The door frame behind her is visibly taller than her head.」
- **不要**写 `huge desk` + `small girl`——模型可能把任何一词放大到极端

---

## E011：极端比例 (巨乳+萝莉/细腰+巨乳) 导致解剖崩坏

### Failure Pattern（错误模式）

`loli` + `huge breasts` 或 `gigantic breasts` + `extremely thin waist` 时，模型要么把胸画成贴在脸上的两大球，要么把腰画成要断掉。

### Correct Pattern（正确做法）

- **不要全身展示**：用胸部特写或上半身构图，只展示胸部 → 脸的部分
- 不要写冲突 tag：loli + huge breasts 换成 `loli body` + `large breasts`（但多数模型没有这个 tag）
- 折中方案：`small body` + `large breasts` 代替 loli + huge
- 用 nltags 锁死结构

### Prompt Use

```
# 推荐方案：胸部+
loli, huge breasts, upper body close-up,
breasts visible in frame, disproportionately large chest

# 不建议的方案：试图全身展示这种比例
❌ 错：loli, huge breasts, full body, standing
```

### Tags vs nltags

- Tag 组合问题：`loli` + `large/huge/gigantic breasts` 属于高风险组合
- 如果非要全身 + 极端比例 → nltags 必须写清楚身体结构
- nltags：「She has a young small body with disproportionately large breasts. Her thin waist supports her chest, keep the anatomy structurally plausible.」
- **核心原则**：不要同时要求「极端比例」和「写实解剖」，这两者本质冲突

---
