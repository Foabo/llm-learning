"""LangGraph workflow for RAG database routing system."""

from typing import Dict, Any, Optional, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.documents import Document

from .agents import RoutingAgent, QAAgent
from .tools import VectorStoreManager, DocumentProcessor
from .data import DatabaseType


class RAGState(TypedDict):
    """State for the RAG workflow."""
    question: str
    routed_database: Optional[DatabaseType]
    answer: str
    documents: List[Document]
    routing_info: Dict[str, Any]
    error: Optional[str]


class RAGWorkflow:
    """LangGraph workflow for RAG database routing."""
    
    def __init__(self):
        """Initialize the workflow."""
        try:
            self.vector_store_manager = VectorStoreManager()
            print("✅ 成功连接到Qdrant向量数据库")
            
            self.routing_agent = RoutingAgent(self.vector_store_manager)
            self.qa_agent = QAAgent(self.vector_store_manager)
            self.doc_processor = DocumentProcessor()
            
            # Build the workflow graph
            self.workflow = self._build_workflow()
            
        except Exception as e:
            error_msg = f"Failed to initialize RAG workflow: {str(e)}"
            print(f"[ERROR] {error_msg}")
            # 记录详细错误信息
            import traceback
            print(f"[DEBUG] Full traceback: {traceback.format_exc()}")
            raise RuntimeError(error_msg)
    
    def _build_workflow(self) -> CompiledStateGraph:
        """Build the LangGraph workflow."""
        
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("route_query", self._route_query_node)
        workflow.add_node("answer_question", self._answer_question_node)
        workflow.add_node("handle_error", self._handle_error_node)
        
        # Add edges
        workflow.set_entry_point("route_query")
        
        # Conditional routing after query routing
        workflow.add_conditional_edges(
            "route_query",
            self._should_continue_to_qa,
            {
                "answer": "answer_question",
                "error": "handle_error"
            }
        )
        
        # End after answering or handling error
        workflow.add_edge("answer_question", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _route_query_node(self, state: RAGState) -> RAGState:
        """Node for routing the query to appropriate database."""
        try:
            question = state["question"]
            
            # Get routing information
            routing_info = self.routing_agent.get_routing_info(question)
            routed_database = self.routing_agent.route_query(question)
            
            return {
                **state,
                "routed_database": routed_database,
                "routing_info": routing_info,
                "error": None
            }
            
        except Exception as e:
            return {
                **state,
                "error": f"Routing error: {str(e)}",
                "routed_database": None,
                "routing_info": {}
            }
    
    def _answer_question_node(self, state: RAGState) -> RAGState:
        """Node for answering the question."""
        try:
            question = state["question"]
            routed_database = state["routed_database"]
            
            # Get answer and documents
            answer, documents = self.qa_agent.answer_question(question, routed_database)
            
            return {
                **state,
                "answer": answer,
                "documents": documents,
                "error": None
            }
            
        except Exception as e:
            return {
                **state,
                "answer": f"Sorry, I encountered an error while answering: {str(e)}",
                "documents": [],
                "error": f"QA error: {str(e)}"
            }
    
    def _handle_error_node(self, state: RAGState) -> RAGState:
        """Node for handling errors with fallback."""
        try:
            question = state["question"]
            
            # Try web search as fallback
            answer, documents = self.qa_agent._answer_from_web_search(question)
            
            return {
                **state,
                "answer": answer,
                "documents": documents
            }
            
        except Exception as e:
            return {
                **state,
                "answer": f"Sorry, all fallback methods failed. Error: {str(e)}",
                "documents": []
            }
    
    def _should_continue_to_qa(self, state: RAGState) -> str:
        """Decide whether to continue to QA or handle error."""
        if state.get("error"):
            return "error"
        return "answer"
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Process a question through the workflow."""
        initial_state = RAGState(
            question=question,
            routed_database=None,
            answer="",
            documents=[],
            routing_info={},
            error=None
        )
        
        try:
            # Run the workflow
            result = self.workflow.invoke(initial_state)
            
            return {
                "question": result["question"],
                "answer": result["answer"],
                "routed_database": result["routed_database"],
                "num_documents": len(result["documents"]),
                "documents": result["documents"],
                "routing_info": result["routing_info"],
                "success": not result.get("error"),
                "error": result.get("error")
            }
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Workflow execution failed: {str(e)}",
                "routed_database": None,
                "num_documents": 0,
                "documents": [],
                "routing_info": {},
                "success": False,
                "error": str(e)
            }
    
    def add_documents(self, db_type: DatabaseType, uploaded_files: List[Any]) -> Dict[str, Any]:
        """Add documents to a specific database."""
        try:
            all_documents = []
            processed_files = []
            
            for uploaded_file in uploaded_files:
                try:
                    documents = self.doc_processor.process_uploaded_file(uploaded_file)
                    all_documents.extend(documents)
                    processed_files.append(uploaded_file.name)
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Error processing file {uploaded_file.name}: {str(e)}",
                        "processed_files": processed_files
                    }
            
            if all_documents:
                self.vector_store_manager.add_documents(db_type, all_documents)
                
                return {
                    "success": True,
                    "message": f"Successfully processed {len(processed_files)} files and added {len(all_documents)} document chunks to {db_type} database.",
                    "processed_files": processed_files,
                    "num_chunks": len(all_documents)
                }
            else:
                return {
                    "success": False,
                    "error": "No documents were extracted from the uploaded files.",
                    "processed_files": []
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add documents: {str(e)}",
                "processed_files": []
            } 