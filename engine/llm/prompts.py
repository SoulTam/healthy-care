from __future__ import annotations

from typing import Any


def render_template(template: str, **kwargs: Any) -> str:
    return template.format(**kwargs)


INTENT_PARSING_TEMPLATE = """
你是一位中医食疗专家。请分析用户的查询，提取以下信息：

用户查询：{query}

请以JSON格式输出：
{{
  "constitutions": [],  // 匹配的体质类型
  "seasons": [],        // 匹配的季节
  "symptoms": [],       // 匹配的症状
  "effects": [],        // 匹配的功效需求
  "meal_type": null     // 餐型偏好
}}
"""

FEEDBACK_INTERPRET_TEMPLATE = """
你是一位中医食疗专家。用户对食补方案给出了反馈，请分析反馈内容。

用户反馈：{feedback}

请分析：
1. 用户对方案的满意程度（满意/一般/不满意）
2. 不满意的具体原因
3. 是否有新的症状或需求出现

请以JSON格式输出。
"""

REPORT_GENERATE_TEMPLATE = """
你是一位中医食疗专家。根据用户的体质评估结果和食补方案，生成一份个性化的健康报告。

用户信息：
{user_info}

体质评估结果：
{assessment}

食补方案摘要：
{plan_summary}

请生成一份全面、易懂的健康报告，包括：
1. 体质分析
2. 饮食建议
3. 生活方式建议
4. 注意事项
"""

REVIEW_TEMPLATE = """
你是一位中医食疗专家。请审核以下食补方案，确保其符合中医理论和安全性。

用户体质：{constitution}
方案内容：{plan_content}

请检查：
1. 食材搭配是否合理
2. 是否与用户体质匹配
3. 是否有禁忌或冲突
4. 改进建议
"""
