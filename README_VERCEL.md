# 🌐 Free LLM API Resources - Vercel 部署版

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-username%2Ffree-llm-api-resources)

## 📖 简介

本项目提供免费的 LLM API 资源列表，并已优化为可部署到 Vercel 的 Web API 服务。

**主要功能：**
- ✅ 从多个 AI 服务提供商获取免费模型信息
- ✅ 提供 RESTful API 接口
- ✅ 完整的中文文档和注释
- ✅ 支持轻量级和完整版两种模式

## 🚀 快速开始

### 方式一：一键部署到 Vercel

点击上方的 "Deploy with Vercel" 按钮，或运行：

```bash
npm install -g vercel
vercel login
vercel
```

### 方式二：本地使用

```bash
# 安装依赖
pip install -r requirements.txt

# 生成 README
cd src
python pull_available_models.py

# 运行测试
cd ..
python test_setup.py
```

## 📊 API 端点

部署后可访问以下端点：

### 轻量版（推荐）
```
GET https://your-project.vercel.app/api/models/lite
```
- ⚡ 快速响应（< 5秒）
- 🔓 无需 API 密钥
- 📦 3个提供商，74+个模型

### 完整版
```
GET https://your-project.vercel.app/api/models
```
- 📦 9个提供商
- 🔑 需要配置环境变量
- ⏱️ 响应时间 10-60秒

## 📝 文档

- 📘 [快速开始指南](QUICKSTART.md) - 5分钟上手
- 📗 [详细部署指南](DEPLOYMENT.md) - 完整部署说明
- 📙 [优化总结](OPTIMIZATION_SUMMARY.md) - 项目改进详情
- 📕 [项目总结](PROJECT_SUMMARY.md) - 完整工作总结

## 🔧 配置环境变量（可选）

如需使用完整版 API，在 Vercel 控制台添加以下环境变量：

| 变量名 | 用途 |
|--------|------|
| `GROQ_API_KEY` | Groq 平台认证 |
| `HYPERBOLIC_API_KEY` | Hyperbolic 平台认证 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账户 ID |
| `CLOUDFLARE_API_KEY` | Cloudflare API 密钥 |
| `LAMBDA_API_KEY` | Lambda Labs 认证 |
| `SCALEWAY_API_KEY` | Scaleway 认证 |
| `COHERE_API_KEY` | Cohere 平台认证 |
| `GCP_PROJECT_ID` | Google Cloud 项目 ID |

查看 [.env.example](.env.example) 获取详细配置说明。

## 💻 使用示例

### cURL
```bash
curl https://your-project.vercel.app/api/models/lite
```

### JavaScript
```javascript
const response = await fetch('https://your-project.vercel.app/api/models/lite');
const data = await response.json();
console.log(data.summary);
```

### Python
```python
import requests
response = requests.get('https://your-project.vercel.app/api/models/lite')
data = response.json()
print(f"共 {data['summary']['total_models']} 个模型")
```

## 📦 支持的提供商

### 无需认证
- ✅ OpenRouter - 免费模型聚合
- ✅ GitHub Models - 需 Copilot 订阅
- ✅ SambaNova Cloud - 基础模型

### 需要认证
- 🔑 Groq - 高速推理
- 🔑 Hyperbolic - 去中心化 AI
- 🔑 Cloudflare Workers AI - 边缘 AI
- 🔑 Lambda Labs - GPU 云
- 🔑 Scaleway - 欧洲云
- 🔑 Cohere - 语言模型
- 🔑 Google AI Studio - Gemini

## 🧪 测试

```bash
python test_setup.py
```

运行自动化测试验证配置。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

与原项目保持一致

## 🙏 致谢

基于 [free-llm-api-resources](https://github.com/BerriAI/free-llm-api-resources) 项目优化

---

**祝你使用愉快！** 🎉
