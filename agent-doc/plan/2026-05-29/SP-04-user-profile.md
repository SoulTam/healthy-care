# SP-04: 用户信息与饮食禁忌管理

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-04 |
| 对应全局任务 | T-04 |
| 对应结果蓝图章节 | 后端API-用户服务/收藏服务, 数据表-user_dietary_restrictions/favorites |
| 前置依赖子计划 | SP-03 |
| 输出产物 | `app/user/profile.py`, 饮食禁忌 API, `app/favorite/` 收藏 API |
| 执行Agent | 后端Dev |
| 预估复杂度 | 低 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**用户信息 API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/user/profile` | GET | 获取用户信息 |
| `/api/v1/user/profile` | PUT | 更新用户信息（nickname, avatar, gender, birthday, region） |
| `/api/v1/user/dietary-restrictions` | GET | 获取饮食禁忌 |
| `/api/v1/user/dietary-restrictions` | PUT | 更新饮食禁忌 |
| `/api/v1/user/delete` | DELETE | 注销账号 |

**收藏 API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/favorite/list` | GET | 收藏列表（分页，按 target_type 筛选） |
| `/api/v1/favorite/toggle` | POST | 切换收藏/取消收藏 |
| `/api/v1/favorite/check` | GET | 检查是否已收藏 |

**数据表 `user_dietary_restrictions`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | UNIQUE FK→users |
| allergies | JSON | ["花生", "海鲜"] |
| religious | JSON | ["清真", "素食"] |
| pregnancy | BOOLEAN | DEFAULT FALSE |
| pregnancy_trimester | INT | 1/2/3 |
| other_restrictions | JSON | ["低盐", "低糖"] |
| updated_at | TIMESTAMP | |

**数据表 `favorites`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK→users, INDEX |
| target_type | VARCHAR(20) | recipe/knowledge/post |
| target_id | UUID | INDEX |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| UNIQUE(user_id, target_type, target_id) |

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| GET /user/profile | 返回当前用户完整信息 | ⬜ |
| PUT /user/profile | 更新后持久化，下次 GET 返回新值 | ⬜ |
| 饮食禁忌 CRUD | GET/PUT 正常，JSON 字段存取正确 | ⬜ |
| 注销账号 | 用户状态改为 deleted，无法再登录 | ⬜ |
| 收藏列表 | GET /favorite/list 返回用户收藏，支持分页+类型筛选 | ⬜ |
| 收藏切换 | POST /favorite/toggle 正确切换收藏状态 | ⬜ |
| 收藏检查 | GET /favorite/check 返回正确状态 | ⬜ |
| 收藏唯一约束 | 同一用户同一目标不可重复收藏 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| User 模型 | SP-03 | users 表模型 |
| get_current_user 依赖 | SP-01 | 鉴权中间件 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 UserDietaryRestrictions 模型 | dietary restrictions 表 | 3.2 user_dietary_restrictions |
| 2 | 实现 ProfileService：get_profile, update_profile, get_restrictions, update_restrictions, delete_account | profile service | 2.2 用户服务 |
| 3 | 实现 profile router 注册所有端点 | profile router | 2.2 |
| 4 | 定义 Favorite 模型 | favorites 表 | 3.2 favorites |
| 5 | 实现 FavoriteService：list, toggle, check | favorite service | 2.2 收藏服务 |
| 6 | 实现 favorite router 注册 3 个端点 | favorite router | 2.2 |
| 7 | 测试用户服务 CRUD + 收藏服务 CRUD | 测试用例 | — |

## 完成标志

- [ ] 5 个用户接口全部实现
- [ ] GET/PUT 正常，数据持久化
- [ ] 注销账号正常
- [ ] 3 个收藏接口全部实现（list/toggle/check）
- [ ] 收藏唯一约束生效
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-04-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
