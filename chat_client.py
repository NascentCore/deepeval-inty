import json
import requests
from typing import List, Dict

class ChatClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            'Accept': 'text/event-stream',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def get_history(self) -> List[Dict]:
        """获取聊天历史记录"""
        response = requests.get(
            f"{self.base_url}/api/v1/chat/history",
            headers=self.headers,
            verify=False
        )
        if response.status_code == 200:
            result = response.json()
            if result["code"] == 200:
                return result["data"]
        return []
    
    def get_recent_messages(self, n: int = 1) -> List[Dict]:
        """获取最近的n条消息（排除inner_voice类型）
        
        返回格式：
        [
            {
                "role": "user" | "assistant",
                "content": str
            },
            ...
        ]
        """
        history = self.get_history()
        valid_messages = []
        
        # 从尾部开始遍历，收集非inner_voice的消息
        for message in reversed(history):
            if message["role"] != "inner_voice":
                # 确保返回标准的消息格式
                valid_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
                if len(valid_messages) >= n:
                    break
        
        # 反转列表，使其按时间顺序排列
        return list(reversed(valid_messages))
    
    def chat(self, message: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/v1/chat",
            headers=self.headers,
            json={"message": message, "stream": True},
            verify=False,
            stream=True
        )
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        if 'content' in data:
                            full_response += data['content']
                    except json.JSONDecodeError:
                        continue
        
        return full_response
    
