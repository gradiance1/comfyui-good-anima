# Anima V3 执行规则

本文件只记录 agent 不能靠常识稳定推断的事实：模型、LoRA、节点、工作流参数、CLI、本地脚本、Danbooru 工具。不要把它写成百科功能表、构图教程或审美教材；每条都必须能指导“该不该传、该传什么、出错找谁”。

## 事实来源

- Anima 官方：模型是 2B 文生图，偏 anime / illustration / 非写实艺术；官方推荐 512^2 到 1536^2 像素、30-50 steps、CFG 4-5、Danbooru tags + 自然语言混合、画师必须 `@artist`。
- ComfyUI Skill CLI 官方：`run` 阻塞，`submit` 非阻塞，`status` 查任务，`run --validate` 验证，`deps check` 查依赖，`models list` 查模型文件名。
- 本地 workflow schema：当前 args 只接受 schema 暴露字段；`prompt_11` / `prompt_12` 是文本必填，其他高级节点参数都是可选。

## Anima 模型规则

Anima 不适合真实摄影。用户要求 photorealistic / real photo 时，保留构图、材质、光影和镜头意图，转译成二次元插画；如果用户坚持真实图，提示需要非 Anima 工作流。

模型文件位置必须按官方目录：

- `anima-base-v1.0.safetensors`：`ComfyUI/models/diffusion_models/`
- `qwen_3_06b_base.safetensors`：`ComfyUI/models/text_encoders/`
- `qwen_image_vae.safetensors`：`ComfyUI/models/vae/`

Prompt 规则：

- 可以混合 Danbooru tags 和短英文自然语言；纯自然语言太短时容易不稳定。
- tag 使用小写和空格，`score_9` 这类质量 token 保留下划线。
- 普通画师必须写 `@artist name`；没有 `@` 效果很弱。
- 中文名、外号、圈名、CP 简称、社交账号先网络解析 canonical 候选，再用 `danbooru-tags` 校验；网络不是最终 tag 来源。
- 多角色必须补基础外观和位置归属；只列角色名会混淆。
- Danbooru / Gelbooru tag 冲突时，优先 Gelbooru 版本。

## 工作流选择

默认用 `local/anima-txt2img-aesthetic-lora`。它已经在 workflow 节点中加载双 LoRA，不要把 LoRA 文件名写进 prompt。

默认加速 + 美学 LoRA 工作流推荐单画师：同一张非融合图只放 1 个已确认 `@artist`。用户说“允许使用多个画师”只表示可从多个候选中选择，不等于要求同图融合。用户明确要求多画师融合时才改用 Artist Mixer；用户要求分别尝试多个画师时，拆成多个普通 job。

只有这些情况改用其他 workflow：

- 用户要求裸模型、禁用 LoRA、对比测试、排障：`local/anima-txt2img-base`。
- 用户明确要求画师融合、artist mixer、artist_chain、多画师合一：`local/anima-txt2img-aesthetic-lora-artist-mixer`。
- 用户只是说“用 A 和 B 分别出图”：这是多个普通 job，不是 Artist Mixer。

## 质量前缀

默认双 LoRA 前缀：

```text
masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025, nsfw
```

裸模型对照前缀：

```text
masterpiece, best quality, score_7, safe
```

执行规则：

- 用户没要求基础版时，用默认双 LoRA 前缀。
- 用户明确 `safe` 时才把默认 `nsfw` 换成 `safe`；否则保留本地默认。
- 不要把官方裸模型 `score_7, safe` 前缀套到双 LoRA 工作流。
- 负向默认不写 `artist name`，避免误伤画师控制。

默认负向：

```text
worst quality, low quality, score_1, score_2, score_3, blurry, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, distorted face, text, watermark, logo
```

## 节点参数边界

节点知识的用途是防止传错字段，不是让 agent 每次都主动调参。默认只传 prompt、尺寸、batch、steps、seed、`rtx_vsr_quality`、`filename_prefix`。下面这些字段只有用户明确要求调速、排障、锐化、细节、稳定性时才传。

`AnimaBoosterLoader` 加载 Anima DiT，并提供 SageAttention / torch compile 性能开关。默认不传 `anima_booster_sage_attention` 和 `anima_booster_torch_compile`。用户要求 SageAttention、JIT、torch compile 或性能排障时再传；依赖不可用时不要猜安装路径，交给 `comfyui-manager` 执行 `deps check` / `models list`。

`FLS_SamplerV4` 是当前 workflow 的采样节点。`fls_fovea_strength` 控高频纹理，`fls_sharpness` 控局部对比和边缘，`fls_mask_inertia` 控焦点区域稳定。默认值来自 workflow，不主动覆盖；只有用户要求“更锐、更有纹理、更稳定焦点、减少塑料感/过锐”时才传。

`AnimaTeaCache` 是加速节点，不是风格节点。它保留 step 数，通过缓存跳过计算；阈值过高会损伤画师 tag 和细节保真。默认不传 `teacache_*`。若必须传，`teacache_version` 必须是完整枚举 `v1 (Legacy Fast)` 或 `v2 (Standard Precise)`，不能写短 `v1` / `v2`。

