#!/usr/bin/env python3
"""
API 密钥验证测试脚本
测试已配置的 API 密钥是否有效
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pull_available_models import (
    fetch_groq_models,
    fetch_hyperbolic_models,
    fetch_cloudflare_models,
    create_logger,
)


def test_api_key(name, env_var, required=True):
    """测试单个 API 密钥是否配置"""
    value = os.getenv(env_var)
    if value:
        if value.startswith('your_') or value == 'your_gcp_project_id':
            print(f"⚠️  {name}: 未配置（使用默认值）")
            return False
        else:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {name}: 已配置 ({masked})")
            return True
    else:
        status = "⚠️" if not required else "❌"
        print(f"{status} {name}: 未设置")
        return required == False


def main():
    print("=" * 70)
    print("API 密钥配置检查")
    print("=" * 70)
    print()
    
    # 检查 API 密钥配置
    configured_keys = []
    
    configured_keys.append(test_api_key("Groq", "GROQ_API_KEY", required=False))
    configured_keys.append(test_api_key("Hyperbolic", "HYPERBOLIC_API_KEY", required=False))
    configured_keys.append(test_api_key("Cloudflare Account ID", "CLOUDFLARE_ACCOUNT_ID", required=False))
    configured_keys.append(test_api_key("Cloudflare API Key", "CLOUDFLARE_API_KEY", required=False))
    configured_keys.append(test_api_key("Lambda Labs", "LAMBDA_API_KEY", required=False))
    configured_keys.append(test_api_key("Scaleway", "SCALEWAY_API_KEY", required=False))
    configured_keys.append(test_api_key("Cohere", "COHERE_API_KEY", required=False))
    configured_keys.append(test_api_key("GCP Project ID", "GCP_PROJECT_ID", required=False))
    
    print()
    print("=" * 70)
    print("API 连接测试")
    print("=" * 70)
    print()
    
    logger = create_logger("Test")
    
    # 测试 Groq
    if os.getenv('GROQ_API_KEY') and not os.getenv('GROQ_API_KEY').startswith('your_'):
        print("🔄 测试 Groq API...")
        try:
            groq_models = fetch_groq_models(logger)
            if groq_models:
                print(f"✅ Groq: 成功获取 {len(groq_models)} 个模型")
                # 显示前3个模型
                for model in groq_models[:3]:
                    print(f"   - {model['name']}")
                if len(groq_models) > 3:
                    print(f"   ... 还有 {len(groq_models) - 3} 个模型")
            else:
                print("⚠️  Groq: 未返回模型（可能是 API 密钥无效或无免费模型）")
        except Exception as e:
            print(f"❌ Groq: 测试失败 - {e}")
    else:
        print("⏭️  Groq: 跳过（未配置）")
    
    print()
    
    # 测试 Hyperbolic
    if os.getenv('HYPERBOLIC_API_KEY') and not os.getenv('HYPERBOLIC_API_KEY').startswith('your_'):
        print("🔄 测试 Hyperbolic API...")
        try:
            hyper_models = fetch_hyperbolic_models(logger)
            if hyper_models:
                print(f"✅ Hyperbolic: 成功获取 {len(hyper_models)} 个模型")
                for model in hyper_models[:3]:
                    print(f"   - {model['name']}")
                if len(hyper_models) > 3:
                    print(f"   ... 还有 {len(hyper_models) - 3} 个模型")
            else:
                print("⚠️  Hyperbolic: 未返回模型（可能是 API 密钥无效或无免费模型）")
        except Exception as e:
            print(f"❌ Hyperbolic: 测试失败 - {e}")
    else:
        print("⏭️  Hyperbolic: 跳过（未配置）")
    
    print()
    
    # 测试 Cloudflare
    if (os.getenv('CLOUDFLARE_ACCOUNT_ID') and not os.getenv('CLOUDFLARE_ACCOUNT_ID').startswith('your_') and
        os.getenv('CLOUDFLARE_API_KEY') and not os.getenv('CLOUDFLARE_API_KEY').startswith('your_')):
        print("🔄 测试 Cloudflare API...")
        try:
            cf_models = fetch_cloudflare_models(logger)
            if cf_models:
                print(f"✅ Cloudflare: 成功获取 {len(cf_models)} 个模型")
                for model in cf_models[:3]:
                    print(f"   - {model['name']}")
                if len(cf_models) > 3:
                    print(f"   ... 还有 {len(cf_models) - 3} 个模型")
            else:
                print("⚠️  Cloudflare: 未返回模型（可能是 API 密钥无效）")
        except Exception as e:
            print(f"❌ Cloudflare: 测试失败 - {e}")
    else:
        print("⏭️  Cloudflare: 跳过（未配置）")
    
    print()
    print("=" * 70)
    print("总结")
    print("=" * 70)
    
    total_configured = sum(configured_keys)
    print(f"\n已配置的 API 密钥: {total_configured}/{len(configured_keys)}")
    
    if total_configured > 0:
        print("\n✅ 项目已准备好部署到 GitHub 和 Vercel！")
        print("\n下一步:")
        print("  1. 将代码推送到 GitHub")
        print("  2. 在 Vercel 中导入项目")
        print("  3. 在 Vercel 控制台配置环境变量（不要提交 .env 文件）")
        print("  4. 部署完成！")
    else:
        print("\n⚠️  尚未配置任何 API 密钥")
        print("   轻量版 API 仍可正常工作（无需密钥）")
    
    print()


if __name__ == "__main__":
    main()
