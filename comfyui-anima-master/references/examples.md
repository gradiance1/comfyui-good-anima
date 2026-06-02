# End-to-End Example / 完整示例

> 用户：生成天使心跳的立华奏，三无感，教室窗边柔光。

**Flow (Standard, built-in):**

1. **Tag Validation** — one `--batch-file` call: `kanade tachibana` (character) + `angel beats!` (series) + `@mignon` (artist candidate) + `silver hair` / `yellow eyes` (appearance anchors)
2. **Prompt Assembly**:
   - Quality: `masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025`
   - Safety: `safe`
   - Positive: `1girl, kanade tachibana, angel beats!, @mignon, silver hair, yellow eyes, long hair, school uniform, solo, expressionless, looking at viewer, face focus, depth of field, classroom, window, soft light, backlighting, blurry background`
   - nltags: `Place her beside the classroom window, facing the viewer. Use soft daylight from the left side. Keep her face centered, sharp, and undistorted. Blur the classroom background gently.`
   - Negative: default (see conventions.md)
3. **Parameters**: `1024×1536`, `steps=30`, workflow defaults `dpmpp_2m_sde_gpu + beta57`, `cfg=4.5`
4. **Execute**: `local/anima-txt2img-aesthetic-lora` workflow, run mode