`RTXVideoSuperResolution` 只做 2x 放大，不决定构图。只允许传 `rtx_vsr_quality`，值为 `LOW / MEDIUM / HIGH / ULTRA`；不要传 `rtx_vsr_scale`，倍率由 workflow 固定。

## Artist Mixer

Artist Mixer 解决的是 Anima 文本编码器中多个画师 tag 互相干扰的问题。它只在“融合多个画师为同一张图”时启用。

执行规则：

- `artist_chain` 写不带 `@` 的画师名，逗号或换行分隔。
- 支持权重：`(wlop:1.2)` 或 `::wlop::1.2`。
- `prompt_11` 不重复画师名；主 prompt 只写主体、场景、服装、构图。
- 默认 `combine_mode=output_avg`、`fusion_mode=interpolate`、`artist_mixer_strength=1.0` 使用 workflow 默认即可。
- `artist_mixer_apply_to_uncond` 默认 `false`，不要主动打开。
- 高级稳定器、block 范围、percent 范围只在用户明确调试 Artist Mixer 时传。

## Prompt 与 nltags

正向顺序：

```text
quality_meta_year_safe → count → character → series → artist/style → appearance → tags → environment → nltags
```

执行规则：

- 同一语义不要同时放 tag 和 `nltags`。
- 查不到的复合概念不要伪造 tag，改写成短英文自然语言。
- `nltags` 只控制可见画面：位置、动作、镜头、光源、景深、脸部可读性。
- 通常 1-4 句；复杂图可以更多，但每句都要服务画面。
- 必须消解人数、景别、视角、闭眼/看镜头、裸体/服装、多角色属性归属冲突。

## Danbooru tag 工具

`danbooru-tags/bin/danbooru-tags.exe` 是本地 Rust CLI，用来查 Anima CSV / SQLite 索引。它不是 prompt 决策者。

执行规则：

- 角色、作品、用户指定画师、关键外观/服装/道具需要稳定时才查。
- 本地 miss 或候选明显不对时，不要扩大弱匹配；先网络解析别名/canonical name，再回来校验。
- 随机角色候选池不全量搜索；最终选中的命名/IP 角色先让模型基于自身知识补身份锚点，不确定、小众、同名/多皮肤、用户要求高还原或已出现漂移时再网络核验。confirmed tag 不等于模型一定记得正确服装/人设。随机画师默认不查画风，除非用户要求画风、时期、代表作或名称消歧。
- 普通构图、光源方向、情绪关系、故事性动作不要强行查 tag，交给 `nltags`。
- `confirmed_tags` 可回填但仍要筛意图。
- `candidate_tags` 只是候选，不能整批塞进 prompt。
- `missing` 交给 `nltags`，不要编造成 hard anchor。
- 画师必须来自 artist category，进入普通 prompt 时保留 `@`。
- `--random N` 是候选池；`--random N --for-prompt` 是生图回填模式，通常只取少量可用结果。

## ComfyUI Skill CLI

本项目不直接拼接长 `--args`。默认通过 `comfyui-manager/workspace/run_workflow_args.js` 读取 args JSON 文件，再调用 `comfyui-skill`，避免 PowerShell 引号、反斜杠、换行、BOM 破坏 JSON。

执行规则：

- 普通生图用 `submit`：非阻塞，返回 `prompt_id` 后停止。
- 用户明确“等结果、看图、检查完成”时才用 `run` 或 `status`。
- 第一次使用、改 schema、改 workflow、排障时先 `validate`。
- 缺模型或 enum 报错时用 `models list` / `deps check`，不要猜文件名。
- `submit` 后不要自动轮询，不要自动缓存；用户要求看结果或整理批量输出时才使用缓存脚本。

## 本地脚本

`run_workflow_args.js`：执行入口。支持 `run / submit / validate`。`submit` 直接返回；`run` 内部 submit 后轮询；`validate` 调用 `run --validate`。读取 args JSON 时会处理 BOM。

`cache_anima_outputs.js`：后处理入口。用户要求查看图片、补缓存、批量任务完成后整理输出时使用。不要在 `submit` 后立即调用。

`runtime_utils.js`：共享 JSON/runtime 工具。不要在新脚本里重复写 runtime 路径和 BOM 解析。

`build_index.py` / `sqlite_index.py`：Danbooru 索引维护。只有 CSV 更新、tag 分组更新或索引损坏时运行；普通生图不运行。

`random_generator.py`：随机语义参数生成器，不是执行器。输出必须回到 `comfyui-animatool` 复核后再交给 `comfyui-manager`。

## PowerShell JSON

Windows PowerShell 5.x 的 `Set-Content -Encoding utf8` 会写 BOM。写 CLI JSON 时用：

```powershell
[System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))
```

运行 workflow 脚本前进入 `comfyui-manager/workspace`。

## 文件命名

```text
anima/%year%-%month%-%day%/<model>-<artist|none>-<subject>[-short]
```

`<model>` 按 workflow，不按文件名猜：

- 默认双 LoRA：`anima_base_1_masterpiece_v51`
- Artist Mixer：`anima_base_1_masterpiece_v51_mixer`
- 裸模型：`anima_base_v1_0`

ComfyUI 自动追加 `_00001_` 等序号。
