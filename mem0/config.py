# -*- coding: utf-8 -*-
"""
Mem0 配置模块
用于初始化 Mem0 客户端并配置本地向量数据库
使用 OpenRouter API 作为 LLM 提供者
"""

import os  # 导入 os 模块，用于操作系统相关功能
from dotenv import load_dotenv  # 导入 load_dotenv 函数，用于加载 .env 文件
from mem0 import Memory  # 导入 Mem0 的 Memory 类

# ========================================
# 第一步：加载环境变量配置
# ========================================

load_dotenv()  # 从 .env 文件加载环境变量到系统环境中

# ========================================
# 第二步：OpenRouter API 配置
# ========================================
# 读取 OpenRouter API 密钥（必需！）
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')

# 读取聊天模型名称（默认 deepseek/deepseek-chat）
# DeepSeek V3 的模型 ID 是 deepseek/deepseek-chat
CHAT_MODEL = os.getenv('CHAT_MODEL', 'deepseek/deepseek-chat')

# OpenRouter API 基础 URL
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'

# ========================================
# 第三步：Mem0 配置（使用本地 Ollama）
# ========================================
# 注意：Mem0 的 LLM 和嵌入模型都使用本地 Ollama
# 聊天功能使用 OpenRouter，但 Mem0 内部处理使用本地模型
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# 设置环境变量，让 localhost 不走代理（避免本地 Ollama 连接失败）
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
os.environ['no_proxy'] = 'localhost,127.0.0.1'

# Mem0 使用的本地 LLM 模型（用于提取记忆，使用轻量级模型即可）
# 推荐使用 gemma2:2b 或 qwen2.5:3b 等小模型
MEM0_LLM_MODEL = os.getenv('MEM0_LLM_MODEL', 'gemma2:2b')

# 读取嵌入模型名称（默认 nomic-embed-text）
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')

# 读取嵌入向量维度（默认 768，对应 nomic-embed-text 的维度）
EMBEDDING_DIMS = int(os.getenv('EMBEDDING_DIMS', '768'))

# 读取本地数据存储路径（默认 ./mem0_data）
DATA_PATH = os.getenv('DATA_PATH', './mem0_data')

# ========================================
# 第四步：配置 Mem0
# ========================================
def get_mem0_config():
    """
    获取 Mem0 配置字典
    
    返回:
        dict: Mem0 的完整配置，包括向量存储、LLM 和嵌入器配置
    """
    config = {
        # 向量存储配置（使用本地 Qdrant）
        "vector_store": {
            "provider": "qdrant",  # 使用 Qdrant 作为向量数据库
            "config": {
                "path": DATA_PATH,  # 本地存储路径
                "collection_name": "chat_memory",  # 集合名称（类似数据库的表名）
                "embedding_model_dims": EMBEDDING_DIMS,  # 嵌入向量维度（关键！必须匹配嵌入模型）
                "on_disk": True,  # 关键！确保数据持久化到磁盘
            }
        },
        # LLM 配置（用于从记忆中提取关键信息）
        # 注意：这里使用本地 Ollama 的轻量级模型，不是 OpenRouter
        "llm": {
            "provider": "ollama",  # 使用 Ollama 作为 LLM 提供者
            "config": {
                "model": MEM0_LLM_MODEL,  # 使用本地轻量级模型（如 gemma2:2b）
                "ollama_base_url": OLLAMA_BASE_URL  # Ollama 服务地址
            }
        },
        # 嵌入器配置（用于生成文本向量）
        "embedder": {
            "provider": "ollama",  # 使用 Ollama 作为嵌入器提供者
            "config": {
                "model": EMBEDDING_MODEL,  # 使用的嵌入模型名称
                "ollama_base_url": OLLAMA_BASE_URL,  # Ollama 服务地址
                "embedding_dims": EMBEDDING_DIMS  # 嵌入向量维度（关键！必须匹配）
            }
        }
    }
    
    return config  # 返回配置字典


def init_mem0():
    """
    初始化 Mem0 客户端
    
    返回:
        Memory: 初始化好的 Mem0 Memory 实例
    """
    config = get_mem0_config()  # 获取配置字典
    memory = Memory.from_config(config)  # 使用配置创建 Memory 实例
    print(f"✅ Mem0 初始化成功！数据存储在: {DATA_PATH}")  # 打印成功信息
    return memory  # 返回 Memory 实例


# ========================================
# 测试代码（可选）
# ========================================
if __name__ == "__main__":
    # 如果直接运行此文件，则执行测试
    print("🔧 测试 Mem0 配置...")
    print(f"🔑 OpenRouter API 密钥: {'已设置' if OPENROUTER_API_KEY else '❌ 未设置'}")
    print(f"🤖 聊天模型: {CHAT_MODEL}")
    print(f"📍 Ollama 地址（嵌入）: {OLLAMA_BASE_URL}")
    print(f"📊 嵌入模型: {EMBEDDING_MODEL}")
    print(f"📏 嵌入维度: {EMBEDDING_DIMS}")
    print(f"💾 数据路径: {DATA_PATH}")
    print("\n尝试初始化 Mem0...")
    
    try:
        mem = init_mem0()  # 尝试初始化
        print("✅ 测试成功！Mem0 已准备就绪。")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
