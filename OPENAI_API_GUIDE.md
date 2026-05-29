# OpenAI 兼容 API 使用指南

## 🎯 已部署的 OpenAI 兼容端点

等待 Vercel 部署完成后（约 1-2 分钟），你可以使用以下端点：

### 基础 URL
```
https://free-llm-api-resources.vercel.app/v1
```

### 可用端点

1. **聊天完成**
   ```
   POST https://free-llm-api-resources.vercel.app/v1/chat/completions
   ```

2. **模型列表**
   ```
   GET https://free-llm-api-resources.vercel.app/v1/models
   ```

## 💻 使用方法

### 方法 1：使用 OpenAI Python SDK

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    base_url="https://free-llm-api-resources.vercel.app/v1",
    api_key="not-needed"  # API Key 在服务器端配置
)

# 调用 DeepSeek V4 Flash
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "user", "content": "你好！请介绍一下你自己"}
    ],
    max_tokens=500,
    temperature=0.7
)

print(response.choices[0].message.content)
```

### 方法 2：使用 requests 库

```python
import requests

response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    json={
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "user", "content": "你好！"}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])
```

### 方法 3：使用 curl

```bash
curl -X POST https://free-llm-api-resources.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-flash",
    "messages": [
      {"role": "user", "content": "你好！"}
    ],
    "max_tokens": 500
  }'
```

## 📦 可用的模型

### 1. DeepSeek V4 Flash
- **模型 ID**: `deepseek-v4-flash`
- **提供商**: OpenRouter
- **特点**: 完全免费，高质量对话
- **限制**: 需要 OpenRouter API Key（已在服务器配置）

### 2. Llama 3.1 8B
- **模型 ID**: `llama-3.1-8b`
- **提供商**: Groq
- **特点**: 超高速推理（每秒数百 tokens）
- **限制**: 14,400 requests/day

## 🔧 配置说明

### 服务器端已配置的 API Keys

以下 API Keys 已在 Vercel 环境变量中配置：

- ✅ `GROQ_API_KEY` - Groq 平台
- ✅ `HYPERBOLIC_API_KEY` - Hyperbolic 平台
- ✅ `CLOUDFLARE_ACCOUNT_ID` - Cloudflare
- ✅ `CLOUDFLARE_API_KEY` - Cloudflare
- ✅ `COHERE_API_KEY` - Cohere
- ✅ `OPENCODE_ZEN_API_KEY` - OpenCode Zen
- ⚠️ `OPENROUTER_API_KEY` - **需要添加**（用于 DeepSeek V4 Flash）

### 添加 OpenRouter API Key

如果要使用 DeepSeek V4 Flash，需要在 Vercel 控制台添加：

1. 访问 https://vercel.com/dashboard
2. 找到项目 `free-llm-api-resources`
3. Settings → Environment Variables
4. 添加：
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```
5. 重新部署

## 📊 获取模型列表

```python
import requests

response = requests.get("https://free-llm-api-resources.vercel.app/v1/models")
models = response.json()

for model in models['data']:
    print(f"- {model['id']}: {model['description']}")
```

## ⚠️ 注意事项

1. **API Key 管理**: 所有的 API Keys 都在服务器端配置，客户端不需要提供
2. **模型路由**: API 会根据 `model` 参数自动路由到正确的提供商
3. **错误处理**: 如果某个提供商失败，会返回错误信息
4. **速率限制**: 各个提供商有自己的速率限制

## 🚀 快速开始

### 测试连接

```python
import requests

# 测试模型列表
response = requests.get("https://free-llm-api-resources.vercel.app/v1/models")
print(response.json())

# 测试聊天
response = requests.post(
    "https://free-llm-api-resources.vercel.app/v1/chat/completions",
    json={
        "model": "llama-3.1-8b",  # 使用 Groq（已配置）
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(response.json()['choices'][0]['message']['content'])
```

## 💡 优势

- ✅ **OpenAI 兼容**: 可以使用标准的 OpenAI SDK
- ✅ **多模型支持**: 自动路由到不同的提供商
- ✅ **无需客户端配置**: API Keys 在服务器端管理
- ✅ **免费使用**: 利用各个平台的免费额度
- ✅ **易于集成**: 与现有 OpenAI 应用无缝对接
