#!/usr/bin/env python3
import requests

print("测试 DeepSeek V4 Flash (OpenCode Zen)")
print("=" * 60)

try:
    r = requests.post(
        'https://free-llm-api-resources.vercel.app/v1/chat/completions',
        json={
            'model': 'deepseek-v4-flash',
            'messages': [{'role': 'user', 'content': 'Hello!'}],
            'max_tokens': 100
        },
        timeout=60
    )
    
    print(f'状态码: {r.status_code}')
    
    if r.status_code == 200:
        data = r.json()
        print('✅ 成功!')
        print(f'回复: {data["choices"][0]["message"]["content"][:200]}')
    else:
        print(f'❌ 失败: {r.text[:300]}')
        
except Exception as e:
    print(f'❌ 错误: {e}')
