#!/usr/bin/env python3
"""
测试 Cohere API
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pull_available_models import fetch_cohere_models, create_logger

def main():
    logger = create_logger('Cohere')
    
    print('=' * 60)
    print('测试 Cohere API')
    print('=' * 60)
    
    # 检查 API 密钥
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        print('❌ 错误: 未找到 COHERE_API_KEY 环境变量')
        return False
    
    if api_key.startswith('your_'):
        print('⚠️  警告: API 密钥使用默认值，请配置真实的 API 密钥')
        return False
    
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f'✅ API 密钥已配置: {masked_key}')
    print()
    
    # 获取模型列表
    print('正在获取 Cohere 模型列表...')
    models = fetch_cohere_models(logger)
    
    if not models:
        print('❌ 未能获取到任何模型')
        return False
    
    print(f'\n✅ 成功获取 {len(models)} 个 Cohere 聊天模型\n')
    print('模型列表:')
    print('-' * 60)
    
    for i, model in enumerate(models, 1):
        model_id = model.get('id', 'N/A')
        model_name = model.get('name', 'N/A')
        print(f'{i}. {model_name}')
        print(f'   ID: {model_id}')
        print()
    
    # 显示统计信息
    print('=' * 60)
    print(f'📊 总计: {len(models)} 个可用的 Cohere 聊天模型')
    print('=' * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f'\n❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
