#!/usr/bin/env python3
"""
测试 Gemini API (Google AI Studio)
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pull_available_models import fetch_gemini_limits, create_logger

def main():
    logger = create_logger('Gemini')
    
    print('=' * 60)
    print('测试 Gemini API (Google AI Studio)')
    print('=' * 60)
    
    # 检查 GCP_PROJECT_ID
    project_id = os.getenv('GCP_PROJECT_ID')
    if not project_id:
        print('❌ 错误: 未找到 GCP_PROJECT_ID 环境变量')
        print('\n💡 提示: Gemini 配额查询需要 Google Cloud 项目 ID')
        return False
    
    if project_id.startswith('your_'):
        print('⚠️  警告: GCP_PROJECT_ID 使用默认值')
        print('\n💡 提示: 请在 .env 文件中配置真实的 Google Cloud 项目 ID')
        return False
    
    # 检查是否是 API Key 格式（应该是项目 ID）
    if project_id.startswith('AIzaSy'):
        print(f'⚠️  警告: GCP_PROJECT_ID 看起来是 API Key，不是项目 ID')
        print(f'   当前值: {project_id[:20]}...')
        print('\n💡 提示:')
        print('   - GCP_PROJECT_ID 应该是类似 "my-project-123456" 的格式')
        print('   - API Key 不能用于配额查询')
        print('   - 如果只想使用 Gemini API，可以直接调用 Google AI Studio')
        print()
    
    print(f'📋 GCP_PROJECT_ID: {project_id}')
    print()
    
    # 检查是否有 Google Cloud 认证凭证
    credentials_vars = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_CLOUD_KEYFILE_JSON',
    ]
    
    has_credentials = any(os.getenv(var) for var in credentials_vars)
    
    if not has_credentials:
        print('⚠️  警告: 未检测到 Google Cloud 认证凭证')
        print('\n💡 提示: 需要以下任一方式认证:')
        print('   1. 设置 GOOGLE_APPLICATION_CREDENTIALS 环境变量指向服务账号密钥文件')
        print('   2. 运行 gcloud auth application-default login')
        print('   3. 在 Google Cloud Console 中启用 Cloud Quotas API')
        print()
        print('   如果不配置认证，将跳过 Gemini 配额信息获取')
        print()
    
    # 尝试获取 Gemini 配额信息
    print('正在获取 Gemini 配额信息...')
    try:
        gemini_models = fetch_gemini_limits(logger)
        
        if not gemini_models:
            print('\n⚠️  未能获取 Gemini 配额信息')
            print('\n可能的原因:')
            print('   1. 缺少 Google Cloud 认证凭证')
            print('   2. Cloud Quotas API 未启用')
            print('   3. GCP_PROJECT_ID 配置不正确')
            print('   4. 没有足够的权限访问配额信息')
            print('\n💡 建议:')
            print('   - 如果只是使用 Gemini API，可以直接调用 Google AI Studio')
            print('   - 配额查询功能主要用于生成 README 文档')
            print('   - 可以跳过此步骤，不影响其他功能')
            return True
        
        print(f'\n✅ 成功获取 {len(gemini_models)} 个模型的配额信息\n')
        print('模型配额:')
        print('-' * 60)
        
        for model_id, limits in list(gemini_models.items())[:10]:  # 只显示前10个
            print(f'{model_id}:')
            for key, value in limits.items():
                print(f'  - {key}: {value:,}')
            print()
        
        if len(gemini_models) > 10:
            print(f'... 还有 {len(gemini_models) - 10} 个模型')
        
        print('=' * 60)
        return True
        
    except Exception as e:
        print(f'\n❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f'\n❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
