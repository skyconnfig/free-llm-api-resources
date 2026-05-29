# 快速开始指南

## 🚀 5分钟部署到 Vercel

### 步骤 1: 准备项目

```bash
# 进入项目目录
cd D:\python\free-llm-api-resources

# 确保已安装 Vercel CLI
npm install -g vercel
```

### 步骤 2: 部署

```bash
# 登录 Vercel
vercel login

# 一键部署
vercel
```

按照提示操作：
- Set up and deploy? **Y**
- Which scope? **选择你的账户**
- Link to existing project? **N**
- What's your project's name? **free-llm-api**（或自定义）
- In which directory is your code located? **./**
- Want to override the settings? **N**

### 步骤 3: 测试 API

部署完成后，你会得到一个 URL，例如：`https://free-llm-api.vercel.app`

访问以下端点测试：

```bash
# 轻量级版本（快速响应，无需认证）
curl https://your-project.vercel.app/api/models/lite

# 完整版本（需要配置环境变量）
curl https://your-project.vercel.app/api/models
```

### 步骤 4: 添加环境变量（可选）

如果需要获取需要认证的提供商数据：

```bash
# 在 Vercel 控制台添加，或使用命令行
vercel env add GROQ_API_KEY
vercel env add HYPERBOLIC_API_KEY
# ... 添加其他密钥
```

## 📊 API 端点说明

### 1. 轻量级端点 `/api/models/lite`

**特点：**
- ⚡ 快速响应（< 5秒）
- 🔓 无需 API 密钥
- ✅ 适合 Vercel Hobby 计划

**包含的提供商：**
- OpenRouter（免费模型聚合）
- GitHub Models（需 Copilot）
- SambaNova Cloud

**示例响应：**
```json
{
  "providers": {
    "openrouter": {
      "name": "OpenRouter",
      "url": "https://openrouter.ai",
      "models": [...],
      "model_count": 50
    }
  },
  "summary": {
    "total_providers": 3,
    "total_models": 120
  }
}
```

### 2. 完整版端点 `/api/models`

**特点：**
- 📦 包含所有提供商
- 🔑 需要配置 API 密钥
- ⏱️ 响应时间较长（10-60秒）

**包含的提供商：**
- 所有轻量版提供商 +
- Groq
- Hyperbolic
- Cloudflare Workers AI
- Lambda Labs
- Scaleway
- Cohere
- Google AI Studio

## 💻 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行脚本生成 README

```bash
cd src
python pull_available_models.py
```

### 测试 API 端点

```bash
# 使用 Python 测试
python -c "
import sys
sys.path.append('api')
from lite import generate_lightweight_model_list
import json
data = generate_lightweight_model_list()
print(json.dumps(data, indent=2, ensure_ascii=False))
"
```

## 🔧 常见问题

### Q: 为什么某些提供商返回空列表？

A: 缺少对应的 API 密钥。检查是否已在 Vercel 中配置环境变量。

### Q: 部署后响应超时怎么办？

A: 
1. 使用轻量级端点 `/api/models/lite`
2. 升级到 Vercel Pro 计划（60秒限制）
3. 减少获取的提供商数量

### Q: 如何只获取特定提供商的数据？

A: 修改 `api/index.py` 或 `api/lite.py`，注释掉不需要的提供商获取代码。

### Q: 可以缓存结果吗？

A: 可以！Vercel 支持 Edge Config 或 Upstash Redis：

```python
# 示例：使用简单的内存缓存
import time

cache = {}
CACHE_TTL = 3600  # 1小时

def get_cached_data():
    if 'data' in cache and time.time() - cache['timestamp'] < CACHE_TTL:
        return cache['data']
    
    # 获取新数据
    data = generate_model_list()
    cache['data'] = data
    cache['timestamp'] = time.time()
    return data
```

## 📝 下一步

1. **自定义域名**：在 Vercel 控制台绑定自己的域名
2. **添加监控**：集成 UptimeRobot 等服务监控 API 可用性
3. **前端界面**：创建一个简单的前端页面展示数据
4. **定时更新**：使用 GitHub Actions 定时运行脚本更新数据

## 🆘 获取帮助

- 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细部署说明
- 查看 Vercel 文档：https://vercel.com/docs
- 提交 Issue 到 GitHub 仓库

---

**祝你使用愉快！** 🎉
