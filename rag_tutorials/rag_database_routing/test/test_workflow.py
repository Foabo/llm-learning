"""测试LangGraph工作流"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_workflow_state():
    """测试工作流状态"""
    print("🧪 测试工作流状态")
    print("="*40)
    
    try:
        from src.workflow import State
        
        # 创建测试状态
        test_state = State(
            question="什么是人工智能？",
            database_type=None,
            documents=[],
            answer=None,
            error=None
        )
        
        print(f"✅ 工作流状态创建成功")
        print(f"   问题: {test_state['question']}")
        print(f"   数据库类型: {test_state['database_type']}")
        print(f"   文档数量: {len(test_state['documents'])}")
        print(f"   答案: {test_state['answer']}")
        print(f"   错误: {test_state['error']}")
        
        # 测试状态更新
        test_state['database_type'] = 'products'
        test_state['documents'] = [{'doc': '测试文档', 'score': 0.9}]
        test_state['answer'] = '这是一个测试答案'
        
        print(f"\n📝 测试状态更新...")
        print(f"   更新后数据库类型: {test_state['database_type']}")
        print(f"   更新后文档数量: {len(test_state['documents'])}")
        print(f"   更新后答案: {test_state['answer']}")
        
        return True
    except Exception as e:
        print(f"❌ 工作流状态测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_nodes():
    """测试工作流节点"""
    print("\n🧪 测试工作流节点")
    print("="*40)
    
    try:
        from src.workflow import (
            route_query, 
            search_documents, 
            generate_answer, 
            handle_error,
            State
        )
        
        # 测试路由节点
        print("📝 测试路由节点...")
        route_state = State(
            question="产品有什么功能？",
            database_type=None,
            documents=[],
            answer=None,
            error=None
        )
        
        try:
            updated_route_state = route_query(route_state)
            print(f"   路由结果: {updated_route_state.get('database_type', 'None')}")
        except Exception as e:
            print(f"   路由节点错误: {e}")
        
        # 测试搜索节点
        print("\n📝 测试搜索节点...")
        search_state = State(
            question="产品功能介绍",
            database_type="products",
            documents=[],
            answer=None,
            error=None
        )
        
        try:
            updated_search_state = search_documents(search_state)
            docs = updated_search_state.get('documents', [])
            print(f"   搜索结果: {len(docs)} 个文档")
            if docs:
                print(f"   第一个文档预览: {str(docs[0])[:100]}...")
        except Exception as e:
            print(f"   搜索节点错误: {e}")
        
        # 测试答案生成节点
        print("\n📝 测试答案生成节点...")
        answer_state = State(
            question="产品有什么特点？",
            database_type="products",
            documents=[
                {"document": "产品具有AI功能", "score": 0.9, "metadata": {}}
            ],
            answer=None,
            error=None
        )
        
        try:
            updated_answer_state = generate_answer(answer_state)
            answer = updated_answer_state.get('answer', 'None')
            print(f"   生成答案: {answer}")
        except Exception as e:
            print(f"   答案生成节点错误: {e}")
        
        # 测试错误处理节点
        print("\n📝 测试错误处理节点...")
        error_state = State(
            question="测试问题",
            database_type=None,
            documents=[],
            answer=None,
            error="模拟错误"
        )
        
        try:
            updated_error_state = handle_error(error_state)
            answer = updated_error_state.get('answer', 'None')
            print(f"   错误处理结果: {answer}")
        except Exception as e:
            print(f"   错误处理节点错误: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 工作流节点测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_graph():
    """测试完整工作流图"""
    print("\n🧪 测试完整工作流图")
    print("="*40)
    
    try:
        from src.workflow import create_workflow
        
        # 创建工作流图
        workflow = create_workflow()
        print(f"✅ 工作流图创建成功")
        print(f"   图类型: {type(workflow).__name__}")
        
        # 测试工作流编译
        print("\n📝 测试工作流编译...")
        try:
            app = workflow.compile()
            print(f"   编译成功: {type(app).__name__}")
        except Exception as e:
            print(f"   编译失败: {e}")
            return False
        
        # 测试简单查询
        print("\n📝 测试简单查询...")
        test_questions = [
            "产品有什么功能？",
            "如何联系客服？",
            "财务状况如何？"
        ]
        
        for question in test_questions:
            try:
                print(f"   问题: '{question}'")
                
                # 创建初始状态
                initial_state = {
                    "question": question,
                    "database_type": None,
                    "documents": [],
                    "answer": None,
                    "error": None
                }
                
                # 运行工作流
                result = app.invoke(initial_state)
                
                print(f"   结果类型: {type(result)}")
                if isinstance(result, dict):
                    print(f"   数据库类型: {result.get('database_type', 'None')}")
                    print(f"   文档数量: {len(result.get('documents', []))}")
                    print(f"   答案: {result.get('answer', 'None')[:100]}...")
                    if result.get('error'):
                        print(f"   错误: {result.get('error')}")
                print()
                
            except Exception as e:
                print(f"   查询失败: {e}")
                print()
        
        return True
    except Exception as e:
        print(f"❌ 工作流图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_conditions():
    """测试工作流条件判断"""
    print("\n🧪 测试工作流条件判断")
    print("="*40)
    
    try:
        from src.workflow import should_search, should_answer
        
        print("📝 测试搜索条件...")
        
        # 测试成功路由的情况
        success_state = {
            "database_type": "products",
            "error": None
        }
        search_decision = should_search(success_state)
        print(f"   成功路由 -> 搜索决策: {search_decision}")
        
        # 测试路由失败的情况
        failed_state = {
            "database_type": None,
            "error": "路由失败"
        }
        search_decision = should_search(failed_state)
        print(f"   失败路由 -> 搜索决策: {search_decision}")
        
        print("\n📝 测试答案生成条件...")
        
        # 测试有文档的情况
        with_docs_state = {
            "documents": [{"doc": "test"}],
            "error": None
        }
        answer_decision = should_answer(with_docs_state)
        print(f"   有文档 -> 答案决策: {answer_decision}")
        
        # 测试无文档的情况
        no_docs_state = {
            "documents": [],
            "error": None
        }
        answer_decision = should_answer(no_docs_state)
        print(f"   无文档 -> 答案决策: {answer_decision}")
        
        return True
    except Exception as e:
        print(f"❌ 工作流条件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_performance():
    """测试工作流性能"""
    print("\n🧪 测试工作流性能")
    print("="*40)
    
    try:
        from src.workflow import create_workflow
        import time
        
        # 创建并编译工作流
        workflow = create_workflow()
        app = workflow.compile()
        
        print("📝 测试工作流执行时间...")
        
        test_question = "产品功能测试"
        initial_state = {
            "question": test_question,
            "database_type": None,
            "documents": [],
            "answer": None,
            "error": None
        }
        
        # 多次执行测试
        execution_times = []
        num_tests = 3
        
        for i in range(num_tests):
            start_time = time.time()
            
            try:
                result = app.invoke(initial_state)
                end_time = time.time()
                execution_time = end_time - start_time
                execution_times.append(execution_time)
                
                print(f"   执行 {i+1}: {execution_time:.3f}s")
                
            except Exception as e:
                print(f"   执行 {i+1} 失败: {e}")
        
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            
            print(f"\n📊 性能统计:")
            print(f"   平均时间: {avg_time:.3f}s")
            print(f"   最短时间: {min_time:.3f}s")
            print(f"   最长时间: {max_time:.3f}s")
        
        return True
    except Exception as e:
        print(f"❌ 工作流性能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有工作流测试"""
    print("🔧 RAG数据库路由系统 - 工作流测试")
    print("="*50)
    
    tests = [
        ("工作流状态", test_workflow_state),
        ("工作流节点", test_workflow_nodes),
        ("工作流图", test_workflow_graph),
        ("工作流条件", test_workflow_conditions),
        ("工作流性能", test_workflow_performance)
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