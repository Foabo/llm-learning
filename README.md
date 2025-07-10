# LLM Learning

一个大语言模型（LLM）学习项目，收集并改进网络上优秀的 LLM 应用演示。

## 项目结构

```
llm-learning/
├── starter_ai_agents/           # 入门AI代理项目
│   └── ai_travel_agent_langchain/  # LangChain旅行规划代理
├── advanced_ai_agents/         # 高级AI代理系统
│   └── multi_agent_apps/
│       └── deep-research-mini/  # 多代理深度研究系统
└── rag_tutorials/              # RAG技术教程
    └── rag_database_routing/    # 智能数据库路由系统
```

## 项目介绍

### 🚀 AI Travel Agent (LangChain版)
- **位置**: `starter_ai_agents/ai_travel_agent_langchain/`
- **功能**: 智能旅行规划，支持多种搜索API
- **技术**: LangChain + OpenAI + Streamlit

### 🧠 Deep Research Mini 
- **位置**: `advanced_ai_agents/multi_agent_apps/deep-research-mini/`
- **功能**: 多代理协作的深度研究系统
- **技术**: LangGraph + 多代理架构

### 📚 RAG Database Routing
- **位置**: `rag_tutorials/rag_database_routing/`
- **功能**: 智能文档分类和数据库路由
- **技术**: LangGraph + Qdrant + 豆包多模态Embedding

## 快速开始

1. 选择感兴趣的项目目录
2. 阅读对应的 README.md
3. 安装依赖并配置环境变量: 
4. 运行项目: `uv run streamlit run main.py`

## 环境要求

- Python >= 3.13
- UV 包管理器
- 相关API密钥 (OpenAI、豆包等)
