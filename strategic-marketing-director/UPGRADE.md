# Upgrade Log

本页记录 strategic-marketing-director 的重大升级。每次升级都应填一行，注明版本号、变更摘要、变更时间、变更作者。

---

## v2.1.1 — 2026-09-11 — 双技能串联（阿七 升级）

### 升级背景

v2.1.0 把"PPT 交付"补到了能直出 .pptx 的程度，但**没有把 SMD 与 marketing-skills 串联起来**。用户提出：「最佳用法是串联，SMD 跑阶段 1-3，把结论喂给 marketing-skills 跑具体产出」——v2.1.0 没沉淀这条工作流。

### 升级内容

| # | 文件 | 变更 |
|---|---|---|
| 1 | `references/dual-skill-workflow.md` | **新增**。第 18 个参考文档：SMD 阶段 1-3 ↔ marketing-skills 23 模块映射表、12-14 页标准结构、8 步 SOP、5 条反模式 |
| 2 | `templates/examples/rose-silk-dual-deck.json` | **新增**。12 页实战模板，**7 处改写**就能复用 |
| 3 | `templates/examples/rose-silk-dual-deck.pptx` | **新增**。配套实物输出（53 KB，minimalism 主题） |
| 4 | `templates/README.md` | 第八节：实战模板引用 |
| 5 | `SKILL.md` frontmatter | version → 2.1.1；触发场景加 "双技能串联"；关键词加 4 个 |
| 6 | `SKILL.md` 目录结构 | scripts 标注从「预留」改为实际交付；references 数量 16 → 18 |
| 7 | `CHANGELOG.md` | 追加 v2.1.1 段 |

### 升级后能力对照

| 维度 | v2.1.0 | v2.1.1 |
|---|---|---|
| PPT 直出 | ✅ | ✅ |
| 双技能串联方法论 | ❌ | ✅ `dual-skill-workflow.md` |
| 实战示例（json + pptx） | ❌ | ✅ `templates/examples/` |
| 完整提案 12 页模板 | ❌ | ✅ 改 7 处复用 |

### 验证

- 12 页 PPT 生成 ✅（`scripts/generate_pptx.py` + `examples/rose-silk-dual-deck.json`）
- 双层落盘 ✅（用户级 + 项目级）
- 关键词触发覆盖 ✅（"双技能串联" / "完整提案" / "战略+执行"）

### 依赖

- python-pptx >= 1.0.2（仅生成 pptx 时需要，其余能力零依赖）
- `microsoft yahei` / `simsun` 字体（中文渲染，系统自带）

---

## v2.1.0 — 2026-09-11 — PPT 交付能力补齐（阿七 升级）

### 升级背景

原 v2.0.0 标榜"3 格式交付 md/html/ppt"，但 PPT 那栏原文写的是「由 html-ppt / frontend-slides 类外部 skill 生成」——**没有一条能落地的 .pptx 路径**。三格式，实际只有两格式。

### 升级内容

| # | 文件 | 变更 |
|---|---|---|
| 1 | `scripts/generate_pptx.py` | **新增**。python-pptx 直出 16:9 .pptx，约 600 行 |
| 2 | `scripts/deck.example.json` | **新增**。8 页骨架，与 HTML 模板 13 占位符同构 |
| 3 | `references/ppt-delivery.md` | **新增**。第 17 个参考文档 |
| 4 | `SKILL.md` 全文 | 统一「5 风格 vs 12 风格」口径冲突 |
| 5 | `SKILL.md` frontmatter | version → 2.1.0；visual_styles: 5 → 12 |

### 升级后能力对照

| 维度 | v2.0.0 | v2.1.0 |
|---|---|---|
| 模型库 | 16 references | 17 references（新增 ppt-delivery） |
| PPT 交付 | 依赖外部 skill | ✅ 内置生成器 |
| 主题数 | 5 | 12 |
| 版式数 | 0（需手动） | 9 |

### 验证

- 玫瑰丝语 8 页 demo ✅
- 12 主题批量生成 ✅
- 读回校验结构正常 ✅

---

## v2.0.0 — 2026-08-10 — 9组决策框架（原作者 黄晓轩）

5 阶段闭环 + 9 库 210+ 模型 + 8 思维链 + 9 执行层倒推 + 6 类用户 + POES 12 渠道 + 7 层心理 + 5 模板 + 5 调性。详见 `CHANGELOG.md`。

---

## v1.0.0 — 2026-04-24 — 初版（原作者 黄晓轩）

9 库 50+ 模型 + 4 阶段闭环 + 5 模板。