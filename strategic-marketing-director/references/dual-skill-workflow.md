# 双技能串联工作流（SMD × marketing-skills）

> strategic-marketing-director v2.1.1 references
> **战略层 SMD 跑阶段 1-3 → 战略结论喂给执行层 marketing-skills → 完整提案**
> 用这两个 skill 不是"二选一"，而是按层级拼接。最小成本做完整提案的官方配方。

---

## 一、为什么要串联

| Skill | 层级 | 强项 | 短板 |
|---|---|---|---|
| strategic-marketing-director | 战略/决策层 | PESTEL/五力/3C/定位三角/Kapferer/4P/POES 12 渠道 | 不写落地页文案、不埋点、不出 A/B 配置 |
| marketing-skills v1.0.0 | 执行/战术层 | 23 个可直接落地的 CRO/SEO/付费/邮件/Referral 模块 | 不做战略论证、不做宏观扫描、不出 PPT |

把战略层结论（定位、4P 组合、POES 分配）当成 briefing，扔给执行层的对应模块，能省掉"从市场分析一路写到具体怎么发邮件"的中间断层。

---

## 二、串联流程

```
┌─────────────── strategic-marketing-director ───────────────┐
│ 阶段1 搜索：拉行业/竞品/消费者数据（WebSearch）              │
│   ↓ 输出：数据包                                            │
│ 阶段2 诊断：PESTEL → 五力 → 3C → SWOT                      │
│   ↓ 输出：诊断报告                                          │
│ 阶段3 策略：定位三角 → Kapferer → 价值主张 → STP → 4P → POES │
│   ↓ 输出：策略方案（含定位、4P 分配、POES 占比）             │
└───────────────────────┬─────────────────────────────────────┘
                        │ 战略 briefing（定位/4P/POES）
                        ▼
┌─────────────── marketing-skills（按需路由）────────────────┐
│ launch-strategy / pricing-strategy    → 上市与定价          │
│ copywriting / social-content / email-sequence → 渠道文案    │
│ paid-ads / referral-program          → 投放与裂变          │
│ seo-audit / programmatic-seo / schema-markup → 自然搜索     │
│ page-cro / signup-flow-cro / onboarding-cro / form-cro /   │
│ popup-cro / paywall-upgrade-cro      → 全链路转化            │
│ ab-test-setup / analytics-tracking   → 数据与实验            │
│ free-tool-strategy / competitor-alternatives → 获客与竞品   │
└───────────────────────┬─────────────────────────────────────┘
                        │ 执行 deliverable（文案/邮件/落地页/埋点）
                        ▼
┌─────────────── 完整提案 deck.pptx ─────────────────────────┐
│ 12-14 页：封面 → 方案结构 → 核心结论 → 战略 4-5 页         │
│ （PESTEL/五力/3C/Kapferer/价值主张） → STP+4P → POES        │
│ → 行动 → 风险 → 复盘                                       │
└────────────────────────────────────────────────────────────┘
```

---

## 三、SMD 阶段 1-3 的输出 ↔ marketing-skills 模块 映射

| SMD 战略层输出 | 喂给哪些执行模块 |
|---|---|
| PESTEL（合规红线） | paid-ads / 投放策略（绕开禁投）、free-tool-strategy（用工具触达） |
| 五力（行业吸引力） | launch-strategy、competitor-alternatives（vs 竞品页） |
| 3C（三角诊断） | competitor-alternatives |
| 定位三角（占位） | copywriting（主标语）、social-content |
| Kapferer（6 维人格） | copywriting、social-content、email-sequence（统一调性） |
| 价值主张画布 | copywriting（hero/CTA）、page-cro、form-cro |
| STP（细分/目标/定位） | email-sequence（分群）、onboarding-cro、paywall-upgrade-cro |
| 4P（产品/价格/渠道/推广） | pricing-strategy、copywriting、paid-ads |
| POES 12 渠道 | paid-ads（付费 3）/ copywriting+email-sequence（自有 4）/ marketing-ideas（赢得 3）/ referral-program（共享 2） |

---

## 四、完整提案 deck 结构（12-14 页标准）

| # | layout | 内容 |
|---|---|---|
| 1 | cover | 品牌 + 场景 + 双技能串联方法一句话 |
| 2 | agenda | 12 页方案结构 |
| 3 | metrics | 核心结论 + 4 个关键数字 + 调用框架 |
| 4 | table | **战略：PESTEL** |
| 5 | two_column | **战略：五力 + 3C** |
| 6 | bullets | **战略：Kapferer 品牌棱镜 6 维** |
| 7 | two_column | **战略：价值主张画布** |
| 8 | table | **STP + 4P 组合** |
| 9 | table | **POES 12 渠道分配** |
| 10 | table | 90 天行动建议 P0/P1 |
| 11 | bullets | 风险与合规红线 |
| 12 | closing | 复盘指标 + 下一步 |

需要多页战略层时，在第 4 页前插一页 `layout: "section"` 的章节分隔（如"战略层"深色页）。

---

## 五、完整提案 SOP

1. **拿到一个商业问题**（"X 品牌要怎么做上市/增长"）
2. **SMD 阶段 1-2**：跑 PESTEL/五力/3C，输出诊断报告（直接放进 deck P4-P7）
3. **SMD 阶段 3**：定定位、4P、POES（放进 deck P8-P9）
4. **marketing-skills 按模块拼执行**：
   - 落地页 → `page-cro`
   - 邮件 → `email-sequence`
   - 投放 → `paid-ads`
   - SEO → `seo-audit` + `programmatic-seo`
   - Referral → `referral-program`
   - 埋点 → `analytics-tracking`
   - A/B → `ab-test-setup`
5. **填 deck.json**：把战略结论和模块要点全部填进 `outputs/<项目>-dual-deck.json`
6. **跑生成器**：`python generate_pptx.py -i deck.json -o deck.pptx -s minimalism`
7. **质量检验**：过 `references/ppt-delivery.md` 第七节自检清单
8. **打包分发**：项目级 + 用户级双层落盘

---

## 六、实战模板

`templates/rose-silk-dual-deck.json` 是按这个 SOP 做出的真实案例（女用成人用品 DTC 品牌），可作下一个项目的骨架。修改方法：

- 改 `cover.title / scenario / subtitle`
- 改 `metrics.metrics`（4 个数字）
- 改 PESTEL 表的 6 行
- 改五力/3C 的两栏 bullets
- 改 Kapferer 6 维
- 改 STP+4P 表
- 改 POES 12 渠道分配
- 改 90 天行动与风险 bullets

7 个表格/栏改了就是一份新提案。

---

## 七、常见反模式

- **跳过 SMD 直接 marketing-skills**：战术做得再细，定位站错位就是给竞品打工。
- **SMD 写完战略层就停**：战略对了但没落地页/邮件/投放 SOP，也是空谈。
- **deck 塞太多页**：战略层 4 页够了（PESTEL/五力+3C/Kapferer/价值主张），执行层再补 4-5 页。
- **数字没标来源**：ppt 比 md 更严，被截图外传后口径混乱会很难收场，所有 benchmark 标出处。
- **PPT 风格乱选**：双技能联动一般走"高端 + 专业"，默认 minimalism 或 modernism，不要 y2k/pixel。