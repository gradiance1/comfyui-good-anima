# Character Interaction Composition / 多人互动构图案例

## 双人构图的三个核心锚点

1. **视线关系** — 看对方/看同一方向/看不同方向（= 关系状态）
2. **空间关系** — 面对面/并排/前后/上下（= 权力关系）
3. **接触关系** — 有接触/无接触/道具连接（= 亲密程度）

---

### Pattern 1：面对面·对话构图

**Wrong Pattern**

- 面对面但眼睛没对上 → 各看各的，像在吵架
- 两人面部在同一平面 → 像 PS 抠图拼在一起

**Correct Prompt Control**

```
2girls, facing each other, eye contact, two-shot,
one slightly closer to camera, depth of field,
soft expression, intimate atmosphere
```

- **关键**：`facing each other` + `eye contact` 锁死关系
- **不要**只写 `2girls talking`，模型不知道他们在哪、怎么站的

### Pattern 2：前后位·守护/拥抱构图

**Wrong Pattern**

- 两人在前后线上重叠太多 → 分不清谁是谁
- 前者挡了后者的脸 → 后者变成没有脸的背景板

**Correct Prompt Control**

```
2girls, back hug, one arm around waist,
taller girl behind, chin resting on shoulder,
both facing forward, soft smile, warm lighting
```

- **关键**：明确谁在前谁在后、手放哪
- Tag 用 `back_hug` / `arm_around_waist` / `chin_on_shoulder`

### Pattern 3：三人三角构图

**Wrong Pattern**

- 三人并排 → 像毕业照
- 三人在同一深度 → 没有层次感
- 给了三人同等细节 → 读者不知道看谁

**Correct Prompt Control**

```
3girls, triangle composition, one center front, two behind sides,
center girl facing viewer, side girls looking at center girl,
depth between figures, layered positioning
```

- **关键**：只给主角最完整的描述，其他两人降低细节密度
- **不要**写三个人各穿什么各是什么表情 → 信息过载 + 属性错乱

### Pattern 4：大小对比·大人 × 小孩

**Wrong Pattern**

- 大人和小孩在同一水平线 → 身高差没体现
- 小孩的脸被大人的身体挡住

**Correct Prompt Control**

```
2girls, height difference, tall and short,
tall girl kneeling down, short girl standing,
eye level conversation, soft smile, warm tone
```

- **关键**：用 `height_difference` 或 `tall_and_short` 显式声明
- **特殊 tag**: `loli` + `adult` 同时存在时要小心 anatomy 冲突

---

### Pattern 5：体型差与关系构图（不限性别）

**核心**：不是「一男一女」，而是任何体型组合（女女、男男、男女、大人小孩）的体型差控制。

#### 体型差控制三板斧

**1. 显式声明相对高度**

```
# 对的
height difference, tall and short, one head taller than the other

# 不对的（不含相对信息）
tall man, short woman
```

**2. 锁定头部大小一致**
模型崩体型差的主要原因不是身高，而是头的大小不一致。

```
nltags: 「Their head sizes are roughly equal. The height difference comes from body proportion, not head scale.」
```

**3. 用参照物锚定**
在两人之间放一个已知大小的物体（桌子、门框、柱子）。

```
# 站姿参照
standing beside each other, door frame behind them
nltags: 「The shorter character's head reaches the taller character's shoulder. The door frame beside them confirms their height difference.」
```

#### 身高差 cm 梯度参考表

当需要精确控制两人身高差时，使用以下梯度作为 nltags 写死的参照：

| 等级 | 身高差   | 高者视线             | 矮者姿态 | 禁止行为                       |
| :--- | :------- | :------------------- | :------- | :----------------------------- |
| T1   | 0–8 cm   | 视线平齐             | 视线微抬 | 禁止夸大高度差                 |
| T2   | 9–14 cm  | 视线自然落在对方面部 | 需要抬头 | 禁止高方大幅度俯身             |
| T3   | 15–25 cm | 俯视对方头顶         | 明显仰头 | 禁止矮方站立时触碰高方头顶     |
| T4   | 25 cm+   | 俯视对方轮廓         | 抬头仰望 | 绝对禁止不经姿态调整的面部互动 |

**nltags 写法按梯度**：

- T1: `「They stand nearly eye-to-eye. The slight height gap is barely noticeable.」`
- T2: `「Her eyes meet his chin naturally when standing close. She looks up slightly to meet his gaze.」`
- T3: `「She reaches only to his shoulder. He looks down to see her face; she tilts her head back to look up at him.」`
- T4: `「The height gap is dramatic — her head barely reaches his chest. Any face-to-face interaction requires one to kneel or the other to bend down significantly.」`

**关键规则**：

- T3 及以上 → 避免 `full body`，用 `upper body` / `medium shot` 裁剪
- T4 → 侧面角度优先，正面容易让矮方被遮挡
- 所有梯度 → 必须锁定「头部大小一致，身高差来自身体比例，不是头缩放」

#### 不同 CP 组合的处理差异

**体型差 CP（高矮/大小组合）**
最常见，也是最容易崩的——模型倾向于抹平高矮差，让两个人看起来接近同高。

```
1boy, 1girl, height difference, boy taller,
boy's hand on girl's shoulder, girl looking up at boy,
romantic atmosphere, warm lighting
nltags: 「The man stands a full head taller than the woman. His hand rests gently on her shoulder. She looks up slightly to meet his eyes.」
```

**双女 CP（高女 × 矮女）**

```
2girls, height difference, tall girl and short girl,
tall girl with arm around short girl,
both smiling, casual pose, matching outfits
nltags: 「The taller girl is about one head taller than her shorter companion. Their head sizes match; the difference is in body length.」
```

**双男 CP（同高或差距小）**

```
2boys, similar height, one slightly taller,
standing shoulder to shoulder, friendly pose,
both in school uniform, looking in same direction
nltags: 「The two boys are nearly the same height, standing shoulder to shoulder. Their builds are similar—lean and athletic.」
```

**家长 × 儿童（大落差）**

```
1girl, 1child, adult and child,
parent kneeling down, child standing,
eye level conversation, holding hands
nltags: 「The adult kneels to bring her face to the child's level. The child stands upright, their eyes meeting at the same height.」
```

#### 特殊技巧：用服装/道具统一体型差

当两人体型差距很大时，用相同或互补的服装元素帮助模型理解关系：

- 同色系服装 → 模型知道两人「属于一起」
- 互补轮廓（宽肩外套 vs 紧身裙）→ 强化对比
- 共享道具（牵绳/手杖/围巾）→ 物理连接帮助空间定位

```
# 共享道具
1boy, 1girl, holding opposite ends of same scarf,
height difference, wind blowing, outdoor autumn,
boy in long coat, girl in dress
nltags: 「A long scarf connects them, stretching between their hands. The wind pulls the fabric taut, emphasizing the distance between them.」
```
