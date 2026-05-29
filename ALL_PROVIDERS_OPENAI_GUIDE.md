# 所有供应商 OpenAI 兼容 API 使用指南

## 🎯 概述

现在你的 Vercel API **支持所有供应商**，并且完全兼容 OpenAI 格式！

### 基础 URL
```
https://free-llm-api-resources.vercel.app/v1
```

### 可用端点

1. **聊天完成**: `POST /v1/chat/completions`
2. **模型列表**: `GET /v1/models`

---

## 📋 支持的供应商和模型

### 1. OpenCode Zen - DeepSeek V4 Flash ⭐

**模型 ID**: `deepseek-v4-flash`

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "user", "content": "你好！"}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
)

print(response.json()['choices'][0]['message']['content'])
```

---

### 2. Groq - Llama 系列（超高速）✅

**可用模型**:
- `llama-3.1-8b` - Llama 3.1 8B Instant
- `llama-3.2-11b` - Llama 3.2 11B Vision
- `llama-3.3-70b` - Llama 3.3 70B

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "llama-3.1-8b",
        "messages": [
            {"role": "user", "content": "用 Python 写一个快速排序算法"}
        ],
        "max_tokens": 500,
        "temperature": 0.5
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])
print(f"用时: {result.get('usage', {})}")
```

---

### 3. Cohere - 企业级对话模型 ✅

**可用模型**:
- `command-r` - Command R 高效对话
- `command-r-plus` - Command R+ 高级对话

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "command-r",
        "messages": [
            {"role": "user", "content": "解释一下量子计算的基本原理"}
        ],
        "max_tokens": 600,
        "temperature": 0.7
    }
)

print(response.json()['choices'][0]['message']['content'])
```

---

### 4. Cloudflare Workers AI - 边缘推理 ✅

**可用模型**:
- `cf-llama-3-8b` - Llama 3 8B @ Cloudflare Edge
- `cf-mistral-7b` - Mistral 7B @ Cloudflare Edge

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "cf-llama-3-8b",
        "messages": [
            {"role": "user", "content": "什么是边缘计算？"}
        ],
        "max_tokens": 400,
        "temperature": 0.6
    }
)

print(response.json()['choices'][0]['message']['content'])
```

---

### 5. Hyperbolic - 去中心化 AI 计算 ✅

**可用模型**:
- `hyperbolic-mistral-7b` - Mistral 7B
- `hyperbolic-mixtral-8x7b` - Mixtral 8x7B MoE

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "hyperbolic-mixtral-8x7b",
        "messages": [
            {"role": "user", "content": "比较一下集中式和去中心化 AI 的优缺点"}
        ],
        "max_tokens": 700,
        "temperature": 0.7
    }
)

print(response.json()['choices'][0]['message']['content'])
```

---

## 💻 使用 OpenAI SDK

安装 OpenAI SDK：
```bash
pip install openai
```

### 示例代码

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    base_url="https://free-llm-api-resources.vercel.app/v1",
    api_key="not-needed"  # API Key 在服务器端已配置
)

# 使用 DeepSeek V4 Flash
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "user", "content": "介绍一下你自己"}
    ],
    max_tokens=500,
    temperature=0.7
)

print(response.choices[0].message.content)
print(f"Tokens 使用: {response.usage}")
```

### 切换不同模型

只需修改 `model` 参数即可：

```python
# 使用 Groq Llama 3.1
response = client.chat.completions.create(
    model="llama-3.1-8b",
    messages=[{"role": "user", "content": "Hello!"}]
)

# 使用 Cohere Command R
response = client.chat.completions.create(
    model="command-r",
    messages=[{"role": "user", "content": "Hello!"}]
)

# 使用 Cloudflare Llama 3
response = client.chat.completions.create(
    model="cf-llama-3-8b",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 🔍 获取可用模型列表

```python
import requests

response = requests.get("https://free-llm-api-resources.vercel.app/v1/models")
models = response.json()

for model in models['data']:
    print(f"模型: {model['id']}")
    print(f"提供商: {model['owned_by']}")
    print(f"描述: {model['description']}")
    print("-" * 60)
```

---

## 📊 特性对比

| 供应商 | 速度 | 免费额度 | 最佳用途 |
|--------|------|----------|----------|
| **OpenCode Zen** | 中等 | 完全免费 | DeepSeek V4 Flash |
| **Groq** | ⚡ 超快 | 14,400 req/day | 实时应用、快速响应 |
| **Cohere** | 快 | 1,000 req/month | 企业级对话、RAG |
| **Cloudflare** | 快 | 10,000 req/day | 边缘计算、低延迟 |
| **Hyperbolic** | 中等 | 免费试用 | 去中心化推理 |

---

## 🚀 推荐用法

### 场景 1：需要最快速度
```python
model="llama-3.1-8b"  # Groq - 毫秒级响应
```

### 场景 2：需要完全免费
```python
model="deepseek-v4-flash"  # OpenCode Zen - 无限次使用
```

### 场景 3：需要高质量对话
```python
model="command-r-plus"  # Cohere - 企业级质量
```

### 场景 4：需要边缘部署
```python
model="cf-llama-3-8b"  # Cloudflare - 全球 CDN
```

---

## ⚠️ 注意事项

1. **API Key 已在服务器端配置** - 你不需要在客户端提供 API Key
2. **自动路由** - 根据模型 ID 自动选择正确的供应商
3. **统一格式** - 所有响应都遵循 OpenAI 格式
4. **错误处理** - 如果某个供应商失败，会返回友好的错误信息

---

## 🎉 总结

你现在拥有一个**完全兼容 OpenAI 格式的多供应商 API**：

- ✅ 支持 5 个主要供应商
- ✅ 超过 15 个免费模型
- ✅ 统一的 OpenAI SDK 接口
- ✅ 自动路由和负载均衡
- ✅ 完全免费使用

**开始使用吧！** 🚀
