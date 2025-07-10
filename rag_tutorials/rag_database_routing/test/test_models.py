"""测试模型配置和LLM/Embedding组件"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_config():
    """测试配置加载"""
    print("🧪 测试配置加载")
    print("="*40)
    
    try:
        from src.models.config import settings
        
        print(f"✅ 配置加载成功")
        print(f"   OpenAI API Key: {'已设置' if settings.openai_api_key else '未设置'}")
        print(f"   OpenAI Model: {settings.openai_model}")
        print(f"   ARK API Key: {'已设置' if settings.ark_api_key else '未设置'}")
        print(f"   ARK Base URL: {settings.ark_base_url}")
        print(f"   豆包模型: {settings.doubao_embedding_model}")
        print(f"   Qdrant URL: {settings.qdrant_url}")
        print(f"   Qdrant API Key: {'已设置' if settings.qdrant_api_key else '未设置'}")
        
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_llm():
    """测试LLM初始化和调用"""
    print("\n🧪 测试LLM")
    print("="*40)
    
    try:
        from src.models import get_chat_model
        from langchain_core.messages import HumanMessage
        
        print("📝 测试LLM初始化和调用...")
        llm = get_chat_model()
        print(f"   类型: {type(llm).__name__}")
        
        response = llm.invoke([HumanMessage(content="Hello, 请用中文回复")])
        print(f"   响应: {response.content[:100]}...")
            
        return True
    except Exception as e:
        print(f"❌ LLM测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_embeddings():
    """测试Embedding组件"""
    print("\n🧪 测试Embeddings")
    print("="*40)
    
    try:
        from src.models import get_embedding_model
        
        print("📝 测试Embeddings初始化...")
        embeddings = get_embedding_model()
        print(f"   类型: {type(embeddings).__name__}")
        
        test_text = "这是一个测试文本"
        vector = embeddings.embed_query(test_text)
        print(f"   向量维度: {len(vector)}")
        print(f"   前5个值: {vector[:5]}")
        
        # 测试批量处理
        print("\n📝 测试批量embedding...")
        test_docs = ["文档1", "文档2", "文档3"]
        vectors = embeddings.embed_documents(test_docs)
        print(f"   处理文档数: {len(test_docs)}")
        print(f"   生成向量数: {len(vectors)}")
        
        return True
    except Exception as e:
        print(f"❌ Embeddings测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_doubao_embeddings():
    """专门测试豆包embedding"""
    print("\n🧪 测试豆包Embeddings")
    print("="*40)
    
    try:
        from src.models.doubao_embeddings import DoubaoEmbeddings
        from src.models.config import settings
        
        if not settings.ark_api_key:
            print("⚠️ 未配置ARK_API_KEY，跳过豆包测试")
            return True
            
        embeddings = DoubaoEmbeddings(
            model=settings.doubao_embedding_model,
            api_key=settings.ark_api_key,
            base_url=settings.ark_base_url
        )
        
        print("📝 测试单个查询...")
        vector = embeddings.embed_query("人工智能")
        print(f"   向量维度: {len(vector)}")
        print(f"   前5个值: {vector[:5]}")
        
        print("\n📝 测试批量文档...")
        docs = ["人工智能", "机器学习", "深度学习"]
        vectors = embeddings.embed_documents(docs)
        print(f"   文档数: {len(docs)}")
        print(f"   向量数: {len(vectors)}")
        
        # 计算相似性
        import numpy as np
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
        print("\n📝 相似性分析:")
        for i, doc in enumerate(docs):
            similarity = cosine_similarity(vector, vectors[i])
            print(f"   '{doc}' 相似度: {similarity:.4f}")
        
        return True
    except Exception as e:
        print(f"❌ 豆包Embeddings测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有模型测试"""
    print("🔧 RAG数据库路由系统 - 模型测试")
    print("="*50)
    
    tests = [
        ("配置", test_config),
        ("LLM", test_llm),
        ("Embeddings", test_embeddings),
        ("豆包Embeddings", test_doubao_embeddings)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
    
    print("\n📊 测试结果汇总")
    print("="*50)
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\n总体结果: {total_passed}/{total_tests} 通过")

if __name__ == "__main__":
    main() 