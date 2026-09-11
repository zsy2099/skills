# PPT 交付（.pptx 生成规范）

> strategic-marketing-director v2.1.0 references
> 把"汇报用 PPT"从概念落到**可执行的 .pptx 文件**：内置生成器 + 12 套主题 + 9 种版式 + 8 页标准结构

---

## 一、什么时候用 pptx，什么时候用 html

| 场景 | 交付物 | 理由 |
|---|---|---|
| 现场演示、投屏演讲 | **html**（`templates/template-01~05.html`） | 有滚动动效、seen 类翻页、可交互 |
| 发给客户/老板离线看 | **pptx** | 对方要能下载、转发、二次编辑 |
| 需要邮件附件归档 | **pptx** | 通用格式，WPS/Office/Pages 都能开 |
| 需要打印成册 | **pptx** | 打印排版可控 |
| 需要图表联动/筛选 | html | pptx 无交互能力 |

**同构原则**：两者共用同一套 13 占位符与 8 页结构（见第五节），内容只写一次，两个格式都出。

---

## 二、生成器

```
scripts/generate_pptx.py      # 生成器（python-pptx）
scripts/deck.example.json     # 空白骨架，复制后填内容
```

### 依赖

```bash
pip install python-pptx>=1.0.2
```

### 命令

```bash
# 生成
python generate_pptx.py --input deck.json --output deck.pptx

# 覆盖视觉风格（忽略 deck.json 里的 style 字段）
python generate_pptx.py --input deck.json --output deck.pptx --style minimalism

# 列出全部可用风格
python generate_pptx.py --list-styles
```

### 固定规格

- 画布 16:9，13.333 × 7.5 英寸
- 页边距 0.72 英寸，内容宽 11.893 英寸
- 中文默认字体：微软雅黑；像素风/终端风自动切 Consolas（中文自动回落）
- 所有文本框自动估算字号，**内容多不会溢出**（`fit_size()` 逐档降号）
- 每页自动带页脚说明与"n / total"页码（封面与章节页除外）

---

## 三、deck.json 结构

### 顶层

| 字段 | 类型 | 说明 |
|---|---|---|
| `style` | string | 12 风格键之一，见第四节 |
| `cover` | object | 封面：`title` / `scenario` / `subtitle` / `presenter` / `date` |
| `sections` | array | 正文页数组，封面之后逐页渲染 |

### 页面通用字段

| 字段 | 说明 |
|---|---|
| `layout` | 版式键，见第五节。缺省 `bullets` |
| `title` | 页面标题（左侧主色竖条 + 大号标题） |
| `kicker` | 页脚左侧小字，标注调用框架/模型 |

### 各版式专有字段

| layout | 专有字段 |
|---|---|
| `agenda` | `items[]` 目录条目 |
| `metrics` | `conclusion`（结论长句）、`frameworks`（调用框架）、`metrics[]`（`num` + `label`，最多 4 个） |
| `bullets` | `bullets[]`、`note`（标题下引言，可选） |
| `two_column` | `left{title,bullets[]}`、`right{title,bullets[]}` |
| `table` | `headers[]`、`rows[][]` |
| `timeline` | `stages[]{name,desc}` |
| `section` | `title`、`note`（整屏主色章节页） |
| `closing` | `bullets[]`（箭头前缀的下一步清单） |

---

## 四、12 套视觉主题

与 `references/output-templates.md` 的 12 种视觉风格一一对应，`--style` 直接填键名。

| 键 | 名称 | 底色 | 主色 | 适用调性 |
|---|---|---|---|---|
| `minimalism` | 极简主义 | 米白 | 近黑 + 柠檬黄 | 高端 / 专业 |
| `modernism` | 现代主义 | 纯白 | 包豪斯红 #DA1F26 | 专业 / 高端 |
| `brutalism` | 新野兽派 | 米白 | 亮粉 #FF3D7F | 活力 |
| `pixel` | 像素风 | 深黑蓝 | 荧光绿 #39FF14 | 活力 / 科技 |
| `maximalism` | 极繁主义 | 浅粉 | 玫红 #E91E63 | 活力 |
| `retro` | 复古风 | 米黄 | 砖橙 #C05F2C | 亲和 |
| `glassmorphism` | 玻璃拟物 | 淡蓝紫 | 蓝 #4A6CF7 | 科技 / 高端 |
| `terminal` | 终端风 | 纯黑 | 绿 #22C55E | 科技 |
| `nordic` | 北欧风 | 灰白 | 鼠尾草绿 + 木色 | 亲和 / 专业 |
| `postmodern` | 后现代主义 | 纯白 | 紫 #7C3AED + 橙 | 创意 |
| `futurism` | 未来主义 | 深蓝黑 | 青 #00E5FF + 洋红 | 科技 |
| `y2k` | Y2K千禧 | 淡紫 | 紫 #7B5CFF + 粉 | 活力 |

