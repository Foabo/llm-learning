"""QA agent for answering questions based on retrieved documents."""

from typing import List, Tuple, Optional
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from ..models import get_chat_model
from ..prompts import get_qa_prompt
from ..tools import WebSearchTool
from ..tools.base_vector_store import BaseVectorStoreManager
from ..data import DatabaseType


class QAAgent:
    """Agent responsible for answering questions based on retrieved context."""
    
    def __init__(self, vector_store_manager: BaseVectorStoreManager):
        """Initialize QA agent."""
        self.llm = get_chat_model()
        self.vector_store = vector_store_manager
        self.web_search_tool = WebSearchTool()
    
    def answer_question(
        self, 
        question: str, 
        db_type: Optional[DatabaseType] = None
    ) -> Tuple[str, List[Document]]:
        """Answer question using database or web search fallback."""
        
        if db_type:
            return self._answer_from_database(question, db_type)
        else:
            return self._answer_from_web_search(question)
    
    def _answer_from_database(
        self, 
        question: str, 
        db_type: DatabaseType
    ) -> Tuple[str, List[Document]]:
        """Answer question using specific database."""
        try:
            # Get retriever for the specific database
            retriever = self.vector_store.get_retriever(db_type, k=4)
            
            # Get relevant documents
            relevant_docs = retriever.get_relevant_documents(question)
            
            if not relevant_docs:
                return self._answer_from_web_search(question)
            
            # Create QA chain
            qa_prompt = get_qa_prompt()
            combine_docs_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
            
            # Get answer
            response = retrieval_chain.invoke({"input": question})
            return response['answer'], relevant_docs
            
        except Exception as e:
            error_msg = f"数据库查询出错: {str(e)}. 尝试网络搜索..."
            print(error_msg)
            return self._answer_from_web_search(question)
    
    def _answer_from_web_search(self, question: str) -> Tuple[str, List[Document]]:
        """Answer question using web search."""
        try:
            # Use web search tool
            web_result = self.web_search_tool._run(question)
            
            # Format the response
            answer = f"由于数据库中没有找到相关文档，以下是网络搜索结果：\n\n{web_result}"
            
            return answer, []
            
        except Exception as e:
            # Ultimate fallback - direct LLM response
            try:
                fallback_response = self.llm.invoke(
                    f"请基于你的知识回答以下问题：{question}"
                ).content
                
                answer = f"网络搜索不可用。基于一般知识的回答：\n\n{fallback_response}"
                return answer, []
                
            except Exception as fallback_error:
                return f"抱歉，由于技术问题无法回答您的问题。错误：{str(fallback_error)}", []
    
    def get_detailed_answer(
        self, 
        question: str, 
        db_type: Optional[DatabaseType] = None,
        include_sources: bool = True
    ) -> dict:
        """Get detailed answer with metadata and sources."""
        
        answer, documents = self.answer_question(question, db_type)
        
        result = {
            "question": question,
            "answer": answer,
            "database_used": db_type,
            "num_sources": len(documents),
            "sources": []
        }
        
        if include_sources and documents:
            for i, doc in enumerate(documents[:3]):  # Limit to top 3 sources
                source_info = {
                    "index": i + 1,
                    "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                result["sources"].append(source_info)
        
        return result 