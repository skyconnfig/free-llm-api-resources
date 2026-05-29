#!/usr/bin/env python3
"""
使用 OpenCode Zen DeepSeek V4 Flash - OpenAI 兼容格式
"""

import requests
import json


def test_opencode_zen_deepseek():
    """
    测试调用 OpenCode Zen 的 DeepSeek V4 Flash Free（OpenAI 兼容格式）
    """
    print("=" * 60)
    print("🚀 测试 OpenCode Zen DeepSeek V4 Flash (OpenAI 兼容)")
    print("=" * 60)
    
    # API URL（Vercel 部署的地址）
    url = "https://free-llm-api-resources.vercel.app/v1/chat/completions"
    
    # 请求数据（完全兼容 OpenAI 格式）
    payload = {
        "model": "deepseek-v4-flash",  # 模型 ID
        "messages": [
            {
                "role": "user",
                "content": "用 Python 写一个简单的计算器函数"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    print("\n📝 请求信息:")
    print(f"   URL: {url}")
    print(f"   模型: {payload['model']}")
    print(f"   消息: {payload['messages'][0]['content'][:50]}...")
    
    try:
        print("\n⏳ 发送请求...")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        print(f"\n📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ 调用成功！\n")
            print("🤖 AI 回复:")
            print("-" * 60)
            
            # 提取回复内容
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(content)
            
            print("-" * 60)
            
            # 显示使用统计
            usage = result.get('usage', {})
            if usage:
                print("\n📊 使用统计:")
                print(f"   - 总 tokens: {usage.get('total_tokens', 'N/A')}")
                print(f"   - 提示 tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   - 完成 tokens: {usage.get('completion_tokens', 'N/A')}")
            
            # 显示模型信息
            model = result.get('model', 'N/A')
            print(f"\n🔧 模型信息: {model}")
            
            return True
            
        else:
            print(f"\n❌ 调用失败")
            print(f"响应内容:\n{response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_openai_sdk():
    """
    使用 OpenAI Python SDK 调用（需要先安装 openai 库）
    """
    print("\n" + "=" * 60)
    print("💻 使用 OpenAI SDK 调用示例")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        # 初始化客户端
        client = OpenAI(
            base_url="https://free-llm-api-resources.vercel.app/v1",
            api_key="not-needed"  # API Key 在服务器端配置
        )
        
        print("\n⏳ 发送请求...")
        
        # 调用 DeepSeek V4 Flash
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "user", "content": "解释一下什么是人工智能"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        print("\n✅ 调用成功！\n")
        print("🤖 AI 回复:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        
        return True
        
    except ImportError:
        print("\n⚠️  未安装 openai 库")
        print("安装命令: pip install openai")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


if __name__ == "__main__":
    print("\n🎯 本脚本演示如何使用 OpenCode Zen DeepSeek V4 Flash")
    print("   通过 OpenAI 兼容格式调用\n")
    
    # 方法 1：使用 requests（推荐）
    test_opencode_zen_deepseek()
    
    # 方法 2：使用 OpenAI SDK（可选）
    # test_with_openai_sdk()
    
    print("\n" + "=" * 60)
    print("✨ 完成！")
    print("=" * 60)