**调性 → 风格**：高端→minimalism/modernism；专业→modernism/minimalism；科技→futurism/terminal；活力→brutalism/y2k；亲和→nordic/retro。

---

## 五、8 页标准结构（与 HTML 模板同构）

| 页 | layout | 内容 | 对应 HTML 占位符 |
|---|---|---|---|
| 1 | cover | 品牌 + 场景 + 主旨 | `{{TITLE}}` `{{SCENARIO}}` `{{SUBTITLE}}` |
| 2 | agenda | 方案结构 | — |
| 3 | metrics | 核心结论 + 4 个关键数字 | `{{CONCLUSION}}` `{{FRAMEWORKS}}` `{{METRIC_1~4_NUM/LABEL}}` |
| 4 | two_column | STP 定位 + 4P 组合 | — |
| 5 | table / timeline | POES 渠道 + 增长路径 | — |
| 6 | table | 行动建议 P0/P1 | — |
| 7 | bullets | 风险预案 | — |
| 8 | bullets / closing | 复盘指标 | — |

页数可增：需要章节分隔时在对应位置插一页 `layout: "section"`。

---

## 六、内容纪律（写 deck.json 前先过一遍）

1. **结论先行**：第 3 页 `conclusion` 必须是一句完整判断，不是"分析如下"。
2. **一页一论点**：每页只回答一个问题，讲不完就拆页。
3. **字数上限**：
   - 页面标题 ≤ 18 字
   - `bullets` 每条 ≤ 45 字，每页 ≤ 6 条
   - 表格单元格 ≤ 22 字（超出自动降号，但会难看）
   - `conclusion` ≤ 90 字
4. **每条要有 So What**：写了发现必须带洞察或动作，否则删。
5. **标框架**：`kicker` 或 `frameworks` 写清调用了哪组决策框架，便于追溯。
6. **数字有来源**：口径未交叉验证的数字不进 PPT（比 md 更严格，因为 PPT 会被截图外传）。

---

## 七、生成后自检清单

- [ ] 页数 = 1 封面 + 正文页数
- [ ] 没有文本框互相重叠（重点看 `two_column` 内容多时）
- [ ] 表格没有被截断（行数 > 6 时考虑拆两页）
- [ ] 深色主题（pixel / terminal / futurism）文字对比度足够
- [ ] 页脚框架标注与正文用的模型一致
- [ ] 用 WPS 或 PowerPoint 实际打开一次（字体替换检查）
- [ ] 交付前另存 PDF 做一次静态检查

---

## 八、已知边界

- **不支持图表**：生成器不画 Chart.js 类图表。需要数据图时，先用 html 交付出图，再截图贴进 pptx，或改用 `table` 版式。
- **不支持图片占位**：`cover`/版式不自动插图。需要配图时在生成后手工插入，或在 html 里用 `<img>`。
- **字号是估算**：中英混排按 CJK 1.02em 近似，极端混排可能偏小，生成后肉眼扫一遍。
- **动效为零**：pptx 是静态排版，切换动画需在 PowerPoint 里另加（建议统一"淡入/推入"，别用花哨切换）。

---

## 九、SOP

1. 定场景 → 确认要 pptx（要发客户/离线看）还是 html（现场讲）
2. 选调性 → 映射视觉风格 → 得到 `--style`
3. 按第五节搭 8 页骨架（复制 `scripts/deck.example.json`）
4. 填内容，过第六节纪律
5. 跑生成器
6. 过第七节自检
7. 需要现场演示时，同内容再套一份 `templates/template-0X.html`
