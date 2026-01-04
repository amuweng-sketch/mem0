# OpenRouter DeepSeek V3 使用说明

## 🎯 修改概述

已将聊天机器人的大模型调用从 **本地 Ollama** 改为 **OpenRouter API 的 DeepSeek V3 模型**。

### 修改的文件

1. **config.py** - 更新配置，添加 OpenRouter API 设置
2. **app.py** - 重写 API 调用函数，适配 OpenRouter 格式
3. **.env.example** - 新建环境变量模板文件

---

## 🔑 配置步骤

### 1️⃣ 获取 OpenRouter API 密钥

1. 访问 [OpenRouter 官网](https://openrouter.ai/)
2. 注册/登录账号
3. 前往 [API Keys 页面](https://openrouter.ai/keys) 生成你的 API 密钥
4. 复制你的 API 密钥（保存好，只显示一次）

### 2️⃣ 创建 `.env` 文件

在项目根目录下（`d:\antigravity\mem0`）创建 `.env` 文件：

```bash
# 复制模板文件
cp .env.example .env
```

或者手动创建一个名为 `.env` 的文件。

### 3️⃣ 配置 API 密钥

在 `.env` 文件中填写你的 API 密钥：

```env
# 必填：你的 OpenRouter API 密钥
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxx

# 可选：聊天模型（默认 deepseek/deepseek-chat）
CHAT_MODEL=deepseek/deepseek-chat

# 以下为本地 Ollama 嵌入模型配置（保持默认即可）
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIMS=768
DATA_PATH=./mem0_data
```

> ⚠️ **注意**：
> - `.env` 文件中的 `OPENROUTER_API_KEY` 是**必需**的！
> - Mem0 的嵌入模型仍使用本地 Ollama，需要确保 Ollama 服务正在运行

### 4️⃣ 确保本地 Ollama 服务运行

因为 Mem0 的向量嵌入功能仍然使用本地 Ollama，你需要：

1. 启动 Ollama 服务
2. 确保嵌入模型已安装：

```bash
ollama pull nomic-embed-text
```

---

## 🚀 运行程序

配置好 `.env` 文件后，运行：

```bash
# 激活虚拟环境（如果还没激活）
.\venv\Scripts\activate

# 启动应用
chainlit run app.py -w
```

---

## 🔄 主要代码修改

### 修改 1：config.py - 添加 OpenRouter 配置

```python
# OpenRouter API 配置
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
CHAT_MODEL = os.getenv('CHAT_MODEL', 'deepseek/deepseek-chat')
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
```

### 修改 2：app.py - 更新导入

```python
from config import init_mem0, OPENROUTER_API_KEY, OPENROUTER_BASE_URL, CHAT_MODEL
```

### 修改 3：app.py - 重写 API 调用函数

将原有的 `call_ollama_stream()` 函数重写为 `call_openrouter_stream()`

**关键变化**：

1. **API 端点**：`/api/chat` → `/chat/completions`
2. **认证方式**：添加 `Authorization: Bearer {API_KEY}` 请求头
3. **响应格式**：Ollama 格式 → OpenAI 兼容格式（SSE）
   - Ollama: `{"message": {"content": "..."}}`
   - OpenRouter: `{"choices": [{"delta": {"content": "..."}}]}`

---

## 📊 技术架构

修改后的架构：

```
用户输入
  ↓
Chainlit UI
  ↓
Mem0 记忆检索 (本地 Qdrant + Ollama 嵌入)
  ↓
OpenRouter API (DeepSeek V3)  ← 新！
  ↓
流式输出给用户
  ↓
Mem0 保存新记忆 (本地 Qdrant + Ollama 嵌入)
```

---

## 🔥 DeepSeek V3 模型介绍

DeepSeek V3 是一个高性能的开源大模型：

- 💪 **671B 参数**：但使用 MoE 架构，每次只激活 37B
- 🚀 **极快速度**：推理效率非常高
- 🧠 **强大能力**：接近 Claude 3.5 Sonnet 和 GPT-4 水平
- 💰 **成本低**：通过 OpenRouter 调用比直接调用 OpenAI 便宜很多

---

## ❓ 常见问题

### Q1: 为什么还需要本地 Ollama？

**A:** Mem0 需要使用嵌入模型将文本转换为向量存储。目前配置仍使用本地 Ollama 的嵌入模型，这样更快且免费。

如果你想完全不依赖本地模型，可以修改 `config.py` 使用 OpenAI 的嵌入 API。

### Q2: 支持哪些其他模型？

**A:** OpenRouter 支持非常多的模型，你可以在 `.env` 中修改 `CHAT_MODEL`：

```env
# 示例：使用 Claude 3.5 Sonnet
CHAT_MODEL=anthropic/claude-3.5-sonnet

# 示例：使用 GPT-4
CHAT_MODEL=openai/gpt-4-turbo
```

查看所有可用模型：[OpenRouter Models](https://openrouter.ai/models)

### Q3: 价格怎么样？

**A:** DeepSeek V3 非常便宜：
- 输入：$0.27 / 1M tokens
- 输出：$1.10 / 1M tokens

查看实时价格：[OpenRouter Pricing](https://openrouter.ai/models/deepseek/deepseek-chat)

---

## ✅ 测试验证

启动应用后：

1. 检查欢迎消息是否显示 **"OpenRouter (DeepSeek V3)"**
2. 发送一条测试消息，确认流式输出正常
3. 检查控制台输出，确认没有错误信息

---

## 📝 总结

✅ 已将大模型调用改为 OpenRouter DeepSeek V3  
✅ 保持了流式输出功能  
✅ Mem0 记忆系统继续使用本地向量存储  
✅ 添加了环境变量配置模板  

现在你可以使用强大的 DeepSeek V3 模型，同时仍然保持本地记忆系统的私密性和高效性！🎉
