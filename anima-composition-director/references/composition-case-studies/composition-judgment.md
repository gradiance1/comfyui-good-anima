# Composition Judgment / 构图判断力

> 教模型**审视自己的构图**，不是教它执行构图。这是元构图思维——判断一个构图好不好、哪里不对、怎么改。

## 核心认知
AI能生成画面，但它不知道自己画的「好不好」。这些原则帮模型在生成后做一次自我检查。

---

### 原则1：视觉平衡 (Visual Balance)

**Self-Check（生成后自检）**
- [ ] 画面是否明显歪向一边？左边重右边空？右边重左边空？
- [ ] 主要人物的脸是否居中或靠近三分线的交叉点？
- [ ] 背景的明亮区域和人物的明亮区域是否在画面对角上平衡？

**Fix**
- 一边太重 → 在轻的那边加一个有重量的元素（暗色块、人物、大道具）
- 不要太重 → 在重的那边减元素或加负空间（留白/开放天空）
- nltags 补：「Balance the visual weight by placing a dark tree silhouette on the right to counter the bright figure on the left.」

**Wrong**: 非对称 ≠ 不平衡。非对称构图可以非常平衡（如左暗右亮）。但「左边满满右边全空」= 构图失败。


### 原则2：视觉节奏 (Visual Rhythm)

**Self-Check**
- [ ] 背景元素是否散落得毫无关系，各说各的？
- [ ] 有没有3个以上的相似元素形成了一组视觉流？
- [ ] 重复元素之间的间隔是否合适——太密 = 拥挤、太疏 = 散乱

**Fix**
- 背景散乱 → 把背景元素整理成1-2条视觉路径（如：灯柱列→导视线）
- 无节奏 → 加3-5个相似元素（3棵树、5个漂浮气泡、一排窗）
- nltags：「Place a row of identical flowering trees in the midground, evenly spaced to create a gentle visual rhythm.」

**经典节奏模式**:
- `regular rhythm` — 等间距（日式走廊的柱子→秩序感）
- `flowing rhythm` — 曲线重复（花瓣飘落路径→自然感）
- `progressive rhythm` — 递进变化（从大到小的气球→引导视线）


### 原则3：焦点控制 (Emphasis / Focal Point)

**Self-Check**
- [ ] 第一眼看这张图时，眼睛看到的是什么？是你要的焦点吗？
- [ ] 画面中有没有背景元素比主角还抢眼？（窗户太亮、花朵太鲜艳、字体太大）
- [ ] 焦点元素是否在画面的光线最亮/对比最强/细节最多的位置？

**Fix**
- 焦点选错了 → 增强焦点元素的对比度（亮对暗/暖对冷/细节对简化）
- 背景抢眼 → 模糊背景、降低背景饱和度、让背景颜色统一
- nltags：「Let the girl's face be the brightest element in the frame. Keep the background soft and toned down so nothing competes with her expression.」

**焦点强度的控制手段**: `contrast` > `color saturation` > `detail level` > `size`


### 原则4：统一性 (Unity / Harmony)

**Self-Check**
- [ ] 左右/上下半的画面风格是否一致？
- [ ] 人物和背景的色调是否和谐（不会人暖景冷、人写实景写意）？
- [ ] 有没有某个元素特别「突兀」，不属于画面？

**Fix**
- 不统一 → 用一个统一色调的叠加层（如：整体加一层暖橙色→秋天感、「整体加蓝色→月光感）
- 色调冲突 → 用人物的服装色去协调背景（如：蓝发人物的蓝色和蓝天的蓝互相呼应）
- nltags：「Use a unified warm golden tone across the entire scene, from the character's skin to the background lighting.」

**注意**: 统一 ≠ 单调。你可以在统一的蓝调中让一个暖色细节突出。


### 原则5：变化性 (Variety)

**Self-Check**
- [ ] 画面是否过于统一，看起来单调？（全蓝、全绿、全站一列）
- [ ] 有没有一处意外的对比色/异形元素来活跃画面？
- [ ] 变化元素是否「破坏」了统一性？（而不是增强）

**Fix**
- 太单调 → 加1个对比色元素（如：全绿的森林中一朵红花）
- 加1个不规则的形状（如：整齐队列中有一个人回头）
- nltags：「While the entire scene has a cool blue night atmosphere, keep a single warm lantern glowing near the girl's face to break the uniformity.」

**变化 vs 统一**: 大部分元素保持统一，只保留少量变化点；不要把 80/20 当硬规则。


### 原则6：奇数分组倾向 (Rule of Odds)

**Self-Check**
- [ ] 如果是物品摆设，数量是否形成清晰节奏？
- [ ] 如果是多人场景，是否有主次层级和明确站位？

**Fix**
- 摆设散乱 → 调整成 3/5 个成组元素，或让它们沿线条/弧线排列。
- 4 角色 → 不改人数；把 1 人放前景，其余 3 人放中景，形成前后层级。
