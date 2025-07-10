"""Modern Streamlit app for RAG Database Routing System."""

import streamlit as st
from typing import Dict, Any, Optional
import traceback

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.workflow import RAGWorkflow
from src.data import COLLECTIONS, DatabaseType


class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the Streamlit app."""
        self.workflow: Optional[RAGWorkflow] = None
        
    def run(self):
        """Run the Streamlit application."""
        st.set_page_config(
            page_title="RAG数据库路由系统", 
            page_icon="📚",
            layout="wide"
        )
        
        st.title("📚 RAG数据库路由系统")
        st.markdown("### 基于LangGraph的智能文档检索系统")
        
        # Initialize workflow
        self._initialize_workflow()
        
        if self.workflow is None:
            st.error("❌ 系统初始化失败。请检查环境变量配置。")
            self._show_env_help()
            return
        
        # Main interface
        self._show_document_upload_section()
        self._show_query_section()
    
    def _initialize_workflow(self):
        """Initialize the RAG workflow."""
        if self.workflow is not None:
            return
            
        try:
            with st.spinner("🔄 正在初始化系统..."):
                self.workflow = RAGWorkflow()
            st.success("✅ 系统初始化成功！")
            
        except Exception as e:
            st.error(f"❌ 系统初始化失败: {str(e)}")
            with st.expander("查看详细错误信息"):
                st.code(traceback.format_exc())
            
            # Show configuration help
            self._show_env_help()
    
    def _show_env_help(self):
        """Show environment variable configuration help."""
        st.info("💡 请确保已正确配置环境变量")
        
        with st.expander("🔧 环境变量配置说明"):
            st.markdown("""
            **必需的环境变量:**
            
            1. **OpenAI配置:**
               - `OPENAI_API_KEY`: 您的OpenAI API密钥
               - `OPENAI_MODEL`: 使用的模型（默认: gpt-4o）
               - `EMBEDDING_MODEL`: 嵌入模型（默认: text-embedding-3-small）
            
            2. **Qdrant配置:**
               - `QDRANT_URL`: Qdrant集群URL
               - `QDRANT_API_KEY`: Qdrant API密钥
            
            **配置步骤:**
            1. 复制 `.env.example` 文件为 `.env`
            2. 填入您的实际API密钥和配置
            3. 重启应用程序
            """)
    
    def _show_document_upload_section(self):
        """Show document upload interface."""
        st.header("📄 文档上传")
        st.info("上传文档到不同的数据库集合中，每个标签页对应不同的业务领域。")
        
        # Create tabs for different collections
        tabs = st.tabs([config.name for config in COLLECTIONS.values()])
        
        for (db_type, config), tab in zip(COLLECTIONS.items(), tabs):
            with tab:
                st.write(f"**{config.description}**")
                
                uploaded_files = st.file_uploader(
                    f"上传文档到 {config.name}",
                    type=["pdf", "txt", "md"],
                    key=f"upload_{db_type}",
                    accept_multiple_files=True,
                    help="支持PDF、TXT和Markdown文件"
                )
                
                if uploaded_files:
                    if st.button(f"处理并添加到{config.name}", key=f"process_{db_type}"):
                        self._process_uploaded_files(db_type, uploaded_files)
    
    def _process_uploaded_files(self, db_type: DatabaseType, uploaded_files):
        """Process and add uploaded files to database."""
        with st.spinner(f"🔄 正在处理 {len(uploaded_files)} 个文件..."):
            result = self.workflow.add_documents(db_type, uploaded_files)
        
        if result["success"]:
            st.success(f"✅ {result['message']}")
            
            # Show processing details
            with st.expander("📊 处理详情"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("处理的文件数", len(result["processed_files"]))
                with col2:
                    st.metric("生成的文档块数", result["num_chunks"])
                
                st.write("**处理的文件:**")
                for filename in result["processed_files"]:
                    st.write(f"- {filename}")
        else:
            st.error(f"❌ 处理失败: {result['error']}")
    
    def _show_query_section(self):
        """Show query interface."""
        st.header("❓ 智能问答")
        st.info("输入您的问题，系统将自动路由到最相关的数据库进行检索。")
        
        # Query input
        question = st.text_input(
            "请输入您的问题:",
            placeholder="例如：这个产品有什么特性？",
            help="系统会分析您的问题并自动选择最合适的数据库"
        )
        
        # Query options
        with st.expander("🔧 高级选项"):
            show_routing_info = st.checkbox("显示路由信息", value=True)
            show_sources = st.checkbox("显示文档来源", value=True)
        
        if question:
            with st.spinner("🔍 正在搜索答案..."):
                result = self.workflow.process_question(question)
            
            self._display_query_result(result, show_routing_info, show_sources)
    
    def _display_query_result(
        self, 
        result: Dict[str, Any], 
        show_routing_info: bool, 
        show_sources: bool
    ):
        """Display query result."""
        
        # Main answer
        st.subheader("💡 答案")
        if result["success"]:
            st.write(result["answer"])
        else:
            st.error(f"❌ 查询失败: {result['error']}")
            return
        
        # Routing information
        if show_routing_info:
            with st.expander("🧭 路由信息"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("路由到的数据库", result["routed_database"] or "网络搜索")
                    st.metric("使用的文档数", result["num_documents"])
                
                with col2:
                    routing_info = result.get("routing_info", {})
                    routing_method = routing_info.get("routing_method", "未知")
                    st.write(f"**路由方法:** {routing_method}")
                    
                    # Show vector scores if available
                    vector_scores = routing_info.get("vector_scores", {})
                    if vector_scores:
                        st.write("**向量相似性分数:**")
                        for db, score in vector_scores.items():
                            st.write(f"- {COLLECTIONS[db].name}: {score:.3f}")
        
        # Document sources
        if show_sources and result["documents"]:
            with st.expander(f"📚 文档来源 ({len(result['documents'])} 个)"):
                for i, doc in enumerate(result["documents"][:3], 1):
                    st.write(f"**来源 {i}:**")
                    
                    # Show document preview
                    preview = doc.page_content[:300]
                    if len(doc.page_content) > 300:
                        preview += "..."
                    
                    st.write(f"```\n{preview}\n```")
                    
                    # Show metadata if available
                    if doc.metadata:
                        st.json(doc.metadata)
                    
                    st.divider()


def main():
    """Main entry point for the Streamlit app."""
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main() 