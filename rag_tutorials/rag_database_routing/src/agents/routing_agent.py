"""Routing agent for determining which database to query."""

from typing import Optional, Dict, List, Tuple
from langchain_core.documents import Document

from ..models import get_chat_model
from ..models.config import settings
from ..data import DatabaseType, COLLECTIONS
from ..prompts import get_routing_prompt
from ..tools.base_vector_store import BaseVectorStoreManager


class RoutingAgent:
    """Agent responsible for routing queries to appropriate databases."""
    
    def __init__(self, vector_store_manager: BaseVectorStoreManager):
        """Initialize routing agent."""
        self.llm = get_chat_model()
        self.vector_store = vector_store_manager
        self.confidence_threshold = settings.similarity_threshold
    
    def route_query(self, question: str) -> Optional[DatabaseType]:
        """Route query using hybrid approach: vector similarity + LLM fallback."""
        
        # First try vector similarity routing
        best_db_type = self._vector_similarity_routing(question)
        if best_db_type:
            return best_db_type
            
        # Fallback to LLM routing
        return self._llm_routing(question)
    
    def _vector_similarity_routing(self, question: str) -> Optional[DatabaseType]:
        """Route based on vector similarity scores."""
        try:
            all_results = self.vector_store.search_all_databases(question, k=3)
            
            best_score = -1
            best_db_type = None
            
            for db_type, results in all_results.items():
                if results:
                    # Calculate average similarity score
                    avg_score = sum(score for _, score in results) / len(results)
                    
                    if avg_score > best_score:
                        best_score = avg_score
                        best_db_type = db_type
            
            # Check confidence threshold
            if best_score >= self.confidence_threshold and best_db_type:
                print(f"向量相似性路由: {best_db_type} (置信度: {best_score:.3f})")
                return best_db_type
                
            print(f"置信度低于阈值 ({self.confidence_threshold})，转向LLM路由")
            return None
            
        except Exception as e:
            print(f"向量路由错误: {e}")
            return None
    
    def _llm_routing(self, question: str) -> Optional[DatabaseType]:
        """Route using LLM analysis."""
        try:
            prompt = get_routing_prompt()
            formatted_prompt = prompt.format(question=question)
            
            response = self.llm.invoke(formatted_prompt)
            
            # Extract and clean the response
            content = response.content if isinstance(response.content, str) else str(response.content)
            db_type = (content
                      .strip()
                      .lower()
                      .translate(str.maketrans('', '', '`\'"')))
            
            if db_type in COLLECTIONS:
                print(f"LLM路由决策: {db_type}")
                return db_type
                
            print("LLM路由未找到合适的数据库")
            return None
            
        except Exception as e:
            print(f"LLM路由错误: {e}")
            return None
    
    def get_routing_info(self, question: str) -> Dict:
        """Get detailed routing information for debugging."""
        info = {
            "question": question,
            "vector_scores": {},
            "chosen_database": None,
            "routing_method": None
        }
        
        try:
            # Get vector similarity scores for all databases
            all_results = self.vector_store.search_all_databases(question, k=3)
            
            for db_type, results in all_results.items():
                if results:
                    avg_score = sum(score for _, score in results) / len(results)
                    info["vector_scores"][db_type] = avg_score
            
            # Determine routing
            chosen_db = self.route_query(question)
            info["chosen_database"] = chosen_db
            
            # Determine method used
            if chosen_db and info["vector_scores"].get(chosen_db, 0) >= self.confidence_threshold:
                info["routing_method"] = "vector_similarity"
            elif chosen_db:
                info["routing_method"] = "llm_fallback"
            else:
                info["routing_method"] = "web_search_fallback"
                
        except Exception as e:
            info["error"] = str(e)
            
        return info 