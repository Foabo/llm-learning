"""嵌入模型配置和管理."""

import os
from typing import Union
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from .config import settings
from .doubao_embeddings import DoubaoEmbeddings


@lru_cache(maxsize=1) 
def get_embedding_model() -> Union[OpenAIEmbeddings, DoubaoEmbeddings]:
    """获取缓存的嵌入模型实例 (支持OpenAI、豆包等)."""
    
    # 优先检查豆包配置
    if settings.ark_api_key and settings.ark_base_url and settings.doubao_embedding_model:
        print(f"🥄 使用豆包多模态Embedding: {settings.doubao_embedding_model}")
        print(f"🔗 豆包API端点: {settings.ark_base_url}")
        
        return DoubaoEmbeddings(
            model=settings.doubao_embedding_model,
            api_key=settings.ark_api_key,
            base_url=settings.ark_base_url
        )
    
    # 使用OpenAI embedding
    if not settings.openai_api_key:
        raise ValueError("未配置API密钥，请在.env文件中设置OPENAI_API_KEY或ARK_API_KEY")
    
    # 检查OpenRouter（不支持embedding）
    if settings.openai_base_url and "openrouter" in settings.openai_base_url.lower():
        raise ValueError("OpenRouter不支持Embedding，请配置豆包API或标准OpenAI API")
    
    print(f"🔄 使用OpenAI Embedding: {settings.embedding_model}")
    if settings.openai_base_url:
        print(f"🔗 API端点: {settings.openai_base_url}")
    
    # 设置环境变量，让OpenAIEmbeddings自动读取
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    if settings.openai_base_url:
        os.environ["OPENAI_BASE_URL"] = settings.openai_base_url
    
    return OpenAIEmbeddings(
        model=settings.embedding_model
    )