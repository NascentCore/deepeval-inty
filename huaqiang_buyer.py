import json
import os
from chat_client import ChatClient
from typing import List, Dict
from config import CHAT_CONFIG

# 从配置文件读取API配置
BASE_URL = CHAT_CONFIG["base_url"]
TOKEN = CHAT_CONFIG["token"]

def get_buyer_prompts() -> List[Dict]:
    """获取买瓜人的对话提示"""
    return [
        {"role": "user", "content": "请你扮演华强买瓜中的买瓜人，我会扮演卖瓜人。开始对话吧。"},
        {"role": "user", "content": "你好，要买瓜吗？"},
        {"role": "user", "content": "两块钱一斤"},
        {"role": "user", "content": "你瞧瞧这现在哪有瓜呀，这都是大棚的瓜，你嫌贵我还嫌贵呢"},
        {"role": "user", "content": "这个怎么样"},
        {"role": "user", "content": "我开水果摊的能卖给你生瓜蛋的？！"},
        {"role": "user", "content": "你是故意找茬是不是，你要不要吧"},
        {"role": "user", "content": "不熟我自己吃了它满意了吧。十五斤三十块"},
        {"role": "user", "content": "你他妈故意找茬是不是你要不要。"},
        {"role": "user", "content": "你他妈骗我瓜是吧"}
    ]

def generate_buyer_conversation(client: ChatClient) -> List[Dict]:
    """生成买瓜人的对话，真实调用chat接口"""
    conversation = []
    prompts = get_buyer_prompts()
    
    for prompt in prompts:
        # 添加提示到对话
        conversation.append({
            "role": "user",
            "content": prompt["content"]
        })
        
        # 调用API获取回复
        response = client.chat(prompt["content"])
        conversation.append({
            "role": "assistant",
            "content": response
        })
    
    return conversation

def save_conversation(conversation: List[Dict], filename: str):
    """将对话保存为JSON文件"""
    filepath = os.path.join("conversations", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=4)
    print(f"对话已保存到: {filepath}")

def main():
    # 初始化ChatClient
    print(f"使用配置: BASE_URL={BASE_URL}")
    client = ChatClient(BASE_URL, TOKEN)
    
    # 生成买瓜人对话
    conversation = generate_buyer_conversation(client)
    
    # 保存对话
    save_conversation(conversation, "华强买瓜_买瓜人.json")

if __name__ == "__main__":
    main() 