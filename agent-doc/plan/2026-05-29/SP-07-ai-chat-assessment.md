# SP-07: AI 对话问诊

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-07 |
| 对应全局任务 | T-07 |
| 对应结果蓝图章节 | 后端API-对话评估, 数据表-constitution_chat_sessions |
| 前置依赖子计划 | SP-02, SP-06 |
| 输出产物 | AI对话问诊 API（SSE 流式） |
| 执行Agent | 后端Dev |
| 预估复杂度 | 中 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/constitution/chat` | POST | AI对话问诊（SSE 流式） |
| `/api/v1/constitution/chat/assess` | POST | 对话评估汇总 |

**数据表 `constitution_chat_sessions`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK→users |
| messages | JSON | [{role, content}] |
| status | ENUM(active/completed) | |
| created_at | TIMESTAMP | |
| completed_at | TIMESTAMP | |

**对话流程**：
1. 用户发送消息 → SSE 流式返回 AI 回复
2. AI 根据多轮对话收集症状信息
3. 用户调用 `/chat/assess` → 汇总对话 → LLM 提取症状特征 → 调用评分算法 → 返回评估结果

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| SSE 流式 | POST /chat 返回 `text/event-stream`，客户端可逐段接收 | ⬜ |
| 多轮对话 | 对话上下文保存在 session 中，后续请求带 session_id | ⬜ |
| 对话汇总评估 | POST /chat/assess → LLM 提取症状 → 映射体质 → 保存评估 | ⬜ |
| 历史对话 | session 支持继续未完成的对话 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| LLM 客户端 | SP-02 | engine/llm/client.py |
| 评分算法 | SP-06 | 九种体质评分算法 |
| 评估模型 | SP-06 | ConstitutionAssessment |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 ConstitutionChatSession 模型 | chat session 表 | 3.2 |
| 2 | 创建 AI 问诊提示词模板（引导用户描述症状、多轮追问策略） | chat prompt | — |
| 3 | 实现 SSE 流式端点：接收消息 → 拼接对话历史 → 调用 LLM 流式生成 → 返回 SSE | SSE 端点 | 2.2 对话评估 |
| 4 | 实现对话汇总端点：调用 LLM 提取症状特征 → 转为 10 题评分 → 调用 algorithm.py 计算 → 保存报告 | 汇总端点 | 2.2 |
| 5 | 测试：多轮对话 → 汇总评估 → 输出体质类型 | 测试用例 | — |

## 完成标志

- [ ] SSE 流式端点正常，客户端可逐段接收
- [ ] 对话可保存和继续
- [ ] 对话汇总可正确输出体质评估
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-07-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
