"""运行所有测试的主脚本"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_test_module(module_name, module_main):
    """运行单个测试模块"""
    print(f"\n🚀 开始测试: {module_name}")
    print("="*60)
    
    start_time = time.time()
    
    try:
        # 运行测试模块的main函数
        module_main()
        end_time = time.time()
        duration = end_time - start_time
        print(f"\n✅ {module_name} 测试完成，耗时: {duration:.2f}s")
        return True, duration
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\n❌ {module_name} 测试失败: {e}")
        print(f"耗时: {duration:.2f}s")
        import traceback
        traceback.print_exc()
        return False, duration

def main():
    """运行所有测试"""
    print("🧪 RAG数据库路由系统 - 完整测试套件")
    print("="*60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 导入所有测试模块
    test_modules = []
    
    try:
        from test_models import main as test_models_main
        test_modules.append(("模型测试", test_models_main))
    except ImportError as e:
        print(f"⚠️ 无法导入模型测试: {e}")
    
    try:
        from test_tools import main as test_tools_main
        test_modules.append(("工具测试", test_tools_main))
    except ImportError as e:
        print(f"⚠️ 无法导入工具测试: {e}")
    
    try:
        from test_agents import main as test_agents_main
        test_modules.append(("代理测试", test_agents_main))
    except ImportError as e:
        print(f"⚠️ 无法导入代理测试: {e}")
    
    try:
        from test_workflow import main as test_workflow_main
        test_modules.append(("工作流测试", test_workflow_main))
    except ImportError as e:
        print(f"⚠️ 无法导入工作流测试: {e}")
    
    if not test_modules:
        print("❌ 未找到可用的测试模块")
        return
    
    # 运行所有测试
    total_start_time = time.time()
    results = {}
    durations = {}
    
    for module_name, module_main in test_modules:
        success, duration = run_test_module(module_name, module_main)
        results[module_name] = success
        durations[module_name] = duration
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # 生成测试报告
    print("\n" + "="*60)
    print("📊 测试结果总汇")
    print("="*60)
    
    passed_count = 0
    failed_count = 0
    
    for module_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        duration = durations[module_name]
        print(f"{module_name:15} | {status:8} | {duration:6.2f}s")
        
        if success:
            passed_count += 1
        else:
            failed_count += 1
    
    print("-" * 60)
    print(f"总计: {passed_count + failed_count} 个模块")
    print(f"通过: {passed_count} 个")
    print(f"失败: {failed_count} 个")
    print(f"通过率: {passed_count/(passed_count + failed_count)*100:.1f}%")
    print(f"总耗时: {total_duration:.2f}s")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 生成详细报告
    print("\n" + "="*60)
    print("📝 测试建议")
    print("="*60)
    
    if failed_count == 0:
        print("🎉 所有测试都通过了！系统状态良好。")
    else:
        print("⚠️ 有测试失败，建议检查以下方面：")
        
        for module_name, success in results.items():
            if not success:
                print(f"   • {module_name}: 检查相关配置和依赖")
        
        print("\n常见问题解决方案：")
        print("   • 检查 .env 文件中的API密钥配置")
        print("   • 确认网络连接正常")
        print("   • 验证Qdrant服务可访问")
        print("   • 检查依赖包版本兼容性")
    
    print("\n" + "="*60)
    print("🔧 系统状态检查")
    print("="*60)
    
    # 环境检查
    try:
        from src.models.config import settings
        print("📋 配置状态:")
        print(f"   OpenAI API: {'✅' if settings.openai_api_key else '❌'}")
        print(f"   ARK API: {'✅' if settings.ark_api_key else '❌'}")
        print(f"   Qdrant: {'✅' if settings.qdrant_url else '❌'}")
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
    
    # 依赖检查
    print("\n📦 关键依赖:")
    dependencies = [
        "langchain",
        "langchain-openai", 
        "qdrant-client",
        "streamlit",
        "langgraph"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   {dep}: ✅")
        except ImportError:
            print(f"   {dep}: ❌")
    
    # 返回整体结果
    if failed_count == 0:
        print("\n🎯 结论: 系统测试全部通过，可以正常使用！")
        return True
    else:
        print(f"\n⚠️ 结论: {failed_count} 个模块测试失败，需要修复后再使用。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 