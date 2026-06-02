# Lighting & Depth / 光影与深度构图案例

## 核心认知
光影在AI生成中往往比构图角度更能决定画面质量。错误的打光会让好构图变废片。

---

### Pattern 1：逆光/轮廓光 (Backlight / Rim Light)

**Wrong Pattern**
- 逆光 + 正面没补光 → 主体全黑，五官全丢
- rim light 强度太大 → 主体像被火烧
- 逆光 + 复杂背景 → 光边和背景混在一起

**Correct Prompt Control**
```
backlighting, rim light, edge lit,
sunlight from behind, hair glow,
fill light from front, soft face lighting
```
- **关键**：必须加 `fill_light` 或 `soft_front_light` 否则脸黑
- **必配**：`rim_light` + `backlight` + `fill_light` 三件套
- **不要**只用 `backlight` 不加补充

### Pattern 2：侧光/戏剧光 (Rembrandt / Split Lighting)

**Wrong Pattern**
- 侧光 + 方向不明确 → 像光从四面八方来
- 侧光 + 浅色眼睛 → 亮侧的眼睛过曝
- 侧光 + 彩色光 → 像夜店

**Correct Prompt Control**
```
side lighting, dramatic shadow, strong contrast,
one light source from left, dark shadow on right side,
volumetric lighting, deep shadow
```
- **关键**：只指定一个光源方向
- Tag 用 `side_lighting` + `one_light_source`

### Pattern 3：顶光/教堂光 (Top Light / God Rays)

**Wrong Pattern**
- 顶光 + 刘海遮眼 → 整张脸在阴影里
- 顶光 + 无补光 → 骷髅头效果
- top light + 仰视 → 死亡打光

**Correct Prompt Control**
```
top lighting, god rays, volumetric light,
light beam from above, holy atmosphere,
slight fill light for face visibility
```
- **关键**：顶光必须补 `fill_light` 否则太硬
- **不要**顶光 + `from_below` = 上下夹击会导致崩坏

### Pattern 4：景深控制 (Depth of Field)

**Wrong Pattern**
- 全部清晰 = 没有主次
- 景深太强 = 背景变色块，场景感丢失
- 前景模糊物体太大 = 挡了半个画面

**Correct Prompt Control**
```
depth of field, blurred background, bokeh,
shallow focus, soft background,
f/1.4 aperture, cinematic depth
```
- **Tag控制强度**：`depth_of_field`（弱）→ `shallow_focus`（中）→ `extreme_bokeh`（强）
- **R18特殊**：浅景深 + 局部焦点 = 高级色图常见手法

### Pattern 5：剪影 (Silhouette)

**Wrong Pattern**
- 剪影 + 无法辨认是谁 → 和路人没区别
- 剪影 + 背景不够亮 → 只剩一片黑
- 剪影 + 发型没特征 → 分不清角色

**Correct Prompt Control**
```
silhouette, strong backlight, sunset background,
dark figure, only outline visible,
distinctive hair silhouette, recognizable profile
```
- **关键**：角色的发型/轮廓必须有辨识度
- **R15-R17应用**：剪影 = 合法的「不露点但很色」

---

### Pattern 6：硬光 vs 柔光 (Hard vs Soft Light)

**Wrong Pattern**
- 硬光 + 萝莉萌系 → 像恐怖片
- 柔光 + 战斗 → 不够力度
- 混合硬柔（脸部硬光+背景柔光）→ 像合成的

**Correct Prompt Control**
```
# 硬光
harsh sunlight, sharp shadows, high contrast,
strong lighting, dramatic shadow, hard light, direct sunlight

# 柔光
soft light, diffused light, overcast, gentle lighting,
soft shadow, dreamy atmosphere, window light, cloudy
```
- **选光诀窍**：场景氛围 → 对应光质。温馨/日常=柔、战斗/戏剧=硬
- **不要**在同一画面混用硬柔光tag


### Pattern 7: 色温情绪 (Color Temperature)

**Wrong Pattern**
- 暖光+冷光混用 → 像两个画面拼在一起（除非故意做冷暖对比叙事）
- 冷光+欢乐场景 → 画面情绪矛盾
- 色温tag过多 → 互相覆盖

**Correct Prompt Control**
```
# 暖光
warm lighting, golden hour, amber light, candlelight,
sunset glow, warm tone, nostalgic atmosphere

# 冷光
cool lighting, moonlight, blue hour, neon light,
cold tone, lonely atmosphere, night scene

# 冷暖对比（叙事用）
warm window light, cold exterior, cozy inside, harsh outside
```
- **金律**：一幅画只选一个主色温。冷暖对比只在有叙事需求时用
