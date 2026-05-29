#!/usr/bin/env python3
import requests
import json

print("直接测试 OpenCode Zen API")
print("=" * 60)

API_KEY = "sk-NEflLdzc059Ja2D5zlJRKy8YzEm5xW4hzP1DNWjIMfZVEAskD0ndcGZKtMwDw4zn"

try:
    r = requests.post(
        'https://opencode.ai/zen/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'deepseek-v4-flash-free',
            'messages': [{'role': 'user', 'content': '用 Python 写一个 hello world'}],
            'max_tokens': 150,
            'stream': False  # 禁用 stream 模式
        },
        timeout=30
    )
    
    print(f'状态码: {r.status_code}\n')
    
    if r.status_code == 200:
        data = r.json()
        print('✅ 成功!\n')
        print('回复:')
        print(data['choices'][0]['message']['content'])
        print(f'\nTokens: {data.get("usage", {})}')
    else:
        print(f'❌ 失败:')
        print(r.text[:500])
        
except Exception as e:
    print(f' 错误: {e}')
    import traceback
    traceback.print_exc()
