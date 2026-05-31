# SP-14: 内容系统

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-14 |
| 对应全局任务 | T-14 |
| 对应结果蓝图章节 | 后端API-内容服务, 数据表-content_* |
| 前置依赖子计划 | SP-05 |
| 输出产物 | 养生知识/食材百科/科普卡片 API |
| 执行Agent | 后端Dev |
| 预估复杂度 | 低 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**数据表**：`content_daily_tips`, `content_education_cards`, `content_ingredient_library`

**API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/content/daily-tip` | GET | 今日养生知识（按用户体质+季节个性化） |
| `/api/v1/content/daily-tip/history` | GET | 历史养生知识 |
| `/api/v1/content/ingredient/{id}` | GET | 食材百科详情 |
| `/api/v1/content/ingredient/list` | GET | 食材百科列表（分类/季节/体质/搜索） |
| `/api/v1/content/education-cards` | GET | 科普卡片列表 |
| `/api/v1/content/education-card/{id}` | GET | 科普卡片详情 |
| `/api/v1/content/education-card/{id}/related` | GET | 相关卡片 |

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| 每日养生知识 | 返回当天内容，按用户体质个性化 | ⬜ |
| 食材百科 | 列表+详情完整，支持筛选 | ⬜ |
| 科普卡片 | 列表+详情+相关推荐正常 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| content 模型 | SP-05 | 内容表 |
| 用户信息 | SP-04 | 体质个性化 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 3 个内容表模型（如 SP-05 未完成则在此补充） | 内容模型 | 3.2 |
| 2 | 实现每日养生知识：按日期查询 + 按体质+季节过滤 | daily tip API | 2.2 内容服务 |
| 3 | 实现食材百科：列表（分页+筛选）+ 详情 | ingredient API | 2.2 |
| 4 | 实现科普卡片：列表（分类）+ 详情 + 相关 | education API | 2.2 |
| 5 | 编写初始内容数据（养生知识7天、食材30种、科普卡片20张） | 初始数据 | — |

## 完成标志

- [ ] 7 个内容接口实现
- [ ] 初始内容数据入库
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-14-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
