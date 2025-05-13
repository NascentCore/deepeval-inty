# DeepEval 对话评测工具

这是一个基于 DeepEval 框架的对话评测工具，用于评估大语言模型对话的质量。该工具可以从 API 获取最近的对话消息或从 JSON 文件中读取对话内容，并使用多种评估指标进行全面评测。

## 功能特点

- 支持从 API 获取最近的对话消息进行评测
- 支持从 JSON 文件读取对话内容进行评测
- 使用多种评测指标：

  - 对话相关性：评估回复与上下文的相关性,计算如何下
    $$
    Conversation Relevancy= \frac{Number of Turns of Relevant Actual Outputs}{Total Number of Turns}
    $$
    先为每个轮次构建一个轮次滑动窗口，然后使用 LLM 确定每个滑动窗口中的最后一个轮次是否具有与输入相关的 actual_output，具体取决于在滑动窗口中找到的上一个对话上下文。
  - 对话完整性：评估是否满足用户意图，使用大模型提取对话中用户的意图数量，使用大模型提取对话中满足了用户的意图数量,计算方式如下
    $$
    Conversation Completeness = \frac{Number of Satisfied User Intentions in Conversation}{Total number of User Intention Conversation}
    $$
    总用户意图和被满足的用户意图数均通过 judge model 提取
  - 角色一致性：评估是否始终扮演设定角色,计算方式如下
    $$
    Role Adherence = \frac{Numbers of Turns that Adhered to Chatbot role in converation}{Total number of Turns}
    $$
  - 知识保持：评估是否重复询问已给出信息，计算方式如下
    $$
    Knowledge Retention = \frac{Numbers of Turns without Knowledge Attritions}{Total number of Turns}
    $$

## 使用方法

### 配置

使用前需要在`config.py`中配置以下参数：

```python
CHAT_CONFIG = {
    "base_url": "你的聊天API基础URL",
    "token": "你的聊天API访问令牌"
}

EVAL_MODEL_CONFIG = {
    "base_url": "评估模型API基础URL",
    "api_key": "评估模型API密钥",
    "model": "评估使用的模型名称",
    "chatbot_role": "被评测的聊天机器人角色描述"
}
```

### 命令行使用

#### 评测最近的对话消息

```bash
python test_chat.py recent [-n 消息数量]
```

选项：

- `-n, --num`：要评测的最近消息数量，默认为 20 条

#### 从 JSON 文件评测对话

```bash
python test_chat.py file <json文件路径>
```

参数：

- `file_path`：对话 JSON 文件路径

### JSON 文件格式

JSON 文件需要包含以下格式的对话内容：

```json
[
    {"role": "user", "content": "用户消息1"},
    {"role": "assistant", "content": "助手回复1"},
    {"role": "user", "content": "用户消息2"},
    {"role": "assistant", "content": "助手回复2"},
    ...
]
```

其中：

- `role`：消息角色，可以是`user`或`assistant`
- `content`：消息内容

## 示例

```bash
# 评测最近10条消息
python test_chat.py recent -n 10

# 从文件评测对话
python test_chat.py file conversations/sample_conversation.json

# 不带参数默认评测示例文件
python test_chat.py
```

## 依赖项

- deepeval
- langchain
- requests
- argparse

## 项目结构

- `test_chat.py`: 主要的测试和评估逻辑
- `chat_client.py`: 聊天客户端实现
- `config.py`: 配置文件
- `requirements.txt`: 项目依赖

## 注意事项

- 确保在运行测试前正确配置所有必要的环境变量和 API 密钥
- 评估结果会以百分比形式显示各个指标的得分
- 可以根据需要调整评估指标和阈值

## 测试内容

当前测试用例包括：

- 所配置的 token 对应的 inty 用户的最近 20 轮对话内容评估

## 实测结果

![image](https://github.com/user-attachments/assets/71b00d2f-e11e-4777-8fcb-d927c4d22c52)
