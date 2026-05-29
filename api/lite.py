#!/usr/bin/env python3
"""
Vercel API 端点 - 轻量级版本
只获取不需要 API 密钥的提供商，适合快速响应
"""

import json
import os
import sys
from datetime import datetime

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pull_available_models import (
    fetch_openrouter_models,
    fetch_github_models,
    fetch_samba_models,
    create_logger,
)


def generate_lightweight_model_list():
    """
    生成轻量级模型列表（仅包含无需认证的提供商）
    适合 Vercel Hobby 计划的执行时间限制
    """
    logger = create_logger("API-Lite")
    
    result = {
        "providers": {},
        "timestamp": None,
        "version": "lightweight"
    }
    
    # 1. OpenRouter - 免费模型聚合平台（无需认证）
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
                "models": openrouter_models,
                "model_count": len(openrouter_models)
            }
            logger.info(f"✓ 成功获取 {len(openrouter_models)} 个 OpenRouter 模型")
    except Exception as e:
        logger.error(f"✗ 获取 OpenRouter 模型失败: {e}")
    
    # 2. GitHub Models - GitHub 模型市场（无需认证）
    try:
        logger.info("正在获取 GitHub 模型...")
        github_models = fetch_github_models(logger)
        if github_models:
            result["providers"]["github"] = {
                "name": "GitHub Models",
                "url": "https://github.com/marketplace/models",
                "description": "GitHub 模型市场，需要 Copilot 订阅",
                "limits": {
                    "note": "根据 Copilot 订阅层级不同而不同"
                },
                "models": github_models,
                "model_count": len(github_models)
            }
            logger.info(f"✓ 成功获取 {len(github_models)} 个 GitHub 模型")
    except Exception as e:
        logger.error(f"✗ 获取 GitHub 模型失败: {e}")
    
    # 3. SambaNova Cloud - AI 云平台（无需认证）
    try:
        logger.info("正在获取 SambaNova 模型...")
        samba_models = fetch_samba_models(logger)
        if samba_models:
            result["providers"]["sambanova"] = {
                "name": "SambaNova Cloud",
                "url": "https://cloud.sambanova.ai",
                "description": "企业级 AI 云平台",
                "credits": "$5（3个月试用期）",
                "models": samba_models,
                "model_count": len(samba_models)
            }
            logger.info(f"✓ 成功获取 {len(samba_models)} 个 SambaNova 模型")
    except Exception as e:
        logger.error(f"✗ 获取 SambaNova 模型失败: {e}")
    
    # 添加统计信息
    total_providers = len(result["providers"])
    total_models = sum(p.get("model_count", 0) for p in result["providers"].values())
    
    result["summary"] = {
        "total_providers": total_providers,
        "total_models": total_models,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }
    
    result["timestamp"] = result["summary"]["fetched_at"]
    
    logger.info(f"✓ 完成！共获取 {total_providers} 个提供商，{total_models} 个模型")
    
    return result


def handler(req, res):
    """
    Vercel Serverless Function 处理器
    """
    # 设置 CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    
    if req.method == 'OPTIONS':
        res.status_code = 200
        return {}
    
    if req.method == 'GET':
        try:
            model_data = generate_lightweight_model_list()
            res.status_code = 200
            res.setHeader('Content-Type', 'application/json; charset=utf-8')
            return model_data
        except Exception as e:
            res.status_code = 500
            return {
                "error": str(e),
                "message": "服务器内部错误"
            }
    else:
        res.status_code = 405
        return {"error": "Method not allowed"}
