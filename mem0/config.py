# -*- coding: utf-8 -*-
"""
Mem0 配置模块
用于初始化 Mem0 客户端并配置本地向量数据库
"""

import os  # 导入 os 模块，用于操作系统相关功能
from dotenv import load_dotenv  # 导入 load_dotenv 函数，用于加载 .env 文件
from mem0 import Memory  # 导入 Mem0 的 Memory 类

# ========================================
# 第一步：处理代理绕过（非常重要！）
# ========================================
# 设置环境变量，让 localhost 和 127.0.0.1 不走代理
# 这可以避免全局代理软件拦截本地 Ollama 连接导致报错
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'  # 设置不走代理的地址列表
os.environ['no_proxy'] = 'localhost,127.0.0.1'  # 兼容小写版本（某些系统使用小写）

# ========================================
# 第二步：加载环境变量配置
# ========================================
load_dotenv()  # 从 .env 文件加载环境变量到系统环境中

# 读取 Ollama 服务地址（默认 http://localhost:11434）
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# 读取聊天模型名称（默认 gemma3:27b）
CHAT_MODEL = os.getenv('CHAT_MODEL', 'gemma3:27b')

# 读取嵌入模型名称（默认 nomic-embed-text）
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')

# 读取嵌入向量维度（默认 768，对应 nomic-embed-text 的维度）
EMBEDDING_DIMS = int(os.getenv('EMBEDDING_DIMS', '768'))

# 读取本地数据存储路径（默认 ./mem0_data）
DATA_PATH = os.getenv('DATA_PATH', './mem0_data')

# ========================================
# 第三步：配置 Mem0
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
        "llm": {
            "provider": "ollama",  # 使用 Ollama 作为 LLM 提供者
            "config": {
                "model": CHAT_MODEL,  # 使用的模型名称
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
    print(f"📍 Ollama 地址: {OLLAMA_BASE_URL}")
    print(f"🤖 聊天模型: {CHAT_MODEL}")
    print(f"📊 嵌入模型: {EMBEDDING_MODEL}")
    print(f"📏 嵌入维度: {EMBEDDING_DIMS}")
    print(f"💾 数据路径: {DATA_PATH}")
    print("\n尝试初始化 Mem0...")
    
    try:
        mem = init_mem0()  # 尝试初始化
        print("✅ 测试成功！Mem0 已准备就绪。")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
