# Dynamic Pose & Action / 动态姿势与动作案例

## 核心认知

静止的画面让人感觉「在动」靠的是三个东西：**线 of action**、**contrapposto**、**力与冲击的视觉暗示**。

---

### Pattern 1：线 of Action（动作线）—— 最核心的动态原则

**Wrong Pattern**

- 没有任何弧线，人物像木偶一样
- 动作线断掉（腰断开、颈断开）→ 身体分成两部分在动
- 动作线和实际运动方向矛盾

**Correct Prompt Control**

```
dynamic pose, leaning forward, reaching out,
S-curve silhouette, flowing motion,
one leg forward, arm stretched toward viewer
```

- **关键 tag**: `dynamic pose` + `action pose` + `motion`
- **强化**: `flowing hair` / `wind effect` / `speed lines` 加强动态感

### Pattern 2：Contrapposto（对立式平衡）—— 自然化的关键

**Wrong Pattern**

- 肩线和髋线完全平行 → 像被压扁的
- contrapposto 太过（肩转过 90 度但髋还在正面）→ 腰断了

**Correct Prompt Control**

```
standing, weight on one leg, relaxed pose,
slight hip tilt, shoulder line angled,
natural standing posture, contrapposto
```

- **tag**: `contrapposto` / `weight_shift` / `slight_twist`
- **不要**: 硬写「肩 90 度髋 0 度」模型理解不了角度值

### Pattern 3：力与冲击（Force & Impact）—— 「く」字法则

**Wrong Pattern**

- 没有折弯 → 像没打到
- 折弯反了方向 → 像自己在反方向跳
- 折弯程度太小 → 力度不够

**Correct Prompt Control**

```
impact frame, body bent back, recoil,
hit reaction, flying backward, arms flailing,
wind pressure, shockwave, debris flying
```

- **tag**: `impact_frame` / `recoil` / `knock_back`
- **nltags 补方向**: 「The force comes from the left, her body is bending backward from the impact, arms thrown up」

### Pattern 4：速度线 / 集中线 / 效果线

**Wrong Pattern**

- 速度线方向与运动方向不一致
- 速度线盖在人物脸上 → 脸被切成条纹
- 所有场景都用速度线 → 滥用等于没效果

**Correct Prompt Control**

```
# 速度线
speed lines, motion lines, rushing,
wind effect, fast movement, dynamic speed

# 集中线
concentration lines, radial lines, focus lines,
spotlight effect, dramatic focus, attention lines

# 冲击效果
impact lines, action lines, force wave,
shockwave effect, boom effect
```

- **tag 控制**: `speed_lines` / `action_lines` / `impact_lines`
- **区别**: 速度线=运动方向、集中线=汇聚焦点、冲击线=爆炸辐射

### Pattern 5：残像与运动模糊（Afterimage & Motion Blur）

**Wrong Pattern**

- 静态姿势+残像 → 像 bug（没动为什么有残像？）
- 全身残像 → 像分身术
- 模糊 + 残像 + 速度线 → 视觉过载

**Correct Prompt Control**

```
afterimage, motion blur, trailing effect,
multiple exposure effect, ghost trail,
smear, fast action, extreme speed
```

- **tag**: `afterimage` / `motion_blur` / `trail` / `ghost_effect`
- **安全**: 只在主体高速运动的部分加，不要全身
