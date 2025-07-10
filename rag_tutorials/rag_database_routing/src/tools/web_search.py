"""Web search tool for fallback scenarios."""

from typing import Any, Dict
from langchain_core.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import Field


class WebSearchTool:
    """Web search tool using DuckDuckGo."""
    
    def __init__(self, **kwargs):
        try:
            self.search_engine = DuckDuckGoSearchRun()
        except Exception as e:
            print(f"⚠️  网络搜索初始化失败: {e}")
            self.search_engine = None
    
    def _run(self, query: str) -> str:
        """Execute web search."""
        if self.search_engine is None:
            return f"网络搜索不可用。针对问题'{query}'的模拟回答：这是一个测试回答，实际使用时会进行网络搜索。"
        
        try:
            results = self.search_engine.run(query)
            return f"网络搜索结果：\n{results}"
        except Exception as e:
            return f"网络搜索失败：{str(e)}。基于一般知识提供答案。"
    
    async def _arun(self, query: str) -> str:
        """Async version of web search."""
        return self._run(query) 