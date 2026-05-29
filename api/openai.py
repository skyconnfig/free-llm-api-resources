#!/usr/bin/env python3
"""
OpenAI 兼容的 API 端点
支持标准的 OpenAI SDK 调用格式
"""

import json
import os
import sys
import requests
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
    支持所有已配置的供应商
    """
    model_lower = model.lower()
    
    # DeepSeek V4 Flash - 使用 OpenCode Zen
    if 'deepseek' in model_lower and ('v4' in model_lower or 'flash' in model_lower):
        return call_opencode_zen_deepseek(messages, max_tokens, temperature, logger)
    
    # Llama 系列 - 使用 Groq
    elif 'llama' in model_lower:
        return call_groq_llama(messages, max_tokens, temperature, logger)
    
    # Cohere 模型
    elif 'command' in model_lower or 'cohere' in model_lower:
        return call_cohere_model(model, messages, max_tokens, temperature, logger)
    
    # Cloudflare Workers AI 模型
    elif 'cf-' in model_lower or '@cf/' in model_lower:
        return call_cloudflare_model(model, messages, max_tokens, temperature, logger)
    
    # Hyperbolic 模型
    elif 'hyperbolic' in model_lower or any(x in model_lower for x in ['mistral', 'mixtral']):
        return call_hyperbolic_model(model, messages, max_tokens, temperature, logger)
    
    # 默认使用 Groq（最稳定的免费服务）
    else:
        logger.info(f"未识别模型 {model}，使用默认 Groq")
        return call_groq_llama(messages, max_tokens, temperature, logger)


def call_opencode_zen_deepseek(messages, max_tokens, temperature, logger):
    """
    调用 OpenCode Zen 的 DeepSeek V4 Flash Free
    """
    OPENCODE_ZEN_API_KEY = os.environ.get('OPENCODE_ZEN_API_KEY', '')
    
    if not OPENCODE_ZEN_API_KEY:
        raise Exception("OpenCode Zen API Key 未配置")
    
    logger.info("调用 OpenCode Zen DeepSeek V4 Flash...")
    
    # 尝试多个可能的 API 端点
    endpoints = [
        "https://api.opencode.ai/v1/chat/completions",
        "https://zen.opencode.ai/v1/chat/completions",
    ]
    
    last_error = None
    for endpoint in endpoints:
        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {OPENCODE_ZEN_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-v4-flash-free",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"OpenCode Zen 调用成功 (端点: {endpoint})")
                return result
            else:
                last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                logger.warning(f"端点 {endpoint} 失败: {last_error}")
                
        except Exception as e:
            last_error = str(e)
            logger.warning(f"端点 {endpoint} 异常: {e}")
            continue
    
    # 如果所有端点都失败，返回模拟响应
    logger.error(f"所有 OpenCode Zen 端点都失败。最后错误: {last_error}")
    
    # 返回一个友好的错误提示
    return {
        "id": "chatcmpl-opencode-zen-error",
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()),
        "model": "deepseek-v4-flash-free",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "⚠️ OpenCode Zen API 当前不可用。\n\n可能原因：\n1. API 端点地址不正确\n2. API Key 无效\n3. 服务暂时不可用\n\n建议：\n- 查看官方文档: https://opencode.ai/docs/zen/\n- 或使用其他模型（如 llama-3.1-8b）"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


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


def call_opencode_zen_deepseek(messages, max_tokens, temperature, logger):
    """
    调用 OpenCode Zen 的 DeepSeek V4 Flash Free
    """
    OPENCODE_ZEN_API_KEY = os.environ.get('OPENCODE_ZEN_API_KEY', '')
    
    if not OPENCODE_ZEN_API_KEY:
        raise Exception("OpenCode Zen API Key 未配置")
    
    logger.info("调用 OpenCode Zen DeepSeek V4 Flash...")
    
    # 尝试多个可能的 API 端点
    endpoints = [
        "https://api.opencode.ai/v1/chat/completions",
        "https://zen.opencode.ai/v1/chat/completions",
    ]
    
    last_error = None
    for endpoint in endpoints:
        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {OPENCODE_ZEN_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-v4-flash-free",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"OpenCode Zen 调用成功 ({endpoint})")
            return result
            
        except Exception as e:
            last_error = e
            logger.warning(f"端点 {endpoint} 失败: {e}")
            continue
    
    # 所有端点都失败
    if last_error:
        raise Exception(f"OpenCode Zen 所有端点都失败: {last_error}")


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


def call_cohere_model(model, messages, max_tokens, temperature, logger):
    """
    调用 Cohere 模型
    """
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY', '')
    
    if not COHERE_API_KEY:
        raise Exception("Cohere API Key 未配置")
    
    # 如果只提供了简写，转换为完整模型 ID
    if model == 'command' or model == 'command-r':
        cohere_model = 'command-r'
    elif model == 'command-r-plus':
        cohere_model = 'command-r-plus'
    else:
        cohere_model = model
    
    logger.info(f"调用 Cohere 模型: {cohere_model}")
    
    response = requests.post(
        "https://api.cohere.ai/v2/chat",
        headers={
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": cohere_model,
            "message": messages[-1]['content'],  # Cohere 使用 message 而不是 messages
            "chat_history": [
                {
                    "role": "USER" if msg['role'] == 'user' else "CHATBOT",
                    "message": msg['content']
                }
                for msg in messages[:-1]
            ] if len(messages) > 1 else [],
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=60
    )
    
    response.raise_for_status()
    result = response.json()
    
    # 转换 Cohere 响应格式为 OpenAI 格式
    openai_format = {
        "id": f"chatcmpl-cohere-{result.get('generation_id', '')}",
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()),
        "model": cohere_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result.get('text', '')
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": result.get('meta', {}).get('tokens', {}).get('input_tokens', 0),
            "completion_tokens": result.get('meta', {}).get('tokens', {}).get('output_tokens', 0),
            "total_tokens": sum(result.get('meta', {}).get('tokens', {}).values())
        }
    }
    
    logger.info(f"Cohere 调用成功")
    return openai_format


def call_cloudflare_model(model, messages, max_tokens, temperature, logger):
    """
    调用 Cloudflare Workers AI 模型
    """
    CLOUDFLARE_ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '')
    CLOUDFLARE_API_KEY = os.environ.get('CLOUDFLARE_API_KEY', '')
    
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_KEY:
        raise Exception("Cloudflare API 凭证未配置")
    
    # 提取模型名称（去除 cf- 或 @cf/ 前缀）
    if model.startswith('cf-'):
        cf_model = model[3:]
    elif model.startswith('@cf/'):
        cf_model = model[4:]
    else:
        cf_model = model
    
    logger.info(f"调用 Cloudflare 模型: {cf_model}")
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/{cf_model}"
    
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=60
    )
    
    response.raise_for_status()
    result = response.json()
    
    # 转换 Cloudflare 响应格式为 OpenAI 格式
    openai_format = {
        "id": f"chatcmpl-cf-{int(datetime.now().timestamp())}",
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()),
        "model": cf_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result.get('result', {}).get('response', '')
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
    
    logger.info(f"Cloudflare 调用成功")
    return openai_format


def call_hyperbolic_model(model, messages, max_tokens, temperature, logger):
    """
    调用 Hyperbolic 模型
    """
    HYPERBOLIC_API_KEY = os.environ.get('HYPERBOLIC_API_KEY', '')
    
    if not HYPERBOLIC_API_KEY:
        raise Exception("Hyperbolic API Key 未配置")
    
    # 提取实际模型名称
    if model.startswith('hyperbolic-'):
        hyper_model = model[len('hyperbolic-'):]
    else:
        hyper_model = model
    
    logger.info(f"调用 Hyperbolic 模型: {hyper_model}")
    
    response = requests.post(
        "https://api.hyperbolic.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": hyper_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=60
    )
    
    response.raise_for_status()
    result = response.json()
    
    logger.info(f"Hyperbolic 调用成功")
    return result


def models_list(environ, start_response):
    """
    返回可用的模型列表
    GET /v1/models
    """
    models = [
        # OpenCode Zen - DeepSeek V4 Flash
        {
            "id": "deepseek-v4-flash",
            "object": "model",
            "created": 1700000000,
            "owned_by": "opencode-zen",
            "description": "DeepSeek V4 Flash Free - 完全免费"
        },
        
        # Groq - Llama 系列
        {
            "id": "llama-3.1-8b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "groq",
            "description": "Llama 3.1 8B - 超高速推理"
        },
        {
            "id": "llama-3.2-11b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "groq",
            "description": "Llama 3.2 11B Vision"
        },
        {
            "id": "llama-3.3-70b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "groq",
            "description": "Llama 3.3 70B"
        },
        
        # Cohere 模型
        {
            "id": "command-r",
            "object": "model",
            "created": 1700000000,
            "owned_by": "cohere",
            "description": "Cohere Command R - 高效对话模型"
        },
        {
            "id": "command-r-plus",
            "object": "model",
            "created": 1700000000,
            "owned_by": "cohere",
            "description": "Cohere Command R+ - 高级对话模型"
        },
        
        # Cloudflare Workers AI 模型
        {
            "id": "cf-llama-3-8b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "cloudflare",
            "description": "Cloudflare Llama 3 8B - 边缘推理"
        },
        {
            "id": "cf-mistral-7b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "cloudflare",
            "description": "Cloudflare Mistral 7B - 边缘推理"
        },
        
        # Hyperbolic 模型
        {
            "id": "hyperbolic-mistral-7b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "hyperbolic",
            "description": "Hyperbolic Mistral 7B - 去中心化推理"
        },
        {
            "id": "hyperbolic-mixtral-8x7b",
            "object": "model",
            "created": 1700000000,
            "owned_by": "hyperbolic",
            "description": "Hyperbolic Mixtral 8x7B - 去中心化推理"
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
