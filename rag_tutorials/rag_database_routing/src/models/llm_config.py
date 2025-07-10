"""LLM和嵌入模型统一配置入口."""

# 从新的专用模块导入
from .chat_model import get_chat_model
from .embedding_model import get_embedding_model

# 导出清晰的新接口
__all__ = [
    "get_chat_model",    # 聊天模型
    "get_embedding_model"  # 嵌入模型
] 