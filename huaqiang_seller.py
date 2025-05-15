import json
import os
from chat_client import ChatClient
from typing import List, Dict
from config import CHAT_CONFIG

# 从配置文件读取API配置
BASE_URL = CHAT_CONFIG["base_url"]
TOKEN = CHAT_CONFIG["token"]

def get_seller_prompts() -> List[Dict]:
    """获取卖瓜人的对话提示"""
    return [
        {"role": "user", "content": "请你扮演华强买瓜中的卖瓜人，我会扮演买瓜人。开始对话吧。"},
        {"role": "user", "content": "你瓜多少钱一斤"},
        {"role": "user", "content": "卧槽...这瓜皮子是金子做的，还是瓜栗子金子做的？"},
        {"role": "user", "content": "给我挑一个"},
        {"role": "user", "content": "这瓜保熟吗"},
        {"role": "user", "content": "我问你这瓜保熟吗？"},
        {"role": "user", "content": "你这瓜要熟我肯定要啊；....那它要是不熟怎么办啊"},
        {"role": "user", "content": "你这哪够十五斤呢你这秤有问题啊"},
        {"role": "user", "content": "吸铁石，另外你说的这瓜儿生的你自己吞进去"}
    ]

def generate_seller_conversation(client: ChatClient) -> List[Dict]:
    """生成卖瓜人的对话"""
    conversation = []
    prompts = get_seller_prompts()
    
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
    
    # 生成卖瓜人对话
    conversation = generate_seller_conversation(client)
    
    # 保存对话
    save_conversation(conversation, "华强买瓜_卖瓜人.json")

if __name__ == "__main__":
    main() 