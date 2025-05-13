# Chat 应用评测程序

这是一个使用 DeepEval 框架开发的聊天应用评测程序。

## 安装

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 创建 `.env` 文件并添加以下内容：
```
CHAT_TOKEN=your_token_here
```

## 运行测试

```bash
python test_chat.py
```

## 测试内容

当前测试用例包括：
- 天气查询测试：测试系统对天气相关问题的回答准确性

## 评估指标

- HallucinationMetric：检测回答中是否存在幻觉（阈值：0.3）
- AnswerRelevancyMetric：评估回答的相关性（阈值：0.5） 