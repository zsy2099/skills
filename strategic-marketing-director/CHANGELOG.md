# Changelog

本文件记录 strategic-marketing-director skill 版本变更。

## [2.1.0] - 2026-09-11

### 新增
- **PPT 交付落地**:`scripts/generate_pptx.py`,python-pptx 直出 16:9 .pptx(此前 ppt 交付只写"由外部技能生成",无可执行路径)
- **12 套 pptx 主题**:与 12 视觉风格一一对应(minimalism/modernism/brutalism/pixel/maximalism/retro/glassmorphism/terminal/nordic/postmodern/futurism/y2k)
- **9 种版式**:cover / agenda / metrics / bullets / two_column / table / timeline / section / closing
- **deck.json schema**:`scripts/deck.example.json`,8 页标准结构与 HTML 模板的 13 占位符同构
- **新参考文档**:`references/ppt-delivery.md`(生成规范 + 字数纪律 + 自检清单 + 已知边界)
- **自动排版**:`fit_size()` 按框体估算字号,内容超量自动降号不溢出;自动页码与页脚框架标注

### 修复
- SKILL.md 第十节写"5 视觉风格",references/output-templates.md 已是 12 种 -> 全文统一为 12 风格
- frontmatter `visual_styles: 5` -> 12
- 触发场景补充 PPT 相关关键词(汇报PPT/提案PPT/PPTX/生成PPT/deck)

### 变更
- version: 2.0.0 -> 2.1.0
- references: 16 文件 -> 17 文件(9 基础 + 8 扩展)
- scripts: 由"预留"变为实际交付(pptx 生成器 + deck 骨架)

### 依赖
- python-pptx >= 1.0.2(仅生成 pptx 时需要,其余能力零依赖)

## [2.1.1] - 2026-09-11

### 新增
- **双技能串联工作流**:新增 `references/dual-skill-workflow.md`(第 18 个参考文档)
  - SMD 阶段 1-3 战略结论 ↔ marketing-skills 23 模块映射表
  - 12-14 页完整提案标准结构
  - 8 步 SOP(从商业问题到 deck.pptx)
  - 7 处改写复用实战模板
  - 5 条常见反模式
- **实战模板**:`templates/examples/rose-silk-dual-deck.json`(玫瑰丝语 12 页完整提案案例,minimalism 主题)
- **templates/README.md 第八节**:双技能串联实战模板引用

### 变更
- version: 2.1.0 -> 2.1.1
- references: 17 -> 18
- SKILL.md 触发场景补"双技能串联 / 完整提案 / SMD × marketing-skills"
- 关键词补:双技能串联、完整提案、SMD × marketing-skills、战略+执行串联

## [2.0.0] - 2026-08-10

### 新增
- 5阶段工作流:新增"搜索"阶段,形成搜索->诊断->策略->执行->复盘完整闭环
- 9组决策框架:210+模型按分析链路系统化组合(场景+调用顺序+输出)
- 思维方法论决策驱动链:8思维模型各驱动一决策环节,收敛+发散双闭环
- 执行层倒推:9组战术+工具+SOP,从决策框架倒推落地执行
- POES渠道体系:12渠道(付费/自有/赢得/共享)链路+SOP+方法论
- 深度心理洞察:7层心理模型+三层穿透法+15应用点闭环
- 增长执行SOP:5 Phase增长闭环+5标准化交付模板
- 多格式品牌化输出:md/html/ppt 3格式 + 5调性 + 5视觉风格HTML模板
- 6类用户定位:品牌顾问/企业老板/CMO/产品经理/操盘手/CEO

### 变更
- 模型库:9库50+模型 -> 9库210+模型
- references:9文件 -> 16文件(9基础+7扩展)
- 用户定位:营销总监 -> 6类决策者
- 输出交付:md文本 -> md/html/ppt+5调性+5视觉风格

### 交付物
- 5视觉风格HTML模板(现代主义/极简主义/新野兽派/像素风/极繁主义)
- 3测试用例(evals/)
- 16参考文档(references/)

## [1.0.0] - 2026-04-24

### 初始版本
- 9库50+模型(战略/思维/品牌/营销/增长/心理/数据/运营/销售)
- 4阶段工作流(诊断-策略-执行-复盘)
- md文本输出
- references 9文件
