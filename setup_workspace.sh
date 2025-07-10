#!/bin/bash

# 脚本：LLM Learning 项目工作区设置
# 用途：自动为所有子项目创建和配置虚拟环境

set -e  # 遇到错误时退出

echo "🚀 开始设置 LLM Learning 工作区..."
echo "============================================"

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误：未找到 uv 命令"
    echo "请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 子项目列表
PROJECTS=(
    "starter_ai_agents/ai_travel_agent_langchain"
    "advanced_ai_agents/multi_agent_apps/deep-research-mini" 
    "rag_tutorials/rag_database_routing"
)

# 函数：设置单个项目
setup_project() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    echo ""
    echo "📦 设置项目: $project_name"
    echo "路径: $project_path"
    echo "----------------------------------------"
    
    if [ ! -d "$project_path" ]; then
        echo "⚠️  警告：项目目录不存在: $project_path"
        return 1
    fi
    
    cd "$project_path"
    
    # 删除现有虚拟环境
    if [ -d ".venv" ]; then
        echo "🗑️  删除现有虚拟环境..."
        rm -rf .venv
    fi
    
    # 创建新的虚拟环境
    echo "🔨 创建虚拟环境..."
    uv venv
    
    # 安装依赖
    echo "📥 安装依赖..."
    uv sync
    
    # 检查是否有 .env.example 文件
    if [ -f ".env.example" ]; then
        if [ ! -f ".env" ]; then
            echo "📝 复制环境变量模板..."
            cp .env.example .env
            echo "⚠️  请编辑 .env 文件配置您的API密钥"
        else
            echo "✅ .env 文件已存在"
        fi
    fi
    
    echo "✅ $project_name 设置完成"
    cd - > /dev/null
}

# 函数：创建全局虚拟环境（可选）
setup_global_venv() {
    echo ""
    echo "🌍 设置全局虚拟环境..."
    echo "----------------------------------------"
    
    if [ -d ".venv" ]; then
        echo "🗑️  删除现有全局虚拟环境..."
        rm -rf .venv
    fi
    
    echo "🔨 创建全局虚拟环境..."
    uv venv
    
    # 安装常用的开发工具
    echo "📥 安装开发工具..."
    .venv/bin/pip install black pylint pytest python-dotenv
    
    echo "✅ 全局虚拟环境设置完成"
}

# 主执行流程
main() {
    # 确保在项目根目录
    if [ ! -f "llm-learning.code-workspace" ]; then
        echo "❌ 错误：请在 llm-learning 项目根目录下运行此脚本"
        exit 1
    fi
    
    # 设置全局虚拟环境
    setup_global_venv
    
    # 设置各个子项目
    for project in "${PROJECTS[@]}"; do
        setup_project "$project"
    done
    
    echo ""
    echo "🎉 所有项目设置完成！"
    echo "============================================"
    echo ""
    echo "📚 使用说明："
    echo "1. 打开 Cursor/VSCode"
    echo "2. 文件 -> 打开工作区 -> 选择 'llm-learning.code-workspace'"
    echo "3. 或者在命令行中运行: code llm-learning.code-workspace"
    echo ""
    echo "🔧 配置建议："
    echo "- 编辑各项目的 .env 文件配置API密钥"
    echo "- 使用 Ctrl+Shift+P -> 'Python: Select Interpreter' 选择虚拟环境"
    echo ""
    echo "🚀 启动项目："
    echo "- AI Travel Agent: cd starter_ai_agents/ai_travel_agent_langchain && uv run streamlit run travel_agent_langchain.py"
    echo "- Deep Research: cd advanced_ai_agents/multi_agent_apps/deep-research-mini && uv run langgraph dev"
    echo "- RAG Routing: cd rag_tutorials/rag_database_routing && uv run streamlit run main.py"
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "LLM Learning 工作区设置脚本"
        echo ""
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  --help, -h    显示此帮助信息"
        echo "  --global-only 仅设置全局虚拟环境"
        echo "  --project PROJECT_PATH 仅设置指定项目"
        echo ""
        echo "示例:"
        echo "  $0                              # 设置所有项目"
        echo "  $0 --global-only               # 仅设置全局环境"
        echo "  $0 --project rag_tutorials/rag_database_routing  # 仅设置RAG项目"
        ;;
    --global-only)
        setup_global_venv
        ;;
    --project)
        if [ -z "${2:-}" ]; then
            echo "❌ 错误：--project 需要指定项目路径"
            exit 1
        fi
        setup_global_venv
        setup_project "$2"
        ;;
    "")
        main
        ;;
    *)
        echo "❌ 错误：未知选项 '$1'"
        echo "使用 --help 查看帮助信息"
        exit 1
        ;;
esac 