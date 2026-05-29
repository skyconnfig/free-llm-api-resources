#!/usr/bin/env python3
"""
OpenAI 兼容的 API 端点
支持标准的 OpenAI SDK 调用格式
"""

import json
import os
import sys
from datetime import datetime

# 添加 src 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pull_available_models import create_logger


def chat_completions(environ, start_response):
    """
    OpenAI 兼容的聊天完成端点
    POST /v1/chat/completions
    """
    logger = create_logger("OpenAI-API")
    
    # 只处理 POST 请求
    if environ['REQUEST_METHOD'] != 'POST':
        status = '405 Method Not Allowed'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": "Method not allowed"}).encode('utf-8')]
    
    try:
        # 读取请求体
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(content_length)
        data = json.loads(request_body.decode('utf-8'))
        
        # 提取参数
        model = data.get('model', '')
        messages = data.get('messages', [])
        max_tokens = data.get('max_tokens', 500)
        temperature = data.get('temperature', 0.7)
        stream = data.get('stream', False)
        
        logger.info(f"收到请求 - 模型: {model}, 消息数: {len(messages)}")
        
        # 根据模型 ID 路由到不同的提供商
        response_data = route_to_provider(model, messages, max_tokens, temperature, logger)
        
        # 返回响应
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
        ]
        start_response(status, headers)
        
        return [json.dumps(response_data, ensure_ascii=False).encode('utf-8')]
        
    except Exception as e:
        logger.error(f"处理请求失败: {e}")
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": str(e)}).encode('utf-8')]


def route_to_provider(model, messages, max_tokens, temperature, logger):
    """
    根据模型 ID 路由到不同的提供商
    """
    import requests
    
    # DeepSeek V4 Flash - 使用 OpenRouter
    if 'deepseek' in model.lower() and 'v4' in model.lower():
        return call_openrouter_deepseek(messages, max_tokens, temperature, logger)
    
    # Llama 3.1 - 使用 Groq
    elif 'llama' in model.lower():
        return call_groq_llama(messages, max_tokens, temperature, logger)
    
    # 默认使用 Groq
    else:
        return call_groq_llama(messages, max_tokens, temperature, logger)


def call_openrouter_deepseek(messages, max_tokens, temperature, logger):
    """
    调用 OpenRouter 的 DeepSeek V4 Flash
    """
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
    
    if not OPENROUTER_API_KEY:
        raise Exception("OpenRouter API Key 未配置")
    
    logger.info("调用 OpenRouter DeepSeek V4 Flash...")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://free-llm-api-resources.vercel.app",
        },
        json={
            "model": "deepseek/deepseek-v4-flash:free",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=60
    )
    
    response.raise_for_status()
    result = response.json()
    
    logger.info(f"OpenRouter 调用成功")
    return result


def call_groq_llama(messages, max_tokens, temperature, logger):
    """
    调用 Groq 的 Llama 3.1
    """
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    
    if not GROQ_API_KEY:
        raise Exception("Groq API Key 未配置")
    
    logger.info("调用 Groq Llama 3.1...")
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=30
    )
    
    response.raise_for_status()
    result = response.json()
    
    logger.info(f"Groq 调用成功")
    return result


def models_list(environ, start_response):
    """
    返回可用的模型列表
    GET /v1/models
    """
    models = [
        {
            "id": "deepseek-v4-flash",
            "object": "model",
            "created": 1700000000,
            "owned_by": "opencode-zen",
            "description": "DeepSeek V4 Flash Free - 完全免费"
        },
        {
            "id": "llama-3.1-8b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "groq",
            "description": "Llama 3.1 8B - 超高速推理"
        }
    ]
    
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)
    
    return [json.dumps({"data": models, "object": "list"}).encode('utf-8')]


def app(environ, start_response):
    """
    WSGI 应用入口
    """
    path = environ.get('PATH_INFO', '')
    
    # 路由处理
    if path == '/v1/chat/completions' and environ['REQUEST_METHOD'] == 'POST':
        return chat_completions(environ, start_response)
    elif path == '/v1/models' and environ['REQUEST_METHOD'] == 'GET':
        return models_list(environ, start_response)
    else:
        status = '404 Not Found'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": "Not found"}).encode('utf-8')]
