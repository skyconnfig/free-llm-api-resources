# 部署到 Vercel 指南

本项目可以部署为 Vercel Serverless Function，提供免费的 LLM API 资源查询服务。

## 快速部署

### 方法一：通过 Vercel CLI

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **部署项目**
   ```bash
   cd D:\python\free-llm-api-resources
   vercel
   ```

4. **配置环境变量**（可选）
   
   在 Vercel 控制台或命令行中添加以下环境变量以启用更多提供商：
   
   ```bash
   vercel env add GROQ_API_KEY
   vercel env add HYPERBOLIC_API_KEY
   vercel env add CLOUDFLARE_ACCOUNT_ID
   vercel env add CLOUDFLARE_API_KEY
   vercel env add LAMBDA_API_KEY
   vercel env add SCALEWAY_API_KEY
   vercel env add COHERE_API_KEY
   vercel env add GCP_PROJECT_ID
   ```

### 方法二：通过 GitHub 集成

1. **将代码推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **在 Vercel 控制台导入项目**
   - 访问 https://vercel.com
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 点击 "Deploy"

3. **配置环境变量**
   - 在项目设置中添加上述环境变量

## API 使用

部署后，你可以通过以下端点访问数据：

```
GET https://your-project.vercel.app/
```

返回格式：
```json
{
  "providers": {
    "openrouter": {
      "name": "OpenRouter",
      "url": "https://openrouter.ai",
      "description": "免费模型聚合平台",
      "limits": {...},
      "models": [...]
    },
    ...
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 支持的提供商

### 无需 API 密钥
- ✅ OpenRouter - 免费模型聚合
- ✅ GitHub Models - 需要 Copilot 订阅
- ✅ SambaNova Cloud - 基础模型列表

### 需要 API 密钥
- 🔑 Groq - 高速推理平台
- 🔑 Hyperbolic - 去中心化 AI 计算
- 🔑 Cloudflare Workers AI - 边缘 AI
- 🔑 Lambda Labs - GPU 云平台
- 🔑 Scaleway - 欧洲云服务商
- 🔑 Cohere - 企业级语言模型
- 🔑 Google AI Studio - 需要 GCP 认证

## 本地开发

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **创建 .env 文件**（可选）
   ```env
   GROQ_API_KEY=your_key_here
   HYPERBOLIC_API_KEY=your_key_here
   # ... 其他密钥
   ```

3. **运行脚本**
   ```bash
   cd src
   python pull_available_models.py
   ```

## 项目结构

```
free-llm-api-resources/
├── api/
│   └── index.py          # Vercel API 端点（带中文注释）
├── src/
│   ├── pull_available_models.py  # 主脚本（带中文注释）
│   ├── data.py           # 数据配置文件
│   ├── README_template.md
│   └── requirements.txt
├── vercel.json           # Vercel 配置
├── requirements.txt      # Python 依赖
└── README.md            # 生成的文档
```

## 注意事项

1. **冷启动时间**：Serverless Function 首次访问可能需要几秒冷启动
2. **执行时间限制**：Vercel Hobby 计划限制为 10 秒，Pro 计划为 60 秒
3. **响应大小限制**：Hobby 计划限制为 4.5MB
4. **环境变量**：敏感信息应存储在 Vercel 环境变量中，不要提交到 Git

## 优化建议

如果响应时间过长，可以：

1. **减少并发请求**：修改 `FETCH_CONCURRENTLY` 环境变量
2. **缓存结果**：添加 Redis 或其他缓存层
3. **按需加载**：只获取需要的提供商数据
4. **增加超时时间**：升级到 Pro 计划获得更长的执行时间

## 故障排除

### 问题：某些提供商返回空列表

**原因**：缺少对应的 API 密钥

**解决**：在 Vercel 控制台添加相应的环境变量

### 问题：部署失败

**原因**：依赖安装问题

**解决**：检查 `requirements.txt` 和 Python 版本兼容性

### 问题：响应超时

**原因**：获取所有提供商数据耗时过长

**解决**：
- 升级 Vercel 计划
- 减少获取的提供商数量
- 实现异步处理和缓存

## 许可证

与原项目保持一致
