"""豆包多模态Embedding实现."""

import os
import requests
from typing import List, Dict, Any, Union
from langchain_core.embeddings import Embeddings


class DoubaoEmbeddings(Embeddings):
    """豆包多模态Embedding类."""
    
    def __init__(
        self, 
        model: str = "doubao-embedding-vision-250615",
        api_key: str = None,
        base_url: str = None,
        **kwargs
    ):
        """初始化豆包Embedding."""
        self.model = model
        self.api_key = api_key or os.getenv("ARK_API_KEY")
        self.base_url = base_url or os.getenv("ARK_BASE_URL", "ark.cn-beijing.volces.com/api/v3")
        
        if not self.api_key:
            raise ValueError("ARK_API_KEY is required for DoubaoEmbeddings")
            
        # 确保base_url格式正确
        if not self.base_url.startswith('http'):
            self.base_url = f"https://{self.base_url}"
            
        self.endpoint = f"{self.base_url}/embeddings/multimodal"
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _create_text_input(self, text: str) -> Dict[str, Any]:
        """创建文本输入格式."""
        return {
            "type": "text",
            "text": text
        }
    
    def _call_api(self, inputs: List[Dict[str, Any]]) -> List[List[float]]:
        """调用豆包API."""
        payload = {
            "model": self.model,
            "encoding_format": "float",
            "input": inputs
        }
        
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🔍 豆包API响应结构: {list(result.keys())}")  # 调试信息
                
                if "data" in result and "embedding" in result["data"]:
                    # 豆包的格式：data.embedding 直接是向量数组
                    embedding = result["data"]["embedding"]
                    if isinstance(embedding, list):
                        # 如果是单个查询，返回包含一个embedding的列表
                        return [embedding] if len(inputs) == 1 else [embedding] * len(inputs)
                    else:
                        raise ValueError(f"embedding应该是数组，但得到: {type(embedding)}")
                else:
                    raise ValueError(f"响应格式不正确，缺少data.embedding: {result}")
            else:
                raise ValueError(f"API call failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """嵌入多个文档."""
        # 豆包API似乎不支持真正的批量处理，需要逐个调用
        embeddings = []
        
        for i, text in enumerate(texts):
            try:
                print(f"🔄 处理文档 {i+1}/{len(texts)}: {text[:50]}{'...' if len(text) > 50 else ''}")
                single_input = [self._create_text_input(text)]
                result = self._call_api(single_input)
                embeddings.append(result[0])
            except Exception as single_error:
                print(f"⚠️ 文档 {i+1} embedding失败: {single_error}")
                # 返回零向量作为fallback
                embeddings.append([0.0] * 2048)  # 豆包向量维度是2048
                
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """嵌入单个查询."""
        input_data = [self._create_text_input(text)]
        try:
            result = self._call_api(input_data)
            return result[0]
        except Exception as e:
            print(f"⚠️ 豆包embedding查询失败: {e}")
            # 返回零向量作为fallback
            return [0.0] * 2048
    
    def embed_multimodal(
        self, 
        text: str = None,
        image_url: str = None, 
        video_url: str = None
    ) -> List[float]:
        """多模态嵌入（支持文本、图片、视频）."""
        inputs = []
        
        if text:
            inputs.append(self._create_text_input(text))
            
        if image_url:
            inputs.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })
            
        if video_url:
            inputs.append({
                "type": "video_url", 
                "video_url": {"url": video_url}
            })
        
        if not inputs:
            raise ValueError("At least one of text, image_url, or video_url must be provided")
            
        try:
            result = self._call_api(inputs)
            # 如果有多个输入，返回第一个结果（或者可以平均）
            return result[0] if result else [0.0] * 1536
        except Exception as e:
            print(f"⚠️ 多模态embedding失败: {e}")
            return [0.0] * 2048 