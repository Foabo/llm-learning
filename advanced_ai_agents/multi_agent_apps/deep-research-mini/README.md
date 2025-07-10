# Deep Research Mini

> 🔬 基于 LangGraph 的 AI 深度研究助手

一个强大的 AI 研究助手，使用多代理架构来进行深度研究和信息收集。该项目基于 LangGraph 框架构建，提供了模块化的代理系统来处理复杂的研究任务。

## ✨ 特性

- 🤖 **多代理协作**：包含规划器、研究员和监督者三个智能代理
- 🌐 **网络搜索与爬取**：集成 Tavily 搜索和 Firecrawl 网页内容提取
- 📝 **智能提示模板**：使用 Jinja2 模板系统管理代理提示
- 🔄 **流式处理**：支持实时响应和状态更新
- 🚀 **开箱即用**：基于 LangGraph 的声明式配置，无需复杂的启动代码

## 🏗️ 架构概览

```
deep-research-mini/
├── src/
│   ├── agents/          # 代理定义
│   │   ├── planner.py   # 研究规划代理
│   │   ├── researcher.py # 研究执行代理  
│   │   └── supervisor.py # 监督协调代理
│   ├── models/          # 语言模型配置
│   ├── prompts/         # 提示模板管理
│   │   └── templates/   # Jinja2 模板文件
│   └── tools/           # 工具集成
│       ├── web_search.py # 网络搜索工具
│       └── web_crawl.py  # 网页爬取工具
├── langgraph.json       # LangGraph 配置文件
└── pyproject.toml       # 项目依赖配置
```

### 代理说明

| 代理 | 功能 | 工具 |
|------|------|------|
| **Planner** | 研究任务规划与分解 | Web Search |
| **Researcher** | 深度研究与信息收集 | Web Search + Web Crawl |
| **Supervisor** | 代理协调与结果整合 | 管理其他代理 |

## 🚀 快速开始

### 环境要求

- Python >= 3.13
- UV 包管理器

### 安装

1. **克隆项目**
```bash
git clone <repository-url>
cd deep-research-mini
```

2. **安装依赖**
```bash
uv sync
```

3. **配置环境变量**

创建 `.env` 文件并添加必要的 API 密钥：

```bash
# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Tavily 搜索 API  
TAVILY_API_KEY=your_tavily_api_key

# Firecrawl API
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

### 运行

#### 方式 1：启动 LangGraph 服务 (推荐)

```bash
# 启动开发服务器 (推荐方式 - 避免依赖问题)
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph dev --allow-blocking

# 备选方式 (如果所有依赖都正确安装)
uv run langgraph dev

# 启动生产服务器
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph up
```

服务启动后，你可以通过 Web 界面访问代理系统。

#### 方式 2：直接调用代理

```bash
# 使用研究代理
uv run python -c "
from src.agents.researcher import researcher
from src.agents.run_agent import run_agent
run_agent(researcher, '什么是大模型里的A2A技术？')
"
```

#### 方式 3：使用监督代理协调多个代理

```bash
# 使用监督代理进行复杂研究任务
uv run python -c "
from src.agents.supervisor import supervisor
result = supervisor.invoke({
    'messages': [{'role': 'user', 'content': '研究大模型的最新发展趋势'}]
})
print(result)
"
```

## 🔧 配置说明

### LangGraph 配置 (langgraph.json)

```json
{
    "graphs": {
        "planner": "./src/agents/planner.py:planner",
        "researcher": "./src/agents/researcher.py:researcher", 
        "supervisor": "./src/agents/supervisor.py:supervisor"
    },
    "python_version": "3.13",
    "env": "./.env"
}
```

### 提示模板

项目使用 Jinja2 模板系统管理代理提示，模板文件位于 `src/prompts/templates/`：

- `planner.jinja-md` - 规划代理提示模板
- `researcher.jinja-md` - 研究代理提示模板  
- `supervisor.jinja-md` - 监督代理提示模板

## 🛠️ 开发指南

### 添加新代理

1. 在 `src/agents/` 目录下创建新的代理文件
2. 在 `src/prompts/templates/` 添加对应的提示模板
3. 更新 `langgraph.json` 配置文件
4. 在 `src/agents/__init__.py` 中导出新代理

### 添加新工具

1. 在 `src/tools/` 目录下创建工具文件
2. 在 `src/tools/__init__.py` 中导出工具
3. 在相应的代理中引入和使用工具

### 自定义提示模板

编辑 `src/prompts/templates/` 中的 Jinja2 模板文件，支持动态变量和条件逻辑。

## 📦 主要依赖

- **LangGraph**: 多代理协作框架
- **LangChain**: AI 应用开发框架
- **OpenAI**: 语言模型 API
- **Tavily**: 网络搜索 API
- **Firecrawl**: 网页内容爬取
- **Jinja2**: 模板引擎

## 🔧 故障排除

### 常见问题

#### 1. `uv run langgraph dev` 报错 403 Forbidden

**问题**: 使用国内镜像源时可能遇到包下载失败的问题。

**解决方案**: 使用 `uvx` 命令代替：
```bash
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph dev --allow-blocking
```

**原因**: `uvx` 会创建一个隔离的环境来运行 langgraph-cli，避免了依赖冲突和镜像源问题。

#### 2. 环境变量未加载

确保在项目根目录下创建了 `.env` 文件并包含所需的 API 密钥。

#### 3. Python 版本问题

确保使用 Python >= 3.13，可以通过以下命令检查：
```bash
python --version
uv python list
```

## 🔗 相关链接

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangChain 文档](https://python.langchain.com/)
- [Tavily API](https://tavily.com/)
- [Firecrawl API](https://firecrawl.dev/)

---