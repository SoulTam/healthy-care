# SP-12: 食补方案生成与替换

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-12 |
| 对应全局任务 | T-12 |
| 对应结果蓝图章节 | 后端API-食补方案, 数据表-diet_plans/plan_meals, 调用链路 |
| 前置依赖子计划 | SP-04, SP-10, SP-11 |
| 输出产物 | 方案生成/替换/查询 API |
| 执行Agent | 后端Dev |
| 预估复杂度 | 高 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**数据表 `diet_plans`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK→users |
| plan_type | ENUM(daily/weekly) | |
| plan_date | DATE | |
| constitution_type | VARCHAR(20) | |
| season | VARCHAR(10) | |
| status | ENUM(active/history) | |
| metadata | JSON | {feedback_count, overall_rating} |
| created_at, updated_at | TIMESTAMP | |

**数据表 `plan_meals`**：plan_id + day_index + meal_type + recipe_id + sort_order + is_replaced

**API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/diet/plan/generate` | POST | 生成方案（参数：plan_type） |
| `/api/v1/diet/plan/{id}` | GET | 方案详情 |
| `/api/v1/diet/plan/list` | GET | 方案列表 |
| `/api/v1/diet/plan/{id}/replace/{meal}` | POST | 替换单餐 |
| `/api/v1/diet/plan/{id}/regenerate` | POST | 重新生成 |

**生成调用链路**：
1. 读取用户档案（体质/禁忌/地域）
2. 获取当前季节（基于日期+节气）
3. 调用检索服务 → 引擎组合三餐/周
4. 写入 diet_plans + plan_meals
5. 返回方案

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| 方案生成 | 一日三餐/一周计划均可生成 | ⬜ |
| 方案查询 | 列表 + 详情返回完整 | ⬜ |
| 单餐替换 | 同季同体质候补 → 选择后替换 → 去重+性平衡检查 | ⬜ |
| 重新生成 | 重新基于同条件生成新方案 | ⬜ |
| 过期检测 | daily 3天过期 / weekly 7天过期，过期方案提示 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 检索 API | SP-10, SP-11 | 检索候选食谱 |
| 用户禁忌 | SP-04 | 排除条件 |
| 最新体质 | SP-06 | 体质上下文 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 DietPlan + PlanMeal 模型 | 方案表模型 | 3.2 |
| 2 | 实现方案生成：读取用户上下文 → 调检索 → 存方案 → 返回 | generate API | 2.2 方案生成 |
| 3 | 实现方案查询：列表/详情/过期检测 | query API | 2.2 |
| 4 | 实现单餐替换：同条件检索候补 → 食材去重 → 返回 top 5 → 用户确认 → 替换 | replace API | 2.2 |
| 5 | 实现重新生成 | regenerate API | 2.2 |
| 6 | 添加免责声明自动注入 | 方案输出处 | 4.2 R-038 |

## 完成标志

- [ ] 5 个方案 API 全部实现
- [ ] 生成→查询→替换→重新生成流程完整
- [ ] 过期检测正常，免责声明自动附带
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-12-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
