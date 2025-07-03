## 🛫 AI Travel Agent (LangChain 版本)

本项目是基于 LangChain 重写的 AI 智能旅行规划助手，支持通过大模型和多种搜索 API 自动生成个性化旅行行程。

### 主要特性
- 使用 LangChain 框架，支持 OpenAI GPT-4o 大模型
- **多种搜索 API 支持**：
  - Tavily (推荐) - LangChain 原生支持，搜索质量高，AI 优化
  - SerpAPI - 搜索质量高，稳定性好
  - Google Custom Search - 谷歌搜索结果
  - DuckDuckGo (免费) - 免费但可能有限制
- 自动生成高质量、结构化的旅行行程
- Streamlit 前端界面，交互友好
- 智能错误处理，即使搜索受限也能提供建议

### 快速开始

1. 安装依赖（推荐使用 uv 管理 Python 环境）：

```bash
mkdir starter_ai_agents && mkdir starter_ai_agents/ai_travel_agent_langchain  && cd starter_ai_agents/ai_travel_agent_langchain

uv init
//  File-右键-将starter_ai_agents/ai_travel_agent_langchain文件夹加入工作区
uv sync
```

2. 获取 API Keys：

**必需：**
- [OpenAI API Key](https://platform.openai.com/)

**可选（选择一个）：**
- [Tavily API Key](https://tavily.com/) (推荐，LangChain 原生支持)
- [SerpAPI Key](https://serpapi.com/)
- [Google Custom Search API](https://developers.google.com/custom-search) + Search Engine ID

3. 运行应用：
```bash
uv run streamlit run travel_agent_langchain.py
```

### 搜索 API 对比

| API | 优点 | 缺点 | 推荐度 |
|-----|------|------|--------|
| Tavily | LangChain 原生支持，AI 优化搜索，结果相关性强 | 付费 | ⭐⭐⭐⭐⭐ |
| SerpAPI | 搜索质量高，稳定性好 | 付费 | ⭐⭐⭐⭐ |
| Google Custom Search | 谷歌搜索结果，质量高 | 可能连接不上，需要配置，有配额限制 | ⭐⭐⭐ |
| DuckDuckGo | 免费 | 不稳定，容易遇到限制 | ⭐⭐ |

### 使用说明

**环境变量配置：**
1. 设置必需的环境变量：
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

2. 根据选择的搜索 API 设置对应环境变量（选择其中一个）：
   ```bash
   # Tavily (推荐)
   export TAVILY_API_KEY="your_tavily_api_key"
   
   # 或者 SerpAPI
   export SERPAPI_API_KEY="your_serpapi_key"
   
   # 或者 Google Custom Search
   export GOOGLE_SEARCH_API_KEY="your_google_api_key"
   export GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id"
   
   # DuckDuckGo 不需要密钥（免费但可能不稳定）
   ```

**使用步骤：**
1. 在应用界面选择搜索 API（推荐 Tavily）
2. 填写目的地和旅行天数
3. 点击"生成行程"即可获得个性化旅行规划

### 组件说明
- **多搜索支持**：支持 4 种不同的搜索 API，用户可根据需求选择
- **LangChain 集成**：Tavily 使用 LangChain 原生工具，兼容性更好
- **AI 规划**：基于搜索结果和用户偏好，生成详细旅行行程
- **错误处理**：当搜索遇到限制时，自动降级到基于 AI 知识的建议

---

本项目为 LangChain 版本，适合希望体验更强大 LLM 工作流和生态的用户。 