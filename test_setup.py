#!/usr/bin/env python3
"""
测试脚本 - 验证项目配置和 API 端点
"""

import sys
import os
import json

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def test_imports():
    """测试导入是否成功"""
    print("=" * 60)
    print("测试 1: 导入模块")
    print("=" * 60)
    
    try:
        from pull_available_models import (
            fetch_openrouter_models,
            fetch_github_models,
            fetch_samba_models,
            create_logger,
        )
        print("✅ 成功导入所有必需模块")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_lightweight_api():
    """测试轻量级 API"""
    print("\n" + "=" * 60)
    print("测试 2: 轻量级 API")
    print("=" * 60)
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
        from lite import generate_lightweight_model_list
        
        print("正在获取数据...")
        data = generate_lightweight_model_list()
        
        # 验证数据结构
        assert "providers" in data, "缺少 providers 字段"
        assert "timestamp" in data, "缺少 timestamp 字段"
        assert "summary" in data, "缺少 summary 字段"
        
        # 打印摘要
        summary = data["summary"]
        print(f"\n✅ 成功获取数据:")
        print(f"   - 提供商数量: {summary['total_providers']}")
        print(f"   - 模型总数: {summary['total_models']}")
        print(f"   - 获取时间: {summary['fetched_at']}")
        
        # 显示各提供商信息
        for provider_id, provider_data in data["providers"].items():
            print(f"\n   📦 {provider_data['name']}:")
            print(f"      URL: {provider_data['url']}")
            print(f"      模型数: {provider_data.get('model_count', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_files():
    """测试配置文件是否存在"""
    print("\n" + "=" * 60)
    print("测试 3: 配置文件检查")
    print("=" * 60)
    
    required_files = [
        "vercel.json",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "DEPLOYMENT.md",
        "QUICKSTART.md",
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} 不存在")
            all_exist = False
    
    return all_exist


def test_environment():
    """测试环境变量"""
    print("\n" + "=" * 60)
    print("测试 4: 环境变量检查")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = [
        "GROQ_API_KEY",
        "HYPERBOLIC_API_KEY",
        "CLOUDFLARE_ACCOUNT_ID",
        "CLOUDFLARE_API_KEY",
        "LAMBDA_API_KEY",
        "SCALEWAY_API_KEY",
        "COHERE_API_KEY",
        "GCP_PROJECT_ID",
    ]
    
    configured = 0
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # 隐藏实际值，只显示前4个字符
            masked = value[:4] + "*" * (len(value) - 4) if len(value) > 4 else "***"
            print(f"✅ {var}: {masked}")
            configured += 1
        else:
            print(f"⚠️  {var}: 未配置")
    
    print(f"\n已配置: {configured}/{len(env_vars)}")
    
    if configured == 0:
        print("\n💡 提示: 如需使用完整版 API，请配置环境变量")
        print("   复制 .env.example 为 .env 并填入你的密钥")
    
    return True


def main():
    """运行所有测试"""
    print("\n🧪 开始运行测试...\n")
    
    results = []
    
    # 运行测试
    results.append(("导入模块", test_imports()))
    results.append(("配置文件", test_config_files()))
    results.append(("环境变量", test_environment()))
    results.append(("轻量级 API", test_lightweight_api()))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！项目已准备就绪。")
        print("\n下一步:")
        print("  1. 部署到 Vercel: vercel")
        print("  2. 查看文档: DEPLOYMENT.md, QUICKSTART.md")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查上述错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
