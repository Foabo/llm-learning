"""Prompt templates for routing and QA."""

from langchain.prompts import ChatPromptTemplate


def get_routing_prompt() -> str:
    """Get routing prompt for determining which database to query."""
    return """你是一个查询路由专家。你的任务是分析问题并确定应该将其路由到哪个数据库。

你必须准确返回以下三个选项之一：'products', 'support', 或 'finance'。

路由规则：
1. 产品相关问题（产品特性、规格、项目详情、产品手册）→ 返回 'products'
2. 客户支持问题（帮助、指导、故障排除、客服、FAQ、指南）→ 返回 'support'  
3. 财务相关问题（成本、收入、定价、财务数据、财务报告、投资）→ 返回 'finance'

重要：只返回数据库名称，不要任何其他文本或解释。

用户问题：{question}"""


def get_qa_prompt() -> ChatPromptTemplate:
    """Get QA prompt template for answering questions based on context."""
    return ChatPromptTemplate.from_messages([
        ("system", """你是一个有用的AI助手，基于提供的上下文回答问题。
        
指导原则：
- 始终直接且简洁地回应
- 如果上下文不包含足够信息来完全回答问题，请承认这一限制
- 严格基于提供的上下文回答，避免做出假设
- 用中文回答"""),
        ("human", "以下是上下文信息：\n{context}"),
        ("human", "问题：{input}"),
        ("assistant", "我将根据提供的上下文帮助回答您的问题。"),
        ("human", "请提供您的答案："),
    ]) 