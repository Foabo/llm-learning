"""聊天模型配置和管理."""

import os
from functools import lru_cache
from langchain_openai import ChatOpenAI
from .config import settings


@lru_cache(maxsize=1)
def get_chat_model() -> ChatOpenAI:
    """获取缓存的聊天模型实例."""
    
    if not settings.openai_api_key:
        raise ValueError("未配置OpenAI API密钥，请在.env文件中设置OPENAI_API_KEY")
    
    # 设置环境变量，让ChatOpenAI自动读取
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    if settings.openai_base_url:
        os.environ["OPENAI_BASE_URL"] = settings.openai_base_url
    
    print(f"🤖 使用聊天模型: {settings.openai_model}")
    if settings.openai_base_url:
        print(f"🔗 API端点: {settings.openai_base_url}")
    
    return ChatOpenAI(
        model=settings.openai_model,
        temperature=0
    )