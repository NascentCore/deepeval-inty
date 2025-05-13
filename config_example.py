# 聊天服务配置
CHAT_CONFIG = {
    "base_url": "http://inty.llm.sxwl.ai:30005",
    "token": "eyJhbG..."  # 请替换为实际的token
}

# 评估模型配置
EVAL_MODEL_CONFIG = {
    "base_url": "", 
    "api_key": "",
    "model": "",
    "chatbot_role": "你是一个智能助手，能够理解用户需求并提供准确、相关的回答"
}

# 评估指标配置
METRICS_CONFIG = {
    "hallucination_threshold": 0.3,
    "answer_relevancy_threshold": 0.5
} 