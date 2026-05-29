#!/usr/bin/env python3
"""
测试所有供应商的 OpenAI 兼容 API
"""

import requests
import json


def test_openai_endpoint():
    """测试 OpenAI 兼容端点"""
    print("=" * 60)
    print("🧪 测试 OpenAI 兼容 API")
    print("=" * 60)
    
    base_url = "https://free-llm-api-resources.vercel.app/v1"
    
    # 测试 1: 获取模型列表
    print("\n1️⃣  测试获取模型列表 (/v1/models)")
    print("-" * 60)
    
    try:
        response = requests.get(f"{base_url}/models", timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print(f"✅ 成功获取 {len(models)} 个模型\n")
            
            for model in models:
                print(f"   • {model['id']} ({model['owned_by']})")
                print(f"     {model['description']}")
        else:
            print(f"❌ 失败: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False
    
    # 测试 2: 调用 Groq Llama 3.1（最稳定）
    print("\n2️⃣  测试 Groq Llama 3.1")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b",
                "messages": [
                    {"role": "user", "content": "用一句话介绍你自己"}
                ],
                "max_tokens": 100,
                "temperature": 0.5
            },
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"✅ 调用成功\n")
            print(f"回复: {content[:200]}")
            
            usage = result.get('usage', {})
            if usage:
                print(f"\nTokens: {usage.get('total_tokens', 'N/A')}")
        else:
            print(f"❌ 失败: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试 3: 调用 OpenCode Zen DeepSeek V4 Flash
    print("\n3️⃣  测试 OpenCode Zen DeepSeek V4 Flash")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "deepseek-v4-flash",
                "messages": [
                    {"role": "user", "content": "Hello!"}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            },
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"✅ 调用成功\n")
            print(f"回复: {content[:200]}")
        else:
            print(f"❌ 失败: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试 4: 调用 Cohere Command R
    print("\n4️⃣  测试 Cohere Command R")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "command-r",
                "messages": [
                    {"role": "user", "content": "Hi there!"}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            },
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"✅ 调用成功\n")
            print(f"回复: {content[:200]}")
        else:
            print(f"❌ 失败: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 60)
    print("✨ 测试完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_openai_endpoint()
