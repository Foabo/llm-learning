"""测试智能代理：路由代理和问答代理"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_routing_agent():
    """测试路由代理"""
    print("🧪 测试路由代理")
    print("="*40)
    
    try:
        from src.agents.routing_agent import RoutingAgent
        from src.models import get_llm
        
        # 初始化路由代理
        llm = get_llm()
        agent = RoutingAgent(llm=llm)
        
        print(f"✅ 路由代理初始化成功")
        print(f"   LLM类型: {type(llm).__name__}")
        
        # 测试不同类型的问题路由
        test_queries = [
            "我想了解产品功能和特性",
            "客服支持怎么联系？遇到问题怎么办？",
            "财务成本和收入情况如何？",
            "今天天气怎么样？",  # 非特定类别的问题
        ]
        
        print("\n📝 测试路由决策...")
        for query in test_queries:
            try:
                result = agent.route(query)
                print(f"   问题: '{query}'")
                print(f"   路由: {result}")
                print()
            except Exception as e:
                print(f"   问题: '{query}'")
                print(f"   错误: {e}")
                print()
        
        return True
    except Exception as e:
        print(f"❌ 路由代理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qa_agent():
    """测试问答代理"""
    print("\n🧪 测试问答代理")
    print("="*40)
    
    try:
        from src.agents.qa_agent import QAAgent
        from src.models import get_llm
        
        # 初始化问答代理
        llm = get_llm()
        agent = QAAgent(llm=llm)
        
        print(f"✅ 问答代理初始化成功")
        print(f"   LLM类型: {type(llm).__name__}")
        
        # 测试问答功能
        print("\n📝 测试问答功能...")
        
        # 模拟检索到的上下文
        mock_context = [
            {
                "document": "我们的产品具有AI驱动的智能分析功能，支持实时数据处理和可视化。",
                "score": 0.95,
                "metadata": {"source": "product_manual.pdf", "page": 1}
            },
            {
                "document": "产品还包括自动化工作流程，可以大大提高工作效率。",
                "score": 0.87,
                "metadata": {"source": "product_features.md", "page": 1}
            }
        ]
        
        test_questions = [
            "产品有什么功能？",
            "如何提高工作效率？",
            "支持实时处理吗？"
        ]
        
        for question in test_questions:
            try:
                answer = agent.answer(question, mock_context)
                print(f"   问题: '{question}'")
                print(f"   回答: {answer}")
                print()
            except Exception as e:
                print(f"   问题: '{question}'")
                print(f"   错误: {e}")
                print()
        
        return True
    except Exception as e:
        print(f"❌ 问答代理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_integration():
    """测试代理集成"""
    print("\n🧪 测试代理集成")
    print("="*40)
    
    try:
        from src.agents.routing_agent import RoutingAgent
        from src.agents.qa_agent import QAAgent
        from src.tools.vector_store import VectorStoreManager
        from src.models import get_llm, get_embeddings
        
        # 初始化组件
        llm = get_llm()
        embeddings = get_embeddings()
        
        routing_agent = RoutingAgent(llm=llm)
        qa_agent = QAAgent(llm=llm)
        vector_store = VectorStoreManager(embeddings=embeddings)
        
        print(f"✅ 代理集成初始化成功")
        
        # 模拟完整的问答流程
        print("\n📝 测试完整问答流程...")
        
        # 1. 准备测试数据
        test_collection = "test_knowledge"
        vector_store.create_collection(test_collection)
        
        # 添加一些测试文档
        test_docs = [
            "我们的产品支持多种数据格式，包括CSV、JSON、XML等。",
            "客服团队24小时在线，可以通过电话、邮件、在线聊天联系。",
            "公司去年收入增长了25%，主要来源于新产品销售。"
        ]
        
        for i, doc in enumerate(test_docs):
            vector_store.add_document(
                test_collection, 
                doc, 
                {"doc_id": i, "category": ["products", "support", "finance"][i]}
            )
        
        # 2. 测试完整流程
        test_question = "产品支持什么数据格式？"
        
        print(f"   问题: '{test_question}'")
        
        # 步骤1：路由决策
        route_result = routing_agent.route(test_question)
        print(f"   路由结果: {route_result}")
        
        # 步骤2：向量检索
        search_results = vector_store.search_similar(
            test_collection, 
            test_question, 
            limit=3
        )
        print(f"   检索结果: {len(search_results)} 个")
        
        # 步骤3：生成答案
        if search_results:
            answer = qa_agent.answer(test_question, search_results)
            print(f"   最终答案: {answer}")
        else:
            print(f"   无法找到相关信息")
        
        return True
    except Exception as e:
        print(f"❌ 代理集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_templates():
    """测试提示词模板"""
    print("\n🧪 测试提示词模板")
    print("="*40)
    
    try:
        from src.prompts.routing_prompts import get_routing_prompt, get_qa_prompt
        
        print("📝 测试路由提示词...")
        routing_prompt = get_routing_prompt()
        print(f"   路由提示词长度: {len(routing_prompt)} 字符")
        print(f"   内容预览: {routing_prompt[:200]}...")
        
        print("\n📝 测试问答提示词...")
        context = "这是一些上下文信息..."
        question = "这是一个测试问题？"
        qa_prompt = get_qa_prompt(context, question)
        print(f"   问答提示词长度: {len(qa_prompt)} 字符")
        print(f"   内容预览: {qa_prompt[:200]}...")
        
        # 测试提示词格式化
        print("\n📝 测试提示词变量替换...")
        test_context = "产品具有AI功能"
        test_question = "产品有什么特点？"
        
        formatted_prompt = get_qa_prompt(test_context, test_question)
        
        # 检查变量是否被正确替换
        if test_context in formatted_prompt and test_question in formatted_prompt:
            print("   ✅ 变量替换成功")
        else:
            print("   ❌ 变量替换失败")
        
        return True
    except Exception as e:
        print(f"❌ 提示词模板测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有代理测试"""
    print("🔧 RAG数据库路由系统 - 代理测试")
    print("="*50)
    
    tests = [
        ("路由代理", test_routing_agent),
        ("问答代理", test_qa_agent),
        ("代理集成", test_agent_integration),
        ("提示词模板", test_prompt_templates)
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