# Single Character Composition / 单人构图案例

## 核心问题

单人构图的核心只有一个：**主体在画面中占多少、放哪里、怎么不被背景吞掉**

### Pattern 1：中心对称立绘

**Wrong Pattern**

- 对称构图 + 平淡表情 = 静态证件照感
- 背景太对称 + 主体太小 = 主体存在感不足，画面显得空洞

**Correct Prompt Control**

```
1girl, center composition, waist_up, symmetrical background,
facing viewer, eye contact, confident expression, hands at sides
```

- **关键**：表情必须有情绪，否则对称=死板
- **不要** `plain background` + 对称，会变成抠图素材

### Pattern 2：黄金分割/三分法立绘

**Wrong Pattern**

- 主体偏左但看向左侧 → 视线撞墙，画面堵死
- 留白侧没有任何东西也没文字 → 就是切歪了

**Correct Prompt Control**

```
1girl, off-center, looking right, rule of thirds,
copy space on right, dynamic pose, flowing hair
```

- **关键**：视线方向必须朝向留白侧
- Tag 用 `looking_away` / `looking_to_side` 锁定方向

### Pattern 3：俯视/仰视单人

**Wrong Pattern**

- 仰视 + 仰头角度过大 → 鼻孔镜头，脸崩
- 俯视 + 低头 → 只看到头顶，表情全丢
- 极端角度 + 复杂背景 → anatomy 崩盘

**Correct Prompt Control**

```
# 仰视
1girl, from below, slight low angle, looking down at viewer,
confident smirk, arms crossed, dynamic shadow
```

```
# 俯视（俯瞰）
1girl, from above, high angle, looking up,
kneeling, vulnerable expression, soft lighting
```

- **角度强度控制**：`slight_low_angle` > `low_angle` > `extreme_low_angle`，选最弱能达到效果的
- **安全组合**：极端角度 + 简单背景 + `perfect_face`

### Pattern 4：动态剪影立绘

**Wrong Pattern**

- 动态姿势 + 平光 → 身体曲线被吃掉
- 复杂姿势 + 背景太满 → 画面没呼吸感

**Correct Prompt Control**

```
1girl, sitting on edge, leaning back, one leg bent, arm resting on knee,
S-curve silhouette, rim light, simple background, dramatic shadow
```

- **关键**：动态姿势必须配合 `rim_light` 或 `backlight` 来强调轮廓
- **tag 不要**：`standing` + 动态姿势描述，模型会困惑

---

### Pattern 5：男性/中性角色单人构图

**核心差异**：不是「男性怎么画 vs 女性怎么画」，而是男性常见的全身比例崩点和轮廓处理方式不同。

#### 男性全身：肩窄、头小、腿怪

```
# 错误
1boy, full body, standing, looking at viewer

# 修正
1boy, full body, wide shoulders, broad frame, confident standing,
long coat, looking at viewer, arms at sides
```

**正确 nltags**

```
「He has a lean but athletic build with broad shoulders about three head-widths across.
His legs are long and straight, proportionate to his upper body.
His hands are relaxed at his sides, not oversized.」
```

**安全方案**：用半身构图避免全身比例问题。男性半身对 Anima 更稳定。

#### 男性半身/头像：肩颈、下颌、手

**容易崩的地方**

- 肩颈过渡太窄 → 头看起来太大
- 下颌线不清晰 → 男性脸被画成女性
- 手放的位置不对 → 破坏上半身轮廓

```
# 半身
1boy, upper body, chest up, broad shoulders,
sharp jawline, relaxed hands in pockets,
confident expression, dress shirt, rolled sleeves

# 头像
1boy, portrait, sharp jaw, masculine face,
short hair, clean face, sharp eyes
```

**注意 tag 选择**：如果目标是成熟、硬朗或宽肩男性，避免用 `cute` / `beautiful` 作为主导词，这些词会把脸往女性方向拉，改用 `handsome` / `cool` / `masculine`。美少年、偶像、少年角色可以使用 `cute` / `beautiful`，但要同时锁定 `1boy`、年龄和体型。

#### 中性角色：不被画成少女的关键

**核心原则**：先确认角色身份设定，再选择路由 tag。

- 角色身份是男性/少年 → 优先用 `1boy` + 中性特征
- 角色身份是女性但气质中性 → 用 `1girl` + `tomboy` / `androgynous` / `flat_chest` / `short_hair`
- 不要为了「中性」随便切换 `1girl` / `1boy`，身份 tag 优先服从角色设定

**当角色身份是男性/少年时：**

```
1boy, young teenager, androgynous, flat chest,
short hair, school uniform, androgynous figure
```

**当角色身份是女性但气质中性时：**

```
1girl, flat chest, no curves, androgynous, short hair,
boyish, tomboy, school uniform
```

**使用 `1girl` 的风险**：仍然可能画出胸线或腰线。用 nltags 锁定：

```
「She has a completely flat chest with no curves at the waist or hips.
Her figure is lean and boyish, like a young teenager.」
```

**最后手段**：`1girl` + `child` / `young girl` + 中性服装 → 模型会画出幼女体型而非中性体型。只在角色本身是低龄时使用。

#### 男性常见轮廓处理

| 场景      | Tag 组合                                       | 轮廓提示               |
| :-------- | :--------------------------------------------- | :--------------------- |
| 战士/战斗 | `broad shoulders, thick neck, muscular arms`   | 用护甲/披风扩展肩宽    |
| 少年/青年 | `lean build, narrow waist, school uniform`     | 肩宽 ≈2 头宽           |
| 王族/贵族 | `tall, regal posture, long coat, high collar`  | 用披风/大衣强化垂直感  |
| 重装/壮汉 | `large frame, massive shoulders, thick torso`  | 用重甲块面代替肌肉 tag |
| 偶像/文系 | `slim build, soft features, casual clothes`    | 用服装层次代替身体轮廓 |
| 反派/冷系 | `sharp features, lean silhouette, trench coat` | 用轮廓阴影代替具体 tag |
