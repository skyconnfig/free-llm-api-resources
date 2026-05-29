#!/usr/bin/env python3
"""
Vercel API 端点 - 获取免费 LLM API 资源列表
此文件作为 Vercel Serverless Function 的入口点
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# 添加 src 目录到路径以便导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pull_available_models import (
    fetch_openrouter_models,
    fetch_groq_models,
    fetch_hyperbolic_models,
    fetch_cloudflare_models,
    fetch_github_models,
    fetch_samba_models,
    fetch_scaleway_models,
    fetch_cohere_models,
    fetch_gemini_limits,
    create_logger,
)


def generate_model_list():
    """
    生成模型列表数据
    返回包含所有可用模型的 JSON 数据
    """
    # 创建日志记录器
    logger = create_logger("API")
    
    result = {
        "providers": {},
        "timestamp": None
    }
    
    # 1. OpenRouter - 免费模型聚合平台
    # API: https://openrouter.ai/api/v1/models
    try:
        logger.info("正在获取 OpenRouter 模型...")
        openrouter_models = fetch_openrouter_models(logger)
        if openrouter_models:
            result["providers"]["openrouter"] = {
                "name": "OpenRouter",
                "url": "https://openrouter.ai",
                "description": "免费模型聚合平台，提供多种开源模型",
                "limits": {
                    "requests_per_minute": 20,
                    "requests_per_day": 50,
                    "note": "充值$10后每日最多1000次请求"
                },
                "models": openrouter_models
            }
            logger.info(f"成功获取 {len(openrouter_models)} 个 OpenRouter 模型")
    except Exception as e:
        logger.error(f"获取 OpenRouter 模型失败: {e}")
    
    # 2. Groq - 高速推理平台
    # API: https://api.groq.com/openai/v1/models
    try:
        logger.info("正在获取 Groq 模型...")
        groq_models = fetch_groq_models(logger)
        if groq_models:
            result["providers"]["groq"] = {
                "name": "Groq",
                "url": "https://console.groq.com",
                "description": "超高速 AI 推理平台",
                "models": groq_models
            }
            logger.info(f"成功获取 {len(groq_models)} 个 Groq 模型")
    except Exception as e:
        logger.error(f"获取 Groq 模型失败: {e}")
    
    # 3. Hyperbolic - 去中心化 AI 计算平台
    # API: https://api.hyperbolic.xyz/v1/models
    try:
        logger.info("正在获取 Hyperbolic 模型...")
        hyperbolic_models = fetch_hyperbolic_models(logger)
        if hyperbolic_models:
            result["providers"]["hyperbolic"] = {
                "name": "Hyperbolic",
                "url": "https://app.hyperbolic.ai",
                "description": "去中心化 AI 计算网络",
                "limits": {
                    "requests_per_minute": 60
                },
                "models": hyperbolic_models
            }
            logger.info(f"成功获取 {len(hyperbolic_models)} 个 Hyperbolic 模型")
    except Exception as e:
        logger.error(f"获取 Hyperbolic 模型失败: {e}")
    
    # 4. Cloudflare Workers AI - 边缘 AI 推理
    # API: https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/models/search
    try:
        logger.info("正在获取 Cloudflare 模型...")
        cloudflare_models = fetch_cloudflare_models(logger)
        if cloudflare_models:
            result["providers"]["cloudflare"] = {
                "name": "Cloudflare Workers AI",
                "url": "https://developers.cloudflare.com/workers-ai",
                "description": "在 Cloudflare 边缘网络上运行 AI 模型",
                "limits": {
                    "neurons_per_day": 10000,
                    "note": "免费额度"
                },
                "models": cloudflare_models
            }
            logger.info(f"成功获取 {len(cloudflare_models)} 个 Cloudflare 模型")
    except Exception as e:
        logger.error(f"获取 Cloudflare 模型失败: {e}")
    
    # 5. GitHub Models - GitHub 模型市场
    # API: https://github.com/marketplace?type=models&page={page}
    try:
        logger.info("正在获取 GitHub 模型...")
        github_models = fetch_github_models(logger)
        if github_models:
            result["providers"]["github"] = {
                "name": "GitHub Models",
                "url": "https://github.com/marketplace/models",
                "description": "GitHub 模型市场，需要 Copilot 订阅",
                "limits": {
                    "note": "根据 Copilot 订阅层级不同而不同（Free/Pro/Pro+/Business/Enterprise）"
                },
                "models": github_models
            }
            logger.info(f"成功获取 {len(github_models)} 个 GitHub 模型")
    except Exception as e:
        logger.error(f"获取 GitHub 模型失败: {e}")
    
    # 6. SambaNova - AI 云平台
    # API: https://api.sambanova.ai/v1/models
    try:
        logger.info("正在获取 SambaNova 模型...")
        samba_models = fetch_samba_models(logger)
        if samba_models:
            result["providers"]["sambanova"] = {
                "name": "SambaNova Cloud",
                "url": "https://cloud.sambanova.ai",
                "description": "企业级 AI 云平台",
                "credits": "$5（3个月）",
                "models": samba_models
            }
            logger.info(f"成功获取 {len(samba_models)} 个 SambaNova 模型")
    except Exception as e:
        logger.error(f"获取 SambaNova 模型失败: {e}")
    
    # 7. Scaleway - 欧洲云服务商
    # API: https://api.scaleway.ai/v1/models
    try:
        logger.info("正在获取 Scaleway 模型...")
        scaleway_models = fetch_scaleway_models(logger)
        if scaleway_models:
            result["providers"]["scaleway"] = {
                "name": "Scaleway Generative APIs",
                "url": "https://console.scaleway.com/generative-api/models",
                "description": "欧洲云服务商的生成式 API",
                "credits": "1,000,000 免费 tokens",
                "models": scaleway_models
            }
            logger.info(f"成功获取 {len(scaleway_models)} 个 Scaleway 模型")
    except Exception as e:
        logger.error(f"获取 Scaleway 模型失败: {e}")
    
    # 8. Cohere - 企业级语言模型平台
    # API: https://api.cohere.com/v1/models
    try:
        logger.info("正在获取 Cohere 模型...")
        cohere_models = fetch_cohere_models(logger)
        if cohere_models:
            result["providers"]["cohere"] = {
                "name": "Cohere",
                "url": "https://cohere.com",
                "description": "企业级语言模型平台",
                "limits": {
                    "requests_per_minute": 20,
                    "requests_per_month": 1000,
                    "note": "共享月度配额"
                },
                "models": cohere_models
            }
            logger.info(f"成功获取 {len(cohere_models)} 个 Cohere 模型")
    except Exception as e:
        logger.error(f"获取 Cohere 模型失败: {e}")
    
    # 9. Google AI Studio - Gemini 模型
    # 使用 Google Cloud Quotas API 获取配额信息
    try:
        logger.info("正在获取 Google AI Studio 配额...")
        gemini_limits = fetch_gemini_limits(logger)
        if gemini_limits:
            result["providers"]["google_ai_studio"] = {
                "name": "Google AI Studio",
                "url": "https://aistudio.google.com",
                "description": "Google 的 Gemini 模型平台",
                "note": "在英国/瑞士/欧洲经济区/欧盟以外使用时，数据会用于训练",
                "limits": gemini_limits
            }
            logger.info("成功获取 Google AI Studio 配额信息")
    except Exception as e:
        logger.error(f"获取 Google AI Studio 配额失败: {e}")
    
    from datetime import datetime
    result["timestamp"] = datetime.utcnow().isoformat() + "Z"
    
    return result


# Vercel app - 必须命名为 app
def app(environ, start_response):
    """
    WSGI application for Vercel
    """
    # 处理 GET 请求
    if environ['REQUEST_METHOD'] == 'GET':
        try:
            model_data = generate_model_list()
            status = '200 OK'
            headers = [
                ('Content-Type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'),
            ]
            start_response(status, headers)
            import json
            return [json.dumps(model_data, ensure_ascii=False).encode('utf-8')]
        except Exception as e:
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            import json
            return [json.dumps({"error": str(e)}).encode('utf-8')]
    else:
        status = '405 Method Not Allowed'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [b'{"error": "Method not allowed"}']
