# LLM Learning 工作区管理指南

> 📚 通过配置文件管理多子项目的最佳实践

## 🎯 解决的问题

在 `llm-learning` 这样的大型仓库中，包含多个子项目时，每次都需要手动添加子项目到 Cursor/VSCode 工作区才能使虚拟环境和 pylint 正常工作。本方案通过配置文件自动化解决此问题。

## 🛠️ 解决方案

### 1. VSCode/Cursor Workspace 配置文件

**文件**: `llm-learning.code-workspace`

这个配置文件包含：
- **多文件夹配置**: 自动加载所有子项目
- **Python 环境配置**: 统一的 Python 解释器和路径设置  
- **调试配置**: 为每个项目预设的启动配置
- **任务配置**: 批量安装依赖、运行测试等任务
- **扩展推荐**: 推荐安装的 VS Code 扩展

### 2. 自动化设置脚本

**文件**: `setup_workspace.sh`

一键设置所有子项目的虚拟环境和依赖。

## 🚀 快速开始

### 方法一：完全自动化设置（推荐）

```bash
# 1. 克隆或进入项目目录
cd llm-learning

# 2. 运行自动设置脚本
./setup_workspace.sh

# 3. 打开工作区
code llm-learning.code-workspace
# 或在 Cursor 中：File -> Open Workspace -> 选择 llm-learning.code-workspace
```

### 方法二：手动设置

```bash
# 1. 为每个子项目设置虚拟环境
cd starter_ai_agents/ai_travel_agent_langchain
uv venv && uv sync

cd ../../advanced_ai_agents/multi_agent_apps/deep-research-mini  
uv venv && uv sync

cd ../../../rag_tutorials/rag_database_routing
uv venv && uv sync

# 2. 打开工作区配置文件
code llm-learning.code-workspace
```

## 📁 工作区结构

打开 `llm-learning.code-workspace` 后，你会看到：

```
📁 LLM Learning (主项目)           # 项目根目录
📁 🚀 AI Travel Agent (LangChain)   # 旅行代理项目  
📁 🧠 Deep Research Mini (多代理)   # 深度研究项目
📁 📚 RAG Database Routing         # RAG路由项目
```

每个文件夹都会：
- 自动识别对应的虚拟环境
- 配置正确的 Python 路径
- 启用 pylint 和代码格式化
- 提供调试配置

## 🔧 高级配置

### 自定义 Python 解释器

在工作区设置中，每个项目会自动使用自己的虚拟环境：

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.analysis.extraPaths": [
        "./starter_ai_agents/ai_travel_agent_langchain",
        "./advanced_ai_agents/multi_agent_apps/deep-research-mini/src",
        "./rag_tutorials/rag_database_routing/src"
    ]
}
```

### 调试配置

为每个项目预配置了调试设置：

- **AI Travel Agent**: 直接启动 Streamlit 应用
- **Deep Research Mini**: 启动主程序
- **RAG Database Routing**: 启动 Streamlit 应用

使用方法：
1. 按 `F5` 或 `Ctrl+Shift+D`
2. 选择对应的调试配置
3. 开始调试

### 内置任务

可以使用 `Ctrl+Shift+P` -> `Tasks: Run Task` 运行预定义任务：

- **Install All Dependencies**: 为所有项目安装依赖
- **Run All Tests**: 运行所有测试
- **Format All Code**: 格式化所有代码

## 🎨 个性化定制

### 添加新的子项目

1. **更新工作区配置**:
   ```json
   {
       "folders": [
           // ... 现有项目
           {
               "name": "🆕 新项目名称",
               "path": "./new_project_path"
           }
       ]
   }
   ```

2. **更新设置脚本**:
   ```bash
   PROJECTS=(
       # ... 现有项目
       "path/to/new_project"
   )
   ```

3. **更新 Python 路径**:
   ```json
   {
       "python.analysis.extraPaths": [
           // ... 现有路径
           "./path/to/new_project/src"
       ]
   }
   ```

### 自定义调试配置

在 `launch` 部分添加新的调试配置：

```json
{
    "name": "新项目调试",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/new_project/main.py",
    "cwd": "${workspaceFolder}/new_project",
    "console": "integratedTerminal"
}
```

## 🔧 故障排除

### 常见问题

1. **Python 解释器识别问题**
   - 解决方案：`Ctrl+Shift+P` -> `Python: Select Interpreter` -> 选择正确的虚拟环境

2. **模块导入错误**
   - 检查 `python.analysis.extraPaths` 配置
   - 确保 `PYTHONPATH` 环境变量正确设置

3. **Pylint 不工作**
   - 确保在对应项目的虚拟环境中安装了 pylint
   - 检查 `python.linting.pylintPath` 配置

4. **调试配置不生效**
   - 检查 `cwd` 和 `program` 路径是否正确
   - 确认环境变量配置

### 重置环境

如果遇到问题，可以重新设置：

```bash
# 重置所有项目环境
./setup_workspace.sh

# 或者重置单个项目
./setup_workspace.sh --project rag_tutorials/rag_database_routing
```

## 📖 使用技巧

### 1. 快速切换项目

在侧边栏的资源管理器中，你可以看到所有项目文件夹。点击任意文件夹即可快速切换工作上下文。

### 2. 多项目调试

可以同时为不同项目设置断点，实现多项目联合调试。

### 3. 统一的代码风格

所有项目使用相同的代码格式化配置，保持一致的代码风格。

### 4. 环境变量管理

每个项目的 `.env` 文件会被自动识别，无需手动配置环境变量路径。

## 🔄 最佳实践

### 1. 版本控制

建议将以下文件添加到版本控制：
- `llm-learning.code-workspace`
- `setup_workspace.sh`  
- `WORKSPACE_SETUP.md`

不要添加：
- 各项目的 `.venv/` 目录
- 各项目的 `.env` 文件（包含密钥）

### 2. 团队协作

团队成员只需要：
1. 克隆仓库
2. 运行 `./setup_workspace.sh`
3. 打开 `llm-learning.code-workspace`
4. 配置各自的 API 密钥

### 3. 持续维护

- 新增子项目时及时更新配置文件
- 定期检查依赖更新
- 保持文档同步更新

## 🎯 效果对比

### 之前的工作流程
```
1. 打开 Cursor
2. 手动添加 starter_ai_agents/ai_travel_agent_langchain 到工作区
3. 选择 Python 解释器
4. 配置 pylint 路径
5. 重复步骤 2-4 为其他项目
6. 每次重启都要重新配置
```

### 现在的工作流程
```
1. 运行 ./setup_workspace.sh（仅首次）
2. 打开 llm-learning.code-workspace
3. 开始开发 ✨
```

## 📞 支持

如果遇到问题或有改进建议，请：
1. 检查本文档的故障排除部分
2. 查看项目的 Issues
3. 提交新的 Issue 并附上详细信息

---

> 💡 **提示**: 这个配置文件方法同样适用于其他多项目 monorepo 的管理，可以根据具体需求进行调整。 