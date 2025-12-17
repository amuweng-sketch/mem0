# Mem0 + Chainlit 本地记忆聊天机器人

这是一个基于 **Mem0** 和 **Chainlit** 的本地记忆聊天机器人，使用本地 Ollama 大模型和本地向量数据库。

## ✨ 功能特性

- 🤖 **本地 LLM**: 使用 Ollama 运行 `gemma3:27b` 模型
- 🧠 **本地记忆**: 使用 Mem0 + Qdrant 在本地存储对话记忆
- 🎨 **Web 界面**: 使用 Chainlit 提供类似 ChatGPT 的聊天界面
- 💾 **数据本地化**: 所有数据存储在 `mem0_data` 文件夹中
- 🔒 **代理绕过**: 已配置 localhost 不走代理，避免连接错误

## 📋 环境要求

- **Python**: 3.8 或更高版本
- **Ollama**: 已安装并运行（默认地址 `http://localhost:11434`）
- **模型**: 已安装以下 Ollama 模型
  - `gemma3:27b`（聊天模型）
  - `nomic-embed-text`（嵌入模型，768 维）

## 🚀 安装步骤

### 1️⃣ 创建虚拟环境

在项目目录下打开终端（PowerShell 或 CMD），运行以下命令：

```powershell
# 创建虚拟环境
python -m venv venv
```

### 2️⃣ 激活虚拟环境

**Windows (PowerShell)**:
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux**:
```bash
source venv/bin/activate
```

激活成功后，命令提示符前会显示 `(venv)`。

### 3️⃣ 安装依赖

确保虚拟环境已激活，然后运行：

```powershell
pip install -r requirements.txt
```

### 4️⃣ 检查 Ollama 模型

运行以下命令检查模型是否已安装：

```powershell
ollama list
```

如果没有看到 `gemma3:27b` 或 `nomic-embed-text`，请安装：

```powershell
# 安装聊天模型（如果尚未安装）
ollama pull gemma3:27b

# 安装嵌入模型（必须安装，用于生成向量）
ollama pull nomic-embed-text
```

## ▶️ 运行应用

确保虚拟环境已激活，然后运行：

```powershell
chainlit run app.py -w
```

- `-w` 参数表示监听文件变化（修改代码后自动重载）
- 浏览器会自动打开 `http://localhost:8000`
- 开始聊天吧！

## 💡 使用示例

### 测试记忆功能

1️⃣ **告诉 AI 一些信息**:
```
用户: 你好，我叫李明，我是一名软件工程师
AI: 你好李明！很高兴认识你...
```

2️⃣ **稍后询问**:
```
用户: 我叫什么名字？我的职业是什么？
AI: 你叫李明，是一名软件工程师。
```

3️⃣ **重启应用后再问**:
```
# 关闭应用（Ctrl+C），重新运行 chainlit run app.py -w
用户: 你还记得我吗？
AI: 当然记得！你是李明，一名软件工程师。
```

## 📂 数据存储

所有记忆数据存储在项目目录下的 `mem0_data` 文件夹中：

```
mem0/
├── mem0_data/          # Qdrant 本地数据库
│   ├── collection/     # 向量数据
│   ├── meta.json       # 元数据
│   └── ...
```

**删除记忆**: 如果想清空所有记忆，直接删除 `mem0_data` 文件夹即可。

## ⚙️ 配置说明

可以在 `.env` 文件中修改配置：

```env
# Ollama 服务地址
OLLAMA_BASE_URL=http://localhost:11434

# 聊天模型
CHAT_MODEL=gemma3:27b

# 嵌入模型
EMBEDDING_MODEL=nomic-embed-text

# 嵌入向量维度（nomic-embed-text 是 768 维）
EMBEDDING_DIMS=768

# 数据存储路径
DATA_PATH=./mem0_data
```

## 🔧 常见问题

### ❓ 问题 1: 启动时提示 "维度不匹配" 错误

**原因**: 嵌入模型的维度与配置不一致。

**解决方法**:
1. 检查 `.env` 文件中的 `EMBEDDING_DIMS` 是否为 `768`
2. 确认已安装 `nomic-embed-text` 模型：`ollama pull nomic-embed-text`
3. 删除 `mem0_data` 文件夹，重新启动应用

### ❓ 问题 2: 连接 Ollama 失败

**原因**: Ollama 未运行或被代理拦截。

**解决方法**:
1. 确认 Ollama 正在运行
2. 测试连接：`curl http://localhost:11434/api/tags`
3. 代码已配置代理绕过，如仍有问题，检查代理软件设置

### ❓ 问题 3: 虚拟环境激活失败（PowerShell）

**原因**: PowerShell 执行策略限制。

**解决方法**:
```powershell
# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 然后再激活虚拟环境
.\venv\Scripts\Activate.ps1
```

## 📚 项目结构

```
mem0/
├── venv/               # Python 虚拟环境
├── mem0_data/          # 本地数据存储（自动创建）
├── .env                # 环境变量配置
├── requirements.txt    # Python 依赖
├── config.py           # Mem0 配置模块
├── app.py              # Chainlit 主应用
├── README.md           # 本文档
└── .chainlit/          # Chainlit 配置（自动创建）
```

## 🎯 下一步优化

- [ ] 支持多用户会话管理
- [ ] 添加记忆总结功能
- [ ] 自定义 Chainlit UI 样式
- [ ] 支持切换不同的 Ollama 模型

## 📝 技术栈

- **Chainlit**: Web 聊天界面框架
- **Mem0**: 记忆管理和向量存储
- **Qdrant**: 本地向量数据库
- **Ollama**: 本地大语言模型服务
- **Python**: 3.8+

---

**🎉 享受你的本地记忆聊天机器人吧！**
