# Chat 应用评测程序

这是一个使用 DeepEval 框架开发的聊天应用评测程序，用于评估聊天机器人的回复质量。

## 功能特点

- 支持对聊天历史进行批量评估
- 使用多个维度评估回复质量
- 支持自定义评估模型和指标
- 异步处理能力

## 安装

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 配置 `config.py` 文件：
- `CHAT_CONFIG`: 聊天服务配置
  - `base_url`: 聊天服务的基础URL
  - `token`: 访问令牌
- `EVAL_MODEL_CONFIG`: 评估模型配置
  - `base_url`: 评估模型API的基础URL
  - `api_key`: API密钥
  - `model`: 使用的模型名称
  - `chatbot_role`: 聊天机器人的角色定义

## 运行测试

```bash
python test_chat.py
```

## 评估指标

程序使用以下指标评估聊天质量：

1. 对话相关性 (ConversationRelevancyMetric)
   - 评估回复与上下文的相关程度
   - 确保回答与用户问题紧密相关

2. 对话完整性 (ConversationCompletenessMetric)
   - 评估回复是否完整满足用户意图
   - 检查是否提供了足够的信息

3. 角色一致性 (RoleAdherenceMetric)
   - 评估回复是否始终符合设定的角色
   - 确保回答风格的一致性

4. 知识保持 (KnowledgeRetentionMetric)
   - 评估是否避免重复询问已提供的信息
   - 确保对话的连贯性

## 项目结构

- `test_chat.py`: 主要的测试和评估逻辑
- `chat_client.py`: 聊天客户端实现
- `config.py`: 配置文件
- `requirements.txt`: 项目依赖

## 注意事项

- 确保在运行测试前正确配置所有必要的环境变量和API密钥
- 评估结果会以百分比形式显示各个指标的得分
- 可以根据需要调整评估指标和阈值

## 测试内容

当前测试用例包括：
- 所配置的token对应的inty用户的最近20轮对话内容评估
