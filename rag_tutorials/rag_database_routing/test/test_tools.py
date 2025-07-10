"""测试工具组件：向量存储、文档处理、网络搜索"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_vector_store():
    """测试向量存储管理器"""
    print("🧪 测试向量存储")
    print("="*40)
    
    try:
        from src.tools.vector_store import VectorStoreManager
        from src.models import get_embeddings
        
        # 初始化向量存储管理器
        embeddings = get_embeddings()
        manager = VectorStoreManager(embeddings=embeddings)
        
        print(f"✅ 向量存储管理器初始化成功")
        print(f"   Embedding类型: {type(embeddings).__name__}")
        print(f"   Qdrant客户端: {type(manager.client).__name__}")
        
        # 测试集合操作
        print("\n📝 测试集合操作...")
        test_collection = "test_products"
        
        # 创建集合
        manager.create_collection(test_collection)
        print(f"   集合 '{test_collection}' 创建成功")
        
        # 测试文档添加
        print("\n📝 测试文档添加...")
        test_docs = [
            "这是第一个产品文档",
            "这是第二个产品文档", 
            "这是第三个产品文档"
        ]
        
        doc_ids = []
        for i, doc in enumerate(test_docs):
            doc_id = manager.add_document(test_collection, doc, {"id": i, "type": "product"})
            doc_ids.append(doc_id)
            print(f"   文档 {i+1} 添加成功，ID: {doc_id}")
        
        # 测试搜索
        print("\n📝 测试相似性搜索...")
        query = "产品文档"
        results = manager.search_similar(test_collection, query, limit=2)
        print(f"   查询: '{query}'")
        print(f"   返回结果数: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"   结果 {i+1}: 分数={result.get('score', 'N/A'):.4f}")
            print(f"            文档={result.get('document', 'N/A')[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 向量存储测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_document_processor():
    """测试文档处理器"""
    print("\n🧪 测试文档处理")
    print("="*40)
    
    try:
        from src.tools.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print(f"✅ 文档处理器初始化成功")
        print(f"   分块大小: {processor.chunk_size}")
        print(f"   重叠大小: {processor.chunk_overlap}")
        
        # 测试文本分割
        print("\n📝 测试文本分割...")
        test_text = """
        这是一个长文档的示例。它包含多个段落和句子。
        文档处理器需要将其分割成合适的块。
        
        第二段落包含更多的内容。我们需要确保分割是合理的。
        每个块应该有适当的大小，并且保持语义的完整性。
        
        第三段落是为了测试重叠功能。重叠可以帮助保持上下文。
        这样可以避免重要信息在分割时丢失。
        """
        
        chunks = processor.split_text(test_text)
        print(f"   原文长度: {len(test_text)} 字符")
        print(f"   分割块数: {len(chunks)}")
        
        for i, chunk in enumerate(chunks):
            print(f"   块 {i+1}: {len(chunk)} 字符")
            print(f"        内容: {chunk[:100].strip()}...")
        
        # 测试文件处理
        print("\n📝 测试文件类型检测...")
        test_files = [
            "document.pdf",
            "text.txt", 
            "readme.md",
            "data.csv"
        ]
        
        for filename in test_files:
            file_type = processor.get_file_type(filename)
            supported = processor.is_supported_file(filename)
            print(f"   {filename}: 类型={file_type}, 支持={supported}")
        
        return True
    except Exception as e:
        print(f"❌ 文档处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_search():
    """测试网络搜索工具"""
    print("\n🧪 测试网络搜索")
    print("="*40)
    
    try:
        from src.tools.web_search import WebSearchTool
        
        search_tool = WebSearchTool()
        print(f"✅ 网络搜索工具初始化成功")
        
        # 测试搜索功能
        print("\n📝 测试网络搜索...")
        query = "人工智能最新发展"
        
        print(f"   搜索查询: '{query}'")
        results = search_tool.search(query, max_results=3)
        
        if results:
            print(f"   返回结果数: {len(results)}")
            for i, result in enumerate(results):
                print(f"   结果 {i+1}:")
                print(f"     标题: {result.get('title', 'N/A')[:80]}...")
                print(f"     链接: {result.get('link', 'N/A')}")
                print(f"     摘要: {result.get('snippet', 'N/A')[:100]}...")
        else:
            print("   未返回搜索结果")
        
        # 测试搜索格式化
        print("\n📝 测试结果格式化...")
        formatted = search_tool.format_results(results)
        print(f"   格式化结果长度: {len(formatted)} 字符")
        print(f"   格式化内容预览: {formatted[:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ 网络搜索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """测试工具集成"""
    print("\n🧪 测试工具集成")
    print("="*40)
    
    try:
        from src.tools.vector_store import VectorStoreManager
        from src.tools.document_processor import DocumentProcessor
        from src.models import get_embeddings
        
        # 集成测试：文档处理 + 向量存储
        embeddings = get_embeddings()
        processor = DocumentProcessor()
        manager = VectorStoreManager(embeddings=embeddings)
        
        print("📝 测试文档处理到向量存储的完整流程...")
        
        # 模拟文档内容
        document_content = """
        人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
        机器学习是人工智能的一个子集，它使计算机能够从数据中学习，而无需明确编程。
        深度学习是机器学习的一个专门领域，使用神经网络来模拟人脑的工作方式。
        自然语言处理（NLP）是人工智能的另一个重要分支，专注于使计算机理解和生成人类语言。
        """
        
        collection_name = "test_integration"
        
        # 1. 处理文档
        chunks = processor.split_text(document_content)
        print(f"   文档分割: {len(chunks)} 个块")
        
        # 2. 创建集合
        manager.create_collection(collection_name)
        print(f"   集合创建: {collection_name}")
        
        # 3. 添加到向量存储
        doc_ids = []
        for i, chunk in enumerate(chunks):
            doc_id = manager.add_document(
                collection_name, 
                chunk, 
                {"chunk_id": i, "source": "test_doc"}
            )
            doc_ids.append(doc_id)
        print(f"   文档添加: {len(doc_ids)} 个向量")
        
        # 4. 测试检索
        test_queries = [
            "什么是人工智能？",
            "机器学习如何工作？",
            "深度学习和神经网络"
        ]
        
        print("\n📝 测试检索效果...")
        for query in test_queries:
            results = manager.search_similar(collection_name, query, limit=2)
            print(f"   查询: '{query}'")
            if results:
                best_result = results[0]
                print(f"   最佳匹配: 分数={best_result.get('score', 0):.4f}")
                print(f"            内容={best_result.get('document', '')[:80]}...")
            else:
                print(f"   无匹配结果")
        
        return True
    except Exception as e:
        print(f"❌ 工具集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有工具测试"""
    print("🔧 RAG数据库路由系统 - 工具测试")
    print("="*50)
    
    tests = [
        ("向量存储", test_vector_store),
        ("文档处理", test_document_processor),
        ("网络搜索", test_web_search),
        ("工具集成", test_integration)
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