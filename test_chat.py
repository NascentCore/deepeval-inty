from deepeval import assert_test, evaluate
from deepeval.test_case import ConversationalTestCase, LLMTestCase
from deepeval.metrics import (
    ConversationRelevancyMetric,
    ConversationCompletenessMetric,
    RoleAdherenceMetric,
    KnowledgeRetentionMetric
)
from deepeval.models.base_model import DeepEvalBaseLLM
from config import CHAT_CONFIG, EVAL_MODEL_CONFIG
from chat_client import ChatClient
import requests
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import asyncio
import argparse  # 导入argparse库
from deepeval.dataset import EvaluationDataset

class CustomEvalModel(DeepEvalBaseLLM):
    def __init__(self, base_url: str, api_key: str, model: str):
        super().__init__(model_name=model)
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.chat_model = ChatOpenAI(
            openai_api_base=base_url,
            openai_api_key=api_key,
            model_name=model,
            temperature=0
        )
        
    def load_model(self):
        # 这里不需要实际加载模型，因为我们使用API调用
        pass
        
    def _call(self, prompt: str) -> str:
        """实现实际的API调用"""
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            print(f"API调用异常: {str(e)}")
            return ""
        
    def generate(self, prompt: str) -> str:
        return self._call(prompt)
        
    async def a_generate(self, prompt: str) -> str:
        """异步生成方法"""
        try:
            messages = [HumanMessage(content=prompt)]
            response = await self.chat_model.ainvoke(messages)
            return response.content
        except Exception as e:
            print(f"异步API调用异常: {str(e)}")
            return ""
            
    def get_model_name(self) -> str:
        """返回模型名称"""
        return self.model

def build_turns_from_irregular_history(messages: list) -> list[LLMTestCase]:
    """从不规则的历史消息中构建对话轮次"""
    turns = []
    i = 0
    while i < len(messages):
        if messages[i]["role"] == "user":
            # 找接下来的第一个 assistant 回复作为配对
            j = i + 1
            while j < len(messages) and messages[j]["role"] != "assistant":
                j += 1
            if j < len(messages):  # 找到了配对
                turns.append(LLMTestCase(
                    input=messages[i]["content"],
                    actual_output=messages[j]["content"]
                ))
                i = j + 1
            else:
                break  # 后面没有 assistant 回复了
        else:
            i += 1
    return turns

def evaluate_conversation(messages: list, source_description: str = "对话"):
    """评估对话质量
    
    Args:
        messages: 对话消息列表，格式为[{"role": "user/assistant", "content": "消息内容"}, ...]
        source_description: 数据源描述，用于显示
        
    Returns:
        dict: 评测结果，包含四个指标的得分
    """
    # 初始化评估模型
    eval_model = CustomEvalModel(
        base_url=EVAL_MODEL_CONFIG["base_url"],
        api_key=EVAL_MODEL_CONFIG["api_key"],
        model=EVAL_MODEL_CONFIG["model"]
    )
    
    # 构建对话轮次
    turns = build_turns_from_irregular_history(messages)
    
    if not turns:
        print("没有找到有效的对话轮次，请检查消息格式")
        return {}
    
    # 构造 ConversationalTestCase
    convo = ConversationalTestCase(
        chatbot_role=EVAL_MODEL_CONFIG["chatbot_role"],
        turns=turns
    )
    
    # 使用四个指标进行评估
    metrics = [
        ConversationRelevancyMetric(model=eval_model,verbose_mode=True),      # 评估回复与上下文的相关性
        ConversationCompletenessMetric(model=eval_model,verbose_mode=True),   # 评估是否满足用户意图
        RoleAdherenceMetric(model=eval_model,verbose_mode=True),              # 评估是否始终扮演设定角色
        KnowledgeRetentionMetric(model=eval_model,verbose_mode=True)          # 评估是否重复询问已给出信息
    ]
    
    # 运行评估并打印结果
    print(f"🧪 {source_description}的评估结果:")
    print(f"共 {len(turns)} 个对话轮次")
    
    metric_names = {
        ConversationRelevancyMetric: "对话相关性",
        ConversationCompletenessMetric: "对话完整性",
        RoleAdherenceMetric: "角色一致性",
        KnowledgeRetentionMetric: "知识保持"
    }
    
    datasets = EvaluationDataset(test_cases=[convo])
    results = evaluate(datasets,metrics)


    # results = {}
    # for metric in metrics:
    #     metric.measure(convo)
    #     metric_type = type(metric)
    #     metric_name = metric_names.get(metric_type, metric_type.__name__)
    #     score = metric.score
    #     results[metric_name] = score
    #     print(f"{metric_name}: {score:.2%}")
        
    return results

def test_recent_messages(n_messages: int = 1):
    """测试最近的n条消息
    
    将最近的n条非inner_voice消息作为一个完整对话来评测
    """
    # 初始化聊天客户端
    client = ChatClient(
        base_url=CHAT_CONFIG["base_url"],
        token=CHAT_CONFIG["token"]
    )
    
    # 获取最近的消息
    messages = client.get_recent_messages(n_messages)
    
    # 评估对话
    return evaluate_conversation(messages, f"最近{n_messages}条消息")

def test_from_json_file(file_path: str):
    """从JSON文件中读取对话并进行评测
    
    JSON文件格式要求:
    [
        {"role": "user", "content": "用户消息1"},
        {"role": "assistant", "content": "助手回复1"},
        ...
    ]
    
    Args:
        file_path: JSON文件路径
    """
    # 读取JSON文件
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    except Exception as e:
        print(f"读取JSON文件失败: {str(e)}")
        return {}
    
    # 评估对话
    return evaluate_conversation(messages, f"文件 {file_path}")

if __name__ == "__main__":
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='大模型对话评测工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 添加评测最近消息的子命令
    recent_parser = subparsers.add_parser('recent', help='评测最近的对话消息')
    recent_parser.add_argument('-n', '--num', type=int, default=20, help='要评测的最近消息数量')
    
    # 添加从文件评测的子命令
    file_parser = subparsers.add_parser('file', help='从JSON文件评测对话')
    file_parser.add_argument('file_path', help='对话JSON文件路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 根据子命令执行对应功能
    if args.command == 'recent':
        test_recent_messages(args.num)
    elif args.command == 'file':
        test_from_json_file(args.file_path)
    else:
        # 默认评测示例文件
        test_from_json_file("conversations/sample_conversation.json")