# SP-06: 体质评估系统（问卷模式）

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-06 |
| 对应全局任务 | T-06 |
| 对应结果蓝图章节 | 后端API-体质评估, 数据表-constitution_assessments/assessment_scores |
| 前置依赖子计划 | SP-03 |
| 输出产物 | `app/constitution/`（模型+算法+API+报告） |
| 执行Agent | 后端Dev |
| 预估复杂度 | 高 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**数据表 `constitution_assessments`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK→users |
| constitution_type | VARCHAR(20) | 九种体质之一 |
| total_score | DECIMAL(5,2) | 综合得分 |
| source | ENUM(questionnaire/chat/ai_adjusted) | |
| assessment_date | DATE | |
| trend | VARCHAR(20) | improving/stable/declining |
| summary_report | TEXT | 评估报告全文 |
| created_at | TIMESTAMP | |

**数据表 `assessment_scores`**：assessment_id + dimension(九种体质维度) + score

**API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/constitution/questions` | GET | 获取问卷题目 |
| `/api/v1/constitution/assess` | POST | 提交问卷评估 |
| `/api/v1/constitution/result/{id}` | GET | 获取评估报告 |
| `/api/v1/constitution/latest` | GET | 获取最新体质 |

**九种体质评分算法**：
- 10 题问卷，覆盖九种体质维度
- 每题 1-4 分
- 加权计算各维度得分 → 归一化 0-100
- 最高维度 = 主体质类型
- 判断轻度/中度/重度偏颇（分数区间）

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| 评分算法 | 10 题输入 → 九维度分数 + 体质类型 + 综合分 | ⬜ |
| GET /questions | 返回 10 道题目（标题+选项+分值） | ⬜ |
| POST /assess | 提交答案 → 计算 → 保存 → 返回报告 | ⬜ |
| GET /result/{id} | 返回完整评估报告（分数+特征+建议+趋势） | ⬜ |
| 两次评估间隔 | < 7 天返回错误提示 | ⬜ |
| 首次评估 | 无历史时 trend = null | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 数据库 | SP-01 | 会话管理 |
| 用户鉴权 | SP-03 | get_current_user |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 ConstitutionAssessment + AssessmentScore 模型 | `models.py` | 3.2 评估表 |
| 2 | 实现九种体质评分算法：定义 10 题（每题对应多个维度）+ 加权计算 + 归一化 | `algorithm.py` | 4.1 评估逻辑 |
| 3 | 实现 ConstitutionService：create_assessment, get_result, get_latest, check_interval | `service.py` | — |
| 4 | 实现报告生成：根据分数组装报告文本（体质特征+调养建议+注意事项） | `report_generator.py` | 评估报告 |
| 5 | 实现 constitution router（questions, assess, result, latest） | `router.py` | 2.2 体质评估 |
| 6 | 测试：10 题输入 → 输出正确的体质类型和分数 | 测试用例 | — |

## 完成标志

- [ ] 评分算法正确（可验证：已知答案序列 → 预期体质类型）
- [ ] 4 个 API 全部实现
- [ ] 评估→保存→查询流程完整
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-06-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
