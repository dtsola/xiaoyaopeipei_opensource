"""
LLM客户端 - 基于LangChain和通义千问
"""
from typing import Optional, List, Dict, Any
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """LLM客户端单例类"""

    _instance: Optional["LLMClient"] = None
    _chat_model: Optional[ChatTongyi] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化LLM客户端（懒加载）"""
        self._chat_model = None

    @property
    def chat_model(self) -> ChatTongyi:
        """获取Chat模型"""
        if self._chat_model is None:
            self._chat_model = ChatTongyi(
                dashscope_api_key=settings.QWEN_API_KEY,
                model_name=settings.QWEN_MODEL,
                temperature=settings.QWEN_TEMPERATURE,
                max_tokens=settings.QWEN_MAX_TOKENS,
                streaming=False,
            )
            logger.info(f"LLM客户端初始化成功: {settings.QWEN_MODEL}")
        return self._chat_model

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        发送聊天请求

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            AI响应文本
        """
        try:
            # 转换消息格式
            lc_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    lc_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))

            # 调用模型
            if temperature is not None or max_tokens is not None:
                model = ChatTongyi(
                    dashscope_api_key=settings.QWEN_API_KEY,
                    model_name=settings.QWEN_MODEL,
                    temperature=temperature or settings.QWEN_TEMPERATURE,
                    max_tokens=max_tokens or settings.QWEN_MAX_TOKENS,
                )
                response = model.invoke(lc_messages)
            else:
                response = self.chat_model.invoke(lc_messages)

            return response.content

        except Exception as e:
            logger.error(f"LLM请求失败: {e}")
            raise

    def chat_with_structured_output(
        self,
        messages: List[Dict[str, str]],
        output_schema: Dict[str, Any],
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回结构化输出

        Args:
            messages: 消息列表
            output_schema: 输出JSON Schema
            temperature: 温度参数

        Returns:
            结构化输出字典
        """
        try:
            # 添加JSON格式要求到system消息
            system_prompt = (
                messages[0]["content"]
                if messages and messages[0]["role"] == "system"
                else ""
            )
            system_prompt += "\n\n请严格按照JSON格式返回结果，不要包含其他任何文字。"

            if messages and messages[0]["role"] == "system":
                messages[0]["content"] = system_prompt
            else:
                messages.insert(0, {"role": "system", "content": system_prompt})

            # 调用模型
            response_text = self.chat(messages=messages, temperature=temperature)

            # 打印原始响应用于调试
            logger.info(f"[DEBUG] 通义千问原始响应: {response_text[:500]}...")

            # 解析JSON响应
            import json

            # 尝试提取JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # 尝试解析JSON
            result = json.loads(response_text)

            logger.debug(f"结构化输出: {result}")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败，原始响应: {response_text[:200]}..., error: {e}")
            # 返回None让调用方知道解析失败
            return None
        except Exception as e:
            logger.error(f"结构化输出请求失败: {e}")
            # 返回None让调用方知道解析失败
            return None

    def chat_with_history(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        基于历史记录的对话

        Args:
            user_message: 用户消息
            history: 对话历史 [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词
            temperature: 温度参数

        Returns:
            AI响应文本
        """
        messages = []

        # 添加系统提示
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 添加历史消息
        messages.extend(history)

        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})

        return self.chat(messages=messages, temperature=temperature)


# 创建全局实例
llm_client = LLMClient()


def get_llm_client() -> LLMClient:
    """
    获取LLM客户端实例

    Returns:
        LLM客户端单例
    """
    return llm_client
