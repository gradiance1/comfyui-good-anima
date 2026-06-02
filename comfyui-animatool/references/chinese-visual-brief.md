# 中文视觉需求展开检查表

只在用户中文需求过于抽象、画面细节不足、但又希望“更华丽/更电影感/更东方幻想/更商业视觉”时读取。本文件不是构图教材，也不是扩写模板；只补用户意图中缺失且会影响 Anima 输出稳定性的少量上下文。

## 使用边界

- 目标：把中文审美意图转成 Anima 可执行的英文 prompt 细节。
- 输出仍由 `comfyui-animatool` 组装成 `prompt_11`，不是只输出中文段落。
- 不写署名、水印、底部文字、海报排版文字。
- 不自动补默认画师；需要画师时按 `prompt-assembly.md` 解析并用 `danbooru-tags` 校验。
- 不把默认前缀改成 `safe, score_7`；质量前缀跟随当前 workflow。
- 优先补少量真正能让需求变清楚的缺失信息；不要把所有类别都填满。
- 模型常识能处理的普通构图、普通情绪、普通光源不展开；只补 Anima 容易漂移的身份、服装、光源保护、脸部可读性和画布适配。

## 可选展开项（最多选 2 类）

构图与视角：

- 选一个主构图：三分法、中心对称、对角线、框中框、前中后景层次、负空间。
- 选一个镜头意图：平视、低角度、微俯视、鸟瞰、POV、过肩、近景、中景、全身、宽景。
- 如果需要镜头感，用 `nltags` 写可见控制，不写摄影术语堆叠。

人物特征：

- 补基础外观：脸型气质、眼型/瞳色、发型/发色、身份锚点。
- 多角色必须绑定位置与外观，不写 loose list。
- 原作角色优先保留 canonical tag，再补基础外观防混淆。

妆容与皮肤质感：

- 二次元插画中只保留可见效果：清透肤色、冷光高光、珠光、微红、眼尾装饰、花钿、泪痣、鳞纹/冰晶纹等。
- 不写真实摄影皮肤术语过多；Anima 偏插画，质感要转成可见色光和材质。

服饰与配饰：

- 先确定服装大类：校服、巫女服、洛丽塔、礼服、古风裙、战斗服、机能服、长袍。
- 再补 1-2 个身份细节：袖型、领口、裙摆、纹样、甲片、飘带、发饰、玉佩、手套、武器、乐器。
- 需要更强画面张力时，选择一个服装状态：整洁、半脱、湿透、破损、透明、开口、裁短、配饰保留。
- 复杂服装配干净背景或中景/全身，避免脸部周围堆小配饰。

光线与色调：

- 选一个主光源：窗光、月光、霓虹、烛光、晨光、暮光、舞台光、背光、侧逆光。
- 选一个色彩关系：冷暖对比、蓝银、紫金、朱黑、粉紫琥珀、青黛莹白。
- 光影必须服务主体：脸部可读、轮廓分离、背景不抢主体。

质感与后期：

- 只选一个主质感方向：水墨氤氲、绢本工笔、琉璃流光、冰晶通透、星云粒子、珐琅光泽、赛璐璐、厚涂插画。
- 后期词最多 1-2 个：soft glow、bloom、rim light、film grain、bokeh、mist、sparkle particles。
- 不要同时堆满“8K、电影级、商业传播、跨媒介”等抽象营销词。

场景心理：

- 私密空间适合情绪细节和服装细节；半公开空间适合风险感和动作克制；大场景适合尺度、天气和主体占比。
- 场景必须解释人物为什么在那里：窗边、走廊、神社、教室、舞台、废墟、街道、温泉、庭院都要有 1 个可见锚点。
- 只选 1-3 个故事道具：伞、书、手机、杯子、花枝、灯笼、乐器、武器、信件、散落衣物、破碎玻璃、脚印。
- 情绪要转成可见元素：表情、视线、手势、身体姿态、人与物的距离、光源压暗或照亮的位置。

## 东方幻想轻量词库

只在用户明确要东方幻想、古风、仙侠或华丽商业插画时选用；最多选 1 个场景、1 个材质、1 个光影，不要全用：

- 场景：moonlit shrine、misty garden、floating petals、ancient window、cloud sea、ice crystal palace、lantern-lit corridor。
- 材质：silk, translucent gauze, gold embroidery, jade ornament, glass-like glow, crystal fragments。
- 光影：soft moonlight, warm lantern glow, thin rim light, misty backlight, scattered sparkles。
- nltags 示例：

```text
Frame her with drifting flower branches while keeping her face clear.
Use soft moonlight from the upper left, with a thin rim light on her silhouette.
Keep the gold embroidery readable without crowding the face.
Let the misty background fade softly behind her.
```

## 压缩规则

最终 prompt 只保留：

- 质量前缀和安全标签。
- 人数、角色、作品、画师（如已确认）。
- 关键外观、服装、道具、场景 tag。
- 通常用 1-4 句 `nltags` 控制构图、光源、脸部、故事性；复杂图可以更多，但每句都要能改变画面。

如果某个细节不能明显改变画面，或只是模型已知的通用审美知识，就不要写。
