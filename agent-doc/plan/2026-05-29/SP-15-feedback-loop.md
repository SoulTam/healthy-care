# SP-15: 反馈闭环系统

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-15 |
| 对应全局任务 | T-15 |
| 对应结果蓝图章节 | 后端API-反馈/通知服务, 数据表-user_feedback/feedback_symptoms/user_preferences/notifications/notification_settings, 调用链路-反馈闭环 |
| 前置依赖子计划 | SP-02, SP-12 |
| 输出产物 | 反馈 API + 通知 API + 权重更新机制 + 定时提醒 |
| 执行Agent | 后端Dev |
| 预估复杂度 | 中 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**数据表 `user_feedback`**：id + user_id + plan_id + recipe_id + rating(1-5) + text_content + ai_response + status

**数据表 `feedback_symptoms`**：feedback_id + symptom + improvement(improved/unchanged/worsened/new)

**数据表 `user_preferences`**：user_id + dimension + value + weight + reason

**数据表 `notifications`**：id + user_id + type + title + body + data(JSON) + is_read + created_at
**数据表 `notification_settings`**：user_id(UNIQUE FK) + feedback_reminder + daily_tip + community_interaction

**反馈 API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/feedback/submit` | POST | 提交反馈（评分+症状+文字 → AI解读 → 更新权重） |
| `/api/v1/feedback/history` | GET | 反馈历史 |
| `/api/v1/feedback/{id}` | GET | 反馈详情 |
| `/api/v1/feedback/unfeedbacked` | GET | 未反馈餐列表 |

**通知 API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/notification/list` | GET | 通知列表（分页，is_read 筛选） |
| `/api/v1/notification/unread-count` | GET | 未读通知数 |
| `/api/v1/notification/{id}/read` | PUT | 标记已读 |

**反馈闭环**：
1. 用户提交反馈 → 保存 + AI 生成反馈解读 → 更新 user_preferences 权重
2. 好评 → 提升该食材/维度权重
3. 差评 → 降低权重
4. 连续 3 次 ≤ 2 分 → 推送重新评估提醒

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| 反馈提交 | 评分+症状+文字 → 保存 → AI 反馈解读返回 | ⬜ |
| 反馈历史 | 列表+详情，含 AI 解读展示 | ⬜ |
| 未反馈列表 | 返回当前方案中未反馈的餐 | ⬜ |
| 权重更新 | 好评升权重，差评降权重 | ⬜ |
| 连续低分提醒 | 3 次 ≤ 2 分 → 推送重评通知 | ⬜ |
| 通知列表 | GET /notification/list 返回分页通知 | ⬜ |
| 未读计数 | GET /notification/unread-count 返回正确数量 | ⬜ |
| 标记已读 | PUT /notification/{id}/read 正确更新状态 | ⬜ |
| 通知设置 | 通知开关控制通知生成 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| LLM 客户端 | SP-02 | AI 反馈解读 |
| 方案/食谱数据 | SP-12 | 关联方案和食谱 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 3 个反馈表模型 | 反馈模型 | 3.2 |
| 2 | 实现反馈提交：保存 → LLM 生成解读 → 更新权重 → 返回 | submit API | 2.2 反馈+闭环 |
| 3 | 实现反馈历史/详情/未反馈查询 | query API | 2.2 |
| 4 | 实现权重更新引擎：好评/差评 → 增减 weight | weight engine | 4.2 R-052 |
| 5 | 实现连续低分检测（定时任务或提交时检查） | low score check | 4.2 R-052 |
| 6 | 定义 Notification + NotificationSetting 模型 | 通知模型 | 3.2 |
| 7 | 实现通知服务：create_notification, list, unread_count, mark_read | notification service | 2.2 通知服务 |
| 8 | 实现通知 router 注册 3 个端点 | notification router | 2.2 |
| 9 | 集成：低分检测→自动创建通知 | 闭环集成 | 反馈闭环 |

## 完成标志

- [ ] 4 个反馈接口实现
- [ ] 反馈提交→AI解读→权重更新流程完整
- [ ] 连续低分检测正常
- [ ] 3 个通知接口实现（list/unread-count/read）
- [ ] 低分检测→创建通知闭环正常
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-15-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
